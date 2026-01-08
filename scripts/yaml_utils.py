#!/usr/bin/env python3
"""
YAML utilities that preserve formatting when modifying files.
Uses ruamel.yaml to maintain comments, ordering, and style.
"""

from pathlib import Path
from typing import Any, Optional
from ruamel.yaml import YAML


def get_yaml() -> YAML:
    """Get a configured YAML instance that preserves formatting."""
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 120
    yaml.indent(mapping=2, sequence=2, offset=2)
    return yaml


def load_yaml(filepath: Path) -> dict:
    """Load a YAML file preserving formatting info."""
    yaml = get_yaml()
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.load(f) or {}


def save_yaml(filepath: Path, data: dict):
    """Save data to YAML file preserving formatting."""
    yaml = get_yaml()
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)


def add_structure(filepath: Path, new_struct: dict):
    """Add a structure to a YAML file, preserving formatting."""
    data = load_yaml(filepath)
    
    if 'structures' not in data:
        data['structures'] = []
    
    data['structures'].append(new_struct)
    save_yaml(filepath, data)


def remove_structure_by_index(filepath: Path, index: int) -> Optional[dict]:
    """Remove a structure by index, preserving formatting."""
    data = load_yaml(filepath)
    
    if 'structures' not in data or index >= len(data['structures']):
        return None
    
    removed = data['structures'].pop(index)
    save_yaml(filepath, data)
    return dict(removed)  # Convert from ruamel type


def update_structure_parent(filepath: Path, struct_id: str, new_parent_id: str):
    """Update the parent of a structure, preserving formatting."""
    data = load_yaml(filepath)
    
    for struct in data.get('structures', []):
        if struct.get('id') == struct_id:
            struct['parent'] = new_parent_id
            break
    
    save_yaml(filepath, data)


def add_relationship(filepath: Path, new_rel: dict):
    """Add a relationship to a YAML file, preserving formatting."""
    data = load_yaml(filepath)
    
    if 'relationships' not in data or data['relationships'] is None:
        data['relationships'] = []
    
    data['relationships'].append(new_rel)
    save_yaml(filepath, data)


def remove_relationships_by_structure(filepath: Path, structure_id: str) -> int:
    """Remove all relationships involving a structure. Returns count removed."""
    data = load_yaml(filepath)
    
    if 'relationships' not in data or not data['relationships']:
        return 0
    
    original_count = len(data['relationships'])
    data['relationships'] = [
        rel for rel in data['relationships']
        if rel.get('subject') != structure_id and rel.get('object') != structure_id
    ]
    removed_count = original_count - len(data['relationships'])
    
    if removed_count > 0:
        save_yaml(filepath, data)
    
    return removed_count


def deprecate_structure(filepath: Path, index: int, reason: str):
    """Mark a structure as deprecated, preserving formatting."""
    from datetime import datetime
    
    data = load_yaml(filepath)
    
    if 'structures' in data and index < len(data['structures']):
        data['structures'][index]['deprecated'] = True
        data['structures'][index]['deprecated_date'] = datetime.now().strftime('%Y-%m-%d')
        data['structures'][index]['deprecation_reason'] = reason
        save_yaml(filepath, data)
