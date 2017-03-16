import tools

if __name__ == '__main__':
	tfIdfDict,togetherMatrix,allWords = tools.buildTfIdfDict()
	while True:
		s = input("input 1 or 2 to choose what to find:\n1:similar document\n2:similar vocubulary\n")
		if s == "1":
			docName = input("Document Name:")
			tools.calcTop5Doc(docName,tfIdfDict,docName,allWords)
		if s == "2":
			voc = input("vocabulary:")
			tools.calcTop5Voc(voc,togetherMatrix)
