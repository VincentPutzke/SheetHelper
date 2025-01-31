from groq import Groq

class AiConnect():
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
        self.use_deepseek()
        
    def use_deepseek(self):
        self.model = "deepseek-r1-distill-llama-70b"
        
    def use_llama(self):
        self.model = "llama-3.3-70b-versatile"
        
    def use_mistral(self):
        self.model = "mixtral-8x7b-32768"
    
    def send_request(self, raw_prompt):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    'role':'user',
                    'content':raw_prompt
                }
            ],
            temperature=0.6,
            max_completion_tokens=4096,
            top_p=0.95,
            stream=True,
            stop=None
        )
        return completion