#!/usr/bin/env python3
"""
Parse reorganization requests and generate proper action JSON.
This script helps convert natural language reorganization descriptions 
into structured actions that the AI can understand.

Usage:
    python scripts/parse_reorganization_request.py < request.txt
    
Or use interactively:
    python scripts/parse_reorganization_request.py --interactive
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Import context functions
try:
    from ai_context import load_all_structures, build_hierarchy_context, find_structure_id_by_name
    HAS_CONTEXT = True
except ImportError:
    HAS_CONTEXT = False
    print("Warning: ai_context not available, will use placeholder IDs")


def get_next_id(structures: Dict = None) -> int:
    """Get next available BAP ID."""
    max_id = 21700
    
    if structures:
        for struct_id in structures.keys():
            if struct_id.startswith('BAP_'):
                try:
                    num = int(struct_id.split('_')[1])
                    max_id = max(max_id, num)
                except:
                    pass
    
    return max_id + 1


def parse_reorganization_text(text: str, structures: Dict = None, context: Dict = None) -> dict:
    """
    Parse natural language reorganization requests.
    
    Expected patterns:
    - "Create [group name] under [parent name]"
    - "Move [structure name] to [target group]"
    - "Rename [old name] to [new name]"
    """
    
    actions = []
    next_id = get_next_id(structures) if structures else 21700
    created_groups = {}  # Track groups we create for reference
    
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Pattern: Create "X" under "Y"
        create_match = re.search(
            r'[Cc]reate\s+(?:a\s+)?(?:new\s+)?(?:group\s+)?["\']([^"\']+)["\']?\s+under\s+["\']([^"\']+)["\']?',
            line
        )
        
        if create_match:
            group_name = create_match.group(1).strip()
            parent_name = create_match.group(2).strip()
            
            # Try to find parent ID
            parent_id = None
            if context:
                parent_id = find_structure_id_by_name(parent_name, context)
            
            new_id = f"BAP_{next_id:07d}"
            next_id += 1
            
            actions.append({
                'type': 'create_structure',
                'name': group_name,
                'id': new_id,
                'parent_name': parent_name,
                'parent_id': parent_id,
                'definition': f'{group_name}'
            })
            
            # Track this for later moves
            created_groups[group_name.lower()] = new_id
            
            print(f"  [CREATE] {group_name} ({new_id}) under {parent_name} ({parent_id or '?'})")
            continue
        
        # Pattern: Move "X" to "Y" or Move X (ID) to Y
        move_match = re.search(
            r'[Mm]ove\s+["\']([^"\']+)["\'](?:\s*\(([^)]+)\))?\s+to\s+["\']([^"\']+)["\']',
            line
        )
        
        if move_match:
            struct_name = move_match.group(1).strip()
            struct_id = move_match.group(2).strip() if move_match.group(2) else None
            target_name = move_match.group(3).strip()
            
            # Try to find structure ID if not provided
            if not struct_id and context:
                struct_id = find_structure_id_by_name(struct_name, context)
            
            # Try to find target ID
            target_id = None
            target_lower = target_name.lower()
            
            # Check if target was just created
            if target_lower in created_groups:
                target_id = created_groups[target_lower]
            elif context:
                target_id = find_structure_id_by_name(target_name, context)
            
            actions.append({
                'type': 'move_structure',
                'structure_name': struct_name,
                'structure_id': struct_id,
                'new_parent_name': target_name,
                'new_parent_id': target_id
            })
            
            print(f"  [MOVE] {struct_name} ({struct_id or '?'}) → {target_name} ({target_id or '?'})")
            continue
        
        # Pattern: Rename "X" to "Y"
        rename_match = re.search(
            r'[Rr]ename\s+["\']?([^"\']+?)["\']?(?:\s*\(([^)]+)\))?\s+to\s+["\']?([^"\']+?)["\']?',
            line
        )
        
        if rename_match:
            old_name = rename_match.group(1).strip()
            struct_id = rename_match.group(2).strip() if rename_match.group(2) else None
            new_name = rename_match.group(3).strip()
            
            # Try to find structure ID if not provided
            if not struct_id and context:
                struct_id = find_structure_id_by_name(old_name, context)
            
            actions.append({
                'type': 'update_structure',
                'structure_name': old_name,
                'structure_id': struct_id,
                'changes': {
                    'name': new_name
                }
            })
            
            print(f"  [RENAME] {old_name} ({struct_id or '?'}) → {new_name}")
            continue
    
    return {
        'understood': f'Reorganization with {len(actions)} actions',
        'actions': actions,
        'warnings': []
    }


def interactive_mode():
    """Interactive mode for building reorganization requests."""
    print("=" * 70)
    print("REORGANIZATION REQUEST BUILDER")
    print("=" * 70)
    print()
    print("Enter your reorganization commands (one per line).")
    print("Supported patterns:")
    print("  - Create \"Group Name\" under \"Parent Name\"")
    print("  - Move \"Structure Name\" (BAP_XXXXXXX) to \"Target Group\"")
    print("  - Rename \"Old Name\" (BAP_XXXXXXX) to \"New Name\"")
    print()
    print("Type 'done' when finished, 'cancel' to abort.")
    print()
    
    lines = []
    while True:
        try:
            line = input("> ").strip()
            if line.lower() == 'done':
                break
            if line.lower() == 'cancel':
                print("Cancelled.")
                return
            if line:
                lines.append(line)
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            return
    
    text = '\n'.join(lines)
    
    # Load context if available
    structures = None
    context = None
    if HAS_CONTEXT:
        print("\nLoading ontology context...")
        structures = load_all_structures()
        context = build_hierarchy_context(structures)
        print(f"  Loaded {len(structures)} structures")
    
    print("\nParsing...")
    parsed = parse_reorganization_text(text, structures, context)
    
    print("\n" + "=" * 70)
    print("GENERATED ACTIONS")
    print("=" * 70)
    print(json.dumps(parsed, indent=2))
    
    # Ask to save
    save = input("\nSave to .ai_requests/manual.json? (y/n): ").strip().lower()
    if save == 'y':
        output_dir = Path('.ai_requests')
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / 'manual.json'
        with open(output_file, 'w') as f:
            json.dump(parsed, f, indent=2)
        
        print(f"\n✓ Saved to {output_file}")
        print("\nTo apply these changes, run:")
        print(f"  ISSUE_NUMBER=manual python scripts/ai_create_changes_v2.py")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_mode()
        return
    
    # Read from stdin
    text = sys.stdin.read()
    
    # Load context if available
    structures = None
    context = None
    if HAS_CONTEXT:
        structures = load_all_structures()
        context = build_hierarchy_context(structures)
    
    parsed = parse_reorganization_text(text, structures, context)
    
    # Output JSON
    print(json.dumps(parsed, indent=2))


if __name__ == '__main__':
    main()
