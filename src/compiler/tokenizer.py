from dataclasses import dataclass
import re
from typing import Any, List


@dataclass
class Location:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

# Special location for ease of testing
L = Location(row=0, column=-1)


@dataclass
class Token:
    def __init__(self, location: Location, type: str, text: str):
        self.location = location
        self.type = type
        self.text = text
        
    def __eq__(self, other: Any) -> bool:
        # Return true if self or the argument is L
        if isinstance(other, Token):
            return self.location == L or other.location == L
        return False


# Regexes for each type of token
regexes = {
    "identifier": re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*'),
    "int_literal": re.compile(r'[0-9]+'),
    "operator": re.compile(r'==|!=|<=|>=|\+|\-|\*|/|%|=|<|>'),
    "punctuation": re.compile(r'[(){},;:]'),
    "BLANK": re.compile(r'[ \t]+'),
    "COMMENT": re.compile(r'#.*|//.*|(/\*).*?(\*/)'),
    "ENDLINE": re.compile(r'\n')
}


# Helper function to create the token
def find_type(source_code: str, pos: int) -> tuple[str, str, int]:
    for type in ["identifier", "int_literal", "operator", "punctuation"]:
            match = regexes[type].match(source_code, pos)
            # Define the token
            if match is not None:
                end = match.end()
                text = source_code[pos:end]
                return type, text, end
    
    # Raise error if no token is found
    raise Exception(f'Fail to tokenize at {pos}')


# *** Build the tokenizer of the compiler ***
def tokenize(source_code: str) -> list[Token]:
    # Counters for location
    pos = 0; row = 1; column = 0
    # List for storing tokens
    tokens: List[Token] = []
    
    # Loop through each character in the source code
    while pos < len(source_code):
        # Skip blank spaces
        match = regexes["BLANK"].match(source_code, pos)
        if match is not None:
            column += match.end() - pos
            pos = match.end()
            continue
        # Skip comments
        match = regexes["COMMENT"].match(source_code, pos)
        if match is not None:
            pos = match.end()
            continue
        # Skip end of lines
        match = regexes["ENDLINE"].match(source_code, pos)
        if match is not None:
            row += 1
            column = 0
            pos = match.end()
            continue
        
        # Find the match and create the token
        location = Location(row=row, column=column)
        type, text, end = find_type(source_code, pos)
        token = Token(location=location, type=type, text=text)
        tokens.append(token)
        pos = end
    
    return tokens