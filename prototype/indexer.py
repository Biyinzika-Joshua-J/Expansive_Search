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
     
    
    def get(self, term): 
        term = term.lower()
        return self.index.get(term, None)
    
    def fetchOne(self, doc_id):
        return self.documents[doc_id]["content"]
    
    def search_phrase(self, phrase):
        tokens = self._tokenize(phrase)
        
        if not tokens:
            return []
        
        results = []
        
        entry = self.index[tokens[0]]
        
        if not entry:
            return []
        
        for idx, doc_id in enumerate(entry["doc_ids"]):
            for position in entry["positions"][idx]:
                if self._match_phrase_at(doc_id, position, tokens):
                    result = {
                        "content": self.documents[doc_id]["content"],
                        "location": [position, position+len(tokens)]
                    }
                    results.append(result)
        
        return results
    
    def _match_phrase_at(self, doc_id, start_position, words):
        document_tokens = self.documents[doc_id]["tokens"]
        
        for offeset, word in enumerate(words):
            offset_position = start_position + offeset
            if offset_position >= len(document_tokens) or document_tokens[offset_position] != word:
                return False 
        
        return True
    
if __name__ == '__main__':
    indexer = Indexer()

    indexer.add("doc1", "this is testing the freqs because freqs matter")
    indexer.add("doc2", "that is testing the freqs")
    indexer.add("doc3", "dad is testing the freqs")
    indexer.add("doc4", "mom is testing the freqs")

    results = indexer.search_phrase('freqs')
    

    print('=========Results================')


    print(results)