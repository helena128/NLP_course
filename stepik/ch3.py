import math

v = 1500 # number of unique words
unigram_freq = [10000, 100, 1, 5000, 3000, 50]
bigram_freq = [20, 0, 0, 300, 15, 5]

probab_array = []
result_prob = 1

for i in range(len(bigram_freq)):
	prob = (bigram_freq[i] + 1)/(unigram_freq[i] + v)
	result_prob *= prob

print('Result prob: ', result_prob)
print('Log: ', math.log(result_prob))
