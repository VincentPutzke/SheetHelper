import unittest
import groq
from groq import Groq

from unittest.mock import MagicMock, patch

from ai_connect import AiConnect

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
    
    @patch('groq.Groq')
    def test_send_request(self, MagicGroq):
        self.ai_connect.client = MagicGroq.return_value
        
        content = "Mocked response"
        delta_mock = MagicMock()
        delta_mock.content = content
        
        choices_mock = MagicMock()
        choices_mock.delta = delta_mock
        
        choices_list_mock = []
        choices_list_mock.append(choices_mock)
        
        chunk_mock = MagicMock()
        chunk_mock.choices = choices_list_mock
        
        response_mock = [chunk_mock]
        
        self.ai_connect.client.chat.completions.create = MagicMock(return_value=response_mock)
        
        result = self.ai_connect.send_request("test prompt")
        self.ai_connect.client.chat.completions.create.assert_called_with(
            model=self.ai_connect.model,
            messages=[
                {
                    'role':'user',
                    'content':'test prompt'
                }
            ],
            temperature=0.0,
            max_completion_tokens=4096,
            top_p=0.95,
            stream=True,
            stop=None
        )
        self.assertEqual(result, "Mocked response")
        
if __name__ == '__main__':
    unittest.main()