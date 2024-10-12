import os
import string
from collections import Counter

def load_all_plaintexts():
    #this function loads all the plaintext from five files
    file_names = ['plaintext_1.txt', 'plaintext_2.txt', 'plaintext_3.txt', 'plaintext_4.txt', 'plaintext_5.txt']
    plaintexts = []
    for file_name in file_names:
        try:
            with open(file_name, 'r') as file:
                content = file.read().strip()
                if content:
                    plaintexts.append(content)
                else:
                    print(f"Warning: {file_name} is empty.")
        except FileNotFoundError:
            print(f"Error: {file_name} not found.")
    
    return plaintexts


def load_local_percentage(text):
    #this function computes local aplphabets distribution stastics
    frequency_dict = {char: 0 for char in string.ascii_lowercase + ' '}
    content = text.lower()
    for char in content:
        if char in frequency_dict:
            frequency_dict[char] += 1

    total_count = sum(frequency_dict.values())
    if total_count == 0:
        return {char: 0 for char in frequency_dict}
    percentage_frequency = {char: (count / total_count) * 100 for char, count in frequency_dict.items()}
    return percentage_frequency


def calculate_index_of_coincidence(text):
    #this function calculate index of function to judge whether the encrypt function is mono or poly
    #information see at https://en.wikipedia.org/wiki/Index_of_coincidence
    filtered_text = ''.join([char for char in text if char.isalpha()]).lower()
    frequency = Counter(filtered_text)
    N = len(filtered_text)
    ic = sum(f * (f - 1) for f in frequency.values()) / (N * (N - 1)) if N > 1 else 0
    return ic


def identify_cipher_type(ciphertext):
    #use the above function to judge the encrypt function, the bar 0.05 is chosen by myself
    ic = calculate_index_of_coincidence(ciphertext)
    print(f"Index of Coincidence (IC) for the ciphertext: {ic:.4f}")
    mono_ic_threshold = 0.05
    if ic >= mono_ic_threshold:
        return "mono-alphabetic substitution cipher"
    else:
        return "poly-alphabetic substitution cipher"


def frequency_analysis(text):
    #analyze the frequency distribution of a specified text
    frequencies = Counter(char for char in text if char in string.ascii_lowercase + ' ')
    total = sum(frequencies.values())
    if total == 0:
        return {char: 0 for char in string.ascii_lowercase + ' '}
    frequency_percentages = {char: (count / total) * 100 for char, count in frequencies.items()}
    return frequency_percentages



def decrypt_monoalphabetic_cipher(cipher_text, cipher_to_plain_mapping):
    decrypted_text = ''.join([cipher_to_plain_mapping.get(char, char) for char in cipher_text])
    return decrypted_text


def score_decryption(decrypted_text, plaintext):
    """计算解密后的文本和候选明文的相似度得分"""
    matches = sum(1 for a, b in zip(decrypted_text, plaintext) if a == b)
    return matches / len(plaintext)


def mono_decrpt(ciphertext, plaintexts):
    #the main decrpt function when it is mono_decrpt
    cipher_freq = frequency_analysis(ciphertext)
    sorted_cipher_letters = sorted(cipher_freq, key=cipher_freq.get, reverse=True)
    print("Sorted cipher letters by frequency:", sorted_cipher_letters)
    
    best_score = 0
    best_decryption = "Decryption failed"
    # find the best score after each mapping of frequency
    for i, plaintext in enumerate(plaintexts, start=1):
        percentage_dict = load_local_percentage(plaintext)
        sorted_plaintext_letters = sorted(percentage_dict, key=percentage_dict.get, reverse=True)
        print(f"Plaintext {i} sorted by frequency:", sorted_plaintext_letters)

        cipher_to_plain_mapping = {cipher_letter: plain_letter for cipher_letter, plain_letter in zip(sorted_cipher_letters, sorted_plaintext_letters)}
        print(f"Cipher to Plain mapping for Plaintext {i}: {cipher_to_plain_mapping}")

        decrypted_text = decrypt_monoalphabetic_cipher(ciphertext, cipher_to_plain_mapping)
        print(f"Decrypted text using Plaintext {i}: {decrypted_text}")
        
        score = score_decryption(decrypted_text, plaintext)
        print(f"Score for Plaintext {i}: {score}")

        if score > best_score:
            best_score = score
            best_decryption = decrypted_text
    
    return best_decryption


