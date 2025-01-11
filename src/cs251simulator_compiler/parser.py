"""
Author       : FYWinds i@windis.cn
Date         : 1969-12-31 19:00:00
LastEditors  : FYWinds i@windis.cn
LastEditTime : 2025-01-10 19:10:06
FilePath     : /cs251simulator-compiler/src/cs251simulator_compiler/parser.py
"""

from ply.lex import lex  # type: ignore
from ply.yacc import yacc  # type: ignore

tokens = (
    "MEMORY",
    "REGISTERS",
    "INSTRUCTIONS",
    "INST",
    "REG",
    "IMM",
    "COMMA",
    "LBRACKET",
    "RBRACKET",
    "ASSIGN",
    "NUMBER",
)

t_COMMA = r","
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_ASSIGN = r"="

t_INST = r"ADDI|ADD|SUBI|SUB|LDUR|STUR|B|CBZ|CBNZ"

literals = ["M"]


def t_MEMORY(t):
    r"\.memory"
    return t


def t_REGISTERS(t):
    r"\.registers"
    return t


def t_INSTRUCTIONS(t):
    r"\.instructions"
    return t


def t_IMM(t):
    r"\#-?\d+"
    t.value = int(t.value[1:])
    return t


def t_REG(t):
    r"X(ZR|[0-2]?[0-9]|3[0-1])"
    t.value = int(t.value[1:] if t.value != "XZR" else 31)
    return t


def t_NUMBER(t):
    r"-?\d+"
    t.value = int(t.value)
    return t


t_ignore = " \t"


# Ignored token with an action associated with it
def t_ignore_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_ignore_comment(t):
    r"\#.*"
    pass


# Error handler for illegal characters
def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)


# Build the lexer object
lexer = lex()


def p_program(p):
    """
    program : memory_section register_section instruction_section
    """
    p[0] = ("program", p[1], p[2], p[3])


def p_memory_section(p):
    """
    memory_section : MEMORY memory_assignments
    """
    p[0] = ("memory_section", p[2])


def p_memory_assignments(p):
    """
    memory_assignments : memory_assignments memory_assignment
                       | memory_assignment
    """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_memory_assignment(p):
    """
    memory_assignment : 'M' LBRACKET NUMBER RBRACKET ASSIGN NUMBER
    """
    p[0] = ("memory_assignment", p[3], p[6])


def p_register_section(p):
    """
    register_section : REGISTERS register_assignments
    """
    p[0] = ("register_section", p[2])


def p_register_assignments(p):
    """
    register_assignments : register_assignments register_assignment
                         | register_assignment
    """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_register_assignment(p):
    """
    register_assignment : REG ASSIGN NUMBER
    """
    p[0] = ("register_assignment", p[1], p[3])


def p_instruction_section(p):
    """
    instruction_section : INSTRUCTIONS instructions
    """
    p[0] = ("instruction_section", p[2])


def p_instructions(p):
    """
    instructions : instructions instruction
                 | instruction
    """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_instruction(p):
    """
    instruction : INST instruction_args
    """
    p[0] = ("instruction", p[1], p[2])


def p_instruction_args(p):
    """
    instruction_args : instruction_args COMMA instruction_arg
                     | instruction_arg
    """
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_instruction_arg(p):
    """
    instruction_arg : REG
                    | LBRACKET REG COMMA IMM RBRACKET
                    | IMM
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = ("offset", p[2])
    else:
        p[0] = ("memory_access", p[2], p[4])


def p_error(p):
    print(f"Syntax error at line {p.lineno}: '{p.value}'")


# Build the parser
parser = yacc()

if __name__ == "__main__":
    # Test the lexer
    data = """
    .memory
    M[208] = 10101
    M[216] = 123
    .registers
    X9 = 8
    X3 = 15
    .instructions
    ADD X9, X3, X2
    ADDI X3, X9, #5
    LDUR X3, [X9, #8]
    STUR X3, [X9, #8]
    B #-4
    CBNZ X3, #-4
    """

    # Create a lexer
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)

    ast = parser.parse(data)
    ast = parser.parse(data, debug=True)
    print(ast)
