import logging
import ply.yacc as yacc
from lex import tokens, lexer

arquivos_zig = []
isFine = True
QUIET_PLY = True

# Precedência de operadores
precedence = (
    ('left', 'RANGE', 'RANGE_INCLUSIVE'),
    ('left', 'BITWISE_OR'),
    ('left', 'BITWISE_XOR'),
    ('left', 'BITWISE_AND'),
    ('left', 'EQUALS_THEN', 'NOT_EQUALS'),
    ('left', 'LESS_THEN', 'LESS_EQUALS', 'GREATER_THEN', 'GREATER_EQUALS'),
    ('left', 'BITWISE_SHIFT_LEFT', 'BITWISE_SHIFT_RIGHT'),
    ('left', 'PLUS', 'MINUS', 'PLUS_PERCENT', 'MINUS_PERCENT', 'PLUS_PIPE', 'MINUS_PIPE', 'PLUS_PLUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULUS', 'TIMES_PERCENT', 'TIMES_PIPE'),
    ('right', 'NOT', 'BITWISE_COMPLEMENT', 'UMINUS', 'UPLUS'),
)

# Programa

def p_program(p):
    'program : items'
    p[0] = ('program', p[1])


def p_items(p):
    '''items : items item
             | item'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_item(p):
    '''item : function
            | struct_decl
            | enum_decl
            | const_decl SEMICOLON
            | var_decl SEMICOLON
            | import_decl
            | KEYWORD_PUB const_decl SEMICOLON
            | KEYWORD_PUB var_decl SEMICOLON'''
    p[0] = p[1]

# Declarações

def p_const_decl(p):
    'const_decl : KEYWORD_CONST IDENTIFIER type_annot_opt ASSIGN expression'
    p[0] = ('const_decl', p[2], p[3], p[5])


def p_var_decl(p):
    'var_decl : KEYWORD_VAR IDENTIFIER type_annot_opt ASSIGN expression'
    p[0] = ('var_decl', p[2], p[3], p[5])


def p_import_decl(p):
    'import_decl : KEYWORD_CONST IDENTIFIER ASSIGN AT IDENTIFIER LPAREN args_opt RPAREN SEMICOLON'
    p[0] = ('import', p[2], ('builtin', p[5], p[7]))


def p_type_annot_opt(p):
    '''type_annot_opt : COLON type_spec
                      | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None


def p_type_spec(p):
    '''type_spec : data_type
                 | IDENTIFIER'''
    p[0] = p[1]


def p_data_type(p):
    '''data_type : TYPE_I8
                 | TYPE_I16
                 | TYPE_I32
                 | TYPE_I64
                 | TYPE_I128
                 | TYPE_ISIZE
                 | TYPE_U8
                 | TYPE_U16
                 | TYPE_U32
                 | TYPE_U64
                 | TYPE_U128
                 | TYPE_USIZE
                 | TYPE_F16
                 | TYPE_F32
                 | TYPE_F64
                 | TYPE_F80
                 | TYPE_F128
                 | TYPE_BOOL
                 | TYPE_VOID
                 | TYPE_NORETURN
                 | TYPE_TYPE
                 | TYPE_ANYERROR
                 | TYPE_COMPTIME_INT
                 | TYPE_COMPTIME_FLOAT
                 | TYPE_C_SHORT
                 | TYPE_C_USHORT
                 | TYPE_C_INT
                 | TYPE_C_UINT
                 | TYPE_C_LONG
                 | TYPE_C_ULONG
                 | TYPE_C_LONGLONG
                 | TYPE_C_ULONGLONG
                 | TYPE_C_LONGDOUBLE'''
    p[0] = p[1]

# Funções

def p_function(p):
    'function : visibility_opt KEYWORD_FN IDENTIFIER LPAREN params_opt RPAREN return_type_opt block'
    p[0] = ('function', p[3], p[5], p[7], p[8])


def p_visibility_opt(p):
    '''visibility_opt : KEYWORD_PUB
                      | empty'''
    p[0] = p[1]


def p_return_type_opt(p):
    '''return_type_opt : type_spec
                       | NOT type_spec
                       | empty'''
    if len(p) == 3:
        p[0] = ('error_union', p[2])
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = None


def p_params_opt(p):
    '''params_opt : params
                  | empty'''
    p[0] = p[1]


