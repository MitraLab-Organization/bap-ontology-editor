#!/usr/bin/env python3
"""
Bootstrap a new species ontology from the BAP template.

Usage:
    python scripts/bootstrap_species.py --species "Marmoset" \
                                       --scientific "Callithrix jacchus" \
                                       --common "Common Marmoset" \
                                       --ncbi 9483 \
                                       --id-start 1000000

This will:
1. Clear existing structure data
2. Create base structure files with species info
3. Update README and documentation
4. Configure OWL generation for the species
"""

import argparse
import yaml
import re
from pathlib import Path
from datetime import date


SPECIES_ID_RANGES = {
    "mouse": (0, 999999),
    "marmoset": (1000000, 1999999),
    "zebrafinch": (2000000, 2999999),
    "macaque": (3000000, 3999999),
    "rat": (4000000, 4999999),
    "human": (5000000, 5999999),
}


def get_id_range(species_key: str, custom_start: int = None):
    """Get ID range for species."""
    if custom_start:
        return (custom_start, custom_start + 999999)
    
    species_lower = species_key.lower()
    if species_lower in SPECIES_ID_RANGES:
        return SPECIES_ID_RANGES[species_lower]
    
    # Default to 6000000 range for unknown species
    return (6000000, 6999999)


def create_base_structure(species: str, scientific: str, ncbi: str, id_start: int):
    """Create base body regions structure."""
    return {
        'metadata': {
            'category': 'regions',
            'description': f'{species} body regions',
            'version': '1.0.0',
            'last_modified': str(date.today()),
            'species': scientific,
            'ncbi_taxon': str(ncbi)
        },
        'structures': [
            {
                'id': f'BAP_{id_start:07d}',
                'name': 'Body',
                'parent': None,
                'definition': f'Entire body of {species.lower()}'
            },
            {
                'id': f'BAP_{id_start+1:07d}',
                'name': 'Head',
                'parent': f'BAP_{id_start:07d}',
                'definition': f'Cranial region of {species.lower()}'
            },
            {
                'id': f'BAP_{id_start+2:07d}',
                'name': 'Neck',
                'parent': f'BAP_{id_start:07d}',
                'definition': f'Cervical region of {species.lower()}'
            },
            {
                'id': f'BAP_{id_start+3:07d}',
                'name': 'Trunk',
                'parent': f'BAP_{id_start:07d}',
                'definition': f'Torso of {species.lower()}'
            },
        ]
    }


def create_empty_structure(category: str, species: str, scientific: str):
    """Create empty structure file with metadata."""
    return {
        'metadata': {
            'category': category,
            'description': f'{species} {category}',
            'version': '1.0.0',
            'last_modified': str(date.today()),
            'species': scientific
        },
        'structures': []
    }


def create_empty_relationships(rel_type: str, species: str, scientific: str):
    """Create empty relationship file with metadata."""
    return {
        'metadata': {
            'type': rel_type,
            'description': f'{species} {rel_type} relationships',
            'version': '1.0.0',
            'last_modified': str(date.today()),
            'species': scientific
        },
        'relationships': []
    }


