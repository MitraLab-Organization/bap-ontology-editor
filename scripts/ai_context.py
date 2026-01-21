#!/usr/bin/env python3
"""
AI Context Builder - Provides rich hierarchical context for reasoning.
"""

from pathlib import Path
from typing import Dict, List, Set, Optional
import yaml


def load_yaml_file(filepath: Path) -> Optional[dict]:
    """Load a YAML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def load_all_structures() -> Dict[str, dict]:
    """Load all structures from all YAML files."""
    structures = {}
    structures_dir = Path('structures')
    
    if not structures_dir.exists():
        return structures
    
    for yaml_file in structures_dir.glob('*.yaml'):
        data = load_yaml_file(yaml_file)
        if data and 'structures' in data:
            for struct in data['structures']:
                if 'id' in struct:
                    structures[struct['id']] = {
                        **struct,
                        '_source_file': yaml_file.name
                    }
    
    return structures


def classify_structure_type(name: str, definition: str = '') -> str:
    """Classify a structure by its type."""
    text = f"{name} {definition}".lower()
    
    if any(word in text for word in ['muscle', 'muscular', 'rectus', 'oblique', 'levator', 'tensor']):
        return 'muscle'
    elif any(word in text for word in ['bone', 'ossicle', 'vertebra', 'cranium', 'nasal', 'vomer', 'maxilla']):
        return 'bone'
    elif any(word in text for word in ['nerve', 'neural', 'ganglion', 'plexus']):
        return 'nerve'
    elif any(word in text for word in ['artery', 'vein', 'vessel', 'vascular']):
        return 'vessel'
    elif any(word in text for word in ['cavity', 'space', 'sinus', 'passage', 'meatus']):
        return 'cavity'
    elif any(word in text for word in ['system', 'region', 'group']):
        return 'category'
    else:
        return 'organ'


def build_hierarchy_context(structures: Dict[str, dict]) -> dict:
    """Build comprehensive hierarchy context for AI reasoning."""
    
    context = {
        'parent_child_map': {},  # parent_id -> [child_ids]
        'child_parent_map': {},  # child_id -> parent_id
        'structure_metadata': {},  # id -> metadata
        'type_classifications': {
            'muscles': [],
            'bones': [],
            'nerves': [],
            'vessels': [],
            'cavities': [],
            'categories': [],
            'organs': []
        },
        'file_map': {},  # id -> source_file
        'name_to_id_map': {},  # name.lower() -> id
        'depth_map': {}  # id -> depth in tree
    }
    
    # Build basic maps
    for struct_id, struct in structures.items():
        name = struct.get('name', '')
        definition = struct.get('definition', '')
        parent_id = struct.get('parent')
        source_file = struct.get('_source_file', 'unknown')
        
        # Parent-child relationships
        if parent_id:
            if parent_id not in context['parent_child_map']:
                context['parent_child_map'][parent_id] = []
            context['parent_child_map'][parent_id].append(struct_id)
            context['child_parent_map'][struct_id] = parent_id
        
        # Classification
        struct_type = classify_structure_type(name, definition)
        type_key = struct_type + 's' if not struct_type.endswith('s') else struct_type
        if type_key in context['type_classifications']:
            context['type_classifications'][type_key].append(struct_id)
        
        # Other maps
        context['file_map'][struct_id] = source_file
        context['name_to_id_map'][name.lower()] = struct_id
        
        # Metadata
        context['structure_metadata'][struct_id] = {
            'name': name,
            'type': struct_type,
            'parent_id': parent_id,
            'has_children': struct_id in context['parent_child_map'],
            'child_count': 0,  # Will update later
            'definition': definition,
            'source_file': source_file
        }
    
    # Calculate child counts and depths
    for struct_id in structures:
        children = context['parent_child_map'].get(struct_id, [])
        context['structure_metadata'][struct_id]['child_count'] = len(children)
        context['depth_map'][struct_id] = calculate_depth(struct_id, context['child_parent_map'])
    
    return context


def calculate_depth(struct_id: str, child_parent_map: Dict[str, str], visited: Set[str] = None) -> int:
    """Calculate depth of a structure in the hierarchy (0 = root)."""
    if visited is None:
        visited = set()
    
    if struct_id in visited:
        return 999  # Circular reference
    
    visited.add(struct_id)
    
    parent_id = child_parent_map.get(struct_id)
    if parent_id is None:
        return 0  # Root node
    
    return 1 + calculate_depth(parent_id, child_parent_map, visited)


def get_direct_children(parent_id: str, context: dict) -> List[str]:
    """Get direct children (depth = 1) of a parent structure."""
    return context['parent_child_map'].get(parent_id, [])


def get_all_descendants(parent_id: str, context: dict) -> List[str]:
    """Get all descendants (any depth) of a parent structure."""
    descendants = []
    direct_children = context['parent_child_map'].get(parent_id, [])
    
    for child_id in direct_children:
        descendants.append(child_id)
        descendants.extend(get_all_descendants(child_id, context))
    
    return descendants


def is_descendant(potential_descendant: str, ancestor: str, context: dict) -> bool:
    """Check if potential_descendant is anywhere under ancestor in tree."""
    descendants = get_all_descendants(ancestor, context)
    return potential_descendant in descendants


def find_structure_id_by_name(name: str, context: dict) -> Optional[str]:
    """Find structure ID by name (case-insensitive)."""
    return context['name_to_id_map'].get(name.lower())


def get_structure_summary(struct_id: str, structures: Dict[str, dict], context: dict) -> str:
    """Get a human-readable summary of a structure."""
    struct = structures.get(struct_id)
    if not struct:
        return f"Unknown structure: {struct_id}"
    
    metadata = context['structure_metadata'][struct_id]
    name = struct.get('name', 'Unknown')
    struct_type = metadata['type']
    child_count = metadata['child_count']
    depth = context['depth_map'].get(struct_id, 0)
    
    summary = f"{name} ({struct_id}) - Type: {struct_type}, Depth: {depth}"
    if child_count > 0:
        summary += f", Children: {child_count}"
    
    return summary


def validate_action_safety(action: dict, structures: Dict[str, dict], context: dict) -> dict:
    """Validate that a single action is safe to execute."""
    action_type = action.get('type')
    errors = []
    warnings = []
    
    if action_type == 'delete_structure':
        struct_id = action.get('structure_id')
        struct_name = action.get('structure_name', struct_id)
        
        # Check if has children
        children = context['parent_child_map'].get(struct_id, [])
        if children:
            child_names = [structures[cid].get('name', cid) for cid in children[:3]]
            errors.append(
                f"Cannot delete '{struct_name}' - has {len(children)} children: {', '.join(child_names)}"
                + ("..." if len(children) > 3 else "")
            )
    
    elif action_type == 'move_structure':
        struct_id = action.get('structure_id')
        new_parent_id = action.get('new_parent_id')
        struct_name = action.get('structure_name', struct_id)
        new_parent_name = action.get('new_parent_name', new_parent_id)
        
        # Check for circular reference
        if is_descendant(new_parent_id, struct_id, context):
            errors.append(
                f"Circular reference: Cannot move '{struct_name}' under its own descendant '{new_parent_name}'"
            )
        
        # Check if structure exists
        if struct_id not in structures:
            errors.append(f"Structure '{struct_name}' ({struct_id}) not found")
        
        # Check if new parent exists (might be created in same batch)
        if new_parent_id not in structures:
            warnings.append(f"New parent '{new_parent_name}' ({new_parent_id}) not found - should be created first")
    
    elif action_type == 'create_structure':
        parent_id = action.get('parent_id')
        parent_name = action.get('parent_name', parent_id)
        
        # Check if parent exists
        if parent_id and parent_id not in structures:
            errors.append(f"Parent structure '{parent_name}' ({parent_id}) not found")
    
    return {
        'action': action,
        'safe': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }


def validate_action_plan(actions: List[dict], structures: Dict[str, dict], context: dict) -> dict:
    """Validate entire action plan for safety and correct ordering."""
    
    all_errors = []
    all_warnings = []
    individual_results = []
    
    # Track what will be created in this batch
    will_be_created = set()
    for action in actions:
        if action.get('type') == 'create_structure':
            struct_id = action.get('id')
            if struct_id:
                will_be_created.add(struct_id)
    
    # Validate each action
    for i, action in enumerate(actions):
        result = validate_action_safety(action, structures, context)
        
        # If error is about parent not existing, check if it will be created
        if not result['safe']:
            filtered_errors = []
            for error in result['errors']:
                if 'Parent structure' in error and action.get('parent_id') in will_be_created:
                    # This is OK - parent will be created in same batch
                    continue
                filtered_errors.append(error)
            
            result['errors'] = filtered_errors
            result['safe'] = len(filtered_errors) == 0
        
        individual_results.append(result)
        all_errors.extend(result['errors'])
        all_warnings.extend(result['warnings'])
    
    # Check ordering: CREATEs should come before MOVEs that depend on them
    create_indices = {}
    for i, action in enumerate(actions):
        if action.get('type') == 'create_structure':
            create_indices[action.get('id')] = i
    
    for i, action in enumerate(actions):
        if action.get('type') == 'move_structure':
            new_parent_id = action.get('new_parent_id')
            if new_parent_id in create_indices and create_indices[new_parent_id] > i:
                all_errors.append(
                    f"Action {i}: MOVE before CREATE - '{action.get('structure_name')}' "
                    f"is moved to '{action.get('new_parent_name')}' which is created later"
                )
    
    # Check deletes don't happen before dependent moves
    for i, action in enumerate(actions):
        if action.get('type') == 'delete_structure':
            struct_id = action.get('structure_id')
            children = context['parent_child_map'].get(struct_id, [])
            
            if children:
                # Check if all children are moved in earlier actions
                moved_children = set()
                for j in range(i):
                    earlier_action = actions[j]
                    if earlier_action.get('type') == 'move_structure':
                        if earlier_action.get('structure_id') in children:
                            moved_children.add(earlier_action.get('structure_id'))
                
                if len(moved_children) < len(children):
                    unmoved = set(children) - moved_children
                    unmoved_names = [structures[cid].get('name', cid) for cid in list(unmoved)[:3]]
                    all_errors.append(
                        f"Action {i}: DELETE '{action.get('structure_name')}' before moving {len(unmoved)} children: "
                        + ", ".join(unmoved_names)
                    )
    
    return {
        'valid': len(all_errors) == 0,
        'errors': all_errors,
        'warnings': all_warnings,
        'individual_results': individual_results
    }
