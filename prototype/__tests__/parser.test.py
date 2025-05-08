import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unittest
from parser import Tokenizer

class TokenizerTest(unittest.TestCase):
    def setUp(self):
        self.tokeninzer = Tokenizer('')
        
    def test_should_turn_expressions_into_tokens(self):
        expected_tokens = ['that', 'AND', '"mom freqs"', 'OR', '(', 'NOT', 'dad', ')']
        self.tokeninzer.set_expression('that AND "mom freqs" OR (NOT dad)')
                
        i = 0
        while i < len(expected_tokens):
            expected_token = expected_tokens[i]
            
            token = self.tokeninzer.get_token()
            self.assertIsNotNone(token)
            
            self.assertEqual(token.literal, expected_token)
            
            i += 1
            
    def test_should_throw_unexpected_token_error(self):
        self.tokeninzer.set_expression('that AND + "mom freqs" OR (NOT dad)')
        
        with self.assertRaises(TypeError) as context:
            while True:
                token = self.tokeninzer.get_token()
                
                if token.type == 'EOF':
                    break

        self.assertIn('Unexpected token', str(context.exception))
    
    
class ParserTest(unittest.TestCase):
    def setUp(self):
        return super().setUp()

if __name__ == '__main__':
    unittest.main()