# BAP Mouse Head Ontology

A collaborative repository for managing the Brain Architecture Project (BAP) mouse head anatomical ontology.

## Overview

This repository provides a human-readable way to manage:
- **Anatomical structures** (muscles, nerves, blood vessels)
- **Hierarchies** (parent-child relationships)
- **Biological relationships** (innervation, blood supply, developmental origins)

Changes are validated automatically via GitHub Actions and generate OWL files for use in WebProtégé and other tools.

## Current Hierarchy

<!-- HIERARCHY_START -->
```
Body
├── Appendages
│   ├── Forelimb
│   │   ├── clavicle
│   │   └── scapula
│   ├── Hindlimb
│   └── Tail
├── Head
│   ├── Cavities and passages
│   │   ├── Nasal cavity
│   │   │   ├── nasal
│   │   │   └── vomer
│   │   ├── Nasal sinuses
│   │   ├── Oral cavity
│   │   └── Tongue
│   │       ├── Genioglossus
│   │       ├── Hyoglossus
│   │       ├── Inferior longitudinal
│   │       ├── Palatoglossus
│   │       ├── Styloglossus
│   │       ├── Superior longitudinal
│   │       ├── Transverse
│   │       └── Vertical
│   ├── Endocrine and exocrine system
│   │   ├── Palatal submucosa
│   │   └── Parotid glands
│   ├── Integumentary system
│   │   ├── External ear
│   │   │   ├── Pinna
│   │   │   └── external acoustic meatus
│   │   ├── Skin
│   │   └── Whiskers
│   ├── Musculoskeletal system
│   │   ├── Cranial muscles
│   │   │   ├── Buccinatorius
│   │   │   ├── Ceratohyoideus
│   │   │   ├── Depressor rhinarii
│   │   │   ├── Depressor septi nasi
│   │   │   ├── Digastricus anterior
│   │   │   ├── Digastricus posterior
│   │   │   ├── Dilatator nasi
│   │   │   ├── Frontalis
│   │   │   ├── Geniohyoideus
│   │   │   ├── Interscutularis
│   │   │   ├── Levator anguli oris
│   │   │   ├── Levator labii superioris
│   │   │   ├── Levator labii superioris alaeque nasi
│   │   │   ├── Levator rhinarii
│   │   │   ├── Mandibuloauricularis
│   │   │   ├── Masseter
│   │   │   │   ├── Deep masseter
│   │   │   │   ├── Superficial masseter
│   │   │   │   └── Zygomaticomandibularis
│   │   │   ├── Mylohyoideus
│   │   │   ├── Nasalis
│   │   │   ├── Occipitalis
│   │   │   ├── Orbicularis oculi
│   │   │   ├── Orbicularis oris
│   │   │   ├── Orbito-temporo-auricularis
│   │   │   ├── Platysma cervicale
│   │   │   ├── Platysma myoides
│   │   │   ├── Pterygoideus lateralis
│   │   │   ├── Pterygoideus medialis
│   │   │   ├── Sphincter colli profundus
│   │   │   ├── Sphincter colli superficialis
│   │   │   ├── Sternohyoideus
│   │   │   ├── Stylohyoideus
│   │   │   ├── Stylopharyngeus
│   │   │   ├── Temporalis
│   │   │   │   ├── Temporalis lateralis
│   │   │   │   └── Temporalis medialis
│   │   │   ├── Zygomaticus major
│   │   │   └── Zygomaticus minor
│   │   └── Cranium
│   │       ├── Neurocranium
│   │       │   ├── basisphenoid
│   │       │   ├── ethmoid
│   │       │   ├── frontal
│   │       │   ├── interparietal
│   │       │   ├── occipital
│   │       │   ├── parietal
│   │       │   └── presphenoid
│   │       └── Viscerocranium
│   │           ├── Jaw apparatus
│   │           ├── lacrimal
│   │           ├── mandible
│   │           ├── maxilla
│   │           ├── palatine
│   │           ├── premaxilla
│   │           ├── sphenoid
│   │           ├── squamosal
│   │           └── zygomatic
│   ├── Nervous system
│   │   ├── Central nervous system
│   │   │   └── Brain
│   │   └── Peripheral nervous system
│   │       └── Cranial Nerves
│   │           ├── Abducens nerve
│   │           ├── Accessory nerve
│   │           ├── Facial nerve
│   │           ├── Glossopharyngeal nerve
│   │           ├── Hypoglossal nerve
│   │           ├── Oculomotor nerve
│   │           ├── Olfactory nerve
│   │           ├── Optic nerve
│   │           ├── Terminal nerve
│   │           ├── Trigeminal nerve
│   │           ├── Trochlear nerve
│   │           ├── Vagus nerve
│   │           └── Vestibulocochlear nerve
│   ├── Sense organs
│   │   ├── Eye
│   │   │   ├── inferior oblique
│   │   │   ├── lateral rectus
│   │   │   ├── levator palpebrae superioris
│   │   │   ├── medial rectus
│   │   │   ├── retractor bulbi
│   │   │   ├── superior oblique muscle
│   │   │   │   └── superior oblique tendon
│   │   │   │       └── trochlea
│   │   │   └── superior rectus
│   │   ├── Gustatory epithelium
│   │   ├── Inner ear
│   │   │   ├── incus
│   │   │   ├── internal acoustic meatus
│   │   │   ├── malleus
│   │   │   ├── stapes
│   │   │   └── tympanic
│   │   ├── Olfactory epithelium
│   │   └── Whisker barrels
│   └── Vascular system
│       ├── Arteries
│       │   ├── Lingual artery
│       │   ├── Maxillary artery
│       │   └── Temporal artery
│       ├── Lymphatics
│       └── Veins
├── Neck
│   ├── Cavities and passages
│   │   ├── Larynx
│   │   │   ├── Arytenoideus
│   │   │   ├── Cricoarytenoideus alaris
│   │   │   ├── Cricoarytenoideus lateralis
│   │   │   ├── Cricoarytenoideus posterior
│   │   │   ├── Thyroarytenoideus
│   │   │   ├── arytenoid cartilage
│   │   │   ├── cricoid cartilage
│   │   │   ├── epiglottis
│   │   │   ├── laryngeal alar cartilage
│   │   │   └── thyroid cartilage
│   │   └── Pharynx
│   │       ├── Constrictor pharyngis inferior
│   │       ├── Constrictor pharyngis medius
│   │       ├── Constrictor pharyngis superior
│   │       ├── Esophagus
│   │       ├── Levator veli palatini
│   │       ├── Palatopharyngeus
│   │       ├── Pterygopharyngeus
│   │       ├── Salpingopharyngeus
│   │       ├── Tensor veli palatini
│   │       ├── hyoid bone
│   │       └── sternofacialis left
│   ├── Endocrine and exocrine system
│   │   └── Thyroid gland
│   ├── Integumentary system
│   │   └── Skin
│   ├── Musculoskeletal system
│   │   ├── Neck muscles
│   │   │   ├── Cleidomastoideus
│   │   │   ├── Cleidooccipitalis
│   │   │   ├── Cricothyroideus
│   │   │   ├── Jugulohyoideus
│   │   │   ├── Omohyoideus
│   │   │   ├── Sternomastoideus
│   │   │   ├── Sternothyroideus
│   │   │   ├── Thyrohyoideus
│   │   │   └── Trapezius
│   │   │       ├── Acromiotrapezius
│   │   │       └── Spinotrapezius
│   │   └── Neck skeletal system
│   │       └── cervical vertebra
│   ├── Nervous system
│   │   ├── Central nervous system
│   │   │   └── Spinal Cord
│   │   └── Peripheral nervous system
│   │       └── Cervical nerves
│   └── Vascular system
│       ├── Arteries
│       ├── Lymphatics
│       └── Veins
└── Trunk
    ├── Abdomen
    ├── Pelvis
    └── Thorax
        └── sternum
```
<!-- HIERARCHY_END -->

