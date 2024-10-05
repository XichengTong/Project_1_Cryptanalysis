import string
import random
from collections import Counter

def load_plaintext(file_path):
    plaintexts = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

        for index in range(4, len(lines), 5):
            line = lines[index].strip()
            if line:
                plaintexts.append(line)

    return plaintexts

def load_plaintext_dictionary(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()
def load_local_percentage(file_path):
    """
    Reads a text file and calculates the frequency distribution of alphabets and spaces.
    Converts the distribution into percentage form and stores it in a dictionary.
    """
    # Initialize a dictionary to hold frequencies of all lowercase letters and space
    frequency_dict = {char: 0 for char in string.ascii_lowercase + ' '}

    # Open and read the file content
    with open(file_path, 'r') as file:
        content = file.read().lower()  # Convert content to lowercase

    # Count the frequency of each alphabet and space in the content
    for char in content:
        if char in frequency_dict:
            frequency_dict[char] += 1

    # Calculate total characters counted (only alphabets and spaces)
    total_count = sum(frequency_dict.values())

    # Calculate the percentage frequency for each character
    percentage_frequency = {char: (count / total_count) * 100 for char, count in frequency_dict.items()}

    return percentage_frequency

def calculate_index_of_coincidence(text):
    """
    Calculate the Index of Coincidence (IC) for the given text.
    IC is calculated as the sum of n_i * (n_i - 1) / N * (N - 1),
    where n_i is the frequency of character i, and N is the total number of characters.
    """
    # Remove non-alphabetic characters and convert to lowercase
    filtered_text = ''.join([char for char in text if char.isalpha()]).lower()

    # Calculate frequency of each character in the filtered text
    frequency = Counter(filtered_text)
    N = len(filtered_text)

    # Calculate the Index of Coincidence
    ic = sum(f * (f - 1) for f in frequency.values()) / (N * (N - 1)) if N > 1 else 0

    return ic


def identify_cipher_type(ciphertext):
    """
    Identify whether the given ciphertext is encrypted using a mono-alphabetic or poly-alphabetic cipher.
    """
    # Calculate the Index of Coincidence (IC) for the given ciphertext
    ic = calculate_index_of_coincidence(ciphertext)
    print(f"Index of Coincidence (IC) for the ciphertext: {ic:.4f}")

    # Thresholds for determining mono vs poly
    english_ic = 0.068  # Approximate IC for English text
    mono_ic_threshold = 0.05  # A threshold value for classifying mono-alphabetic vs poly-alphabetic

    # Determine the cipher type based on the IC value
    if ic >= mono_ic_threshold:
        return "mono-alphabetic substitution cipher"
    else:
        return "poly-alphabetic substitution cipher"

def frequency_analysis(text):
    """Perform frequency analysis on the given text, including spaces."""
    # Create a counter for all lowercase letters and space
    frequencies = Counter(char for char in text if char in string.ascii_lowercase + ' ')

    # Calculate the total count of characters considered (only lowercase letters and spaces)
    total = sum(frequencies.values())

    # Calculate the percentage frequency of each character
    frequency_percentages = {char: (count / total) * 100 for char, count in frequencies.items()}

    return frequency_percentages

def decrypt_monoalphabetic_cipher(cipher_text, cipher_to_plain_mapping):
    """Decrypt the cipher text using the provided cipher-to-plain mapping."""
    decrypted_text = ''.join([cipher_to_plain_mapping.get(char, char) for char in cipher_text])
    return decrypted_text


def word_count(text, char):
    """Count the frequency of a specific character in the given text."""
    # Convert the text to lowercase to count both lowercase and uppercase "e"
    lower_text = text.lower()
    char = char.lower()  # Convert the character to lowercase for a case-insensitive count

    # Count the occurrences of the character
    count = lower_text.count(char)

    return count

def mono_decrpt(ciphertext):

    # Step 1: Perform frequency analysis on the cipher text
    cipher_freq = frequency_analysis(ciphertext)

    # Step 2: Sort the cipher text characters by frequency in descending order
    sorted_cipher_letters = sorted(cipher_freq, key=cipher_freq.get, reverse=True)
    print(sorted_cipher_letters)
    print(load_plaintext("s24_dictionary1.txt"))

    for i in range(1,6):

        # Step 3: Get the frequency distribution of every plaintext
        percentage_dict = load_local_percentage(f"plaintext_{i}.txt")
        sorted_plaintext_letters = sorted(percentage_dict, key=percentage_dict.get, reverse=True)

        # Step 4: Create a mapping from the cipher text letters to English letters
        cipher_to_plain_mapping = {}
        for cipher_letter, plain_letter in zip(sorted_cipher_letters, sorted_plaintext_letters):
            cipher_to_plain_mapping[cipher_letter] = plain_letter

        # Step 5: Decrypt the cipher text using the frequency-based mapping
        decrypted_text = decrypt_monoalphabetic_cipher(ciphertext, cipher_to_plain_mapping)
        print(decrypted_text)

        # Step 6: Check the decrypted text

        if decrypted_text in load_plaintext("s24_dictionary1.txt"):
            print(decrypted_text)
            return decrypted_text


def shift_letter(char, shift):
    if char == ' ':
        return ' '
    return chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))


