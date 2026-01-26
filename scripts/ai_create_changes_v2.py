#!/usr/bin/env python3
"""
Enhanced AI Changes Creator - Supports complex multi-action operations.
Includes: create, move, delete, update actions with context awareness.
"""

import os
import json
import sys
from pathlib import Path
from typing import Optional, Dict

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

# Import our context builder
from ai_context import (
    load_all_structures,
    build_hierarchy_context,
    validate_action_plan,
    find_structure_id_by_name,
    classify_structure_type
)


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


def determine_target_file(struct_name: str, parent_name: str, definition: str, struct_type: str = None) -> str:
    """Determine which YAML file a structure should be added to."""
    if struct_type is None:
        struct_type = classify_structure_type(struct_name, definition)
    
    file_map = {
        'muscle': 'structures/muscles.yaml',
        'bone': 'structures/skeletal.yaml',
        'nerve': 'structures/nerves.yaml',
        'vessel': 'structures/vessels.yaml',
    }
    
    return file_map.get(struct_type, 'structures/body_regions.yaml')


def find_structure_file(struct_id: str) -> Optional[Path]:
    """Find which YAML file contains a given structure."""
    structures_dir = Path('structures')
    
    for yaml_file in structures_dir.glob('*.yaml'):
        data = load_yaml_file(yaml_file)
        if data and 'structures' in data:
            for struct in data['structures']:
                if struct.get('id') == struct_id:
                    return yaml_file
    
    return None


def action_create_structure(action: dict, context: dict) -> bool:
    """CREATE action handler."""
    name = action.get('name')
    struct_id = action.get('id')
    parent_name = action.get('parent_name')
    parent_id = action.get('parent_id')  # Check if ID is provided
    definition = action.get('definition', '')
    target_file = action.get('file')
    
    print(f"  Creating: {name} ({struct_id})")
    
    # Find parent ID (use provided ID if available, otherwise look up by name)
    if not parent_id and parent_name:
        parent_id = find_structure_id_by_name(parent_name, context)
    
    if not parent_id and parent_name:
        print(f"    ⚠️  Parent '{parent_name}' not found")
        return False
    
    # Determine target file
    if not target_file:
        target_file = determine_target_file(name, parent_name, definition)
    
    filepath = Path(target_file)
    if not filepath.exists():
        print(f"    ⚠️  File {filepath} not found")
        return False
    
    # Load and update file
    data = load_yaml_file(filepath)
    if 'structures' not in data:
        data['structures'] = []
    
    new_struct = {
        'id': struct_id,
        'name': name,
        'parent': parent_id,
    }
    
    if definition:
        new_struct['definition'] = definition
    
    data['structures'].append(new_struct)
    save_yaml_file(filepath, data)
    
    print(f"    ✓ Created in {filepath.name}")
    return True


def action_move_structure(action: dict, context: dict) -> bool:
    """MOVE action handler."""
    struct_name = action.get('structure_name')
    struct_id = action.get('structure_id')
    new_parent_name = action.get('new_parent_name')
    new_parent_id = action.get('new_parent_id')
    
    print(f"  Moving: {struct_name} → {new_parent_name}")
    
    # Find structure ID if not provided
    if not struct_id:
        struct_id = find_structure_id_by_name(struct_name, context)
        if not struct_id:
            print(f"    ⚠️  Structure '{struct_name}' not found")
            return False
    
    # Find new parent ID if not provided
    if not new_parent_id:
        new_parent_id = find_structure_id_by_name(new_parent_name, context)
        if not new_parent_id:
            print(f"    ⚠️  Parent '{new_parent_name}' not found")
            return False
    
    # Find which file contains the structure
    filepath = find_structure_file(struct_id)
    if not filepath:
        print(f"    ⚠️  Structure file not found")
        return False
    
    # Load and update
    data = load_yaml_file(filepath)
    found = False
    
    for struct in data.get('structures', []):
        if struct.get('id') == struct_id:
            old_parent = struct.get('parent')
            struct['parent'] = new_parent_id
            found = True
            print(f"    ✓ Moved from {old_parent} to {new_parent_id}")
            break
    
    if not found:
        print(f"    ⚠️  Structure not found in {filepath}")
        return False
    
    save_yaml_file(filepath, data)
    return True


def action_delete_structure(action: dict, context: dict) -> bool:
    """DELETE action handler."""
    struct_name = action.get('structure_name')
    struct_id = action.get('structure_id')
    reason = action.get('reason', 'user request')
    
    print(f"  Deleting: {struct_name} (reason: {reason})")
    
    # Find structure ID if not provided
    if not struct_id:
        struct_id = find_structure_id_by_name(struct_name, context)
        if not struct_id:
            print(f"    ⚠️  Structure '{struct_name}' not found")
            return False
    
    # Safety check: reload fresh context and ensure no children
    # (Context may be stale if structures were moved earlier)
    fresh_structures = load_all_structures()
    fresh_context = build_hierarchy_context(fresh_structures)
    children = fresh_context['parent_child_map'].get(struct_id, [])
    if children:
        print(f"    ⚠️  Structure has {len(children)} children - cannot delete")
        return False
    
    # Find which file contains the structure
    filepath = find_structure_file(struct_id)
    if not filepath:
        print(f"    ⚠️  Structure file not found")
        return False
    
    # Load and delete
    data = load_yaml_file(filepath)
    structures = data.get('structures', [])
    
    for i, struct in enumerate(structures):
        if struct.get('id') == struct_id:
            del structures[i]
            save_yaml_file(filepath, data)
            print(f"    ✓ Deleted from {filepath.name}")
            return True
    
    print(f"    ⚠️  Structure not found in {filepath}")
    return False


