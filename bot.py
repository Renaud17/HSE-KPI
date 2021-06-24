import streamlit as st
import pandas as pd
import nltk
import numpy as np
import string
import warnings
import requests
import pickle
import random

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import json
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import GridSearchCV
from responses import *
# Lemmitization

lemmer = nltk.stem.WordNetLemmatizer()

@st.cache(allow_output_mutation=True)
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

@st.cache(allow_output_mutation=True)
def Normalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

vectorizer = TfidfVectorizer(tokenizer=Normalize,stop_words = stopwords.words('french'))

@st.cache(allow_output_mutation=True)
def load_doc(jsonFile):
    with open(jsonFile) as file:
        Json_data = json.loads(file.read())
    return Json_data


data = load_doc('data.json')
book = load_doc('book.json')
eclf= joblib.load('eclf.pkl')
df = pd.DataFrame(data, columns = ["Text","Intent"])
x = df['Text']
y = df['Intent']
X = vectorizer.fit_transform(x)

# To get responnse
@st.cache(allow_output_mutation=True)
def response(user_input):
    text_test = [user_input]
    X_test = vectorizer.transform(text_test)
    prediction = eclf.predict(X_test)
    reply = random.choice(responses[prediction[0]]['response'])
    return reply

# To get indent
@st.cache(allow_output_mutation=True)
def intent(user_input):
    text_intent = [user_input]
    X_test_intent = vectorizer.transform(text_intent)
    predicted_intent = eclf.predict(X_test_intent)
    intent_predicted = responses[predicted_intent[0]]['intent']
    return intent_predicted



@st.cache(allow_output_mutation=True)
def bot_initialize(user_msg):
    flag=True
    while(flag==True):
        user_input = user_msg
        
        user_intent = intent(user_input)
        
        if (user_intent != 'Bye'):
            if (user_input == 'Start'):
                resp = """Salut je  suis HSEbot une intelligence artificielle qui t'aide à identifier les dangers et les risques ainsi qu'à les prévenirs.Mon créateur est Dahou Renaud L:https://www.linkedin.com/in/dahou-renaud-louis-8958599a/\n\nComment puis-je t'aider ?\n\nTapez Bye pour quitter."""
                return resp
            
            elif (user_intent == 'salutation'):
                resp = str(random.choice(responses[0]['response'])) + ", comment puis-je vous aider?"
                return resp
        
            elif (user_intent == 'conaissance'):
                resp = str(random.choice(responses[1]['response']))+ ", comment puis-je vous aider?"
                return resp
            
            elif (user_intent == 'fin_conversation'):
                resp = random.choice(responses[2]['response'])
                return resp

            elif (user_intent == 'Merci'):
                resp = random.choice(responses[3]['response'])
                return resp

            elif (user_intent == 'confus'):
                resp = random.choice(responses[4]['response'])
                return resp

            elif (user_intent == 'but'):
                resp = random.choice(responses[5]['response'])
                return resp

            elif (user_intent == 'début'):
                resp = random.choice(responses[6]['response'])
                return resp

            elif (user_intent == 'ques'):
                user_input=user_input.lower()
                resp =  response(user_input)
                return resp
            
            elif (user_intent == "question"):
                user_input=user_input.lower()
                resp =  response(user_input)
                return resp + "\n\n🎁CADEAU SURPRISE.🎁\nJe t'offre ce document HSE qui te servira un jour.😊:\n"+random.choice(book)

            elif (user_intent == "Act"):
                user_input=user_input.lower()
                resp =  response(user_input)
                return resp + "\n\n🎁CADEAU SURPRISE.🎁\nJe t'offre ce document HSE qui te servira un jour.😊:\n"+random.choice(book)
            
            else:
                resp = random.choice(responses[4]['response'])
                return resp
                
            
        else:
            flag = False
            resp = random.choice(responses[2]['response'])
            return resp


def get_text():
    user_input = st.text_input("Toi: ","Ecrivez ici")
    return user_input 
