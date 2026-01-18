import compiler.ast as ast
from compiler.parser import parse
from compiler.tokenizer import tokenize, Token, Location, L

def test_parser_basics() -> None:
    tokens = tokenize("a + 3")
    assert parse(tokens) == ast.BinaryOp(
        left=ast.Identifier(name="a"),
        op="+",
        right=ast.Literal(value=3)
    )