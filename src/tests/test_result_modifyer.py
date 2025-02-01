import unittest

from unittest.mock import MagicMock, patch
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
        
    def test_filter_task_result(self):
        text = "Some text <TASK>This is the content</TASK> more text <TASK>Another content</TASK>"
        result = result_modifyer.filter_task_result(text)
        self.assertEqual(result, "Another content")
        
        text = "Some text without TASK!"
        result = result_modifyer.filter_task_result(text)
        self.assertEqual(result, "")
        
        text = "Some text with just <TASK> but no closing tag"
        result = result_modifyer.filter_task_result(text)
        self.assertEqual(result, " but no closing tag")
        
        text = "This is the start. <TASK>#table(\n  columns: ( auto, auto, auto),\n  [H0],[H1],[H2],\n  [C00],[C01],[C02],\n  [C10],[C11],[C12],\n  [C20],[C21],[C22],\n  [C30],[C31],[C32],\n  [C40],[C41],[C42],\n)</TASK> This is the ending."
        result = result_modifyer.filter_task_result(text)
        self.assertEqual(result, "#table(\n  columns: ( auto, auto, auto),\n  [H0],[H1],[H2],\n  [C00],[C01],[C02],\n  [C10],[C11],[C12],\n  [C20],[C21],[C22],\n  [C30],[C31],[C32],\n  [C40],[C41],[C42],\n)")
        
        text = "This is the start. <TASK>Here is wrong text!<TASK>Here is the right text.</TASK>"
        result = result_modifyer.filter_task_result(text)
        self.assertEqual(result, "Here is the right text.")
    
    def test_filter_with_pattern(self):
        text = "Some text <PATTERN>This is the content</PATTERN> more text <PATTERN>Another content</PATTERN>"
        result = result_modifyer._filter_with_pattern(text, r"<PATTERN>", r"</PATTERN>")
        self.assertEqual(result, "Another content")
        
        text = "Some text without PATTERN!"
        result = result_modifyer._filter_with_pattern(text, r"<PATTERN>", r"</PATTERN>")
        self.assertEqual(result, "")
        
        text = "Some text !PATTERN with other patterns /PATTERN"
        result = result_modifyer._filter_with_pattern(text, "!PATTERN", "/PATTERN")
        self.assertEqual(result, " with other patterns ")
        
        text = "Some text with just <HTML> but no closing tag"
        result = result_modifyer._filter_with_pattern(text, r"<HTML>", r"</HTML>")
        self.assertEqual(result, " but no closing tag")
        
        text = "This is the start. <TASK>#table(\n  columns: ( auto, auto, auto),\n  [H0],[H1],[H2],\n  [C00],[C01],[C02],\n  [C10],[C11],[C12],\n  [C20],[C21],[C22],\n  [C30],[C31],[C32],\n  [C40],[C41],[C42],\n)</HTML> This is the ending."
        result = result_modifyer._filter_with_pattern(text, r"<TASK>", r"</HTML>")
        self.assertEqual(result, "#table(\n  columns: ( auto, auto, auto),\n  [H0],[H1],[H2],\n  [C00],[C01],[C02],\n  [C10],[C11],[C12],\n  [C20],[C21],[C22],\n  [C30],[C31],[C32],\n  [C40],[C41],[C42],\n)")
        
        text = "This is the start. <TASK>Here is wrong text!<TASK>Here is the right text.</HTML>"
        result = result_modifyer._filter_with_pattern(text, r"<TASK>", r"</HTML>")
        self.assertEqual(result, "Here is the right text.")
    
    @patch('numpy.random.shuffle')
    def test_randomize_row_order(self, mock_shuffle):
        # Test case 1: Basic test with 3 columns
        text = "\"Name\",\"Age\",\"City\"\n\"Alice\",\"25\",\"New York\"\n\"Bob\",\"30\",\"London\"\n\"Charlie\",\"22\",\"Paris\""
        column_count = 3
        expected_header = "\"Name\",\"Age\",\"City\"\n"
        
        # Define the shuffle behavior.  Crucially, we control the order!
        mock_shuffle.side_effect = lambda x: x.reverse()  # Reverse the order for predictable testing

        result = result_modifyer.randomize_row_order(text, column_count)
        
        expected_rows = "\"Charlie\",\"22\",\"Paris\"\n\"Bob\",\"30\",\"London\"\n\"Alice\",\"25\",\"New York\"\n"
        self.assertEqual(result, expected_header + expected_rows)

        # Test case 2:  Different data, 2 columns
        text = "\"Product\",\"Price\"\n\"A\", \"10\"\n\"B\", \"20\"\n\"C\", \"30\""
        column_count = 2
        mock_shuffle.side_effect = lambda x: x.sort() # Sort for a different predictable test

        result = result_modifyer.randomize_row_order(text, column_count)
        expected_header = "\"Product\",\"Price\"\n"
        expected_rows = "\"A\",\"10\"\n\"B\",\"20\"\n\"C\",\"30\"\n" # Already sorted
        self.assertEqual(result, expected_header + expected_rows)