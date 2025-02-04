import unittest
from unittest.mock import MagicMock
from typst_doc import TypstDoc, SnippetAdder
from typst_fragment import TypstFragment

class TestTypstDoc(unittest.TestCase):
    
    def setUp(self):
        self.doc = TypstDoc()
        self.snippet_adder = SnippetAdder(self.doc)
    
    def test_add_fragment(self):
        fragment = MagicMock(spec=TypstFragment)
        self.doc.add_fragment(fragment)
        self.assertIn(fragment, self.doc.fragments)
    
    def test_to_text(self):
        fragment1 = TypstFragment("H1")
        fragment1.add("Fragment 1 text.")
        fragment2 = TypstFragment("H2")
        fragment2.add("Fragment 2 text.")
        
        self.doc.add_fragment(fragment1)
        self.doc.add_fragment(fragment2)
        
        result = self.doc.to_text()
        self.assertEqual(result, '= H1\nFragment 1 text.\n= H2\nFragment 2 text.\n')
    
    def test_snippet_adder_setup(self):
        self.snippet_adder.setup()
        
        self.assertEquals("= This is a setup.\n", self.doc.fragments[-1].to_text())

if __name__ == '__main__':
    unittest.main()