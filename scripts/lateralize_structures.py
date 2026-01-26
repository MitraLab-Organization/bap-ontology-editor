#!/usr/bin/env python3
"""
Lateralize leaf structures by creating (L) and (R) versions.
Only applies to leaf nodes (structures with no children) that are not midline.
"""

import sys
from pathlib import Path
from typing import Set, Dict, List

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

from ai_context import load_all_structures, build_hierarchy_context


def load_all_relationships() -> Dict:
    """Load all relationships from YAML files."""
    relationships = []
    rel_dir = Path('relationships')
    
    if not rel_dir.exists():
        return relationships
    
    for yaml_file in rel_dir.glob('*.yaml'):
        try:
            data = load_yaml_file(yaml_file)
            if data and 'relationships' in data and data['relationships']:
                for rel in data['relationships']:
                    relationships.append(rel)
        except Exception:
            pass
    
    return relationships


# Midline structures that should NOT be lateralized
MIDLINE_STRUCTURES = {
    'Tail',
    'Nasal cavity',
    'Oral cavity',
    'Orbicularis oris',
    'frontal',
    'occipital',
    'sphenoid',
    'vomer',
    'Brain',
    'Larynx',
    'epiglottis',
    'thyroid cartilage',
    'Esophagus',
    'hyoid bone',
    'Thyroid gland',
    'cervical vertebra',
    'Spinal Cord',
    'Central nervous system',
}


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


def find_structure_file(struct_id: str) -> Path:
    """Find which YAML file contains a given structure."""
    structures_dir = Path('structures')
    
    for yaml_file in structures_dir.glob('*.yaml'):
        data = load_yaml_file(yaml_file)
        if data and 'structures' in data:
            for struct in data['structures']:
                if struct.get('id') == struct_id:
                    return yaml_file
    
    return None


def get_next_available_id(structures: Dict) -> int:
    """Get next available BAP ID."""
    max_id = 21700
    
    for struct_id in structures.keys():
        if struct_id.startswith('BAP_'):
            try:
                num = int(struct_id.split('_')[1])
                max_id = max(max_id, num)
            except:
                pass
    
    return max_id + 1


def is_leaf_node(struct_id: str, context: Dict) -> bool:
    """Check if a structure is a leaf node (has no children)."""
    children = context['parent_child_map'].get(struct_id, [])
    return len(children) == 0


def has_relationships(struct_id: str, relationships: list) -> bool:
    """Check if a structure is referenced in any relationships."""
    for rel in relationships:
        if rel.get('subject') == struct_id or rel.get('object') == struct_id:
            return True
    return False


def lateralize_structure(struct_id: str, struct_name: str, structures: Dict, context: Dict, relationships: list, next_id: int) -> List[dict]:
    """
    Create left and right versions of a structure.
    If structure has relationships, keep it as parent with (L) and (R) children.
    If no relationships, delete it and create (L) and (R) at the same level.
    Returns list of actions to perform.
    """
    actions = []
    
    # Get original structure details
    original = structures[struct_id]
    parent_id = original.get('parent')
    definition = original.get('definition', '')
    
    # Check if structure has relationships
    has_rels = has_relationships(struct_id, relationships)
    
    if has_rels:
        # Keep structure as parent, create (L) and (R) as children
        left_id = f"BAP_{next_id:07d}"
        next_id += 1
        
        actions.append({
            'type': 'create_structure',
            'name': f"{struct_name} (L)",
            'id': left_id,
            'parent_name': struct_name,
            'parent_id': struct_id,
            'definition': definition
        })
        
        right_id = f"BAP_{next_id:07d}"
        next_id += 1
        
        actions.append({
            'type': 'create_structure',
            'name': f"{struct_name} (R)",
            'id': right_id,
            'parent_name': struct_name,
            'parent_id': struct_id,
            'definition': definition
        })
    else:
        # No relationships - delete and create (L) and (R) at same level
        parent_name = None
        if parent_id and parent_id in structures:
            parent_name = structures[parent_id].get('name')
        
        left_id = f"BAP_{next_id:07d}"
        next_id += 1
        
        actions.append({
            'type': 'create_structure',
            'name': f"{struct_name} (L)",
            'id': left_id,
            'parent_name': parent_name,
            'parent_id': parent_id,
            'definition': definition
        })
        
        right_id = f"BAP_{next_id:07d}"
        next_id += 1
        
        actions.append({
            'type': 'create_structure',
            'name': f"{struct_name} (R)",
            'id': right_id,
            'parent_name': parent_name,
            'parent_id': parent_id,
            'definition': definition
        })
        
        actions.append({
            'type': 'delete_structure',
            'structure_name': struct_name,
            'structure_id': struct_id,
            'reason': 'replaced with lateralized (L) and (R) versions'
        })
    
    return actions, next_id


def main():
    print("=" * 70)
    print("LATERALIZATION SCRIPT - Add (L) and (R) to Leaf Nodes")
    print("=" * 70)
    print()
    
    # Load current structures and relationships
    print("Loading structures...")
    structures = load_all_structures()
    context = build_hierarchy_context(structures)
    print(f"  ✓ Loaded {len(structures)} structures")
    
    print("Loading relationships...")
    relationships = load_all_relationships()
    print(f"  ✓ Loaded {len(relationships)} relationships")
    
    # Find all leaf nodes
    print("\nFinding leaf nodes...")
    leaf_nodes = []
    for struct_id, struct in structures.items():
        if is_leaf_node(struct_id, context):
            name = struct.get('name', '')
            if name not in MIDLINE_STRUCTURES:
                leaf_nodes.append((struct_id, name))
    
    print(f"  ✓ Found {len(leaf_nodes)} non-midline leaf nodes to lateralize")
    
    if not leaf_nodes:
        print("\n✓ No structures to lateralize")
        return
    
    # Show what will be lateralized
    print("\n📋 Structures to be lateralized:")
    for struct_id, name in sorted(leaf_nodes, key=lambda x: x[1])[:20]:
        print(f"  - {name} ({struct_id})")
    
    if len(leaf_nodes) > 20:
        print(f"  ... and {len(leaf_nodes) - 20} more")
    
    # Ask for confirmation
    print()
    response = input(f"Proceed with lateralizing {len(leaf_nodes)} structures? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("Cancelled.")
        return
    
    # Generate actions
    print("\nGenerating lateralization actions...")
    all_actions = []
    next_id = get_next_available_id(structures)
    
    for struct_id, name in leaf_nodes:
        actions, next_id = lateralize_structure(struct_id, name, structures, context, relationships, next_id)
        all_actions.extend(actions)
    
    print(f"  ✓ Generated {len(all_actions)} actions")
    
    # Save to JSON for processing
    import json
    output = {
        'understood': f'Lateralize {len(leaf_nodes)} leaf structures',
        'actions': all_actions,
        'warnings': []
    }
    
    output_dir = Path('.ai_requests')
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / 'lateralization.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✓ Saved to {output_file}")
    print("\nTo apply these changes, run:")
    print("  ISSUE_NUMBER=lateralization python scripts/ai_create_changes_v2.py")


if __name__ == '__main__':
    main()
