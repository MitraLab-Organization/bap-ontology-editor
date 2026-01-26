# Ontology Template Guide

This guide explains how to adapt the BAP Ontology Editor system for a completely different ontology domain (e.g., plants, chemistry, software architecture, etc.).

## Table of Contents
1. [Overview](#overview)
2. [Key Components to Customize](#key-components-to-customize)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Configuration Checklist](#configuration-checklist)
5. [Example: Plant Taxonomy Ontology](#example-plant-taxonomy-ontology)

---

## Overview

The BAP Ontology Editor is a **domain-agnostic** system with these core features:
- **YAML-based structure definitions** (hierarchies + properties)
- **Relationship management** (cross-references between entities)
- **JSON Schema validation**
- **Automated GitHub workflows** (validation, wiki generation, OWL export)
- **AI-assisted editing** (natural language → structured changes)
- **Issue templates** (no-code contributions)

**What makes it adaptable:**
- Schemas define structure, not domain
- Scripts work with generic YAML structure
- Naming conventions are configurable
- Relationship types are extensible

---

## Key Components to Customize

### 1. **Identifier Prefix** (`BAP_` → `YOUR_`)

**Files to modify:**
- `schemas/structure.schema.json` - Change ID pattern
- `schemas/relationship.schema.json` - Change ID pattern
- All YAML files in `structures/` and `relationships/`
- `scripts/generate_owl.py` - Update namespace URIs
- `scripts/ai_context.py` - Update ID regex

**Example change:**
```json
// Before (BAP)
"pattern": "^BAP_[0-9]{7}$"

// After (for Plant Ontology)
"pattern": "^PLT_[0-9]{7}$"
```

### 2. **Domain-Specific Categories**

**Files to modify:**
- `schemas/structure.schema.json` - Update category enum
- Structure YAML files in `structures/` directory

**Current categories (BAP):**
```yaml
enum: ["muscles", "nerves", "vessels", "bones", "organs", "regions"]
```

**Example for Plant Ontology:**
```yaml
enum: ["taxa", "traits", "habitats", "morphology", "genetics", "ecology"]
```

### 3. **Relationship Types**

**Files to modify:**
- `schemas/relationship.schema.json` - Update predicate enum
- `scripts/generate_owl.py` - Map predicates to OBO relation IRIs

**Current relationships (BAP):**
```yaml
enum: ["part_of", "innervated_by", "supplied_by", "develops_from", ...]
```

**Example for Plant Ontology:**
```yaml
enum: ["has_part", "grows_in", "pollinated_by", "native_to", "flowers_during", ...]
```

### 4. **Structure YAML Files**

**Files to modify:**
- Rename/recreate files in `structures/` directory
- Update metadata to reflect new domain

**Current structure (BAP):**
```
structures/
├── muscles.yaml
├── nerves.yaml
├── vessels.yaml
├── skeletal.yaml
└── body_regions.yaml
```

**Example for Plant Ontology:**
```
structures/
├── families.yaml
├── species.yaml
├── traits.yaml
├── habitats.yaml
└── morphology.yaml
```

### 5. **Documentation & Branding**

**Files to modify:**
- `README.md` - Replace project description, examples
- `docs/*.md` - Update all documentation
- `.github/ISSUE_TEMPLATE/*.yml` - Customize forms
- `scripts/generate_wiki.py` - Update titles, headers

### 6. **OWL Export Configuration**

**Files to modify:**
- `scripts/generate_owl.py`

**Key changes:**
- Ontology IRI (e.g., `https://yourdomain.org/ontology.owl`)
- Namespace prefix
- Import statements (external ontologies)
- Property mappings

---

## Step-by-Step Setup

### Phase 1: Repository Setup

1. **Clone/Fork the BAP repository:**
   ```bash
   git clone https://github.com/MitraLab-Organization/bap-ontology-editor.git my-ontology-editor
   cd my-ontology-editor
   ```

2. **Update repository metadata:**
   - Edit `README.md` - change title, description, links
   - Edit `.github/ISSUE_TEMPLATE/config.yml` - update project name
   - Update `requirements.txt` if needed

### Phase 2: Schema Customization

3. **Update identifier prefix in schemas:**

**Edit `schemas/structure.schema.json`:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://yourdomain.org/schemas/structure.schema.json",
  "title": "Your Ontology Structure",
  "definitions": {
    "your_id": {
      "type": "string",
      "pattern": "^YOUR_[0-9]{7}$",
      "description": "YOUR identifier in format YOUR_XXXXXXX"
    }
  }
}
```

4. **Update categories in structure schema:**
```json
"category": {
  "type": "string",
  "enum": ["category1", "category2", "category3"]
}
```

5. **Update relationship types:**

**Edit `schemas/relationship.schema.json`:**
```json
"predicate": {
  "type": "string",
  "enum": [
    "your_relation_1",
    "your_relation_2",
    "your_relation_3"
  ]
}
```

### Phase 3: Data Structure Setup

6. **Create initial structure files:**

**Example: `structures/plants.yaml`:**
```yaml
metadata:
  category: plants
  description: Plant taxonomy structures
  version: 1.0.0
  last_modified: '2026-01-22'

structures:
  - id: YOUR_0000001
    name: Plantae
    parent: null
    definition: Kingdom of plants
  
  - id: YOUR_0000002
    name: Angiosperms
    parent: YOUR_0000001
    definition: Flowering plants
```

7. **Create initial relationship files:**

**Example: `relationships/pollination.yaml`:**
```yaml
metadata:
  type: pollination
  description: Pollination relationships
  version: 1.0.0

relationships:
  - subject: YOUR_0000100  # Species A
    predicate: pollinated_by
    object: YOUR_0000200   # Insect B
    reference: "DOI:10.1234/example"
    confidence: high
```

### Phase 4: Script Adaptation

8. **Update validation script:**

**Edit `scripts/validate.py`:**
- Update ID regex patterns
- Update file paths if needed
- Update error messages

9. **Update OWL generation:**

**Edit `scripts/generate_owl.py`:**
```python
# Update namespace
ONTOLOGY_IRI = "https://yourdomain.org/your-ontology.owl"
ONTOLOGY_PREFIX = "YOUR"

# Update property mappings
PREDICATE_TO_OBO = {
    "part_of": "BFO_0000050",
    "your_custom_relation": "RO_XXXXXXX",  # Use appropriate OBO relation
}
```

10. **Update AI context:**

**Edit `scripts/ai_context.py`:**
```python
# Update ID pattern
ID_PATTERN = re.compile(r'^YOUR_\d{7}$')

# Update type detection logic (if needed)
def detect_structure_type(name: str) -> str:
    """Detect structure type from name"""
    if 'plant' in name.lower():
        return 'plant'
    # Add your domain logic
```

### Phase 5: GitHub Workflows

11. **Update issue templates:**

**Edit `.github/ISSUE_TEMPLATE/add-structure.yml`:**
- Change title to reflect your domain
- Update dropdown options for categories
- Update example text

**Example:**
```yaml
name: "➕ Add New Plant Species"
description: Submit a new plant species to the ontology
title: "[Add Species]: "
labels: ["enhancement", "needs-review"]

body:
  - type: dropdown
    id: category
    attributes:
      label: Category
      options:
        - Angiosperms
        - Gymnosperms
        - Ferns
        - Mosses
```

12. **Update workflow files:**

**Edit `.github/workflows/*.yml`:**
- Update output file names (e.g., `your-ontology.owl`)
- Update validation messages
- Update deploy paths

### Phase 6: Documentation

13. **Update wiki generation:**

**Edit `scripts/generate_wiki.py`:**
```python
# Update titles
WIKI_TITLE = "Your Ontology Wiki"
PROJECT_NAME = "Your Ontology"

# Update relationship display names
RELATIONSHIP_DISPLAY = {
    "pollinated_by": "Pollination",
    "native_to": "Native Range",
}
```

14. **Regenerate documentation:**
```bash
python scripts/generate_wiki.py
python scripts/generate_tree.py
```

### Phase 7: Testing

15. **Test validation:**
```bash
python scripts/validate.py
```

16. **Test OWL generation:**
```bash
python scripts/generate_owl.py --output your-ontology.owl
```

17. **Test AI workflow (optional):**
```bash
# Create test request
cat > .ai_requests/issue_test.json << 'EOF'
{
  "actions": [
    {
      "type": "create_structure",
      "name": "Test Species",
      "id": "YOUR_9999999",
      "parent_name": "Plantae",
      "definition": "Test plant species"
    }
  ]
}
EOF

ISSUE_NUMBER=test python scripts/ai_create_changes_v2.py
```

### Phase 8: Deployment

18. **Enable GitHub Pages:**
- Go to repository Settings → Pages
- Select source: GitHub Actions
- The wiki will auto-deploy on push

19. **Set up branch protection:**
- Require PR reviews
- Require status checks (validation)
- Set up CODEOWNERS

20. **Initial commit:**
```bash
git add .
git commit -m "Initialize Your Ontology Editor"
git push origin main
```

---

## Configuration Checklist

Use this checklist to ensure you've customized all necessary components:

### Core Identity
- [ ] Repository name updated
- [ ] Identifier prefix changed (e.g., `BAP_` → `YOUR_`)
- [ ] Ontology IRI defined
- [ ] Namespace prefix set

### Schemas
- [ ] `structure.schema.json` - ID pattern updated
- [ ] `structure.schema.json` - Categories updated
- [ ] `relationship.schema.json` - ID pattern updated
- [ ] `relationship.schema.json` - Predicates updated

### Data Files
- [ ] Structure YAML files created/renamed
- [ ] Relationship YAML files created/renamed
- [ ] Initial data populated
- [ ] Metadata fields filled

### Scripts
- [ ] `validate.py` - ID regex updated
- [ ] `generate_owl.py` - Namespace updated
- [ ] `generate_owl.py` - Predicate mappings updated
- [ ] `generate_tree.py` - (minimal changes needed)
- [ ] `generate_wiki.py` - Title/branding updated
- [ ] `ai_context.py` - ID pattern updated (if using AI)
- [ ] `ai_enhanced_prompt.py` - Domain knowledge updated (if using AI)

### GitHub
- [ ] Issue templates customized (`.github/ISSUE_TEMPLATE/*.yml`)
- [ ] Workflow files updated (`.github/workflows/*.yml`)
- [ ] CODEOWNERS file updated
- [ ] Branch protection configured

### Documentation
- [ ] `README.md` rewritten
- [ ] `docs/*.md` files updated
- [ ] Examples replaced with domain-appropriate ones
- [ ] Wiki pages regenerated

### Testing
- [ ] Validation passes
- [ ] OWL generation works
- [ ] Wiki generates correctly
- [ ] GitHub Actions run successfully
- [ ] Issue templates work

---

## Example: Plant Taxonomy Ontology

Here's a complete example for a plant taxonomy ontology:

### 1. Structure Schema Excerpt
```json
{
  "definitions": {
    "plant_id": {
      "type": "string",
      "pattern": "^PLT_[0-9]{7}$"
    }
  },
  "properties": {
    "metadata": {
      "properties": {
        "category": {
          "enum": ["taxonomy", "morphology", "ecology", "genetics"]
        }
      }
    }
  }
}
```

### 2. Sample Structure File
```yaml
# structures/taxonomy.yaml
metadata:
  category: taxonomy
  description: Plant taxonomic hierarchy
  version: 1.0.0

structures:
  - id: PLT_0000001
    name: Plantae
    parent: null
    definition: Kingdom comprising all plants
    
  - id: PLT_0000010
    name: Angiosperms
    parent: PLT_0000001
    definition: Division of flowering plants
    
  - id: PLT_0001000
    name: Rosaceae
    parent: PLT_0000010
    definition: Rose family of flowering plants
    synonyms:
      - "Rose family"
    external_id: "NCBI_3745"
```

### 3. Sample Relationship File
```yaml
# relationships/ecology.yaml
metadata:
  type: ecology
  description: Ecological relationships
  version: 1.0.0

relationships:
  - subject: PLT_0002001  # Rosa canina
    predicate: native_to
    object: PLT_0100001   # Europe region
    confidence: high
    reference: "DOI:10.1234/flora2023"
    
  - subject: PLT_0002001  # Rosa canina
    predicate: pollinated_by
    object: PLT_0200001   # Apis mellifera (honeybee)
    confidence: medium
```

### 4. Updated OWL Generator
```python
# scripts/generate_owl.py (excerpt)

ONTOLOGY_IRI = "https://plantontology.org/plt.owl"
ONTOLOGY_PREFIX = "PLT"

PREDICATE_TO_OBO = {
    "part_of": "BFO_0000050",
    "native_to": "RO_0002303",  # ecologically related to
    "pollinated_by": "RO_0002455",  # pollinates (inverse)
    "flowers_during": "RO_0002090",  # during which starts
}
```

### 5. Issue Template Example
```yaml
# .github/ISSUE_TEMPLATE/add-plant-species.yml
name: "🌱 Add Plant Species"
description: Add a new plant species to the taxonomy
title: "[Species]: "
labels: ["enhancement", "taxonomy"]

body:
  - type: input
    id: scientific_name
    attributes:
      label: Scientific Name
      description: Binomial nomenclature (e.g., Rosa canina)
      placeholder: "Genus species"
    validations:
      required: true
      
  - type: dropdown
    id: family
    attributes:
      label: Family
      options:
        - Rosaceae
        - Fabaceae
        - Asteraceae
        - Poaceae
        - Other
```

---

## Advanced Customization

### Adding Custom Validation Rules

**Edit `scripts/validate.py`:**
```python
def validate_custom_rules(structures: List[dict]) -> List[str]:
    """Add domain-specific validation"""
    errors = []
    
    for struct in structures:
        # Example: Validate that species have valid parent families
        if struct['name'].startswith('Species:'):
            parent = find_parent(struct['parent'])
            if parent and 'Family' not in parent['name']:
                errors.append(f"Species {struct['name']} must have Family as parent")
    
    return errors
```

### Custom AI Context

**Edit `scripts/ai_enhanced_prompt.py`:**
```python
DOMAIN_KNOWLEDGE = """
Plant Taxonomy Rules:
1. Hierarchy: Kingdom → Division → Class → Order → Family → Genus → Species
2. Species names must be in Latin binomial format
3. Cultivars use single quotes (e.g., Rosa 'Peace')
4. Ecological relationships require geographic context
"""
```

### Custom Visualizations

**Edit `scripts/generate_wiki.py`:**
```python
def generate_distribution_map(relationships):
    """Generate geographic distribution visualization"""
    # Add custom Mermaid diagram or embed maps
    pass
```

---

## Migration Strategies

### From Existing Data

If you have existing ontology data:

1. **From OWL/RDF:**
   ```bash
   # Use tools like ROBOT to convert
   robot convert --input existing.owl --output structures.yaml
   # Then manually adjust to schema
   ```

2. **From CSV/Spreadsheet:**
   ```python
   # Create conversion script
   import csv
   import yaml
   
   def csv_to_yaml(csv_file):
       structures = []
       with open(csv_file) as f:
           reader = csv.DictReader(f)
           for row in reader:
               structures.append({
                   'id': row['ID'],
                   'name': row['Name'],
                   'parent': row['Parent'] or None,
                   'definition': row['Definition']
               })
       return {'structures': structures}
   ```

3. **From Database:**
   - Export to CSV first, then use above method
   - Or create direct DB→YAML converter script

---

## Maintenance Tips

1. **Version Control:**
   - Tag releases (v1.0.0, v2.0.0)
   - Maintain CHANGELOG.md
   - Use semantic versioning

2. **ID Assignment:**
   - Reserve ID ranges for different categories
   - Example: PLT_0000000-0999999 = Taxonomy
   - PLT_1000000-1999999 = Traits

3. **Collaboration:**
   - Use CODEOWNERS for different domains
   - Set up required reviewers
   - Use project boards for tracking

4. **Documentation:**
   - Keep wiki updated automatically
   - Document ID ranges
   - Maintain relationship reference

---

## Troubleshooting

### Common Issues

**Problem:** Validation fails after identifier change
- **Solution:** Update all ID patterns in schemas AND scripts

**Problem:** OWL generation produces invalid IRIs
- **Solution:** Check namespace configuration in `generate_owl.py`

**Problem:** AI makes wrong assumptions
- **Solution:** Update domain knowledge in `ai_enhanced_prompt.py`

**Problem:** Wiki doesn't render correctly
- **Solution:** Check GitHub Pages settings, verify Mermaid syntax

---

## Resources

- JSON Schema: https://json-schema.org/
- OBO Relations: http://www.obofoundry.org/ontology/ro.html
- OWL/RDF: https://www.w3.org/OWL/
- GitHub Actions: https://docs.github.com/actions
- Mermaid Diagrams: https://mermaid.js.org/

---

## Need Help?

1. Check existing BAP structure as reference
2. Test changes incrementally
3. Use validation scripts frequently
4. Keep backups before major changes

---

**Ready to start?** Follow the [Step-by-Step Setup](#step-by-step-setup) section!