# Frequency analysis for a given text
def frequency_analysis(text):
    frequencies = {char: 0 for char in string.ascii_lowercase + ' '}
    for char in text:
        if char in frequencies:
            frequencies[char] += 1
    total = len(text)
    return {char: (count / total) * 100 for char, count in frequencies.items()}


# Compare frequency of ciphertext to English frequency
def compare_frequencies(ciphertext_freq, frequency_get):
    score = 0
    for char, freq in ciphertext_freq.items():
        expected_freq = frequency_get.get(char, 0)
        score += abs(freq - expected_freq)
    return score


# Brute force all possible key lengths (for polyalphabetic cipher)
def decrypt_with_key_length(ciphertext, dictionary, key_length, frequency_get):
    possible_plaintexts = []

    # Break ciphertext into key_length segments
    segments = [''.join([ciphertext[i] for i in range(idx, len(ciphertext), key_length)]) for idx in range(key_length)]

    # Apply frequency analysis and brute force each segment
    for segment in segments:
        best_score = float('inf')
        best_decryption = ""

        for shift in range(26):
            decrypted_segment = ''.join([shift_letter(char, shift) for char in segment])
            score = compare_frequencies(frequency_analysis(decrypted_segment), frequency_get)

            if score < best_score:
                best_score = score
                best_decryption = decrypted_segment

        possible_plaintexts.append(best_decryption)

    # Reconstruct the full plaintext by merging segments
    plaintext_guess = ''.join([possible_plaintexts[i % key_length][i // key_length] for i in range(len(ciphertext))])
    print(plaintext_guess)
    # Validate against the dictionary
    for candidate in dictionary:

        if candidate in plaintext_guess:
            return plaintext_guess

    return None


# Main cryptanalysis function
def cryptanalysis(ciphertext, dictionary, frequency_get):
    key_lengths = range(2, 10)  # Try key lengths between 2 and 10
    for key_length in key_lengths:
        plaintext = decrypt_with_key_length(ciphertext, dictionary, key_length, frequency_get)

        if plaintext:
            return plaintext

    return "Decryption failed"
def poly_decrpt(ciphertext):
    dictionary = load_plaintext_dictionary('plaintext_dictionary.txt')

    for i in range(1, 6):
        # Get the frequency distribution of every plaintext
        percentage_dict = load_local_percentage(f"plaintext_{i}.txt")
        return cryptanalysis(ciphertext,dictionary,percentage_dict)

def main():

    # Get the ciphertext entered by the user
    ciphertext = input("Enter the ciphertext: ").strip()

    #identify the way to cipher
    cipher_type=identify_cipher_type(ciphertext)
    if cipher_type=="mono-alphabetic substitution cipher":
        result=mono_decrpt(ciphertext)
    elif cipher_type=="poly-alphabetic substitution cipher":
        result = poly_decrpt(ciphertext)

    print("My plaintext guess is:")
    print(result)





if __name__ == "__main__":
    main()