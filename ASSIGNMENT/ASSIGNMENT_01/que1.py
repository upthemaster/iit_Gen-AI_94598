sentence = input("Enter a sentence: ")
print(sentence)

char_length = len(sentence)
print("length of sentence : ", char_length)

num_word = len(sentence.split())
print("Count of Word:", num_word)

vowels = "aeiouAEIOU"
vowel_count = 0
for ch in sentence:
    if ch in vowels:
        vowel_count += 1
print("no of vowels: ", vowel_count)