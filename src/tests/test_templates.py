import unittest
from templates import generate_table_template

class TestTemplates(unittest.TestCase):
    
    def test_generate_table_template(self):
        # Test with 3 columns and 2 rows
        columns = 3
        rows = 2
        expected_output = '#table(\n  columns: ( auto,  auto,  auto),\n  [*HEADER 0*], [*HEADER 1*], [*HEADER 2*],\n  [CELL 0 0], [CELL 0 1], [CELL 0 2],\n  [CELL 1 0], [CELL 1 1], [CELL 1 2],\n\n)'
        result = generate_table_template(columns, rows)
        self.assertEqual(result, expected_output)
        
        # Test with 1 column and 1 row
        columns = 1
        rows = 1
        expected_output = '#table(\n  columns: ( auto),\n  [*HEADER 0*],\n  [CELL 0 0],\n\n)'
        result = generate_table_template(columns, rows)
        self.assertEqual(result, expected_output)
        
        # Test with 2 columns and 3 rows
        columns = 2
        rows = 3
        expected_output = '#table(\n  columns: ( auto,  auto),\n  [*HEADER 0*], [*HEADER 1*],\n  [CELL 0 0], [CELL 0 1],\n  [CELL 1 0], [CELL 1 1],\n  [CELL 2 0], [CELL 2 1],\n\n)'
        result = generate_table_template(columns, rows)
        self.assertEqual(result, expected_output)
        
        # Test with 3 columns and 0 rows (edge case)
        columns = 3
        rows = 0
        expected_output = '#table(\n  columns: ( auto,  auto,  auto),\n  [*HEADER 0*], [*HEADER 1*], [*HEADER 2*],\n\n)'
        result = generate_table_template(columns, rows)
        self.assertEqual(result, expected_output)
        
        # Test with 0 columns and 0 rows (edge case)
        columns = 0
        rows = 0
        expected_output = "#table(\n  columns: ( ),\n)\n"
        result = generate_table_template(columns, rows)
        self.assertEqual(result, expected_output)

if __name__ == '__main__': 
    unittest.main()