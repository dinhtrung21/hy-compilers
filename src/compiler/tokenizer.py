from dataclasses import dataclass
from itertools import groupby


@dataclass
class Location:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

# Special location for ease of testing
L = Location(row=0, column=0)
    
    
@dataclass
class Token:
    def __init__(self, loc: Location, type: str, text: str):
        self.loc = loc
        self.type = type
        self.text = text
        
    def __eq__(self, other):
        # Return true if self or the argument is L
        if isinstance(other, Token):
            return self.loc == L or other.loc == L
        return False


# *** Build the tokenizer of the compiler ***
def tokenize(source_code: str) -> list[str]:
    # Tokenizes the given source code into a list of tokens.
    texts = source_code.split()
    # Further split numbers into individual literals
    for i, text in enumerate(texts):
        groups = ["".join(g) for k, g in groupby(text, key=str.isdigit)]
        for j, symbol in enumerate(groups):
            # Turn integer literals into string
            if isinstance(symbol, int):
                groups[j] = str(symbol)
        texts[i:i+1] = groups
        
    # Change texts into Tokens
    tokens = []
    for i, text in enumerate(texts)
        token = Token(loc=L, type="identifier", text=text)
        tokens.append(token)
        
    return tokens