## Repository Structure

```
bap-ontology/
├── structures/           # Anatomical structure definitions
│   ├── muscles.yaml      # Muscle structures + hierarchies
│   ├── nerves.yaml       # Nerve structures
│   └── vessels.yaml      # Blood vessel structures
├── relationships/        # Cross-structure relationships
│   ├── innervation.yaml  # Nerve → muscle connections
│   ├── blood_supply.yaml # Vessel → structure connections
│   └── developmental.yaml# Developmental origins
├── schemas/              # JSON Schema for validation
│   └── structure.schema.json
├── scripts/              # Build and validation scripts
│   ├── validate.py       # Validate YAML files
│   └── generate_owl.py   # Generate OWL from YAML
└── .github/workflows/    # CI/CD automation
    ├── validate.yml      # Validate on PR
    └── generate.yml      # Generate OWL on merge
```

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_ORG/bap-ontology.git
cd bap-ontology
```

### 2. Edit structures

Edit YAML files directly in `structures/` or `relationships/`:

```yaml
# structures/muscles.yaml
structures:
  - id: BAP_0001000
    name: Head muscle
    parent: null  # Root structure
    definition: Muscles of the head region

  - id: BAP_0001100
    name: Masseter
    parent: BAP_0001000
    definition: Primary muscle of mastication
    abbreviation: MAS
```

### 3. Create a Pull Request

1. Create a branch: `git checkout -b add-temporalis-muscle`
2. Make your changes
3. Push and open a PR
4. GitHub Actions validates your changes
5. Get review and merge

### 4. Generated OWL file

After merge, the `bap-mousehead.owl` file is automatically generated and available in the releases.

## YAML Format Reference

### Structure Definition

```yaml
structures:
  - id: BAP_0000001          # Required: Unique IRI identifier
    name: Structure Name      # Required: Human-readable name
    parent: BAP_0000000       # Optional: Parent structure ID (null for roots)
    definition: Description   # Optional: IAO definition text
    abbreviation: ABBR        # Optional: Short form
    external_id: UBERON_0001  # Optional: Cross-reference to external ontology
```

### Relationship Definition

```yaml
relationships:
  - subject: BAP_0001100      # Required: Source structure ID
    predicate: innervated_by  # Required: Relationship type
    object: BAP_0002001       # Required: Target structure ID
    reference: PMID:12345     # Optional: Citation
```

### Supported Relationship Types

| Predicate | OBO IRI | Description |
|-----------|---------|-------------|
| `part_of` | BFO_0000050 | Structure is part of another |
| `innervated_by` | RO_0002005 | Receives neural input from |
| `supplied_by` | RO_0002178 | Receives blood supply from |
| `develops_from` | RO_0002202 | Developmental origin |
| `adjacent_to` | RO_0002220 | Spatially contiguous |

## Local Development

### Prerequisites

- Python 3.9+
- PyYAML, jsonschema

### Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Validate locally

```bash
python scripts/validate.py
```

### Generate OWL locally

```bash
python scripts/generate_owl.py --output bap-mousehead.owl
```

## Access Control

This repository uses GitHub's built-in access controls:

- **Collaborators**: Can push branches and create PRs
- **Branch protection**: Main branch requires PR reviews
- **CODEOWNERS**: Specific reviewers for critical files

To request access, contact the repository administrators.

## Contributing

1. Create a feature branch from `main`
2. Make your changes to YAML files
3. Run `python scripts/validate.py` locally
4. Open a Pull Request
5. Address review feedback
6. Merge after approval

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) - Brain Architecture Project
