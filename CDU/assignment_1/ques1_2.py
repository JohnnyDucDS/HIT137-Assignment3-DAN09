password = str(input('Password: '))
char = list(password)
has_digit = False
has_upper = False
if len(char) < 7:
    print(f'This password is WEAK\nOnly contains {len(char)} characters')
elif password == '':
    print('Invalid password')
else:
    for x in char:
        if x.isdigit():         # can use: if x in '0123456789' - use string because password is string
            has_digit = True
        if x.isupper():         # can use: if x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            has_upper = True
    if has_digit and len(char) < 11:
        print(f'This password is MEDIUM\n Only contains {len(char)}')
    elif has_digit and has_upper:
        print(f'This password is STRONG')
