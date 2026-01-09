#!/usr/bin/env python3
"""
AI-powered ontology query processor.
Answers questions about the ontology structure and relationships.
"""

import os
import json
import sys
from pathlib import Path

try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

import yaml


def load_ontology_summary() -> dict:
    """Load a summary of the entire ontology for context."""
    summary = {
        'structures': [],
        'relationships': [],
        'hierarchy': {},
        'stats': {
            'total_structures': 0,
            'total_relationships': 0,
            'structures_by_type': {},
        }
    }
    
    # Load structures
    structures_dir = Path('structures')
    if structures_dir.exists():
        for yaml_file in structures_dir.glob('*.yaml'):
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                if data and 'structures' in data:
                    for struct in data['structures']:
                        summary['structures'].append({
                            'id': struct.get('id'),
                            'name': struct.get('name'),
                            'parent': struct.get('parent'),
                            'definition': struct.get('definition', '')[:100],
                        })
                        summary['stats']['total_structures'] += 1
                        
                        # Track by file/type
                        file_type = yaml_file.stem
                        summary['stats']['structures_by_type'][file_type] = \
                            summary['stats']['structures_by_type'].get(file_type, 0) + 1
    
    # Load relationships
    rel_dir = Path('relationships')
    if rel_dir.exists():
        for yaml_file in rel_dir.glob('*.yaml'):
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                if data and 'relationships' in data and data['relationships']:
                    for rel in data['relationships']:
                        summary['relationships'].append({
                            'subject': rel.get('subject'),
                            'predicate': rel.get('predicate'),
                            'object': rel.get('object'),
                            'type': yaml_file.stem,
                        })
                        summary['stats']['total_relationships'] += 1
    
    # Build ID to name lookup
    id_to_name = {s['id']: s['name'] for s in summary['structures']}
    summary['id_to_name'] = id_to_name
    
    return summary


def query_with_ai(question: str, summary: dict, api_key: str) -> dict:
    """Use AI to answer questions about the ontology."""
    
    # Build context
    context = f"""You are a BAP ontology assistant. Answer questions about the anatomical ontology.

ONTOLOGY STATS:
- Total structures: {summary['stats']['total_structures']}
- Total relationships: {summary['stats']['total_relationships']}
- Structure types: {json.dumps(summary['stats']['structures_by_type'])}

STRUCTURES (ID, Name, Parent):
"""
    for s in summary['structures'][:200]:  # Limit for context
        parent_name = summary['id_to_name'].get(s['parent'], s['parent'] or 'ROOT')
        context += f"- {s['id']}: {s['name']} (parent: {parent_name})\n"
    
    context += f"\nRELATIONSHIPS:\n"
    for r in summary['relationships'][:100]:  # Limit for context
        subj_name = summary['id_to_name'].get(r['subject'], r['subject'])
        obj_name = summary['id_to_name'].get(r['object'], r['object'])
        context += f"- {subj_name} {r['predicate']} {obj_name}\n"
    
    context += """

Answer the question based on this data. If the question asks for a list, provide a clear list.
If asking for hierarchy, show it as an indented tree.
If the data doesn't contain the answer, say so clearly.
"""
    
    client = Groq(api_key=api_key)
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": question}
        ],
        temperature=0.1,
        max_tokens=2000,
    )
    
    return {
        'answer': response.choices[0].message.content,
        'stats': summary['stats'],
    }


def generate_response_markdown(result: dict) -> str:
    """Generate markdown response for GitHub issue."""
    md = "## 🔍 Query Results\n\n"
    md += result['answer']
    md += "\n\n---\n"
    md += f"*Searched {result['stats']['total_structures']} structures and {result['stats']['total_relationships']} relationships*"
    return md


def main():
    issue_body = os.environ.get('ISSUE_BODY', '')
    api_key = os.environ.get('GROQ_API_KEY', '')
    
    if not issue_body:
        print("No issue body")
        sys.exit(1)
    
    # Load ontology
    print("Loading ontology summary...")
    summary = load_ontology_summary()
    print(f"Loaded {summary['stats']['total_structures']} structures")
    
    # Query with AI
    if api_key and HAS_GROQ:
        print("Querying with AI...")
        result = query_with_ai(issue_body, summary, api_key)
    else:
        result = {
            'answer': "AI not available. Please set GROQ_API_KEY.",
            'stats': summary['stats']
        }
    
    # Generate response
    response = generate_response_markdown(result)
    
    with open('ai_response.md', 'w') as f:
        f.write(response)
    
    print("Query complete!")


if __name__ == '__main__':
    main()