def poly_decrpt(ciphertext, plaintexts):
    # the main decrpt function when it is poly_decrpt
    decrpted_collect=[]
    for plaintext in plaintexts:
        percentage_dict = load_local_percentage(plaintext)
        decrypted_texts = cryptanalysis(ciphertext, plaintexts, percentage_dict)
        decrpted_collect.append(decrypted_texts)
    return decrpted_collect
    #note this is a list of lists, with all possible decrpyted_texts


def cryptanalysis(ciphertext, dictionary, frequency_get):
    #the loop used for key length search doing poly_decrpted
    key_lengths = range(2, 10)
    decrpted_texts=[]
    for key_length in key_lengths:
        plaintext = decrypt_with_key_length(ciphertext, dictionary, key_length, frequency_get)
        decrpted_texts.append(plaintext)
    return decrpted_texts
    #this is a list of possible answer

def shift_letter(char, shift):
    #just shift letter
    if char == ' ':
        return ' '
    if 'a' <= char <= 'z':
        return chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
    return char

def compare_frequencies(ciphertext_freq, frequency_get):
    score = 0
    for char, freq in ciphertext_freq.items():
        expected_freq = frequency_get.get(char, 0)
        score += abs(freq - expected_freq)
    return score

def decrypt_with_key_length(ciphertext, dictionary, key_length, frequency_get):
    #key length search, use a specified key and brute force to get the highest score
    possible_plaintexts = []

    segments = [''.join([ciphertext[i] for i in range(idx, len(ciphertext), key_length)]) for idx in range(key_length)]
    #segments here are small string collections of key length
    #the loop below do the brute force attack
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

    plaintext_guess = ''.join([possible_plaintexts[i % key_length][i // key_length] for i in range(len(ciphertext))])
    #print("Reconstructed plaintext guess:", plaintext_guess)
    #if you want to see all the guesses, use the command above

    return plaintext_guess



def final_judge(decrpytedtext):
    #mono final_judge, the key idea is to compare the plaintext and the decypted text, and then find the most similar one
    #this is applied because of randomized
    counts=[]
    count=0
    for i in range(1, 6):
        with open(f"plaintext_{i}.txt", 'r') as file:
            plaintext = file.read().strip()
        for j in range(len(decrpytedtext)):
            if plaintext[j]==decrpytedtext[j]:
                count+=1
        print(count)
        counts.append(count)
        count=0
    index=counts.index(max(counts))
    with open(f"plaintext_{index+1}.txt", 'r') as file:
        plaintext = file.read().strip()
        return plaintext

def poly_final_judge(decrpted_collection):
    #final judge for poly, key idea is similar to the mono part
    counts = []
    count = 0
    for i in range(1,6):
        with open(f"plaintext_{i}.txt", 'r') as file:
            plaintext = file.read().strip()
        #open every plaintexts
        for j in range(8):
            #go over every key lengths
            for k in range(len(decrpted_collection[i-1][j])):
                if plaintext[k] == decrpted_collection[i-1][j][k]:
                    count += 1
                #compare every alphabets
            counts.append(count)
            count = 0
    index = counts.index(max(counts))
    #get the index of the most similar one, here divided by 8 because there is 8 different kinds of key lengths
    true_index=index//8
    with open(f"plaintext_{true_index+1}.txt", 'r') as file:
        plaintext = file.read().strip()
        return plaintext


def main():

    ciphertext = input("Enter the ciphertext: ").strip()

    all_plaintexts = load_all_plaintexts()
    if not all_plaintexts:
        print("No plaintexts loaded. Exiting.")
        return

    cipher_type = identify_cipher_type(ciphertext)

    if cipher_type == "mono-alphabetic substitution cipher":
        result = mono_decrpt(ciphertext, all_plaintexts)
        final_result = final_judge(result)
        print(final_result)
    elif cipher_type == "poly-alphabetic substitution cipher":
        result = poly_decrpt(ciphertext, all_plaintexts)
        print(result)
        final_result = poly_final_judge(result)
        print(final_result)
    else:
        result = "Unknown cipher type"



if __name__ == "__main__":
    main()
