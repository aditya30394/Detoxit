import tensorflow as tf
import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model

import pickle

import os
cwd = os.path.dirname(os.path.realpath(__file__))

global graph
graph = tf.get_default_graph()
processing_len = 160
category = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
weights = [0.5, 0.1, 0.1, 0.1, 0.1, 0.1]


with graph.as_default():
	model = load_model(cwd + "/detoxit_model_sigmoid.h5")

with open(cwd + '/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

print(model)
def predict(str_comment):
	result = dict()
	new_sent = [str_comment]
	new_sent_tokens = tokenizer.texts_to_sequences(new_sent)
	new_sent = pad_sequences(new_sent_tokens, maxlen=processing_len, padding="post", truncating="post")
	with graph.as_default():
		prediction = model.predict(new_sent)
		for i in range(0,6):
			result[i] = '{:.0}'.format(prediction[0][i])
	return result


def getPredictions(str_comment):
	res = predict(str_comment)
	score = 0.0
	for i in range(0,6):
		# score += float(res[i]) * weights[i]
		score = max(score, float(res[i]))
	return score
