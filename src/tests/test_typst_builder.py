import unittest
from unittest.mock import MagicMock
from typst_builder import TypstBuilder
from typst_doc import TypstDoc
from typst_fragment import TypstFragment

class TestTypstBuilder(unittest.TestCase):
    
    def setUp(self):
        self.builder = TypstBuilder(5, "Test")
        self.builder.ai = MagicMock()

    def test_generate_table(self):
        self.builder.clear_doc()
        self.builder.clear_queue()
        
        self.builder.ai.send_request.return_value = "<TYP>Mocked AI response</TYP>"
        self.builder.ai.send_request = MagicMock(return_value="This is the start. <TYP>#table(\n  columns: ( auto, auto, auto),\n  [H0],[H1],[H2],\n  [C00],[C01],[C02],\n  [C10],[C11],[C12],\n  [C20],[C21],[C22],\n  [C30],[C31],[C32],\n  [C40],[C41],[C42],\n)</TYP> This is the ending.")
        
        # Call the generate_table method
        index = self.builder.generate_table("Small Topic", columns=3, rows=5)
        
        # Verify the AI request
        self.builder.ai.send_request.assert_called_once()
        
        # Verify the fragment was added to the queued_fragments
        self.assertEqual(index, 0)
        self.assertEqual(len(self.builder.queued_fragments), 1)
        fragment = self.builder.queued_fragments[0]
        self.assertIsInstance(fragment, TypstFragment)
        self.assertEqual(fragment.header, "= Small Topic")
        self.assertEqual(fragment.blocks, ["#table(\n  columns: ( auto, auto, auto),\n  [H0],[H1],[H2],\n  [C00],[C01],[C02],\n  [C10],[C11],[C12],\n  [C20],[C21],[C22],\n  [C30],[C31],[C32],\n  [C40],[C41],[C42],\n)"])
    
    def test_filter_answer(self):
        text = "Some text <TYP>This is the content</TYP> more text <TYP>Another content</TYP>"
        result = self.builder._filter_answer(text)
        self.assertEqual(result, "Another content")
        
        text = "Some text without typ!"
        result = self.builder._filter_answer(text)
        self.assertEqual(result, "")
        
        text = "Some text with just <TYP> but no closing tag"
        result = self.builder._filter_answer(text)
        self.assertEqual(result, "")
        
        text = "This is the start. <TYP>#table(\n  columns: ( auto, auto, auto),\n  [H0],[H1],[H2],\n  [C00],[C01],[C02],\n  [C10],[C11],[C12],\n  [C20],[C21],[C22],\n  [C30],[C31],[C32],\n  [C40],[C41],[C42],\n)</TYP> This is the ending."
        result = self.builder._filter_answer(text)
        self.assertEqual(result, "#table(\n  columns: ( auto, auto, auto),\n  [H0],[H1],[H2],\n  [C00],[C01],[C02],\n  [C10],[C11],[C12],\n  [C20],[C21],[C22],\n  [C30],[C31],[C32],\n  [C40],[C41],[C42],\n)")
        
    def test_export(self):
        self.builder.clear_doc()
        self.builder.clear_queue()
        self.builder.doc = MagicMock()
        self.builder.topic = "test_topic"
        self.builder.doc.to_text.return_value = "Test content with ä, ö, ü"
        self.builder.export()
        with open("output/test_topic.typ", "r", encoding="utf-8") as file:
            content = file.read()
        self.assertEqual(content, "Test content with ä, ö, ü")
    
    def test_clear_doc(self):
        self.builder.clear_doc()
        self.builder.clear_queue()
        self.builder.doc = TypstDoc()
        fragment = TypstFragment("Header")
        fragment.add("Content")
        self.builder.doc.add_fragment(fragment)
        self.builder.clear_doc()
        self.assertEqual(self.builder.doc.fragments, [])
    
    def test_setup_doc(self):
        self.builder.clear_doc()
        self.builder.clear_queue()
        self.builder.doc = MagicMock()
        self.builder.setup_doc()
        self.builder.doc.append.setup.assert_called_once()
    
    def test_view_fragment(self):
        self.builder.clear_doc()
        self.builder.clear_queue()
        fragment = TypstFragment("Header")
        fragment.add("Content")
        self.builder.queued_fragments.append(fragment)
        with unittest.mock.patch('builtins.print') as mocked_print:
            self.builder.view_fragment(0)
            mocked_print.assert_called_once_with("= Header\nContent\n")
    
    def test_add_to_doc(self):
        self.builder.clear_doc()
        self.builder.clear_queue()
        self.builder.doc = TypstDoc()
        fragment = TypstFragment("Header")
        fragment.add("Content")
        self.builder.queued_fragments.append(fragment)
        self.builder.add_to_doc(0)
        self.assertEqual(len(self.builder.doc.fragments), 1)
        self.assertEqual(self.builder.doc.fragments[0].header, "= Header")
        self.assertEqual(self.builder.doc.fragments[0].blocks, ["Content"])
    
    def test_build(self):
        self.builder.clear_doc()
        self.builder.clear_queue()
        self.builder.doc = TypstDoc()
        fragment = TypstFragment("Header")
        fragment.add("Content")
        self.builder.doc.add_fragment(fragment)
        with unittest.mock.patch('builtins.print') as mocked_print:
            self.builder.build()
            mocked_print.assert_called_once_with("= Header\nContent\n")
    
    def test_clear_queue(self):
        self.builder.clear_doc()
        self.builder.clear_queue()
        # Add some fragments to the queue
        fragment1 = TypstFragment("Header1")
        fragment1.add("Content1")
        fragment2 = TypstFragment("Header2")
        fragment2.add("Content2")
        self.builder.queued_fragments.append(fragment1)
        self.builder.queued_fragments.append(fragment2)
        
        # Verify the queue is not empty
        self.assertEqual(len(self.builder.queued_fragments), 2)
        
        # Call the clear_queue method
        self.builder.clear_queue()
        
        # Verify the queue is empty
        self.assertEqual(len(self.builder.queued_fragments), 0)
    
if __name__ == '__main__':
    unittest.main()