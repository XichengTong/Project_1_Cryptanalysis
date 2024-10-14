import os
import string
from collections import Counter
import re

# Load plaintexts from a file
def load_plaintext(file_path):
    with open(file_path, 'r') as file:
        # Read the entire content of the file
        file_content = file.read()

    # Split the content into sections based on "Candidate Plaintext"
    plaintexts = []
    sections = file_content.split("Candidate Plaintext")

    plaintexts = [remove_first_pattern(sections[i].strip()) for i in range(1, 6)]
    return plaintexts


def remove_first_pattern(text):
    # Define the pattern to match '#1' followed by two newlines
    pattern = r"#[1-5]\n\n"
    return re.sub(pattern, '', text, count=1)


#Computes local alphabets distribution stastics
def load_local_percentage(text):  
    frequency_dict = {char: 0 for char in string.ascii_lowercase + ' '}
    content = text.lower()
    for char in content:
        if char in frequency_dict:
            frequency_dict[char] += 1

    total_count = sum(frequency_dict.values())
    if total_count == 0:
        return {char: 0 for char in frequency_dict}
    return {char: (count / total_count) * 100 for char, count in frequency_dict.items()}
    
#Calculate the index of function to judge whether the cipher type is mono or poly 
#See https://en.wikipedia.org/wiki/Index_of_coincidence for information
def calculate_index_of_coincidence(text):

    filtered_text = ''.join([char for char in text if char.isalpha()]).lower()
    frequency = Counter(filtered_text)
    N = len(filtered_text)
    return sum(f * (f - 1) for f in frequency.values()) / (N * (N - 1)) if N > 1 else 0

#Use the above function to identify whether the cipher is mono-alphabetic or poly-alphabetic,
#we choose the bar 0.05
def identify_cipher_type(ciphertext):
    ic = calculate_index_of_coincidence(ciphertext)
    #print(f"Index of Coincidence (IC) for the ciphertext: {ic:.4f}")
    mono_ic_threshold = 0.05
    if ic >= mono_ic_threshold:
        return "mono-alphabetic substitution cipher"
    else:
        return "poly-alphabetic substitution cipher"

#Analyze the frequency distribution of a specified text
def frequency_analysis(text):
    frequencies = Counter(char for char in text if char in string.ascii_lowercase + ' ')
    total = sum(frequencies.values())
    if total == 0:
        return {char: 0 for char in string.ascii_lowercase + ' '}
    frequency_percentages = {char: (count / total) * 100 for char, count in frequencies.items()}
    return frequency_percentages


#Using a provided mapping, decrypt a monoalphabetic cipher
def decrypt_monoalphabetic_cipher(cipher_text, cipher_to_plain_mapping):
    decrypted_text = ''.join([cipher_to_plain_mapping.get(char, char) for char in cipher_text])
    return decrypted_text

#Decrypt using monoalphabetic substitution and find a plausible match.
def mono_decrpt(ciphertext, plaintexts):  
    cipher_freq = frequency_analysis(ciphertext)
    sorted_cipher_letters = sorted(cipher_freq, key=cipher_freq.get, reverse=True)

    best_decryption = "Decryption failed"
    
    for plaintext in plaintexts:
        percentage_dict = load_local_percentage(plaintext)
        sorted_plaintext_letters = sorted(percentage_dict, key=percentage_dict.get, reverse=True)

        cipher_to_plain_mapping = {cipher_letter: plain_letter for cipher_letter, plain_letter in zip(sorted_cipher_letters, sorted_plaintext_letters)}

        decrypted_text = decrypt_monoalphabetic_cipher(ciphertext, cipher_to_plain_mapping)

        #Choose the first successful decryption
        if decrypted_text:
            best_decryption = decrypted_text
            break
    
    return best_decryption

#The main decrpt function when it is poly_decrpt
def poly_decrpt(ciphertext, plaintexts):
    decrpted_collect=[]
    for plaintext in plaintexts:
        percentage_dict = load_local_percentage(plaintext)
        decrypted_texts = cryptanalysis(ciphertext, plaintexts, percentage_dict)
        decrpted_collect.append(decrypted_texts)
    #Note this is a list of lists, with all possible decrpyted_texts
    return decrpted_collect
    


def cryptanalysis(ciphertext, dictionary, frequency_get):
    #The loop used for key length search doing poly_decrpted
    key_lengths = range(2, 10)
    decrpted_texts=[]
    for key_length in key_lengths:
        plaintext = decrypt_with_key_length(ciphertext, dictionary, key_length, frequency_get)
        decrpted_texts.append(plaintext)
    #Here got a list of possible answer
    return decrpted_texts
    

def shift_letter(char, shift):
    #Shift letter
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

    return plaintext_guess



def final_judge(decrpytedtext,plaintexts):
    #Mono final_judge, the key idea is to compare the plaintext and the decypted text, 
    #and then find the most similar one. This is applied because of randomized
    counts=[]
    count=0
    for i in range(5):
        plaintext = plaintexts[i]
 
        for j in range(len(decrpytedtext)):
            if plaintext[j]==decrpytedtext[j]:
                count+=1
        #print(count)
        counts.append(count)
        count=0
    index=counts.index(max(counts))
    return plaintexts[index]
    

def poly_final_judge(decrpted_collection,plaintexts):
    #Final judge for poly, key idea is similar to the mono part
    counts = []
    count = 0
    for i in range(5):
        plaintext = plaintexts[i]
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
    #Get the index of the most similar one, here divided by 8 because there 
    #is 8 different kinds of key lengths
    true_index=index//8

    return plaintexts[true_index]
     

# Based on user input, the main function of executing decryption  
def main():

    ciphertext = input("Enter the ciphertext:").strip()

    all_plaintexts = load_plaintext("s24_dictionary1.txt")
    if not all_plaintexts:
        print("No plaintexts loaded. Exiting.")
        return

    cipher_type = identify_cipher_type(ciphertext)

    if cipher_type == "mono-alphabetic substitution cipher":
        result = mono_decrpt(ciphertext, all_plaintexts)
        final_result = final_judge(result,all_plaintexts)
        print("My plaintext guess is:"+final_result)
    
    elif cipher_type == "poly-alphabetic substitution cipher":
        result = poly_decrpt(ciphertext, all_plaintexts)
        #print("My plaintext guess is:",result)
        final_result = poly_final_judge(result,all_plaintexts)
        print("My plaintext guess is:"+final_result)


if __name__ == "__main__":
    main()