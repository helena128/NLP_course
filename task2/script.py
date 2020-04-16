from nltk.tokenize import sent_tokenize, word_tokenize
from numpy import array_split

file_path = "/home/helena/Documents/NLP/data/study_in_scarlet.txt"
num_of_sentences = 30

# Pos index structure: {word: {doc: [po1, pos2]}}
def build_positional_index(documents):
	positional_index_dict = {}
	for doc_id in range(len(documents)):
		for word_id, word in enumerate(word_tokenize(documents[doc_id])):
			if str(word) not in positional_index_dict:
				positional_index_dict[str(word)] = {}
			if doc_id not in positional_index_dict[word]:
				positional_index_dict[word][doc_id] = []
			positional_index_dict[word][doc_id].append(word_id)
	return positional_index_dict

# search function
def search(search_query, documents, positional_index_dict):
	#print('Searching for: ', search_query)
	search_query_tokens = word_tokenize(str(search_query))

	for token in search_query_tokens:
		if token not in positional_index_dict:
			print('Token <', token, '> was not found in dict')
			return []

	result_docs = []
	first_token = search_query_tokens[0]

	for doc_id in range(len(documents)):
		# If first token exists in positional index for current doc
		if doc_id in positional_index_dict[first_token]:
			for ft_pos in positional_index_dict[first_token][doc_id]:
				flag = True
				for inc, token in enumerate(search_query_tokens[1:], start=1):
					#print(doc_id, ' ', ft_pos, inc, token)
					if doc_id not in positional_index_dict[token] or (ft_pos + inc) not in positional_index_dict[token][doc_id]:
						flag = False
						break
				if flag:
					result_docs.append((doc_id, ft_pos))
	return result_docs

# Read file
file = open(file_path, 'r')
text = file.read()

# Tokenize into sentences
sentences = sent_tokenize(text)
#print(type(sentences), sentences[:3])

# Split - create docs
documents = ['\n'.join(sentences[x: x + num_of_sentences]) for x in range(0, len(sentences), num_of_sentences)]

#print('Num of docs: ', len(documents))
#print('1st doc: ', documents[0])

# Create positional index
positional_index_dict = build_positional_index(documents)

# Search
print(search('Indian possessions', documents, positional_index_dict))
print(search('No res', documents, positional_index_dict))