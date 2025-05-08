import re

token_patterns = [
    # Whitespace
     [r'^\s+', 'WHITESPACE'],
     
    # Operators
    [ r'^AND\b', 'OPERATOR'],
    [ r'^OR\b', 'OPERATOR'],
    [ r'^NOT\b', 'OPERATOR'],
    
    # Parentheses
    [r'^\(', 'LPAREN'],
    [r'^\)', 'RPAREN'],
    
    # Phrase
    [r'^"[^"]+"', 'PHRASE'],
    
    # Terms
    [r'^\w+\b', 'TERM'],
    
    
]

class Token:
    def __init__(self, type, value):
        self.type = type
        self.literal = value

class Tokenizer:
    def __init__(self, expression):
        self.expression = expression
        self.length = len(expression)
        self.eof = False
        self._cursor = 0
        
    def set_expression(self, expression):
        self.expression = expression
        self.length = len(expression)
    
    def get_token(self):
        while self._cursor < self.length:
            expression = self.expression[self._cursor:]
            
            for pattern, token_type in token_patterns:
                match = re.match(pattern, expression)
                if match:
                    value = match.group()
                    
                    self._cursor += len(value)
                    
                    if token_type == 'WHITESPACE':
                        return self.get_token()  

                    token = Token(token_type, value)
                    return token
            
            raise TypeError(f'Unexpected token at column {self._cursor}: {self.expression[self._cursor]}')

        self.eof = True
        return Token('EOF', None)
            
    
# PARSER - RD    

class Parser:
    def __init__(self):
        self._cursor = 0
        self.tokens = []
    
    def parse(self, expression):
        tokenizer = Tokenizer(expression)
        while not tokenizer.eof:
            token = tokenizer.get_token()
            if token:
                self.tokens.append(token)
        
        return self.expression()
    
    def get_current_token(self):
        return self.tokens[self.cursor] if self.cursor < len(self.tokens) else None

    def _eat(self, expected_type=None):
        token = self.get_current_token()
        if expected_type and token.type != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {token.type}")
        self.cursor += 1
        return token
    

    def expression(self):
        return {
            "type": "Expression",
            "program": self.or_expression()
        }
    
    def or_expression(self):
        left = self.and_expression()
        return True
        
        
    def and_expression(self):
        pass
    
    def not_expression(self):
        pass
    
    def atom(self):
        return
    
    
    
"""parser = Parser()
parser.parse('that AND "mom freqs" OR (NOT dad)')

tokenizer = Tokenizer('that AND "mom freqs" OR (NOT dad)')
print(tokenizer.get_token().literal)
print(tokenizer.get_token().literal)
print(tokenizer.get_token().literal)
print(tokenizer.get_token().literal)
print(tokenizer.get_token().literal)
print(tokenizer.get_token().literal)
print(tokenizer.get_token().literal)
print(tokenizer.get_token().literal)
print(tokenizer.get_token().literal) """
    
"""
    Grammar:
    
    expr        → or_expr
    or_expr     → and_expr ( "OR" and_expr )*
    and_expr    → not_expr ( "AND" not_expr )*
    not_expr    → "NOT" not_expr | atom
    atom        → PHRASE | TERM | "(" expr ")"
"""