# Species Adaptation Guide

This guide explains how to adapt the BAP Ontology Editor for a **different species** while keeping the same anatomical domain (muscles, nerves, vessels, bones, etc.).

**Current:** Mouse (Mus musculus)  
**Examples:** Marmoset, Zebrafinch, Rat, Macaque, Human, etc.

---

## Quick Overview

### What Stays the Same ✓
- **Structure categories:** muscles, nerves, vessels, bones, organs, regions
- **Relationship types:** innervated_by, supplied_by, develops_from, etc.
- **Schemas:** Structure and relationship schemas work as-is
- **Scripts:** All Python scripts work without changes
- **Workflows:** GitHub Actions work as-is
- **AI system:** Works with any anatomical structure

### What Changes ✗
- **Species-specific anatomy:** Different structures, hierarchies, relationships
- **Identifier ranges:** (optional) Different ID ranges per species
- **Repository name/branding:** Documentation and titles
- **Data files:** Different YAML content

---

## Two Deployment Models

### Model A: Separate Repository Per Species (Recommended)
**Best for:** Independent projects, different teams, species-specific focus

```
bap-ontology-editor-mouse/      ← Current repo
bap-ontology-editor-marmoset/   ← New repo
bap-ontology-editor-zebrafinch/ ← New repo
```

**Pros:**
- Clean separation of data
- Independent version control
- Species-specific documentation
- Easier collaboration per species

**Cons:**
- Code duplication (scripts/schemas)
- Updates need to be synced
- Multiple deployments

### Model B: Multi-Species Single Repository
**Best for:** Comparative anatomy, shared team, unified management

```
bap-ontology-editor/
├── species/
│   ├── mouse/
│   │   ├── structures/
│   │   ├── relationships/
│   │   └── config.yaml
│   ├── marmoset/
│   │   ├── structures/
│   │   ├── relationships/
│   │   └── config.yaml
│   └── zebrafinch/
│       ├── structures/
│       ├── relationships/
│       └── config.yaml
├── schemas/          # Shared
├── scripts/          # Shared
└── .github/          # Shared
```

**Pros:**
- Single codebase
- Easy cross-species comparison
- Unified workflows
- Shared scripts/schemas

**Cons:**
- More complex structure
- Larger repository
- Needs significant refactoring

---

## Quick Start: Model A (Separate Repos)

This is the **fastest** way to get started.

### Step 1: Fork/Clone for New Species

```bash
# Clone the mouse repo as template
git clone https://github.com/MitraLab-Organization/bap-ontology-editor.git bap-ontology-marmoset
cd bap-ontology-marmoset

# Remove git history (optional - start fresh)
rm -rf .git
git init
```

### Step 2: Update Branding (5 minutes)

**Edit `README.md`:**
```markdown
# BAP Marmoset Head Ontology

A collaborative repository for managing the Brain Architecture Project (BAP) 
marmoset (Callithrix jacchus) head anatomical ontology.
```

**Edit `docs/Home.md`:**
```markdown
# BAP Marmoset Ontology Wiki

This wiki provides comprehensive documentation for the marmoset head anatomy ontology.
```

**Edit `.github/ISSUE_TEMPLATE/config.yml`:**
```yaml
blank_issues_enabled: false
contact_links:
  - name: Marmoset Ontology Questions
    url: https://github.com/your-org/bap-ontology-marmoset/discussions
```

### Step 3: Clear Existing Data (5 minutes)

**Option A: Start from scratch**
```bash
# Clear all structure data
cat > structures/body_regions.yaml << 'EOF'
metadata:
  category: regions
  description: Marmoset body regions
  version: 1.0.0
  last_modified: '2026-01-22'

structures:
  - id: BAP_0000001
    name: Body
    parent: null
    definition: Entire body of marmoset

  - id: BAP_0000002
    name: Head
    parent: BAP_0000001
    definition: Cranial region of marmoset
EOF

# Clear other files
> structures/muscles.yaml
> structures/nerves.yaml
> structures/vessels.yaml
> structures/skeletal.yaml
> relationships/innervation.yaml
> relationships/blood_supply.yaml
> relationships/developmental.yaml
```

