import pandas as pd

from textblob import TextBlob

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

df= pd.read_csv('businessreview_2023.csv', encoding='utf-8')
df['Sentiment'] = df['Review'].apply(get_sentiment)
df['Sentiment'] = df['Sentiment'].apply(lambda x: 'Positive' if x >= 0 else 'Negative')

#save the new dataframe to a csv
df.to_csv('businessreview_2023_sentiment.csv', encoding='utf-8', index=False)

positive_reviews = df[df['Sentiment'] == 'Positive']['Review']
negative_reviews = df[df['Sentiment'] == 'Negative']['Review']

positive_summary = ' '.join(positive_reviews)
negative_summary = ' '.join(negative_reviews)

print("Positive Feedback Summary:")
print(positive_summary)
print("\nNegative Feedback Summary:")
print(negative_summary)
