#!/usr/bin/env python3
"""
Move Structure Helper Script

Safely moves a structure to a new parent in the hierarchy by:
1. Finding the structure in all YAML files
2. Checking for duplicates
3. Updating the parent reference or removing duplicates

Usage:
    python scripts/move_structure.py BAP_0000102 BAP_0012007
    python scripts/move_structure.py BAP_0000102 BAP_0012007 --dry-run
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml


# ============================================================================
# Configuration
# ============================================================================

ROOT_DIR = Path(__file__).parent.parent
STRUCTURES_DIR = ROOT_DIR / "structures"


# ============================================================================
# YAML Utilities
# ============================================================================

def load_yaml_file(filepath: Path) -> Optional[dict]:
    """Load a YAML file preserving order and comments where possible."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        return None


def save_yaml_file(filepath: Path, data: dict):
    """Save data to YAML file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


# ============================================================================
# Structure Finding
# ============================================================================

def load_all_structures() -> Dict[str, str]:
    """
    Load all structures and create ID-to-name mapping.
    
    Returns:
        Dictionary mapping structure IDs to names
    """
    id_to_name = {}
    
    yaml_files = list(STRUCTURES_DIR.glob("*.yaml")) + list(STRUCTURES_DIR.glob("*.yml"))
    
    for filepath in yaml_files:
        data = load_yaml_file(filepath)
        if not data or "structures" not in data:
            continue
        
        for struct in data["structures"]:
            struct_id = struct.get("id")
            struct_name = struct.get("name")
            if struct_id and struct_name:
                id_to_name[struct_id] = struct_name
    
    return id_to_name


def find_structure_occurrences(structure_id: str) -> List[Tuple[Path, int, dict]]:
    """
    Find all occurrences of a structure ID across YAML files.
    
    Returns:
        List of (filepath, index, structure_dict) tuples
    """
    occurrences = []
    
    yaml_files = list(STRUCTURES_DIR.glob("*.yaml")) + list(STRUCTURES_DIR.glob("*.yml"))
    
    for filepath in yaml_files:
        data = load_yaml_file(filepath)
        if not data or "structures" not in data:
            continue
        
        for idx, struct in enumerate(data["structures"]):
            if struct.get("id") == structure_id:
                occurrences.append((filepath, idx, struct))
    
    return occurrences


# ============================================================================
# Structure Movement
# ============================================================================

def move_structure(structure_id: str, new_parent_id: str, dry_run: bool = False) -> bool:
    """
    Move a structure to a new parent.
    
    Args:
        structure_id: The ID of the structure to move (e.g., BAP_0000102)
        new_parent_id: The ID of the new parent (e.g., BAP_0012007)
        dry_run: If True, only show what would be done
    
    Returns:
        True if successful, False otherwise
    """
    # Load all structures for name lookup
    id_to_name = load_all_structures()
    
    def format_parent(parent_id: Optional[str]) -> str:
        """Format parent ID with name."""
        if parent_id is None:
            return "None (root)"
        parent_name = id_to_name.get(parent_id, "Unknown")
        return f"{parent_name} ({parent_id})"
    
    print(f"\n🔍 Searching for structure {structure_id}...")
    
    occurrences = find_structure_occurrences(structure_id)
    
    if not occurrences:
        print(f"❌ Structure {structure_id} not found in any YAML file")
        return False
    
    print(f"✅ Found {len(occurrences)} occurrence(s)")
    
    # Show all occurrences
    for filepath, idx, struct in occurrences:
        parent = struct.get("parent")
        name = struct.get("name", "Unknown")
        print(f"  📄 {filepath.name}: '{name}' (parent: {format_parent(parent)})")
    
    if len(occurrences) == 1:
        # Single occurrence - update the parent
        filepath, idx, struct = occurrences[0]
        old_parent = struct.get("parent")
        
        print(f"\n📝 Updating parent:")
        print(f"   FROM: {format_parent(old_parent)}")
        print(f"   TO:   {format_parent(new_parent_id)}")
        
        if not dry_run:
            data = load_yaml_file(filepath)
            data["structures"][idx]["parent"] = new_parent_id
            save_yaml_file(filepath, data)
            print(f"✅ Updated {filepath.name}")
        else:
            print("   (DRY RUN - no changes made)")
        
        return True
    
    else:
        # Multiple occurrences - need to handle duplicates
        print(f"\n⚠️  Found {len(occurrences)} duplicate entries!")
        print("   Will keep the entry with the correct parent and remove others.")
        
        # Find which one should be kept (the one we want to update)
        keep_idx = None
        for i, (filepath, idx, struct) in enumerate(occurrences):
            parent = struct.get("parent")
            if parent == new_parent_id:
                keep_idx = i
                print(f"\n✅ Keeping entry in {filepath.name} (already has correct parent)")
                break
        
        if keep_idx is None:
            # None have the correct parent, keep the first one and update it
            keep_idx = 0
            filepath, idx, struct = occurrences[0]
            old_parent = struct.get("parent")
            print(f"\n📝 Updating {filepath.name}:")
            print(f"   FROM: {format_parent(old_parent)}")
            print(f"   TO:   {format_parent(new_parent_id)}")
            
            if not dry_run:
                data = load_yaml_file(filepath)
                data["structures"][idx]["parent"] = new_parent_id
                save_yaml_file(filepath, data)
        
        # Remove all other occurrences
        print(f"\n🗑️  Removing {len(occurrences) - 1} duplicate(s):")
        for i, (filepath, idx, struct) in enumerate(occurrences):
            if i == keep_idx:
                continue
            
            parent = struct.get("parent")
            print(f"   - {filepath.name} (parent: {format_parent(parent)})")
            
            if not dry_run:
                data = load_yaml_file(filepath)
                # Remove the structure at the given index
                del data["structures"][idx]
                save_yaml_file(filepath, data)
        
        if dry_run:
            print("\n   (DRY RUN - no changes made)")
        else:
            print("\n✅ Structure moved successfully")
        
        return True


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Safely move a structure to a new parent in the hierarchy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Move Tongue to Cranial muscles
  python scripts/move_structure.py BAP_0000102 BAP_0012007
  
  # Preview changes without applying
  python scripts/move_structure.py BAP_0000102 BAP_0012007 --dry-run
        """
    )
    parser.add_argument("structure_id", help="ID of structure to move (e.g., BAP_0000102)")
    parser.add_argument("new_parent_id", help="ID of new parent (e.g., BAP_0012007)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    
    args = parser.parse_args()
    
    success = move_structure(args.structure_id, args.new_parent_id, args.dry_run)
    
    if success and not args.dry_run:
        print("\n💡 Next steps:")
        print("   1. Run: python scripts/validate.py")
        print("   2. Review changes and commit")
        print("   3. Run: python scripts/sync_to_db.py --dry-run")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
