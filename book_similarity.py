import urllib.request
import pickle
import ssl

from fuzzywuzzy import fuzz
ssl._create_default_https_context = ssl._create_unverified_context

# Load data from a file (will be part of your data processing script)
with open('alice_original.pickle', 'rb') as f:
    reloaded_original_text = pickle.load(f, encoding='ISO-8859-1')

# List of book titles
book_titles = ['Through the Looking-Glass', 'Sylvie and Bruno', 'Peter Pan', 'The Wonderful Wizard of Oz',
               'The Game of Logic', 'Symbolic Logic', 'The Essentials of Logic', 'Logic as the Science of the Pure Concept']

# List of URLs for the books
book_urls = ['https://www.gutenberg.org/files/12/12-0.txt', 'https://www.gutenberg.org/files/620/620-0.txt', 'https://www.gutenberg.org/files/16/16-0.txt', 'https://www.gutenberg.org/files/55/55-0.txt',
             'https://www.gutenberg.org/cache/epub/4763/pg4763.txt', 'https://www.gutenberg.org/cache/epub/28696/pg28696.txt', 'https://www.gutenberg.org/files/63598/63598-0.txt', 'https://www.gutenberg.org/files/54137/54137-0.txt']

# List of texts for the books
book_texts = []

# Get the text for each book
for url in book_urls:
    with urllib.request.urlopen(url) as f:
        book_text = f.read().decode('utf-8')
        book_texts.append(book_text)

# from https://pypi.org/


def similarity(compared_text, text):
    """
    Computes the similarity ratio between 2 texts using fuzzy string matching. 
    """
    similarity_ratio = fuzz.ratio(compared_text, text)
    return similarity_ratio


def main():
    carroll_lit = book_texts[:2]
    other_lit = book_texts[2:4]
    carroll_math = book_texts[4:6]
    other_math = book_texts[-2:]

    # Compare "Alice's Adventure in Wonderland" to Carroll's other literature
    for i, text in enumerate(carroll_lit):
        print(
            f'The matching score between "Alice\'s Adventure in Wonderland" and "{book_titles[i]}" is {similarity(reloaded_original_text, text)}')

    # Compare other children's literature to "Alice's Adventure in Wonderland"
    for i, text in enumerate(other_lit):
        print(
            f'The matching score between "Alice\'s Adventure in Wonderland" and "{book_titles[i+2]}" is {similarity(reloaded_original_text, text)}')

    # Compare "Alice's Adventure in Wonderland" to Carroll's mathematical work
    for i, text in enumerate(carroll_math):
        print(
            f'The matching score between "Alice\'s Adventure in Wonderland" and "{book_titles[i+4]}" is {similarity(reloaded_original_text, text)}')

    # Compare Carroll's mathematical work to other mathematical work
    for i, text in enumerate(other_math):
        for j, carroll_work in enumerate(carroll_math):
            print(
                f'The matching score between "{book_titles[(j+6)]}" and "{book_titles[i+4]}" is {similarity(carroll_work, text)}')


if __name__ == '__main__':
    main()
