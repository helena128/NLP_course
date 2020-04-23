def precision_at_k(model, pos, neg, k, expectations, log=True):
	similar = model.wv.most_similar(
                           positive=pos,
                           negative=neg,
                           topn=k)
	results = list(map(lambda x: x[0], similar))
	corr_found_cnt = len(set(expectations).intersection(set(results)))
	precision = corr_found_cnt / len(results)
	if log:
		print("Positive:", pos, "negative:", neg, "precision", precision)
	return precision
	#print("Results:", results)
