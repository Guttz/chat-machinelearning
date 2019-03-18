# Import dependencies
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from sklearn.externals import joblib
import traceback
import math
import pickle
from flask_cors import CORS, cross_origin 
from flask import Flask, make_response, request, current_app
import os 
import csv
import json


# Your API definition

app = Flask(__name__)

CORS(app, resources=r'*')

port = int(os.getenv('PORT', 8080)) 

@app.route('/Portfolio', methods=['GET'])

def portfolio():
	try:
		df_ = pd.read_csv(r"port.csv")
		df_= df_.to_dict('dict')
		df_ = json.dumps(df_)
		df_json = json.loads(df_)
		return jsonify({'Portfolio': df_json})
	except:
		return jsonify({'trace': traceback.format_exc()})
		
    		

@app.route('/predict', methods=['POST'])

def predict():
	try:

		from sklearn import preprocessing
		json_ = request.json
		if json_["customer"]== "Gus":
			df = pd.read_csv(r"data1.csv")
		elif json_["customer"]== "Leo":
			df = pd.read_csv(r"data2.csv")
		else:
			df = pd.read_csv(r"data3.csv")		

		le = preprocessing.LabelEncoder()
		le.fit(df['Product'])
		list(le.classes_)
		df["Product"]= pd.Series(list(le.transform(df["Product"]))) 
		dependent_variable = 'Product'
		y = df[dependent_variable]
		#Get list of unique items
		itemList=list(set(df["Product"].tolist()))

		#Get count of users
		userCount=len(set(df["Customer"].tolist()))

		#Create an empty data frame to store item affinity scores for items.
		itemAffinity= pd.DataFrame(columns=('item1', 'item2', 'score'))
		rowCount=0
		#For each item in the list, compare with other items.
		for ind1 in range(len(itemList)):
			#Get list of users who bought this item 1.
			item1Users = df[df.Product==itemList[ind1]]["Customer"].tolist()
    		#print("Item 1 ", item1Users)
    
    		#Get item 2 - items that are not item 1 or those that are not analyzed already.
			for ind2 in range(ind1, len(itemList)):
        
				if (ind1 == ind2):
					continue
            		#Get list of users who bought item 2
				item2Users=df[df.Product==itemList[ind2]]["Customer"].tolist()
        		#print("Item 2",item2Users)
        
        		#Find score. Find the common list of users and divide it by the total users.
				commonUsers= len(set(item1Users).intersection(set(item2Users)))
				score=commonUsers / userCount

        		#Add a score for item 1, item 2
				itemAffinity.loc[rowCount] = [itemList[ind1],itemList[ind2],score]
				rowCount +=1
				#Add a score for item2, item 1. The same score would apply irrespective of the sequence.
				itemAffinity.loc[rowCount] = [itemList[ind2],itemList[ind1],score]
				rowCount +=1
        
#Check final result
#itemAffinity.head()
		#json_ = request.json
		#print(json_)
		query = pd.DataFrame([json_])
		query = query.reindex(fill_value=0)
		searchItem= query["product"].iloc[0]
		if searchItem=="beer":
			searchItem=0
		elif searchItem=="chips":
			searchItem=1
		elif searchItem=="chocolate":
			searchItem=2
		elif searchItem=="coffee":
			searchItem=3
		elif searchItem=="coke":
			searchItem=4

		recoList=itemAffinity[itemAffinity.item1==searchItem]\
        [["item2","score"]]\
        .sort_values("score", ascending=[0])
		json_ = request.json
		if json_["customer"]== "Gus":
			dic = {0.0:"beer",1.0:"chips",2.0:"chocolate",3.0:"coffee",4.0:"coke"}
		elif json_["customer"]== "Leo":
			dic = {1.0:"beer",0.0:"chips",3.0:"chocolate",2.0:"coffee",4.0:"coke"}
		else:
			dic = {0.0:"beer",3.0:"chips",4.0:"chocolate",1.0:"coffee",2.0:"coke"}

	

		recoList= [dic.get(n, n) for n in recoList.item2]
        		
        				
		#recoList= recoList.to_json()
		return jsonify({"Recommendations": recoList})
        #print("Recommendations for item \n", recoList)
	except:
		return jsonify({'trace': traceback.format_exc()})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port, debug=False)
	#app.run(debug=True)

