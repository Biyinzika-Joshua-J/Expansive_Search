import unittest
from indexer import Indexer

class TestIndexer(unittest.TestCase):
    def setUp(self):
        self.index = Indexer()
        
    def test_should_generate_tokens_from_text(self):
        tokens = self.index._tokenize("this is text")
        
        self.assertEqual(len(tokens), 3)
        
if __name__ == '__main__':
    unittest.main()