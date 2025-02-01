import unittest

from unittest.mock import MagicMock
import result_modifyer

# from typst_builder import TypstBuilder
# from typst_doc import TypstDoc
# from typst_fragment import TypstFragment

class TestResultModifyer(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_find_after_last(self):
        text = "Some text <TYP>This is the content</TYP> more text <TYP>Another content</TYP>"
        result = result_modifyer._find_after_last(text, r"<TYP>")
        self.assertEqual(result, "Another content</TYP>")
        
        text = "Some text without typ!"
        result = result_modifyer._find_after_last(text, r"<TYP>")
        self.assertEqual(result, "")
    
        text = "This is the start. <TYP>Here is wrong text!</TYP><TYP>Here is the right text.</TYP>"
        result = result_modifyer._find_after_last(text, r"<TYP>")
        self.assertEqual(result, "Here is the right text.</TYP>")
        
    def test_find_before_first(self):
        text = "Some text <TYP>This is the content</TYP> more text <TYP>Another content</TYP>"
        result = result_modifyer._find_before_first(text, r"</TYP>")
        self.assertEqual(result, "Some text <TYP>This is the content")
        
        text = "Some text without typ!"
        result = result_modifyer._find_before_first(text, r"</TYP>")
        self.assertEqual(result, "Some text without typ!")
    
        text = "This is the start. <TYP>Here is wrong text!</TYP><TYP>Here is the right text.</TYP>"
        result = result_modifyer._find_before_first(text, r"</TYP>")
        self.assertEqual(result, "This is the start. <TYP>Here is wrong text!")
    
    def test_filter_code_result(self):
        text = "Some text <TYP>This is the content</TYP> more text <TYP>Another content</TYP>"
        result = result_modifyer.filter_code_result(text)
        self.assertEqual(result, "Another content")
        
        text = "Some text without typ!"
        result = result_modifyer.filter_code_result(text)
        self.assertEqual(result, "")
        
        text = "Some text with just <TYP> but no closing tag"
        result = result_modifyer.filter_code_result(text)
        self.assertEqual(result, " but no closing tag")
        
        text = "This is the start. <TYP>#table(\n  columns: ( auto, auto, auto),\n  [H0],[H1],[H2],\n  [C00],[C01],[C02],\n  [C10],[C11],[C12],\n  [C20],[C21],[C22],\n  [C30],[C31],[C32],\n  [C40],[C41],[C42],\n)</TYP> This is the ending."
        result = result_modifyer.filter_code_result(text)
        self.assertEqual(result, "#table(\n  columns: ( auto, auto, auto),\n  [H0],[H1],[H2],\n  [C00],[C01],[C02],\n  [C10],[C11],[C12],\n  [C20],[C21],[C22],\n  [C30],[C31],[C32],\n  [C40],[C41],[C42],\n)")
        
        text = "This is the start. <TYP>Here is wrong text!<TYP>Here is the right text.</TYP>"
        result = result_modifyer.filter_code_result(text)
        self.assertEqual(result, "Here is the right text.")