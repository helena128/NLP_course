from gensim.models import KeyedVectors
from math import log
import numpy as np
from nltk import word_tokenize

class SentenceModel:
	def __init__(self, sentences, word_vec):
		self.word_vec = word_vec
		self.idf_index = self.__build_idf_index(sentences)
		self.sent_vector = self.__build_sentence_vectors(sentences)

	# idf = log (n/t)
	# n - total number of docs
	# t - number of docs where term t appears
	def __build_idf_index(self, sentences):
		N = len(sentences)
		index = {}
		for s in sentences:
			for word in set(s):
				index[word] = index.get(word, 0) + 1
		for i in index:
			index[i] = log(N/index[i])
		return index

	def __build_sentence_vectors(self, sentences):
		word_vec = self.word_vec
		sent_vec = KeyedVectors(word_vec.vector_size)
		idf_index = self.idf_index

		for sent in sentences:
			sent_vec.add( \
				' '.join(sent), \
				np.average([word_vec.get_vector(word) * idf_index[word] \
                            for word in sent], 0))
		return sent_vec

	def search(self, query, k=10):
		print('>> query', query)
		query_vec = np.average([self.word_vec[word] * self.idf_index.get(word, 0)
			for word in word_tokenize(query)], 0)
		return self.sent_vector.similar_by_vector(query_vec, topn=k)