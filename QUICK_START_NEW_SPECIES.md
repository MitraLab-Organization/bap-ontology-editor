# Quick Start: New Species Ontology

**TL;DR:** Setting up a new species (marmoset, zebrafinch, etc.) is much simpler than a completely different domain because the anatomy concepts stay the same!

## 5-Minute Setup

### 1. Clone the Template
```bash
git clone https://github.com/MitraLab-Organization/bap-ontology-editor.git bap-ontology-marmoset
cd bap-ontology-marmoset
```

### 2. Run Bootstrap Script
```bash
# Activate your virtual environment
source venv/bin/activate

# Bootstrap for Marmoset
python scripts/bootstrap_species.py \
  --species "Marmoset" \
  --scientific "Callithrix jacchus" \
  --common "Common Marmoset" \
  --ncbi 9483 \
  --id-start 1000000

# Or for Zebrafinch
python scripts/bootstrap_species.py \
  --species "Zebrafinch" \
  --scientific "Taeniopygia guttata" \
  --common "Zebra Finch" \
  --ncbi 59729 \
  --id-start 2000000
```

This automatically:
- ✓ Creates empty structure files with species metadata
- ✓ Updates README with species information
- ✓ Configures OWL generation
- ✓ Sets up proper ID ranges

### 3. Validate
```bash
python scripts/validate.py
```

### 4. Start Adding Data
You can now add structures using:
- **Issue templates** (easiest - no coding)
- **Direct YAML editing**
- **AI-assisted requests**

That's it! 🎉

---

## What Stays the Same ✓

When adapting for a new species, **most things don't change**:

| Component | Changes Needed? |
|-----------|----------------|
| **Schemas** | ✗ No changes |
| **Scripts** | ✗ Work as-is (except 1 config line) |
| **GitHub Actions** | ✗ Work as-is |
| **Issue Templates** | ✗ Work as-is |
| **AI System** | ✗ Understands all species |
| **Categories** | ✗ Still muscles, nerves, vessels, bones |
| **Relationships** | ✗ Still innervated_by, supplied_by, etc. |

**Only thing that changes:** The actual anatomical data (different structures, hierarchies)

---

## ID Strategy

Use **BAP_ prefix with different ranges** for each species:

```
BAP_0000000 - BAP_0999999   = Mouse
BAP_1000000 - BAP_1999999   = Marmoset  
BAP_2000000 - BAP_2999999   = Zebrafinch
BAP_3000000 - BAP_3999999   = Macaque
BAP_4000000 - BAP_4999999   = Rat
BAP_5000000 - BAP_5999999   = Human
```

**Benefits:**
- No code changes needed
- All species share same ID format
- Easy cross-species comparison
- Can reference structures across species

---

## Example: Adding Marmoset Data

After bootstrapping, just add structures:

**`structures/muscles.yaml`:**
```yaml
metadata:
  category: muscles
  description: Marmoset cranial muscles
  species: "Callithrix jacchus"
  version: 1.0.0

structures:
  - id: BAP_1001000
    name: Cranial muscles
    parent: BAP_1000002  # Head
    definition: Muscles of the marmoset head
    
  - id: BAP_1001100
    name: Masticatory muscles
    parent: BAP_1001000
    
  - id: BAP_1001110
    name: Masseter
    parent: BAP_1001100
    definition: Primary jaw elevator
    external_id: "UBERON:0001597"
    
  # Marmoset-specific: facial expression muscles
  - id: BAP_1002000
    name: Facial expression muscles
    parent: BAP_1001000
    definition: Muscles controlling facial expression
    
  - id: BAP_1002010
    name: Frontalis
    parent: BAP_1002000
    definition: Raises eyebrows; absent in rodents
```

**`relationships/innervation.yaml`:**
```yaml
metadata:
  type: innervation
  species: "Callithrix jacchus"

relationships:
  - subject: BAP_1001110  # Masseter
    predicate: innervated_by
    object: BAP_1010001   # Trigeminal nerve
    confidence: high
    reference: "Ikai et al. 2020"
```

---

## Species-Specific Considerations

### Marmoset vs Mouse

**Conserved structures** (present in both):
- Basic cranial nerves (trigeminal, facial, etc.)
- Core muscles (masseter, temporalis)
- Major vessels
- Basic brain regions

