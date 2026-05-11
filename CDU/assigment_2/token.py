# read input txt file
import os

# Get the absolute path of the directory where txt file is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Join the script's directory path with the filename to get the full file path
file_path = os.path.join(script_dir, "expression_1.txt")

with open(file_path, "r") as file:
    content = file.read()


# token
def get_tokens(content):
    tokens = []
    i = 0
    while i < len(content):
        if content[i].isspace():
            i += 1
            continue
        
        # Handle Numbers (integers and floats)
        if content[i].isdigit() or content[i] == '.':
            start = i
            while i < len(content) and (content[i].isdigit() or content[i] == '.'):
                i += 1
            val = content[start:i]
            if val.count('.') > 1:
                return None
            tokens.append(('NUM', val))
            continue    
            
        # Handle Operators
        if content[i] in '+-*/':
            tokens.append(('OP', content[i]))
            i += 1
            continue
            
        # Handle Parentheses
        if content[i] == '(':
            tokens.append(('LPAREN', '('))
            i += 1
            continue
        if content[i] == ')':
            tokens.append(('RPAREN', ')'))
            i += 1
            continue
            
        # Invalid character
        return None
        
    tokens.append(('END', ''))
    return tokens

print(get_tokens(content))