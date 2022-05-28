#Importing the Libraries

#flask is use for run the web application.
import flask
#import newspaper3k
#request is use for accessing file which was uploaded by the user on our application.
from flask import Flask, request,render_template 
from flask_cors import CORS

#Python pickle module is used for serializing
# and de-serializing a Python object structure.
import pickle      



import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "UqKC_K9ox9COEdiL0JxjLV-fr5T0qVXA0FX6b1KmQOD4"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}

#response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/2645d777-d20d-442e-bdd4-a51ac7783587/predictions?version=2022-03-07', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
#print("Scoring response")
#print(response_scoring.json())

#OS module in python provides functions for interacting with the operating system
import os

#Newspaper is used for extracting and parsing newspaper articles.
#For extracting all the useful text from a website.
from newspaper import Article
#import Article
#URLlib is use for the urlopen function and is able to fetch URLs.
#This module helps to define functions and classes to open URLs 
import urllib

#Loading Flask and assigning the model variable
app = Flask(__name__)
CORS(app)
app=flask.Flask(__name__,template_folder='templates')

with open('model.pkl', 'rb') as handle:
    model = pickle.load(handle)
#@app.route('/') # rendering the html template
#def home():
  #  return render_template("home.html")
#@app.route('/predict') # rendering the html template
#def main() :
  #  return render_template("main.html")
@app.route('/') #default route
def main():
    return render_template('main.html')

#Receiving the input url from the user and using Web Scrapping to extract the news content

#Route for prediction

@app.route('/predict',methods=['GET','POST'])


def predict():
	#Contains the incoming request data as string in case.	
    url =request.get_data(as_text=True)[5:]
	
	#The URL parsing functions focus on splitting a URL string into its components, 
	#or on combining URL components into a URL string.
    url = urllib.parse.unquote(url)
	
	#A new article come from Url and convert onto string
    article = Article(str(url))	
	
	#To download the article 
    article.download()
	
	#To parse the article 
    article.parse()
	
	#To perform natural language processing ie..nlp
    #article.nlp()
	#To extract summary 
    news = article.summary
    print(type(news))

    #Passing the news article to the model and returing whether it is Fake or Real
   # pred = model.predict([news])

   # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ['FAKE'], "values": [news]}]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/2645d777-d20d-442e-bdd4-a51ac7783587/predictions?version=2022-03-07', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    pred=response_scoring.json()
    print(pred)
    return render_template('main.html', prediction_text='The news is "{}"'.format(pred[0]))
    
if __name__=="__main__":
    port=int(os.environ.get('PORT',5000))
    app.run(port=port,debug=True,use_reloader=False)