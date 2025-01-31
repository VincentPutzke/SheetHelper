import unittest
from unittest.mock import MagicMock
from src.typst_builder import TypstBuilder

class TestTypstBuilder(unittest.TestCase):
    
    def setUp(self):
        self.builder = TypstBuilder(5, "Test")
    
    def test_filter_answer(self):
        text = "Some text <TYP>This is the content</TYP> more text <TYP>Another content</TYP>"
        result = self.builder._filter_answer(text)
        self.assertEqual(result, "Another content")
    
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