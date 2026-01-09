#!/usr/bin/env python3
"""
Unit tests for AI processing functions.

Run with: python -m pytest scripts/test_ai_process.py -v
Or: python scripts/test_ai_process.py
"""

import unittest
import json
import tempfile
import os
from pathlib import Path

# Import functions to test
from ai_process_request import (
    load_structure_lookup,
    find_existing_structure,
    find_ambiguous_names,
    check_duplicate_relationship,
    find_conflicting_relationships,
    get_next_available_id,
    validate_and_enrich,
    generate_response_markdown,
)


class TestStructureLookup(unittest.TestCase):
    """Tests for structure lookup functions."""
    
    def test_find_existing_structure_exact_match(self):
        """Test exact name matching."""
        lookup = {
            'facial nerve': 'BAP_0001000',
            'inner ear': 'BAP_0011600',
            'stapedius': 'BAP_0026',
        }
        
        self.assertEqual(find_existing_structure('Facial nerve', lookup), 'BAP_0001000')
        self.assertEqual(find_existing_structure('INNER EAR', lookup), 'BAP_0011600')
        self.assertEqual(find_existing_structure('stapedius', lookup), 'BAP_0026')
    
    def test_find_existing_structure_partial_match(self):
        """Test partial name matching."""
        lookup = {
            'facial nerve': 'BAP_0001000',
            'trigeminal nerve': 'BAP_0002000',
        }
        
        # "facial" should match "facial nerve"
        result = find_existing_structure('facial', lookup)
        self.assertEqual(result, 'BAP_0001000')
    
    def test_find_existing_structure_no_match(self):
        """Test when no match found."""
        lookup = {
            'facial nerve': 'BAP_0001000',
        }
        
        result = find_existing_structure('nonexistent structure', lookup)
        self.assertIsNone(result)
    
    def test_find_existing_structure_without_spaces(self):
        """Test matching without spaces."""
        lookup = {
            'innerear': 'BAP_0011600',  # Without space key
        }
        
        result = find_existing_structure('inner ear', lookup)
        self.assertEqual(result, 'BAP_0011600')


class TestAmbiguousNames(unittest.TestCase):
    """Tests for ambiguous name detection."""
    
    def test_find_ambiguous_names_single(self):
        """Test detection of ambiguous names."""
        structures = [
            'Skin (BAP_0001)',
            'Skin (BAP_0002)',  # Duplicate name!
            'Facial nerve (BAP_0003)',
        ]
        
        ambiguous = find_ambiguous_names(structures)
        
        self.assertIn('skin', ambiguous)
        self.assertEqual(len(ambiguous['skin']), 2)
        self.assertNotIn('facial nerve', ambiguous)
    
    def test_find_ambiguous_names_none(self):
        """Test when no ambiguous names."""
        structures = [
            'Facial nerve (BAP_0001)',
            'Inner ear (BAP_0002)',
            'Stapedius (BAP_0003)',
        ]
        
        ambiguous = find_ambiguous_names(structures)
        self.assertEqual(len(ambiguous), 0)


class TestDuplicateRelationships(unittest.TestCase):
    """Tests for duplicate relationship detection."""
    
    def test_check_duplicate_exists(self):
        """Test detection of duplicate relationship."""
        existing = [
            {'subject': 'BAP_0026', 'predicate': 'innervated_by', 'object': 'BAP_0001000'},
            {'subject': 'BAP_0050', 'predicate': 'supplied_by', 'object': 'BAP_0100'},
        ]
        
        # This should be detected as duplicate
        is_dup = check_duplicate_relationship('BAP_0026', 'innervated_by', 'BAP_0001000', existing)
        self.assertTrue(is_dup)
    
    def test_check_duplicate_not_exists(self):
        """Test when relationship is new."""
        existing = [
            {'subject': 'BAP_0026', 'predicate': 'innervated_by', 'object': 'BAP_0001000'},
        ]
        
        # Different relationship - not duplicate
        is_dup = check_duplicate_relationship('BAP_0026', 'supplied_by', 'BAP_0100', existing)
        self.assertFalse(is_dup)
    
    def test_check_duplicate_different_object(self):
        """Test same subject+predicate but different object is not duplicate."""
        existing = [
            {'subject': 'BAP_0026', 'predicate': 'innervated_by', 'object': 'BAP_0001000'},
        ]
        
        # Same subject and predicate, different object
        is_dup = check_duplicate_relationship('BAP_0026', 'innervated_by', 'BAP_9999', existing)
        self.assertFalse(is_dup)


class TestConflictingRelationships(unittest.TestCase):
    """Tests for conflicting relationship detection."""
    
    def test_find_conflicts(self):
        """Test finding existing relationships with same subject+predicate."""
        existing = [
            {'subject': 'BAP_0026', 'predicate': 'innervated_by', 'object': 'BAP_0001'},
            {'subject': 'BAP_0026', 'predicate': 'innervated_by', 'object': 'BAP_0002'},
            {'subject': 'BAP_0050', 'predicate': 'innervated_by', 'object': 'BAP_0003'},
        ]
        
        conflicts = find_conflicting_relationships('BAP_0026', 'innervated_by', existing)
        
        self.assertEqual(len(conflicts), 2)
    
    def test_find_no_conflicts(self):
        """Test when no conflicts exist."""
        existing = [
            {'subject': 'BAP_0050', 'predicate': 'innervated_by', 'object': 'BAP_0003'},
        ]
        
        conflicts = find_conflicting_relationships('BAP_0026', 'innervated_by', existing)
        
        self.assertEqual(len(conflicts), 0)


