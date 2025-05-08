import re
from collections import defaultdict
from itertools import product

from fuzzy import leven

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
        matches = self._fuzzy_match_term(term)
        
        if len(matches) > 0:
            term = matches[0]
        
        return self.index.get(term, None)
    
    def fetchOne(self, doc_id):
        return self.documents[doc_id]["content"]
    
    def search_phrase(self, phrase):
        tokens = self._tokenize(phrase)
        
        if not tokens:
            return []
        
        results = []
        seen = set()
        
        entry = self.index[tokens[0]]
        
        if not entry:
            return []
        
        for idx, doc_id in enumerate(entry["doc_ids"]):
            for position in entry["positions"][idx]:
                if self._match_phrase_at(doc_id, position, tokens):
                    
                    key = (doc_id, position, tuple(tokens))
                    if key in seen:
                        continue
                    seen.add(key)
                    
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
    
    def _fuzzy_match_term(self, word, threshold=50):
        matches = []
        
        for candidate in self.index.keys():
            score = leven.ratio(word, candidate)
            
            if score >= threshold:
                matches.append((candidate, score))
        
        result = [word for word, _ in sorted(matches, key=lambda x: -x[1])]       
        return result
    
    def fuzzy_search_phrase(self, phrase, threshold=50):
        tokens = self._tokenize(phrase)
        
        if not tokens:
            return []
        
        fuzzy_options = []
        for token in tokens:
            matches = self._fuzzy_match_term(token, threshold)
            if not matches:
                return []  
            fuzzy_options.append(matches)
        
        phrase_variants = product(*fuzzy_options)
        # print(phrase_variants)
        
        results = []
        for variant in phrase_variants:
            print(variant)
            phrase_variant = " ".join(variant)
            search_results = self.search_phrase(phrase_variant)
            
            if search_results:
                results.extend(search_results)
           
            
        return results
    
    
    def boolean_search(self, query):
        tokens = self._tokenize(query)
        result_set = set()
        current_operation = None
        negate_next = False
        
        all_docs = set(self.documents.keys())
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token == 'and':
                current_operation = 'AND'
            elif token == 'or':
                current_operation = 'OR'
            elif token == 'not':
                negate_next = True
            else:
                term_docs = set(self.get(token)["doc_ids"]) if self.get(token) else set()
                
                if negate_next:
                    term_docs = all_docs - term_docs
                    negate_next = False
                    
                if not result_set:
                    result_set = term_docs
                elif current_operation == 'AND':
                    result_set &= term_docs
                elif current_operation == 'OR':
                    result_set |= term_docs
                else:
                    result_set &= term_docs
                    
                current_operation = None
            
            i += 1
        
        return [self.documents[doc_id]["content"] for doc_id in result_set]
            
            
    
    
if __name__ == '__main__':
    indexer = Indexer()

    indexer.add("doc1", "this is testing the freqs because freqs matter")
    indexer.add("doc2", "that is testing the freqs")
    indexer.add("doc3", "dad is testing the freqs today")
    indexer.add("doc4", "mom is testing the freqs today")

    results = indexer.boolean_search('freq NOT matter NOT mom NOT dad')
    

    print('=========Results================')


    print(results)