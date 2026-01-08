#!/usr/bin/env python3
"""
Process GitHub issue form for batch hierarchy reorganization.
Moves multiple structures to a new parent, optionally creating the parent first.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Optional


def parse_issue_body(body: str) -> dict:
    """Parse the structured issue body into a dictionary."""
    data = {}
    
    sections = re.split(r'###\s+', body)
    
    for section in sections[1:]:
        lines = section.strip().split('\n')
        if not lines:
            continue
            
        label = lines[0].strip()
        content_lines = [l for l in lines[1:] if l.strip() and not l.startswith('- [')]
        content = '\n'.join(content_lines).strip()
        
        key = label.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_').replace('?', '')
        
        if content and content != '_No response_':
            data[key] = content
    
    return data


def load_all_structures(structures_dir: Path) -> dict:
    """Load all structures from all YAML files."""
    structures = {}
    file_map = {}  # id -> filepath
    
    for yaml_file in structures_dir.glob('*.yaml'):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
            if data and 'structures' in data:
                for struct in data['structures']:
                    if 'id' in struct:
                        structures[struct['id']] = struct
                        file_map[struct['id']] = yaml_file
    
    return structures, file_map


def find_structure_by_name(structures: dict, name: str) -> Optional[str]:
    """Find structure ID by name (case-insensitive)."""
    name_lower = name.lower().strip()
    for struct_id, struct in structures.items():
        if struct.get('name', '').lower() == name_lower:
            return struct_id
    return None


def get_next_id(structures: dict) -> str:
    """Generate the next available BAP ID."""
    max_id = 0
    for struct_id in structures:
        if struct_id.startswith('BAP_'):
            try:
                num = int(struct_id.split('_')[1])
                max_id = max(max_id, num)
            except (ValueError, IndexError):
                pass
    return f"BAP_{max_id + 1:07d}"


def add_structure_to_file(filepath: Path, new_struct: dict):
    """Add a new structure to a YAML file."""
    with open(filepath) as f:
        data = yaml.safe_load(f) or {'structures': []}
    
    if 'structures' not in data:
        data['structures'] = []
    
    data['structures'].append(new_struct)
    
    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def update_structure_parent(filepath: Path, struct_id: str, new_parent_id: str):
    """Update the parent of a structure in a YAML file."""
    with open(filepath) as f:
        data = yaml.safe_load(f)
    
    for struct in data.get('structures', []):
        if struct.get('id') == struct_id:
            struct['parent'] = new_parent_id
            break
    
    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def main():
    issue_body = os.environ.get('ISSUE_BODY', '')
    issue_number = os.environ.get('ISSUE_NUMBER', 'unknown')
    
    if not issue_body:
        print("No issue body found")
        return
    
    data = parse_issue_body(issue_body)
    print(f"Parsed data: {data}")
    
    structures_dir = Path('structures')
    
    # Load all structures
    structures, file_map = load_all_structures(structures_dir)
    
    # Parse fields
    structures_to_move = data.get('structures_to_move', '').strip().split('\n')
    structures_to_move = [s.strip() for s in structures_to_move if s.strip()]
    
    new_parent_name = data.get('new_parent_structure', '').strip()
    # Check various possible key names for "create parent"
    create_parent_value = (
        data.get('does_the_new_parent_need_to_be_created', '') or
        data.get('does_the_new_parent_need_to_be_created?', '') or
        ''
    )
    create_parent = 'yes' in create_parent_value.lower()
    parent_of_new_parent = data.get('parent_of_new_parent_if_creating', '').strip()
    new_parent_definition = data.get('definition_for_new_parent_if_creating', '').strip()
    region = data.get('body_region', 'Head')
    
    if not structures_to_move or not new_parent_name:
        print("Missing required fields")
        return
    
    # Find or create the new parent
    new_parent_id = find_structure_by_name(structures, new_parent_name)
    
    if not new_parent_id and create_parent:
        # Need to create the new parent first
        parent_parent_id = find_structure_by_name(structures, parent_of_new_parent)
        
        if not parent_parent_id:
            print(f"Error: Parent '{parent_of_new_parent}' not found")
            return
        
        new_parent_id = get_next_id(structures)
        new_parent_struct = {
            'id': new_parent_id,
            'name': new_parent_name,
            'parent': parent_parent_id,
        }
        if new_parent_definition:
            new_parent_struct['definition'] = new_parent_definition
        
        # Add to body_regions.yaml (or appropriate file based on region)
        target_file = structures_dir / 'body_regions.yaml'
        add_structure_to_file(target_file, new_parent_struct)
        print(f"✓ Created new parent: {new_parent_name} ({new_parent_id})")
        
        # Update our local structures dict
        structures[new_parent_id] = new_parent_struct
        file_map[new_parent_id] = target_file
    
    elif not new_parent_id:
        print(f"Error: Parent '{new_parent_name}' not found and 'create parent' was not selected")
        return
    
    # Move all the structures
    moved = []
    errors = []
    
    for struct_name in structures_to_move:
        struct_id = find_structure_by_name(structures, struct_name)
        
        if not struct_id:
            errors.append(f"Structure not found: {struct_name}")
            continue
        
        filepath = file_map.get(struct_id)
        if not filepath:
            errors.append(f"File not found for: {struct_name}")
            continue
        
        old_parent = structures[struct_id].get('parent', 'None')
        update_structure_parent(filepath, struct_id, new_parent_id)
        moved.append(f"{struct_name}: {old_parent} → {new_parent_id}")
        print(f"✓ Moved {struct_name} to {new_parent_name}")
    
    # Write summary
    with open('REORG_SUMMARY.md', 'w') as f:
        f.write(f"# Batch Reorganization Summary\n\n")
        f.write(f"**New Parent**: {new_parent_name} ({new_parent_id})\n\n")
        
        f.write(f"## Moved Structures ({len(moved)})\n\n")
        for m in moved:
            f.write(f"- ✓ {m}\n")
        
        if errors:
            f.write(f"\n## Errors ({len(errors)})\n\n")
            for e in errors:
                f.write(f"- ❌ {e}\n")
    
    print(f"\nSummary: Moved {len(moved)} structures, {len(errors)} errors")


if __name__ == '__main__':
    main()