def update_readme(species: str, scientific: str, ncbi: str):
    """Generate updated README content."""
    return f"""# BAP {species} Head Ontology

A collaborative repository for managing the Brain Architecture Project (BAP) 
{species} ({scientific}) head anatomical ontology.

## 📚 [**View the Auto-Generated Wiki →**](https://mitralab-organization.github.io/bap-ontology-editor/)

Complete documentation with detailed reports, statistics, and visualizations - 
**automatically updated on every push!**

## Overview

This repository provides a human-readable way to manage:
- **Anatomical structures** (muscles, nerves, blood vessels, bones)
- **Hierarchies** (parent-child relationships)
- **Biological relationships** (innervation, blood supply, developmental origins)

Changes are validated automatically via GitHub Actions and generate OWL files 
for use in WebProtégé and other tools.

## Species Information

- **Common name:** {species}
- **Scientific name:** {scientific}
- **NCBI Taxonomy:** {ncbi}
- **Focus:** Head and neck anatomy

<!-- STATS_START -->
📊 **Ontology Statistics**
```
├── Structures: 0 (initial setup)
├── Hierarchy depth: 1 level
└── Relationships: 0 (initial setup)
```
<!-- STATS_END -->

## Getting Started

### Add Structures via Issue Templates

1. Go to [Issues → New Issue](../../issues/new/choose)
2. Select **"➕ Add New Structure"**
3. Fill out the form and submit
4. Wait for approval and automatic PR creation

### Local Development

```bash
# Clone and setup
git clone <this-repo>
cd bap-ontology-{species.lower()}

# Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Validate
python scripts/validate.py

# Generate OWL
python scripts/generate_owl.py --output bap-{species.lower()}.owl
```

## Repository Structure

```
bap-ontology-{species.lower()}/
├── structures/           # Anatomical structure definitions
│   ├── body_regions.yaml # Base hierarchy
│   ├── muscles.yaml      # Muscle structures
│   ├── nerves.yaml       # Nerve structures
│   ├── vessels.yaml      # Blood vessel structures
│   └── skeletal.yaml     # Bone structures
├── relationships/        # Cross-structure relationships
│   ├── innervation.yaml  # Nerve → muscle connections
│   ├── blood_supply.yaml # Vessel → structure connections
│   └── developmental.yaml# Developmental origins
├── schemas/              # JSON Schema for validation
├── scripts/              # Build and validation scripts
└── .github/workflows/    # CI/CD automation
```

## Contributing

1. Create a feature branch from `main`
2. Make your changes to YAML files
3. Run `python scripts/validate.py` locally
4. Open a Pull Request
5. Address review feedback
6. Merge after approval

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) - Brain Architecture Project
"""


def update_generate_owl(species: str, scientific: str, ncbi: str, repo_root: Path):
    """Update generate_owl.py with species information."""
    owl_script = repo_root / "scripts" / "generate_owl.py"
    
    if not owl_script.exists():
        print(f"Warning: {owl_script} not found, skipping OWL script update")
        return
    
    content = owl_script.read_text()
    
    # Update key variables
    species_lower = species.lower().replace(' ', '-')
    
    replacements = {
        r'ONTOLOGY_IRI = ".*?"': f'ONTOLOGY_IRI = "https://bap.org/ontology/{species_lower}/bap-{species_lower}.owl"',
        r'ONTOLOGY_TITLE = ".*?"': f'ONTOLOGY_TITLE = "BAP {species} Head Anatomy Ontology"',
        r'ONTOLOGY_DESCRIPTION = ".*?"': f'ONTOLOGY_DESCRIPTION = "Anatomical ontology for {species} ({scientific}) head region"',
    }
    
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)
    
    # Add species metadata section if not present
    if 'SPECIES_NAME' not in content:
        species_block = f'''
# Species metadata
SPECIES_NAME = "{scientific}"
SPECIES_COMMON = "{species}"
NCBI_TAXON = "{ncbi}"
'''
        # Insert after ONTOLOGY_DESCRIPTION
        content = re.sub(
            r'(ONTOLOGY_DESCRIPTION = ".*?")',
            r'\1' + species_block,
            content
        )
    
    owl_script.write_text(content)
    print(f"✓ Updated {owl_script}")


