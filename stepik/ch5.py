import re
from summa import summarizer

with open('ch5.json', 'r') as file:
	texts = re.split("\",", file.read())

sums = []
for text in texts:
	summ = summarizer.summarize(text.replace("\n", "").replace("\"", ""), words=30)
	print(summ)
	sums.append(summ)