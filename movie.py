import ssl
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from imdb import Cinemagoer
ssl._create_default_https_context = ssl._create_unverified_context

# create an instance of the Cinemagoer class
ia = Cinemagoer()
# search movie
movie = ia.search_movie("Alice's Adventures in Wonderland")[0]
# print(movie.movieID)
# '0068190'


def movie_review():
    """
    Returns a random movie review from the first 25 reviews.
    """
    global movie_reviews
    movie_reviews = ia.get_movie_reviews('0068190')
    number = random.randint(0, 25)
    return (movie_reviews['data']['reviews'][number]['content'])


def review_sentiment(review):
    """
    For the review generated above, compute the sentiment score of the review
    """
# Tokenize reviews
    tokenized_review = word_tokenize(review.lower())
# from geeks for geeks
# Remove stop words
    # creates a set of stop words from the stopwords corpus for the English language.
    stop_words = set(stopwords.words('english'))
    filtered_review = []
    for word in tokenized_review:
        if word not in stop_words:
            filtered_review.append(word)
# from geeks for geeks
# Perform sentiment analysis
    sentiment = SentimentIntensityAnalyzer()
    sentiment_scores = sentiment.polarity_scores(' '.join(filtered_review))
# Print sentiment scores
    return f"Sentiment Score: Positive = {sentiment_scores['pos']:.2f}, Negative = {sentiment_scores['neg']:.2f}, Neutral = {sentiment_scores['neu']:.2f}, Compound = {sentiment_scores['compound']:.2f}"


def search_word(word):
    """
    Search the word in the review, returns whether the review contains the word or not.
    """
# Define word to search
    word_to_search = word
# Get the text of the randomly selected review
    review_text = movie_review()
# Check if the word is present in the review text
    if word_to_search in review_text:
        return f"The word '{word_to_search}' is present in the review."
    else:
        return f"The word '{word_to_search}' is not present in the review."


def main():
    review = movie_review()
    print(review)
    print(review_sentiment(review))
    # To see whether the movie reviews mentioned "Carroll"
    print(search_word('Carroll'))


if __name__ == '__main__':
    main()
