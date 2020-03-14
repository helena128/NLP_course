from nltk.tokenize import sent_tokenize
from numpy import array_split

file_path = "/home/helena/Documents/NLP/data/study_in_scarlet.txt"
num_of_sentences = 30

# Read file
file = open(file_path, 'r')
text = file.read()

# Tokenize into sentences
sentences = sent_tokenize(text)
#print(sentences[0])

# Split - create docs
documents = array_split(sentences, num_of_sentences)
#print(documents[1])