**Option B: Keep structure, replace data**
- Use existing hierarchy as template
- Replace mouse-specific names with marmoset equivalents
- Adjust IDs if needed

### Step 4: Update OWL Generation (2 minutes)

**Edit `scripts/generate_owl.py`:**
```python
# Find and update these lines (around line 10-20)
ONTOLOGY_IRI = "https://bap.org/ontology/marmoset/bap-marmoset.owl"
ONTOLOGY_TITLE = "BAP Marmoset Head Anatomy Ontology"
ONTOLOGY_DESCRIPTION = "Anatomical ontology for the marmoset (Callithrix jacchus) head region"

# Update species metadata
SPECIES_NAME = "Callithrix jacchus"
SPECIES_COMMON = "Common Marmoset"
NCBI_TAXON = "9483"  # NCBI Taxonomy ID for marmoset
```

### Step 5: Test Setup (2 minutes)

```bash
# Activate virtual environment
source venv/bin/activate

# Validate structure
python scripts/validate.py

# Generate tree
python scripts/generate_tree.py

# Generate OWL
python scripts/generate_owl.py --output bap-marmoset.owl
```

### Step 6: Add Initial Data

Now you can start adding marmoset-specific anatomy!

---

## Identifier Strategy

### Option 1: Keep BAP_ Prefix (Simplest)
**Use when:** You want consistency across all BAP species projects

```yaml
# Mouse uses: BAP_0000001 - BAP_0999999
# Marmoset uses: BAP_1000000 - BAP_1999999
# Zebrafinch uses: BAP_2000000 - BAP_2999999
```

**ID Range Allocation:**
```
BAP_0000000 - BAP_0999999   = Mouse
BAP_1000000 - BAP_1999999   = Marmoset
BAP_2000000 - BAP_2999999   = Zebrafinch
BAP_3000000 - BAP_3999999   = Macaque
BAP_4000000 - BAP_4999999   = Human
...
```

**No code changes needed!** Just use different ID ranges.

### Option 2: Species-Specific Prefix
**Use when:** You want clear separation between species

```yaml
# Mouse: BAP_0000001
# Marmoset: MAR_0000001
# Zebrafinch: ZFN_0000001
```

**Code changes required:**
1. Update schemas (`schemas/*.schema.json`)
2. Update scripts (`scripts/generate_owl.py`, `scripts/ai_context.py`)

**Example change in `schemas/structure.schema.json`:**
```json
"bap_id": {
  "type": "string",
  "pattern": "^MAR_[0-9]{7}$",  // Changed from BAP_
  "description": "Marmoset identifier in format MAR_XXXXXXX"
}
```

**Recommendation:** Use Option 1 (keep BAP_ with different ranges) for simplicity.

---

## Species-Specific Anatomy Considerations

### Marmoset (Callithrix jacchus)

**Key anatomical differences from mouse:**
- Larger brain with more defined gyri/sulci
- Different cranial nerve branching patterns
- Primate-specific muscles (e.g., facial expression muscles)
- Different dental formula
- Opposable thumb structures

**Structure additions needed:**
```yaml
# structures/muscles.yaml
- id: BAP_1000001
  name: Corrugator supercilii
  parent: BAP_1000000  # Facial muscles
  definition: Primate facial expression muscle; draws eyebrow downward

- id: BAP_1000002
  name: Frontalis
  parent: BAP_1000000
  definition: Raises eyebrows and wrinkles forehead
```

**Useful references:**
- Stephan et al. (1981) - Marmoset brain atlas
- Tokuno et al. (2009) - Marmoset cortical areas

### Zebrafinch (Taeniopygia guttata)

**Key anatomical differences from mouse:**
- Avian skull structure (no sutures, pneumatic bones)
- Syrinx instead of larynx
- Different brain organization (no cortex, specialized song nuclei)
- Feather muscles
- No teeth

