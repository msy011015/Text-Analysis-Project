import urllib.request
import ssl
import pickle
import string

# from ChatGPT
# disabling SSL verification
ssl._create_default_https_context = ssl._create_unverified_context


def word_freq_dict(skip_header):
    """
    Downloads the text of "Alice’s Adventures in Wonderland" from the Gutenberg Project website, 
    removes the header if specified, 
    and then counts the frequency of each word, 
    ignoring stop words, 
    and prints out a dictionary with the word frequencies.
    """
    url = 'https://www.gutenberg.org/cache/epub/11/pg11.txt'
    with urllib.request.urlopen(url) as f:
        global text
        text = f.read().decode('utf-8')
    # print(text) # for testing

    # create an empty dict
    word_freq = {}

    # skip the head/remove the punctuation
    if skip_header:
        text = skip_gutenberg_header(text)
    strippables = string.punctuation + string.whitespace + \
        ''.join(filter(lambda x: not x.isprintable(), string.printable))
    stop_words = ["the", "and", "a", "an", "in", "on", "at", "to", "of", "for",
                  "with", "that", "this", "these", "those", "is", "was", "were", "am", "are", "be"]

    # cut the end
    for line in text.split('\n'):  # creates a list for the single line
        if line.startswith('*** END OF THE PROJECT'):
            break
    # replace hyphens and em dashes with spaces respectively
        line = line.replace('-', ' ')
        line = line.replace(chr(8212), ' ')
    # each word
        for word in line.split():
            clean_word = ''.join(char for char in word.strip(
                strippables) if char not in string.punctuation)  # debug by chatGPT
            clean_word = clean_word.lower()
            if clean_word not in stop_words:
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
    return word_freq


def skip_gutenberg_header(text):
    """
    Reads from text until it finds the line that ends the header.
    """
    lines = text.split('\n')  # creates a list for the single line
    for i, line in enumerate(lines):  # i = index, line = item
        if line.startswith('*** START OF THE PROJECT '):
            return '\n'.join(lines[i+1:])
    return text


# Save data to a file (will be part of your data fetching script)
# Dict we created
with open('alice_texts.pickle', 'wb') as f:
    pickle.dump(word_freq_dict(skip_header=True), f)
# The original text
with open('alice_original.pickle', 'wb') as f:
    pickle.dump((text), f)


def main():
    word_freq = word_freq_dict(skip_header=True)
    print(word_freq)


if __name__ == '__main__':
    main()