def p_params(p):
    '''params : params COMMA param
              | param'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_param(p):
    'param : IDENTIFIER COLON type_spec'
    p[0] = ('param', p[1], p[3])

# Struct e Enum

def p_struct_decl(p):
    'struct_decl : KEYWORD_CONST IDENTIFIER ASSIGN KEYWORD_STRUCT LBRACE fields_opt RBRACE SEMICOLON'
    p[0] = ('struct_decl', p[2], p[6])


def p_enum_decl(p):
    'enum_decl : KEYWORD_CONST IDENTIFIER ASSIGN KEYWORD_ENUM LBRACE enum_fields_opt RBRACE SEMICOLON'
    p[0] = ('enum_decl', p[2], p[6])


def p_fields_opt(p):
    '''fields_opt : fields
                  | empty'''
    p[0] = p[1]


def p_fields(p):
    '''fields : fields field
              | field'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_field(p):
    'field : IDENTIFIER COLON type_spec COMMA'
    p[0] = ('field', p[1], p[3])


def p_enum_fields_opt(p):
    '''enum_fields_opt : enum_fields
                       | empty'''
    p[0] = p[1]


def p_enum_fields(p):
    '''enum_fields : enum_fields enum_field
                   | enum_field'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_enum_field(p):
    'enum_field : IDENTIFIER COMMA'
    p[0] = ('enum_field', p[1])

# Blocos e comandos

def p_block(p):
    'block : LBRACE stmts_opt RBRACE'
    p[0] = ('block', p[2])


def p_stmts_opt(p):
    '''stmts_opt : stmts
                 | empty'''
    p[0] = p[1]


def p_stmts(p):
    '''stmts : stmts stmt
             | stmt'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_stmt(p):
    '''stmt : expr_stmt SEMICOLON
            | return_stmt SEMICOLON
            | var_decl SEMICOLON
            | const_decl SEMICOLON
            | if_stmt
            | while_stmt
            | block'''
    p[0] = p[1]


def p_expr_stmt(p):
    'expr_stmt : expression'
    p[0] = ('expr_stmt', p[1])


def p_return_stmt(p):
    '''return_stmt : KEYWORD_RETURN expression
                   | KEYWORD_RETURN'''
    if len(p) == 3:
        p[0] = ('return', p[2])
    else:
        p[0] = ('return', None)


def p_if_stmt(p):
    'if_stmt : KEYWORD_IF LPAREN expression RPAREN block else_opt'
    p[0] = ('if', p[3], p[5], p[6])


def p_else_opt(p):
    '''else_opt : KEYWORD_ELSE block
                | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None


def p_while_stmt(p):
    'while_stmt : KEYWORD_WHILE LPAREN expression RPAREN block'
    p[0] = ('while', p[3], p[5])

# Expressões

def p_expression_assign(p):
    'expression : IDENTIFIER assign_op expression'
    p[0] = ('assign', p[1], p[2], p[3])


def p_assign_op(p):
    '''assign_op : ASSIGN
                 | PLUS_ASSIGN
                 | MINUS_ASSIGN
                 | TIMES_ASSIGN
                 | DIVIDE_ASSIGN
                 | MODULUS_ASSIGN
                 | SHIFT_LEFT_ASSIGN
                 | SHIFT_RIGHT_ASSIGN
                 | BITWISE_AND_ASSIGN
                 | BITWISE_OR_ASSIGN
                 | BITWISE_XOR_ASSIGN
                 | PLUS_PERCENT_ASSIGN
                 | MINUS_PERCENT_ASSIGN
                 | TIMES_PERCENT_ASSIGN
                 | PLUS_PIPE_ASSIGN
                 | MINUS_PIPE_ASSIGN
                 | TIMES_PIPE_ASSIGN'''
    p[0] = p[1]


def p_expression_binary(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULUS expression
                  | expression PLUS_PERCENT expression
                  | expression MINUS_PERCENT expression
                  | expression TIMES_PERCENT expression
                  | expression PLUS_PIPE expression
                  | expression MINUS_PIPE expression
                  | expression TIMES_PIPE expression
                  | expression PLUS_PLUS expression
                  | expression BITWISE_AND expression
                  | expression BITWISE_OR expression
                  | expression BITWISE_XOR expression
                  | expression BITWISE_SHIFT_LEFT expression
                  | expression BITWISE_SHIFT_RIGHT expression
                  | expression EQUALS_THEN expression
                  | expression NOT_EQUALS expression
                  | expression LESS_THEN expression
                  | expression LESS_EQUALS expression
                  | expression GREATER_THEN expression
                  | expression GREATER_EQUALS expression
                  | expression RANGE expression
                  | expression RANGE_INCLUSIVE expression'''
    p[0] = ('binop', p[2], p[1], p[3])


