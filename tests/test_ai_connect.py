import unittest
from dotenv import load_dotenv
import os

from src.ai_connect import AiConnect

class TestAiConnect(unittest.TestCase):
    
    def setUp(self):
        self.api_key = "test_api_key"
        self.ai_connect = AiConnect(self.api_key)
    
    def test_initial_api_key(self):
        self.assertEqual(self.ai_connect.client.api_key, "test_api_key")
    
    def test_initial_model(self):
        self.assertEqual(self.ai_connect.model, "deepseek-r1-distill-llama-70b")
    
    def test_use_llama(self):
        self.ai_connect.use_llama()
        self.assertEqual(self.ai_connect.model, "llama-3.3-70b-versatile")
    
    def test_use_mistral(self):
        self.ai_connect.use_mistral()
        self.assertEqual(self.ai_connect.model, "mixtral-8x7b-32768")
    
    def load_api_key(self):
        load_dotenv("src\.env")
        self.api_key = os.getenv('key')
        self.ai_connect.client.api_key = self.api_key
    
    def test_send_request(self):
        raw_prompt = "test raw prompt"
        self.load_api_key()
        completion = self.ai_connect.send_request(raw_prompt)
        self.assertIsNotNone(completion.response)
    
    
if __name__ == '__main__':
    unittest.main()