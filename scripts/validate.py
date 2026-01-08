#!/usr/bin/env python3
"""
BAP Ontology Validator

Validates YAML structure and relationship files for:
1. Schema compliance (JSON Schema validation)
2. Referential integrity (all referenced IDs exist)
3. Hierarchy consistency (no cycles, valid parents)
4. Relationship validity (subjects/objects exist)

Usage:
    python scripts/validate.py
    python scripts/validate.py --strict  # Fail on warnings too
    python scripts/validate.py --json report.json  # Output JSON report
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
from dataclasses import dataclass, field

import yaml
try:
    import jsonschema
except ImportError:
    jsonschema = None
    print("Warning: jsonschema not installed. Schema validation disabled.")


# ============================================================================
# Configuration
# ============================================================================

ROOT_DIR = Path(__file__).parent.parent
STRUCTURES_DIR = ROOT_DIR / "structures"
RELATIONSHIPS_DIR = ROOT_DIR / "relationships"
SCHEMAS_DIR = ROOT_DIR / "schemas"


# ============================================================================
# Report Classes
# ============================================================================

@dataclass
class ValidationIssue:
    level: str  # "error" or "warning"
    category: str
    message: str
    file: Optional[str] = None
    line: Optional[int] = None
    
    def to_dict(self) -> dict:
        return {
            "level": self.level,
            "category": self.category,
            "message": self.message,
            "file": self.file,
            "line": self.line
        }


@dataclass
class ValidationReport:
    issues: List[ValidationIssue] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)
    
    def add_error(self, category: str, message: str, file: str = None):
        self.issues.append(ValidationIssue("error", category, message, file))
    
    def add_warning(self, category: str, message: str, file: str = None):
        self.issues.append(ValidationIssue("warning", category, message, file))
    
    @property
    def errors(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.level == "error"]
    
    @property
    def warnings(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.level == "warning"]
    
    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0
    
    def to_dict(self) -> dict:
        return {
            "valid": self.is_valid,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "stats": self.stats,
            "issues": [i.to_dict() for i in self.issues]
        }
    
    def print_report(self):
        print("\n" + "=" * 70)
        print("🔍 BAP ONTOLOGY VALIDATION REPORT")
        print("=" * 70)
        
        print("\n📊 STATISTICS:")
        for key, value in self.stats.items():
            print(f"  {key}: {value}")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for i, err in enumerate(self.errors, 1):
                loc = f" ({err.file})" if err.file else ""
                print(f"  {i}. [{err.category}] {err.message}{loc}")
        else:
            print("\n✅ No errors found!")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for i, warn in enumerate(self.warnings[:20], 1):
                loc = f" ({warn.file})" if warn.file else ""
                print(f"  {i}. [{warn.category}] {warn.message}{loc}")
            if len(self.warnings) > 20:
                print(f"  ... and {len(self.warnings) - 20} more warnings")
        
        print("\n" + "=" * 70)
        status = "✅ PASSED" if self.is_valid else "❌ FAILED"
        print(f"Result: {status}")
        print("=" * 70 + "\n")


# ============================================================================
# YAML Loading
# ============================================================================

def load_yaml_file(filepath: Path) -> Optional[dict]:
    """Load a YAML file and return its contents."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        return None
    except FileNotFoundError:
        return None


def load_all_structures(report: ValidationReport) -> Dict[str, dict]:
    """Load all structure definitions from YAML files."""
    structures = {}
    
    if not STRUCTURES_DIR.exists():
        report.add_error("FileSystem", f"Structures directory not found: {STRUCTURES_DIR}")
        return structures
    
    yaml_files = list(STRUCTURES_DIR.glob("*.yaml")) + list(STRUCTURES_DIR.glob("*.yml"))
    
    for filepath in yaml_files:
        data = load_yaml_file(filepath)
        if data is None:
            report.add_error("YAML", f"Failed to parse {filepath.name}")
            continue
        
        if "structures" not in data:
            report.add_warning("Schema", f"No 'structures' key in {filepath.name}")
            continue
        
        for struct in data.get("structures", []):
            if "id" not in struct:
                report.add_error("Schema", f"Structure missing 'id' in {filepath.name}")
                continue
            
            struct_id = struct["id"]
            if struct_id in structures:
                report.add_error("Duplicate", f"Duplicate structure ID: {struct_id}", filepath.name)
            
            structures[struct_id] = {
                **struct,
                "_source_file": filepath.name
            }
    
    report.stats["Total structures"] = len(structures)
    return structures


