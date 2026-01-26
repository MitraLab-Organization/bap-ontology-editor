#!/usr/bin/env python3
"""
Lateralize relationships to connect (L) structures to (L) nerves/vessels and (R) to (R).
"""

import sys
from pathlib import Path
from typing import Dict, List

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

from ai_context import load_all_structures


def load_yaml_file(filepath: Path) -> dict:
    """Load a YAML file."""
    if USE_RUAMEL:
        y = get_yaml()
        with open(filepath) as f:
            return y.load(f) or {}
    else:
        with open(filepath) as f:
            return yaml.safe_load(f) or {}


def save_yaml_file(filepath: Path, data: dict):
    """Save data to YAML file."""
    if USE_RUAMEL:
        y = get_yaml()
        with open(filepath, 'w') as f:
            y.dump(data, f)
    else:
        with open(filepath, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def find_lateralized_version(base_id: str, structures: Dict, side: str) -> str:
    """
    Find the (L) or (R) version of a structure.
    Returns the lateralized ID if found, None otherwise.
    """
    # Get the base structure name
    if base_id not in structures:
        return None
    
    base_name = structures[base_id].get('name', '')
    target_name = f"{base_name} ({side})"
    
    # Search for the lateralized version
    for struct_id, struct in structures.items():
        if struct.get('name') == target_name:
            return struct_id
    
    return None


def lateralize_relationships():
    """Lateralize all relationships."""
    print("=" * 70)
    print("RELATIONSHIP LATERALIZATION")
    print("=" * 70)
    print()
    
    # Load structures
    print("Loading structures...")
    structures = load_all_structures()
    print(f"  ✓ Loaded {len(structures)} structures")
    
    # Process each relationship file
    rel_dir = Path('relationships')
    
    for yaml_file in rel_dir.glob('*.yaml'):
        print(f"\nProcessing {yaml_file.name}...")
        data = load_yaml_file(yaml_file)
        
        if not data or 'relationships' not in data or not data['relationships']:
            print("  (no relationships)")
            continue
        
        original_rels = data['relationships'][:]
        new_rels = []
        kept_rels = []
        
        for rel in original_rels:
            subject_id = rel.get('subject')
            predicate = rel.get('predicate')
            object_id = rel.get('object')
            
            # Try to find (L) and (R) versions
            subject_L = find_lateralized_version(subject_id, structures, 'L')
            subject_R = find_lateralized_version(subject_id, structures, 'R')
            object_L = find_lateralized_version(object_id, structures, 'L')
            object_R = find_lateralized_version(object_id, structures, 'R')
            
            # If both sides have lateralized versions, create (L)→(L) and (R)→(R)
            if subject_L and object_L:
                new_rels.append({
                    'subject': subject_L,
                    'predicate': predicate,
                    'object': object_L
                })
                print(f"  + {structures[subject_L]['name']} → {structures[object_L]['name']}")
            
            if subject_R and object_R:
                new_rels.append({
                    'subject': subject_R,
                    'predicate': predicate,
                    'object': object_R
                })
                print(f"  + {structures[subject_R]['name']} → {structures[object_R]['name']}")
            
            # Keep original if neither side is lateralized
            if not (subject_L or subject_R or object_L or object_R):
                kept_rels.append(rel)
        
        # Update relationships: only keep non-lateralized + add new lateralized ones
        # (Don't keep originals that were lateralized - they point to deleted structures)
        data['relationships'] = kept_rels + new_rels
        
        print(f"  Original: {len(original_rels)} relationships")
        print(f"  Kept: {len(kept_rels)} (non-lateralized)")
        print(f"  Added: {len(new_rels)} (lateralized)")
        print(f"  Total: {len(data['relationships'])} relationships")
        
        # Save updated file
        save_yaml_file(yaml_file, data)
    
    print("\n" + "=" * 70)
    print("✓ Relationship lateralization complete!")
    print("=" * 70)


if __name__ == '__main__':
    lateralize_relationships()
