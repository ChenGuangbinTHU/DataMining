#!/usr/bin/python
#coding = UFT-8
import re
import math

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

def buildTfIdfDict() :
	IdfDict = {}
	tfIdfDict = {}
	for i in range(0,300):
		docLen,wordDictPerDoc = pretreat(str(i))
		#print(str(i) + ":" + str(docLen))
		IdfDict = calcIdf(IdfDict,wordDictPerDoc)
		for word in wordDictPerDoc :
			wordDictPerDoc[word] /= docLen
		tfIdfDict[str(i)] = wordDictPerDoc

	for docName in tfIdfDict:
		for word in tfIdfDict[docName] :
			tfIdfDict[docName][word] *= math.log(300/IdfDict[word],10)
	# for docName in tfIdfDict:
	# 	print(docName)
	# 	print(tfIdfDict[docName])
	# 	print('\n\n')

	# f = open('test.txt', 'w')
	# for item in IdfDict :
	# 	f.write(item + ":" + str(IdfDict[item]) + '\n')
	# f.close()

if __name__ == '__main__':
	buildTfIdfDict()
