#!/usr/bin/env python3
"""
BAP Database Sync

Synchronizes YAML structure and relationship definitions to the PostgreSQL database.
This script is designed to be run by GitHub Actions on merge to main.

Usage:
    python scripts/sync_to_db.py
    python scripts/sync_to_db.py --dry-run  # Preview changes without applying
    python scripts/sync_to_db.py --force    # Skip confirmation prompts

Environment Variables:
    DB_HOST     - Database host (default: localhost)
    DB_PORT     - Database port (default: 5567)
    DB_NAME     - Database name (default: groundtruth)
    DB_USER     - Database user (default: groundtruth)
    DB_PASSWORD - Database password (default: groundtruth)
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass

import yaml

try:
    import psycopg2
    from psycopg2.extras import execute_values
except ImportError:
    print("Error: psycopg2 not installed. Run: pip install psycopg2-binary")
    sys.exit(1)


# ============================================================================
# Configuration
# ============================================================================

ROOT_DIR = Path(__file__).parent.parent
STRUCTURES_DIR = ROOT_DIR / "structures"
RELATIONSHIPS_DIR = ROOT_DIR / "relationships"

# Database configuration from environment
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '5567')),
    'database': os.getenv('DB_NAME', 'groundtruth'),
    'user': os.getenv('DB_USER', 'groundtruth'),
    'password': os.getenv('DB_PASSWORD', 'groundtruth'),
}

# BAP Nomenclature ID (you may need to adjust this)
BAP_NOMENCLATURE_ID = 1  # Adjust based on your database


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class SyncStats:
    structures_added: int = 0
    structures_updated: int = 0
    structures_unchanged: int = 0
    hierarchies_added: int = 0
    hierarchies_updated: int = 0
    relationships_added: int = 0
    relationships_updated: int = 0
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
    
    def print_summary(self):
        print("\n" + "=" * 50)
        print("📊 SYNC SUMMARY")
        print("=" * 50)
        print(f"  Structures added:    {self.structures_added}")
        print(f"  Structures updated:  {self.structures_updated}")
        print(f"  Structures unchanged:{self.structures_unchanged}")
        print(f"  Hierarchies added:   {self.hierarchies_added}")
        print(f"  Hierarchies updated: {self.hierarchies_updated}")
        print(f"  Relationships added: {self.relationships_added}")
        print(f"  Relationships updated:{self.relationships_updated}")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for err in self.errors[:10]:
                print(f"  - {err}")
        else:
            print("\n✅ No errors!")
        print("=" * 50)


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


def load_all_relationships() -> List[dict]:
    """Load all relationships from YAML files."""
    relationships = []
    for data in load_yaml_files(RELATIONSHIPS_DIR):
        rels = data.get("relationships") or []  # Handle None case
        relationships.extend([r for r in rels if r is not None])
    return relationships


# ============================================================================
# Database Operations
# ============================================================================

def get_db_connection():
    """Get database connection."""
    return psycopg2.connect(**DB_CONFIG)


def bap_id_to_db_id(bap_id: str) -> int:
    """Extract numeric ID from BAP ID (BAP_0000015 -> 15)."""
    # Remove BAP_ prefix and leading zeros, convert to int
    numeric_part = bap_id.replace("BAP_", "")
    return int(numeric_part)  # int() handles leading zeros automatically


def get_existing_structures(conn) -> Dict[str, dict]:
    """Get existing structures from database."""
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, abbreviation, description, external_id, iri
        FROM anatomical_structure
        WHERE nomenclature_id = %s
    """, (BAP_NOMENCLATURE_ID,))
    
    structures = {}
    for row in cur.fetchall():
        db_id = row[0]
        # Convert back to BAP ID format
        bap_id = f"BAP_{db_id:07d}"
        structures[bap_id] = {
            'db_id': db_id,
            'name': row[1],
            'abbreviation': row[2],
            'description': row[3],
            'external_id': row[4],
            'iri': row[5]
        }
    
    return structures


def get_existing_hierarchies(conn) -> Dict[int, int]:
    """Get existing hierarchies (child_id -> parent_id)."""
    cur = conn.cursor()
    cur.execute("""
        SELECT anatomical_entity_id, parent_entity_id
        FROM anatomical_structure_hierarchy
    """)
    return {row[0]: row[1] for row in cur.fetchall()}


def get_relationship_type_map(conn) -> Dict[str, int]:
    """Get relationship type name -> ID mapping."""
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM relationship_type")
    return {row[1].lower(): row[0] for row in cur.fetchall()}


