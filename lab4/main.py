import threading
import queue
import re

# --- Configuration ---
BUFFER_SIZE = 128
KEYWORDS = {
    'void', 'int', 'double', 'bool', 'string', 'class', 'interface', 
    'null', 'this', 'extends', 'implements', 'for', 'while', 'if', 
    'else', 'return', 'break', 'New', 'NewArray', 'Print', 
    'ReadInteger', 'ReadLine', 'true', 'false'
}

# Shared queue for thread synchronization
buffer_queue = queue.Queue()
stop_signal = threading.Event()

def producer(file_path):
    """Reads file into two buffers and sends them to the consumer."""
    try:
        with open(file_path, 'r') as f:
            while True:
                chunk = f.read(BUFFER_SIZE)
                if not chunk:
                    break
                buffer_queue.put(chunk)
        buffer_queue.put(None)  # End of file signal
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        stop_signal.set()

def consumer():
    """Processes buffers and identifies Decaf tokens."""
    tokens = []
    while not stop_signal.is_set():
        buffer = buffer_queue.get()
        if buffer is None: break
        
        # Combined Regex for Decaf Lexical Specifications
        token_specification = [
            ('COMMENT',   r'//.*|/\*[\s\S]*?\*/'),           # Single/Multi-line comments [cite: 206, 207]
            ('HEX',       r'0[xX][0-9a-fA-F]+'),             # Hexadecimal constants [cite: 184]
            ('DOUBLE',    r'\d+\.\d*([eE][+-]?\d+)?'),       # Double constants [cite: 187, 189]
            ('INT',       r'\d+'),                           # Decimal constants [cite: 183]
            ('STRING',    r'"[^"\n]*"'),                     # String constants [cite: 191, 192]
            ('ID',        r'[a-zA-Z][a-zA-Z0-9_]{0,30}'),    # Identifiers (max 31 chars) 
            ('OP',        r'<=|>=|==|!=|&&|\|\||[+\-*/%<>=!;,.\(\)\[\]\{\}]'), # Operators [cite: 195, 201]
            ('NEWLINE',   r'\n'),                            # Line tracking
            ('SKIP',      r'[ \t]+'),                        # Skip whitespace [cite: 178]
            ('MISMATCH',  r'.'),                             # Any other character
        ]
        
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        
        for mo in re.finditer(tok_regex, buffer):
            kind = mo.lastgroup
            value = mo.group()
            
            if kind == 'ID' and value in KEYWORDS:
                kind = 'KEYWORD'
            elif kind == 'SKIP' or kind == 'NEWLINE' or kind == 'COMMENT':
                continue
            elif kind == 'MISMATCH':
                print(f"Lexical Error: Unexpected character '{value}'")
                continue
                
            tokens.append(f"<{kind}, {value}>")
    
    # Write output to file as required 
    with open('tokens.out', 'w') as out_f:
        out_f.write('\n'.join(tokens))
    print("✅ Lexical Analysis Complete. Tokens saved to tokens.out")

if __name__ == "__main__":
    # Create a dummy input file for testing
    with open('input.decaf', 'w') as f:
        f.write('void main() {\n  int x = 0x1A;\n  Print("Hello Decaf");\n}')

    prod_thread = threading.Thread(target=producer, args=('input.decaf',))
    cons_thread = threading.Thread(target=consumer)

    prod_thread.start()
    cons_thread.start()
    prod_thread.join()
    cons_thread.join()