**Structure additions needed:**
```yaml
# structures/body_regions.yaml
- id: BAP_2000001
  name: Syrinx
  parent: BAP_2000000  # Respiratory system
  definition: Vocal organ unique to birds

# structures/muscles.yaml
- id: BAP_2000010
  name: Musculus tracheolateralis
  parent: BAP_2000001
  definition: Syringeal muscle controlling sound production

# Song system nuclei
- id: BAP_2001000
  name: HVC
  parent: BAP_2001001  # Telencephalon
  definition: High vocal center; sensorimotor nucleus for song
```

**Useful references:**
- Wild et al. (2010) - Zebrafinch brain atlas
- Vates et al. (1996) - Syringeal anatomy

---

## Data Population Strategies

### Strategy 1: Manual Entry via Issue Templates
**Best for:** Community contributions, gradual building

1. Use existing issue templates
2. Team members submit structures via forms
3. AI processes approved issues
4. Build incrementally

**Pros:** Quality control, documented decisions
**Cons:** Slower initial setup

### Strategy 2: Bulk Import from Literature
**Best for:** Existing data, rapid initial population

```python
# Create import script: scripts/import_species_data.py
import yaml
import csv

def import_from_atlas(csv_file, species_prefix="MAR"):
    """Import structures from anatomical atlas CSV"""
    structures = []
    id_counter = 1000000 if species_prefix == "MAR" else 0
    
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            structures.append({
                'id': f'BAP_{id_counter:07d}',
                'name': row['Structure_Name'],
                'parent': row['Parent_ID'] if row['Parent_ID'] else None,
                'definition': row['Definition'],
                'abbreviation': row['Abbrev']
            })
            id_counter += 1
    
    return {'structures': structures}

# Usage
data = import_from_atlas('marmoset_atlas.csv', 'MAR')
with open('structures/imported.yaml', 'w') as f:
    yaml.dump(data, f, sort_keys=False)
```

### Strategy 3: Adapt from Mouse
**Best for:** Conserved structures, comparative anatomy

```python
# scripts/adapt_from_mouse.py
def adapt_structure_for_species(mouse_struct, species="marmoset"):
    """
    Adapt mouse structure for another species.
    Keep conserved structures, flag species-specific ones.
    """
    # Conserved structures (present in most mammals)
    conserved = [
        "Trigeminal nerve", "Facial nerve", "Masseter",
        "Temporalis", "Brain", "Spinal cord"
    ]
    
    if mouse_struct['name'] in conserved:
        # Keep structure, adjust ID range
        new_struct = mouse_struct.copy()
        new_struct['id'] = convert_id_range(mouse_struct['id'], species)
        return new_struct
    else:
        # Flag for review
        return None
```

---

## Cross-Species Comparison Features

### Adding Species Metadata

**Enhance structure definitions:**
```yaml
structures:
  - id: BAP_1000100
    name: Masseter
    parent: BAP_1000000
    definition: Primary muscle of mastication
    species_notes:
      mouse: "Relatively large, three distinct parts"
      marmoset: "Smaller relative to skull, two main divisions"
      human: "Deep and superficial parts, varies by diet"
    conservation: "Highly conserved across mammals"
    ncbi_homology: "HGNC:6900"  # Human gene homology
```

### Comparative Visualization

**Edit `scripts/generate_wiki.py` to add comparison tables:**
```python
def generate_species_comparison():
    """Generate cross-species comparison table"""
    return """
## Cross-Species Comparison

| Structure | Mouse | Marmoset | Human |
|-----------|-------|----------|-------|
| Masseter | Present | Present | Present |
| Whisker muscles | 12 muscles | Absent | Absent |
| Facial expression | Limited | 8+ muscles | 20+ muscles |
"""
```

---

## Maintaining Multiple Species Repos

### Syncing Script Updates

When you update scripts in one repo, sync to others:

