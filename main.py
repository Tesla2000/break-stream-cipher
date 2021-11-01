import math

def XOR_str(str1, str2):
    if len(str1) > len(str2):
        return "".join([chr(ord(x) ^ ord(y)) for x, y in zip(str1[:len(str2)], str2)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for x, y in zip(str1, str2[:len(str1)])])


def XOR_char(c1, c2):
    return chr(ord(c1) ^ ord(c2))

def get_cryptograms(name) -> []:
    cryp = []
    with open(name, 'r') as file:
        for line in file:
            cryp.append(parse_cryptogram(line))
    return cryp

def parse_cryptogram(line) -> str:
    chars = []
    tmp = str(line).split(' ')
    for ch in tmp:
        chars.append(chr(int(ch, 2)))
    return "".join(chars)

# messages must be the same length (or padded) to reuse the same key, here we XOR with the length of the shorter message

cryptograms = get_cryptograms("data.txt")

# frequency of letters in polish (only ASCII characters) (e.g. ą + a freq in a), alphabet
frequency = {'a': 99, 'e': 87, 'o': 86, 'i': 82, 'z': 65, 'n': 57,
             's': 50, 'r': 47, 'w': 46, 'c': 44, 't': 40,  'l': 39, 'y': 38,
             'k': 35, 'd': 33, 'p': 31, 'm': 28, 'u': 25, 'j': 23,
             'b': 15, 'g': 15, 'h': 10, 'f': 1, 'q': 1, 'v': 1,
             'x': 1, ' ': 100, ',': 20, '.': 10, '-': 5, '"': 5, '!': 10, '?': 10, ':': 5, ';': 10, '(': 10,
             ')': 10}

# frequency of numbers - 10 (1%)
for i in range(48, 58):
    frequency[chr(i)] = 10

# uppercase letters, 3/4 frequency of lowercase
for i in range(65, 91):
    frequency[chr(i)] = math.ceil(frequency[chr(i + 32)] * 3 / 4)

# add other symbols, 0% frequency
for i in range(32, 128):
    if not chr(i) in frequency:
        frequency[chr(i)] = 1

key_best = []
# find the longest cryptogram
longest_idx = 0
for idx, crypto in enumerate(cryptograms):
    if len(crypto) > len(cryptograms[longest_idx]):
        longest_idx = idx

for i, c in enumerate(cryptograms[longest_idx]):
    possible = []
    for alpha in frequency:
        # try to match on the same position
        # p_1 xor p_1guess xor p_2 = p_2guess, if we guess p_1guess correctly then p_2guess = p_2, p1 xor c1 = k1
        count = 0
        count_length = 0
        for (index, match) in enumerate(cryptograms):
            # don't xor with yourself, get only cryptograms which have the position i
            if index != longest_idx and len(match) > i:
                count_length += 1
                result = XOR_char(XOR_char(c, match[i]), alpha)
                # if result is a valid character, then there's a chance that guess is correct
                if 32 <= ord(result) <= 126:
                    count += 1
        # gave valid letter in the remained cryptograms of valid length
        if count == count_length:
            possible.append(alpha)  # possible p_1
    # frequency analysis on p_2, find character of p_1, use p_1 which produces the most used chars in all streams
    if len(possible) > 0:
        best_char = possible[0]
        best_freq = 0
        for char in possible:
            curr_freq = 0
            for (index, match) in enumerate(cryptograms):
                if longest_idx != index and len(match) > i:
                    curr_freq += frequency[XOR_char(XOR_char(match[i], char), c)]
            if curr_freq >= best_freq:
                best_char = char
                best_freq = curr_freq
        key_best.append(XOR_char(best_char, c))

key = "".join(key_best)
# output
with open('output.txt', 'w') as file:
    for c in cryptograms:
        file.write(XOR_str(c, key))
        file.write('\n')

