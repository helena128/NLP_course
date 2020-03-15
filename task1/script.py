from nltk.corpus import webtext, stopwords
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk import Text, FreqDist
from functools import reduce
import operator
import string
#from nltk.book import text1
from nltk.corpus import gutenberg

num_of_words_to_plot = 20
num_of_words_compare = 50
file_path = "/home/helena/Documents/NLP/data/study_in_scarlet.txt"
moby_file_name = 'melville-moby_dick.txt'

# Read file
file = open(file_path, 'r')
raw_text = file.read()

# Word and sentence tokenization
tokenized_sentences = sent_tokenize(webtext.raw(file_path))
#tokenized_words = reduce(operator.concat, [word_tokenize(s) for s in tokenized_sentences])

tokenizer = RegexpTokenizer(r'\w+')

stop = stopwords.words('english') + list(string.punctuation)
#raw_tokens = word_tokenize(webtext.raw(file_path).lower())
raw_tokens = tokenizer.tokenize(webtext.raw(file_path).lower())
tokens = [i for i in raw_tokens if i not in stop]
#print(tokenized_sentences[20])
#print(tokenized_words[20], tokenized_words[21])

# Convert to nltk text
text = Text(tokens)

# Freq dist
fdist = FreqDist(text)
fdist.plot(num_of_words_to_plot, cumulative = False)
scarlet_commons = [word for word, counts in fdist.most_common(num_of_words_compare)]
print('Most common words for Study in Scarlet:\n', fdist.most_common(num_of_words_to_plot), '\n\n')

# Moby Dick frequencies
moby_raw_text = gutenberg.raw(moby_file_name)
moby_tokens = tokenizer.tokenize(moby_raw_text.lower())
moby_text = Text([w for w in moby_tokens if w not in stop])
fdist_moby = FreqDist(moby_text)
moby_commons = [word for word, counts in fdist_moby.most_common(num_of_words_compare)]
print('Most common words for Moby Dick:\n', fdist_moby.most_common(num_of_words_compare))

# Frequencies comparison
## In scarlet but not in moby
diff_scarlet_vs_moby = [word for word in scarlet_commons if word not in moby_commons]
print('In Study in scarlet, but not in Moby Dick: ', ', '.join(diff_scarlet_vs_moby))

## In scarlet but not in moby
diff_moby_vs_scarlet = [word for word in moby_commons if  word not in scarlet_commons]
print('In Moby Dick, but not in Study In Scarlet: ', ', '.join(diff_moby_vs_scarlet))