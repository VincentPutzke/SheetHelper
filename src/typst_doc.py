from typst_fragment import TypstFragment

class TypstDoc:
    fragments = []
    add = None
    
    def __init__(self):
        """
        Initialize a TypstDoc instance and create a SnippetAdder.
        """
        self.fragments = []
        self.add = SnippetAdder(self)
    
    def add_fragment(self, fragment: TypstFragment):
        """
        Add a TypstFragment to the document.
        
        Args:
            fragment (TypstFragment): The fragment to add.
        """
        self.fragments.append(fragment)
    
    def to_text(self):
        """
        Convert the document to text by concatenating all fragment texts.
        
        Returns:
            str: The concatenated text of all fragments.
        """
        result = ""
        for fragment in self.fragments:
            result += fragment.to_text()
        return result
    
class SnippetAdder:
    def __init__(self, doc):
        """
        Initialize a SnippetAdder instance.
        
        Args:
            doc (TypstDoc): The document to which snippets will be added.
        """
        self.doc = doc
        
    def setup(self):
        """
        Add a setup fragment to the document.
        """
        self.doc.add_fragment(TypstFragment("This is a setup."))