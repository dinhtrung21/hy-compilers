from compiler.tokenizer import tokenize, Token, Location, L

def test_tokenizer_basics() -> None:
    assert tokenize("abc123_") == [
        Token(location=L, type="identifier", text="abc123_")
    ]
    
def test_tokenizer_full() -> None:
    assert tokenize("(if 3 # this is a comment\nwhile*)") == [
        Token(location=Location(row=1, column=0), type="punctuation", text="("),
        Token(location=Location(row=1, column=1), type="identifier", text="if"),
        Token(location=Location(row=1, column=4), type="int_literal", text="3"),
        Token(location=Location(row=2, column=0), type="identifier", text="while"),
        Token(location=Location(row=2, column=5), type="operator", text="*"),
        Token(location=Location(row=2, column=6), type="punctuation", text=")")
    ]