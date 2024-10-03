import string
import random

# Define the alphabet size t=27 (26 letters + space)
alphabet = string.ascii_lowercase + " "


# Create a random substitution for the alphabet (this is just an example key)
# In practice, you would choose a permutation of the alphabet randomly or use a predefined one.
mono_substitution_key = "qwertyuiopasdfghjklzxcvbnm "
poly_key="mykey"
# Create dictionaries for encryption
mono_encryption_dict = {original: substitute for original, substitute in zip(alphabet, mono_substitution_key)}


# Create a dictionary to map 'a' to 'z' to 1 through 26, and add space (' ') mapped to 27
letter_to_number = {letter: index for index, letter in enumerate(string.ascii_lowercase, start=1)}
letter_to_number[' '] = 27  # Manually add the space character mapped to 27
number_to_letter = {index: letter for index, letter in enumerate(string.ascii_lowercase + ' ', start=1)}


def load_plaintext(filename):
    with open(filename, 'r') as file:
        content = file.read()  # Read the file content as a string

    # Split the content into a list of lines without newlines
    lines = content.splitlines()

    # Print each line as a separate string
    text=""
    for line in lines:
        text+=line
    return text



def mono_encrypt(message, encryption_dict):
    """Encrypt the message using the substitution key."""
    encrypted_message=""
    for char in message:
        encrypted_message += encryption_dict.get(char)
    return encrypted_message

def poly_encrypt(message,poly_key,letter_to_number,number_to_letter):
    encrypted_message=""
    i=0

    for char in message:
        index=(int(letter_to_number.get(char))+int(letter_to_number.get(poly_key[i])))%27
        if index==0:
            encrypted_message+=" "
            i += 1
            if i >= len(poly_key):
                i = 0
            continue
        encrypted_message += number_to_letter[index]
        i+=1
        if i>=len(poly_key):
            i=0
    return encrypted_message


def random_change_10_percent(input_string):
    """Randomly change 10% of the characters in the input string."""
    # Calculate the number of characters to change (10% of the length of the string)
    length = len(input_string)
    num_changes = max(1, int(length * 0.10))  # Ensure at least 1 change if the string is very short

    # Create a list of characters from the input string (strings are immutable in Python)
    input_list = list(input_string)

    # Define the set of characters to choose replacements from (all lowercase letters + digits)
    replacement_chars = string.ascii_lowercase  + " "

    # Randomly select positions to change
    positions_to_change = random.sample(range(length), num_changes)

    # Replace characters at the selected positions with random choices from the replacement_chars set
    for pos in positions_to_change:
        # Ensure the new character is different from the original one
        new_char = random.choice(replacement_chars)
        while new_char == input_list[pos]:
            new_char = random.choice(replacement_chars)
        input_list[pos] = new_char

    # Join the list back into a string
    return ''.join(input_list)


if __name__ == "__main__":

    #randomly choose a plaintext
    choice=random.randint(1,5)
    choice=3
    plain_choice="plaintext_"+str(choice)+".txt"
    print(plain_choice)

    # Load the plaintext dictionary
    plaintext_decided = load_plaintext(plain_choice)
    print(plaintext_decided)

    mono_cyphertext=mono_encrypt(plaintext_decided,mono_encryption_dict)
    print(mono_cyphertext)

    poly_cyphertext=poly_encrypt(plaintext_decided,poly_key,letter_to_number,number_to_letter)
    print(poly_cyphertext)

    randomized=random_change_10_percent(plaintext_decided)
    print(randomized)