```bash
# Create sync script: scripts/sync_common_code.sh
#!/bin/bash

# List of repos to sync
REPOS=(
    "bap-ontology-mouse"
    "bap-ontology-marmoset"
    "bap-ontology-zebrafinch"
)

# Files to sync (common code)
SYNC_FILES=(
    "scripts/validate.py"
    "scripts/generate_tree.py"
    "scripts/generate_wiki.py"
    "schemas/structure.schema.json"
    "schemas/relationship.schema.json"
)

for repo in "${REPOS[@]}"; do
    for file in "${SYNC_FILES[@]}"; do
        if [ -f "$file" ]; then
            cp "$file" "../$repo/$file"
        fi
    done
done
```

### Git Submodules for Shared Code

**Advanced:** Use git submodules for common code:

```bash
# In each species repo
git submodule add https://github.com/your-org/bap-common-scripts.git common

# Link to common scripts
ln -s common/scripts/* scripts/
ln -s common/schemas/* schemas/
```

---

## Working Example: Marmoset Setup

Here's a complete walkthrough for setting up marmoset:

### 1. Initial Setup
```bash
# Clone and setup
git clone https://github.com/MitraLab-Organization/bap-ontology-editor.git bap-ontology-marmoset
cd bap-ontology-marmoset
rm -rf .git
git init
```

### 2. Update Core Files

**`README.md`:**
```markdown
# BAP Marmoset (Callithrix jacchus) Head Ontology

📊 **Ontology Statistics**
```
├── Structures: 0 (in progress)
├── Hierarchy depth: TBD
└── Relationships: 0 (in progress)
```

## Species Information
- **Common name:** Common Marmoset
- **Scientific name:** Callithrix jacchus
- **NCBI Taxonomy:** 9483
- **Order:** Primates
- **Family:** Callitrichidae
```

**`scripts/generate_owl.py`:**
```python
# Update lines 15-25
ONTOLOGY_IRI = "https://bap.org/ontology/marmoset/bap-marmoset.owl"
ONTOLOGY_PREFIX = "BAP"
ONTOLOGY_TITLE = "BAP Marmoset Head Anatomy"
SPECIES = "Callithrix jacchus"
NCBI_TAXON = "9483"

# Update in generate_ontology function
ont.metadata.ncbi_taxon = "NCBITaxon:9483"
ont.metadata.species = "Callithrix jacchus"
```

### 3. Create Initial Structure

**`structures/body_regions.yaml`:**
```yaml
metadata:
  category: regions
  description: Marmoset body regions
  version: 1.0.0
  last_modified: '2026-01-22'
  species: "Callithrix jacchus"
  ncbi_taxon: "9483"

structures:
  - id: BAP_1000001
    name: Body
    parent: null
    definition: Entire body of the common marmoset
    
  - id: BAP_1000002
    name: Head
    parent: BAP_1000001
    definition: Cranial region, including brain, skull, and associated structures
    
  - id: BAP_1000003
    name: Nervous system
    parent: BAP_1000002
    definition: Neural structures of the marmoset head
    
  - id: BAP_1000004
    name: Brain
    parent: BAP_1000003
    definition: Central nervous system structure; more gyrencephalic than mouse
```

**`structures/muscles.yaml`:**
```yaml
metadata:
  category: muscles
  description: Marmoset cranial muscles
  version: 1.0.0
  species: "Callithrix jacchus"

structures:
  - id: BAP_1001000
    name: Cranial muscles
    parent: BAP_1000002
    definition: Muscles of the marmoset head
    
  - id: BAP_1001001
    name: Masticatory muscles
    parent: BAP_1001000
    definition: Muscles involved in chewing
    
  - id: BAP_1001010
    name: Masseter
    parent: BAP_1001001
    definition: Primary jaw elevator; smaller than in mouse relative to skull size
    external_id: "UBERON:0001597"
    
  - id: BAP_1001011
    name: Temporalis
    parent: BAP_1001001
    definition: Jaw elevator and retractor
    external_id: "UBERON:0001578"
    
  - id: BAP_1002000
    name: Facial expression muscles
    parent: BAP_1001000
    definition: Muscles controlling facial expression; more developed than in mouse
    
  - id: BAP_1002001
    name: Frontalis
    parent: BAP_1002000
    definition: Raises eyebrows and wrinkles forehead; absent in mouse
    external_id: "UBERON:0008229"
```

