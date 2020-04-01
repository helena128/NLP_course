from nltk.tokenize import sent_tokenize, word_tokenize
from numpy import array_split

file_path = "/home/helena/Documents/NLP/data/study_in_scarlet.txt"
num_of_sentences = 30
'''
def build_positional_index(positional_index_dict, documents):
	for doc_id in range(len(documents)):
		for word_id, word in enumerate(word_tokenize(documents[doc_id])):
			if str(word) not in positional_index_dict:
				positional_index_dict[str(word)] = {}
			if doc_id not in positional_index_dict[word]:
				positional_index_dict[word][doc_id] = []
			positional_index_dict[word][doc_id].append(word_id)
'''
'''
def search(search_query, positional_index_dict):
	print('Searching for: ', search_query)
	search_query_tokens = word_tokenize(str(search_query))
	result_docs = []
	res_for_curr_doc = {}
	for doc_id in range(len(positional_index_dict)):
		for token_id in range(len(search_query_tokens)):
			token = search_query_tokens[token_id]
			if search_query_tokens[token] in positional_index_dict:
				res_for_curr_doc[token] = search_query_tokens[token] 
			else: break
			if token_id > 0 and bool(res_for_curr_doc[search_query_tokens[token_id - 1]]):
				break
			if token_id == len(search_query_tokens) - 1:
				res_for_curr_doc.append(doc_id)
	print('Doc Ids: ', result_docs)
'''

# Read file
file = open(file_path, 'r')
text = file.read()

# Tokenize into sentences
sentences = sent_tokenize(text)
print(type(sentences))

# Split - create docs
documents = []
curr_doc = []
for sent_id in range(1, len(sentences)):
	if sent_id % num_of_sentences == 1:
		curr_doc = []
		continue
	if sent_id % num_of_sentences == 0:
		documents.append(''.join(curr_doc))
		continue
	else:
		curr_sent = sentences[sent_id]
		curr_doc.append[curr_sent]

print('Num of docs: ', len(documents))

# Create positional index
positional_index_dict = {}
#build_positional_index(positional_index_dict, documents)

# Search
'''
search('STUDY IN', positional_index_dict)
search('No res', positional_index_dict)
'''