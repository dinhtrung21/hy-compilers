from compiler.tokenizer import Token
import compiler.ast as ast


def parse(tokens: list[Token]) -> ast.Expression:
    # This keeps track of which token we're looking at.
    pos = 0
    
    # 'peek()' returns the token at 'pos',
    # or a special 'end' token if we're past the end
    # of the token list.
    # This way we don't have to worry about going past
    # the end elsewhere.
    def peek() -> Token:
        if len(tokens) > 0:
            if pos < len(tokens):
                return tokens[pos]
            else:
                return Token(
                    location=tokens[-1].location,
                    type="end",
                    text="",
                )
        raise IndexError(f'The list of tokens has no entry.')
    
    
    # 'consume()' returns the token at 'pos'
    # and increments 'pos' by one.
    #
    # If the optional parameter 'expected' is given,
    # it checks that the token being consumed has that text.
    # If 'expected' is a list, then the token must have
    # one of the texts in the list.
    def consume(expected: str | list[str] | None = None) -> Token:
        nonlocal pos    # Python's "nonlocal" lets us modify `pos`
                        # without creating a local variable of the same name.
        token = peek()
        if isinstance(expected, str) and token.text != expected:
            raise Exception((f'Row {token.location.row}, column {token.location.column}: '\
                            f'expected "{expected}" instead of "{token.text}".'))
        if isinstance(expected, list) and token.text not in expected:
            comma_separated = ", ".join([f'"{e}"' for e in expected])
            raise Exception((f'Row {token.location.row}, column {token.location.column}: '\
                            f'expected one of: {comma_separated} instead of "{token.text}".'))
        pos += 1
        return token
    
    
    # This is the parsing function for integer literals.
    def parse_int_literal() -> ast.Literal:
        if peek().type != 'int_literal':
            raise Exception((f'Row {peek().location.row}, column {peek().location.column}: '\
                            f'expected an integer literal instead of "{peek().text}".'))
        token = consume()
        return ast.Literal(int(token.text))
    
    
    # This is the parsing function for identifiers.
    def parse_identifier() -> ast.Identifier:
        if peek().type != 'identifier':
            raise Exception((f'Row {peek().location.row}, column {peek().location.column}: '\
                            f'expected an identifier instead of "{peek().text}".'))
        token = consume()
        return ast.Identifier(token.text)
    
    
    def parse_expression() -> ast.Expression:
        # Same as before
        left = parse_term()
        while peek().text in ['+', '-']:
            operator_token = consume()
            operator = operator_token.text
            right = parse_term()
            left = ast.BinaryOp(
                left,
                operator,
                right
            )
        if (peek().type != "identifier" and peek().text != '(') \
        or peek().text in ['if', 'then', 'else']:
            return left
        raise Exception((f'Row {peek().location.row}, column {peek().location.column}: '\
                        f'expected an operator instead of "{peek().text}".'))
    
    
    def parse_term() -> ast.Expression:
        # Same structure as in 'parse_expression',
        # but the operators and function calls differ.
        left = parse_factor()
        while peek().text in ['*', '/']:
            operator_token = consume()
            operator = operator_token.text
            right = parse_factor()
            left = ast.BinaryOp(
                left,
                operator,
                right
            )
        return left
    
    
    def parse_factor() -> ast.Expression:
        if peek().text == '(':
            return parse_parenthesized()
        elif peek().text == 'if':
            return parse_conditional()
        elif peek().type == 'int_literal':
            return parse_int_literal()
        elif peek().type == 'identifier':
            return parse_identifier()
        else:
            raise Exception((f'Row {peek().location.row}, column {peek().location.column}: '\
                            f'expected "(", an integer literal or an identifier instead of "{peek().text}".'))
    
    
    def parse_parenthesized() -> ast.Expression:
        consume('(')
        # Recursively call the top level parsing function
        # to parse whatever is inside the parentheses.
        expr = parse_expression()
        consume(')')
        return expr
    
    def parse_conditional() -> ast.Expression:
        consume('if')
        cond_ = parse_expression()
        consume('then')
        then_ = parse_expression()
        else_ = None
        if peek().text == 'else':
            consume('else')
            else_ = parse_expression()
        
        expr = ast.Conditional(cond_=cond_, then_=then_, else_=else_)
        return expr
    
    
    return parse_expression()