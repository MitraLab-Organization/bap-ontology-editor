#!/usr/bin/env python3
"""
Create actual YAML changes from AI-parsed data when user approves.
"""

import os
import json
import sys
from pathlib import Path

# Try ruamel for format preservation, fall back to pyyaml
try:
    from ruamel.yaml import YAML
    def get_yaml():
        y = YAML()
        y.preserve_quotes = True
        y.width = 120
        return y
    USE_RUAMEL = True
except ImportError:
    import yaml
    USE_RUAMEL = False


def load_yaml_file(filepath: Path) -> dict:
    if USE_RUAMEL:
        y = get_yaml()
        with open(filepath) as f:
            return y.load(f) or {}
    else:
        with open(filepath) as f:
            return yaml.safe_load(f) or {}


def save_yaml_file(filepath: Path, data: dict):
    if USE_RUAMEL:
        y = get_yaml()
        with open(filepath, 'w') as f:
            y.dump(data, f)
    else:
        with open(filepath, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


def find_structure_id_by_name(name: str) -> str | None:
    """Find a structure's ID by its name."""
    structures_dir = Path('structures')
    
    for yaml_file in structures_dir.glob('*.yaml'):
        data = load_yaml_file(yaml_file)
        if data and 'structures' in data:
            for struct in data['structures']:
                if struct.get('name', '').lower() == name.lower():
                    return struct.get('id')
    return None


def add_structure(struct_data: dict):
    """Add a structure to body_regions.yaml."""
    filepath = Path('structures/body_regions.yaml')
    data = load_yaml_file(filepath)
    
    if 'structures' not in data:
        data['structures'] = []
    
    # Find parent ID
    parent_name = struct_data.get('parent_name', '')
    parent_id = find_structure_id_by_name(parent_name)
    
    if not parent_id:
        print(f"Warning: Parent '{parent_name}' not found, skipping structure")
        return False
    
    new_struct = {
        'id': struct_data['id'],
        'name': struct_data['name'],
        'parent': parent_id,
    }
    
    if struct_data.get('definition'):
        new_struct['definition'] = struct_data['definition']
    
    data['structures'].append(new_struct)
    save_yaml_file(filepath, data)
    print(f"✓ Added structure: {struct_data['name']} ({struct_data['id']})")
    return True


def add_relationship(rel_data: dict):
    """Add a relationship to the appropriate file."""
    predicate = rel_data.get('predicate', '')
    
    # Map predicate to file
    file_map = {
        'innervated_by': 'relationships/innervation.yaml',
        'supplied_by': 'relationships/blood_supply.yaml',
        'develops_from': 'relationships/developmental.yaml',
        'part_of': 'relationships/developmental.yaml',
        'adjacent_to': 'relationships/developmental.yaml',
    }
    
    filepath = Path(file_map.get(predicate, 'relationships/developmental.yaml'))
    
    if not filepath.exists():
        print(f"Warning: Relationship file {filepath} not found")
        return False
    
    data = load_yaml_file(filepath)
    
    if 'relationships' not in data or data['relationships'] is None:
        data['relationships'] = []
    
    # Find structure IDs
    subject_id = find_structure_id_by_name(rel_data.get('subject_name', ''))
    object_id = find_structure_id_by_name(rel_data.get('object_name', ''))
    
    if not subject_id:
        print(f"Warning: Subject '{rel_data.get('subject_name')}' not found")
        return False
    
    if not object_id:
        print(f"Warning: Object '{rel_data.get('object_name')}' not found")
        return False
    
    new_rel = {
        'subject': subject_id,
        'predicate': predicate,
        'object': object_id,
    }
    
    data['relationships'].append(new_rel)
    save_yaml_file(filepath, data)
    print(f"✓ Added relationship: {rel_data['subject_name']} {predicate} {rel_data['object_name']}")
    return True


def main():
    issue_number = os.environ.get('ISSUE_NUMBER', '')
    
    if not issue_number:
        print("No issue number provided")
        sys.exit(1)
    
    # Load the saved AI data
    data_file = Path(f'.ai_requests/issue_{issue_number}.json')
    
    if not data_file.exists():
        print(f"No AI data found for issue {issue_number}")
        sys.exit(1)
    
    with open(data_file) as f:
        parsed = json.load(f)
    
    print(f"Processing AI changes for issue #{issue_number}")
    
    # Add structures first
    structures = parsed.get('structures', [])
    for struct in structures:
        add_structure(struct)
    
    # Then add relationships
    relationships = parsed.get('relationships', [])
    for rel in relationships:
        add_relationship(rel)
    
    # Update README with new tree
    print("\nUpdating README...")
    os.system('python scripts/generate_tree.py --update-readme')
    
    print("\n✅ All changes applied!")


if __name__ == '__main__':
    main()
