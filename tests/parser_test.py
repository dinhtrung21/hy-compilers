import compiler.ast as ast
from compiler.parser import parse
from compiler.tokenizer import tokenize, Token, Location, L


def test_parser_task1() -> None:
    tokens = tokenize('9 - (a + b - 3) * f / c')
    assert parse(tokens) == ast.BinaryOp(
        left=ast.Literal(value=9),
        op="-",
        right=ast.BinaryOp(
            left=ast.BinaryOp(
                left=ast.BinaryOp(
                    left=ast.BinaryOp(
                        left=ast.Identifier(name="a"),
                        op="+",
                        right=ast.Identifier(name="b")
                    ),
                    op="-",
                    right=ast.Literal(value=3)
                ),
                op="*",
                right=ast.Identifier(name="f")
            ),
            op="/",
            right=ast.Identifier(name="c")
        )
    )