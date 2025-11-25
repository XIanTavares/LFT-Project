import ply.lex as lex

# Lista de tokens
tokens = (
    # Identificadores e literais
    'ID',
    'NUMBER',
    'FLOAT',
    'STRING',
    'CHAR',
    
    # Operadores aritméticos
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULO',
    'POWER',
    
    # Operadores de comparação
    'EQ',
    'NE',
    'LT',
    'LE',
    'GT',
    'GE',
    
    # Operadores lógicos
    'AND',
    'OR',
    'NOT',
    
    # Operadores bitwise
    'BITAND',
    'BITOR',
    'BITXOR',
    'BITNOT',
    'LSHIFT',
    'RSHIFT',
    
    # Operadores de atribuição
    'ASSIGN',
    'PLUSASSIGN',
    'MINUSASSIGN',
    'TIMESASSIGN',
    'DIVIDEASSIGN',
    'MODULOASSIGN',
    
    # Delimitadores
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'SEMICOLON',
    'COMMA',
    'DOT',
    'COLON',
    'ARROW',
    'QUESTION',
    'ELLIPSIS',
    'DOUBLECOLON',
    
    # Outros
    'PIPE',
    'AMPERSAND',
    'AT',
    'HASH',
)

# Palavras reservadas
reserved = {
    'const': 'CONST',
    'var': 'VAR',
    'fn': 'FN',
    'pub': 'PUB',
    'extern': 'EXTERN',
    'export': 'EXPORT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'switch': 'SWITCH',
    'return': 'RETURN',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'defer': 'DEFER',
    'errdefer': 'ERRDEFER',
    'try': 'TRY',
    'catch': 'CATCH',
    'struct': 'STRUCT',
    'enum': 'ENUM',
    'union': 'UNION',
    'error': 'ERROR',
    'inline': 'INLINE',
    'noinline': 'NOINLINE',
    'asm': 'ASM',
    'volatile': 'VOLATILE',
    'align': 'ALIGN',
    'comptime': 'COMPTIME',
    'test': 'TEST',
    'packed': 'PACKED',
    'null': 'NULL',
    'undefined': 'UNDEFINED',
    'true': 'TRUE',
    'false': 'FALSE',
    'and': 'KAND',
    'or': 'KOR',
    'orelse': 'ORELSE',
    'anytype': 'ANYTYPE',
    'usingnamespace': 'USINGNAMESPACE',
    'nosuspend': 'NOSUSPEND',
    'suspend': 'SUSPEND',
    'resume': 'RESUME',
    'await': 'AWAIT',
    'async': 'ASYNC',
    'threadlocal': 'THREADLOCAL',
    'allowzero': 'ALLOWZERO',
    'callconv': 'CALLCONV',
    'linksection': 'LINKSECTION',
}

# Adiciona as palavras reservadas aos tokens
tokens = tokens + tuple(reserved.values())

# Regras de tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_POWER = r'\*\*'

t_EQ = r'=='
t_NE = r'!='
t_LE = r'<='
t_GE = r'>='
t_LT = r'<'
t_GT = r'>'

t_BITAND = r'&'
t_BITOR = r'\|'
t_BITXOR = r'\^'
t_BITNOT = r'~'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'

t_ASSIGN = r'='
t_PLUSASSIGN = r'\+='
t_MINUSASSIGN = r'-='
t_TIMESASSIGN = r'\*='
t_DIVIDEASSIGN = r'/='
t_MODULOASSIGN = r'%='

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'\.'
t_COLON = r':'
t_QUESTION = r'\?'
t_ELLIPSIS = r'\.\.\.'
t_DOUBLECOLON = r'::'

t_PIPE = r'\|'
t_AMPERSAND = r'&'
t_AT = r'@'
t_HASH = r'\#'

# Operadores compostos
def t_ARROW(t):
    r'->'
    return t

def t_AND(t):
    r'&&'
    return t

def t_OR(t):
    r'\|\|'
    return t

def t_NOT(t):
    r'!'
    return t

# Identificadores e palavras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Números de ponto flutuante
def t_FLOAT(t):
    r'\d+\.\d+([eE][+-]?\d+)?|\d+[eE][+-]?\d+'
    t.value = float(t.value)
    return t

# Números inteiros (decimal, hex, octal, binário)
def t_NUMBER(t):
    r'0x[0-9a-fA-F]+|0o[0-7]+|0b[01]+|\d+'
    if t.value.startswith('0x'):
        t.value = int(t.value, 16)
    elif t.value.startswith('0o'):
        t.value = int(t.value, 8)
    elif t.value.startswith('0b'):
        t.value = int(t.value, 2)
    else:
        t.value = int(t.value)
    return t

# String literal
def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]  # Remove aspas
    return t

# Character literal
def t_CHAR(t):
    r"'([^'\\]|\\.)'"
    t.value = t.value[1:-1]  # Remove aspas simples
    return t

# Comentários de linha
def t_COMMENT(t):
    r'//.*'
    pass  # Ignora comentários

# Comentários multi-linha (Zig não tem comentários multi-linha tradicionais)

# Novas linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Espaços e tabs
t_ignore = ' \t'

# Tratamento de erros
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Construir o lexer
lexer = lex.lex()

# Função para testar o lexer
def test_lexer(code):
    lexer.input(code)
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append(tok)
    return tokens_list

# Exemplo de uso
if __name__ == '__main__':
    # Código de exemplo em Zig
    test_code = '''
    const std = @import("std");
    
    pub fn main() !void {
        const x: i32 = 42;
        var y: f64 = 3.14;
        
        if (x > 0) {
            std.debug.print("x é positivo\\n", .{});
        } else {
            std.debug.print("x não é positivo\\n", .{});
        }
        
        const z = x + 10;
        return;
    }
    '''
    
    print("Analisando código Zig:")
    print("=" * 60)
    print(test_code)
    print("=" * 60)
    print("\nTokens encontrados:")
    print("-" * 60)
    
    lexer.input(test_code)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"Tipo: {tok.type:20} | Valor: {tok.value:20} | Linha: {tok.lineno}")