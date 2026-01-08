#!/usr/bin/env python3
"""
Process GitHub issue form for removing/deprecating a structure.
Handles removal, deprecation, and merge operations.
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from yaml_utils import (
        load_yaml, save_yaml, remove_structure_by_index, 
        deprecate_structure, remove_relationships_by_structure, update_structure_parent
    )
    USE_RUAMEL = True
except ImportError:
    import yaml
    USE_RUAMEL = False


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
        
        key = label.lower().replace(' ', '_').replace('(', '').replace(')', '')
        
        if content and content != '_No response_':
            data[key] = content
    
    return data


def _load_yaml_file(filepath: Path) -> dict:
    """Load YAML file using appropriate library."""
    if USE_RUAMEL:
        return load_yaml(filepath)
    else:
        with open(filepath) as f:
            return yaml.safe_load(f) or {}


def _save_yaml_file(filepath: Path, data: dict):
    """Save YAML file using appropriate library."""
    if USE_RUAMEL:
        save_yaml(filepath, data)
    else:
        with open(filepath, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def find_structure_in_files(structures_dir: Path, name: str) -> tuple[Path | None, dict | None, int | None]:
    """Find a structure by name, return (file_path, structure_dict, index)."""
    for yaml_file in structures_dir.glob('*.yaml'):
        data = _load_yaml_file(yaml_file)
        if data and 'structures' in data:
            for i, struct in enumerate(data['structures']):
                if struct.get('name', '').lower() == name.lower():
                    return yaml_file, dict(struct), i
    return None, None, None


def find_children(structures_dir: Path, parent_id: str) -> list[dict]:
    """Find all structures that have this as parent."""
    children = []
    for yaml_file in structures_dir.glob('*.yaml'):
        data = _load_yaml_file(yaml_file)
        if data and 'structures' in data:
            for struct in data['structures']:
                if struct.get('parent') == parent_id:
                    children.append(dict(struct))
    return children


def find_relationships(relationships_dir: Path, structure_id: str) -> list[tuple[Path, dict]]:
    """Find all relationships involving this structure."""
    found = []
    for yaml_file in relationships_dir.glob('*.yaml'):
        data = _load_yaml_file(yaml_file)
        if data and 'relationships' in data and data['relationships']:
            for rel in data['relationships']:
                if rel.get('subject') == structure_id or rel.get('object') == structure_id:
                    found.append((yaml_file, dict(rel)))
    return found


def do_deprecate_structure(file_path: Path, index: int, reason: str):
    """Mark a structure as deprecated instead of removing."""
    if USE_RUAMEL:
        deprecate_structure(file_path, index, reason)
    else:
        data = _load_yaml_file(file_path)
        data['structures'][index]['deprecated'] = True
        data['structures'][index]['deprecated_date'] = datetime.now().strftime('%Y-%m-%d')
        data['structures'][index]['deprecation_reason'] = reason
        _save_yaml_file(file_path, data)


def remove_structure(file_path: Path, index: int):
    """Remove a structure from the YAML file."""
    if USE_RUAMEL:
        return remove_structure_by_index(file_path, index)
    else:
        data = _load_yaml_file(file_path)
        removed = data['structures'].pop(index)
        _save_yaml_file(file_path, data)
        return removed


def merge_structures(structures_dir: Path, relationships_dir: Path, 
                     source_file: Path, source_index: int, source_struct: dict,
                     target_name: str):
    """Merge source structure into target, transferring relationships."""
    # Find target
    target_file, target_struct, target_index = find_structure_in_files(structures_dir, target_name)
    
    if not target_struct:
        print(f"Error: Merge target '{target_name}' not found")
        return False
    
    source_id = source_struct.get('id')
    target_id = target_struct.get('id')
    
    # Update all relationships pointing to source to point to target
    for yaml_file in relationships_dir.glob('*.yaml'):
        data = _load_yaml_file(yaml_file)
        
        if data and 'relationships' in data and data['relationships']:
            modified = False
            for rel in data['relationships']:
                if rel.get('subject') == source_id:
                    rel['subject'] = target_id
                    rel['merged_from'] = source_id
                    modified = True
                if rel.get('object') == source_id:
                    rel['object'] = target_id
                    rel['merged_from'] = source_id
                    modified = True
            
            if modified:
                _save_yaml_file(yaml_file, data)
    
    # Update children to point to new parent
    for yaml_file in structures_dir.glob('*.yaml'):
        data = _load_yaml_file(yaml_file)
        
        if data and 'structures' in data:
            modified = False
            for struct in data['structures']:
                if struct.get('parent') == source_id:
                    struct['parent'] = target_id
                    modified = True
            
            if modified:
                _save_yaml_file(yaml_file, data)
    
    # Remove the source structure
    remove_structure(source_file, source_index)
    
    return True


def remove_relationship_from_file(filepath: Path, structure_id: str):
    """Remove all relationships involving a structure from a YAML file."""
    if USE_RUAMEL:
        removed = remove_relationships_by_structure(filepath, structure_id)
        if removed > 0:
            print(f"  Removed {removed} relationships from {filepath.name}")
        return
    
    data = _load_yaml_file(filepath)
    
    if data and 'relationships' in data and data['relationships']:
        original_count = len(data['relationships'])
        data['relationships'] = [
            rel for rel in data['relationships']
            if rel.get('subject') != structure_id and rel.get('object') != structure_id
        ]
        removed_count = original_count - len(data['relationships'])
        
        if removed_count > 0:
            _save_yaml_file(filepath, data)
            print(f"  Removed {removed_count} relationships from {filepath.name}")


def main():
    issue_body = os.environ.get('ISSUE_BODY', '')
    issue_number = os.environ.get('ISSUE_NUMBER', 'unknown')
    
    if not issue_body:
        print("No issue body found")
        return
    
    data = parse_issue_body(issue_body)
    print(f"Parsed data: {data}")
    
    structures_dir = Path('structures')
    relationships_dir = Path('relationships')
    
    # Get fields
    structure_name = data.get('structure_to_remove', '')
    action = data.get('action_type', '').split(' ')[0]  # "deprecate (mark...)" -> "deprecate"
    merge_target = data.get('merge_into_if_merging', '')
    reason = data.get('reason_for_removal', '')
    justification = data.get('detailed_justification', '')
    
    if not structure_name:
        print("No structure name provided")
        return
    
    # Find the structure
    file_path, struct, index = find_structure_in_files(structures_dir, structure_name)
    
    if not struct:
        print(f"Error: Structure '{structure_name}' not found")
        return
    
    structure_id = struct.get('id')
    
    # Check for dependencies
    children = find_children(structures_dir, structure_id)
    relationships = find_relationships(relationships_dir, structure_id)
    
    # Write impact report
    with open('REMOVAL_IMPACT.md', 'w') as f:
        f.write(f"# Removal Impact Report\n\n")
        f.write(f"**Structure**: {structure_name} ({structure_id})\n")
        f.write(f"**Action**: {action}\n")
        f.write(f"**Reason**: {reason}\n\n")
        
        if children:
            f.write(f"## Affected Children ({len(children)})\n\n")
            for child in children:
                f.write(f"- {child.get('name')} ({child.get('id')})\n")
            f.write("\n")
        
        if relationships:
            f.write(f"## Affected Relationships ({len(relationships)})\n\n")
            for rel_file, rel in relationships:
                f.write(f"- {rel.get('subject')} --{rel.get('predicate')}--> {rel.get('object')}\n")
            f.write("\n")
    
    # Perform the action
    if action == 'deprecate':
        do_deprecate_structure(file_path, index, f"{reason}: {justification}")
        print(f"Deprecated structure '{structure_name}'")
        
    elif action == 'remove':
        if children:
            print(f"Warning: Structure has {len(children)} children that will be orphaned!")
        
        # Remove relationships that reference this structure
        if relationships:
            print(f"Removing {len(relationships)} relationships...")
            for rel_file, rel in relationships:
                remove_relationship_from_file(rel_file, structure_id)
        
        removed = remove_structure(file_path, index)
        print(f"Removed structure '{structure_name}'")
        
    elif action == 'merge':
        if not merge_target:
            print("Error: Merge action requires a target structure")
            return
        
        if merge_structures(structures_dir, relationships_dir, file_path, index, struct, merge_target):
            print(f"Merged '{structure_name}' into '{merge_target}'")
        else:
            print("Merge failed")


if __name__ == '__main__':
    main()
