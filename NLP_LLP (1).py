#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('punkt')
nltk.download('stopwords')


# In[ ]:


input_df = pd.read_excel("Input.xlsx")


# In[ ]:


def extract_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    article_title = soup.find("title").get_text()
    article_text_elements = soup.find_all("p")
    article_text = "\n".join([element.get_text() for element in article_text_elements])
    return article_title, article_text


# In[ ]:


def syllable_count(word):
    vowels = "aeiouy"
    count = 0
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count


# In[ ]:


def count_personal_pronouns(text):
    pronouns = ["i", "me", "my", "mine", "myself", "we", "us", "our", "ours", "ourselves"]
    words = word_tokenize(text)
    count = sum([1 for word in words if word.lower() in pronouns])
    return count


# In[ ]:


def calculate_text_analysis(text):
    blob = TextBlob(text)
    polarity_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity
    positive_score = max(0, polarity_score) 
    negative_score = max(0, -polarity_score) 
    words = word_tokenize(text)
    word_count = len(words)
    sentences = sent_tokenize(text)
    sentence_lengths = [len(word_tokenize(sentence)) for sentence in sentences]
    avg_sentence_length = sum(sentence_lengths) / len(sentences)
    complex_words = [word for word in words if len(word) > 6]
    percentage_complex_words = (len(complex_words) / word_count) * 100
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_words_per_sentence = word_count / len(sentences)
    complex_word_count = len(complex_words)
    syllables_per_word = sum([syllable_count(word) for word in words]) / word_count 
    personal_pronouns = count_personal_pronouns(text)
    avg_word_length = sum([len(word) for word in words]) / word_count
    
    
    return positive_score, negative_score, polarity_score, subjectivity_score, \
           avg_sentence_length, percentage_complex_words, fog_index, \
           avg_words_per_sentence, complex_word_count, word_count, \
           syllables_per_word, personal_pronouns, avg_word_length


# In[ ]:


output_data = []

for index, row in input_df.iterrows():
    url_id = row["URL_ID"]
    url = row["URL"]    
    article_title, article_text = extract_article_text(url)    
    positive_score, negative_score, polarity_score, subjectivity_score, \
    avg_sentence_length, percentage_complex_words, fog_index, \
    avg_words_per_sentence, complex_word_count, word_count, \
    syllables_per_word, personal_pronouns, avg_word_length = calculate_text_analysis(article_text)
    
    output_data.append({
        "URL_ID": url_id,
        "URL": url,
        "Article_Title": article_title,
        "Article_Text": article_text,
        "POSITIVE SCORE": positive_score,
        "NEGATIVE SCORE": negative_score,
        "POLARITY SCORE": polarity_score,
        "SUBJECTIVITY SCORE": subjectivity_score,
        "AVG SENTENCE LENGTH": avg_sentence_length,
        "PERCENTAGE OF COMPLEX WORDS": percentage_complex_words,
        "FOG INDEX": fog_index,
        "AVG NUMBER OF WORDS PER SENTENCE": avg_words_per_sentence,
        "COMPLEX WORD COUNT": complex_word_count,
        "WORD COUNT": word_count,
        "SYLLABLE PER WORD": syllables_per_word,
        "PERSONAL PRONOUNS": personal_pronouns,
        "AVG WORD LENGTH": avg_word_length
    })


# In[ ]:


output_df = pd.DataFrame(output_data)
output_df.to_excel("Output Data Structure.xlsx", index=False)


# In[ ]:




