import unittest
from unittest.mock import MagicMock
from typst_builder import TypstBuilder
from typst_fragment import TypstFragment

class TestTypstBuilder(unittest.TestCase):
    
    def setUp(self):
        self.builder = TypstBuilder(5, "Test")
        self.builder.ai = MagicMock()
    
    def test_generate_table(self):
        # Mock the AI response
        self.builder.ai.send_request.return_value = "<TYP>Mocked AI response</TYP>"
        
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
        self.assertEqual(fragment.blocks, ["Mocked AI response"])
    
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
        
        text = "Some text with just </TYP> but no opening tag"
        result = self.builder._filter_answer(text)
        self.assertEqual(result, "")
        
        text = "Some text with reversed tags </TYP>...<TYP>"
        result = self.builder._filter_answer(text)
        self.assertEqual(result, "")
    
    def test_export(self):
        self.builder.doc = MagicMock()
        self.builder.topic = "test_topic"
        self.builder.doc.to_text.return_value = "Test content with ä, ö, ü"
        self.builder.export()
        with open("output/test_topic.typ", "r", encoding="utf-8") as file:
            content = file.read()
        self.assertEqual(content, "Test content with ä, ö, ü")

if __name__ == '__main__':
    unittest.main()