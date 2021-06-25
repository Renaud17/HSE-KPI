import telebot
from flask import Flask, request
import os

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



TOKEN =  "1836903308:AAHtERNcpC-aJjb6J86k2AUzzUu_rxlT53k"
ktu_link = "https://www.ktu.edu.in/"
welcome_msg  ="""Salut je  suis HSEbot une intelligence artificielle qui t'aide à identifier les dangers et les risques ainsi qu'à les prévenirs.Mon créateur est Dahou Renaud L:https://www.linkedin.com/in/dahou-renaud-louis-8958599a/\n\nComment puis-je t'aider ?\n\nTapez Bye pour quitter."""
help_msg = Il te suffit de me poser une question liés aux risques et dangers par exemple du style 👉'Comment prévenir les risques liés aux ambiances thermiques?\nje suis en mesure de t'aider à identifier les risques et dangers sur les termes suivants:\n\n💥AMBIANCES THERMIQUES\n💥MANQUE D’HYGIENE\n💥BIOLOGIQUE\n💥MANUTENTION MANUELLE ET A L’ACTIVITE PHYSIQUE\n💥BRUIT\n💥MANUTENTION MECANIQUE\n💥CHUTES\n💥ORGANISATION DE LA SECURITE ET DES SECOURS\n💥CHUTES D’OBJETS\n💥ORGANISATION DU TRAVAIL\n💥DEPLACEMENTS ET A LA CIRCULATION\n💥PRODUITS CHIMIQUES\n💥RAYONNEMENTS IONISANTS\n💥ECLAIRAGE\n💥RECOURS A DES INTERIMAIRES\n💥ELECTRICITE\n💥SOUDURE\n💥INCENDIE OU D’EXPLOSION\n💥TRAVAIL SUR ECRAN\n💥INTERVENTION D’ENTREPRISES EXTERIEURES	VIBRATIONS\n💥MACHINES ET AUX OUTILS\n"
contact_msg = "Mon créateur est Dahou Renaud L:https://www.linkedin.com/in/dahou-renaud-louis-8958599a/"


bot = telebot.TeleBot(token = TOKEN)
server = Flask(__name__)
@bot.message_handler(commands=['/start','start','Start','START','START'])
def greetings(message):
    cli = message.chat.id
    bot.send_message(cli,welcome_msg)

@bot.message_handler(commands=['/help','HELP','/HELP','/Help','help','Help'])
def helpmsg(message):
     cli = message.chat.id
     bot.send_message(cli,help_msg)


@bot.message_handler(commands=['/master','master','Master','MASTER'])
def ma_details(message):
    cli = message.chat.id
    bot.send_message(cli,contact_msg)


@bot.message_handler(commands=['NEWS','news','News','/NEWS','/news','/News'])
def news(message):
    cli = message.chat.id

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
    
    news_message = news_ret
    bot.send_message(cli,resp)




@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="http://new-appiren.herokuapp.com/" + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', {port number})))