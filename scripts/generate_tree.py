#!/usr/bin/env python3
"""
BAP Hierarchy Tree Generator

Generates a visual hierarchy tree from YAML definitions and updates the README.

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

def update_readme(tree_content: str):
    """Update README.md with the hierarchy tree."""
    if not README_PATH.exists():
        print(f"README not found: {README_PATH}")
        return False
    
    with open(README_PATH, 'r', encoding='utf-8') as f:
        readme = f.read()
    
    # Markers for the hierarchy section
    start_marker = "<!-- HIERARCHY_START -->"
    end_marker = "<!-- HIERARCHY_END -->"
    
    if start_marker not in readme:
        # Add section if it doesn't exist
        hierarchy_section = f"""
## Current Hierarchy

{start_marker}
```
{tree_content}
```
{end_marker}
"""
        # Insert before ## Quick Start or at the end
        if "## Quick Start" in readme:
            readme = readme.replace("## Quick Start", hierarchy_section + "\n## Quick Start")
        else:
            readme += hierarchy_section
    else:
        # Replace existing section
        import re
        pattern = f"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
        replacement = f"{start_marker}\n```\n{tree_content}\n```\n{end_marker}"
        readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
    
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print(f"✓ Updated {README_PATH}")
    return True


# ============================================================================
# Statistics
# ============================================================================

def generate_stats(structures: Dict[str, dict]) -> str:
    """Generate statistics about the hierarchy."""
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
    
    stats = []
    stats.append(f"Total structures: {len(structures)}")
    stats.append(f"Root nodes: {len(children_map.get(None, []))}")
    stats.append(f"Max depth: {max(total_counts.keys()) if total_counts else 0}")
    
    return '\n'.join(stats)


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
    
    if args.stats:
        print("\nStatistics:")
        print(generate_stats(structures))
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
        update_readme(tree)
    else:
        print("\n" + tree)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
