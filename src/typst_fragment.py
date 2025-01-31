

class TypstFragment:
    blocks = []
    
    def __init__(self, r_header):
        self.header = f"= {r_header}"
        
    def add(self, text):
        if text is None:
            return
        self.blocks.append(text)
        
    def to_text(self):
        result = self.header + "\n"
        for block in self.blocks:
            result += block + "\n"
        return result