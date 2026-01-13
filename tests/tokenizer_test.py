from compiler.tokenizer import tokenize

def test_tokenizer_basics() -> None:
    assert tokenize("if  3\nwhile") == ['if', '3', 'while']
    assert tokenize("123abc456def") == ['123', 'abc', '456', 'def']
    assert tokenize("3-2 is ok") == ['3', '-', '2', 'is', 'ok']