def p_expression_unary(p):
    '''expression : NOT expression
                  | MINUS expression %prec UMINUS
                  | PLUS expression %prec UPLUS
                  | BITWISE_COMPLEMENT expression'''
    p[0] = ('unary', p[1], p[2])


def p_expression_postfix(p):
    'expression : postfix'
    p[0] = p[1]




def p_postfix(p):
    '''postfix : primary
               | postfix DOT IDENTIFIER
               | postfix LPAREN args_opt RPAREN
               | postfix LBRACKET expression RBRACKET
               | postfix OPTIONAL_UNWRAP
               | postfix DEREF'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = ('postfix', p[2], p[1])
    elif len(p) == 4:
        p[0] = ('access', p[1], p[3])
    elif len(p) == 5:
        p[0] = ('call', p[1], p[3])
    else:
        p[0] = ('index', p[1], p[3])


def p_args_opt(p):
    '''args_opt : args
                | empty'''
    p[0] = p[1]


def p_args(p):
    '''args : args COMMA expression
            | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_primary(p):
    '''primary : NUMBER
               | FLOAT_NUMBER
               | HEXADECIMAL_NUMBER
               | BINARY_NUMBER
               | OCTAL_NUMBER
               | STRING
               | C_STRING
               | CHARACTER
               | IDENTIFIER
               | IDENTIFIER_ESCAPED
               | KEYWORD_TRUE
               | KEYWORD_FALSE
               | KEYWORD_NULL
               | KEYWORD_UNDEFINED
               | AT IDENTIFIER LPAREN args_opt RPAREN
               | DOT LBRACE init_list_opt RBRACE
               | LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = ('literal', p[1])
    elif len(p) == 5:
        p[0] = ('init_struct', p[3])
    elif len(p) == 6:
        p[0] = ('builtin', p[2], p[4])
    else:
        p[0] = p[2]


def p_init_list_opt(p):
    '''init_list_opt : init_list
                     | empty'''
    p[0] = p[1]


def p_init_list(p):
    '''init_list : init_list COMMA expression
                 | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_empty(p):
    'empty :'
    p[0] = None


def p_error(p):
    global isFine
    if p:
        print(f"Erro sintático próximo a '{p.value}' na linha {p.lineno}")
    else:
        print("Erro sintático no fim do arquivo")
    isFine = False

def build_parser():
    if QUIET_PLY:
        return yacc.yacc(start='program', errorlog=yacc.NullLogger())
    return yacc.yacc(start='program')


def parse(data):
    parser = build_parser()
    return parser.parse(data, lexer=lexer)


def main():
    global isFine
    logging.basicConfig(filename='logSintatico.txt', level=logging.INFO, filemode='w')

    if arquivos_zig:
        for arquivo in arquivos_zig:
            isFine = True
            print(f"-----------Analise Sintatica do arquivo: {arquivo}-----------")
            logging.info(f"-----------Analise Sintatica do arquivo: {arquivo}-----------")

            with open(arquivo, 'r', encoding='utf-8') as f:
                lexer.input(f.read())
                result = build_parser().parse(debug=0)

            print(result)
            logging.info(result)

            if isFine:
                print("Analise sintatica realizada com sucesso!")
                logging.info("Analise sintatica realizada com sucesso!")
            else:
                print("Analise sintatica constatou erro!")
                logging.info("Analise sintatica constatou erro!")

            print("\n")
    else:
        code = '''
const std = @import("std");

pub fn main() !void {
    const x: i32 = 42;
    var y: f64 = 3.14;

    const a = x +% 10;
    const b = x -% 5;
    const c = x *% 2;

    if (x > 0) {
        std.debug.print("Positivo\\n", .{});
    } else {
        return;
    }

    const z = x + 10;
    return;
}

fn add(a: i32, b: i32) i32 {
    return a + b;
}

const Point = struct {
    x: f32,
    y: f32,
};

const Color = enum {
    Red,
    Green,
    Blue,
};
'''
        result = parse(code)
        print(result)


if __name__ == "__main__":
    main()
