#!/usr/bin/python
#coding = UFT-8
import re
import math
import heapq

def getWord(word):
	word = word.lower()
	if(word[0] == "-"):
		return word[1:len(word)]
	elif(word[0:2] == "\'\'"):
		return word[2:len(word)]
	elif(word[len(word)-2:len(word)] == '\'s'):
		return word[0:len(word)-2]
	else:
		return word



def pretreat(documentName) :
	result=[]
	wordDict = {}
	fd = open(documentName, "r" )
	result = re.split('[ ,\n\.;\?:!\()"]?',fd.read())#- need to condider
	for word in result :
		#print(word)
		if word == '':
			continue
		if(len(word) > 1):
			word = getWord(word)
		'''
		if(len(word) > 1):
			wordRe = re.findall(r"^[$(\w].*[)%\w]$",word)
			if(wordRe):
				word = wordRe[0]
			else:
				print("syntax error word:" + word)
		'''
		if(word not in wordDict):
			wordDict[word] = 1
		else:
			wordDict[word] += 1
	#print(wordDict.keys())
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
				togetherMatrix[word1][word2] = 1
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

	for docName in tfIdfDict:
		for word in tfIdfDict[docName] :
			tfIdfDict[docName][word] *= math.log(300/IdfDict[word],10)

	return tfIdfDict,togetherMatrix,IdfDict.keys()
	# for docName in tfIdfDict:
	# 	print(docName)
	# 	print(tfIdfDict[docName])
	# 	print('\n\n')

	# f = open('test.txt', 'w')
	# for item in IdfDict :
	# 	f.write(item + ":" + str(IdfDict[item]) + '\n')
	# f.close()

def calcDistance(docToCalc,tfIdfDoc,allWords) :
	dis = 0
	c = ["the","a","of","and","or",'in','at','to','by','on','s','from',
				'as','an','is','','he','she','for','with','that','after',
				'they','their','had','have','just','be','her','m','we','has','but'
				,'are','it','this','were','also','been','new']
	for word in allWords:
		if word in c:
			continue
		if word in docToCalc and word in tfIdfDoc:
			minus = docToCalc[word] - tfIdfDoc[word]
			dis += minus*minus
		elif word in docToCalc and word not in tfIdfDoc:
			minus = docToCalc[word]
			dis += minus*minus
		elif word not in docToCalc and word in tfIdfDoc:
			minus = tfIdfDoc[word]
			dis += minus*minus
		else:
			dis += 0
	return dis

def calcTop5Doc(docToCalc,tfIdfDict,docToCalcName,allWords):
	l = []
	
	for i in range(0,300):
		if str(i) == docToCalcName:
			continue
		dis = calcDistance(tfIdfDict[docToCalc],tfIdfDict[str(i)],allWords)
		l.append([str(i),dis])
	Top5 = heapq.nsmallest(5, l, key=lambda s: s[1])
	# for item in Top5:
	# 	file.write(item[0] + " ")
	# 	file.write('\n')
	print(Top5)

def calcTop5Voc(target,togetherMatrix):
	target = target.lower()
	common = ["the","a","of","and","or",'was','in','at','to','by','on','s','from',
				'his','as','an','is','','he','she','for','with','that','will','all','one','after',
				'they','their','had','have','just','be','not','her','m','we','has','but','said',
				'say','are','it','this','may','mr','were','also','been','up','one','two','three','new',
				'york','which','-','who','when','about','him','i','there','out','more','under']
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
	file = open('test2.txt','w')
	tfIdfDict,togetherMatrix,allWords = buildTfIdfDict()
	for i in range(0,300):
		print(i)
		file.write(str(i) + '\'th doc is familiar with')
		file.write('\n')
		calcTop5Doc(str(i),tfIdfDict,str(i),allWords)
	# for i in range(0,1):
	# 	pretreat(str(i))
