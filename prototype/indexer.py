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
    
    def add(self, doc_id, content):
        if doc_id in self.documents:
            print(f'Document with {doc_id} is already present. Try updating or deleting.')
            return False
        
        tokens = self._tokenize(content)
        self.documents[doc_id] = {
            "tokens": tokens,
            "content": content
        }
        
        term_positions = defaultdict(list)
        
        for position, token in enumerate(tokens):
            term_positions[token].append(position)
            
        for term, positions in term_positions.items():
            term_obj = self.index[term]
           
            term_obj["doc_ids"].append(doc_id) 
            term_obj["positions"].append(positions)
            term_obj["frequencies"].append(len(positions))
            
        return True
            
    def update(self, doc_id, new_content):
        if not self.delete(doc_id):
            return False
        return self.add(doc_id, new_content)
    
    
    def delete(self, doc_id):
        if doc_id not in self.documents:
            print(f'Document with id {doc_id} doesn\'t exist.')
            return False

        tokens = self.documents[doc_id]["tokens"]
        
        seen = set()
        
        for token in tokens:
            if token in seen:
                continue
            seen.add(token)
            
            term_obj = self.index[token]
            
            if doc_id in term_obj["doc_ids"]:
                idx = term_obj["doc_ids"].index(doc_id)
            
                del term_obj["doc_ids"][idx]
                del term_obj["positions"][idx]
                del term_obj["frequencies"][idx]
                
                if not term_obj["doc_ids"]:
                    del self.index[token]
        
        del self.documents[doc_id]
        return True
     
    
    def get(): 
        pass
    
    def fetchOne():
        pass
    
    
if __name__ == '__main__':
    indexer = Indexer()

    indexer.add("doc1", "this is testing the freqs because freqs matter")
    indexer.add("doc2", "that is testing the freqs")
    indexer.add("doc3", "dad is testing the freqs")
    indexer.add("doc4", "mom is testing the freqs")

    print(indexer.index)

    indexer.delete('doc1')
    indexer.delete('doc2')
    indexer.delete('doc3')
    indexer.delete('doc4')

    print('=========After deleting all objects================')


    print(indexer.index)