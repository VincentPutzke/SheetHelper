import unittest
from typst_fragment import TypstFragment

class TestTypstFragment(unittest.TestCase):
    
    def setUp(self):
        self.fragment = TypstFragment("Header")
    
    def test_add(self):
        self.fragment.add("First block")
        self.fragment.add("Second block")
        self.assertEqual(self.fragment.blocks, ["First block", "Second block"])
    
    def test_add_none(self):
        self.fragment.add(None)
        self.assertEqual(self.fragment.blocks, [])
    
    def test_to_text(self):
        self.fragment.add("First block")
        self.fragment.add("Second block")
        result = self.fragment.to_text()
        expected = "= Header\nFirst block\nSecond block\n"
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()