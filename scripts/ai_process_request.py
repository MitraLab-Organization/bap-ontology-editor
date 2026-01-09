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
    """Load all current structure names for context."""
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

IMPORTANT RULES:
1. Use EXACT existing structure names when referring to parents or relationship targets
2. Generate new BAP IDs starting from {next_id} (format: BAP_XXXXXXX)
3. Only output valid JSON with this structure:

{{
  "understood": "Brief summary of what you understood",
  "structures": [
    {{
      "id": "BAP_XXXXXXX",
      "name": "Structure Name",
      "parent_name": "Existing Parent Name",
      "definition": "Brief anatomical definition"
    }}
  ],
  "relationships": [
    {{
      "subject_name": "Structure Name",
      "predicate": "innervated_by|supplied_by|develops_from|part_of|adjacent_to",
      "object_name": "Target Structure Name"
    }}
  ],
  "warnings": ["Any issues or clarifications needed"]
}}

EXISTING STRUCTURES (use these exact names):
{structures}

If a parent doesn't exist, add it to warnings.
If unsure about anatomical accuracy, add it to warnings.
"""


def process_with_ai(user_request: str, api_key: str) -> dict:
    """Process the request using Groq's free Llama model."""
    
    # Load context
    structures = load_current_structures()
    next_id = get_next_available_id()
    
    # Build prompt
    system = SYSTEM_PROMPT.format(
        next_id=next_id,
        structures='\n'.join(f"- {s}" for s in structures[:100])  # Limit for context
    )
    
    client = Groq(api_key=api_key)
    
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",  # Free and powerful!
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
        md += "### 📦 Structures to Add\n\n"
        md += "| Name | ID | Parent | Definition |\n"
        md += "|------|-----|--------|------------|\n"
        for s in structures:
            md += f"| {s.get('name', '?')} | `{s.get('id', '?')}` | {s.get('parent_name', '?')} | {s.get('definition', '-')[:50]} |\n"
        md += "\n"
    
    # Relationships
    relationships = parsed.get('relationships', [])
    if relationships:
        md += "### 🔗 Relationships to Add\n\n"
        for r in relationships:
            predicate = r.get('predicate', '?').replace('_', ' ')
            md += f"- **{r.get('subject_name', '?')}** {predicate} **{r.get('object_name', '?')}**\n"
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
