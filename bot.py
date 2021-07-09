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
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import GridSearchCV
from responses import *
from data import *
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


#data = load_doc('data.json')
#book = load_doc('book.json')
eclf= joblib.load('eclf.pkl')
df = pd.DataFrame(data, columns = ["Text","Intent"])
x = df['Text']
y= df['Intent']
X= vectorizer.fit_transform(x)
#eclf.fit(X, y)

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
        
        if (user_intent !=''):
            if (user_input == 'Ecrivez ici'):
                resp = """Salut je  suis HSEbot une intelligence artificielle qui t'aide à identifier les dangers et les risques ainsi qu'à les prévenirs.Pour bien tiré profit de notre conversation, pose moi des questions précises, ne m'envoie pas juste un mot, je risque de mal répondre mon créateur m'a habitué aux questions courantes pas à définir des mots, je ne suis pas un dictionnaire 😊 \n\nComment puis-je t'aider ?"""
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

            elif (user_intent == 'but'):
                resp = random.choice(responses[5]['response'])
                return resp

            elif (user_intent == 'conaissance'):
                resp = random.choice(responses[1]['response'])
                return resp
            
            elif (user_intent == "question"):
                user_input=user_input.lower()
                resp =  response(user_input)
                return resp #+ "\n\n🎁CADEAU SURPRISE.🎁\nJe t'offre ce document HSE qui te servira un jour.😊:\n"+random.choice(book)

            else:
                resp = "Désolé je ne comprend pas mon vocabulaire est en amélioration.Envoie ta question à mon créateur @Renaud17" #random.choice(responses[4]['response'])
                return resp
                   
        else:
            flag = False
            resp = "Mais vous ne m'avez posé aucune question"+ ", comment puis-je vous aider?" #random.choice(responses[2]['response'])
            return resp


def get_text():
    user_input = st.text_input("Toi: ","Ecrivez ici")
    return user_input 
