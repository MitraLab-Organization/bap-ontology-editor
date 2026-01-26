#!/usr/bin/env python3
"""
Remove parent structures that have been lateralized.
Promotes (L) and (R) children to the parent's level and deletes the parent.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List

from ai_context import load_all_structures, build_hierarchy_context


def main():
    print("=" * 70)
    print("REMOVE LATERALIZED PARENT STRUCTURES")
    print("=" * 70)
    print()
    
    # Load structures
    print("Loading structures...")
    structures = load_all_structures()
    context = build_hierarchy_context(structures)
    print(f"  ✓ Loaded {len(structures)} structures")
    
    # Find parents that have exactly (L) and (R) children
    actions = []
    parents_to_remove = []
    
    for struct_id, struct in structures.items():
        name = struct.get('name', '')
        children = context['parent_child_map'].get(struct_id, [])
        
        if len(children) == 2:
            # Check if children are (L) and (R) versions
            child_names = [structures[cid].get('name') for cid in children]
            expected_L = f"{name} (L)"
            expected_R = f"{name} (R)"
            
            if expected_L in child_names and expected_R in child_names:
                parents_to_remove.append((struct_id, name))
                
                # Get parent's parent
                grandparent_id = struct.get('parent')
                grandparent_name = None
                if grandparent_id and grandparent_id in structures:
                    grandparent_name = structures[grandparent_id].get('name')
                
                # Move (L) and (R) to grandparent level
                for child_id in children:
                    child_name = structures[child_id].get('name')
                    actions.append({
                        'type': 'move_structure',
                        'structure_name': child_name,
                        'structure_id': child_id,
                        'new_parent_name': grandparent_name,
                        'new_parent_id': grandparent_id
                    })
                
                # Delete the parent (after moves)
                actions.append({
                    'type': 'delete_structure',
                    'structure_name': name,
                    'structure_id': struct_id,
                    'reason': 'lateralized parent no longer needed'
                })
    
    print(f"\n📋 Found {len(parents_to_remove)} parents to remove:")
    for struct_id, name in sorted(parents_to_remove, key=lambda x: x[1])[:20]:
        print(f"  - {name} ({struct_id})")
    
    if len(parents_to_remove) > 20:
        print(f"  ... and {len(parents_to_remove) - 20} more")
    
    if not parents_to_remove:
        print("\n✓ No lateralized parents to remove")
        return
    
    # Ask for confirmation
    print()
    response = input(f"Proceed with removing {len(parents_to_remove)} parents? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("Cancelled.")
        return
    
    # Save actions
    output = {
        'understood': f'Remove {len(parents_to_remove)} lateralized parents and promote (L) and (R) children',
        'actions': actions,
        'warnings': []
    }
    
    output_dir = Path('.ai_requests')
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / 'remove_parents.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✓ Saved to {output_file}")
    print(f"  Generated {len(actions)} actions")
    print("\nTo apply these changes, run:")
    print("  cp .ai_requests/remove_parents.json .ai_requests/issue_remove_parents.json")
    print("  ISSUE_NUMBER=remove_parents python scripts/ai_create_changes_v2.py")


if __name__ == '__main__':
    main()
