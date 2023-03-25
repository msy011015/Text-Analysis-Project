from nltk.tag import pos_tag
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import ssl
import pickle
import nltk
import pprint
ssl._create_default_https_context = ssl._create_unverified_context

# Load data from a file (will be part of your data processing script)
with open('alice_texts.pickle', 'rb') as f:
    reloaded_copy_of_dict = pickle.load(f, encoding='ISO-8859-1')

with open('alice_original.pickle', 'rb') as f:
    reloaded_original_text = pickle.load(f, encoding='ISO-8859-1')

# Computing Summary Stats


def most_common(reloaded_copy_of_dict):
    """
    Makes a list of word-freq pairs in descending order of frequency.
    """
    res = []
    for word in reloaded_copy_of_dict:
        freq = reloaded_copy_of_dict[word]
        res.append((freq, word))

    res.sort(reverse=True)
    return res


def top_10_words(reloaded_copy_of_dict, num=10):
    """
    Makes a list of the top 10 most common words and their frequencies.
    """
    common_word = most_common(reloaded_copy_of_dict)
    common = []
    for i in range(num):
        freq, word = common_word[i]
        common.append((freq, word))
    return common


def total_words(reloaded_copy_of_dict):
    """
    Returns the number of the total words in the text.
    """
    total = 0
    for word in reloaded_copy_of_dict.keys():
        total += reloaded_copy_of_dict[word]
    return total


def type_taken_ratio(reloaded_copy_of_dict):
    """
    Returns TTR, which measures the diversity of words used in a text 
    by comparing the number of unique words (types) to the total number of words (tokens).
    """
    unique_words = set(reloaded_copy_of_dict.keys())
    total = total_words(reloaded_copy_of_dict)
    TTR = len(unique_words) / total
    TTR_percent = round(TTR * 100, 2)
    return TTR_percent

# Natural Language Processing
# Sentiment analysis


def sentiment_analysis(reloaded_original_text):
    """
    Do the sentiment analysis to the text, return scores
    """
    score = SentimentIntensityAnalyzer().polarity_scores(reloaded_original_text)
    return score

# Part-of-speech (POS) tagging


def pos(reloaded_original_text):
    """
    Identify nouns, verbs and adjectives in the text and compute the numbers of them.
    """
    words = nltk.word_tokenize(reloaded_original_text)
    # learned from https://www.guru99.com/
    pos_tags = nltk.pos_tag(words)
    noun = 0
    verb = 0
    adj = 0
    for word, pos in pos_tags:
        if pos.startswith('N'):
            noun += 1
        elif pos.startswith('V'):
            verb += 1
        elif pos.startswith('J'):
            adj += 1
    return noun, verb, adj


def top_adj(reloaded_copy_of_dict):
    """
    Find the top common adjs in the text.
    """
    words = list(reloaded_copy_of_dict.keys())
    adj_freq = {}
    for word in words:
        pos_tags = nltk.pos_tag([word])
        pos = pos_tags[0][1]
        if pos.startswith('J'):
            adj_freq[word] = reloaded_copy_of_dict[word]

    # from ChatGpt >> simplify the code
    sorted_nouns = sorted(adj_freq.items(), key=lambda x: x[1], reverse=True)
    top_adjs = sorted_nouns[:20]

    # from ChatGPT debug suggestion
    # I don't know why they were identified as noun, but I just eliminate them from the list manually
    top_adjs = [(word, freq) for word, freq in top_adjs if word not in [
        'much', 'such', 'other', 'last', 'next']]
    return top_adjs


def concordance(word, lines):
    """
    Display up to 25 lines containing the search word, with the search term highlighted in context.
    """
    words = nltk.word_tokenize(reloaded_original_text)
    text = nltk.Text(words)
    conc = text.concordance(word, width=140, lines=lines)
    return conc


def main():
    print("10 most common words in the text are:")
    pprint.pprint(top_10_words(reloaded_copy_of_dict, num=10))
    print()

    # print(f"The TTR of Alice’s Adventures in Wonderland is {type_taken_ratio(reloaded_copy_of_dict):.2f}%")

    print("The sentiment scores of Alice's Adverturens in Wonderland are:")
    print(sentiment_analysis(reloaded_original_text))
    print()

    # noun, verb, adj = pos(reloaded_original_text)
    # print (f'Nouns = {noun}')
    # print (f'Verbs = {verb}')
    # print (f'Adjectives = {adj}')

    print("10 most common adjs in the text are:")
    pprint.pprint(top_adj(reloaded_copy_of_dict))

    # print(concordance("Alice", 10))


if __name__ == '__main__':
    main()
