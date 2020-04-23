from nltk import sent_tokenize, word_tokenize
from gensim.models import Word2Vec
from normalizer import normalize
from visualizer import visualize

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
params = {'workers': 3, 'min_count': 1}
model5 = Word2Vec([tokens], window = 5, **params)
model20 = Word2Vec([tokens], window = 20, **params)
model5.save(model_window_5_file)
model20.save(model_window_20_file)

# Similiarities
sample_queries = ['one', 'flaw', 'reason']
for query in sample_queries:
	results = model5.most_similar(query)[:3]
	print('Results for query', query, ':', results)

# Visualization
visualize(model5, 'Study in scarlett, window=5, no split', 'model5.png')
visualize(model5, 'Study in scarlett, window=20, no split', 'model20.png')