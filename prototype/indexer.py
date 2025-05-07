import re
from collections import defaultdict

class Indexer:
    def __init__(self):
        self.index = defaultdict(
            lambda: {
                "doc_ids": [],
                "positions": [],
                "frequencies": []
            }
        )
        self.documents = {}
    
    def _tokenize(self, text):
        return re.findall(r'\w+', text.lower())
    
    def add(self, text):
        pass
    
    def update():
        pass
    
    def delete():
        pass
    
    def get(): 
        pass
    
    def fetchOne():
        pass
    
    