def load_all_relationships(report: ValidationReport) -> List[dict]:
    """Load all relationship definitions from YAML files."""
    relationships = []
    
    if not RELATIONSHIPS_DIR.exists():
        report.add_warning("FileSystem", f"Relationships directory not found: {RELATIONSHIPS_DIR}")
        return relationships
    
    yaml_files = list(RELATIONSHIPS_DIR.glob("*.yaml")) + list(RELATIONSHIPS_DIR.glob("*.yml"))
    
    for filepath in yaml_files:
        data = load_yaml_file(filepath)
        if data is None:
            report.add_error("YAML", f"Failed to parse {filepath.name}")
            continue
        
        rels = data.get("relationships") or []  # Handle None case
        for rel in rels:
            if rel is not None:  # Skip None entries
                rel["_source_file"] = filepath.name
                relationships.append(rel)
    
    report.stats["Total relationships"] = len(relationships)
    return relationships


# ============================================================================
# Schema Validation
# ============================================================================

def validate_schema(data: dict, schema_path: Path, report: ValidationReport, source_file: str):
    """Validate data against JSON schema."""
    if jsonschema is None:
        return
    
    if not schema_path.exists():
        report.add_warning("Schema", f"Schema file not found: {schema_path}")
        return
    
    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        
        jsonschema.validate(data, schema)
    except jsonschema.ValidationError as e:
        report.add_error("Schema", f"Schema validation failed: {e.message}", source_file)
    except json.JSONDecodeError as e:
        report.add_error("Schema", f"Invalid JSON schema: {e}", str(schema_path))


# ============================================================================
# Referential Integrity Checks
# ============================================================================

def check_hierarchy_integrity(structures: Dict[str, dict], report: ValidationReport):
    """Check that all parent references are valid."""
    for struct_id, struct in structures.items():
        parent = struct.get("parent")
        if parent is not None and parent not in structures:
            report.add_error(
                "Hierarchy",
                f"Structure '{struct.get('name', struct_id)}' references non-existent parent: {parent}",
                struct.get("_source_file")
            )


def check_relationship_integrity(
    relationships: List[dict],
    structures: Dict[str, dict],
    report: ValidationReport
):
    """Check that all relationship references are valid."""
    for rel in relationships:
        subject = rel.get("subject")
        obj = rel.get("object")
        source_file = rel.get("_source_file")
        
        if subject and subject not in structures:
            report.add_error(
                "Relationship",
                f"Relationship subject not found: {subject}",
                source_file
            )
        
        if obj and obj not in structures:
            report.add_error(
                "Relationship",
                f"Relationship object not found: {obj}",
                source_file
            )


# ============================================================================
# Hierarchy Cycle Detection
# ============================================================================

def check_hierarchy_cycles(structures: Dict[str, dict], report: ValidationReport):
    """Detect cycles in the hierarchy (A -> B -> C -> A)."""
    # Build parent map
    parent_map = {}
    for struct_id, struct in structures.items():
        parent = struct.get("parent")
        if parent is not None:
            parent_map[struct_id] = parent
    
    # Check for cycles using path traversal
    cycles_found = []
    for start_id in parent_map:
        visited = set()
        current = start_id
        path = [current]
        
        while current in parent_map and current not in visited:
            visited.add(current)
            current = parent_map[current]
            path.append(current)
            
            if current == start_id:
                cycles_found.append(path)
                break
    
    for cycle in cycles_found:
        names = [structures.get(sid, {}).get("name", sid) for sid in cycle]
        report.add_error("Hierarchy", f"Cycle detected: {' -> '.join(names)}")


# ============================================================================
# Data Quality Checks
# ============================================================================

