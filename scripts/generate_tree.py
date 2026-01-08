#!/usr/bin/env python3
"""
BAP Hierarchy Tree Generator

Generates a visual hierarchy tree, relationship diagrams, and stats from YAML.

Usage:
    python scripts/generate_tree.py
    python scripts/generate_tree.py --output tree.txt  # Save to file
    python scripts/generate_tree.py --update-readme    # Update README.md
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

import yaml


# ============================================================================
# Configuration
# ============================================================================

ROOT_DIR = Path(__file__).parent.parent
STRUCTURES_DIR = ROOT_DIR / "structures"
RELATIONSHIPS_DIR = ROOT_DIR / "relationships"
README_PATH = ROOT_DIR / "README.md"

# Tree drawing characters
TREE_CHARS = {
    'branch': '├── ',
    'last': '└── ',
    'pipe': '│   ',
    'space': '    ',
}


# ============================================================================
# YAML Loading
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
                    data.append(content)
        except Exception as e:
            print(f"Warning: Failed to load {filepath}: {e}")
    
    return data


def load_all_structures() -> Dict[str, dict]:
    """Load all structures from YAML files."""
    structures = {}
    for data in load_yaml_files(STRUCTURES_DIR):
        for struct in data.get("structures", []):
            if "id" in struct:
                structures[struct["id"]] = struct
    return structures


def load_all_relationships() -> Dict[str, List[dict]]:
    """Load all relationships grouped by type."""
    relationships = defaultdict(list)
    for data in load_yaml_files(RELATIONSHIPS_DIR):
        for rel in data.get("relationships", []) or []:
            predicate = rel.get("predicate", "unknown")
            relationships[predicate].append(rel)
    return dict(relationships)


def get_structure_name(structures: Dict[str, dict], id_or_name: str) -> str:
    """Get structure name from ID or return as-is if already a name."""
    if id_or_name in structures:
        return structures[id_or_name].get('name', id_or_name)
    return id_or_name


# ============================================================================
# Tree Building
# ============================================================================

def build_children_map(structures: Dict[str, dict]) -> Dict[Optional[str], List[str]]:
    """Build a map of parent_id -> list of child_ids."""
    children = defaultdict(list)
    
    for struct_id, struct in structures.items():
        parent_id = struct.get('parent')
        children[parent_id].append(struct_id)
    
    # Sort children by name for consistent output
    for parent_id in children:
        children[parent_id].sort(key=lambda x: structures[x].get('name', x))
    
    return children


def generate_tree_lines(
    structures: Dict[str, dict],
    children_map: Dict[Optional[str], List[str]],
    node_id: str,
    prefix: str = "",
    is_last: bool = True,
    max_depth: int = 10,
    current_depth: int = 0
) -> List[str]:
    """Generate tree lines for a node and its children."""
    if current_depth > max_depth:
        return []
    
    lines = []
    struct = structures.get(node_id, {})
    name = struct.get('name', node_id)
    
    # Determine connector
    if current_depth == 0:
        connector = ""
        new_prefix = ""
    else:
        connector = TREE_CHARS['last'] if is_last else TREE_CHARS['branch']
        new_prefix = prefix + (TREE_CHARS['space'] if is_last else TREE_CHARS['pipe'])
    
    lines.append(f"{prefix}{connector}{name}")
    
    # Get children
    child_ids = children_map.get(node_id, [])
    
    # Skip deprecated structures
    child_ids = [c for c in child_ids if not structures.get(c, {}).get('deprecated', False)]
    
    for i, child_id in enumerate(child_ids):
        is_last_child = (i == len(child_ids) - 1)
        lines.extend(generate_tree_lines(
            structures,
            children_map,
            child_id,
            new_prefix,
            is_last_child,
            max_depth,
            current_depth + 1
        ))
    
    return lines


def generate_full_tree(structures: Dict[str, dict], max_depth: int = 10) -> str:
    """Generate the complete hierarchy tree."""
    children_map = build_children_map(structures)
    
    # Find root nodes (parent is None)
    root_ids = children_map.get(None, [])
    
    all_lines = []
    for i, root_id in enumerate(root_ids):
        is_last = (i == len(root_ids) - 1)
        lines = generate_tree_lines(
            structures,
            children_map,
            root_id,
            "",
            is_last,
            max_depth
        )
        all_lines.extend(lines)
        if not is_last:
            all_lines.append("")  # Add spacing between roots
    
    return '\n'.join(all_lines)


def generate_subtree(structures: Dict[str, dict], root_name: str, max_depth: int = 10) -> str:
    """Generate tree for a specific subtree by name."""
    children_map = build_children_map(structures)
    
    # Find the structure by name
    root_id = None
    for struct_id, struct in structures.items():
        if struct.get('name') == root_name:
            root_id = struct_id
            break
    
    if root_id is None:
        return f"Structure '{root_name}' not found"
    
    lines = generate_tree_lines(structures, children_map, root_id, "", True, max_depth)
    return '\n'.join(lines)


# ============================================================================
# README Update
# ============================================================================

def update_readme_section(readme: str, start_marker: str, end_marker: str, content: str) -> str:
    """Update a section in the README between markers."""
    import re
    
    if start_marker not in readme:
        return readme  # Section doesn't exist, skip
    
    pattern = f"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
    replacement = f"{start_marker}\n{content}\n{end_marker}"
    return re.sub(pattern, replacement, readme, flags=re.DOTALL)


def update_readme(
    tree_content: str,
    stats_content: str = "",
    mermaid_content: str = "",
    tables_content: str = ""
):
    """Update README.md with all generated content."""
    if not README_PATH.exists():
        print(f"README not found: {README_PATH}")
        return False
    
    with open(README_PATH, 'r', encoding='utf-8') as f:
        readme = f.read()
    
    # Update hierarchy tree
    readme = update_readme_section(
        readme,
        "<!-- HIERARCHY_START -->",
        "<!-- HIERARCHY_END -->",
        f"```\n{tree_content}\n```"
    )
    
    # Update stats
    if stats_content:
        readme = update_readme_section(
            readme,
            "<!-- STATS_START -->",
            "<!-- STATS_END -->",
            stats_content
        )
    
    # Update relationship diagrams
    if mermaid_content:
        readme = update_readme_section(
            readme,
            "<!-- MERMAID_START -->",
            "<!-- MERMAID_END -->",
            mermaid_content
        )
    
    # Update relationship tables
    if tables_content:
        readme = update_readme_section(
            readme,
            "<!-- TABLES_START -->",
            "<!-- TABLES_END -->",
            tables_content
        )
    
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print(f"✓ Updated {README_PATH}")
    return True


# ============================================================================
# Statistics
# ============================================================================

def generate_stats(structures: Dict[str, dict], relationships: Dict[str, List[dict]]) -> str:
    """Generate statistics about the ontology."""
    children_map = build_children_map(structures)
    
    # Count by depth
    def count_at_depth(node_id: str, depth: int = 0) -> Dict[int, int]:
        counts = {depth: 1}
        for child_id in children_map.get(node_id, []):
            child_counts = count_at_depth(child_id, depth + 1)
            for d, c in child_counts.items():
                counts[d] = counts.get(d, 0) + c
        return counts
    
    total_counts = defaultdict(int)
    for root_id in children_map.get(None, []):
        for d, c in count_at_depth(root_id).items():
            total_counts[d] += c
    
    total_rels = sum(len(r) for r in relationships.values())
    max_depth = max(total_counts.keys()) if total_counts else 0
    
    # Build tree-style stats
    lines = [
        "📊 **Ontology Statistics**",
        "```",
        f"├── Structures: {len(structures)}",
        f"├── Hierarchy depth: {max_depth} levels",
        f"└── Relationships: {total_rels}",
    ]
    
    rel_types = sorted(relationships.keys())
    for i, rel_type in enumerate(rel_types):
        count = len(relationships[rel_type])
        prefix = "    └── " if i == len(rel_types) - 1 else "    ├── "
        nice_name = rel_type.replace('_', ' ').title()
        lines.append(f"{prefix}{nice_name}: {count}")
    
    lines.append("```")
    return '\n'.join(lines)


# ============================================================================
# Mermaid Diagrams
# ============================================================================

def generate_mermaid_innervation(structures: Dict[str, dict], relationships: Dict[str, List[dict]]) -> str:
    """Generate Mermaid diagram for innervation relationships."""
    innervation = relationships.get('innervated_by', [])
    
    if not innervation:
        return ""
    
    # Group by nerve (object)
    by_nerve = defaultdict(list)
    for rel in innervation:
        nerve = get_structure_name(structures, rel.get('object', ''))
        muscle = get_structure_name(structures, rel.get('subject', ''))
        by_nerve[nerve].append(muscle)
    
    lines = [
        "```mermaid",
        "graph LR",
    ]
    
    # Create subgraphs for major nerves
    for nerve, muscles in sorted(by_nerve.items()):
        # Create safe ID
        nerve_id = nerve.replace(' ', '_').replace('-', '_')
        lines.append(f"    {nerve_id}[{nerve}]")
        
        for muscle in sorted(muscles)[:8]:  # Limit to 8 per nerve for readability
            muscle_id = muscle.replace(' ', '_').replace('-', '_')
            lines.append(f"    {nerve_id} -->|innervates| {muscle_id}[{muscle}]")
        
        if len(muscles) > 8:
            lines.append(f"    {nerve_id} -->|innervates| {nerve_id}_more[+{len(muscles)-8} more]")
    
    lines.append("```")
    return '\n'.join(lines)


def generate_mermaid_blood_supply(structures: Dict[str, dict], relationships: Dict[str, List[dict]]) -> str:
    """Generate Mermaid diagram for blood supply relationships."""
    blood_supply = relationships.get('supplied_by', [])
    
    if not blood_supply:
        return ""
    
    # Group by artery
    by_artery = defaultdict(list)
    for rel in blood_supply:
        artery = get_structure_name(structures, rel.get('object', ''))
        structure = get_structure_name(structures, rel.get('subject', ''))
        by_artery[artery].append(structure)
    
    lines = [
        "```mermaid",
        "graph LR",
    ]
    
    for artery, supplied in sorted(by_artery.items()):
        artery_id = artery.replace(' ', '_').replace('-', '_')
        lines.append(f"    {artery_id}([{artery}])")
        
        for struct in sorted(supplied)[:6]:
            struct_id = struct.replace(' ', '_').replace('-', '_')
            lines.append(f"    {artery_id} -.->|supplies| {struct_id}[{struct}]")
    
    lines.append("```")
    return '\n'.join(lines)


# ============================================================================
# Relationship Tables
# ============================================================================

def generate_relationship_tables(structures: Dict[str, dict], relationships: Dict[str, List[dict]]) -> str:
    """Generate markdown tables for all relationships."""
    sections = []
    
    # Innervation table (grouped by nerve)
    innervation = relationships.get('innervated_by', [])
    if innervation:
        by_nerve = defaultdict(list)
        for rel in innervation:
            nerve = get_structure_name(structures, rel.get('object', ''))
            muscle = get_structure_name(structures, rel.get('subject', ''))
            by_nerve[nerve].append(muscle)
        
        lines = ["### Innervation", "", "| Nerve | Innervates |", "|-------|------------|"]
        for nerve, muscles in sorted(by_nerve.items()):
            muscle_list = ", ".join(sorted(muscles))
            lines.append(f"| {nerve} | {muscle_list} |")
        sections.append('\n'.join(lines))
    
    # Blood supply table
    blood_supply = relationships.get('supplied_by', [])
    if blood_supply:
        by_artery = defaultdict(list)
        for rel in blood_supply:
            artery = get_structure_name(structures, rel.get('object', ''))
            structure = get_structure_name(structures, rel.get('subject', ''))
            by_artery[artery].append(structure)
        
        lines = ["### Blood Supply", "", "| Artery | Supplies |", "|--------|----------|"]
        for artery, supplied in sorted(by_artery.items()):
            struct_list = ", ".join(sorted(supplied))
            lines.append(f"| {artery} | {struct_list} |")
        sections.append('\n'.join(lines))
    
    # Developmental origins
    developmental = relationships.get('develops_from', [])
    if developmental:
        lines = ["### Developmental Origins", "", "| Structure | Develops From |", "|-----------|---------------|"]
        for rel in developmental:
            structure = get_structure_name(structures, rel.get('subject', ''))
            origin = get_structure_name(structures, rel.get('object', ''))
            lines.append(f"| {structure} | {origin} |")
        sections.append('\n'.join(lines))
    
    return '\n\n'.join(sections)


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Generate hierarchy tree from YAML")
    parser.add_argument("--output", "-o", type=str, help="Output file path")
    parser.add_argument("--update-readme", action="store_true", help="Update README.md")
    parser.add_argument("--subtree", type=str, help="Generate tree for specific subtree (by name)")
    parser.add_argument("--max-depth", type=int, default=10, help="Maximum tree depth")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    args = parser.parse_args()
    
    print("Loading structures...")
    structures = load_all_structures()
    print(f"  Loaded {len(structures)} structures")
    
    print("Loading relationships...")
    relationships = load_all_relationships()
    total_rels = sum(len(r) for r in relationships.values())
    print(f"  Loaded {total_rels} relationships")
    
    if args.stats:
        print("\nStatistics:")
        print(generate_stats(structures, relationships))
        print()
    
    # Generate tree
    if args.subtree:
        tree = generate_subtree(structures, args.subtree, args.max_depth)
    else:
        tree = generate_full_tree(structures, args.max_depth)
    
    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(tree)
        print(f"✓ Saved to {args.output}")
    elif args.update_readme:
        # Generate all content
        stats = generate_stats(structures, relationships)
        
        # Generate Mermaid diagrams
        mermaid_parts = []
        innervation_mermaid = generate_mermaid_innervation(structures, relationships)
        if innervation_mermaid:
            mermaid_parts.append("#### Innervation Map\n" + innervation_mermaid)
        
        blood_mermaid = generate_mermaid_blood_supply(structures, relationships)
        if blood_mermaid:
            mermaid_parts.append("#### Blood Supply Map\n" + blood_mermaid)
        
        mermaid = '\n\n'.join(mermaid_parts)
        
        # Generate tables
        tables = generate_relationship_tables(structures, relationships)
        
        # Update README
        update_readme(tree, stats, mermaid, tables)
    else:
        print("\n" + tree)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
