import os

tokens = []
pos = 0


def format_number(value):
    # remove zeros, e.g. 3.5000 -> "3.5", 2.0 -> "2"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, int):
        return str(value)

    text = f"{value:.4f}"
    text = text.rstrip("0").rstrip(".")
    return text


def format_result(value):
    # same as format_number but used only for the output file
    if isinstance(value, str):
        return value

    if float(value).is_integer():
        return str(int(value))

    return f"{value:.4f}"


def token_to_string(token):
    # e.g. ("NUM", "3") -> "[NUM:3]"
    token_type, token_value = token

    if token_type == "END":
        return "[END]"

    return f"[{token_type}:{token_value}]"


def tokens_to_string(tokens):
    # joins all tokens into one string for display
    return " ".join(token_to_string(token) for token in tokens)


def tokenize(expr):
    # breaks expression string into typed tokens
    raw_tokens = []
    number = ""
    dot_count = 0

    for ch in expr:
        if ch.isdigit():
            number += ch

        elif ch == ".":
            number += ch
            dot_count += 1

            if dot_count > 1:
                raise ValueError("Invalid number")

        else:
            # flush buffered digits as a NUM token
            if number != "":
                if number == ".":
                    raise ValueError("Invalid number")
                raw_tokens.append(("NUM", format_number(float(number))))
                number = ""
                dot_count = 0

            if ch in "+-*/":
                raw_tokens.append(("OP", ch))
            elif ch == "(":
                raw_tokens.append(("LPAREN", ch))
            elif ch == ")":
                raw_tokens.append(("RPAREN", ch))
            elif ch == " ":
                continue
            else:
                raise ValueError(f"Invalid character: {ch}")

    # flush last number if expression ends with a digit
    if number != "":
        if number == ".":
            raise ValueError("Invalid number")
        raw_tokens.append(("NUM", format_number(float(number))))

    # insert implicit * and append END sentinel
    return add_implicit_multiplication(raw_tokens) + [("END", "")]


def add_implicit_multiplication(raw_tokens):
    # inserts "*" where implied, e.g. "2(3)" -> "2 * (3)"
    if not raw_tokens:
        return raw_tokens

    result = []

    for i in range(len(raw_tokens) - 1):
        current_token = raw_tokens[i]
        next_token = raw_tokens[i + 1]

        result.append(current_token)

        current_type = current_token[0]
        next_type = next_token[0]

        left_ok = current_type in ("NUM", "RPAREN")
        right_ok = next_type in ("NUM", "LPAREN")

        if left_ok and right_ok:
            result.append(("OP", "*"))

    result.append(raw_tokens[-1])
    return result


def current_token():
    # peek at current token without consuming it
    if pos < len(tokens):
        return tokens[pos]
    return None


def match(expected_type=None, expected_value=None):
    # consume current token; raises if type/value doesn't match
    global pos
    tok = current_token()

    if tok is None:
        raise ValueError("Unexpected end of input")

    tok_type, tok_value = tok

    if expected_type is not None and tok_type != expected_type:
        raise ValueError(f"Expected {expected_type}, got {tok}")

    if expected_value is not None and tok_value != expected_value:
        raise ValueError(f"Expected {expected_value}, got {tok}")

    pos += 1
    return tok


def parse_expression():
    # handles + and - (lowest precedence)
    node = parse_term()

    while current_token() is not None and current_token()[0] == "OP" and current_token()[1] in ["+", "-"]:
        op = current_token()[1]
        match("OP", op)
        right = parse_term()
        node = (op, node, right)

    return node


def parse_term():
    # handles * and / (higher precedence than + -)
    node = parse_factor()

    while current_token() is not None and current_token()[0] == "OP" and current_token()[1] in ["*", "/"]:
        op = current_token()[1]
        match("OP", op)
        right = parse_factor()
        node = (op, node, right)

    return node


def parse_factor():
    # handles numbers, parentheses, and unary minus
    tok = current_token()

    if tok is None:
        raise ValueError("Unexpected end of input")

    tok_type, tok_value = tok

    if tok_type == "LPAREN":
        match("LPAREN", "(")
        node = parse_expression()
        match("RPAREN", ")")
        return node

    elif tok_type == "OP" and tok_value == "-":
        match("OP", "-")
        return ("neg", parse_factor())

    elif tok_type == "OP" and tok_value == "+":
        raise ValueError("Unary plus is not supported")

    elif tok_type == "NUM":
        match("NUM")
        return float(tok_value)

    else:
        raise ValueError(f"Unexpected token: {tok}")


def to_tree_string(node):
    # converts AST to prefix string, e.g. "(+ (* 2 3) 4)"
    if isinstance(node, (int, float)):
        return format_number(node)

    if node[0] == "neg":
        return f"(neg {to_tree_string(node[1])})"

    op, left, right = node
    return f"({op} {to_tree_string(left)} {to_tree_string(right)})"


def evaluate_tree(node):
    # recursively computes the numeric result from the AST
    if isinstance(node, (int, float)):
        return node

    if node[0] == "neg":
        return -evaluate_tree(node[1])

    op, left, right = node
    left_val = evaluate_tree(left)
    right_val = evaluate_tree(right)

    if op == "+":
        return left_val + right_val
    if op == "-":
        return left_val - right_val
    if op == "*":
        return left_val * right_val
    if op == "/":
        if right_val == 0:
            raise ZeroDivisionError("Division by zero")
        return left_val / right_val

    raise ValueError(f"Unknown operator: {op}")


def process_expression(expr):
    global tokens, pos

    # stage 1: tokenize + parse — any error marks all fields as ERROR
    try:
        tokens = tokenize(expr)
        pos = 0

        tree = parse_expression()

        # leftover tokens = malformed input, e.g. "1 + 2 3"
        if current_token() is None or current_token()[0] != "END":
            raise ValueError("Extra input after valid expression")

    except Exception:
        return {
            "input": expr,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }

    # stage 2: evaluate — tree/tokens still shown even if eval fails (e.g. div by zero)
    try:
        result = evaluate_tree(tree)
    except Exception:
        result = "ERROR"

    return {
        "input": expr,
        "tree": to_tree_string(tree),
        "tokens": tokens_to_string(tokens),
        "result": result
    }


def write_output_file(output_path, results):
    # writes results to file, blank line between each entry
    with open(output_path, "w", encoding="utf-8") as file:
        for index, item in enumerate(results):
            file.write(f"Input: {item['input']}\n")
            file.write(f"Tree: {item['tree']}\n")
            file.write(f"Tokens: {item['tokens']}\n")
            file.write(f"Result: {format_result(item['result'])}\n")

            if index != len(results) - 1:
                file.write("\n")


def evaluate_file(input_path):
    # reads each non-blank line, processes it, writes output next to input file
    results = []

    with open(input_path, "r", encoding="utf-8") as file:
        for line in file:
            original_line = line.rstrip("\n")
            if original_line.strip() == "":
                continue
            results.append(process_expression(original_line))

    folder = os.path.dirname(input_path)
    output_path = os.path.join(folder, "output.txt") if folder else "output.txt"

    write_output_file(output_path, results)
    return results


if __name__ == "__main__":
    input_file = "sample_input.txt"

    try:
        evaluate_file(input_file)
        print("Done. Results written to output.txt")
    except FileNotFoundError:
        print(f"Error: '{input_file}' not found in this folder.")
