#!/usr/bin/env python3
"""
AI-powered ontology request processor using Groq (FREE).
Parses natural language requests and generates YAML structures/relationships.
"""

import os
import json
import sys
from pathlib import Path

# Try to import groq, fall back gracefully
try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False
    print("Warning: groq not installed, using mock mode")

import yaml

# Import enhanced prompt if available
try:
    from ai_enhanced_prompt import ENHANCED_SYSTEM_PROMPT, build_hierarchy_summary
    from ai_context import build_context
    USE_ENHANCED = True
except ImportError:
    USE_ENHANCED = False


# ============================================================================
# Load Current Ontology for Context
# ============================================================================

def load_current_structures() -> list[str]:
    """Load ALL current structure names for context."""
    structures = []
    structures_dir = Path('structures')
    
    if not structures_dir.exists():
        return structures
    
    for yaml_file in structures_dir.glob('*.yaml'):
        try:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                if data and 'structures' in data:
                    for struct in data['structures']:
                        name = struct.get('name', '')
                        struct_id = struct.get('id', '')
                        if name and struct_id:
                            structures.append(f"{name} ({struct_id})")
        except Exception:
            pass
    
    return structures


def load_structure_lookup() -> dict[str, str]:
    """Load a name->ID lookup dictionary for all structures."""
    lookup = {}
    structures_dir = Path('structures')
    
    if not structures_dir.exists():
        return lookup
    
    for yaml_file in structures_dir.glob('*.yaml'):
        try:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                if data and 'structures' in data:
                    for struct in data['structures']:
                        name = struct.get('name', '')
                        struct_id = struct.get('id', '')
                        if name and struct_id:
                            # Store multiple lookup keys
                            lookup[name.lower()] = struct_id
                            lookup[name.lower().replace(' ', '')] = struct_id
        except Exception:
            pass
    
    return lookup


def find_existing_structure(name: str, lookup: dict[str, str]) -> str | None:
    """Find an existing structure ID by name (fuzzy match)."""
    name_lower = name.lower()
    
    # Exact match
    if name_lower in lookup:
        return lookup[name_lower]
    
    # Without spaces
    if name_lower.replace(' ', '') in lookup:
        return lookup[name_lower.replace(' ', '')]
    
    # Partial match
    for key, struct_id in lookup.items():
        if name_lower in key or key in name_lower:
            return struct_id
    
    return None


def find_ambiguous_names(structures: list[str]) -> dict[str, list[str]]:
    """Find structure names that could be ambiguous (e.g., 'Skin' appears multiple times)."""
    name_counts = {}
    
    for s in structures:
        # Extract just the name (before the ID)
        if ' (' in s:
            name = s.split(' (')[0].lower()
        else:
            name = s.lower()
        
        if name not in name_counts:
            name_counts[name] = []
        name_counts[name].append(s)
    
    # Return only names with multiple entries
    return {k: v for k, v in name_counts.items() if len(v) > 1}


def load_existing_relationships() -> list[dict]:
    """Load all existing relationships from YAML files."""
    relationships = []
    rel_dir = Path('relationships')
    
    if not rel_dir.exists():
        return relationships
    
    for yaml_file in rel_dir.glob('*.yaml'):
        try:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                if data and 'relationships' in data and data['relationships']:
                    for rel in data['relationships']:
                        rel['_file'] = yaml_file.name
                        relationships.append(rel)
        except Exception:
            pass
    
    return relationships


def check_duplicate_relationship(subject_id: str, predicate: str, object_id: str, existing_rels: list[dict]) -> bool:
    """Check if a relationship already exists."""
    for rel in existing_rels:
        if (rel.get('subject') == subject_id and 
            rel.get('predicate') == predicate and 
            rel.get('object') == object_id):
            return True
    return False


def find_conflicting_relationships(subject_id: str, predicate: str, existing_rels: list[dict]) -> list[dict]:
    """Find existing relationships that might conflict (same subject + predicate)."""
    conflicts = []
    for rel in existing_rels:
        if rel.get('subject') == subject_id and rel.get('predicate') == predicate:
            conflicts.append(rel)
    return conflicts


def get_next_available_id() -> int:
    """Find the next available BAP ID number."""
    max_id = 21700  # Start from here for AI-generated
    structures_dir = Path('structures')
    
    if not structures_dir.exists():
        return max_id
    
    for yaml_file in structures_dir.glob('*.yaml'):
        try:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                if data and 'structures' in data:
                    for struct in data['structures']:
                        struct_id = struct.get('id', '')
                        if struct_id.startswith('BAP_'):
                            try:
                                num = int(struct_id.split('_')[1])
                                max_id = max(max_id, num)
                            except:
                                pass
        except Exception:
            pass
    
    return max_id + 1


