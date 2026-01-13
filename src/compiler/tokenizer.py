from itertools import groupby

def tokenize(source_code: str) -> list[str]:
    # Tokenizes the given source code into a list of tokens.
    tokens = source_code.split()
    # Further split numbers into individual literals
    for i, token in enumerate(tokens):
        groups = ["".join(g) for k, g in groupby(token, key=str.isdigit)]
        for j, symbol in enumerate(groups):
            # Turn integer literals into string
            if isinstance(symbol, int):
                groups[j] = str(symbol)
        tokens[i:i+1] = groups
    return tokens