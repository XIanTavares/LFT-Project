import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional

class TokenType(Enum):
    # Palavras reservadas
    ADDRSPACE = auto()
    ALIGN = auto()
    ALLOWZERO = auto()
    AND = auto()
    ANYFRAME = auto()
    ANYTYPE = auto()
    ASM = auto()
    ASYNC = auto()
    AWAIT = auto()
    BREAK = auto()
    CALLCONV = auto()
    CATCH = auto()
    COMPTIME = auto()
    CONST = auto()
    CONTINUE = auto()
    DEFER = auto()
    ELSE = auto()
    ENUM = auto()
    ERRDEFER = auto()
    ERROR = auto()
    EXPORT = auto()
    EXTERN = auto()
    FALSE = auto()
    FN = auto()
    FOR = auto()
    IF = auto()
    INLINE = auto()
    LINKSECTION = auto()
    NOALIAS = auto()
    NOINLINE = auto()
    NOSUSPEND = auto()
    NULL = auto()
    OPAQUE = auto()
    OR = auto()
    ORELSE = auto()
    PACKED = auto()
    PUB = auto()
    RESUME = auto()
    RETURN = auto()
    STRUCT = auto()
    SUSPEND = auto()
    SWITCH = auto()
    TEST = auto()
    THREADLOCAL = auto()
    TRUE = auto()
    TRY = auto()
    UNDEFINED = auto()
    UNION = auto()
    UNREACHABLE = auto()
    USINGNAMESPACE = auto()
    VAR = auto()
    VOLATILE = auto()
    WHILE = auto()
    
    # Identificadores e literais
    ID = auto()
    NUMBER = auto()
    FLOAT = auto()
    STRING = auto()
    CHAR = auto()
    
    # Operadores aritméticos
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    PLUSPLUS = auto()
    PLUSPERCENT = auto()
    MINUSPERCENT = auto()
    ASTERISKPERCENT = auto()
    
    # Operadores de comparação
    EQ = auto()
    NE = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    
    # Operadores lógicos
    LOGAND = auto()
    LOGOR = auto()
    NOT = auto()
    
    # Operadores bitwise
    BITAND = auto()
    BITOR = auto()
    BITXOR = auto()
    BITNOT = auto()
    LSHIFT = auto()
    RSHIFT = auto()
    
    # Operadores de atribuição
    ASSIGN = auto()
    PLUSASSIGN = auto()
    MINUSASSIGN = auto()
    ASTERISKEQUAL = auto()
    SLASHEQUAL = auto()
    PERCENTEQUAL = auto()
    AMPERSANDEQUAL = auto()
    CARETEQUAL = auto()
    PIPEEQUAL = auto()
    PLUSPERCENTEQUAL = auto()
    MINUSPERCENTEQUAL = auto()
    ASTERISKPERCENTEQUAL = auto()
    LARROW2EQUAL = auto()
    RARROW2EQUAL = auto()
    
    # Delimitadores
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    ARROW = auto()
    QUESTION = auto()
    ELLIPSIS = auto()
    DOUBLECOLON = auto()
    PIPE = auto()
    AMPERSAND = auto()
    AT = auto()
    HASH = auto()
    
    # Especiais
    EOF = auto()
    ERROR_TOKEN = auto()

@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, line={self.line}, col={self.column})"

