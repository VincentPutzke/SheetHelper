from typst_fragment import TypstFragment

class TypstDoc:
    fragments = []
    add = None
    
    def __init__(self):
        self.add = SnippetAdder(self)
    
    def add_fragment(self, fragment: TypstFragment):
        self.fragments.append(fragment)
    
    def to_text(self):
        result = ""
        for fragment in self.fragments:
            result += fragment.to_text()
        return result
    
class SnippetAdder:
    def __init__(self, doc):
        self.doc = doc
        
    def setup(self):
        self.doc.add_fragment("This is a setup.")