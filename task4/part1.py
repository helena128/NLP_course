from spacy import displacy
import spacy
from spacy.matcher import Matcher
import re


nlp = spacy.load("en_core_web_lg")
nlp.add_pipe(nlp.create_pipe("merge_entities"))

# used relation: writer - book
docs = [
	"""Anna Karenina is a novel by the Russian author Leo Tolstoy, first published in book form in 1878. Many writers consider Anna Karenina the greatest work of literature ever[2] and Tolstoy himself called it his first true novel. It was initially released in serial installments from 1873 to 1877 in the periodical The Russian Messenger.
	   A complex novel in eight parts, with more than a dozen major characters, it is spread over more than 800 pages (depending on the translation and publisher), typically contained in two volumes. It deals with themes of betrayal, faith, family, marriage, Imperial Russian society, desire, and rural vs. city life. The plot centers on an extramarital affair between Anna and dashing cavalry officer Count Alexei Kirillovich Vronsky that scandalizes the social circles of Saint Petersburg and forces the young lovers to flee to Italy in a search for happiness. Returning to Russia, their lives further unravel.
       Trains are a recurring motif throughout the novel, which takes place against the backdrop of rapid transformations as a result of the liberal reforms initiated by Emperor Alexander II of Russia, with several major plot points taking place either on passenger trains or at stations in Saint Petersburg or elsewhere in Russia. The novel has been adapted into various media including theatre, opera, film, television, ballet, figure skating, and radio drama. The first of many film adaptations was released in 1911 but has not survived.
	""",
	"""Jane Eyre is a novel by English writer Charlotte Bronte, published under the pen name "Currer Bell", on 16 October 1847, by Smith, Elder & Co. of London. The first American edition was published the following year by Harper & Brothers of New York.[1] Jane Eyre follows the experiences of its eponymous heroine, including her growth to adulthood and her love for Mr. Rochester, the brooding master of Thornfield Hall.[2]
		The novel revolutionised prose fiction by being the first to focus on its protagonist's moral and spiritual development through an intimate first-person narrative, where actions and events are coloured by a psychological intensity. Charlotte Brontë has been called the "first historian of the private consciousness", and the literary ancestor of writers like Proust and Joyce.[3]
		The book contains elements of social criticism, with a strong sense of Christian morality at its core, and is considered by many to be ahead of its time because of Jane's individualistic character and how the novel approaches the topics of class, sexuality, religion and feminism.[4][5] It, along with Jane Austen's Pride and Prejudice, is one of the most famous romance novels of all time.[6]
	""",
	"""Dracula is an 1897 Gothic horror novel by Irish author Bram Stoker. It introduced the character of Count Dracula and established many conventions of subsequent vampire fantasy.[1] The novel tells the story of Dracula's attempt to move from Transylvania to England so that he may find new blood and spread the undead curse, and of the battle between Dracula and a small group of people led by Professor Abraham Van Helsing.
	Dracula has been assigned to many literary genres including vampire literature, horror fiction, gothic fiction, and invasion literature. The novel has spawned numerous theatrical, film, and television interpretations.
	"""
]

# remove all citation numbers
for doc in docs:
	doc = re.sub(r"[\(\[].*?[\)\]]", "", doc)

''' Display dependencies
spacifier_doc = nlp(docs[2])
displacy.serve(spacifier_doc, style = "dep")
'''

books = ['anna karenina', 'jane eyre', 'dracula']

book_pattern = 	{ 	'POS': 'PROPN', 
					'DEP': 'nsubj',
					'LOWER': {'IN': books}
				}

author_pattern = 	{ 	'POS': 'PROPN', 
						'DEP': {'IN': ['appos', 'pobj']}
					}

patterns = [

	# anna karenina
	[
		book_pattern,
		{'POS': 'AUX'} , #is
		{'POS': 'DET', 'DEP': 'det'}, # a
		{'POS': 'NOUN', 'DEP': 'attr'}, # novel
		{'POS': 'ADP', 'DEP': 'prep'}, # by
		{'POS': 'DET', 'DEP': 'det'}, # the
		{'POS': 'ADJ', 'DEP': 'amod'}, # Russian
		{'POS': 'NOUN', 'DEP': 'pobj'}, # author
		author_pattern
	],

	# jane eyre
	[
		book_pattern,
		{'POS': 'AUX'} , #is
		{'POS': 'DET', 'DEP': 'det'}, # a
		{'POS': 'NOUN', 'DEP': 'attr'}, # novel
		{'POS': 'ADP', 'DEP': 'prep'}, # by
		{'POS': 'ADJ', 'DEP': 'compound'}, # English
		{'POS': 'NOUN', 'DEP': 'compound'}, # writer
		author_pattern
	],

	# dracula
	[
		book_pattern,
		{'POS': 'AUX'} , # is
		{'POS': 'DET', 'DEP': 'det'}, # an
		{'POS': 'NUM', 'DEP': 'nummod'}, # 1897
		{'POS': 'ADJ', 'DEP': 'amod'}, # Gothic
		{'POS': 'NOUN', 'DEP': 'compound'}, # horror
		{'POS': 'NOUN', 'DEP': 'attr'}, # novel
		{'POS': 'ADP', 'DEP': 'prep'}, # by
		{'POS': 'ADJ', 'DEP': 'amod'}, # Irish
		{'POS': 'NOUN', 'DEP': 'compound'}, # author
		author_pattern
	]
]

def print_match(book, person, span):
	print("""> Processing: {}""".format(span))
	print(""">> Book: {},\tAuthor: {}.""".format(book, person))

def find_author(doc):
	matcher = Matcher(nlp.vocab, validate=True)
	matcher.add('AuthorBookMatcher', patterns)

	for (_, a, b) in matcher(doc):
		#print(doc[a:b].text)
		if doc[a].text.lower() in books:
			print_match(doc[a], doc[b-1], doc[a:b].text)
		else: # jic author comes first
			print_match(doc[b-1], doc[a], doc[a:b].text)

	return doc

nlp.add_pipe(find_author, 'find_author', last=True)

#list(map(nlp, docs))
list(nlp.pipe(docs))