# -*- coding: utf-8 -*-
"""Sentimential_Analysis_With_Tensorflow&Keras.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1glrDtj0PRt5rd60-3vrJOfkGLCfSs4DM

# Sentiment Analysis Project

## System Requirements
Python - 3x
Pandas - 1.2.4
Matplotlib - 3.3.4
Tensorflow - 2.4.1

Dataset : Kaggle - Twitter US Airline Sentiment

If the libraries are not installed, run the command
!pip install pandas matplotlib tensorflow

## Loading Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from google.colab import files
files.upload()

os.listdir()

df = pd.read_csv('Tweets.csv')

"""## Data Preprecossing"""

df.head()

df.columns

df.isnull().sum()

df.info()

df.describe()

review_df = df[['text', 'airline_sentiment']]

review_df.shape

review_df.head()

review_df = review_df[review_df['airline_sentiment'] != 'neutral' ]

review_df.shape

review_df.head()

review_df["airline_sentiment"].value_counts()

# look factorize() 
sentiment_label = review_df.airline_sentiment.factorize()
sentiment_label

tweet = review_df.text.values

from tensorflow.keras.preprocessing.text import Tokenizer

tokenizer =  Tokenizer(num_words = 5000)
tokenizer.fit_on_texts(tweet)

encoded_docs = tokenizer.texts_to_sequences(tweet)

from tensorflow.keras.preprocessing.sequence import pad_sequences

padded_sequence = pad_sequences(encoded_docs, maxlen=200)

"""## Build Text Classifier"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, SpatialDropout1D
from tensorflow.keras.layers import Embedding

embedding_vector_length = 32
vocab_size = 32
model = Sequential()
model.add(Embedding(vocab_size, embedding_vector_length, input_length=200))
model.add(SpatialDropout1D(0.25))
model.add(LSTM(50, dropout=0.5, recurrent_dropout=0.5))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

print(model.summary())

"""## Train the sentimental analysis model"""

history = model.fit(padded_sequence, sentiment_label[0], validation_split=0.2, epochs=5, batch_size=32)

"""## Visualization"""

plt.plot(history.history['accuracy'], label = 'acc')
plt.plot(history.history['val_accuracy'], label = 'val_acc')
plt.legend()
plt.show()

plt.plot(history.history['loss'], label = 'loss')
plt.plot(history.history['val_loss'], label = 'val_loss')
plt.legend()
plt.show()

"""## Predicted"""

def predict_sentiment(text):
  tw = tokenizer.texts_to_sequences([text])
  tw = pad_sequences(tw, maxlen = 200)
  prediction = int(model.predict(tw).round().item())
  print("Predicted label : ", sentiment_label[1][prediction])

test_sentence1 = "I enjoyed my journey on this flight."
print(predict_sentiment(test_sentence1))

test_sentence2 = "This is the worst flight experience of my life!" 
print(predict_sentiment(test_sentence2))