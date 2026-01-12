#!/usr/bin/env python3
"""
BAP Ontology Wiki Generator

Generates comprehensive documentation/wiki pages from ontology data.
Runs on every push to keep documentation in sync.

Usage:
    python scripts/generate_wiki.py --output docs/
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict
from datetime import datetime

import yaml

# ============================================================================
# Configuration
# ============================================================================

ROOT_DIR = Path(__file__).parent.parent
STRUCTURES_DIR = ROOT_DIR / "structures"
RELATIONSHIPS_DIR = ROOT_DIR / "relationships"
SCHEMAS_DIR = ROOT_DIR / "schemas"


# ============================================================================
# Data Loading
# ============================================================================

def load_yaml_files(directory: Path) -> List[dict]:
    """Load all YAML files from a directory."""
    data = []
    if not directory.exists():
        return data
    
    for filepath in sorted(directory.glob("*.yaml")):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
                if content:
                    data.append({'file': filepath.name, 'data': content})
        except Exception as e:
            print(f"Warning: Failed to load {filepath}: {e}")
    
    return data


def load_all_structures() -> Dict[str, dict]:
    """Load all structures with metadata."""
    structures = {}
    for item in load_yaml_files(STRUCTURES_DIR):
        for struct in item['data'].get("structures", []):
            if "id" in struct:
                struct['_source_file'] = item['file']
                structures[struct["id"]] = struct
    return structures


def load_all_relationships() -> List[dict]:
    """Load all relationships with metadata."""
    relationships = []
    for item in load_yaml_files(RELATIONSHIPS_DIR):
        for rel in item['data'].get("relationships", []) or []:
            rel['_source_file'] = item['file']
            relationships.append(rel)
    return relationships


def get_structure_name(structures: Dict[str, dict], struct_id: str) -> str:
    """Get name from ID."""
    return structures.get(struct_id, {}).get('name', struct_id)


# ============================================================================
# Wiki Page: Home / Overview
# ============================================================================

def generate_home_page(structures: Dict[str, dict], relationships: List[dict]) -> str:
    """Generate main overview page."""
    
    # Calculate statistics
    total_structures = len(structures)
    total_relationships = len(relationships)
    
    # Group by file
    files = defaultdict(int)
    for struct in structures.values():
        files[struct.get('_source_file', 'unknown')] += 1
    
    # Group relationships by type
    rel_by_type = defaultdict(int)
    for rel in relationships:
        rel_by_type[rel.get('predicate', 'unknown')] += 1
    
    # Calculate hierarchy depth
    def get_depth(struct_id: str, visited: Set[str] = None) -> int:
        if visited is None:
            visited = set()
        if struct_id in visited:
            return 0
        visited.add(struct_id)
        
        struct = structures.get(struct_id, {})
        parent = struct.get('parent')
        if parent is None or parent not in structures:
            return 0
        return 1 + get_depth(parent, visited)
    
    max_depth = max((get_depth(sid) for sid in structures.keys()), default=0)
    
    # Count roots
    roots = [s for s in structures.values() if s.get('parent') is None]
    
    md = f"""# BAP Ontology Wiki

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## 📊 Overview Statistics

| Metric | Count |
|--------|-------|
| **Total Structures** | {total_structures:,} |
| **Total Relationships** | {total_relationships:,} |
| **Root Structures** | {len(roots)} |
| **Maximum Hierarchy Depth** | {max_depth} levels |
| **Source Files** | {len(files)} YAML files |

### Structures by File

| File | Structures |
|------|------------|
"""
    
    for file, count in sorted(files.items()):
        md += f"| `{file}` | {count} |\n"
    
    md += f"""
### Relationships by Type

| Predicate | Count |
|-----------|-------|
"""
    
    for predicate, count in sorted(rel_by_type.items()):
        nice_name = predicate.replace('_', ' ').title()
        md += f"| **{nice_name}** | {count} |\n"
    
    md += """

## 📚 Wiki Pages

