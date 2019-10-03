import pandas as pd
import os
import json
from collections import OrderedDict

def FilterFiles(files):
	Files = []
	for file in files:
		if file[-4:] == "json":
			Files.append(file)
	return Files

def ProcessUser(data):
	#records = []
	for test in data['tests']:
		record = OrderedDict()
		record['surname'] = data['surname']
		record['first_name'] = data['first_name']
		record['topic'] = test['topic']
		record['score'] = test['score']
		BigMatrix.append(record)
	#return records
def CreateStat(class_n):
	try:
		os.system("rm *.xlsx")
	except:
		pass
	file_names = FilterFiles(os.listdir("classes_info/class_" + str(class_n)))
	global BigMatrix
	BigMatrix = []
	for file in file_names:
		f = open("classes_info/class_" + str(class_n)+"/"+file)
		data = json.load(f)
		ProcessUser(data)
		f.close()
	#print(BigMatrix)
	df = pd.DataFrame(BigMatrix)
	print(df)
	fname = "class_"+str(class_n)+".xlsx"
	df.to_excel(fname)
	return 0
#CreateStat(8)