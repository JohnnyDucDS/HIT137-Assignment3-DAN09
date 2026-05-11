tokens = []
pos = 0

def tokenize(expr):
    tokens = []
    number = ""

    for ch in expr:
        if ch.isdigit():
            number += ch
        else:
            if number != "":            #first 2 if getting the number
                tokens.append(number)
                number = ""

            if ch in "+-*/()":
                tokens.append(ch)
            elif ch == " ":
                continue
            else:
                raise ValueError(f"Invalid character: {ch}")

    if number != "":    #the last number
        tokens.append(number)

    return tokens


def current_token():
    if pos < len(tokens):
        return tokens[pos]
    return None


def match(expected):
    global pos
    if current_token() == expected:
        pos += 1
    else:
        raise ValueError(f"Expected {expected}, got {current_token()}")


def parse_expression():
    node = parse_term()

    while current_token() in ['+', '-']:
        op = current_token()
        match(op)
        right = parse_term()
        node = (op, node, right)    #to build a new node-right branch

    return node


def parse_term():
    node = parse_factor()

    while current_token() in ['*', '/']:
        op = current_token()
        match(op)
        right = parse_factor()
        node = (op, node, right)

    return node


def parse_factor():
    tok = current_token()

    if tok == '(':
        match('(')
        node = parse_expression()
        match(')')
        return node

    elif tok == '-':
        match('-')
        return ('neg', parse_factor())

    elif tok is not None and tok.isdigit():
        match(tok)
        return int(tok)

    else:
        raise ValueError(f"Unexpected token: {tok}")


def to_tree_string(node):
    if isinstance(node, int):
        return str(node)

    if node[0] == 'neg':
        return f"(neg {to_tree_string(node[1])})"

    op, left, right = node
    return f"({op} {to_tree_string(left)} {to_tree_string(right)})"


def parse(expr):
    global tokens, pos
    tokens = tokenize(expr)
    pos = 0
    tree = parse_expression()
    return to_tree_string(tree)



expr = "3 * 2 - 4 / 3 + 4"


"""
node = ('+',
        ('*', ('-', 10, 2), 3),
        ('/', ('neg', 4), 2))
"""

        
expr1 = "(10 - 2) * 3 + -4 / 2"
print(parse(expr1))

