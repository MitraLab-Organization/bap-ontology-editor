#!/usr/bin/env python3
"""
Quality Control checks for the ontology.
Finds issues like orphans, missing definitions, circular refs, etc.
"""

import os
import json
import sys
from pathlib import Path
from collections import defaultdict

import yaml


def load_all_structures() -> list[dict]:
    """Load all structures from YAML files."""
    structures = []
    structures_dir = Path('structures')
    
    for yaml_file in structures_dir.glob('*.yaml'):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
            if data and 'structures' in data:
                for struct in data['structures']:
                    struct['_file'] = yaml_file.name
                    structures.append(struct)
    
    return structures


def load_all_relationships() -> list[dict]:
    """Load all relationships from YAML files."""
    relationships = []
    rel_dir = Path('relationships')
    
    for yaml_file in rel_dir.glob('*.yaml'):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
            if data and 'relationships' in data and data['relationships']:
                for rel in data['relationships']:
                    rel['_file'] = yaml_file.name
                    relationships.append(rel)
    
    return relationships


def check_orphans(structures: list[dict]) -> list[dict]:
    """Find structures without valid parents."""
    issues = []
    all_ids = {s['id'] for s in structures}
    
    for struct in structures:
        parent = struct.get('parent')
        if parent and parent not in all_ids:
            issues.append({
                'type': 'orphan',
                'severity': 'error',
                'structure': struct['name'],
                'id': struct['id'],
                'message': f"Parent '{parent}' not found",
                'file': struct['_file']
            })
    
    return issues


def check_missing_definitions(structures: list[dict]) -> list[dict]:
    """Find structures without definitions."""
    issues = []
    
    for struct in structures:
        if not struct.get('definition'):
            issues.append({
                'type': 'missing_definition',
                'severity': 'warning',
                'structure': struct['name'],
                'id': struct['id'],
                'message': "No definition provided",
                'file': struct['_file']
            })
    
    return issues


def check_duplicate_names(structures: list[dict]) -> list[dict]:
    """Find duplicate structure names."""
    issues = []
    name_counts = defaultdict(list)
    
    for struct in structures:
        name_counts[struct['name'].lower()].append(struct)
    
    for name, structs in name_counts.items():
        if len(structs) > 1:
            ids = [s['id'] for s in structs]
            issues.append({
                'type': 'duplicate_name',
                'severity': 'warning',
                'structure': structs[0]['name'],
                'id': ids[0],
                'message': f"Name appears {len(structs)} times: {ids}",
                'file': structs[0]['_file']
            })
    
    return issues


def check_circular_references(structures: list[dict]) -> list[dict]:
    """Check for circular parent references."""
    issues = []
    id_to_struct = {s['id']: s for s in structures}
    
    for struct in structures:
        visited = set()
        current = struct
        
        while current:
            if current['id'] in visited:
                issues.append({
                    'type': 'circular_reference',
                    'severity': 'error',
                    'structure': struct['name'],
                    'id': struct['id'],
                    'message': f"Circular reference detected: {' -> '.join(visited)} -> {current['id']}",
                    'file': struct['_file']
                })
                break
            
            visited.add(current['id'])
            parent_id = current.get('parent')
            
            if parent_id and parent_id in id_to_struct:
                current = id_to_struct[parent_id]
            else:
                break
    
    return issues


def check_broken_relationships(structures: list[dict], relationships: list[dict]) -> list[dict]:
    """Find relationships referencing non-existent structures."""
    issues = []
    all_ids = {s['id'] for s in structures}
    
    for rel in relationships:
        if rel.get('subject') and rel['subject'] not in all_ids:
            issues.append({
                'type': 'broken_relationship',
                'severity': 'error',
                'structure': rel['subject'],
                'id': rel['subject'],
                'message': f"Subject '{rel['subject']}' not found in structures",
                'file': rel['_file']
            })
        
        if rel.get('object') and rel['object'] not in all_ids:
            issues.append({
                'type': 'broken_relationship',
                'severity': 'error',
                'structure': rel['object'],
                'id': rel['object'],
                'message': f"Object '{rel['object']}' not found in structures",
                'file': rel['_file']
            })
    
    return issues


def check_structures_no_relationships(structures: list[dict], relationships: list[dict]) -> list[dict]:
    """Find structures with no relationships at all."""
    issues = []
    
    # Get all IDs that appear in relationships
    related_ids = set()
    for rel in relationships:
        related_ids.add(rel.get('subject'))
        related_ids.add(rel.get('object'))
    
    for struct in structures:
        if struct['id'] not in related_ids:
            issues.append({
                'type': 'no_relationships',
                'severity': 'info',
                'structure': struct['name'],
                'id': struct['id'],
                'message': "Structure has no relationships",
                'file': struct['_file']
            })
    
    return issues