# ============================================================================
# AI Processing
# ============================================================================

SYSTEM_PROMPT = """You are a BAP (Brain Architecture Project) ontology assistant for mouse anatomy.

Your job is to parse natural language requests about anatomical structures and relationships, and output structured JSON.

CRITICAL RULES:
1. ALWAYS check if a structure already exists before creating a new one!
2. If a structure EXISTS, use its EXACT name and ID from the list below
3. Only create NEW structures if they don't exist in the list
4. For relationships, use EXISTING structure names

Output JSON format:
{{
  "understood": "Brief summary of what you understood",
  "structures": [
    {{
      "id": "BAP_XXXXXXX or EXISTING_ID",
      "name": "Structure Name",
      "parent_name": "Existing Parent Name",
      "parent_id": "Parent's BAP ID if known",
      "definition": "Brief anatomical definition",
      "is_new": true/false
    }}
  ],
  "relationships": [
    {{
      "subject_name": "Structure Name",
      "subject_id": "BAP ID if known",
      "predicate": "innervated_by|supplied_by|develops_from|part_of|adjacent_to",
      "object_name": "Target Structure Name",
      "object_id": "BAP ID if known"
    }}
  ],
  "warnings": ["Any issues or clarifications needed"]
}}

EXISTING STRUCTURES (search this list first!):
{structures}

For NEW structures, use IDs starting from BAP_{next_id}.
"""


def process_with_ai(user_request: str, api_key: str) -> dict:
    """Process the request using Groq's free Llama model."""
    
    # Load ALL structures for context
    structures = load_current_structures()
    next_id = get_next_available_id()
    existing_rels = load_existing_relationships()
    
    print(f"Loaded {len(structures)} existing structures for context")
    print(f"Loaded {len(existing_rels)} existing relationships")
    
    # Use enhanced prompt if available
    if USE_ENHANCED:
        print("Using ENHANCED AI prompt with context-aware reasoning")
        context = build_context()
        hierarchy_summary = build_hierarchy_summary(context['structures'], context)
        
        system = ENHANCED_SYSTEM_PROMPT.format(
            next_id=next_id,
            structures='\n'.join(f"- {s}" for s in structures),
            hierarchy_summary=hierarchy_summary
        )
    else:
        print("Using basic AI prompt")
        # Find ambiguous names to warn about
        ambiguous = find_ambiguous_names(structures)
        ambiguous_warning = ""
        if ambiguous:
            ambiguous_warning = "\n\nWARNING - These names are AMBIGUOUS (exist multiple times):\n"
            for name, entries in list(ambiguous.items())[:10]:  # Limit to 10
                ambiguous_warning += f"- '{name}': {', '.join(entries)}\n"
            ambiguous_warning += "Always use the FULL name with ID when referring to these!\n"
        
        # Build prompt with ALL structures
        system = SYSTEM_PROMPT.format(
            next_id=next_id,
            structures='\n'.join(f"- {s}" for s in structures)  # Include ALL structures
        ) + ambiguous_warning
    
    client = Groq(api_key=api_key)
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_request}
        ],
        temperature=0.1,  # Low for consistency
        max_tokens=2000,
        response_format={"type": "json_object"}
    )
    
    parsed = json.loads(response.choices[0].message.content)
    
    # Post-process: validate relationships
    parsed = validate_and_enrich(parsed)
    
    return parsed


def validate_and_enrich(parsed: dict) -> dict:
    """Post-process AI output to add validation warnings."""
    existing_rels = load_existing_relationships()
    lookup = load_structure_lookup()
    warnings = parsed.get('warnings', [])
    
    # Check each proposed relationship
    for rel in parsed.get('relationships', []):
        subject_id = rel.get('subject_id') or find_existing_structure(rel.get('subject_name', ''), lookup)
        object_id = rel.get('object_id') or find_existing_structure(rel.get('object_name', ''), lookup)
        predicate = rel.get('predicate', '')
        
        if subject_id and object_id and predicate:
            # Check for exact duplicate
            if check_duplicate_relationship(subject_id, predicate, object_id, existing_rels):
                warnings.append(f"⚠️ DUPLICATE: Relationship '{rel.get('subject_name')} {predicate} {rel.get('object_name')}' already exists!")
                rel['_is_duplicate'] = True
            
            # Check for potential conflicts
            conflicts = find_conflicting_relationships(subject_id, predicate, existing_rels)
            if conflicts and not rel.get('_is_duplicate'):
                existing_targets = [c.get('object') for c in conflicts]
                warnings.append(f"ℹ️ Note: {rel.get('subject_name')} already has {predicate} relationship(s) with: {existing_targets}")
    
    parsed['warnings'] = warnings
    return parsed


