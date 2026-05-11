# Function to guarantee chars are always in ASCII, regardless of how many shifts 
def shift_char(char, shift, forward=True):
    # If chars are not in alphabet (numbers, special characters, etc), remain unchanged
    if not char.isalpha():
        return char
    
    # Define the start position in ASCII ('a' = 97, 'A' = 65)               | 'A' - 'Z' | 65 - 90 | 
    start_position = ord('a') if char.islower() else ord('A')

    # Set the character to a range of 0-25 (position in alphabet)           | 'a' - 'z' | 97 - 122 |
    current_position = ord(char) - start_position

    # Calculate new position using modulo operator (%) to rotate from z back to a
    if forward:
        new_position = (current_position + shift) % 26
    else:
        new_position = (current_position - shift) % 26
    return chr(start_position + new_position)


# Encrypted Function
def encrypt(shift1, shift2):
    # Open raw file to read the content
    with open("raw_text.txt", "r") as f:
        raw_content = f.read()
    
    encrypted_content = ""
    for char in raw_content:
        # Lower case: letter from a-m: shift toward by shift1*shift2 positions
        if 'a' <= char <= 'm':
            encrypted_content += shift_char(char, shift1 * shift2, True)

        # Lower case: letter from n-z: shift backward by shift1 + shift2 positions
        elif 'n' <= char <= 'z':
            encrypted_content += shift_char(char, shift1 + shift2, False)

        # Upper case: letter from A-M: shift backward by shift1 positions
        elif 'A' <= char <= 'M':
            encrypted_content += shift_char(char, shift1, False)

        # Upper case: letter from N-Z: shift forward by shift2 squared positions
        elif 'N' <= char <= 'Z':
            encrypted_content += shift_char(char, shift2 ** 2, True)

        # Other characters: remain unchanged
        else:
            encrypted_content += char

    # Write encrypted content in encrypted file:
    with open("encrypted_text.txt", "w") as f:
        f.write(encrypted_content)


# Decrypted Function:
def decrypt(shift1, shift2):
    # Open encrypted file to read the content
    with open("encrypted_text.txt", "r") as f:
        encrypted_content = f.read()

    decrypted_content = ""
    # Decrypt each encrypted letter:
    for char in encrypted_content:
        # Lower case:
        if 'a' <= char <= 'z':
            # Reverse the movement steps to check what is the range (a-m or n-z) that the current letter belong to
            # original 'a-m' is shifted forward => now we move it backward
            attempt_a_to_m = shift_char(char, shift1 * shift2, forward=False)
            if 'a' <= attempt_a_to_m <= 'm':
                decrypted_content += attempt_a_to_m
                continue
            
            # if not a-m, it belong to n-z (is shifted backward => now we move it forward)
            attempt_n_to_z = shift_char(char, shift1 + shift2, forward=True)
            decrypted_content += attempt_n_to_z

        # Upper case:
        elif 'A' <= char <= 'Z':
            # A-M: original letter is moved backward shift1 => now we move it forward
            attempt_A_to_M = shift_char(char, shift1, forward=True)
            if 'A' <= attempt_A_to_M <= 'M':
                decrypted_content += attempt_A_to_M
                continue
            
            # N-Z: original letter is moved forward => now we move it backward
            attempt_N_to_Z = shift_char(char, shift2 ** 2, forward=False)
            decrypted_content += attempt_N_to_Z

        # Other characters: remain unchanged    
        else:
            decrypted_content += char

    # Write decrypted content in decrypted file:
    with open("decrypted_text.txt", "w") as f:
        f.write(decrypted_content)


def verify():
    with open("raw_text.txt", "r") as f:
        raw_content = f.read()

    with open("decrypted_text.txt", "r") as f:
        decrypted_content = f.read()

    if raw_content == decrypted_content:
        print("Decryption was successful.")
    else:
        print("Decryption was not successful.")

# Ask user to enter values of shift1 and shift2

if __name__ == "__main__":
    while True:
        try:
            shift1 = int(input("Enter shift1: "))
            shift2 = int(input("Enter shift2: "))
            break
        except ValueError:
            print("Error: Only integer is accepted")
    encrypt(shift1, shift2)
    decrypt(shift1, shift2)
    verify()
