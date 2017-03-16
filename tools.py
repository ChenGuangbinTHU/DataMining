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
	result = re.split('[ ,\n\.;\?:!\()"]?',fd.read())
	for word in result :
		if word == '':
			continue
		if(len(word) > 1):
			word = getWord(word)
		if(word not in wordDict):
			wordDict[word] = 1
		else:
			wordDict[word] += 1
	return len(result),wordDict

def calcIdf(IdfDict,wordDict):
	for word in wordDict:
		if word in IdfDict:
			IdfDict[word] += 1
		else:
			IdfDict[word] = 1
	return IdfDict

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
		docLen,wordDictPerDoc = pretreat(str(i)) #get document's length and its wordDict

		#update togetherMatrix and IdfDict for each document
		togetherMatrix = calcTogetherMatrix(togetherMatrix,wordDictPerDoc)
		IdfDict = calcIdf(IdfDict,wordDictPerDoc)
		
		#get tf
		for word in wordDictPerDoc :
			wordDictPerDoc[word] /= docLen
		tfIdfDict[str(i)] = wordDictPerDoc

	#get idf
	for docName in tfIdfDict:
		for word in tfIdfDict[docName] :
			tfIdfDict[docName][word] *= math.log(300/IdfDict[word],10)

	return tfIdfDict,togetherMatrix,IdfDict.keys()

#Euclid distance
def calcDistanceForDoc(docToCalc,tfIdfDoc,allWords) :
	dis = 0
	for word in allWords:
		minus = 0
		if word in docToCalc and word in tfIdfDoc:
			minus = docToCalc[word] - tfIdfDoc[word]
		elif word in docToCalc and word not in tfIdfDoc:
			minus = docToCalc[word]
		elif word not in docToCalc and word in tfIdfDoc:
			minus = tfIdfDoc[word]
		else:
			minus = 0
		dis += minus * minus
	return dis

def calcTop5Doc(docToCalc,tfIdfDict,docToCalcName,allWords):
	l = []
	
	for i in range(0,300):
		if str(i) == docToCalcName:
			continue
		dis = calcDistanceForDoc(tfIdfDict[docToCalc],tfIdfDict[str(i)],allWords)
		l.append([str(i),dis])
	Top5 = heapq.nsmallest(5, l, key=lambda s: s[1])
	print(Top5)

#Euclid distance
def calcDistanceForVoc(target,compared,allWords):
	dis = 0
	for word in allWords:
		minus = 0
		if word in target and word in compared:
			minus = target[word] - compared[word]
		elif word in target and word not in compared:
			minus = target[word]
		elif word not in target and word in compared:
			minus = compared[word]
		else:
			minus = 0
		dis += minus*minus
	return dis

def calcTop5Voc(target,togetherMatrix,allWords):
	target = target.lower()

	#most common words need to be removed
	c = ["the","a","of","and","or",'was','in','at','to','by','on','s','from',
				'his','as','an','is','','he','she','for','with','that','will','all','one','after',
				'they','their','had','have','just','be','not','her','m','we','has','but','said',
				'say','are','it','this','may','mr','were','also','been','up','one','two','three','new',
				'york','which','-','who','when','about','him','i','there','out','more','under','name']
	

	if target not in togetherMatrix:
		print(target + " not exist")
		return
	l = []
	for compareWord in togetherMatrix:
		if compareWord == target:
			continue
		dis = calcDistanceForVoc(togetherMatrix[target],togetherMatrix[compareWord],allWords)
		l.append([compareWord,dis])
	l = sorted(l,key = lambda s : s[1])
	i = 0
	count = 0
	
	#if word not in c
	if target not in c:
		while(count < 5):
			if l[i][0] not in c:
				print(l[i])
				count += 1
			i += 1
	else:
		for i in range(0,5):
			print(l[i])