def sync_structures(
    conn,
    yaml_structures: Dict[str, dict],
    existing_structures: Dict[str, dict],
    stats: SyncStats,
    dry_run: bool = False
) -> Dict[str, int]:
    """Sync structures to database. Returns BAP_ID -> db_id mapping."""
    cur = conn.cursor()
    id_map = {}
    
    for bap_id, struct in yaml_structures.items():
        db_id = bap_id_to_db_id(bap_id)
        id_map[bap_id] = db_id
        
        name = struct.get('name', '')
        abbreviation = struct.get('abbreviation')
        description = struct.get('definition')
        external_id = struct.get('external_id')
        iri = f"http://purl.obolibrary.org/obo/{bap_id}"
        
        if bap_id in existing_structures:
            existing = existing_structures[bap_id]
            # Check if update needed
            if (existing['name'] != name or
                existing['abbreviation'] != abbreviation or
                existing['description'] != description or
                existing['external_id'] != external_id):
                
                print(f"    ~ UPDATE structure: {name} (ID:{db_id})")
                if not dry_run:
                    cur.execute("""
                        UPDATE anatomical_structure
                        SET name = %s, abbreviation = %s, description = %s, 
                            external_id = %s, iri = %s
                        WHERE id = %s
                    """, (name, abbreviation, description, external_id, iri, db_id))
                stats.structures_updated += 1
            else:
                stats.structures_unchanged += 1
        else:
            # Insert new structure
            print(f"    + ADD structure: {name} (ID:{db_id})")
            if not dry_run:
                cur.execute("""
                    INSERT INTO anatomical_structure 
                    (id, nomenclature_id, name, abbreviation, description, external_id, iri)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        name = EXCLUDED.name,
                        abbreviation = EXCLUDED.abbreviation,
                        description = EXCLUDED.description,
                        external_id = EXCLUDED.external_id,
                        iri = EXCLUDED.iri
                """, (db_id, BAP_NOMENCLATURE_ID, name, abbreviation, description, external_id, iri))
            stats.structures_added += 1
    
    return id_map


def sync_hierarchies(
    conn,
    yaml_structures: Dict[str, dict],
    id_map: Dict[str, int],
    existing_hierarchies: Dict[int, int],
    stats: SyncStats,
    dry_run: bool = False
):
    """Sync hierarchy relationships to database."""
    cur = conn.cursor()
    
    # Get the next available ID for hierarchy table
    cur.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM anatomical_structure_hierarchy")
    next_id = cur.fetchone()[0]
    
    for bap_id, struct in yaml_structures.items():
        parent_bap_id = struct.get('parent')
        child_db_id = id_map.get(bap_id)
        struct_name = struct.get('name', bap_id)
        
        if child_db_id is None:
            continue
        
        if parent_bap_id is None:
            # Root node - parent is NULL (convention used by other atlases)
            parent_db_id = None
            parent_name = "(NULL - root node)"
        elif parent_bap_id in id_map:
            parent_db_id = id_map[parent_bap_id]
            parent_name = yaml_structures.get(parent_bap_id, {}).get('name', parent_bap_id)
        else:
            stats.errors.append(f"Parent not found for {bap_id}: {parent_bap_id}")
            continue
        
        existing_parent = existing_hierarchies.get(child_db_id)
        
        if existing_parent is None:
            # Insert new hierarchy
            print(f"    + ADD hierarchy: {struct_name} (ID:{child_db_id}) -> parent: {parent_name} (ID:{parent_db_id})")
            if not dry_run:
                cur.execute("""
                    INSERT INTO anatomical_structure_hierarchy 
                    (id, anatomical_entity_id, parent_entity_id)
                    VALUES (%s, %s, %s)
                """, (next_id, child_db_id, parent_db_id))
            next_id += 1
            stats.hierarchies_added += 1
        elif existing_parent != parent_db_id:
            # Update hierarchy
            print(f"    ~ UPDATE hierarchy: {struct_name} (ID:{child_db_id}) -> parent: {parent_name} (ID:{parent_db_id}) [was: {existing_parent}]")
            if not dry_run:
                cur.execute("""
                    UPDATE anatomical_structure_hierarchy
                    SET parent_entity_id = %s
                    WHERE anatomical_entity_id = %s
                """, (parent_db_id, child_db_id))
            stats.hierarchies_updated += 1


