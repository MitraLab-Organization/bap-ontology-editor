# BAP Ontology Wiki

Welcome to the **auto-generated** documentation wiki for the Brain Architecture Project (BAP) Mouse Head Ontology.

## 🤖 Auto-Generated Documentation

This entire wiki is **automatically generated** from the ontology YAML files on every push to the repository. The documentation always stays in sync with the actual data.

### Generation Process

```
Git Push → GitHub Actions → Wiki Generator → Updated Docs
```

- **Trigger:** Every push to `main` that affects `structures/` or `relationships/`
- **Generator:** `scripts/generate_wiki.py`
- **Frequency:** Real-time (within minutes of push)
- **Source:** All data comes directly from validated YAML files

## 📚 Wiki Pages

### Core Documentation

- **[Home](Home.md)** - Overview and statistics
- **[Structure Catalog](Structure-Catalog.md)** - Complete list of all anatomical structures
- **[Hierarchy Explorer](Hierarchy.md)** - Visual hierarchy tree
- **[Relationships](Relationships.md)** - All cross-structure relationships

### Specialized Views

- **[Innervation Map](Innervation.md)** - Neural connectivity details
- **[Blood Supply Map](Blood-Supply.md)** - Vascular supply network
- **[Quality Report](Quality-Report.md)** - Data quality and validation
- **[Statistics Dashboard](Statistics.md)** - Analytics and metrics
- **[Change History](Change-History.md)** - Recent updates and commits

## 🔍 Search Tips

Each wiki page is a Markdown file that can be searched using:
- GitHub's built-in search (press `/` on any page)
- Your browser's find function (Ctrl+F / Cmd+F)
- grep in the repository: `grep -r "search term" docs/`

## 📊 What's Included

### Structure Information
- Complete catalog with IDs, names, and definitions
- Hierarchical parent-child relationships
- Source file locations
- Cross-references

### Relationship Data
- Innervation patterns (nerve → muscle)
- Blood supply (artery → structure)
- Developmental origins
- Spatial relationships
- Confidence levels and references

### Analytics
- Structure counts by system
- Relationship statistics
- Hierarchy depth analysis
- Data quality metrics
- Change frequency

## 🛠️ For Developers

### Regenerate Wiki Manually

```bash
# Install dependencies
pip install -r requirements.txt

# Generate all wiki pages
python scripts/generate_wiki.py --output docs/

# Generate specific pages only
python scripts/generate_wiki.py --pages Home,Statistics

# Generate changelog
python scripts/generate_changelog.py --output docs/Change-History.md --days 30
```

### Add New Wiki Pages

1. Add a generator function to `scripts/generate_wiki.py`
2. Register it in the `pages` dictionary in `main()`
3. Push changes - the page will auto-generate on next commit

### Customize Output

Edit `scripts/generate_wiki.py` to:
- Add new metrics
- Change formatting
- Include additional visualizations
- Filter or group data differently

## 📖 About the Data

All information in this wiki comes from:

- **Structure files:** `structures/*.yaml`
  - `muscles.yaml` - Muscle structures
  - `nerves.yaml` - Neural structures
  - `vessels.yaml` - Vascular structures
  - `skeletal.yaml` - Skeletal structures
  - `body_regions.yaml` - Regional organization

- **Relationship files:** `relationships/*.yaml`
  - `innervation.yaml` - Neural innervation
  - `blood_supply.yaml` - Vascular supply
  - `developmental.yaml` - Developmental relationships

- **Schema files:** `schemas/*.json`
  - JSON Schema validation rules

## 🔗 Quick Links

- [Main Repository](https://github.com/MitraLab-Organization/bap-ontology-editor)
- [Add New Structure](https://github.com/MitraLab-Organization/bap-ontology-editor/issues/new?template=add-structure.yml)
- [Add Relationship](https://github.com/MitraLab-Organization/bap-ontology-editor/issues/new?template=add-relationship.yml)
- [AI Request (Natural Language)](https://github.com/MitraLab-Organization/bap-ontology-editor/issues/new?template=ai-request.yml)
- [Report Issue](https://github.com/MitraLab-Organization/bap-ontology-editor/issues/new)

## ⚡ Live Updates

This documentation is updated automatically:
- **Latency:** 2-3 minutes after push
- **Status:** Check the [Actions tab](https://github.com/MitraLab-Organization/bap-ontology-editor/actions/workflows/generate-wiki.yml)
- **History:** All updates tracked in git history

## 📧 Questions?

If you have questions about:
- **The data:** Open an issue in the repository
- **The wiki system:** Contact the maintainers
- **Contributing:** See the main [README](../README.md)

---

*This wiki is part of the BAP Ontology Editor project*  
*Last system update: Check git log for `docs/` folder*