class ZigLexer:
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        # Palavras reservadas
        self.keywords = {
            'addrspace': TokenType.ADDRSPACE,
            'align': TokenType.ALIGN,
            'allowzero': TokenType.ALLOWZERO,
            'and': TokenType.AND,
            'anyframe': TokenType.ANYFRAME,
            'anytype': TokenType.ANYTYPE,
            'asm': TokenType.ASM,
            'async': TokenType.ASYNC,
            'await': TokenType.AWAIT,
            'break': TokenType.BREAK,
            'callconv': TokenType.CALLCONV,
            'catch': TokenType.CATCH,
            'comptime': TokenType.COMPTIME,
            'const': TokenType.CONST,
            'continue': TokenType.CONTINUE,
            'defer': TokenType.DEFER,
            'else': TokenType.ELSE,
            'enum': TokenType.ENUM,
            'errdefer': TokenType.ERRDEFER,
            'error': TokenType.ERROR,
            'export': TokenType.EXPORT,
            'extern': TokenType.EXTERN,
            'false': TokenType.FALSE,
            'fn': TokenType.FN,
            'for': TokenType.FOR,
            'if': TokenType.IF,
            'inline': TokenType.INLINE,
            'linksection': TokenType.LINKSECTION,
            'noalias': TokenType.NOALIAS,
            'noinline': TokenType.NOINLINE,
            'nosuspend': TokenType.NOSUSPEND,
            'null': TokenType.NULL,
            'opaque': TokenType.OPAQUE,
            'or': TokenType.OR,
            'orelse': TokenType.ORELSE,
            'packed': TokenType.PACKED,
            'pub': TokenType.PUB,
            'resume': TokenType.RESUME,
            'return': TokenType.RETURN,
            'struct': TokenType.STRUCT,
            'suspend': TokenType.SUSPEND,
            'switch': TokenType.SWITCH,
            'test': TokenType.TEST,
            'threadlocal': TokenType.THREADLOCAL,
            'true': TokenType.TRUE,
            'try': TokenType.TRY,
            'undefined': TokenType.UNDEFINED,
            'union': TokenType.UNION,
            'unreachable': TokenType.UNREACHABLE,
            'usingnamespace': TokenType.USINGNAMESPACE,
            'var': TokenType.VAR,
            'volatile': TokenType.VOLATILE,
            'while': TokenType.WHILE,
        }
    
    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.code):
            return None
        return self.code[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        pos = self.pos + offset
        if pos >= len(self.code):
            return None
        return self.code[pos]
    
    def advance(self):
        if self.pos < len(self.code):
            if self.code[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\n\r':
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '/' and self.peek_char() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
            if self.current_char() == '\n':
                self.advance()
    
    def read_number(self) -> Token:
        start_line = self.line
        start_col = self.column
        num_str = ''
        
        # Hexadecimal
        if self.current_char() == '0' and self.peek_char() == 'x':
            num_str += self.current_char()
            self.advance()
            num_str += self.current_char()
            self.advance()
            while self.current_char() and self.current_char() in '0123456789abcdefABCDEF_':
                if self.current_char() != '_':
                    num_str += self.current_char()
                self.advance()
            return Token(TokenType.NUMBER, int(num_str, 16), start_line, start_col)
        
        # Octal
        if self.current_char() == '0' and self.peek_char() == 'o':
            num_str += self.current_char()
            self.advance()
            num_str += self.current_char()
            self.advance()
            while self.current_char() and self.current_char() in '01234567_':
                if self.current_char() != '_':
                    num_str += self.current_char()
                self.advance()
            return Token(TokenType.NUMBER, int(num_str, 8), start_line, start_col)
        
        # Binário
        if self.current_char() == '0' and self.peek_char() == 'b':
            num_str += self.current_char()
            self.advance()
            num_str += self.current_char()
            self.advance()
            while self.current_char() and self.current_char() in '01_':
                if self.current_char() != '_':
                    num_str += self.current_char()
                self.advance()
            return Token(TokenType.NUMBER, int(num_str, 2), start_line, start_col)
        
        # Decimal ou float
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '_'):
            if self.current_char() != '_':
                num_str += self.current_char()
            self.advance()
        
        # Ponto decimal
        if self.current_char() == '.' and self.peek_char() and self.peek_char().isdigit():
            num_str += self.current_char()
            self.advance()
            while self.current_char() and (self.current_char().isdigit() or self.current_char() == '_'):
                if self.current_char() != '_':
                    num_str += self.current_char()
                self.advance()
            
            # Expoente
            if self.current_char() in 'eE':
                num_str += self.current_char()
                self.advance()
                if self.current_char() in '+-':
                    num_str += self.current_char()
                    self.advance()
                while self.current_char() and (self.current_char().isdigit() or self.current_char() == '_'):
                    if self.current_char() != '_':
                        num_str += self.current_char()
                    self.advance()
            
            return Token(TokenType.FLOAT, float(num_str), start_line, start_col)
        
        return Token(TokenType.NUMBER, int(num_str), start_line, start_col)
    
    def read_string(self) -> Token:
        start_line = self.line
        start_col = self.column
        string_val = ''
        
        self.advance()  # pula a primeira "
        
        while self.current_char() and self.current_char() != '"':
            if self.current_char() == '\\':
                self.advance()
                if self.current_char():
                    escapes = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', '0': '\0'}
                    string_val += escapes.get(self.current_char(), self.current_char())
                    self.advance()
            else:
                string_val += self.current_char()
                self.advance()
        
        if self.current_char() == '"':
            self.advance()
        return Token(TokenType.STRING, string_val, start_line, start_col)
    
    def read_char(self) -> Token:
        start_line = self.line
        start_col = self.column
        
        self.advance()  # pula a primeira '
        
        char_val = ''
        if self.current_char() == '\\':
            self.advance()
            escapes = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', "'": "'", '0': '\0'}
            char_val = escapes.get(self.current_char(), self.current_char())
            self.advance()
        else:
            char_val = self.current_char()
            self.advance()
        
        if self.current_char() == "'":
            self.advance()
        return Token(TokenType.CHAR, char_val, start_line, start_col)
    
    def read_identifier(self) -> Token:
        start_line = self.line
        start_col = self.column
        id_str = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            id_str += self.current_char()
            self.advance()
        
        token_type = self.keywords.get(id_str, TokenType.ID)
        return Token(token_type, id_str, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.code):
            self.skip_whitespace()
            
            if self.pos >= len(self.code):
                break
            
            # Comentários
            if self.current_char() == '/' and self.peek_char() == '/':
                self.skip_comment()
                continue
            
            char = self.current_char()
            start_line = self.line
            start_col = self.column
            
            # Números
            if char.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Strings
            if char == '"':
                self.tokens.append(self.read_string())
                continue
            
            # Caracteres
            if char == "'":
                self.tokens.append(self.read_char())
                continue
            
            # Identificadores e palavras reservadas
            if char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Operadores de três caracteres (verificar primeiro)
            if self.pos + 2 < len(self.code):
                three_char = char + (self.peek_char() or '') + (self.peek_char(2) or '')
                
                three_char_tokens = {
                    '...': TokenType.ELLIPSIS,
                    '*%=': TokenType.ASTERISKPERCENTEQUAL,
                    '+%=': TokenType.PLUSPERCENTEQUAL,
                    '-%=': TokenType.MINUSPERCENTEQUAL,
                    '<<=': TokenType.LARROW2EQUAL,
                    '>>=': TokenType.RARROW2EQUAL,
                }
                
                if three_char in three_char_tokens:
                    self.tokens.append(Token(three_char_tokens[three_char], three_char, start_line, start_col))
                    self.advance()
                    self.advance()
                    self.advance()
                    continue
            
            # Operadores de dois caracteres
            two_char = char + (self.peek_char() or '')
            
            two_char_tokens = {
                '==': TokenType.EQ,
                '!=': TokenType.NE,
                '<=': TokenType.LE,
                '>=': TokenType.GE,
                '&&': TokenType.LOGAND,
                '||': TokenType.LOGOR,
                '<<': TokenType.LSHIFT,
                '>>': TokenType.RSHIFT,
                '->': TokenType.ARROW,
                '::': TokenType.DOUBLECOLON,
                '+=': TokenType.PLUSASSIGN,
                '-=': TokenType.MINUSASSIGN,
                '*=': TokenType.ASTERISKEQUAL,
                '/=': TokenType.SLASHEQUAL,
                '%=': TokenType.PERCENTEQUAL,
                '**': TokenType.POWER,
                '++': TokenType.PLUSPLUS,
                '&=': TokenType.AMPERSANDEQUAL,
                '^=': TokenType.CARETEQUAL,
                '|=': TokenType.PIPEEQUAL,
                '*%': TokenType.ASTERISKPERCENT,
                '+%': TokenType.PLUSPERCENT,
                '-%': TokenType.MINUSPERCENT,
            }
            
            if two_char in two_char_tokens:
                self.tokens.append(Token(two_char_tokens[two_char], two_char, start_line, start_col))
                self.advance()
                self.advance()
                continue
            
            # Operadores de um caractere
            one_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.TIMES,
                '/': TokenType.DIVIDE,
                '%': TokenType.MODULO,
                '<': TokenType.LT,
                '>': TokenType.GT,
                '!': TokenType.NOT,
                '&': TokenType.BITAND,
                '|': TokenType.BITOR,
                '^': TokenType.BITXOR,
                '~': TokenType.BITNOT,
                '=': TokenType.ASSIGN,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ';': TokenType.SEMICOLON,
                ',': TokenType.COMMA,
                '.': TokenType.DOT,
                ':': TokenType.COLON,
                '?': TokenType.QUESTION,
                '@': TokenType.AT,
                '#': TokenType.HASH,
            }
            
            if char in one_char_tokens:
                self.tokens.append(Token(one_char_tokens[char], char, start_line, start_col))
                self.advance()
                continue
            
            # Caractere não reconhecido
            print(f"Erro: caractere ilegal '{char}' na linha {start_line}, coluna {start_col}")
            self.advance()
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

# Exemplo de uso
if __name__ == '__main__':
    test_code = '''
    const std = @import("std");
    
    pub fn main() !void {
        const x: i32 = 42;
        var y: f64 = 3.14;
        
        // Operadores wrapping
        const a = x +% 10;
        const b = x -% 5;
        const c = x *% 2;
        
        if (x > 0) {
            std.debug.print("x é positivo\\n", .{});
        } else {
            std.debug.print("x não é positivo\\n", .{});
        }
        
        const z = x + 10;
        const hex = 0xFF;
        const bin = 0b1010;
        
        return;
    }
    '''
    
    print("Analisando código Zig:")
    print("=" * 70)
    print(test_code)
    print("=" * 70)
    print("\nTokens encontrados:")
    print("-" * 70)
    
    lexer = ZigLexer(test_code)
    tokens = lexer.tokenize()
    
    for token in tokens:
        if token.type != TokenType.EOF:
            print(f"{token.type.name:20} | {str(token.value):25} | L{token.line}:C{token.column}")