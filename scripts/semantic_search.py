#!/usr/bin/env python3
"""
Semantic search for finding existing structures.
Uses pre-computed embeddings (no model needed at runtime).
"""

import json
import numpy as np
from pathlib import Path


def load_embeddings() -> dict | None:
    """Load pre-computed embeddings."""
    embeddings_file = Path('data/embeddings.json')
    
    if not embeddings_file.exists():
        return None
    
    with open(embeddings_file) as f:
        return json.load(f)


def cosine_similarity(a: list, b: list) -> float:
    """Calculate cosine similarity between two vectors."""
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def find_similar_structures(query: str, embeddings_data: dict, top_k: int = 5, threshold: float = 0.5) -> list[dict]:
    """
    Find structures similar to the query.
    
    Note: This requires the same embedding model used during generation.
    For GitHub Actions, we use a simple fallback (exact/fuzzy match).
    """
    # Try to use sentence-transformers if available
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        query_embedding = model.encode(query).tolist()
    except ImportError:
        # Fallback: exact name matching
        return find_by_name(query, embeddings_data)
    
    results = []
    for struct in embeddings_data['structures']:
        similarity = cosine_similarity(query_embedding, struct['embedding'])
        if similarity >= threshold:
            results.append({
                'id': struct['id'],
                'name': struct['name'],
                'definition': struct.get('definition', ''),
                'similarity': float(similarity)
            })
    
    # Sort by similarity
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results[:top_k]


def find_by_name(query: str, embeddings_data: dict) -> list[dict]:
    """Fallback: Find by exact or partial name match."""
    query_lower = query.lower().strip()
    results = []
    
    for struct in embeddings_data['structures']:
        name_lower = struct['name'].lower()
        
        # Exact match
        if name_lower == query_lower:
            results.append({
                'id': struct['id'],
                'name': struct['name'],
                'definition': struct.get('definition', ''),
                'similarity': 1.0,
                'match_type': 'exact'
            })
        # Partial match
        elif query_lower in name_lower or name_lower in query_lower:
            results.append({
                'id': struct['id'],
                'name': struct['name'],
                'definition': struct.get('definition', ''),
                'similarity': 0.8,
                'match_type': 'partial'
            })
    
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results[:5]


def find_structure_id(name: str, embeddings_data: dict = None) -> str | None:
    """
    Find the best matching structure ID for a given name.
    Returns None if no good match found.
    """
    if embeddings_data is None:
        embeddings_data = load_embeddings()
    
    if embeddings_data is None:
        return None
    
    matches = find_by_name(name, embeddings_data)
    
    if matches and matches[0]['similarity'] >= 0.8:
        return matches[0]['id']
    
    return None


# Quick lookup dictionary
_name_to_id_cache = {}

def build_name_cache(embeddings_data: dict):
    """Build a quick lookup cache."""
    global _name_to_id_cache
    _name_to_id_cache = {}
    
    for struct in embeddings_data['structures']:
        name_lower = struct['name'].lower()
        _name_to_id_cache[name_lower] = struct['id']


def quick_lookup(name: str) -> str | None:
    """Quick exact name lookup."""
    return _name_to_id_cache.get(name.lower())


if __name__ == '__main__':
    # Test
    data = load_embeddings()
    if data:
        print(f"Loaded {len(data['structures'])} structures")
        
        # Test searches
        tests = ["facial nerve", "inner ear", "masseter", "stapedius"]
        for test in tests:
            results = find_by_name(test, data)
            print(f"\n'{test}':")
            for r in results[:3]:
                print(f"  {r['name']} ({r['id']}) - {r['similarity']:.2f}")
    else:
        print("No embeddings found. Run generate_embeddings.py first.")
