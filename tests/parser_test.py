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


def test_parser_task2() -> None:
    tokens1 = tokenize('if a then b + c else x * y')
    tokens2 = tokenize('if a then b + c')
    tokens3 = tokenize('1 + if true then 2 else 3')
    tokens4 = tokenize('if a then if b then c else d')
    assert parse(tokens1) == ast.Conditional(
        cond_=ast.Identifier(name="a"),
        then_=ast.BinaryOp(
            left=ast.Identifier(name="b"),
            op="+",
            right=ast.Identifier(name="c")
        ),
        else_=ast.BinaryOp(
            left=ast.Identifier(name="x"),
            op="*",
            right=ast.Identifier(name="y")
        )
    )
    assert parse(tokens2) == ast.Conditional(
        cond_=ast.Identifier(name="a"),
        then_=ast.BinaryOp(
            left=ast.Identifier(name="b"),
            op="+",
            right=ast.Identifier(name="c")
        ),
        else_=None
    )
    assert parse(tokens3) == ast.BinaryOp(
        left=ast.Literal(value=1),
        op="+",
        right=ast.Conditional(
            cond_=ast.Identifier(name="true"),
            then_=ast.Literal(value=2),
            else_=ast.Literal(value=3)
        )
    )
    assert parse(tokens4) == ast.Conditional(
        cond_=ast.Identifier(name="a"),
        then_=ast.Conditional(
            cond_=ast.Identifier(name="b"),
            then_=ast.Identifier(name="c"),
            else_=ast.Identifier(name="d"),
        ),
        else_=None
    )


def test_parser_task3() -> None:
    tokens = tokenize('1 + f(x, (y + z) * 3)')
    assert parse(tokens) == ast.BinaryOp(
        left=ast.Literal(value=1),
        op="+",
        right=ast.Function(
            name=ast.Identifier(name="f"),
            args=[
                ast.Identifier(name="x"),
                ast.BinaryOp(
                    left=ast.BinaryOp(
                        left=ast.Identifier(name="y"),
                        op="+",
                        right=ast.Identifier(name="z")
                    ),
                    op="*",
                    right=ast.Literal(value=3)
                )
            ]
        )
    )