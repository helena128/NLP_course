from spacy import displacy
import spacy
from spacy.matcher import Matcher

# used relation Band - album
docs = [
	"In 1979 Dave Marsh panned Jazz as more of the same dull pastiche from Queen",
	"Fallen is the debut studio album by American rock band Evanescence.",
	"Phobia is the third album by Breaking Benjamin."
]

# Merge entitites, e.g. "Breaking", "Benjamin" -> "Breaking Benjamin"
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe(nlp.create_pipe("merge_entities"))

spacified_docs = list(map(nlp, docs))
#displacy.serve(spacified_docs[0], style="dep")

# Create patterns
band_pattern = { 	'POS': 'PROPN',
					'DEP': {'IN': ['pobj', 'dobj', 'pcomp']}}
album_pattern = { 	'POS': {'IN': ['PROPN', 'VERB']},
					'DEP': {'IN': ['dobj', 'nsubj']},
					'LOWER': {'IN': ['fallen', 'jazz', 'phobia']}}
patterns = [
	# Queen
	[
		album_pattern,
		{'DEP': 'dobj'},
		{'OP': '*'},
		{'POS': 'NOUN'},  # pastiche
		{'POS': 'ADP'}, # from
		band_pattern
	],

	# Evanescence
	[
		album_pattern,
		{'DEP': 'dobj'},
		{'POS': 'AUX'},
		{'POS': 'NOUN', 'OP': '?'},
		{'POS': 'ADP'},
		band_pattern
	],

	# Breaking benjamin
	[
		album_pattern,
		{'DEP': 'nsubj'},
		{'POS': 'AUX'},
		{'POS': 'NOUN', 'OP': '?'},
		band_pattern
	]
]

def find_pl(doc):
  matcher = Matcher(nlp.vocab)
  matcher.add('ProgLangCreator', patterns)

  def print_match(lang, person, span):
      print("""{}: {}. Source: {}""".format(lang, person, span))

  for (_, a, b) in matcher(doc):
    if doc[a].text.lower() in languages:
        print_match(doc[a], doc[b-1], doc[a:b].text)
    elif doc[a].text.lower() == 'valim':
        print_match(doc[b-1], doc[a-1:a+1], doc[a:b].text)
    else:
        print_match(doc[b-1], doc[a], doc[a:b].text)

  return doc

nlp.add_pipe(find_pl, 'find_pl', last=True)

print(list(map(nlp, docs)))