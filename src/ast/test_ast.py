from src.lexer import Lexer
from src.parser import Parser


def test_string():
    p = Parser(Lexer("let myVar = 234;"))
    prog = p.parse_program()
    assert str(prog) == "let myVar = ;"