**Marmoset-specific additions**:
- More developed facial expression muscles
- More gyrencephalic brain (more gyri/sulci)
- Different proportions
- Primate-specific features

### Zebrafinch vs Mouse

**Completely different**:
- Avian skull (fused, pneumatic)
- No teeth
- Syrinx instead of larynx
- Song system nuclei (HVC, RA, etc.)
- Feather muscles

**Similar**:
- Basic cranial nerve organization
- Core neuromuscular principles
- Vascular patterns

---

## Testing Your Setup

```bash
# 1. Validate structure
python scripts/validate.py

# Expected output:
# ✓ All structure files valid
# ✓ All relationship files valid
# ✓ No circular references

# 2. Generate hierarchy tree
python scripts/generate_tree.py

# 3. Generate OWL
python scripts/generate_owl.py --output bap-marmoset.owl

# 4. Generate wiki (optional)
python scripts/generate_wiki.py
```

---

## Using the AI System

The AI **automatically understands** you're working with a different species!

**Example request:**
```
Issue: Add the orbicularis oculi muscle for marmoset.
It's innervated by the facial nerve.
```

**AI will:**
1. Recognize it's a facial muscle
2. Find the right parent in YOUR species hierarchy
3. Use YOUR species ID range (BAP_1xxxxxx)
4. Add innervation relationship
5. Generate proper YAML

**No configuration needed!**

---

## Cross-Species Comparison (Advanced)

If you want to compare across species, you can add metadata:

```yaml
structures:
  - id: BAP_1001110
    name: Masseter
    parent: BAP_1001100
    definition: Primary jaw elevator
    species_notes:
      mouse: "Large relative to skull, 3 divisions"
      marmoset: "Smaller, 2 divisions, adapted for fruit/insects"
      human: "Deep and superficial, varies by diet"
    conservation_level: "Highly conserved across mammals"
    homology: "HGNC:6900"  # Human gene
```

---

## Common Species to Add

| Species | Scientific Name | NCBI | ID Range | Notes |
|---------|----------------|------|----------|-------|
| **Marmoset** | Callithrix jacchus | 9483 | 1000000 | Primate model |
| **Zebrafinch** | Taeniopygia guttata | 59729 | 2000000 | Song learning |
| **Macaque** | Macaca mulatta | 9544 | 3000000 | Primate model |
| **Rat** | Rattus norvegicus | 10116 | 4000000 | Rodent model |
| **Human** | Homo sapiens | 9606 | 5000000 | Clinical reference |
| **Pig** | Sus scrofa | 9823 | 6000000 | Surgical model |
| **Drosophila** | Drosophila melanogaster | 7227 | 7000000 | Insect model |

---

## Frequently Asked Questions

### Q: Do I need to change the code?
**A:** No! Just run the bootstrap script and add your data.

### Q: Can I use a different ID prefix (not BAP_)?
**A:** Yes, but it requires editing schemas. Recommended: keep BAP_ with different ranges.

### Q: Will the AI work with my species?
**A:** Yes! It understands anatomy across species automatically.

### Q: Can I import existing data?
**A:** Yes! See `SPECIES_ADAPTATION_GUIDE.md` for import strategies.

### Q: How do I handle species-specific structures?
**A:** Just add them! The system is flexible - add what's unique to your species.

### Q: What about birds vs mammals?
**A:** Works for both! Add bird-specific categories (syrinx, song nuclei, etc.) as needed.

---

## Next Steps

1. **Read full guide:** See `SPECIES_ADAPTATION_GUIDE.md` for details
2. **Check templates:** Look at mouse data as reference
3. **Start adding:** Use issue templates or direct editing
4. **Deploy:** Push to GitHub and enable Pages

---

## Quick Reference

```bash
# Bootstrap
python scripts/bootstrap_species.py --species "X" --scientific "Y" --ncbi Z --id-start N

# Validate
python scripts/validate.py

# Generate outputs
python scripts/generate_tree.py
python scripts/generate_owl.py --output bap-species.owl
python scripts/generate_wiki.py

# Test locally
python -m http.server 8000  # View docs/ folder
```

---

**Questions?** Check the full guides:
- `SPECIES_ADAPTATION_GUIDE.md` - Complete species adaptation guide
- `ONTOLOGY_TEMPLATE_GUIDE.md` - General templating (if changing domains)
- `AI_Enhanced.md` - AI workflow documentation
