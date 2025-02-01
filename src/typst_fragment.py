class TypstFragment:
    blocks = []
    
    def __init__(self, r_header):
        """
        Initialize a TypstFragment instance with a header.
        
        Args:
            r_header (str): The header text for the fragment.
        """
        self.blocks = []
        self.header = f"= {r_header}"
        self.task = ""
        
    def set_task(self, task):
        self.task = task
    
    def add(self, text):
        """
        Add a block of text to the fragment.
        
        Args:
            text (str): The text to add. If None, it will not be added.
        """
        if text is None:
            return
        self.blocks.append(text)
        
    def to_text(self):
        """
        Convert the fragment to text by concatenating the header and all blocks.
        
        Returns:
            str: The concatenated text of the header and all blocks.
        """
        result = self.header + "\n"
        if len(self.task) != 0:
            result += self.task + "\n"
        for block in self.blocks:
            result += block + "\n"
        return result