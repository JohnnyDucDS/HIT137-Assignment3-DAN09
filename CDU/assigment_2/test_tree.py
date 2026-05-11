import unittest
from tree import evaluate_tree, tree_to_string

class TestTreeFunctions(unittest.TestCase):
    # --- Tests for evaluate_tree ---

    def test_evaluate_simple_number(self):
        """Test evaluating a single number."""
        self.assertEqual(evaluate_tree("5"), 5.0)

    def test_evaluate_addition(self):
        """Test evaluating an addition operation."""
        self.assertEqual(evaluate_tree(('+', '2', '3')), 5.0)

    def test_evaluate_subtraction(self):
        """Test evaluating a subtraction operation."""
        self.assertEqual(evaluate_tree(('-', '10', '4')), 6.0)

    def test_evaluate_multiplication(self):
        """Test evaluating a multiplication operation."""
        self.assertEqual(evaluate_tree(('*', '3', '4')), 12.0)

    def test_evaluate_division(self):
        """Test evaluating a division operation."""
        self.assertEqual(evaluate_tree(('/', '10', '2')), 5.0)

    def test_evaluate_division_by_zero(self):
        """Test that division by zero raises ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            evaluate_tree(('/', '10', '0'))

    def test_evaluate_negation(self):
        """Test evaluating a negation operation."""
        self.assertEqual(evaluate_tree(('neg', '5')), -5.0)

    def test_evaluate_complex_tree(self):
        """Test evaluating a deeply nested tree."""
        # Represents: ((- (5 + 3)) * 2) -> (neg (+ 5 3)) * 2
        tree = ('*', ('neg', ('+', '5', '3')), '2')
        self.assertEqual(evaluate_tree(tree), -16.0)

    # --- Tests for tree_to_string ---

    def test_tree_to_string_simple(self):
        """Test converting a single number to string."""
        self.assertEqual(tree_to_string("5"), "5")

    def test_tree_to_string_negation(self):
        """Test converting a negation operation to string."""
        self.assertEqual(tree_to_string(('neg', '5')), "(neg 5)")

    def test_tree_to_string_addition(self):
        """Test converting an addition operation to string."""
        self.assertEqual(tree_to_string(('+', '2', '3')), "(+ 2 3)")

    def test_tree_to_string_complex(self):
        """Test converting a complex tree to string."""
        tree = ('*', ('neg', ('+', '5', '3')), '2')
        self.assertEqual(tree_to_string(tree), "(* (neg (+ 5 3)) 2)")

if __name__ == '__main__':
    unittest.main()
