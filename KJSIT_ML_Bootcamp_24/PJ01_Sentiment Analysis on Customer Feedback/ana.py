import streamlit as st
from textblob import TextBlob
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import cleantext
import matplotlib.pyplot as plt


df = pd.read_csv("Reviews.csv")
review_text = df['Text']

analyzer = SentimentIntensityAnalyzer()

sentiment_scores = []
blob_subj = []
for review in review_text:
    sentiment_scores.append(analyzer.polarity_scores(review)["compound"])
    blob = TextBlob(review)
    blob_subj.append(blob.subjectivity)

sentiment_classes = []
for sentiment_score in sentiment_scores:
    if sentiment_score > 0.8:
        sentiment_classes.append("highly positive")
    elif sentiment_score > 0.4:
        sentiment_classes.append("positive")
    elif -0.4 <= sentiment_score <=0.4:
       sentiment_classes.append("neutral") 
    elif sentiment_score < -0.4:
        sentiment_classes.append("negative")
    else:
        sentiment_classes.append("highly negative")

# streamlit
st.title("Sentiment Analysis On Customer Feedback")

user_input = st.text_area("Enter the Feedback: ")
blob = TextBlob(user_input)

user_sentiment_score = analyzer.polarity_scores(user_input)['compound']
if user_sentiment_score > 0.8:
    user_sentiment_class = "highly positive"
elif user_sentiment_score > 0.4:
    user_sentiment_class = "positive"
elif -0.4<= user_sentiment_score <= 0.4:
    user_sentiment_class = "neutral"
elif user_sentiment_score <-0.4:
    user_sentiment_class = "negative"
else:
    user_sentiment_class = "highly negative"

st.write("**VADER Sentiment Class: **",user_sentiment_class,"**VADER Sentiment Scores: **", user_sentiment_score )
st.write("**TextBlob Polarity: **",blob.sentiment.polarity,"**TextBlob Subjectivity: **", blob.sentiment.subjectivity)

# Display clean text

pre = st.text_input('Clean Text: ')
if pre:
    st.write(cleantext.clean(pre,clean_all= False, extra_spaces = True, stopwords = True, lowercase = True, numbers = True, punct = True))
else:
    st.write("No Text is Been provided from the user for cleaning.")

# GRAPHICAL REPRESENTATION OF THE DATA (REVIEWA DATASET)
st.subheader("Graphical Representation of Data")
plt.figure(figsize=(10,6))

sentiment_scores_by_class = {k: [] for k in set(sentiment_classes)}
for sentiment_scores,sentiment_class in zip(sentiment_scores, sentiment_classes):
    sentiment_scores_by_class[sentiment_class].append(sentiment_scores)

for sentiment_class, scores in sentiment_scores_by_class.items():
    plt.hist(scores, label = sentiment_class, alpha = 0.5)

plt.xlabel("Sentiment score")
plt.ylabel("Count")
plt.title("Score Distribution By Class")
plt.legend()
st.pyplot(plt)

# dataframens switch the sentiment analysis results

df["Sentiment Class"] = sentiment_classes
df["Sentiment Score"] = sentiment_scores
df["Subjectivity"] = blob_subj

new_df = df[["Score","Text","Sentiment Score","Sentiment Class","Subjectivity"]]
st.subheader("Input Dataframe")
st.dataframe(new_df.head(10),use_container_width=True)