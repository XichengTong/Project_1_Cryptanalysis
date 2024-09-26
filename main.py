def load_plaintext(file_path):

    plaintexts = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

        for index in range(4, len(lines), 5):
            line = lines[index].strip()
            if line:  
                plaintexts.append(line)
    
    return plaintexts

def decrypt(ciphertext, plaintexts):
    
    # Use plaintext dictionary to decrypt here
    pass


def main():
    # Get the ciphertext entered by the user
    ciphertext = input("Enter the ciphertext: ").strip()

    # Read plaintext dictionary from file
    file_path = 's24_dictionary1.txt'
    plaintexts = load_plaintext(file_path)


    guessed_plaintext = decrypt(ciphertext, plaintexts)

    print("My plaintext guess is:", guessed_plaintext)

if __name__ == "__main__":
    main()