#!/usr/bin/env python3
"""
Generate embeddings for all structures in the ontology.
Run this locally whenever structures change.

Usage:
    pip install sentence-transformers
    python scripts/generate_embeddings.py
"""

import json
from pathlib import Path
import yaml

# Try to import sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
    HAS_EMBEDDINGS = True
except ImportError:
    HAS_EMBEDDINGS = False
    print("Install sentence-transformers: pip install sentence-transformers")


def load_all_structures() -> list[dict]:
    """Load all structures from YAML files."""
    structures = []
    structures_dir = Path('structures')
    
    for yaml_file in structures_dir.glob('*.yaml'):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
            if data and 'structures' in data:
                for struct in data['structures']:
                    structures.append({
                        'id': struct.get('id', ''),
                        'name': struct.get('name', ''),
                        'definition': struct.get('definition', ''),
                        'parent': struct.get('parent', ''),
                        'file': yaml_file.name
                    })
    
    return structures


def generate_embeddings(structures: list[dict]) -> dict:
    """Generate embeddings for all structures."""
    if not HAS_EMBEDDINGS:
        raise RuntimeError("sentence-transformers not installed")
    
    # Use a small, fast model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Create text for each structure (name + definition for better matching)
    texts = []
    for s in structures:
        text = s['name']
        if s.get('definition'):
            text += f" - {s['definition']}"
        texts.append(text)
    
    print(f"Generating embeddings for {len(texts)} structures...")
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Build output
    result = {
        'model': 'all-MiniLM-L6-v2',
        'structures': []
    }
    
    for i, struct in enumerate(structures):
        result['structures'].append({
            'id': struct['id'],
            'name': struct['name'],
            'definition': struct.get('definition', ''),
            'embedding': embeddings[i].tolist()
        })
    
    return result


def main():
    if not HAS_EMBEDDINGS:
        print("ERROR: Install sentence-transformers first:")
        print("  pip install sentence-transformers")
        return
    
    print("Loading structures...")
    structures = load_all_structures()
    print(f"Found {len(structures)} structures")
    
    print("\nGenerating embeddings...")
    data = generate_embeddings(structures)
    
    output_file = Path('data/embeddings.json')
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(data, f)
    
    print(f"\n✅ Saved to {output_file}")
    print(f"   File size: {output_file.stat().st_size / 1024:.1f} KB")


if __name__ == '__main__':
    main()