def check_unused_structures(structures: list[dict], relationships: list[dict]) -> list[dict]:
    """Find leaf structures with no children and no relationships."""
    issues = []
    
    # Get all parent IDs
    parent_ids = {s.get('parent') for s in structures if s.get('parent')}
    
    # Get all IDs in relationships
    related_ids = set()
    for rel in relationships:
        related_ids.add(rel.get('subject'))
        related_ids.add(rel.get('object'))
    
    for struct in structures:
        # If not a parent and not in any relationship
        if struct['id'] not in parent_ids and struct['id'] not in related_ids:
            issues.append({
                'type': 'unused',
                'severity': 'info',
                'structure': struct['name'],
                'id': struct['id'],
                'message': "Structure has no children and no relationships",
                'file': struct['_file']
            })
    
    return issues


def run_all_checks(checks: list[str] = None) -> dict:
    """Run specified QC checks."""
    structures = load_all_structures()
    relationships = load_all_relationships()
    
    all_issues = []
    
    check_functions = {
        'orphan': lambda: check_orphans(structures),
        'missing_definition': lambda: check_missing_definitions(structures),
        'duplicate_name': lambda: check_duplicate_names(structures),
        'circular_reference': lambda: check_circular_references(structures),
        'broken_relationship': lambda: check_broken_relationships(structures, relationships),
        'no_relationships': lambda: check_structures_no_relationships(structures, relationships),
        'unused': lambda: check_unused_structures(structures, relationships),
    }
    
    # Map template options to check names
    check_mapping = {
        'Orphan structures': 'orphan',
        'Structures without definitions': 'missing_definition',
        'Duplicate names': 'duplicate_name',
        'Circular references': 'circular_reference',
        'Broken relationship references': 'broken_relationship',
        'Structures with no relationships': 'no_relationships',
        'Unused structures': 'unused',
    }
    
    if checks:
        # Run only specified checks
        for check_name in checks:
            mapped = check_mapping.get(check_name, check_name)
            if mapped in check_functions:
                all_issues.extend(check_functions[mapped]())
    else:
        # Run all checks
        for check_func in check_functions.values():
            all_issues.extend(check_func())
    
    return {
        'issues': all_issues,
        'stats': {
            'total_structures': len(structures),
            'total_relationships': len(relationships),
            'total_issues': len(all_issues),
            'errors': len([i for i in all_issues if i['severity'] == 'error']),
            'warnings': len([i for i in all_issues if i['severity'] == 'warning']),
            'info': len([i for i in all_issues if i['severity'] == 'info']),
        }
    }


def generate_report_markdown(result: dict) -> str:
    """Generate markdown report."""
    md = "## 🔬 QC Report\n\n"
    
    stats = result['stats']
    md += f"**Scanned:** {stats['total_structures']} structures, {stats['total_relationships']} relationships\n\n"
    
    if stats['total_issues'] == 0:
        md += "✅ **No issues found!**\n"
        return md
    
    md += f"**Found {stats['total_issues']} issues:**\n"
    md += f"- 🔴 Errors: {stats['errors']}\n"
    md += f"- 🟡 Warnings: {stats['warnings']}\n"
    md += f"- 🔵 Info: {stats['info']}\n\n"
    
    # Group by type
    by_type = defaultdict(list)
    for issue in result['issues']:
        by_type[issue['type']].append(issue)
    
    for issue_type, issues in by_type.items():
        md += f"### {issue_type.replace('_', ' ').title()} ({len(issues)})\n\n"
        
        # Show first 10
        for issue in issues[:10]:
            severity_icon = {'error': '🔴', 'warning': '🟡', 'info': '🔵'}[issue['severity']]
            md += f"- {severity_icon} **{issue['structure']}** (`{issue['id']}`): {issue['message']}\n"
        
        if len(issues) > 10:
            md += f"- *...and {len(issues) - 10} more*\n"
        
        md += "\n"
    
    return md


def main():
    issue_body = os.environ.get('ISSUE_BODY', '')
    
    # Parse which checks to run from issue body
    checks_to_run = []
    if 'Orphan structures' in issue_body:
        checks_to_run.append('orphan')
    if 'Structures without definitions' in issue_body:
        checks_to_run.append('missing_definition')
    if 'Duplicate names' in issue_body:
        checks_to_run.append('duplicate_name')
    if 'Circular references' in issue_body:
        checks_to_run.append('circular_reference')
    if 'Broken relationship references' in issue_body:
        checks_to_run.append('broken_relationship')
    if 'Structures with no relationships' in issue_body:
        checks_to_run.append('no_relationships')
    if 'Unused structures' in issue_body:
        checks_to_run.append('unused')
    
    print(f"Running QC checks: {checks_to_run or 'all'}")
    
    result = run_all_checks(checks_to_run if checks_to_run else None)
    
    print(f"Found {result['stats']['total_issues']} issues")
    
    report = generate_report_markdown(result)
    
    with open('ai_response.md', 'w') as f:
        f.write(report)
    
    # Also save JSON for potential automation
    with open('qc_report.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print("QC complete!")


if __name__ == '__main__':
    main()
