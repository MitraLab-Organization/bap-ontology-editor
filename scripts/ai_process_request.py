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
    
    print(f"Loaded {len(structures)} existing structures for context")
    
    # Build prompt with ALL structures
    system = SYSTEM_PROMPT.format(
        next_id=next_id,
        structures='\n'.join(f"- {s}" for s in structures)  # Include ALL structures
    )
    
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
    
    return json.loads(response.choices[0].message.content)


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
        md += "### 🔗 Relationships to Add\n\n"
        for r in relationships:
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
