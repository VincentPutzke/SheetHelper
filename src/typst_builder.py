from dotenv import load_dotenv
import os
import re

from typst_doc import TypstDoc
from typst_fragment import TypstFragment
from ai_connect import AiConnect
import templates

class TypstBuilder():
    queued_fragments = []
    
    def __init__(self, grade, topic, language="deutsch"):
        """
        Initialize a TypstBuilder instance.
        
        Args:
            grade (int): The grade level.
            topic (str): The topic of the document.
            language (str): The language of the document. Default is "deutsch".
        """
        self.grade = grade
        self.topic = topic
        self.language = language
        
        self.doc = TypstDoc()
        
        # Load API key from environment variables
        load_dotenv("src/.env")
        api_key = os.getenv("key")
        self.ai = AiConnect(api_key)
        
    def generate_table(self, small_topic, columns=3, rows=5):
        """
        Generate a table with information about a small topic.
        
        Args:
            small_topic (str): The small topic for the table.
            columns (int): The number of columns in the table. Default is 3.
            rows (int): The number of rows in the table. Default is 5.
        
        Returns:
            str: The generated table as a string.
        """
        table = templates.generate_table_template(columns, rows)
        prompt = f"""Fill in this table with information about
        the topic {small_topic} in the scheme of {self.topic}.
        Write the typst-syntax answer in <TYP>...</TYP>.
        Here is the table: {table}"""
        result = self.ai.send_request(prompt)
        filtered_result = self._filter_answer(result)
        fragment = TypstFragment(small_topic)
        fragment.add(filtered_result)
        self.queued_fragments.append(fragment)
        return self.queued_fragments.index(fragment)
    
    def _filter_answer(self, text):
        """
        Filter the answer from the AI response.
        
        Args:
            text (str): The text containing the AI response.
        
        Returns:
            str: The filtered answer.
        """
        matches = re.findall(r"<TYP>(.*?)</TYP>", text, re.DOTALL)
        if matches:
            return matches[-1]
        return ""
    
    def clear_queue(self):
        self.queued_fragments = []
    
    def clear_doc(self):
        self.doc.fragments.clear()
    
    def setup_doc(self):
        self.doc.append.setup()
    
    def view_fragment(self, index):
        print(self.queued_fragments[index].to_text())
        
    def add_to_doc(self, index):
        self.doc.add_fragment(self.queued_fragments[index])
    
    def build(self):
        result = self.doc.to_text()
        print(result)
    
    def export(self):
        """
        Export the document to a .typ file.
        """
        content = self.doc.to_text()
        with open(f"output/{self.topic}.typ", "w", encoding="utf-8") as file:
            file.write(content)