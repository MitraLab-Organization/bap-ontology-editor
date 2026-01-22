# Enhanced AI Workflow System

## Overview

The enhanced AI workflow adds context-aware reasoning and support for complex multi-step operations including creating, moving, deleting, and updating structures.

## New Capabilities

### Action Types

1. **create_structure** - Create new anatomical structures
2. **move_structure** - Move existing structures to new parents
3. **delete_structure** - Remove deprecated structures
4. **update_structure** - Update structure properties
5. **add_relationship** - Add relationships between structures

### Context-Aware Reasoning

The AI now has access to:
- Complete hierarchy map (parent→children relationships)
- Structure type classifications (muscle/bone/nerve/vessel/cavity)
- Depth information in the hierarchy tree
- Safety validation (circular references, orphaned children, etc.)

### Intelligent Ordering

Actions are automatically validated and reordered if needed:
- CREATE actions before MOVE actions that depend on them
- MOVE children away before DELETE parent
- Safety checks prevent invalid operations

## Files Added

### Core Components

- **`scripts/ai_context.py`** - Hierarchy context builder and validation
- **`scripts/ai_create_changes_v2.py`** - Enhanced action execution engine
- **`scripts/ai_enhanced_prompt.py`** - AI system prompt with reasoning rules

### Usage

The enhanced system is backwards compatible with the existing workflow. To use:

#### Option 1: Use Enhanced Script Directly

```bash
cd bap-ontology-editor

# Process a complex request
ISSUE_NUMBER=123 python scripts/ai_create_changes_v2.py
```

#### Option 2: Create AI Request JSON Manually

Create a file `.ai_requests/issue_test.json`:

```json
{
  "understood": "Create Eye Muscles group and move all eye muscles",
  "reasoning": [
    "Found 7 eye muscles under Eye",
    "Creating Eye Muscles group first",
    "Then moving all muscles"
  ],
  "actions": [
    {
      "type": "create_structure",
      "name": "Eye Muscles",
      "id": "BAP_0012008",
      "parent_name": "Cranial muscles",
      "definition": "Extraocular and eyelid muscles"
    },
    {
      "type": "move_structure",
      "structure_name": "levator palpebrae superioris",
      "structure_id": "BAP_0000085",
      "new_parent_name": "Eye Muscles",
      "new_parent_id": "BAP_0012008"
    }
  ]
}
```

Then execute:

```bash
ISSUE_NUMBER=test python scripts/ai_create_changes_v2.py
```

## Example Requests

### Simple: Create and Add

**User Request:**
```
Add stapedius muscle under inner ear, it's innervated by the facial nerve
```

**AI Output:**
```json
{
  "actions": [
    {"type": "create_structure", "name": "Stapedius", ...},
    {"type": "add_relationship", "subject_name": "Stapedius", "predicate": "innervated_by", "object_name": "Facial nerve"}
  ]
}
```

### Complex: Multi-Step Reorganization

**User Request:**
```
Move all eye muscles from Eye to a new Eye Muscles group under Cranial muscles.
Move ear muscles (Stapedius and Auricularis muscles) to new groups.
Delete the deprecated Ear structure.
```

**AI Output:**
```json
{
  "reasoning": [
    "Found 7 eye muscles under Eye",
    "Found 4 ear muscles under deprecated Ear",
    "Creating 3 new muscle groups",
    "Moving 11 muscles total",
    "Deleting Ear last (after children moved)"
  ],
  "actions": [
    {"type": "create_structure", "name": "Eye Muscles", ...},
    {"type": "create_structure", "name": "Inner Ear Muscles", ...},
    {"type": "create_structure", "name": "External Ear Muscles", ...},
    {"type": "move_structure", ...},  // 11 move actions
    {"type": "delete_structure", "structure_name": "Ear"}
  ]
}
```

## Safety Features

### Pre-Execution Validation

- Checks all referenced structures exist
- Prevents circular references
- Ensures dependencies are satisfied
- Validates action ordering

### Runtime Safety

- Won't delete structures with children
- Won't create circular parent relationships
- Validates each action before execution
- Provides detailed error messages

### Post-Execution

- Runs `validate.py` to check ontology integrity
- Reports success/failure for each action
- Provides execution summary

## Context-Based Logic

The AI understands implicit anatomical rules:

### Type Classification

- **Muscles** → muscles.yaml, under muscle groups
- **Bones** → skeletal.yaml, under cranial hierarchy
- **Nerves** → nerves.yaml, under nerve groups
- **Vessels** → vessels.yaml, under vascular groups
- **Categories** → body_regions.yaml

### Anatomical Knowledge

- Distinguishes between spaces (cavities) and contents (bones/organs)
- Knows facial bones belong in Viscerocranium
- Understands muscle group organization
- Recognizes deprecated structures should be removed after migration

### Hierarchy Depth

- "Move everything under X" = direct children only
- Sub-structures stay with their immediate parent
- Maintains nested relationships (e.g., tendons stay with muscles)

## Testing

Test the enhanced workflow with:

```bash
# Run with example data
cd bap-ontology-editor

# Create test request
cat > .ai_requests/issue_test.json << 'EOF'
{
  "actions": [
    {
      "type": "create_structure",
      "name": "Test Muscle Group",
      "id": "BAP_9999999",
      "parent_name": "Cranial muscles",
      "definition": "Test muscle group"
    }
  ]
}
EOF

# Execute
ISSUE_NUMBER=test python scripts/ai_create_changes_v2.py

# Validate
python scripts/validate.py

# Clean up
rm .ai_requests/issue_test.json
```

## Integration with GitHub Workflow

To enable in GitHub Actions, update `.github/workflows/ai-approve.yml`:

```yaml
- name: Create changes from AI data
  env:
    ISSUE_NUMBER: ${{ github.event.issue.number }}
  run: |
    # Use enhanced version
    python scripts/ai_create_changes_v2.py
```

## Backwards Compatibility

The system maintains backwards compatibility:

- Old format (`structures` + `relationships`) automatically converted to `actions`
- Existing `ai_create_changes.py` still works
- Enhanced features only activate when using action-based format

## Future Enhancements

Potential additions:

- [ ] Bulk import from spreadsheets
- [ ] Automatic synonym detection
- [ ] Relationship inference from text
- [ ] Cross-ontology mapping
- [ ] Version control integration