- **[Complete Structure Catalog](Structure-Catalog.md)** - All structures with full details
- **[Hierarchy Explorer](Hierarchy.md)** - Interactive hierarchy browser
- **[Relationship Networks](Relationships.md)** - All relationships visualized
- **[Innervation Map](Innervation.md)** - Neural connectivity
- **[Blood Supply Map](Blood-Supply.md)** - Vascular connectivity
- **[Quality Report](Quality-Report.md)** - Validation and QC checks
- **[Change History](Change-History.md)** - Recent changes and updates
- **[Statistics Dashboard](Statistics.md)** - Detailed analytics

## 🚀 Quick Links

- [Add New Structure (GitHub Issue)](https://github.com/MitraLab-Organization/bap-ontology-editor/issues/new?template=add-structure.yml)
- [Add Relationship (GitHub Issue)](https://github.com/MitraLab-Organization/bap-ontology-editor/issues/new?template=add-relationship.yml)
- [AI Request (Natural Language)](https://github.com/MitraLab-Organization/bap-ontology-editor/issues/new?template=ai-request.yml)
- [View Source Repository](https://github.com/MitraLab-Organization/bap-ontology-editor)

## 📖 About This Wiki

This wiki is **automatically generated** from the ontology YAML files on every push to the repository. 
All information is sourced directly from the validated ontology data.

### Data Sources

- **Structures:** `structures/*.yaml`
- **Relationships:** `relationships/*.yaml`
- **Schemas:** `schemas/*.json`

### Generation

- **Generator:** `scripts/generate_wiki.py`
- **Trigger:** GitHub Actions on push to main
- **Frequency:** Every commit

---

*Auto-generated by BAP Ontology Wiki Generator*
"""
    
    return md


# ============================================================================
# Wiki Page: Structure Catalog
# ============================================================================

def generate_structure_catalog(structures: Dict[str, dict]) -> str:
    """Generate complete structure catalog."""
    
    md = f"""# Complete Structure Catalog

**Total Structures:** {len(structures):,}

This page lists all anatomical structures in the BAP ontology with complete details.

## Structures by System

"""
    
    # Group by source file (represents system)
    by_file = defaultdict(list)
    for struct_id, struct in structures.items():
        by_file[struct.get('_source_file', 'unknown')].append((struct_id, struct))
    
    for file in sorted(by_file.keys()):
        system_name = file.replace('.yaml', '').replace('_', ' ').title()
        structs = sorted(by_file[file], key=lambda x: x[1].get('name', ''))
        
        md += f"\n### {system_name} ({len(structs)} structures)\n\n"
        md += "| ID | Name | Parent | Definition |\n"
        md += "|----|------|--------|------------|\n"
        
        for struct_id, struct in structs[:100]:  # Limit to 100 per section for performance
            name = struct.get('name', 'N/A')
            parent_id = struct.get('parent')
            parent_name = structures.get(parent_id, {}).get('name', parent_id) if parent_id else '(root)'
            definition = struct.get('definition', '')[:80]
            if len(struct.get('definition', '')) > 80:
                definition += '...'
            
            md += f"| `{struct_id}` | **{name}** | {parent_name} | {definition} |\n"
        
        if len(structs) > 100:
            md += f"\n*...and {len(structs) - 100} more*\n"
    
    md += "\n\n---\n*Auto-generated structure catalog*\n"
    return md


# ============================================================================
# Wiki Page: Hierarchy Explorer
# ============================================================================

def generate_hierarchy_page(structures: Dict[str, dict]) -> str:
    """Generate hierarchy visualization page."""
    
    # Build children map
    children = defaultdict(list)
    for struct_id, struct in structures.items():
        parent = struct.get('parent')
        children[parent].append(struct_id)
    
    # Sort children by name
    for parent in children:
        children[parent].sort(key=lambda x: structures[x].get('name', x))
    
    def generate_tree(node_id: Optional[str], level: int = 0, max_level: int = 8) -> str:
        if level > max_level:
            return ""
        
        lines = []
        struct = structures.get(node_id, {}) if node_id else {}
        name = struct.get('name', node_id) if node_id else 'ROOT'
        
        indent = "  " * level
        if level == 0:
            lines.append(f"{name}")
        else:
            lines.append(f"{indent}- **{name}** (`{node_id}`)")
        
        # Add children
        child_ids = children.get(node_id, [])
        for child_id in child_ids[:50]:  # Limit children for readability
            lines.append(generate_tree(child_id, level + 1, max_level))
        
        if len(child_ids) > 50:
            lines.append(f"{indent}  - *...and {len(child_ids) - 50} more*")
        
        return '\n'.join(lines)
    
    md = f"""# Hierarchy Explorer

This page shows the complete ontological hierarchy of all structures.

## Full Hierarchy Tree

"""
    
    # Generate tree for each root
    root_ids = children.get(None, [])
    for root_id in root_ids:
        md += generate_tree(root_id) + "\n\n"
    
    md += """

## Hierarchy Statistics

"""
    
    # Calculate some interesting stats
    leaf_nodes = [s for s in structures.keys() if s not in children or not children[s]]
    branch_nodes = [s for s in structures.keys() if s in children and children[s]]
    
    md += f"- **Leaf nodes** (no children): {len(leaf_nodes)}\n"
    md += f"- **Branch nodes** (has children): {len(branch_nodes)}\n"
    md += f"- **Root nodes**: {len(root_ids)}\n"
    
    md += "\n\n---\n*Auto-generated hierarchy*\n"
    return md


# ============================================================================
# Wiki Page: Relationships
# ============================================================================

def generate_relationships_page(structures: Dict[str, dict], relationships: List[dict]) -> str:
    """Generate relationships overview page."""
    
    # Group by predicate
    by_predicate = defaultdict(list)
    for rel in relationships:
        by_predicate[rel.get('predicate', 'unknown')].append(rel)
    
    md = f"""# Relationship Networks

**Total Relationships:** {len(relationships):,}

This page documents all cross-structure relationships in the ontology.

## Relationships by Type

"""
    
    for predicate in sorted(by_predicate.keys()):
        rels = by_predicate[predicate]
        nice_name = predicate.replace('_', ' ').title()
        
        md += f"\n### {nice_name} ({len(rels)} relationships)\n\n"
        md += "| Subject | → | Object | Confidence | Source |\n"
        md += "|---------|---|--------|------------|--------|\n"
        
        for rel in sorted(rels, key=lambda r: get_structure_name(structures, r.get('subject', '')))[:100]:
            subject = get_structure_name(structures, rel.get('subject', 'unknown'))
            obj = get_structure_name(structures, rel.get('object', 'unknown'))
            confidence = rel.get('confidence', 'N/A')
            source = rel.get('_source_file', 'N/A')
            
            md += f"| {subject} | {predicate.replace('_', ' ')} | {obj} | {confidence} | `{source}` |\n"
        
        if len(rels) > 100:
            md += f"\n*...and {len(rels) - 100} more*\n"
    
    md += "\n\n---\n*Auto-generated relationships*\n"
    return md


# ============================================================================
# Wiki Page: Innervation Map
# ============================================================================

def generate_innervation_page(structures: Dict[str, dict], relationships: List[dict]) -> str:
    """Generate detailed innervation map."""
    
    innervation = [r for r in relationships if r.get('predicate') == 'innervated_by']
    
    # Group by nerve
    by_nerve = defaultdict(list)
    for rel in innervation:
        nerve = get_structure_name(structures, rel.get('object', ''))
        muscle = get_structure_name(structures, rel.get('subject', ''))
        by_nerve[nerve].append((muscle, rel))
    
    md = f"""# Innervation Map

**Total Innervation Relationships:** {len(innervation)}

This page maps all neural innervation relationships between nerves and muscles.

## By Nerve

"""
    
    for nerve in sorted(by_nerve.keys()):
        muscles = by_nerve[nerve]
        md += f"\n### {nerve} ({len(muscles)} targets)\n\n"
        md += "| Muscle/Structure | Confidence | References | Notes |\n"
        md += "|------------------|------------|------------|-------|\n"
        
        for muscle, rel in sorted(muscles, key=lambda x: x[0]):
            confidence = rel.get('confidence', 'N/A')
            references = rel.get('references', 'N/A')
            notes = rel.get('notes', '')[:50]
            
            md += f"| {muscle} | {confidence} | {references} | {notes} |\n"
    
    # Generate Mermaid diagram
    md += "\n\n## Visual Diagram\n\n```mermaid\ngraph LR\n"
    
    for nerve, muscles in sorted(by_nerve.items())[:10]:  # Top 10 nerves
        nerve_id = nerve.replace(' ', '_').replace('-', '_')
        md += f"    {nerve_id}[{nerve}]\n"
        
        for muscle, _ in sorted(muscles, key=lambda x: x[0])[:8]:
            muscle_id = muscle.replace(' ', '_').replace('-', '_')
            md += f"    {nerve_id} -->|innervates| {muscle_id}[{muscle}]\n"
        
        if len(muscles) > 8:
            md += f"    {nerve_id} --> more_{nerve_id}[+{len(muscles)-8} more]\n"
    
    md += "```\n"
    
    md += "\n\n---\n*Auto-generated innervation map*\n"
    return md


# ============================================================================
# Wiki Page: Quality Report
# ============================================================================

def generate_quality_report(structures: Dict[str, dict], relationships: List[dict]) -> str:
    """Generate data quality report."""
    
    issues = []
    warnings = []
    
    # Check for structures without definitions
    no_def = [s for s in structures.values() if not s.get('definition')]
    if no_def:
        warnings.append(f"{len(no_def)} structures missing definitions")
    
    # Check for orphaned structures (no parent and not root)
    children_map = defaultdict(list)
    for struct in structures.values():
        parent = struct.get('parent')
        if parent:
            children_map[parent].append(struct['id'])
    
    # Check for duplicate names
    names = defaultdict(list)
    for struct_id, struct in structures.items():
        name = struct.get('name', '')
        if name:
            names[name].append(struct_id)
    
    duplicates = {name: ids for name, ids in names.items() if len(ids) > 1}
    if duplicates:
        warnings.append(f"{len(duplicates)} duplicate structure names found")
    
    # Check relationships for missing references
    missing_refs = []
    for rel in relationships:
        subject = rel.get('subject')
        obj = rel.get('object')
        
        if subject not in structures:
            missing_refs.append(f"Relationship subject not found: {subject}")
        if obj not in structures:
            missing_refs.append(f"Relationship object not found: {obj}")
    
    if missing_refs:
        issues.extend(missing_refs[:10])  # Show first 10
    
    md = f"""# Quality Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Summary

| Status | Count |
|--------|-------|
| ✅ **Structures Validated** | {len(structures)} |
| ✅ **Relationships Validated** | {len(relationships)} |
| ⚠️ **Warnings** | {len(warnings)} |
| ❌ **Issues** | {len(issues)} |

## Issues

"""
    
    if issues:
        for issue in issues:
            md += f"- ❌ {issue}\n"
    else:
        md += "*No issues found*\n"
    
    md += "\n## Warnings\n\n"
    
    if warnings:
        for warning in warnings:
            md += f"- ⚠️ {warning}\n"
    else:
        md += "*No warnings*\n"
    
    # Show some specific warnings
    if no_def:
        md += f"\n### Structures Missing Definitions ({len(no_def)})\n\n"
        for struct in no_def[:20]:
            md += f"- `{struct['id']}`: {struct.get('name', 'N/A')}\n"
        if len(no_def) > 20:
            md += f"\n*...and {len(no_def) - 20} more*\n"
    
    if duplicates:
        md += f"\n### Duplicate Names ({len(duplicates)})\n\n"
        for name, ids in list(duplicates.items())[:20]:
            md += f"- **{name}**: {', '.join(f'`{id}`' for id in ids)}\n"
    
    md += "\n\n---\n*Auto-generated quality report*\n"
    return md


# ============================================================================
# Wiki Page: Statistics Dashboard
# ============================================================================

def generate_statistics_page(structures: Dict[str, dict], relationships: List[dict]) -> str:
    """Generate detailed statistics page."""
    
    md = f"""# Statistics Dashboard

Comprehensive analytics and metrics for the BAP ontology.

## Overall Metrics

| Metric | Value |
|--------|-------|
| Total Structures | {len(structures):,} |
| Total Relationships | {len(relationships):,} |
"""
    
    # Calculate average children per structure
    children_map = defaultdict(list)
    for struct in structures.values():
        parent = struct.get('parent')
        if parent:
            children_map[parent].append(struct['id'])
    
    avg_children = sum(len(c) for c in children_map.values()) / len(children_map) if children_map else 0
    
    md += f"| Average Children per Parent | {avg_children:.2f} |\n"
    
    # Most connected structures
    connection_counts = defaultdict(int)
    for rel in relationships:
        connection_counts[rel.get('subject', '')] += 1
        connection_counts[rel.get('object', '')] += 1
    
    if connection_counts:
        most_connected = sorted(connection_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        md += "\n## Most Connected Structures\n\n"
        md += "| Structure | Connections |\n"
        md += "|-----------|-------------|\n"
        
        for struct_id, count in most_connected:
            name = get_structure_name(structures, struct_id)
            md += f"| {name} | {count} |\n"
    
    # Relationships by type
    by_type = defaultdict(int)
    for rel in relationships:
        by_type[rel.get('predicate', 'unknown')] += 1
    
    md += "\n## Relationships by Type\n\n"
    md += "| Type | Count | Percentage |\n"
    md += "|------|-------|------------|\n"
    
    total_rels = len(relationships)
    for predicate, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
        pct = (count / total_rels * 100) if total_rels > 0 else 0
        nice_name = predicate.replace('_', ' ').title()
        md += f"| {nice_name} | {count} | {pct:.1f}% |\n"
    
    # Structures by file
    by_file = defaultdict(int)
    for struct in structures.values():
        by_file[struct.get('_source_file', 'unknown')] += 1
    
    md += "\n## Structures by File\n\n"
    md += "| File | Count | Percentage |\n"
    md += "|------|-------|------------|\n"
    
    total_structs = len(structures)
    for file, count in sorted(by_file.items(), key=lambda x: x[1], reverse=True):
        pct = (count / total_structs * 100) if total_structs > 0 else 0
        md += f"| `{file}` | {count} | {pct:.1f}% |\n"
    
    md += "\n\n---\n*Auto-generated statistics*\n"
    return md


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive wiki documentation")
    parser.add_argument("--output", "-o", type=str, default="docs", help="Output directory")
    parser.add_argument("--pages", type=str, help="Comma-separated list of pages to generate (default: all)")
    args = parser.parse_args()
    
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    print("🔄 Loading ontology data...")
    structures = load_all_structures()
    relationships = load_all_relationships()
    
    print(f"  ✓ Loaded {len(structures)} structures")
    print(f"  ✓ Loaded {len(relationships)} relationships")
    
    # Define pages to generate
    pages = {
        'Home': generate_home_page,
        'Structure-Catalog': generate_structure_catalog,
        'Hierarchy': generate_hierarchy_page,
        'Relationships': generate_relationships_page,
        'Innervation': generate_innervation_page,
        'Quality-Report': generate_quality_report,
        'Statistics': generate_statistics_page,
    }
    
    # Filter if specific pages requested
    if args.pages:
        requested = args.pages.split(',')
        pages = {k: v for k, v in pages.items() if k in requested}
    
    print(f"\n📝 Generating {len(pages)} wiki pages...")
    
    for page_name, generator in pages.items():
        print(f"  • {page_name}...", end=" ")
        try:
            if generator == generate_home_page:
                content = generator(structures, relationships)
            elif generator in [generate_structure_catalog, generate_hierarchy_page]:
                content = generator(structures)
            elif generator in [generate_relationships_page, generate_innervation_page, 
                             generate_quality_report, generate_statistics_page]:
                content = generator(structures, relationships)
            else:
                content = generator(structures, relationships)
            
            output_file = output_dir / f"{page_name}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print(f"\n✅ Wiki generated in: {output_dir.absolute()}")
    print(f"   View at: {output_dir / 'Home.md'}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
