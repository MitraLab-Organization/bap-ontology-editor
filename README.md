# BAP Marmoset Head Ontology

A collaborative repository for managing the Brain Architecture Project (BAP) 
Marmoset (Callithrix jacchus) head anatomical ontology.

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

- **Common name:** Marmoset
- **Scientific name:** Callithrix jacchus
- **NCBI Taxonomy:** 9483
- **Focus:** Head and neck anatomy

<!-- STATS_START -->
📊 **Ontology Statistics**
```
├── Structures: 805
├── Hierarchy depth: 11 levels
└── Relationships: 0
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
cd bap-ontology-marmoset

# Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Validate
python scripts/validate.py

# Generate OWL
python scripts/generate_owl.py --output bap-marmoset.owl
```

## Repository Structure

```
bap-ontology-marmoset/
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