def mock_process(user_request: str) -> dict:
    """Mock processing for testing without API."""
    return {
        "understood": f"[MOCK] Would process: {user_request[:50]}...",
        "structures": [],
        "relationships": [],
        "warnings": ["Running in mock mode - no API key provided"]
    }


# ============================================================================
# Response Generation
# ============================================================================

def generate_response_markdown(parsed: dict, issue_number: str) -> str:
    """Generate a markdown response for the GitHub issue."""
    
    md = "## 🤖 AI Analysis\n\n"
    md += f"**Understood:** {parsed.get('understood', 'Unable to parse')}\n\n"
    
    # Structures
    structures = parsed.get('structures', [])
    if structures:
        new_structures = [s for s in structures if s.get('is_new', True)]
        existing_refs = [s for s in structures if not s.get('is_new', True)]
        
        if new_structures:
            md += "### 📦 NEW Structures to Add\n\n"
            md += "| Name | ID | Parent | Definition |\n"
            md += "|------|-----|--------|------------|\n"
            for s in new_structures:
                parent = s.get('parent_name', '?')
                if s.get('parent_id'):
                    parent += f" (`{s['parent_id']}`)"
                md += f"| {s.get('name', '?')} | `{s.get('id', '?')}` | {parent} | {s.get('definition', '-')[:50]} |\n"
            md += "\n"
        
        if existing_refs:
            md += "### ✅ Using Existing Structures\n\n"
            for s in existing_refs:
                md += f"- **{s.get('name')}** (`{s.get('id')}`)\n"
            md += "\n"
    
    # Relationships
    relationships = parsed.get('relationships', [])
    if relationships:
        # Separate duplicates from new
        new_rels = [r for r in relationships if not r.get('_is_duplicate')]
        dup_rels = [r for r in relationships if r.get('_is_duplicate')]
        
        if new_rels:
            md += "### 🔗 Relationships to Add\n\n"
            for r in new_rels:
                predicate = r.get('predicate', '?').replace('_', ' ')
                subject = r.get('subject_name', '?')
                obj = r.get('object_name', '?')
                
                # Add IDs if known
                if r.get('subject_id'):
                    subject += f" (`{r['subject_id']}`)"
                if r.get('object_id'):
                    obj += f" (`{r['object_id']}`)"
                
                md += f"- **{subject}** {predicate} **{obj}**\n"
            md += "\n"
        
        if dup_rels:
            md += "### ⚠️ Already Exists (will be skipped)\n\n"
            for r in dup_rels:
                predicate = r.get('predicate', '?').replace('_', ' ')
                md += f"- ~~{r.get('subject_name', '?')} {predicate} {r.get('object_name', '?')}~~ (duplicate)\n"
            md += "\n"
    
    # Warnings
    warnings = parsed.get('warnings', [])
    if warnings:
        md += "### ⚠️ Warnings\n\n"
        for w in warnings:
            md += f"- {w}\n"
        md += "\n"
    
    # Actions
    md += "---\n\n"
    md += "### ✅ Actions\n\n"
    md += "Comment one of the following:\n\n"
    md += "- `/approve` - Create a PR with these changes\n"
    md += "- `/edit` - I'll refine based on your feedback\n"
    md += "- `/cancel` - Discard this request\n"
    
    return md


def save_parsed_data(parsed: dict, issue_number: str):
    """Save parsed data for later PR creation."""
    output_dir = Path('.ai_requests')
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / f'issue_{issue_number}.json', 'w') as f:
        json.dump(parsed, f, indent=2)


# ============================================================================
# Main
# ============================================================================

def main():
    # Get inputs from environment
    issue_body = os.environ.get('ISSUE_BODY', '')
    issue_number = os.environ.get('ISSUE_NUMBER', 'unknown')
    api_key = os.environ.get('GROQ_API_KEY', '')
    
    if not issue_body:
        print("No issue body provided")
        sys.exit(1)
    
    # Extract the request from the issue body
    # (Issue body will have the form fields formatted by GitHub)
    request = issue_body
    
    # Process with AI or mock
    if api_key and HAS_GROQ:
        print(f"Processing with Groq AI...")
        parsed = process_with_ai(request, api_key)
    else:
        print("No API key or groq library - using mock mode")
        parsed = mock_process(request)
    
    print(f"Parsed result: {json.dumps(parsed, indent=2)}")
    
    # Generate response
    response = generate_response_markdown(parsed, issue_number)
    
    # Save for later
    save_parsed_data(parsed, issue_number)
    
    # Write response file (for GitHub Action to comment)
    with open('ai_response.md', 'w') as f:
        f.write(response)
    
    print("Response generated successfully!")


if __name__ == '__main__':
    main()
