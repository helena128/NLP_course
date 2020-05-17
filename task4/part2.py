import spacy
from nltk import sent_tokenize
from sklearn.cluster import KMeans
import random

# Init spacy
nlp = spacy.load('en_core_web_sm')

# Get tezt of the book
file_name = '../data/study_in_scarlet.txt'
file_text = open(file_name, 'r').read()

# Split into sentences 
# Sentence tokenization can also be done with spacy
'''
sentences = list(nlp(file_text).sents)
'''
sentences = sent_tokenize(file_text)

# Create spacy object for each sentence
spacified_sents = tuple(map(nlp, sentences))

# Cluster sentences (based on their vectors)
n_clusters = 10
model = KMeans(n_clusters=n_clusters, random_state=0).fit(
	tuple(map(lambda s: s.vector, spacified_sents)))
clusters = {}
for sentence, assigned_cluster in zip(spacified_sents, model.labels_):
	if assigned_cluster in clusters:
		clusters[assigned_cluster].append(sentence)
	else:
		clusters[assigned_cluster] = [sentence]
for cl_label in clusters:
	print('> Cluster label:', cl_label)
	for sample_sent in random.choices(clusters[cl_label], k=3):
		print('>>', sample_sent)
	print('')

'''
Results:
see psrt2_out.txt
'''