def check_data_quality(structures: Dict[str, dict], report: ValidationReport):
    """Check for data quality issues."""
    for struct_id, struct in structures.items():
        name = struct.get("name", "")
        abbrev = struct.get("abbreviation", "")
        source_file = struct.get("_source_file")
        
        # Check for missing names
        if not name:
            report.add_error("DataQuality", f"Structure {struct_id} is missing a name", source_file)
        
        # Check for very short names (might be abbreviations)
        if name and len(name) < 3:
            report.add_warning("DataQuality", f"Very short name: '{name}' ({struct_id})", source_file)
        
        # Check for very long abbreviations (might be swapped with name)
        if abbrev and len(abbrev) > 15:
            report.add_warning("DataQuality", f"Long abbreviation ({len(abbrev)} chars): {struct_id}", source_file)
        
        # Check ID format
        if not struct_id.startswith("BAP_") or len(struct_id) != 11:
            report.add_warning("DataQuality", f"Non-standard ID format: {struct_id}", source_file)


def check_orphan_structures(structures: Dict[str, dict], report: ValidationReport):
    """Check for structures that aren't connected to the hierarchy."""
    # Find root structures (parent is null)
    roots = {sid for sid, s in structures.items() if s.get("parent") is None}
    
    # Find structures that have a parent
    has_parent = {sid for sid, s in structures.items() if s.get("parent") is not None}
    
    # Structures that are neither roots nor have parents
    orphans = set(structures.keys()) - roots - has_parent
    
    if orphans:
        for orphan in list(orphans)[:5]:
            struct = structures[orphan]
            report.add_warning(
                "Hierarchy",
                f"Structure '{struct.get('name', orphan)}' has no parent defined",
                struct.get("_source_file")
            )


def check_duplicate_relationships(relationships: List[dict], report: ValidationReport):
    """Check for duplicate relationships."""
    seen = set()
    for rel in relationships:
        key = (rel.get("subject"), rel.get("predicate"), rel.get("object"))
        if key in seen:
            report.add_warning(
                "Duplicate",
                f"Duplicate relationship: {key[0]} {key[1]} {key[2]}",
                rel.get("_source_file")
            )
        seen.add(key)


# ============================================================================
# Main Validation
# ============================================================================

def validate_all(strict: bool = False) -> ValidationReport:
    """Run all validation checks."""
    report = ValidationReport()
    
    print("Loading structures...")
    structures = load_all_structures(report)
    
    print("Loading relationships...")
    relationships = load_all_relationships(report)
    
    # Schema validation
    print("Validating schemas...")
    structure_schema = SCHEMAS_DIR / "structure.schema.json"
    relationship_schema = SCHEMAS_DIR / "relationship.schema.json"
    
    for filepath in STRUCTURES_DIR.glob("*.yaml"):
        data = load_yaml_file(filepath)
        if data:
            validate_schema(data, structure_schema, report, filepath.name)
    
    for filepath in RELATIONSHIPS_DIR.glob("*.yaml"):
        data = load_yaml_file(filepath)
        if data:
            validate_schema(data, relationship_schema, report, filepath.name)
    
    # Referential integrity
    print("Checking referential integrity...")
    check_hierarchy_integrity(structures, report)
    check_relationship_integrity(relationships, structures, report)
    
    # Hierarchy checks
    print("Checking hierarchy...")
    check_hierarchy_cycles(structures, report)
    check_orphan_structures(structures, report)
    
    # Data quality
    print("Checking data quality...")
    check_data_quality(structures, report)
    check_duplicate_relationships(relationships, report)
    
    # Count statistics
    report.stats["Structure files"] = len(list(STRUCTURES_DIR.glob("*.yaml")))
    report.stats["Relationship files"] = len(list(RELATIONSHIPS_DIR.glob("*.yaml")))
    report.stats["Root structures"] = sum(1 for s in structures.values() if s.get("parent") is None)
    
    return report


def main():
    parser = argparse.ArgumentParser(description="Validate BAP ontology YAML files")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings too")
    parser.add_argument("--json", type=str, help="Output report to JSON file")
    parser.add_argument("--quiet", "-q", action="store_true", help="Minimal output")
    args = parser.parse_args()
    
    report = validate_all(strict=args.strict)
    
    if not args.quiet:
        report.print_report()
    
    if args.json:
        with open(args.json, 'w') as f:
            json.dump(report.to_dict(), f, indent=2)
        print(f"Report saved to: {args.json}")
    
    # Exit code
    if args.strict:
        return 0 if (report.is_valid and len(report.warnings) == 0) else 1
    return 0 if report.is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
