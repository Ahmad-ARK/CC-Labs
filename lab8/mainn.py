
# 2022-CS-31
import re

class SymbolTable:
    """Manages identifiers, their types, and scopes as per Lab Manual requirements."""
    def __init__(self):
        self.table = {}

    def insert(self, identifier, token_type, scope="global", line=0):
        if identifier not in self.table:
            self.table[identifier] = {
                "type": token_type, 
                "scope": scope, 
                "line": line
            }
            return True
        return False

    def lookup(self, identifier):
        return self.table.get(identifier, None)

    def display(self):
        print("\n--- SYMBOL TABLE ---")
        print(f"{'Identifier':<15} | {'Type':<10} | {'Scope':<10} | {'Line':<5}")
        print("-" * 50)
        for id_name, info in self.table.items():
            print(f"{id_name:<15} | {info['type']:<10} | {info['scope']:<10} | {info['line']:<5}")

class Scanner:
    """Lexical Analyzer for the Decaf subset."""
    def __init__(self, code):
        self.tokens = []
        self.code = code
        self.symbol_table = SymbolTable()
        self.line_num = 1
        self.tokenize()

    def tokenize(self):
        token_specification = [
            ('INT',      r'\bint\b'),
            ('DOUBLE',   r'\bdouble\b'),
            ('BOOL',     r'\bbool\b'),
            ('NUM',      r'\d+(\.\d*)?'), 
            ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('ASSIGN',   r'='),
            ('PLUS',     r'\+'),
            ('MINUS',    r'-'),
            ('SEMI',     r';'),
            ('NEWLINE',  r'\n'),
            ('SKIP',     r'[ \t]+'),
            ('MISMATCH', r'.'),
        ]
        
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        
        for mo in re.finditer(tok_regex, self.code):
            kind = mo.lastgroup
            value = mo.group()
            
            if kind == 'NEWLINE':
                self.line_num += 1
            elif kind == 'SKIP':
                continue
            elif kind == 'ID':
                self.symbol_table.insert(value, "identifier", line=self.line_num)
                self.tokens.append(('ident', value))
            elif kind in ['INT', 'DOUBLE', 'BOOL']:
                self.tokens.append((value, value))
            elif kind == 'NUM':
                self.tokens.append(('num', value))
            elif kind == 'ASSIGN':
                self.tokens.append(('=', value))
            elif kind == 'PLUS':
                self.tokens.append(('+', value))
            elif kind == 'MINUS':
                self.tokens.append(('-', value))
            elif kind == 'SEMI':
                self.tokens.append((';', value))
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Lexical Error at line {self.line_num}: Unexpected character {value}')
        
        self.tokens.append(('$', '$'))

class LL1Parser:
    """Table-driven LL(1) Parser for Ahmad Khalid (2022-CS-31)."""
    def __init__(self, scanner):
        self.tokens = scanner.tokens
        self.symbol_table = scanner.symbol_table
        self.stack = ['$', 'Program'] 
        self.cursor = 0
        
        self.table = {
            'Program': {
                'int': ['Decl', "Program'"], 'double': ['Decl', "Program'"], 
                'bool': ['Decl', "Program'"], 'ident': ['Decl', "Program'"]
            },
            "Program'": {
                'int': ['Decl', "Program'"], 'double': ['Decl', "Program'"], 
                'bool': ['Decl', "Program'"], 'ident': ['Decl', "Program'"],
                '$': ['epsilon']
            },
            'Decl': {
                'int': ['Type', 'ident', ';'], 'double': ['Type', 'ident', ';'], 
                'bool': ['Type', 'ident', ';'], 'ident': ['ident', '=', 'Expr', ';']
            },
            'Type': {
                'int': ['int'], 'double': ['double'], 'bool': ['bool']
            },
            'Expr': {
                'ident': ['Term', "Expr'"], 'num': ['Term', "Expr'"]
            },
            "Expr'": {
                '+': ['+', 'Term', "Expr'"], '-': ['-', 'Term', "Expr'"], 
                ';': ['epsilon']
            },
            'Term': {
                'ident': ['ident'], 'num': ['num']
            }
        }

    def parse(self):
        print(f"\nParser Trace for Ahmad Khalid (2022-CS-31)")
        print(f"{'Stack':<45} | {'Input':<25} | {'Action'}")
        print("-" * 100)

        while len(self.stack) > 0:
            top = self.stack[-1]
            current_tok_type, current_tok_val = self.tokens[self.cursor]
            
            stk_str = " ".join(self.stack)
            inp_str = " ".join([t[1] for t in self.tokens[self.cursor:]])
            if len(inp_str) > 22: inp_str = inp_str[:20] + "..."

            if top in ['ident', 'num', 'int', 'double', 'bool', '=', ';', '+', '-', '$']:
                if top == current_tok_type or top == current_tok_val:
                    print(f"{stk_str:<45} | {inp_str:<25} | Match: {current_tok_val}")
                    self.stack.pop()
                    self.cursor += 1
                else:
                    print(f"\nSYNTAX ERROR: Expected '{top}', found '{current_tok_val}'")
                    return False
            
            elif top in self.table:
                lookup_key = current_tok_type
                if lookup_key in self.table[top]:
                    production = self.table[top][lookup_key]
                    print(f"{stk_str:<45} | {inp_str:<25} | Expand: {top} -> {' '.join(production)}")
                    
                    self.stack.pop()
                    if production != ['epsilon']:
                        for symbol in reversed(production):
                            self.stack.append(symbol)
                else:
                    print(f"\nSYNTAX ERROR: No production for '{top}' on input '{current_tok_val}'")
                    return False
            
            if top == '$' and current_tok_type == '$':
                print("-" * 100)
                print("Final Status: ACCEPTED")
                self.symbol_table.display()
                return True

        return False

def run_test(description, code):
    print(f"\n{'#'*10} TEST: {description} {'#'*10}")
    print(f"Code: {code.strip()}")
    try:
        scanner = Scanner(code)
        parser = LL1Parser(scanner)
        parser.parse()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_test("Valid Declaration", "int x ;")
    run_test("Valid Assignment", "y = 10 + 5 ;")
    run_test("Multiple Declarations", "int a ; b = a - 2 ;")

    run_test("Missing Semicolon", "int x")
    run_test("Invalid Operator", "x = 10 * 5 ;")
    run_test("Leading Equals", "= 5 ;")