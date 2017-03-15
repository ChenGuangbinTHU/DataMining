#!/usr/bin/python
#coding = UFT-8
import re
import math
import heapq

def pretreat(documentName) :
	result=[]
	wordDict = {}
	fd = open(documentName, "r" )
	result = re.split('[ ,\n\.\';\?:!/-]?',fd.read())#- need to condider
	for word in result :
		#print(word)
		if(len(word) > 1):
			wordRe = re.findall(r"^[$(\w].*[)%\w]$",word)
			if(wordRe):
				word = wordRe[0]
			else:
				print("syntax error word:" + word)
		if(word not in wordDict):
			wordDict[word] = 1
		else:
			wordDict[word] += 1
	return len(result),wordDict
	# for item in wordDict:
	# 	print(item + ':' + str(wordDict[item]))
	# print(len(wordDict))

def calcIdf(IdfDict,wordDict):
	for word in wordDict:
		if word in IdfDict:
			IdfDict[word] += 1
		else:
			IdfDict[word] = 1
	return IdfDict

#注意C[I,J]和C[J,I]
def calcTogetherMatrix(togetherMatrix,wordDict): 
	for word1 in wordDict:
		word1 = word1.lower()
		if word1 not in togetherMatrix:
			togetherMatrix[word1] = {}
		for word2 in wordDict:
			word2 = word2.lower()
			if word1 == word2:
				continue
			if word2 not in togetherMatrix[word1]:
				togetherMatrix[word1][word2] = 0
			else:
				togetherMatrix[word1][word2] += 1
	return togetherMatrix


def buildTfIdfDict() :
	IdfDict = {}
	tfIdfDict = {}
	togetherMatrix = {}
	for i in range(0,300):
		docLen,wordDictPerDoc = pretreat(str(i))
		#print(str(i) + ":" + str(docLen))
		calcTogetherMatrix(togetherMatrix,wordDictPerDoc)
		IdfDict = calcIdf(IdfDict,wordDictPerDoc)
		for word in wordDictPerDoc :
			wordDictPerDoc[word] /= docLen
		tfIdfDict[str(i)] = wordDictPerDoc

	# f = open('test1.txt', 'w')
	# for item in togetherMatrix :
	# 	for i in togetherMatrix[item]:
	# 		f.write("[" + item + "]" + "[" + i + "]" + ":" + str(togetherMatrix[item][i]) + '\n')
	# f.close()

	# for docName in tfIdfDict:
	# 	for word in tfIdfDict[docName] :
	# 		tfIdfDict[docName][word] *= math.log(300/IdfDict[word],10)

	return tfIdfDict,togetherMatrix
	# for docName in tfIdfDict:
	# 	print(docName)
	# 	print(tfIdfDict[docName])
	# 	print('\n\n')

	# f = open('test.txt', 'w')
	# for item in IdfDict :
	# 	f.write(item + ":" + str(IdfDict[item]) + '\n')
	# f.close()

def calcDistance(docToCalc,tfIdfDoc) :
	dis = 0
	for word in docToCalc:
		if word in tfIdfDoc:
			dis += tfIdfDoc[word]
	return dis

def calcTop5Doc(docToCalc,tfIdfDoc,docToCalcName):
	l = []
	for i in range(0,300):
		if str(i) == docToCalcName:
			continue
		dis = calcDistance(docToCalc,tfIdfDict[str(i)])
		l.append([str(i),dis])
	Top5 = heapq.nlargest(5, l, key=lambda s: s[1])
	print(Top5)

def calcTop5Voc(target,togetherMatrix):
	target = target.lower()
	common = ["the","a","of","and","or",'was','in','at','to','by','on','s','from',
				'his','as','an','is','','he','she','for','with','that','will','all','one','after',
				'they','their','had','have','just','be','not','her','m','we','has','but','said',
				'say','are','it']
	if target not in togetherMatrix:
		print(target + " not exist")
		return
	dict = sorted(togetherMatrix[target].items(), key=lambda d:d[1], reverse = True)
	count = 0;
	i = 0;
	if target not in common:
		while count < 5:
			if dict[i][0].lower() not in common:
				print(dict[i])
				count += 1
			i += 1
	else:
		n = 5
		while i < n:
			print(i)
			if dict[i][0] == '':
				n += 1
				print("n=" + str(n))
			else:
				print(dict[i])
			i += 1
	#Top5 = heapq.nlargest(5, list(togetherMatrix[target]), key=lambda s: s[1])
	#print(Top5)


if __name__ == '__main__':
	tfIdfDict,togetherMatrix = buildTfIdfDict()
	calcTop5Voc("volleyball",togetherMatrix)
		#calcTop5Doc(tfIdfDict[str(i)],tfIdfDict,str(i))
