from nltk import sent_tokenize, word_tokenize
from gensim.models import Word2Vec
from normalizer import normalize_sentence
from visualizer import visualize, plot_simple_graph
from measurer import precision_at_k
from sentence_analysator import SentenceModel
from operator import is_not
from functools import partial

# Constants
file_path = "/home/helena/Documents/NLP/data/study_in_scarlet.txt"
model_window_5_file = "word2vec_model_5_window.model"
model_window_20_file = "word2vec_model_20_window.model"

# Read file
file = open(file_path, 'r')
text = file.read()

# Tokenize & normalize
sentences = sent_tokenize(text)
sentences = list(map(lambda s: normalize_sentence(s), sentences))
sentences = list(filter(partial(is_not, None), sentences))

# Create model
# min_count (int, optional) – Ignores all words with total frequency lower than this.
# workers (int, optional) – Use these many worker threads to train the model (=faster training with multicore machines).
# sg ({0, 1}, optional) – Training algorithm: 1 for skip-gram; otherwise CBOW.
settings = {'workers': 3, 'min_count': 1, 'sg': 1}

model5 = Word2Vec(sentences, window = 5, **settings)
model20 = Word2Vec(sentences, window = 20, **settings)
model5.save(model_window_5_file)
model20.save(model_window_20_file)

# Sample search
sample_queries = ['one', 'flaw', 'reason']
for query in sample_queries:
	results = model5.most_similar(query)[:3]
	print('Results for query', query, ':', results)

# Visualization
"""
visualize(model5, 'Study in scarlett, window=5, no split', 'model5.png')
visualize(model5, 'Study in scarlett, window=20, no split', 'model20.png')
"""

# Precision@K
k = 30
search_word = 'holmes'
expectations = ['sherlock', 'asked', 'remarked', 'mr', 'observed', 'seemed', 'followed']
precision_at_k(model5, search_word, None, k, expectations)

# Experimenting with different window size
window_range = [i for i in range(5, 11)]
precision_per_window = []
print("Window\tPrecision")
for win in window_range:
	model = Word2Vec(sentences, window=win, **settings)
	precision = precision_at_k(model, search_word, None, k, expectations, log=False)
	precision_per_window.append(precision)
	print("{}\t{}".format(win, precision))
plot_simple_graph("window_vs_precision.png", window_range, precision_per_window)

# Experimenting with dimensions
size_range = [i * 10 for i in range(1, 7)]
precision_per_size = []
print("\nSize\tPrecision")
for s in size_range:
	model = Word2Vec(sentences, window=5, min_count=1, size=s)
	precision = precision_at_k(model, search_word, None, k, expectations, log=False)
	precision_per_size.append(precision)
	print("{}\t{}".format(s, precision))
plot_simple_graph("size_vs_precision.png", size_range, precision_per_size)

# Sentence model
queries = ['sherlock holmes said', 'little girl']
sent_model = SentenceModel(sentences, model5.wv)
for q in queries:
	results = sent_model.search(q, 5)
	print("Results for", q, ":", results)