import unittest
from indexer import Indexer

class TestIndexer(unittest.TestCase):
    def setUp(self):
        self.index = Indexer()
        self.index.add("doc1", "this is testing the freqs because freqs matter")
        self.index.add("doc2", "that is testing the freqs")
        self.index.add("doc3", "dad is testing the freqs")
        self.index.add("doc4", "mom is testing the freqs")
        
    def test_should_generate_tokens_from_text(self):
        tokens = self.index._tokenize("this is, text;")
        
        self.assertEqual(len(tokens), 3)
        
    def test_should_delete_document(self):
        self.assertIn("doc1", self.index.documents)
        
        self.index.delete('doc1')
        self.index.delete('doc2')
        self.index.delete('doc3')
        self.index.delete('doc4')
        
        self.assertEqual(len(self.index.documents.keys()), 0)
        self.assertEqual(len(self.index.index.keys()), 0)
        
    def test_should_update_document(self):
        # should do nothing if doc doesn't exist
        updated = self.index.update("doc10", "new content")
        self.assertFalse(updated) # doc doesn't exist
        
        new_content = "this is the updated version of doc1"
        updated = self.index.update("doc1", new_content)
        self.assertTrue(updated)
        
        self.assertEqual(self.index.documents["doc1"]["content"], new_content)
        
    def test_should_search_phrases(self):
        search_phrase = "the freqs because"
        results = self.index.search_phrase(search_phrase)
        self.assertTrue(len(results) > 0)
        
        first_result_content = results[0]["content"]
        self.assertIn(search_phrase, first_result_content)
        
    def test_should_support_searching_fuzzy_phrases(self):
        search_phrase = "teh freq cause"
        results = self.index.fuzzy_search_phrase(search_phrase)
        self.assertTrue(len(results) > 0)
        
        corrected_phrase = "the freqs because"
        first_result_content = results[0]["content"]
        self.assertIn(corrected_phrase, first_result_content)
        
    
        
if __name__ == '__main__':
    unittest.main()