#!/usr/bin/env python3
"""
Parse AI response from GitHub issue comments and reconstruct the JSON data.
Used when /approve is commented but the original JSON file is not available.
"""

import os
import sys
import json
import re
from pathlib import Path

def parse_ai_comment(comment_text: str) -> dict:
    """Parse the AI response markdown comment back into structured data."""
    
    parsed = {
        "understood": "",
        "structures": [],
        "relationships": [],
        "actions": [],
        "warnings": []
    }
    
    # Extract "Understood" section
    understood_match = re.search(r'\*\*Understood:\*\*\s*(.+?)(?:\n|$)', comment_text)
    if understood_match:
        parsed['understood'] = understood_match.group(1).strip()
    
    # Extract structure updates/renames
    updates_section = re.search(
        r'### ✏️ Structure Updates/Renames\s+(.+?)(?=\n###|\n---|\Z)',
        comment_text,
        re.DOTALL
    )
    if updates_section:
        for line in updates_section.group(1).strip().split('\n'):
            # Format: "- Rename **OldName** (`ID`) to **NewName**"
            match = re.search(r'Rename\s+\*\*(.+?)\*\*\s*\(`(.+?)`\)\s+to\s+\*\*(.+?)\*\*', line)
            if match:
                old_name = match.group(1)
                struct_id = match.group(2)
                new_name = match.group(3)
                
                parsed['actions'].append({
                    'type': 'update_structure',
                    'structure_name': old_name,
                    'structure_id': struct_id,
                    'changes': {
                        'name': new_name
                    }
                })
    
    # Extract NEW structures (table format)
    struct_table = re.search(
        r'### 📦 NEW Structures to (?:Create|Add)\s+\|[^\n]+\|[^\n]+\|\s*\|(.*?)(?=\n###|\n\n---|\Z)',
        comment_text,
        re.DOTALL
    )
    if struct_table:
        for line in struct_table.group(1).strip().split('\n'):
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 5 and parts[1]:  # Has name
                    name = parts[1]
                    struct_id = parts[2].strip('`')
                    parent_match = re.search(r'(.+?)\s*\(`(.+?)`\)', parts[3])
                    if parent_match:
                        parent_name = parent_match.group(1).strip()
                        parent_id = parent_match.group(2)
                    else:
                        parent_name = parts[3]
                        parent_id = None
                    definition = parts[4] if len(parts) > 4 else ""
                    
                    parsed['actions'].append({
                        'type': 'create_structure',
                        'name': name,
                        'id': struct_id,
                        'parent_name': parent_name,
                        'parent_id': parent_id,
                        'definition': definition
                    })
    
    # Extract structure moves
    moves_section = re.search(
        r'### 🔄 Structure Moves \(Change Parent\)\s+(.+?)(?=\n###|\n---|\Z)',
        comment_text,
        re.DOTALL
    )
    if moves_section:
        for line in moves_section.group(1).strip().split('\n'):
            # Format: "- Move **StructName** (`ID`) → **NewParent** (`ParentID`)"
            match = re.search(r'Move\s+\*\*(.+?)\*\*\s*\(`(.+?)`\)\s+→\s+\*\*(.+?)\*\*\s*\(`(.+?)`\)', line)
            if match:
                struct_name = match.group(1)
                struct_id = match.group(2)
                new_parent_name = match.group(3)
                new_parent_id = match.group(4)
                
                parsed['actions'].append({
                    'type': 'move_structure',
                    'structure_name': struct_name,
                    'structure_id': struct_id,
                    'new_parent_name': new_parent_name,
                    'new_parent_id': new_parent_id
                })
    
    # Extract existing structures being used (backwards compatibility)
    existing_section = re.search(
        r'### ✅ Using Existing Structures\s+(.+?)(?=\n###|\n---|\Z)',
        comment_text,
        re.DOTALL
    )
    if existing_section:
        for line in existing_section.group(1).strip().split('\n'):
            match = re.search(r'\*\*(.+?)\*\*\s*\(`(.+?)`\)', line)
            if match:
                name = match.group(1)
                struct_id = match.group(2)
                parsed['structures'].append({
                    'name': name,
                    'id': struct_id,
                    'is_new': False
                })
    
    # Extract relationships
    rel_section = re.search(
        r'### 🔗 Relationships to Add\s+(.+?)(?=\n###|\n---|\Z)',
        comment_text,
        re.DOTALL
    )
    if rel_section:
        for line in rel_section.group(1).strip().split('\n'):
            if line.startswith('- **'):
                # Format: "**Subject (`ID`)** part of **Object (`ID`)**"
                match = re.search(
                    r'\*\*(.+?)\s*\(`(.+?)`\)\*\*\s+(.+?)\s+\*\*(.+?)\s*\(`(.+?)`\)\*\*',
                    line
                )
                if match:
                    subject_name = match.group(1)
                    subject_id = match.group(2)
                    predicate = match.group(3).strip().replace(' ', '_')
                    object_name = match.group(4)
                    object_id = match.group(5)
                    
                    parsed['actions'].append({
                        'type': 'add_relationship',
                        'subject_name': subject_name,
                        'subject_id': subject_id,
                        'predicate': predicate,
                        'object_name': object_name,
                        'object_id': object_id
                    })
    
    # Extract warnings
    warnings_section = re.search(
        r'### ⚠️ Warnings\s+(.+?)(?=\n###|\n---|\Z)',
        comment_text,
        re.DOTALL
    )
    if warnings_section:
        for line in warnings_section.group(1).strip().split('\n'):
            if line.startswith('- '):
                parsed['warnings'].append(line[2:])
    
    return parsed


def fetch_issue_comments_via_api(issue_number: str) -> list:
    """Fetch issue comments using GitHub CLI."""
    import subprocess
    
    result = subprocess.run(
        ['gh', 'api', f'repos/{{owner}}/{{repo}}/issues/{issue_number}/comments'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        print(f"Failed to fetch comments: {result.stderr}")
        return []


def main():
    issue_number = os.environ.get('ISSUE_NUMBER', '')
    
    if not issue_number:
        print("No issue number provided")
        sys.exit(1)
    
    print(f"Fetching AI response from issue #{issue_number}...")
    
    # Fetch comments from GitHub
    comments = fetch_issue_comments_via_api(issue_number)
    
    if not comments:
        print("No comments found")
        sys.exit(1)
    
    # Find the AI bot comment (should contain "🤖 AI Analysis")
    ai_comment = None
    for comment in comments:
        body = comment.get('body', '')
        if '🤖 AI Analysis' in body or 'AI Analysis' in body:
            ai_comment = body
            break
    
    if not ai_comment:
        print("No AI response comment found")
        sys.exit(1)
    
    print("Found AI response, parsing...")
    parsed = parse_ai_comment(ai_comment)
    
    # Save to expected location
    output_dir = Path('.ai_requests')
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f'issue_{issue_number}.json'
    with open(output_file, 'w') as f:
        json.dump(parsed, f, indent=2)
    
    print(f"✓ Parsed and saved to {output_file}")
    print(f"  - {len(parsed['actions'])} actions")
    print(f"  - {len(parsed['warnings'])} warnings")


if __name__ == '__main__':
    main()