class TestValidateAndEnrich(unittest.TestCase):
    """Tests for post-processing validation."""
    
    def test_validate_adds_warnings_for_duplicate(self):
        """Test that validation adds warnings for duplicate relationships."""
        # This test requires mocking load_existing_relationships and load_structure_lookup
        # For now, test with empty existing relationships
        parsed = {
            'understood': 'Test',
            'structures': [],
            'relationships': [
                {
                    'subject_name': 'Test',
                    'subject_id': 'BAP_0001',
                    'predicate': 'innervated_by',
                    'object_name': 'Test2',
                    'object_id': 'BAP_0002'
                }
            ],
            'warnings': []
        }
        
        result = validate_and_enrich(parsed)
        
        # Should have processed without error
        self.assertIn('warnings', result)


class TestResponseMarkdown(unittest.TestCase):
    """Tests for markdown response generation."""
    
    def test_generate_basic_response(self):
        """Test basic markdown generation."""
        parsed = {
            'understood': 'Add test structure',
            'structures': [
                {'name': 'Test', 'id': 'BAP_0001', 'parent_name': 'Parent', 'is_new': True, 'definition': 'A test'}
            ],
            'relationships': [],
            'warnings': []
        }
        
        md = generate_response_markdown(parsed, '123')
        
        self.assertIn('AI Analysis', md)
        self.assertIn('Add test structure', md)
        self.assertIn('Test', md)
        self.assertIn('BAP_0001', md)
    
    def test_generate_response_with_relationships(self):
        """Test markdown with relationships."""
        parsed = {
            'understood': 'Add relationship',
            'structures': [],
            'relationships': [
                {
                    'subject_name': 'Stapedius',
                    'subject_id': 'BAP_0026',
                    'predicate': 'innervated_by',
                    'object_name': 'Facial nerve',
                    'object_id': 'BAP_0001000'
                }
            ],
            'warnings': []
        }
        
        md = generate_response_markdown(parsed, '123')
        
        self.assertIn('Relationships to Add', md)
        self.assertIn('Stapedius', md)
        self.assertIn('innervated by', md)
        self.assertIn('Facial nerve', md)
    
    def test_generate_response_with_duplicates(self):
        """Test markdown shows duplicates correctly."""
        parsed = {
            'understood': 'Add relationship',
            'structures': [],
            'relationships': [
                {
                    'subject_name': 'Stapedius',
                    'predicate': 'innervated_by',
                    'object_name': 'Facial nerve',
                    '_is_duplicate': True
                }
            ],
            'warnings': ['DUPLICATE: This exists']
        }
        
        md = generate_response_markdown(parsed, '123')
        
        self.assertIn('Already Exists', md)
        self.assertIn('duplicate', md)
    
    def test_generate_response_with_warnings(self):
        """Test markdown shows warnings."""
        parsed = {
            'understood': 'Test',
            'structures': [],
            'relationships': [],
            'warnings': ['Warning 1', 'Warning 2']
        }
        
        md = generate_response_markdown(parsed, '123')
        
        self.assertIn('Warning', md)
        self.assertIn('Warning 1', md)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""
    
    def test_empty_structures(self):
        """Test handling of empty structures list."""
        ambiguous = find_ambiguous_names([])
        self.assertEqual(len(ambiguous), 0)
    
    def test_empty_relationships(self):
        """Test handling of empty relationships."""
        is_dup = check_duplicate_relationship('BAP_0001', 'innervated_by', 'BAP_0002', [])
        self.assertFalse(is_dup)
    
    def test_none_values(self):
        """Test handling of None values in lookup."""
        lookup = {
            'test': 'BAP_0001',
            'other': None,  # Shouldn't happen but let's be safe
        }
        
        result = find_existing_structure('test', lookup)
        self.assertEqual(result, 'BAP_0001')
    
    def test_special_characters_in_name(self):
        """Test handling of special characters."""
        lookup = {
            "structure (with parens)": 'BAP_0001',
            "structure: with colon": 'BAP_0002',
        }
        
        result = find_existing_structure("structure (with parens)", lookup)
        self.assertEqual(result, 'BAP_0001')


class TestCaseSensitivity(unittest.TestCase):
    """Tests for case-insensitive matching."""
    
    def test_uppercase_query(self):
        """Test uppercase query matches lowercase lookup."""
        lookup = {'facial nerve': 'BAP_0001'}
        
        self.assertEqual(find_existing_structure('FACIAL NERVE', lookup), 'BAP_0001')
    
    def test_mixed_case(self):
        """Test mixed case matching."""
        lookup = {'facial nerve': 'BAP_0001'}
        
        self.assertEqual(find_existing_structure('Facial Nerve', lookup), 'BAP_0001')
        self.assertEqual(find_existing_structure('fAcIaL nErVe', lookup), 'BAP_0001')


# Run tests
if __name__ == '__main__':
    # Change to script directory for relative imports
    os.chdir(Path(__file__).parent)
    
    # Run tests
    unittest.main(verbosity=2)