def sync_relationships(
    conn,
    yaml_relationships: List[dict],
    id_map: Dict[str, int],
    yaml_structures: Dict[str, dict],
    rel_type_map: Dict[str, int],
    stats: SyncStats,
    dry_run: bool = False
):
    """Sync relationships to database."""
    cur = conn.cursor()
    
    for rel in yaml_relationships:
        subject_bap = rel.get('subject')
        predicate = rel.get('predicate')
        object_bap = rel.get('object')
        
        if not all([subject_bap, predicate, object_bap]):
            continue
        
        subject_id = id_map.get(subject_bap)
        object_id = id_map.get(object_bap)
        rel_type_id = rel_type_map.get(predicate.lower())
        
        # Get names for logging
        subject_name = yaml_structures.get(subject_bap, {}).get('name', subject_bap)
        object_name = yaml_structures.get(object_bap, {}).get('name', object_bap)
        
        if subject_id is None:
            stats.errors.append(f"Subject not found: {subject_bap}")
            continue
        if object_id is None:
            stats.errors.append(f"Object not found: {object_bap}")
            continue
        if rel_type_id is None:
            stats.errors.append(f"Relationship type not found: {predicate}")
            continue
        
        # Check if relationship exists
        cur.execute("""
            SELECT id FROM anatomical_structure_relationship
            WHERE entity1_id = %s AND entity2_id = %s AND relationship_type_id = %s
        """, (subject_id, object_id, rel_type_id))
        
        existing = cur.fetchone()
        
        if existing is None:
            print(f"    + ADD relationship: {subject_name} --[{predicate}]--> {object_name}")
            if not dry_run:
                cur.execute("""
                    INSERT INTO anatomical_structure_relationship
                    (entity1_id, entity2_id, relationship_type_id, notes)
                    VALUES (%s, %s, %s, %s)
                """, (subject_id, object_id, rel_type_id, rel.get('notes')))
            stats.relationships_added += 1
        # Note: We don't update existing relationships to avoid conflicts


# ============================================================================
# Main Sync Function
# ============================================================================

def run_sync(dry_run: bool = False, force: bool = False) -> SyncStats:
    """Run the full sync process."""
    stats = SyncStats()
    
    print("Loading YAML definitions...")
    yaml_structures = load_all_structures()
    yaml_relationships = load_all_relationships()
    print(f"  Structures: {len(yaml_structures)}")
    print(f"  Relationships: {len(yaml_relationships)}")
    
    if not yaml_structures:
        print("No structures found. Aborting.")
        return stats
    
    print(f"\nConnecting to database at {DB_CONFIG['host']}:{DB_CONFIG['port']}...")
    
    try:
        conn = get_db_connection()
    except Exception as e:
        stats.errors.append(f"Database connection failed: {e}")
        return stats
    
    try:
        print("Loading existing data...")
        existing_structures = get_existing_structures(conn)
        existing_hierarchies = get_existing_hierarchies(conn)
        rel_type_map = get_relationship_type_map(conn)
        print(f"  Existing structures: {len(existing_structures)}")
        print(f"  Existing hierarchies: {len(existing_hierarchies)}")
        print(f"  Relationship types: {len(rel_type_map)}")
        
        if dry_run:
            print("\n🔍 DRY RUN MODE - No changes will be made")
        
        if not force and not dry_run:
            print(f"\nThis will sync {len(yaml_structures)} structures to the database.")
            response = input("Continue? [y/N] ")
            if response.lower() != 'y':
                print("Aborted.")
                return stats
        
        print("\nSyncing structures...")
        id_map = sync_structures(conn, yaml_structures, existing_structures, stats, dry_run)
        
        print("Syncing hierarchies...")
        sync_hierarchies(conn, yaml_structures, id_map, existing_hierarchies, stats, dry_run)
        
        print("Syncing relationships...")
        sync_relationships(conn, yaml_relationships, id_map, yaml_structures, rel_type_map, stats, dry_run)
        
        if not dry_run:
            conn.commit()
            print("\n✓ Changes committed to database")
        else:
            conn.rollback()
            print("\n✓ Dry run complete (no changes made)")
        
    except Exception as e:
        conn.rollback()
        stats.errors.append(f"Sync failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()
    
    return stats


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Sync YAML definitions to database")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    parser.add_argument("--force", "-f", action="store_true", help="Skip confirmation prompts")
    args = parser.parse_args()
    
    stats = run_sync(dry_run=args.dry_run, force=args.force)
    stats.print_summary()
    
    return 0 if not stats.errors else 1


if __name__ == "__main__":
    sys.exit(main())