### 4. Add Species-Specific Relationships

**`relationships/innervation.yaml`:**
```yaml
metadata:
  type: innervation
  description: Cranial nerve innervation patterns in marmoset
  version: 1.0.0
  species: "Callithrix jacchus"

relationships:
  - subject: BAP_1001010  # Masseter
    predicate: innervated_by
    object: BAP_1010001   # Trigeminal nerve (V3)
    confidence: high
    reference: "Ikai et al. 2020"
    notes: "Innervation pattern similar to other primates"
    
  - subject: BAP_1002001  # Frontalis
    predicate: innervated_by
    object: BAP_1010002   # Facial nerve
    confidence: high
    reference: "Sherwood et al. 2005"
    notes: "Temporal branch of facial nerve"
```

### 5. Test Everything

```bash
# Validate
python scripts/validate.py

# Should output:
# ✓ All structure files valid
# ✓ All relationship files valid
# ✓ No circular references
# ✓ No orphaned structures

# Generate tree
python scripts/generate_tree.py

# Generate OWL
python scripts/generate_owl.py --output bap-marmoset.owl

# Generate wiki
python scripts/generate_wiki.py
```

### 6. Commit and Deploy

```bash
git add .
git commit -m "Initial marmoset ontology structure"
git remote add origin https://github.com/your-org/bap-ontology-marmoset.git
git push -u origin main
```

---

## AI System for New Species

The AI system works automatically with new species! No changes needed.

**Example request for marmoset:**
```
Issue: Add the orbicularis oculi muscle for marmoset

The AI will:
1. Understand it's a facial muscle
2. Find appropriate parent (Facial expression muscles)
3. Assign correct ID in marmoset range (BAP_1002xxx)
4. Add relationship to facial nerve
5. Generate proper YAML
```

**The AI knows anatomy across species!** It understands:
- Conserved structures (present in most vertebrates)
- Mammal-specific structures
- Primate-specific structures
- Bird-specific structures

---

## Reference: Species ID Ranges

Recommended ID allocation:

```
BAP_0000000 - BAP_0999999   = Mouse (Mus musculus)
BAP_1000000 - BAP_1999999   = Marmoset (Callithrix jacchus)
BAP_2000000 - BAP_2999999   = Zebrafinch (Taeniopygia guttata)
BAP_3000000 - BAP_3999999   = Macaque (Macaca mulatta)
BAP_4000000 - BAP_4999999   = Rat (Rattus norvegicus)
BAP_5000000 - BAP_5999999   = Human (Homo sapiens)
BAP_6000000 - BAP_6999999   = Reserved
BAP_7000000 - BAP_7999999   = Reserved
BAP_8000000 - BAP_8999999   = Reserved
BAP_9000000 - BAP_9999999   = Test/Development
```

Within each species range:
```
X000000 - X099999  = Body regions / Categories
X100000 - X499999  = Muscles
X500000 - X699999  = Nerves
X700000 - X899999  = Vessels
X900000 - X999999  = Skeletal
```

---

## Quick Reference Commands

```bash
# Setup new species repo
git clone <mouse-repo> bap-ontology-<species>
cd bap-ontology-<species>

# Clear data
> structures/*.yaml
> relationships/*.yaml

# Create base structure
python scripts/create_base_structure.py --species="Species name" --id-range=1000000

# Validate
python scripts/validate.py

# Generate outputs
python scripts/generate_tree.py
python scripts/generate_owl.py --output bap-<species>.owl
python scripts/generate_wiki.py

# Test locally
python -m http.server 8000
# Open: http://localhost:8000/docs/
```

---

## Need Help?

1. **Anatomy questions:** Consult species-specific atlases
2. **Technical issues:** Check mouse repo as reference
3. **ID conflicts:** Use recommended ID ranges
4. **Missing structures:** Use issue templates to add

---

**Ready to create your species ontology?** Start with the [Quick Start](#quick-start-model-a-separate-repos) section!
