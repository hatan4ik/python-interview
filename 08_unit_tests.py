#!/usr/bin/env python3
import unittest
from typing import List

# Import the logic we want to test.
# Note: In a real project, you'd likely structure imports differently,
# but for this repo, we import directly from the script file.
# We import 'is_balanced' from script 05.
from importlib.machinery import SourceFileLoader

# Dynamic import trick because filenames start with numbers (05_...)
# which Python doesn't allow in standard 'import' statements.
algo_module = SourceFileLoader("algo", "05_algorithm_warmup.py").load_module()

# ==========================================
# SCENARIO: Quality Assurance
# FAANG Question: "How do you ensure your code doesn't break?"
# ANSWER: "I write Unit Tests covering edge cases."
# ==========================================

class TestBracketLogic(unittest.TestCase):
    
    def test_balanced_simple(self):
        """Test simple balanced cases."""
        self.assertTrue(algo_module.is_balanced("{}"))
        self.assertTrue(algo_module.is_balanced("[]"))
        self.assertTrue(algo_module.is_balanced("()"))
        
    def test_balanced_nested(self):
        """Test complex nested cases."""
        self.assertTrue(algo_module.is_balanced("{[()]}"))
        self.assertTrue(algo_module.is_balanced("({[]})"))
        
    def test_unbalanced_mismatch(self):
        """Test mismatched brackets."""
        self.assertFalse(algo_module.is_balanced("{]"))
        self.assertFalse(algo_module.is_balanced("(]"))
        self.assertFalse(algo_module.is_balanced("[}"))
        
    def test_unbalanced_open(self):
        """Test unclosed brackets."""
        self.assertFalse(algo_module.is_balanced("((("))
        self.assertFalse(algo_module.is_balanced("{"))
        
    def test_empty_string(self):
        """Edge Case: Empty string is technically balanced (0 errors)."""
        self.assertTrue(algo_module.is_balanced(""))

    def test_with_text(self):
        """Test brackets mixed with text."""
        self.assertTrue(algo_module.is_balanced("{ key: [val] }"))
        self.assertFalse(algo_module.is_balanced("function( { )"))

class TestFizzBuzz(unittest.TestCase):
    
    def test_output_capture(self):
        """
        Testing print statements is hard. 
        In a real interview, you would refactor 'devops_fizzbuzz' to RETURN a list
        instead of printing it, so it's testable.
        
        This test serves as a placeholder to discuss 'Testability' with the interviewer.
        """
        pass

if __name__ == '__main__':
    print("--- Running Unit Tests ---")
    unittest.main()
