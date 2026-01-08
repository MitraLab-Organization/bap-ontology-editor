#!/usr/bin/env python3
"""
Process GitHub issue form for adding a new relationship.
Parses the issue body and appends to the appropriate relationship YAML.
"""

import os
import re
import yaml
from pathlib import Path


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


def find_structure_id(structures_dir: Path, name: str) -> str | None:
    """Find the ID of a structure by name."""
    for yaml_file in structures_dir.glob('*.yaml'):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
            if data and 'structures' in data:
                for struct in data['structures']:
                    if struct.get('name', '').lower() == name.lower():
                        return struct.get('id')
    return None


def get_relationship_file(rel_type: str) -> str:
    """Map relationship type to filename."""
    type_map = {
        'innervated_by': 'innervation.yaml',
        'supplied_by': 'blood_supply.yaml',
        'develops_from': 'developmental.yaml',
        'part_of': 'developmental.yaml',  # Could be its own file
        'adjacent_to': 'developmental.yaml',
    }
    return type_map.get(rel_type.split(' ')[0], 'developmental.yaml')


def add_relationship_to_yaml(file_path: Path, new_rel: dict):
    """Add a new relationship to the YAML file."""
    if file_path.exists():
        with open(file_path) as f:
            data = yaml.safe_load(f) or {'relationships': []}
    else:
        data = {'relationships': []}
    
    if 'relationships' not in data or data['relationships'] is None:
        data['relationships'] = []
    
    data['relationships'].append(new_rel)
    
    with open(file_path, 'w') as f:
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
    relationships_dir = Path('relationships')
    
    # Get fields
    rel_type = data.get('relationship_type', '')
    subject = data.get('subject_structure', '')
    obj = data.get('object_structure', '')
    confidence = data.get('confidence_level', 'medium')
    references = data.get('references', '')
    notes = data.get('additional_notes', '')
    
    if not all([rel_type, subject, obj]):
        print(f"Missing required fields")
        return
    
    # Extract relationship type (before the parenthetical explanation)
    rel_type_clean = rel_type.split(' ')[0]
    
    # Find structure IDs
    subject_id = find_structure_id(structures_dir, subject)
    object_id = find_structure_id(structures_dir, obj)
    
    # Build relationship entry
    new_rel = {
        'subject': subject_id or subject,
        'predicate': rel_type_clean,
        'object': object_id or obj,
    }
    
    if confidence:
        conf_level = confidence.split(' ')[0]  # "high (well-established)" -> "high"
        new_rel['confidence'] = conf_level
    
    if references:
        new_rel['references'] = references
    
    if notes:
        new_rel['notes'] = notes
    
    # Add to appropriate file
    target_file = relationships_dir / get_relationship_file(rel_type_clean)
    add_relationship_to_yaml(target_file, new_rel)
    
    print(f"Added relationship: {subject} --{rel_type_clean}--> {obj}")


if __name__ == '__main__':
    main()
