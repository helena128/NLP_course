from nltk import sent_tokenize, word_tokenize
from gensim.models import Word2Vec
from normalizer import normalize
from visualizer import visualize, plot_simple_graph
from measurer import precision_at_k

# Constants
file_path = "/home/helena/Documents/NLP/data/study_in_scarlet.txt"
num_of_sentences = 30
model_window_5_file = "word2vec_model_5_window.model"
model_window_20_file = "word2vec_model_20_window.model"

# Read file
file = open(file_path, 'r')
text = file.read()

# Split into docs, tokenize & normalize
#sentences = sent_tokenize(text)
#documents = ['\n'.join(sentences[x: x + num_of_sentences]) for x in range(0, len(sentences), num_of_sentences)]
#documents = list(map(lambda d: normalize(word_tokenize(d)), documents))
#print(documents[:2])

tokens = normalize(word_tokenize(text))

# Create model
settings = {'workers': 3, 'min_count': 1}
model5 = Word2Vec([tokens], window = 5, **settings)
model20 = Word2Vec([tokens], window = 20, **settings)
model5.save(model_window_5_file)
model20.save(model_window_20_file)

# Similiarities
sample_queries = ['one', 'flaw', 'reason']
for query in sample_queries:
	results = model5.most_similar(query)[:3]
	print('Results for query', query, ':', results)

# Visualization
'''
visualize(model5, 'Study in scarlett, window=5, no split', 'model5.png')
visualize(model5, 'Study in scarlett, window=20, no split', 'model20.png')
'''

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
	model = Word2Vec([tokens], window=win, **settings)
	precision = precision_at_k(model, search_word, None, k, expectations, log=False)
	precision_per_window.append(precision)
	print("{}\t{}".format(win, precision))
plot_simple_graph("window_vs_precision.png", window_range, precision_per_window)

# Experimenting with different settings