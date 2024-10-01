import string
import random

# Load the English letter frequency for analysis
LETTER_FREQUENCY = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702, 'f': 2.228, 'g': 2.015, 'h': 6.094, 
    'i': 6.966, 'j': 0.153, 'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507, 'p': 1.929, 
    'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056, 'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 
    'y': 1.974, 'z': 0.074, ' ': 15.000  # include space for plaintext
}

# Load the plaintext dictionary
def load_plaintext_dictionary(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()

# Shift a letter by a certain number of positions (for decryption in poly-alphabetic cipher)
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
def compare_frequencies(ciphertext_freq):
    score = 0
    for char, freq in ciphertext_freq.items():
        expected_freq = LETTER_FREQUENCY.get(char, 0)
        score += abs(freq - expected_freq)
    return score

# Brute force all possible key lengths (for polyalphabetic cipher)
def decrypt_with_key_length(ciphertext, dictionary, key_length):
    possible_plaintexts = []
    
    # Break ciphertext into key_length segments
    segments = [''.join([ciphertext[i] for i in range(idx, len(ciphertext), key_length)]) for idx in range(key_length)]
    
    # Apply frequency analysis and brute force each segment
    for segment in segments:
        best_score = float('inf')
        best_decryption = ""
        
        for shift in range(26):
            decrypted_segment = ''.join([shift_letter(char, shift) for char in segment])
            score = compare_frequencies(frequency_analysis(decrypted_segment))
            
            if score < best_score:
                best_score = score
                best_decryption = decrypted_segment
        
        possible_plaintexts.append(best_decryption)
    
    # Reconstruct the full plaintext by merging segments
    plaintext_guess = ''.join([possible_plaintexts[i % key_length][i // key_length] for i in range(len(ciphertext))])
    
    # Validate against the dictionary
    for candidate in dictionary:
        if candidate in plaintext_guess:
            return plaintext_guess
    
    return None

# Main cryptanalysis function
def cryptanalysis(ciphertext, dictionary):
    key_lengths = range(2, 10)  # Try key lengths between 2 and 10
    for key_length in key_lengths:
        plaintext = decrypt_with_key_length(ciphertext, dictionary, key_length)
        if plaintext:
            return plaintext
    return "Decryption failed"

# Main program execution
if __name__ == "__main__":
    # Sample ciphertext input
    ciphertext = input("Enter the ciphertext: ")

    # Load the plaintext dictionary
    dictionary = load_plaintext_dictionary('plaintext_dictionary.txt')

    # Perform cryptanalysis
    result = cryptanalysis(ciphertext, dictionary)
    
    # Output the result
    print(f"My plaintext guess is: {result}")