#!/usr/bin/env python3
"""
Verify that lateralized relationships match the database when de-lateralized.
"""

import yaml
from pathlib import Path
from collections import defaultdict

def load_yaml_relationships():
    """Load all relationships from YAML files."""
    relationships = []
    rel_dir = Path('relationships')
    
    for yaml_file in rel_dir.glob('*.yaml'):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
            if data and 'relationships' in data and data['relationships']:
                relationships.extend(data['relationships'])
    
    return relationships

def load_all_structures():
    """Load all structures from YAML files."""
    structures = {}
    struct_dir = Path('structures')
    
    for yaml_file in struct_dir.glob('*.yaml'):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
            if data and 'structures' in data:
                for struct in data['structures']:
                    structures[struct['id']] = struct
    
    return structures

def de_lateralize_name(name: str) -> str:
    """Remove (L) or (R) suffix from name."""
    if name.endswith(' (L)') or name.endswith(' (R)'):
        return name[:-4]
    return name

def main():
    print("=" * 70)
    print("VERIFY RELATIONSHIP CONSISTENCY")
    print("=" * 70)
    print()
    
    # Load YAML data
    print("Loading YAML files...")
    structures = load_all_structures()
    relationships = load_yaml_relationships()
    print(f"  ✓ Loaded {len(structures)} structures")
    print(f"  ✓ Loaded {len(relationships)} relationships")
    
    # De-lateralize relationships
    print("\nDe-lateralizing relationships...")
    delateralized = set()
    
    for rel in relationships:
        subject_id = rel.get('subject')
        object_id = rel.get('object')
        predicate = rel.get('predicate')
        
        if subject_id in structures and object_id in structures:
            subject_name = structures[subject_id]['name']
            object_name = structures[object_id]['name']
            
            # Remove (L) and (R) suffixes
            base_subject = de_lateralize_name(subject_name)
            base_object = de_lateralize_name(object_name)
            
            # Create de-lateralized relationship tuple
            delateralized.add((base_subject, predicate, base_object))
    
    print(f"  ✓ Found {len(delateralized)} unique base relationships")
    
    # Database relationships (from your query)
    db_relationships = [
        ("Buccinatorius", "innervated_by", "Facial nerve"),
        ("Deep masseter", "innervated_by", "Trigeminal nerve"),
        ("Depressor rhinarii", "innervated_by", "Facial nerve"),
        ("Depressor septi nasi", "innervated_by", "Facial nerve"),
        ("Digastricus anterior", "innervated_by", "Trigeminal nerve"),
        ("Digastricus posterior", "innervated_by", "Facial nerve"),
        ("Dilatator nasi", "innervated_by", "Facial nerve"),
        ("Genioglossus", "innervated_by", "Hypoglossal nerve"),
        ("Genioglossus", "supplied_by", "Lingual artery"),
        ("Hyoglossus", "innervated_by", "Hypoglossal nerve"),
        ("Hyoglossus", "supplied_by", "Lingual artery"),
        ("Interscutularis", "innervated_by", "Facial nerve"),
        ("Levator anguli oris", "innervated_by", "Facial nerve"),
        ("Levator labii superioris", "innervated_by", "Facial nerve"),
        ("Levator labii superioris alaeque nasi", "innervated_by", "Facial nerve"),
        ("Levator rhinarii", "innervated_by", "Facial nerve"),
        ("Mandibuloauricularis", "innervated_by", "Facial nerve"),
        ("Masseter", "innervated_by", "Trigeminal nerve"),
        ("Masseter", "supplied_by", "Maxillary artery"),
        ("Mylohyoideus", "innervated_by", "Trigeminal nerve"),
        ("Nasalis", "innervated_by", "Facial nerve"),
        ("Occipitalis", "innervated_by", "Facial nerve"),
        ("Orbicularis oculi", "innervated_by", "Facial nerve"),
        ("Orbicularis oris", "innervated_by", "Facial nerve"),
        ("Orbito-temporo-auricularis", "innervated_by", "Facial nerve"),
        ("Platysma cervicale", "innervated_by", "Facial nerve"),
        ("Platysma myoides", "innervated_by", "Facial nerve"),
        ("Pterygoideus lateralis", "innervated_by", "Trigeminal nerve"),
        ("Pterygoideus medialis", "innervated_by", "Trigeminal nerve"),
        ("Sphincter colli profundus", "innervated_by", "Facial nerve"),
        ("Sphincter colli superficialis", "innervated_by", "Facial nerve"),
        ("Stapedius", "innervated_by", "Facial nerve"),
        ("Stylohyoideus", "innervated_by", "Facial nerve"),
        ("Stylopharyngeus", "innervated_by", "Glossopharyngeal nerve"),
        ("Superficial masseter", "innervated_by", "Trigeminal nerve"),
        ("Temporalis", "innervated_by", "Trigeminal nerve"),
        ("Temporalis", "supplied_by", "Temporal artery"),
        ("Tensor tympani", "innervated_by", "Trigeminal nerve"),
        ("Tensor veli palatini", "innervated_by", "Trigeminal nerve"),
        ("Trapezius", "innervated_by", "Accessory nerve"),
        ("Zygomaticomandibularis", "innervated_by", "Trigeminal nerve"),
        ("Zygomaticus major", "innervated_by", "Facial nerve"),
        ("Zygomaticus minor", "innervated_by", "Facial nerve"),
    ]
    
    db_set = set(db_relationships)
    
    print(f"\nDatabase relationships: {len(db_set)}")
    
    # Compare
    print("\n" + "=" * 70)
    print("COMPARISON RESULTS")
    print("=" * 70)
    
    # In YAML but not in DB
    yaml_only = delateralized - db_set
    if yaml_only:
        print(f"\n⚠️  In YAML but NOT in DB ({len(yaml_only)}):")
        for subj, pred, obj in sorted(yaml_only):
            print(f"  - {subj} --[{pred}]--> {obj}")
    
    # In DB but not in YAML
    db_only = db_set - delateralized
    if db_only:
        print(f"\n⚠️  In DB but NOT in YAML ({len(db_only)}):")
        for subj, pred, obj in sorted(db_only):
            print(f"  - {subj} --[{pred}]--> {obj}")
    
    # Matching
    matching = delateralized & db_set
    print(f"\n✅ Matching relationships: {len(matching)}/{len(db_set)}")
    
    if len(matching) == len(db_set) and len(yaml_only) == 0:
        print("\n✅ PERFECT MATCH! All DB relationships are represented in lateralized YAML.")
    elif len(db_only) > 0:
        print(f"\n⚠️  Database has {len(db_only)} relationships not in YAML")
    
    print("=" * 70)

if __name__ == '__main__':
    main()