def action_update_structure(action: dict, context: dict) -> bool:
    """UPDATE action handler."""
    struct_name = action.get('structure_name')
    struct_id = action.get('structure_id')
    changes = action.get('changes', {})
    
    print(f"  Updating: {struct_name}")
    
    # Find structure ID if not provided
    if not struct_id:
        struct_id = find_structure_id_by_name(struct_name, context)
        if not struct_id:
            print(f"    ⚠️  Structure '{struct_name}' not found")
            return False
    
    # Find which file contains the structure
    filepath = find_structure_file(struct_id)
    if not filepath:
        print(f"    ⚠️  Structure file not found")
        return False
    
    # Load and update
    data = load_yaml_file(filepath)
    found = False
    
    for struct in data.get('structures', []):
        if struct.get('id') == struct_id:
            struct.update(changes)
            found = True
            print(f"    ✓ Updated: {', '.join(changes.keys())}")
            break
    
    if not found:
        print(f"    ⚠️  Structure not found in {filepath}")
        return False
    
    save_yaml_file(filepath, data)
    return True


def action_add_relationship(action: dict, context: dict) -> bool:
    """ADD RELATIONSHIP action handler."""
    subject_name = action.get('subject_name')
    predicate = action.get('predicate')
    object_name = action.get('object_name')
    
    print(f"  Relationship: {subject_name} --[{predicate}]--> {object_name}")
    
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
        print(f"    ⚠️  File {filepath} not found")
        return False
    
    # Find structure IDs
    subject_id = find_structure_id_by_name(subject_name, context)
    object_id = find_structure_id_by_name(object_name, context)
    
    if not subject_id:
        print(f"    ⚠️  Subject '{subject_name}' not found")
        return False
    
    if not object_id:
        print(f"    ⚠️  Object '{object_name}' not found")
        return False
    
    # Load and add
    data = load_yaml_file(filepath)
    if 'relationships' not in data or data['relationships'] is None:
        data['relationships'] = []
    
    new_rel = {
        'subject': subject_id,
        'predicate': predicate,
        'object': object_id,
    }
    
    data['relationships'].append(new_rel)
    save_yaml_file(filepath, data)
    
    print(f"    ✓ Added to {filepath.name}")
    return True


def execute_actions_with_context(actions: list, structures: Dict, context: dict):
    """Execute actions with context awareness and safety checks."""
    
    action_handlers = {
        'create_structure': action_create_structure,
        'move_structure': action_move_structure,
        'delete_structure': action_delete_structure,
        'update_structure': action_update_structure,
        'add_relationship': action_add_relationship,
    }
    
    success_count = 0
    failure_count = 0
    
    for i, action in enumerate(actions):
        action_type = action.get('type')
        
        print(f"\n[{i+1}/{len(actions)}] {action_type.upper().replace('_', ' ')}")
        
        handler = action_handlers.get(action_type)
        if not handler:
            print(f"  ⚠️  Unknown action type: {action_type}")
            failure_count += 1
            continue
        
        try:
            success = handler(action, context)
            if success:
                success_count += 1
            else:
                failure_count += 1
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failure_count += 1
    
    return success_count, failure_count


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
    
    print("=" * 70)
    print(f"🤖 ENHANCED AI CHANGES PROCESSOR - Issue #{issue_number}")
    print("=" * 70)
    
    # Load current ontology state
    print("\n📚 Loading ontology context...")
    structures = load_all_structures()
    context = build_hierarchy_context(structures)
    print(f"  ✓ Loaded {len(structures)} structures")
    print(f"  ✓ Built hierarchy context")
    
    # Get actions
    actions = parsed.get('actions', [])
    if not actions:
        # Backwards compatibility with old format
        print("\n⚠️  Old format detected - converting to actions...")
        actions = []
        for struct in parsed.get('structures', []):
            actions.append({'type': 'create_structure', **struct})
        for rel in parsed.get('relationships', []):
            actions.append({'type': 'add_relationship', **rel})
    
    if not actions:
        print("\n⚠️  No actions found")
        sys.exit(1)
    
    print(f"\n📋 Found {len(actions)} actions:")
    action_types = {}
    for action in actions:
        atype = action.get('type', 'unknown')
        action_types[atype] = action_types.get(atype, 0) + 1
    for atype, count in action_types.items():
        print(f"  - {atype}: {count}")
    
    # Validate action plan
    print("\n🔍 Validating action plan...")
    validation = validate_action_plan(actions, structures, context)
    
    if validation['warnings']:
        print(f"\n⚠️  WARNINGS ({len(validation['warnings'])}):")
        for warning in validation['warnings']:
            print(f"  - {warning}")
    
    if not validation['valid']:
        print(f"\n❌ VALIDATION FAILED - {len(validation['errors'])} errors:")
        for error in validation['errors']:
            print(f"  - {error}")
        print("\n❌ Cannot proceed - fix errors first")
        sys.exit(1)
    
    print("  ✓ Validation passed")
    
    # Execute actions
    print("\n🚀 Executing actions...")
    success_count, failure_count = execute_actions_with_context(actions, structures, context)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 EXECUTION SUMMARY")
    print("=" * 70)
    print(f"  ✓ Successful: {success_count}")
    if failure_count > 0:
        print(f"  ✗ Failed: {failure_count}")
    print()
    
    if failure_count == 0:
        # Run validation
        print("🔍 Running validation...")
        result = os.system('python scripts/validate.py')
        
        if result == 0:
            print("\n✅ All changes applied and validated successfully!")
        else:
            print("\n⚠️  Changes applied but validation found issues")
            sys.exit(1)
    else:
        print("⚠️  Some actions failed - review errors above")
        sys.exit(1)


if __name__ == '__main__':
    main()
