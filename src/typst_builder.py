from dotenv import load_dotenv
import os
import re

from src.typst_doc import TypstDoc
from src.typst_fragment import TypstFragment
from src.ai_connect import AiConnect
import src.templates

class TypstBuilder():
    queued_fragments = []
    
    def __init__(self, grade, topic, language="deutsch"):
        self.grade = grade
        self.topic = topic
        self.language = language
        
        self.doc = TypstDoc()
        
        load_dotenv("src\.env")
        api_key = os.getenv("key")
        self.ai = AiConnect(api_key)
        
    def generate_table(self, small_topic, columns=3, rows=5):
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
    
    def _filter_answer(self, answer):
        # Get the text after the last <TYP>
        last_typ_index = answer.rfind('<TYP>')
        if last_typ_index == -1:
            return None
        
        text_after_last_typ = answer[last_typ_index + len('<TYP>'):]
        
        # Remove all text after the first </TYP>
        first_end_typ_index = text_after_last_typ.find('</TYP>')
        if first_end_typ_index == -1:
            return None
        
        result = text_after_last_typ[:first_end_typ_index]
        return result
    
    def clear_doc(self):
        self.doc.blocks = []
    
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
        result = self.doc.to_text()
        with open(f"output/{self.topic}.typ", "w", encoding="utf-8") as file:
            file.write(result)