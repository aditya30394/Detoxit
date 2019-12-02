from aggiehub.models import Survey, Notification, Claim

import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from keras import optimizers

from decimal import *
import tensorflow as tf
import numpy as np
import pickle
import os

global graph
graph = tf.get_default_graph()
processing_len = 160
cwd = os.path.dirname(os.path.realpath(__file__))
category = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
weights = [0.5, 0.1, 0.1, 0.1, 0.1, 0.1]

with graph.as_default():
	model = load_model(cwd + "/detoxit_model_sigmoid.h5")

with open(cwd + '/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)


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


def update_model(survey_posts):
	train, test = format_survey_results(survey_posts)
	if len(train) > 0 :
		train_seq = tokenizer.texts_to_sequences(train)
		padded_X_train = pad_sequences(train_seq, maxlen=processing_len, padding='post', value=0.0, truncating='post')
		model.fit(padded_X_train, test, batch_size=64, epochs=6, verbose=1, shuffle=False)
		model.save(cwd + "/detoxit_model_sigmoid_updated.h5")


def getPredictions(str_comment):
	res = predict(str_comment)
	score = 0.0
	for i in range(0,6):
		# score += float(res[i]) * weights[i]
		score = max(score, float(res[i]))
	return score


def format_survey_results(survey_posts):
	train = []
	test = []
	for post in survey_posts:
		surveys = Survey.objects.filter(post__exact = post, is_completed__exact = True)
		median = median_value(surveys, "score")
		
		if (post.isToxic() and median > 3) or (not post.isToxic() and median < 3) or median == 3:
			print("Correctly guessed.")
		else:
			if median < 3:
				post.score = 0.0
			else:
				post.score = 1.0
			post.save()
			train.append(post.text)
			res = predict(post.text)
			score = 0.0
			for i in range(0,6):
				score = max(score, float(res[i]))
			one_hot_encoding = []
			for i in range(0,6):
				if float(res[i]) == score:
					one_hot_encoding.append(1)
				else:
					one_hot_encoding.append(0)
			test.append(np.asarray(one_hot_encoding))
		
		all_surveys = Survey.objects.filter(post__exact = post)
		for survey in all_surveys:
			survey.is_completed = True
			survey.save()
	
		resolve_type = Notification.RESOLVE_NONTOXIC
		if post.isToxic():
			resolve_type = Notification.RESOLVE_TOXIC
		claims = post.claim_set.all()
		for claim in claims:
			claim.resolved = True
			claim.save()
			notification = Notification(user = claim.user, notif_id = claim.id, type = resolve_type, text = post.text)
			notification.save()

	return train, np.asarray(test)


def median_value(queryset, term):
    count = queryset.count()
    values = queryset.values_list(term, flat=True).order_by(term)
    if count % 2 == 1:
        return values[int(round(count/2))]
    else:
        return sum(values[count/2-1:count/2+1])/Decimal(2.0)