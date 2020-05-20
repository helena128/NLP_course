import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.manifold import TSNE
import numpy as np

def tsne_plot_2d(label, embeddings, pic_name, words=[], a=1):
    plt.figure(figsize=(16, 9))
    colors = cm.rainbow(np.linspace(0, 1, 1))
    x = embeddings[:,0]
    y = embeddings[:,1]
    plt.scatter(x, y, c=colors, alpha=a, label=label)
    for i, word in enumerate(words):
        plt.annotate(word, alpha=0.3, xy=(x[i], y[i]), xytext=(5, 2), 
                     textcoords='offset points', ha='right', va='bottom', size=10)
    plt.legend(loc=4)
    plt.grid(True)
    plt.savefig(pic_name, format='png', dpi=150, bbox_inches='tight')
    plt.show()

def visualize(model, label, pic_name):
	# Visualization
	words = []
	embeddings = []
	for word in list(model.wv.vocab):
	    embeddings.append(model.wv[word])
	    words.append(word)
	    
	tsne_2d = TSNE(perplexity=30, n_components=2, init='pca', n_iter=3500, random_state=32)
	embeddings_2d = tsne_2d.fit_transform(embeddings)
	tsne_plot_2d(label, embeddings_2d, pic_name, a=0.1)

def plot_simple_graph(name, x, y):
	plt.clf()
	plt.scatter(x, y, label="Window vs precision")
	plt.savefig(name, format='png', dpi=150, bbox_inches='tight')