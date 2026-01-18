from compiler.tokenizer import tokenize, Token, Location, L

def test_tokenizer_basics() -> None:
    assert tokenize("abc123_") == [
        Token(loc=L, type="identifier", text="abc123_")
    ]
    
def test_tokenizer_full() -> None:
    assert tokenize("(if 3 # this is a comment\nwhile*)") == [
        Token(loc=Location(row=0, column=0), type="punctuation", text="("),
        Token(loc=Location(row=0, column=1), type="identifier", text="if"),
        Token(loc=Location(row=0, column=4), type="int_literal", text="3"),
        Token(loc=Location(row=1, column=0), type="identifier", text="while"),
        Token(loc=Location(row=1, column=5), type="operator", text="*"),
        Token(loc=Location(row=1, column=6), type="punctuation", text=")")
    ]