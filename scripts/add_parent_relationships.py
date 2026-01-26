#!/usr/bin/env python3
"""
Add relationships for parent structures to lateralized targets.
E.g., Masseter → Trigeminal nerve (L) and Masseter → Trigeminal nerve (R)
"""

import yaml
from pathlib import Path

def load_structures():
    structures = {}
    for yaml_file in Path('structures').glob('*.yaml'):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
            if data and 'structures' in data:
                for s in data['structures']:
                    structures[s['id']] = s
    return structures

def find_structure_by_name(name, structures):
    for sid, s in structures.items():
        if s['name'] == name:
            return sid
    return None

# Load structures
structures = load_structures()

# Find IDs
relationships_to_add = [
    ('Masseter', 'innervated_by', 'Trigeminal nerve'),
    ('Masseter', 'supplied_by', 'Maxillary artery'),
    ('Temporalis', 'innervated_by', 'Trigeminal nerve'),
    ('Temporalis', 'supplied_by', 'Temporal artery'),
    ('Trapezius', 'innervated_by', 'Accessory nerve'),
    ('Orbicularis oris', 'innervated_by', 'Facial nerve'),
    ('Tensor tympani', 'innervated_by', 'Trigeminal nerve'),
]

print("Finding structure IDs...")
for subj, pred, obj in relationships_to_add:
    subj_id = find_structure_by_name(subj, structures)
    
    # For lateralized targets, find both (L) and (R)
    obj_L = find_structure_by_name(f"{obj} (L)", structures)
    obj_R = find_structure_by_name(f"{obj} (R)", structures)
    
    if not obj_L and not obj_R:
        # Not lateralized, find the base structure
        obj_id = find_structure_by_name(obj, structures)
        print(f"\n# {subj} → {pred} → {obj}")
        print(f"- subject: {subj_id}")
        print(f"  predicate: {pred}")
        print(f"  object: {obj_id}")
    else:
        print(f"\n# {subj} → {pred} → {obj} (lateralized)")
        if obj_L:
            print(f"- subject: {subj_id}")
            print(f"  predicate: {pred}")
            print(f"  object: {obj_L}")
        if obj_R:
            print(f"- subject: {subj_id}")
            print(f"  predicate: {pred}")
            print(f"  object: {obj_R}")
