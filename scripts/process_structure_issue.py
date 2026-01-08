#!/usr/bin/env python3
"""
Process GitHub issue form for adding a new structure.
Parses the issue body and generates the appropriate YAML entry.
"""

import os
import re
import yaml
from pathlib import Path


def parse_issue_body(body: str) -> dict:
    """Parse the structured issue body into a dictionary."""
    data = {}
    
    # Pattern matches "### Label\n\nValue" or "### Label\n\n- [x] checkbox"
    sections = re.split(r'###\s+', body)
    
    for section in sections[1:]:  # Skip first empty section
        lines = section.strip().split('\n')
        if not lines:
            continue
            
        label = lines[0].strip()
        # Get content after the label, skip empty lines
        content_lines = [l for l in lines[1:] if l.strip() and not l.startswith('- [')]
        content = '\n'.join(content_lines).strip()
        
        # Clean up the label for use as key
        key = label.lower().replace(' ', '_').replace('(', '').replace(')', '')
        
        if content and content != '_No response_':
            data[key] = content
    
    return data


def get_next_id(structures_dir: Path, region: str) -> str:
    """Generate the next available BAP ID."""
    max_id = 0
    
    for yaml_file in structures_dir.glob('*.yaml'):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
            if data and 'structures' in data:
                for struct in data['structures']:
                    if 'id' in struct and struct['id'].startswith('BAP_'):
                        try:
                            num = int(struct['id'].split('_')[1])
                            max_id = max(max_id, num)
                        except (ValueError, IndexError):
                            pass
    
    return f"BAP_{max_id + 1:07d}"


def find_parent_id(structures_dir: Path, parent_name: str) -> str | None:
    """Find the ID of a parent structure by name."""
    for yaml_file in structures_dir.glob('*.yaml'):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
            if data and 'structures' in data:
                for struct in data['structures']:
                    if struct.get('name', '').lower() == parent_name.lower():
                        return struct.get('id')
    return None


def determine_target_file(region: str, system: str) -> str:
    """Determine which YAML file this structure should be added to."""
    # Map system to file
    system_file_map = {
        'musculoskeletal system': {
            'muscles': 'muscles.yaml',
            'skeletal': 'skeletal.yaml',
        },
        'nervous system': 'nerves.yaml',
        'vascular system': 'vessels.yaml',
    }
    
    # For musculoskeletal, need to determine if muscle or bone
    # Default to body_regions for most things
    return 'body_regions.yaml'


def add_structure_to_yaml(file_path: Path, new_structure: dict):
    """Add a new structure to the YAML file."""
    with open(file_path) as f:
        data = yaml.safe_load(f) or {'structures': []}
    
    if 'structures' not in data:
        data['structures'] = []
    
    data['structures'].append(new_structure)
    
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def main():
    issue_body = os.environ.get('ISSUE_BODY', '')
    issue_number = os.environ.get('ISSUE_NUMBER', 'unknown')
    
    if not issue_body:
        print("No issue body found")
        return
    
    # Parse the issue
    data = parse_issue_body(issue_body)
    print(f"Parsed data: {data}")
    
    structures_dir = Path('structures')
    
    # Get required fields
    name = data.get('structure_name', '')
    region = data.get('body_region', '')
    system = data.get('organ_system', '')
    parent = data.get('parent_structure', '')
    definition = data.get('definition', '')
    
    if not all([name, region, parent]):
        print(f"Missing required fields. Got: name={name}, region={region}, parent={parent}")
        return
    
    # Generate new ID
    new_id = get_next_id(structures_dir, region)
    
    # Find parent ID
    parent_id = find_parent_id(structures_dir, parent)
    if not parent_id:
        print(f"Warning: Could not find parent '{parent}', using name as parent reference")
        parent_id = parent  # Fall back to name
    
    # Build the new structure entry
    new_structure = {
        'id': new_id,
        'name': name,
        'parent': parent_id,
    }
    
    if definition:
        new_structure['definition'] = definition
    
    if data.get('abbreviation_optional'):
        new_structure['abbreviation'] = data['abbreviation_optional']
    
    if data.get('external_id_optional'):
        new_structure['external_id'] = data['external_id_optional']
    
    # Add to appropriate file
    target_file = structures_dir / determine_target_file(region, system)
    add_structure_to_yaml(target_file, new_structure)
    
    print(f"Added structure '{name}' (ID: {new_id}) to {target_file}")
    
    # Also write a summary for the PR
    with open('CHANGE_SUMMARY.md', 'w') as f:
        f.write(f"# Structure Added\n\n")
        f.write(f"- **Name**: {name}\n")
        f.write(f"- **ID**: {new_id}\n")
        f.write(f"- **Parent**: {parent}\n")
        f.write(f"- **Region**: {region}\n")
        f.write(f"- **System**: {system}\n")
        if definition:
            f.write(f"- **Definition**: {definition}\n")


if __name__ == '__main__':
    main()