def bootstrap_species(
    species: str,
    scientific: str,
    common: str,
    ncbi: str,
    id_start: int = None,
    dry_run: bool = False
):
    """Bootstrap a new species ontology."""
    
    # Get repository root
    repo_root = Path(__file__).parent.parent
    
    # Determine ID range
    if not id_start:
        id_start, _ = get_id_range(species, id_start)
    
    print(f"\n{'='*60}")
    print(f"Bootstrapping {species} Ontology")
    print(f"{'='*60}")
    print(f"Scientific name: {scientific}")
    print(f"Common name: {common}")
    print(f"NCBI Taxon: {ncbi}")
    print(f"ID range: BAP_{id_start:07d} - BAP_{id_start+999999:07d}")
    print(f"{'='*60}\n")
    
    if dry_run:
        print("DRY RUN - No files will be modified\n")
    
    # 1. Create base structure files
    structures_dir = repo_root / "structures"
    
    files_to_create = {
        'body_regions.yaml': create_base_structure(species, scientific, ncbi, id_start),
        'muscles.yaml': create_empty_structure('muscles', species, scientific),
        'nerves.yaml': create_empty_structure('nerves', species, scientific),
        'vessels.yaml': create_empty_structure('vessels', species, scientific),
        'skeletal.yaml': create_empty_structure('bones', species, scientific),
    }
    
    print("Creating structure files:")
    for filename, data in files_to_create.items():
        filepath = structures_dir / filename
        if not dry_run:
            with open(filepath, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        print(f"  ✓ {filepath}")
    
    # 2. Create empty relationship files
    relationships_dir = repo_root / "relationships"
    
    rel_files = {
        'innervation.yaml': create_empty_relationships('innervation', species, scientific),
        'blood_supply.yaml': create_empty_relationships('blood_supply', species, scientific),
        'developmental.yaml': create_empty_relationships('developmental', species, scientific),
    }
    
    print("\nCreating relationship files:")
    for filename, data in rel_files.items():
        filepath = relationships_dir / filename
        if not dry_run:
            with open(filepath, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        print(f"  ✓ {filepath}")
    
    # 3. Update README
    readme_path = repo_root / "README.md"
    print(f"\nUpdating README:")
    if not dry_run:
        readme_path.write_text(update_readme(species, scientific, ncbi))
    print(f"  ✓ {readme_path}")
    
    # 4. Update generate_owl.py
    print(f"\nUpdating OWL generation script:")
    if not dry_run:
        update_generate_owl(species, scientific, ncbi, repo_root)
    else:
        print(f"  (would update scripts/generate_owl.py)")
    
    # 5. Summary
    print(f"\n{'='*60}")
    print("Bootstrap Complete!")
    print(f"{'='*60}\n")
    
    print("Next steps:")
    print("1. Review and commit the changes:")
    print("   git add .")
    print(f"   git commit -m 'Bootstrap {species} ontology'")
    print("\n2. Validate the structure:")
    print("   python scripts/validate.py")
    print("\n3. Start adding structures via:")
    print("   - Issue templates (no code required)")
    print("   - Direct YAML editing")
    print("   - Bulk import scripts")
    print("\n4. Generate outputs:")
    print("   python scripts/generate_tree.py")
    print(f"   python scripts/generate_owl.py --output bap-{species.lower()}.owl")
    print("   python scripts/generate_wiki.py")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Bootstrap a new species ontology",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Marmoset
  python scripts/bootstrap_species.py \\
    --species "Marmoset" \\
    --scientific "Callithrix jacchus" \\
    --common "Common Marmoset" \\
    --ncbi 9483 \\
    --id-start 1000000

  # Zebrafinch
  python scripts/bootstrap_species.py \\
    --species "Zebrafinch" \\
    --scientific "Taeniopygia guttata" \\
    --common "Zebra Finch" \\
    --ncbi 59729 \\
    --id-start 2000000
        """
    )
    
    parser.add_argument(
        '--species',
        required=True,
        help='Species common name (e.g., "Marmoset")'
    )
    parser.add_argument(
        '--scientific',
        required=True,
        help='Scientific name (e.g., "Callithrix jacchus")'
    )
    parser.add_argument(
        '--common',
        help='Alternative common name (defaults to --species)'
    )
    parser.add_argument(
        '--ncbi',
        required=True,
        help='NCBI Taxonomy ID (e.g., "9483")'
    )
    parser.add_argument(
        '--id-start',
        type=int,
        help='Starting ID for species range (default: auto-assign)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without modifying files'
    )
    
    args = parser.parse_args()
    
    common_name = args.common or args.species
    
    bootstrap_species(
        species=args.species,
        scientific=args.scientific,
        common=common_name,
        ncbi=args.ncbi,
        id_start=args.id_start,
        dry_run=args.dry_run
    )


if __name__ == '__main__':
    main()
