from dotenv import load_dotenv
import os
import re

import result_modifyer
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
        
        table = templates.generate_table_data_template(columns, rows, ["ITEM" for i in range(columns)])
        
        prompt = f"""Replace the placeholders in this table with information about
        the topic {small_topic} in the scheme of {self.topic} in this language: {self.language}.
        Also, remember that this is for a worksheet for {self.grade}.-grade students.
        Write the csv-syntax answer in these start and end symbols: <TYP>...</TYP>.
        Here is the table: {table}"""
        
        result = self.ai.send_request(prompt)
        filtered_result = result_modifyer.filter_code_result(result)
        
        self._save_filtered_result(small_topic.replace(" ", "_"), filtered_result)
        
        combined_result = templates.combine_table_with_data(small_topic.replace(" ", "_"))
        
        fragment = TypstFragment(small_topic)
        fragment.add(combined_result)
        
        self.queued_fragments.append(fragment)
        
        return self.queued_fragments.index(fragment)
    
    def generate_combine(self, small_topic, rows=5):
        """
        Generate a Connect Task with information about a small topic.
        
        Args:
            small_topic (str): The small topic for the task.
            rows (int): The number of statements to connect. Default is 5.
        
        Returns:
            str: The generated table as a string.
        """
        
        table = templates.generate_table_data_template(2, rows, hints=["WORD", "DESCRIPTION"])
        
        prompt = f"""Replace the placeholders in this table with information about
        the topic {small_topic} in the scheme of {self.topic} in this language: {self.language}.
        Also, remember that this is for a worksheet for {self.grade}.-grade students.
        Write the csv-syntax answer in these start and end symbols: <TYP>...</TYP>.
        Here is the table: {table}
        
        Also, give a small task description (language: {self.language}) and put it in <TASK>...</TASK>"""
        
        result = self.ai.send_request(prompt)
        code_result = result_modifyer.filter_code_result(result)
        task_result = result_modifyer.filter_task_result(result)
        
        randomized_result = result_modifyer.randomize_row_order(code_result, 2)
        
        self._save_filtered_result(small_topic.replace(" ", "_"), randomized_result)
        
        combined_result = templates.combine_connect_with_template(small_topic.replace(" ", "_"))
        
        fragment = TypstFragment(small_topic)
        fragment.set_task(task_result)
        fragment.add(combined_result)
        
        
        self.queued_fragments.append(fragment)
        
        return self.queued_fragments.index(fragment)
    
    def _save_filtered_result(self, filename: str, csv_data: str):
        """Saves raw CSV text data to a file, creating the directory if necessary.

        Args:
            csv_data: The CSV data as a string.
            filename: The name of the file (without extension, e.g., "my_data").
        """
        try:
            directory = "output/data"  # Define the directory
            if not os.path.exists(directory):
                os.makedirs(directory)  # Create directory if it doesn't exist

            filepath = os.path.join(directory, f"{filename}.csv")  # Construct full file path
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(csv_data)
            print(f"CSV data saved to {filepath}")

        except Exception as e:
            print(f"An error occurred: {e}")
    
    def clear_queue(self):
        self.queued_fragments = []
    
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