import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')

stop_words = set(stopwords.words('english'))
sid = SentimentIntensityAnalyzer()

df= pd.read_csv('businessreview_2023.csv', encoding='utf-8')


def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Convert to lowercase
    tokens = [token.lower() for token in tokens]
    
    # Remove stopwords and punctuation
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    
    # Join tokens back into a string
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text

df['Preprocessed_Review'] = df['Review'].apply(preprocess_text)

def get_sentiment(text):
    sentiment_scores = sid.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    return 'Positive' if compound_score >= 0 else 'Negative'

df['Sentiment'] = df['Preprocessed_Review'].apply(get_sentiment)

#save the new dataframe to a csv
df.to_csv('businessreview_2023_sentiment.csv', encoding='utf-8', index=False)


positive_reviews = df[df['Sentiment'] == 'Positive']['Review']
negative_reviews = df[df['Sentiment'] == 'Negative']['Review']

positive_summary = ' '.join(positive_reviews)
negative_summary = ' '.join(negative_reviews)

#save poisitive and negative summary to a text file
with open('positive_summary.txt', 'w') as f:
    f.write(positive_summary)
    
with open('negative_summary.txt', 'w') as f:
    f.write(negative_summary)