
// 2022-CS-31
const fs = require('fs');

const keywords = new Set([
    "void", "int", "double", "bool", "string", "class", "interface", 
    "null", "this", "extends", "implements", "for", "while", "if", 
    "else", "return", "break", "New", "NewArray", "Print", "ReadInteger", "ReadLine"
]);

class LexicalAnalyzer {
    constructor(filePath) {
        this.source = fs.readFileSync(filePath, 'utf8');
        this.pos = 0;
        this.line = 1;
    }

    peek() {
        return this.pos < this.source.length ? this.source[this.pos] : null;
    }

    advance() {
        const char = this.peek();
        this.pos++;
        return char;
    }

    skipWhitespaceAndComments() {
        while (this.pos < this.source.length) {
            const char = this.peek();
            if (/\s/.test(char)) {
                if (char === '\n') this.line++;
                this.advance();
            } else if (char === '/') {
                this.advance();
                if (this.peek() === '/') {
                    while (this.peek() !== '\n' && this.peek() !== null) this.advance();
                } else if (this.peek() === '*') {
                    this.advance();
                    while (this.pos < this.source.length) {
                        if (this.advance() === '*' && this.peek() === '/') {
                            this.advance();
                            break;
                        }
                    }
                } else {
                    this.pos--; 
                    break;
                }
            } else {
                break;
            }
        }
    }

    getNextToken() {
        this.skipWhitespaceAndComments();
        const char = this.peek();

        if (char === null) return { type: 'EOF', lexeme: '' };

        if (/[a-zA-Z]/.test(char)) {
            let ident = "";
            while (/[a-zA-Z0-9_]/.test(this.peek())) {
                ident += this.advance();
            }
            if (ident === "true" || ident === "false") return { type: 'BoolConstant', lexeme: ident };
            if (keywords.has(ident)) return { type: 'Keyword', lexeme: ident };
            return { type: 'Identifier', lexeme: ident.substring(0, 31) };
        }

        if (/[0-9]/.test(char)) {
            let num = "";
            if (char === '0') {
                num += this.advance();
                if (this.peek()?.toLowerCase() === 'x') {
                    num += this.advance();
                    while (/[0-9a-fA-F]/.test(this.peek())) num += this.advance();
                    return { type: 'IntConstant', lexeme: num };
                }
            }
            while (/[0-9]/.test(this.peek())) num += this.advance();
            if (this.peek() === '.') {
                num += this.advance();
                while (/[0-9]/.test(this.peek())) num += this.advance();
                if (this.peek()?.toLowerCase() === 'e') {
                    num += this.advance();
                    if (this.peek() === '+' || this.peek() === '-') num += this.advance();
                    while (/[0-9]/.test(this.peek())) num += this.advance();
                }
                return { type: 'DoubleConstant', lexeme: num };
            }
            return { type: 'IntConstant', lexeme: num };
        }

        if (char === '"') {
            this.advance();
            let str = "";
            while (this.peek() !== '"' && this.peek() !== '\n' && this.peek() !== null) {
                str += this.advance();
            }
            if (this.peek() === '"') {
                this.advance();
                return { type: 'StringConstant', lexeme: `"${str}"` };
            }
            return { type: 'Unknown', lexeme: str };
        }

        let op = this.advance();
        let combined = op + this.peek();
        const multiOps = ["<=", ">=", "==", "!=", "&&", "||"];
        if (multiOps.includes(combined)) {
            this.advance();
            return { type: 'Operator', lexeme: combined };
        }
        return { type: 'Operator', lexeme: op };
    }
}

const lexer = new LexicalAnalyzer('input.decaf');
let output = "";
let token;

while ((token = lexer.getNextToken()).type !== 'EOF') {
    output += `Line ${lexer.line}: [${token.type}] ${token.lexeme}\n`;
}

fs.writeFileSync('output.txt', output);