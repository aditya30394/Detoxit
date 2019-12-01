import re
import nltk
import pickle
from sklearn.linear_model import LogisticRegression
from nltk.stem import PorterStemmer

import os
cwd = os.path.dirname(os.path.realpath(__file__))

nltk.download('stopwords')
stemmer= PorterStemmer()
stop_words = set(nltk.corpus.stopwords.words('english'))
vectorizer = pickle.load( open( cwd + "/vectorizer.pickle", "rb" ) )
classifer = pickle.load( open( cwd + "/naive_bayes.pickle", "rb" ) )

def preprocess_input(comment):
# remove the extra spaces at the end.
    comment = comment.strip()
# lowercase to avoid difference between 'hate', 'HaTe'
    comment = comment.lower()
# remove the escape sequences. 
    comment = re.sub('[\s0-9]',' ', comment)
    #comment = stemmer.stem(comment)
# Use nltk's word tokenizer to split the sentence into words. It is better than the 'split' method.
    words = nltk.word_tokenize(comment)
# removing the commonly used words.
    #words = [word for word in words if not word in stop_words and len(word) > 2]
    words = [word for word in words if len(word) > 2]
    return words

def predict_each_word(comment):
    toxic_words = list()
    comment = preprocess_input(comment)
    for word in comment:
        token = vectorizer.transform([word])
        score = round(classifer.predict_proba(token)[:,1][0], 2)
        if score >= 0.50:
            toxic_words.append(word)
    
    return toxic_words