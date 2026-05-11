import os

from question_2_test import consume, peek 

def parse_expression(state):
    """Parser: Level 1 - Handles addition and subtraction."""
    node = parse_term(state)
    while True:
        curr_type, curr_val = peek(state)
        if curr_type == 'OP' and curr_val in ('+', '-'):
            op = consume(state)[1]
            right = parse_term(state)
            node = (op, node, right)
        else:
            break
    return node

def parse_term(state):
    """Parser: Level 2 - Handles multiplication, division, and implicit multiplication."""
    node = parse_factor(state)
    while True:
        curr_type, curr_val = peek(state)
        # Check for implicit multiplication (e.g., 2(3) or 2 3)
        if curr_type in ('LPAREN', 'NUM'):
            op = '*'
            right = parse_factor(state)
            node = (op, node, right)
        # Check for explicit multiplication or division
        elif curr_type == 'OP' and curr_val in ('*', '/'):
            op = consume(state)[1]
            right = parse_factor(state)
            node = (op, node, right)
        else:
            break
    return node

def parse_factor(state):
    """Parser: Level 3 - Handles unary negation, numbers, and parentheses."""
    curr_type, curr_val = peek(state)
    
    # Unary negation
    if curr_type == 'OP' and curr_val == '-':
        consume(state)
        operand = parse_factor(state)
        return ('neg', operand)
    
    # Unary plus error requirement
    if curr_type == 'OP' and curr_val == '+':
        raise ValueError("Unary + not supported")
        
    # Numbers
    if curr_type == 'NUM':
        return consume(state)[1]
    
    # Parentheses
    if curr_type == 'LPAREN':
        consume(state)
        node = parse_expression(state)
        if peek(state)[0] != 'RAREN':
            raise ValueError("Unbalanced parentheses")
        consume(state)
        return node
        
    raise ValueError("Unexpected token")

def evaluate_tree(node):
    """Evaluates the parsed expression tree."""
    if isinstance(node, str):
        return float(node)
    
    op = node[0]
    if op == 'neg':
        return -evaluate_tree(node[1])
    
    left = evaluate_tree(node[1])
    right = evaluate_tree(node[2])
    
    if op == '+':  
        return left + right
    if op == '-': 
        return left - right
    if op == '*': 
        return left * right
    if op == '/':
        if right == 0:
            raise ZeroDivisionError("Division by zero")
        return left / right
    return 0.0

def tree_to_string(node):
    """Converts the parsed tree structure back into the required S-expression string."""
    if isinstance(node, str):
        return node
    if node[0] == 'neg':
        return f"(neg {tree_to_string(node[1])})"
    return f"({node[0]} {tree_to_string(node[1])} {tree_to_string(node[2])})"



