from db import *
from get import *
from subprocess import call
import streamlit as st
import pandas as pd
import datetime
import re
import base64
from datetime import datetime,date
from datetime import datetime, timedelta
from pandas import DataFrame
from io import BytesIO
import xlsxwriter
import plotly.express as px
from PIL import Image
import streamlit.components.v1 as components


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
from sklearn.externals import joblib
import json
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import GridSearchCV

@st.cache
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data
@st.cache
def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Votre fichier excel</a>' # decode b'abc' => abc

#pour verifier le type d'entrée
@st.cache
def inputcheck(inputext):
    try:
        inputext = int(inputext)
    except:
        st.error("Veillez à ne saisir qu'un nombre")
        st.stop()
    return inputext


# DB Management
import streamlit as st
#import sqlite3
import psycopg2

#conn = sqlite3.connect('data.db', check_same_thread=False)
conn=psycopg2.connect("dbname='d5ml0i8f3hkgdu' user='nhayouvhvbamum' password='8f228697bceec9cd03609fddd27b608f43a777800ac1b6c8ebd46dbfd91ffc91' host='ec2-52-4-111-46.compute-1.amazonaws.com' port='5432' ")
c = conn.cursor()



# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
@st.cache
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

@st.cache
def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


responses ={0 : {"intent":"salutation","response":["bonjour","Bonjour, je suis sûr que vous aimez protéger les travailleurs de votre entreprise", "Heureux de vous avoir ici", "Heureux de vous revoir","Salut, je suis HSEbot LA SECURITE, parce qu’une vie n’a pas de prix !!!!!!!!"]}, 
1 : {"intent":"conaissance","response":["Salut, je suis HSEbot une intelligence artificielle qui t'aide à identifier les dangers et les risques ainsi qu'à les prévenirs.Mon créateur est Dahou Renaud L:https://www.linkedin.com/in/dahou-renaud-louis-8958599a/."]},
2 : {"intent":"fin_conversation","response":["Au revoir!", "A bientôt!", "Bonne journée !"]},
3 : {"intent":"Merci","response":["Heureux de vous aider !", "A tout moment !", "Tout le plaisir est pour moi"]},
4 : {"intent":"confus","response":["Ummm ! S'il vous plaît, reformulez votre phrase avec un peu plus de précision ou ecrivez à mon créateur https://www.linkedin.com/in/dahou-renaud-louis-8958599a/ pour qu'il m'entraine plus pour répondre correctement à votre préoccupation"]},
5 : {"intent":"but","response":["je suis HSEbot,je peux vous aider à identifier les risques, les dangers et vous conseiller sur la manière de les prévenirs."]},
6 : {"intent":"début","response":["HSE est un sigle qui désigne une méthodologie de maîtrise des risques et de management des entreprises dans les domaines de l’hygiène, de la santé/sécurité et de l’environnement. Cette méthodologie fait appel aux référentiels de normes spécifiques, dont l’application peut faire l’objet, sur la base du volontariat, d’une démarche de certification auprès de divers organismes compétents (AFNOR et autres).Selon l’organisation et la taille des entreprises, les protocoles HSE peuvent être menés en interne ou en externe (cabinet conseil) par un chargé hygiène-sécurité-environnement (technicien supérieur ou même ingénieur) qui en établit les objectifs et les modalités, et qui veille à leur application, en particulier quant au respect des réglementations en vigueur et leur évolution.En tant que stratégie visant à anticiper et réduire les risques (notamment en matière d’accidents professionnels et de nuisances environnementales) mais aussi à favoriser la responsabilisation et le bien-être au travail, le processus HSE trouve de fait toute sa place au sein d’une démarche plus globale de type RSE (responsabilité sociale/sociétale des entreprises)."]},
7 : {"intent":"question","response":["💥AMBIANCES THERMIQUES:\n\nLes ambiances thermiques ont pour conséquence:\n⚡l'inconfort\n⚡la fatigue\n⚡les maladies pulmonaires ou ORL et coup de chaleur.\n\n🤔Pour faire une mise en évidence des risques et dangers liés aux  ambiances thermiques posez-vous les questions suivantes:\n\n👉La température des locaux est-elle adaptée au travail demandé (18 à 25°C selon les saisons et l’activité)❓ OUI🟢NON🔴\n👉Le poste de travail est-il exposé aux courants d’air, à l’humidité, aux intempéries❓ OUI🔴NON🟢\n👉Le poste de travail est-il suffisamment aéré❓ OUI🟢NON🔴\n👉Le poste de travail est-il à l’écart de zones chaudes ou froides❓ OUI🟢NON🔴\n👉Les EPI sont-ils fournis en cas de travail en ambiance froide ou chaude❓ OUI🟢NON🔴\n👉Utilisez-vous des systèmes de climatisation❓ OUI🔴NON🟢\n👉La maintenance et le contrôle de ces systèmes de climatisation sont-ils régulièrement réalisés❓ OUI🟢NON🔴\n👉Avez-vous prévu une organisation spécifique en cas de canicule❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié aux ambiances thermiques est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Installation de chauffages adaptés et réglables individuellement.\n✔Contrôle des courants d’air.\n✔Contrôle et entretien régulier.\n✔Mise en place de pauses en cas de travail en ambiance très chaude ou très froide.\n✔Mise à disposition de points d’eau en cas de travail en ambiance très chaude.\n✔Mise à disposition et port des équipements de protection individuelle.\n✔Information des salariés.\n"]},
8 : {"intent":"question","response":["💥BRUIT:\n\nLes dangers liés au bruit ont pour conséquence:\n⚡l'atteinte de l’acuité auditive\n⚡les difficultés de concentration pour l’exécution de travaux précis\n⚡les gêne à la compréhension de certains ordres pouvant rendre dangereuses certaines tâches.\n\n🤔Pour faire une mise en évidence des risques et dangers lié au bruit posez-vous les questions suivantes:\n\n👉Une estimation du bruit a-t-elle révélé des zones à risques❓ OUI🔴NON🟢\n👉Les salariés soumis à une exposition sonore quotidienne supérieure à 80 dBA sont-ils identifiés ❓ OUI🟢NON🔴\n👉La communication orale est-elle gênée❓ OUI🔴NON🟢\n👉Les alarmes sont-elles masquées par le bruit ❓ OUI🔴NON🟢\n👉Existe-t-il des sources de bruit gênantes dans les locaux❓ OUI🔴NON🟢\n👉Les mesures de prévention sont-elles prises❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié au bruit est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔mesure du niveau sonore reçu par les salariés.\n✔réduction du bruit des machines : contrôle et entretien régulier.\n✔limitation du temps d’exposition des salariés.\n✔éloignement des salariés des sources de bruit.\n✔mise en place de protection collective : capotage, traitement acoustique des locaux.\n✔mise à disposition et port des équipements de protection individuelle.\n✔information et formation des salariés.\n"]},
9 : {"intent":"question","response":["💥ECLAIRAGE:\n\nLes dangers liés à l'éclairage ont pour conséquence:\n⚡la fatigue visuelle liée à un éclairage inadapté\n⚡les erreur dans l’exécution de travaux précis\n⚡les risque de chute\n⚡d’accident dans les allées de circulation.\n\n🤔Pour faire une mise en évidence des risques et dangers liés à l'éclairage posez-vous les questions suivantes:\n\n\👉Le niveau d’éclairage vous semble t-il uniforme❓ OUI🟢NON🔴\n👉Des mesures d’éclairage ont-elles révélé des zones d’inconfort❓ OUI🔴NON🟢\n👉Les aires de circulation sont-elles correctement éclairées❓ OUI🟢NON🔴\n👉Le poste de travail présente-t-il des zones d’éblouissement (lampe nue, soleil) ❓ OUI🔴NON🟢\n👉Les luminaires sont-ils propres et les ampoules sont-elles changées régulièrement❓ OUI🟢NON🔴\n👉L’éclairage entraîne t il des postures contraignantes au poste❓ OUI🔴NON🟢\n👉La chaleur dégagée par l’éclairage vous paraît-elle excessive ❓ OUI🔴NON🟢\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié à l'éclairage est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Eclairage suffisant et adapté au travail à réaliser : précision, détail…\n✔Eclairage naturel suffisant.\n✔Eclairage individuel possible.\n✔Vérification régulière des lampes, néons…\n✔Installation d’éclairages de secours.\n✔Information des salariés.\n"]},
10 : {"intent":"question","response":["💥VIBRATIONS:\n\nLes dangers liés aux vibrations ont pour conséquence des risques de:\n⚡lésion tendineuse\n⚡musculaire\n⚡neurologique ou vasculaire\nsuite à l’utilisation d’outils vibrants, à la conduite d’engins.\n Pour faire une mise en évidence des risques et dangers liés à l'éclairage posez-vous les questions suivantes:\n\n👉Des outils vibrants sont-ils utilisés (perceuse, ponceuse ….)❓ OUI🔴NON🟢\n👉Des outils pneumatiques, à main sont-ils utilisés (marteau, burin …)❓ OUI🔴NON🟢\n👉Des chariots élévateurs sont-ils utilisés❓ OUI🔴NON🟢\n👉Des véhicules P.L. ou des engins de chantier sont-ils utilisés❓ OUI🔴NON🟢\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié aux vibrations est-il mis en évidence ?   OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Diminution des vibrations sur outils par mise en place de protection mousse.\n✔Choisir des outils antivibratoires.\n✔Installation de sièges confortables, suspendus dans les engins de chantier ou PL.\n✔Diminuer la durée d’exposition au risque : alternance des tâches, pauses …\n✔Information des salariés.\n"]},
11 : {"intent":"question","response":["💥PRODUITS CHIMIQUES:\n\nLes dangers liés aux produits chimiques exposent au risque:\n⚡d’irritation\n⚡d’allergie\n⚡de brûlure\n⚡d’intoxication\n⚡de décès par inhalation\n⚡d’ingestion de produits chimiques ou d’exposition cutanée.\n\n🤔Pour faire une mise en évidence des risques et dangers liés aux produits chimiques posez-vous les questions suivantes:\n\n👉La liste des produits utilisés et les fiches de données de sécurité sont-elles disponibles❓ OUI🟢NON🔴\n👉Ces fiches révèlent elles un risque potentiel❓ OUI🔴NON🟢\n👉Les salariés sont-ils exposés à ces produits par contact cutané, inhalation ou ingestion (fumées, poussières, vapeurs,…)❓ OUI🔴NON🟢\n👉Avez-vous des produits classés irritants Xi, corrosifs C, nocifs Xn, toxiques T❓ OUI🔴NON🟢\n👉Avez-vous des produits classés Cancérogène, Mutagène ou Reprotoxique (CMR)❓ OUI🔴NON🟢\n👉Tous les flacons utilisés sont ils étiquetés (nom du produit, pictogramme, phrases de risque, …)❓ OUI🟢NON🔴\n👉Les quantités de produit sur le poste de travail sont-elles limitées❓ OUI🟢NON🔴\n👉Y a-t-il des moyens de stockage des chiffons, déchets aux postes de travail (poubelles à couvercle, …)❓ OUI🟢NON🔴\n👉Les locaux et les zones de stockage sont-ils correctement ventilés❓ OUI🟢NON🔴\n👉Avez-vous une ventilation générale de vos locaux de travail❓ OUI🟢NON🔴\n👉Les zones à pollution spécifique sont-elles correctement ventilées❓ OUI🟢NON🔴\n👉Les salariés sont-ils formés à l’utilisation des produits : connaissance des pictogrammes, des incompatibilités entre produits, des moyens de protection adéquats❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié aux produits chimiques est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Etude des fiches de sécurité mises à jour\n✔Contrôle du stockage et de l’évacuation des déchets\n✔Prévoir les modalités d’action en cas d’accident\n✔Ventilation correcte des locaux\n✔Mise à disposition et port des équipements de protections\n✔Diminution des quantités de produit sur les postes\n✔Information et formation des salariés\n✔Evaluation des risques chimique (logiciel AST74)\n"]},   
12 : {"intent":"question","response":["💥BIOLOGIQUE:\n\nLes secteurs concernés par ce danger ou risque sont:\n✔Santé\n✔agriculture\n✔climatisation\n✔traitement des réseaux d’eau usée\n✔industrie du bois\n✔services funéraires\n✔voyages à l’étranger\n✔travaux au contact des animaux ou des produits d’origine animale\n✔agroalimentaire\n✔traitement des déchets\n✔industrie textile\n✔industrie du papier\n✔travaux de nettoyage\n✔soins aux blessés (SST).\nLes dangers d'origine biologique exposent au risque:\n⚡d’infection\n⚡d’intoxication\n⚡de réaction allergique ou de cancer suite à l’exposition à des agents biologiques par inhalation\n⚡ingestion\n⚡contact ou pénétration suite à une lésion.\n\n🤔Pour faire une mise en évidence des risques et dangers d'origine biologique posez-vous les questions suivantes:\n\n👉Certains salariés ont-ils un travail en milieu de soins, laboratoire, …❓ OUI🔴NON🟢\n👉Certains salariés ont-ils des contacts avec des animaux ou des produits d’origine animale ou agroalimentaire❓ OUI🔴NON🟢\n👉Certains salariés ont-ils des contacts avec des cadavres❓ OUI🔴NON🟢\n👉Des salariés ont-ils des contacts avec des déchets, des eaux usées❓ OUI🔴NON🟢\n👉Les réservoirs de germes sont-ils repérés, signalés, nettoyés, désinfectés❓ OUI🟢NON🔴\n👉Des procédures sont elles en place pour le transport et le traitement des déchets ❓ OUI🟢NON🔴\n👉Le nombre de salariés susceptibles d’être exposé est-il limité au plus bas❓ OUI🟢NON🔴\n👉Le matériel à usage unique est-il éliminé ❓ OUI🟢NON🔴\n👉La liste du personnel exposé (groupe 3 et 4) est-elle tenue à jour❓ OUI🟢NON🔴\n👉Les salariés sont-ils tous formés au risque spécifique de leur poste❓ OUI🟢NON🔴\n👉Les salariés sont-ils informés des accidents, incidents avec agent biologique❓ OUI🟢NON🔴\n👉Les consignes de sécurité sont-elles régulièrement renouvelées❓ OUI🟢NON🔴\n👉Les équipements de protection adéquats sont-ils portés❓ OUI🟢NON🔴\n👉Les salariés ont-ils la possibilité de se laver correctement les mains❓ OUI🟢NON🔴\n👉Le suivi des vaccinations approprié est-il mis en place❓ OUI🟢NON🔴\n👉Avez-vous mis en place une procédure grippe aviaire❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger d'origine biologique est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Respect des précautions d’hygiène.\n✔Confinement des zones à risque.\n✔Organisation de la manipulation, du transport des produits contaminants.\n✔Procédure d’élimination des déchets réalisée et suivie.\n✔Ventilation correcte des locaux\n✔Protocole de la conduite à tenir en cas d’accident avec exposition au sang affiché.\n✔Port effectif des équipements de protection adaptés : gants, lunettes, blouse.\n✔Soin correct de toutes les blessures.\n✔Matériel à usage unique privilégié.\n✔Vaccination des salariés exposés en règle.\n✔Information et formation des salariés.\n"]},
13 : {"intent":"question","response":["💥MANUTENTION MANUELLE ET ACTIVITE PHYSIQUE:\n\nLes dangers  liés à la manutention manuelle et a l’activité physique exposent au\n⚡risque d’atteinte musculaire\n⚡tendineuse\n⚡vertébrale\nsuite à des traumatismes, efforts physiques, posture incorrecte, gestes répétitifs.\n\n🤔Pour faire une mise en évidence des risques et dangers liés à la manutention manuelle et a l’activité physique posez-vous les questions suivantes:\n\n👉L’activité exige-t-elle des manutentions répétées et rapides❓ OUI🔴NON🟢\n👉L’activité exige-t-elle des manutentions de poids élevé❓ OUI🔴NON🟢\n👉L’activité exige-t-elle des manutentions difficiles : taille, encombrement, mauvaises prises❓ OUI🔴NON🟢\n👉L’activité exige-t-elle des manutentions sur des distances importantes❓ OUI🔴NON🟢\n👉L’activité exige-t-elle des manutentions dans un environnement particulier (froid, chaud…)❓ OUI🔴NON🟢\n👉Les salariés se plaignent ils de douleurs articulaires❓ OUI🔴NON🟢\n👉La manutention impose-t-elle des postures incorrectes : dos plié, jambes tendues, charge à bout de bras ….❓ OUI🔴NON🟢\n👉Les postes de travail sont-ils équipés d’aide à la manutention❓ OUI🟢NON🔴\n👉Les salariés sont-ils formés aux bons gestes de la manutention manuelle❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié à la manutention manuelle et a l’activité physique est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Supprimer ou diminuer les manutentions manuelles au poste.\n✔Diminuer le poids des charges, les déplacements, la répétitivité des déplacements\n✔Utilisation  de transpalette, chariots roulants…\n✔Mise des charges à niveau : table élévatrice, quai de chargement, hayon…\n✔Utilisation de moyens de préhension adaptés : poignées…\n✔Formation du personnel à la manutention\n✔Mise à disposition et port d’équipements de protection individuelle : gants, chaussures.\n"]},
14 : {"intent":"question","response":["💥MANUTENTION MECANIQUE:\n\nLes dangers liés à la  manutention mécanique  exposent au risque:\n⚡de blessure souvent grave lié à la circulation d’engins, à la nature de la charge, aux moyens de manutention.\n\n🤔Pour faire une mise en évidence des risques et dangers liés à la manutention mécanique posez-vous les questions suivantes:\n\n👉Les appareils de manutention sont-ils entretenus et vérifiés régulièrement❓ OUI🟢NON🔴\n👉Les élingues à usage unique sont-elles éliminées❓ OUI🟢NON🔴\n👉Les utilisateurs sont-il tous formés et recyclés régulièrement❓ OUI🟢NON🔴\n👉Les zones de circulation et de manœuvre sont-elles larges, bien dégagées et éclairées❓ OUI🟢NON🔴\n👉Les sols sont-ils en bon état, propres, réguliers sans trous❓ OUI🟢NON🔴\n👉Les charges sont-elles bien réparties et arrimées ❓ OUI🟢NON🔴\n👉La vitesse de circulation des engins est-elle correcte ❓ OUI🟢NON🔴\n👉Les postes de travail sont-ils équipés d’aide à la manutention❓ OUI🟢NON🔴\n👉Un plan de circulation est-il en usage (engins, piétons)❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié à la  manutention mécanique est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Utilisation  d’engins conformes à la réglementation.\n✔Respect de la vitesse et de la signalisation.\n✔Entretien régulier du matériel de manutention.\n✔Conduite des engins exclusivement par des salariés formés, habilités et aptes médicalement.\n✔Entretien des voies de circulation.\n"]},
15 : {"intent":"question","response":["💥DEPLACEMENTS ET CIRCULATION:\n\nLes dangers liés aux déplacements et à la circulation exposent au \n⚡risque de blessure lors d’un accident de circulation dans l’entreprise ou à l’extérieur.\n\n🤔Pour faire une mise en évidence des risques et dangers liés aux déplacements et à la circulation posez-vous les questions suivantes:\n\n👉Les véhicules sont-ils entretenus et vérifiés régulièrement❓ OUI🟢NON🔴\n👉Les utilisateurs chauffeurs sont-ils tous formés❓ OUI🟢NON🔴\n👉Les zones de circulation sont-elles larges, bien éclairées avec un sol en bon état❓ OUI🟢NON🔴\n👉Les zones de manœuvre sont-elles signalées, suffisamment larges, bien dégagées et éclairées❓ OUI🟢NON🔴\n👉L’organisation du travail oblige-t-elle à réaliser des déplacements inutiles ou à risque ❓ OUI🔴NON🟢\n👉Les véhicules sont-ils adaptés à l’activité demandée ❓ OUI🟢NON🔴\n👉Pendant la conduite, y a-t-il utilisation de téléphone portable ou autre moyen de communication ❓ OUI🔴NON🟢\n👉Un plan de circulation sans zones communes piétons-véhicules est-il en usage ❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié aux déplacements et à la circulation est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Mise en place d’un plan de circulation.\n✔Eclairage et signalisation des voies de circulation.\n✔Entretien régulier et réparation des véhicules.\n✔Organisation du travail limitant les déplacements.\n✔Respect du code de la route.\n✔Laisser un temps suffisant pour les déplacements.\n✔Entretien des voies de circulation, des zones de manœuvre.\n✔Utiliser des moyens sûrs (train, autoroutes …)\n✔Conduite des véhicules par des salariés formés, habilités et aptes médicalement.\n✔Formation à la conduite en sécurité.\n"]},
16 : {"intent":"question","response":["💥CHUTES:\n\nLes dangers liés aux chutes exposent au\n⚡risque de blessure suite à une chute de plain-pied ou de hauteur d’un salarié.\n\n🤔Pour faire une mise en évidence des risques et dangers liés aux chutes posez-vous les questions suivantes:\n\n👉Le sol est-il glissant : huile, déchets, verglas …❓ OUI🔴NON🟢\n👉Le sol est-il dégradé : trou, revêtement inégal … ❓ OUI🔴NON🟢\n👉Le sol est-il inégal : marche, pente, …❓ OUI🔴NON🟢\n👉Le sol est-il encombré : palettes, câbles, outils …❓ 🔴   NON🟢\n👉Les zones de passage sont-elles étroites, encombrées, mal éclairées❓ OUI🔴NON🟢\n👉Faut-il longer des zones dangereuses pour avancer (machines, partie saillante)❓ OUI🔴NON🟢\n👉L’accès à des zones en hauteur est-il nécessaire : toit, armoire, machine❓ OUI🔴NON🟢\n👉Utilise-t-on des échelles, escabeaux, nacelles …❓ OUI🔴NON🟢\n👉Utilise-t-on des moyens de travail en hauteur bricolés ou inadaptés❓ OUI🔴NON🟢\n👉Les escaliers, passerelles sont-ils équipés de main courante ❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié aux chutes est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Nettoyage immédiatement des sols sales.\n✔Formation du personnel à la sécurité.\n✔Entretien des revêtements, suppression des inégalités des sols.\n✔Organisation de la circulation des personnes dans l’entreprise.\n✔Dégagement et éclairage suffisant des passages.\n✔Mise en place de protections antichute : main courante, garde-corps, marche antidérapante.\n✔Suppression les zones avec des différences de niveau\n✔Utilisation des protections individuelles ou collectives : harnais, lignes de vie, garde-corps, chaussures antidérapantes.\n✔Déneigement l’hiver.\n✔Libérer les zones de circulation.\n"]},
17 : {"intent":"question","response":["💥CHUTES D’OBJETS:\n\nLes dangers liés aux chutes d'objets exposent au\n⚡risque de blessure  suite à la chute d’objets stockés en hauteur ou d’effondrement de moyens de stockage.\n\n🤔Pour faire une mise en évidence des risques et dangers liés aux chutes d'objets posez-vous les questions suivantes:\n\n👉Des objets sont-ils stockés en hauteur : étagères, racks … ❓ OUI🔴NON🟢\n👉Les zones de stockage sont-elles bien délimitées, facilement accessibles ❓ OUI🟢NON🔴\n👉Les palettes sont-elles en bon état, vérifiées … ❓ OUI🟢NON🔴\n👉Les palettes défectueuses sont-elles mises hors circuit ❓ OUI🟢NON🔴\n👉Les moyens de stockage sont-ils adaptés aux charges : encombrement, poids❓ OUI🟢NON🔴\n👉Les moyens de stockage sont-ils en bon état et contrôlés régulièrement ❓ OUI🟢NON🔴\n👉Des objets sont-ils empilés sur de grandes hauteurs, en équilibre précaire ❓ OUI🔴NON🟢\n👉Des travaux sont-ils effectués au-dessus ou en-dessous d’autres postes ❓ OUI🔴NON🟢\n👉Y-a-t-il vérification des piliers des racks, mise en place de protections d’angles ❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié aux chutes d'objets est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Organisation correcte des stockages : emplacement, accessibilité.\n✔Utilisation de matériel de stockage adapté aux charges.\n✔Limitation des hauteurs de stockage.\n✔Installation de protections pouvant retenir les objets en cas de chute.\n✔Vérification régulière des palettes.\n✔Utilisation des protections individuelles : casque, chaussures…\n"]},     
18 : {"intent":"question","response":["💥MACHINES ET OUTILS:\n\nLes dangers liés aux machines et aux outils exposent au\n⚡risque de blessure (coupure ✔écrasement ✔fracture …) par machine ou outil.\n\n🤔Pour faire une mise en évidence des risques et dangers liés aux machines et aux outils posez-vous les questions suivantes:\n\n👉La mise en conformité du parc machines est-elle terminée ❓ OUI🟢NON🔴\n👉Des parties mobiles, dangereuses de machine sont-elles accessibles ❓ OUI🔴NON🟢\n👉Existe-t-il un risque de projection de liquide sous pression, de copeaux ❓ OUI🔴NON🟢\n👉Tout outil défectueux est-il immédiatement signalé et réparé ou éliminé ❓ OUI🟢NON🔴\n👉Toute intervention sur une machine est-elle signalée avec respect des consignes de sécurité ❓ OUI🟢NON🔴\n👉Utilise-t-on des outils tranchants ❓ OUI🔴NON🟢\n👉Utilise-t-on des outils portatifs : scie, tronçonneuse, meuleuse ❓ OUI🔴NON🟢\n👉Existe-t-il un risque d’écrasement entre des équipements mobiles de la machine et des éléments fixes (paroi, pilier, …) ❓ OUI🔴NON🟢\n👉Les dispositifs de sécurité des machines sont-ils présents, efficaces et non shuntés ❓ OUI🟢NON🔴\n👉Les salariés sont-ils formés aux risques de leur poste de travail ❓ OUI🟢NON🔴\n👉Assurez vous la traçabilité des vérifications périodiques ❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié aux machines et aux outils est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Mise en conformité des machines à la réglementation.\n✔Information et formation des salariés.\n✔Utilisation des machines selon les recommandations du fabriquant.\n✔Vérification de l’utilisation, du bon état et du bon fonctionnement.\n✔Contrôle régulier des arrêts d’urgence.\n✔Port des équipements de protection individuelle : lunettes, gants.\n"]},
19 : {"intent":"question","response":["💥MACHINES ET OUTILS:\n\nLes dangers liés aux machines et aux outils exposent au\n⚡risque de blessure (coupure ✔écrasement ✔fracture …) par machine ou outil.\n\n🤔Pour faire une mise en évidence des risques et dangers liés aux machines et aux outils posez-vous les questions suivantes:\n\n👉La mise en conformité du parc machines est-elle terminée ❓ OUI🟢NON🔴\n👉Des parties mobiles, dangereuses de machine sont-elles accessibles ❓ OUI🔴NON🟢\n👉Existe-t-il un risque de projection de liquide sous pression, de copeaux ❓ OUI🔴NON🟢\n👉Tout outil défectueux est-il immédiatement signalé et réparé ou éliminé ❓ OUI🟢NON🔴\n👉Toute intervention sur une machine est-elle signalée avec respect des consignes de sécurité ❓ OUI🟢NON🔴\n👉Utilise-t-on des outils tranchants ❓ OUI🔴NON🟢\n👉Utilise-t-on des outils portatifs : scie, tronçonneuse, meuleuse ❓ OUI🔴NON🟢\n👉Existe-t-il un risque d’écrasement entre des équipements mobiles de la machine et des éléments fixes (paroi, pilier, …) ❓ OUI🔴NON🟢\n👉Les dispositifs de sécurité des machines sont-ils présents, efficaces et non shuntés ❓ OUI🟢NON🔴\n👉Les salariés sont-ils formés aux risques de leur poste de travail ❓ OUI🟢NON🔴\n👉Assurez vous la traçabilité des vérifications périodiques ❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié aux machines et aux outils est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Mise en conformité des machines à la réglementation.\n✔Information et formation des salariés.\n✔Utilisation des machines selon les recommandations du fabriquant.\n✔Vérification de l’utilisation, du bon état et du bon fonctionnement.\n✔Contrôle régulier des arrêts d’urgence.\n✔Port des équipements de protection individuelle : lunettes, gants.\n"]},
20 : {"intent":"question","response":["💥ELECTRICITE:\n\nLes dangers liés  à l'électricité exposent au risque:\n⚡de grave de brûlure\n⚡d’électrisation de salariés.\n\n🤔Pour faire une mise en évidence des risques et dangers liés à l'électricité posez-vous les questions suivantes:\n\n👉Existe-t-il dans l’entreprise des fils dénudés, sous tension accessibles aux salariés (armoire électrique ouverte) ❓ OUI🔴NON🟢\n👉Les intervenants de l’entreprise ont-ils une habilitation électrique ❓ OUI🟢NON🔴\n👉Existe-t-il dans l’entreprise du matériel électrique défectueux connu ❓ OUI🟢NON🔴\n👉Tout le matériel électrique défectueux est-il immédiatement signalé et réparé ou éliminé  ❓ OUI🟢NON🔴\n👉Toute intervention sur une installation électrique est-elle signalée avec respect des consignes de sécurité ❓ OUI🟢NON🔴\n👉Les installations sont-elles vérifiées régulièrement ❓ OUI🟢NON🔴\n👉Les remarques des rapports de vérification sont-elles traitées  ❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié à l'électricité est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Installation et maintenance électrique par des professionnels habilités.\n✔Contrôle régulier des installations.\n✔Traitement immédiat de toute anomalie électrique.\n✔Fermeture des armoires électriques.\n✔Habilitation des salariés devant intervenir sur des installations électriques.\n✔Information des salariés du risque électrique.\n"]},
21 : {"intent":"question","response":["💥INCENDIE OU EXPLOSION:\n\nLes dangers d'incendie ou d'explosion exposent au risque:\n⚡de blessure\n⚡de brûlure souvent grave de salariés\n⚡de dégâts matériels importants.\n\n🤔Pour faire une mise en évidence des risques et dangers d'incendie ou d'explosion posez-vous les questions suivantes:\n\n👉Avez-vous des produits étiquetés inflammable F ou F+, explosif E, comburant O ❓ OUI🔴NON🟢\n👉D’autres produits inflammables comme papier, bois, gaz sont présents❓ OUI🔴NON🟢\n👉Un risque de mélange de produits incompatibles entre eux existe-il ❓ OUI🔴NON🟢\n👉Y a-t-il des sources d’inflammation électrique, mécanique, thermique : soudure, meulage, étincelles électriques, particules incandescentes  … ❓ OUI🔴NON🟢\n👉Existe-t-il dans l’entreprise des secteurs où sont entreposés bidons ouverts, vieux chiffons …  ❓ OUI🔴NON🟢\n👉Les zones à risque d’explosion sont-elles définies et bien délimitées … ❓ OUI🟢NON🔴\n👉Les matériels de lutte contre l’incendie sont-ils adaptés, accessibles, vérifiés … ❓ OUI🟢NON🔴\n👉Les salariés sont-ils formés pour le risque incendie ❓ OUI🟢NON🔴\n👉Un plan d’évacuation existe-t-il ❓ Est-il testé ❓ OUI🟢NON🔴\n👉L’interdiction de fumer est-elle respectée ❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger d'incendie ou d'explosion est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Installation et vérification de moyens de détection, d’alarme, d’extinction.\n✔Stockage des produits dangereux hors secteur de production.\n✔Remplacer les produits inflammables ou explosifs par des moins dangereux.\n✔Installation de protection mur et porte coupe-feu …\n✔Eloignement des sources d’inflammation : soudure, flamme …\n✔Signalisation des zones d’interdiction de fumer.\n✔Installation de  matériel électrique antidéflagrant, mise à la terre…\n✔Formation et entraînement d’évacuation des salariés.\n"]},
22 : {"intent":"question","response":["💥TRAVAIL SUR ECRAN:\n\nLes dangers  liés au travail sur écran exposent au risque:\n⚡de fatigue visuelle (génératrice de gêne à la vision et d’erreurs dans l’activité)\n⚡de troubles musculaires, tendineux.\n\n🤔Pour faire une mise en évidence des risques liés au travail sur écran posez-vous les questions suivantes:\n\n👉L’écran est-il positionné correctement (absence de reflets ou d’éblouissement)❓ OUI🟢NON🔴\n👉Les fenêtres sont-elles équipées de stores à lamelles ❓ OUI🟢NON🔴\n👉Le poste de travail est-il bien agencé permettant une posture de travail correcte tout le temps, un espace suffisant pour bouger ❓ OUI🟢NON🔴\n👉Le travail sur écran est-il discontinu permettant une alternance de tâches ❓ OUI🟢NON🔴\n👉Les salariés sont-ils formés à l’utilisation des logiciels de l’entreprise ❓ OUI🟢NON🔴\n👉Les salariés se plaignent-ils de douleurs, de fatigue visuelle devant l’écran ❓ OUI🔴NON🟢\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié au travail sur écran est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Réflexion sur l’emplacement des écrans dès la conception des bureaux.\n✔Prises électriques  suffisantes et câblage informatique assez long.\n✔Fenêtres équipées de stores réglables (intérieurs et/ou extérieurs)\n✔Qualité du siège réglable, des bureaux.\n✔Alternance des tâches permettant des interruptions du travail sur écran.\n✔Utilisation de logiciels à paramètres réglables : couleur et taille des caractères, fond d’écran…,\n✔Formation des salariés\n"]},
23 : {"intent":"question","response":["💥RAYONNEMENTS IONISANTS:\n\nLes dangers  liés aux rayonnements ionisants exposent au\n⚡risque d’atteinte locale (peau, œil,…) ou générale avec effets irréversibles possibles.\n\n🤔Pour faire une mise en évidence des risques liés aux rayonnements ionisants posez-vous les questions suivantes:\n\n\n👉Avez-vous des postes exposant à des rayonnements ionisants ❓ OUI🔴NON🟢\n👉Connaissez-vous les limites d’exposition aux rayonnements ❓ OUI🟢NON🔴\n👉Avez-vous une personne compétente en radio protection, régulièrement formée ❓ OUI🟢NON🔴\n👉Analysez vous régulièrement les postes de travail de façon à évaluer les doses susceptibles d’être reçues par les salariés ❓ OUI🟢NON🔴\n👉Avez-vous délimité un zonage radio protection autour de la source de rayonnements (zone surveillée ZS – zone contrôlée ZC) ❓ OUI🟢NON🔴\n👉Avez-vous effectué le classement de vos salariés en catégorie A ou B  ❓ OUI🟢NON🔴\n👉Avez-vous affiché les consignes de travail ❓ OUI🟢NON🔴\n👉Avez-vous affiché les panneaux réglementaires ❓ OUI🟢NON🔴\n👉Faites vous procéder à des contrôles techniques de radioprotection de vos sources de vos appareils émetteurs de rayonnement ionisants au moins une fois par an ❓ OUI🟢NON🔴\n👉Chaque salarié intervenant en ZC ou ZS a-t-il un suivi par dosimètre externe (dosimétrie passive) obligatoire ? ❓ OUI🟢NON🔴\n👉Chaque salarié intervenant en Z.C fait-il l’objet d’un suivi par  dosimétrie opérationnelle ❓ OUI🟢NON🔴\n👉Avez-vous établi pour chaque salarié une fiche d’exposition ❓ OUI🟢NON🔴\n👉Chaque salarié classé en catégorie A ou B bénéficie t’il d’un examen médical au moins 1 fois/an ❓ OUI🟢NON🔴\n👉En cas d’intervention d’une entreprise extérieure, coordonnez-vous les mesures de prévention ❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié aux rayonnements ionisants est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Respect des bases de la radioprotection : justification, optimisation, limitation.\n✔Agir sur le temps d’exposition, la distance, les écrans.\n✔délimitation des zones surveillées et contrôlées✔balisage de ces zones par panneaux réglementaires\n✔définition des mesures de protection collectives et individuelles appropriées à la nature de l’exposition susceptible d’être subie par les salariés intervenant en ZC ou ZS\n✔formation des salariés sur les risques liés aux RI (au moins tous les 3 ans)\n✔respect des interdictions en zone (boire, manger, fumer)\n✔fourniture des EPI par l’entreprise utilisatrice aux salariés des entreprises extérieures."]},
24 : {"intent":"question","response":["💥SOUDURE:\n\nLes dangers  liés à la soudure ont pour conséquences\n⚡les atteinte pulmonaire, cutanée, oculaire, des voies aériennes supérieures\n⚡le syndrome parkinsonien (manganèse, aluminium)\n⚡les fumées de soudage sont reconnues cancérigènes par le CIRC (centre internationale de recherche contre le cancer)\n\n🤔Pour faire une mise en évidence des risques liés  à la soudure posez-vous les questions suivantes:\n\n👉Tous les types de soudure sont-ils répertoriés dans votre entreprise ❓ OUI🟢NON🔴\n👉Avez-vous les fiches de données de sécurité des produits que vous soudez ❓ OUI🟢NON🔴\n👉Avez-vous quantifié le temps de soudure par jour et par soudeur ❓ OUI🟢NON🔴\n👉Soudez-vous des pièces peintes ou dégraissées ❓ OUI🟢NON🔴\n👉Le risque incendie, explosion a-t-il été pris en compte ❓ OUI🟢NON🔴\n👉Le système électrique des équipements est-il vérifié régulièrement ❓ OUI🟢NON🔴\n👉Dans le cadre du soudage TIG, utilisez-vous du tungstène thorié ❓ OUI🔴NON🟢\n👉Avez-vous un système d’aspiration ❓ OUI🟢NON🔴\n👉Des EPI sont-ils fournis ❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié à la soudure est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔aspiration locale au poste de soudage (torche aspirante, bras mobile…)\n✔ventilation générale de l’atelier.\n✔isolement des salariés lors des opérations de soudure (écran, panneau, rideau)\n✔stockage correct des bouteilles de gaz (oxygène, acétylène, argon, …)\n✔mise à disposition d’EPI adaptés.\n✔port de masque-lunettes adaptés au rayonnement lors du soudage.\n✔remplacement des électrodes thoriées par des électrodes au césium moins radioactives.\n-affûtage des électrodes sous aspiration.\n"]},
25 : {"intent":"question","response":["💥MANQUE D’HYGIENE:\n\nLes dangers  liés au manque d'hygiène ont pour conséquences:\n⚡le risque sanitaire\n⚡le risque de contamination d’individus et de produits dans les professions de la restauration, de la santé.\n\n🤔Pour faire une mise en évidence des risques liés au manque d'hygiène posez-vous les questions suivantes:\n\n👉Existe-t-il des sanitaires en nombre suffisant, homme/femme ❓ OUI🟢NON🔴\n👉Sont-ils nettoyés et désinfectés régulièrement ❓ OUI🟢NON🔴\n👉Sont-ils ventilés ❓ OUI🟢NON🔴\n👉Existe-t-il des vestiaires en nombre suffisant, homme/femme ❓ OUI🟢NON🔴\n👉Existe-t-il des douches dans le cas de travaux salissants ❓ OUI🟢NON🔴\n👉Existe-t-il des points d’eau potable ❓ OUI🟢NON🔴\n👉Existe-t-il une salle de repos ❓ OUI🟢NON🔴\n👉Tous ces locaux sont-ils correctement entretenus aérés et/ou ventilés ❓ OUI🟢NON🔴\n👉L’interdiction de manger au poste de travail est-elle respectée ❓ OUI🟢NON🔴\n👉Les produits pour se laver les mains sont-ils adéquats ❓ OUI🟢NON🔴\n👉L’usage de solvants pour se laver les mains est-il interdit ❓ OUI🟢NON🔴\n👉Les vêtements de travail sont-ils lavés régulièrement ❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié au manque d'hygiène est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Mise à disposition de produits de lavage des mains adaptés.\n✔Mise à disposition de sanitaires et vestiaires en nombre suffisant, propres, homme/femme.\n✔Mise à disposition de points d’eau, de vêtements de travail lavés régulièrement.\n✔Débit d’air.\n"]},
26 : {"intent":"question","response":["💥ORGANISATION DE LA SECURITE ET DES SECOURS:\n\n🤔Pour faire une mise en évidence des risques liés à la mauvaise organisation de la sécurité et des secours posez-vous les questions suivantes:\n\n👉Avez vous un responsable sécurité ❓ OUI🟢NON🔴\n👉Des visites de sécurité sont elles régulièrement pratiquées ❓ OUI🟢NON🔴\n👉Tous les salariés ont-ils bénéficié d’une formation à la sécurité en rapport avec leur poste de travail❓ OUI🟢NON🔴\n👉Des équipements de protection individuelle entretenus, adaptés aux risques de l’entreprise, sont-ils portés par les salariés❓ OUI🟢NON🔴\n👉Les demandes des salariés, relatives à la sécurité, sont-elles prises en compte ❓ OUI🟢NON🔴\n👉Un plan d’organisation des secours est-il en fonction dans l’entreprise ❓ OUI🟢NON🔴\n👉Les numéros de téléphone d’urgence sont-ils affichés visiblement dans chaque atelier ❓ OUI🟢NON🔴\n👉Y a-t-il des sauveteurs secouristes du travail dans votre entreprise ❓ OUI🟢NON🔴\n👉Sont-ils recyclés ❓ OUI🟢NON🔴\n👉Une trousse d’urgences, régulièrement contrôlée est-elle présente ❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié à la mauvaise organisation de la sécurité et des secours est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Présence d’un animateur de sécurité.\n✔Formation à la sécurité des salariés à leur embauche, puis régulièrement.\n✔Intégration de la sécurité dans la culture de l’entreprise.\n✔Procédure d’organisation des secours réalisée et testée.\n"]},
27 : {"intent":"question","response":["💥ORGANISATION DU TRAVAIL:\n\n🤔Pour faire une mise en évidence des risques liés à l'organisation du travail posez-vous les questions suivantes:\n\n👉Y a-t-il des horaires de travail fixes de nuit❓ OUI🔴NON🟢\n👉Des horaires de travail en équipes alternantes 2x8 ✔3x8 ❓ OUI🔴NON🟢\n👉Des horaires de travail de week-end ❓ OUI🔴NON🟢\n👉Les pauses sont-elles réellement prises ❓ OUI🟢NON🔴\n👉Travaille-t-on dans l’urgence  ❓ OUI🔴NON🟢\n👉Les salariés se plaignent-ils de situation stressante  ❓ OUI🔴NON🟢\n👉Y a-t-il des exigences élevées au poste de travail avec un faible niveau d’initiative ❓ OUI🔴NON🟢\n👉Y a-t-il participation du salarié à la finalité de son travail ❓ OUI🔴NON🟢\n👉Y a-t-il un risque de violence ou d’agression du salarié à son poste ❓ OUI🔴NON🟢\n👉La formation des salariés est-elle régulièrement faite ❓ OUI🟢NON🔴\n👉Y a-t-il des salariés à des postes de travail isolé  ❓ OUI🔴NON🟢\n👉Les salariés sont-ils polyvalents avec roulement sur différents postes ❓ OUI🔴NON🟢\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié à l'organisation du travail est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Postes de travail en journée possibles permettant le reclassement des travailleurs postés.\n✔Accueil au poste de travail systématique avec explication des règles de sécurité.\n✔Consignes de sécurité aux postes rédigées et testées.\n✔Formation professionnelle des salariés régulière.\n✔Communication dans l’entreprise efficace.\n✔Autonomie au poste et participation du salarié aux objectifs.\n"]},
28 : {"intent":"question","response":["💥INTERVENTION D’ENTREPRISES EXTERIEURES:\n\nLes dangers  liés à l'intervention des entreprises extérieures exposent au\n⚡risque d’accident lié aux activités respectives des entreprises et à la méconnaissance des risques spécifiques des autres entreprises.\n\n🤔Pour faire une mise en évidence des risques et dangers liés à l'intervention des entreprises extérieures posez-vous les questions suivantes:\n\n👉Les services d’entreprises extérieures sont-ils utilisés : nettoyage, gardiennages, maintenance, restauration … ❓ OUI🔴NON🟢\n👉Les salariés des entreprises intervenantes sont-ils informés des risques spécifiques de l’entreprise utilisatrice  ❓ OUI🟢NON🔴\n👉Sont-ils informés des consignes de sécurité de l’entreprise utilisatrice ❓ OUI🟢NON🔴\n👉Sont-ils informés du plan de circulation de l’entreprise utilisatrice ❓ OUI🟢NON🔴\n👉Un plan de prévention est-il établi en commun ❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié à l'intervention des entreprises extérieures est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Inspection commune des lieux de travail avec les entreprises extérieures.\n✔Rédaction en commun d’un plan de prévention.\n✔Information des entreprises extérieures sur les risques, consignes de sécurité.\n✔Fourniture d’équipements de protection individuelle spécifiques aux risques de l’entreprise.\n"]},
29 : {"intent":"question","response":["💥RECOURS A DES INTERIMAIRES:\n\n🤔Pour faire une mise en évidence des risques et dangers liés au recours des intérimaires posez-vous les questions suivantes:\n\n\n👉Une visite de l’entreprise est-elle faite pour chaque intérimaire ❓ OUI🟢NON🔴\n👉Une information sur l’entreprise et ses risques est-elle donnée à l’accueil de l’intérimaire ❓ OUI🟢NON🔴\n👉L’intérimaire est-il informé et formé aux risques de son poste ❓ OUI🟢NON🔴\n👉L’information de l’entreprise de travail temporaire est-elle faite ❓ OUI🟢NON🔴\n👉Des intérimaires sont-ils affectés à des postes à risque particulier ❓ OUI🔴NON🟢\n👉Ont-ils alors une formation renforcée à la sécurité ❓ OUI🟢NON🔴\n👉Les équipements de protection individuelle sont-ils fournis aux intérimaires ❓ OUI🟢NON🔴\n👉L’intérimaire est il suivi auprès d’un service de santé au travail ❓ OUI🟢NON🔴\n\n\n🚨 Rappel : Si une case rouge est cochée, un danger est peut être identifié.\n Un danger lié au recours des intérimaires est-il mis en évidence ❓ OUI🔴NON🟢\n\n\n✅Conseils de prévention :\n\n✔Information de tout travailleur intérimaire sur les risques de l’entreprise.\n✔Formation précise, complète par la maîtrise aux risques spécifiques du poste.\n✔Mise à disposition des consignes de sécurité.\n✔Fourniture d’équipements de protection individuelle spécifiques des risques de l’entreprise.\n"]},
30 : {"intent":"question","response":["Alors en quoi puis-je t'être utile?"]},
31 : {"intent":"ques","response":["Mon créateur a fait mon éducation donc revenez-moi si vous avez des questions sur les risques et dangers. Bonne journéé!"]},
32 : {"intent":"question","response":["Il te suffit de me poser une question liés aux risques et dangers par exemple du style 👉'Comment prévenir les risques liés aux ambiances thermiques?\nje suis en mesure de t'aider à identifier les risques et dangers sur les termes suivants:\n\n💥AMBIANCES THERMIQUES\n💥MANQUE D’HYGIENE\n💥BIOLOGIQUE\n💥MANUTENTION MANUELLE ET A L’ACTIVITE PHYSIQUE\n💥BRUIT\n💥MANUTENTION MECANIQUE\n💥CHUTES\n💥ORGANISATION DE LA SECURITE ET DES SECOURS\n💥CHUTES D’OBJETS\n💥ORGANISATION DU TRAVAIL\n💥DEPLACEMENTS ET A LA CIRCULATION\n💥PRODUITS CHIMIQUES\n💥RAYONNEMENTS IONISANTS\n💥ECLAIRAGE\n💥RECOURS A DES INTERIMAIRES\n💥ELECTRICITE\n💥SOUDURE\n💥INCENDIE OU D’EXPLOSION\n💥TRAVAIL SUR ECRAN\n💥INTERVENTION D’ENTREPRISES EXTERIEURES	VIBRATIONS\n💥MACHINES ET AUX OUTILS\n"]},
33 : {"intent":"Act","response":["INSTALLATION DU CHANTIER\n💥RISQUES POTENTIELS:\n⚡Risques liés à la Co activité\n⚡Risque incendie\n⚡Risques liés à la manutention manuelle\n\n✅MESURES PREVENTIVES:\n✔Plan de Prévention\n✔Interdiction de fumer\n✔Port des EPI adaptés (gants, casque, chaussures de sécurité …\n✔Balisage correct de la zone de travail\n✔Boîte à pharmacie\n✔Tools box meeting\n✔Définition du Muster point\n✔Plan d’évacuation en cas de sinistre\n✔Explosimètre\n✔Extincteur adapté\n✔Adopter les bons gestes et postures"]},
34 : {"intent":"Act","response":["TUYAUTERIE\n💥RISQUES POTENTIELS:\n⚡\n⚡Risque de blessures\n⚡Risque de coupure\n⚡Risque incendie\n⚡Risque électrique\n⚡Risque de projection de particules\n⚡Risque d’assourdissement\n⚡Risque de heurt\n⚡Risque d’irritation\n⚡Risque de pollution\n⚡Risque lié à la manutention manuelle\n⚡Risques liés à la Co activité\n\n✅MESURES PREVENTIVES:\n✔Plan de Prévention journalier\n✔Interdiction de fumer\n✔Balisage correct de la zone de travail\n✔Port des EPI adaptés (gants de manutention / pvc,…) casque, lunettes, casque anti bruit, chaussures de sécurité …)\n✔Boîte à pharmacie\n✔Tools box meeting \n✔02 Extincteurs à poudre (ABC) 9kg\n✔Explosimètre\n✔Contrôle du matériel électrique avant utilisation\n✔Coffret électrique conforme\n✔Informer le personnel interne/externe sur les tâches à réaliser\n✔Coussin absorbant / sable\n✔Plan d’évacuation en cas de sinistre\n✔Bien ranger son matériel\n✔Adopter les bons gestes et postures\n✔Signaler/Dégager les voies de circulation\n✔Respecter les consignes de sécurité préétablies\n✔Vigilance"]},
35 : {"intent":"Act","response":["LA CIRCULATION\n\n✅MESURES PREVENTIVES:\n✔Respectez le code de la route et les panneaux de signalisation internes. La vitesse desvoitures est limitée à 25 km/h.\n✔Le chemin de fer est prioritaire, les locomotives sont télécommandées. Il est interdit destationner ou de déposer quoi que ce soità moins d’1,50 m des rails.\n✔Ne vous placez jamais derrière un camion ouun engin qui manœuvre, leur champ de vue est limité.\n✔Piétons : empruntez obligatoirement les passages, les portes et les passerelles réservées aux piétons. Respectez les balisages des zones d’intervention.\n✔Attention aux coupures aux mains ou aux jambes lors du passage dans les allées de stockage des tôles.\n✔Portez attention à l’état des sols (sols inégaux, encombrements, …). Déplacez-vous normalement sans courir. Tenez toujours la rampe d’escalier.\n✔Anticipez les déplacements des ponts. Eloignez-vous des charges et des zones de déplacement des ponts, ne stationnez et ne circulez jamais sous une charge."]},
36 : {"intent":"Act","response":["💥EN CAS D'ACCIDENT\n⚡Cas bénin\n•Rendez-vous accompagné de votre responsable au dispensaire médical.⚡Cas grave\n•Restez calme\n•Prévenez immédiatement les secours\n•communiquez votre point d’ambulance et envoyez y deux signaleurs\n•Eliminez tout danger persistant\n•Ne déplacez la victime que s’il subsisteun danger particulier (gaz, feu, …)."]},
37 : {"intent":"Act","response":["💥EN CAS D'INCENDIE\n✔Eloignez de la zone dangereuse les blessés éventuels.\n✔Prévenez immédiatement les secours communiquez votre point d’ambulance et envoyez y deux signaleurs\n✔Essayez d’éteindre le feu avec les moyens appropriés à votre disposition\n✔Si vous ne pouvez pas maîtriser le feu,évacuez"]},
38 :{"intent":"Act","response":["💥EN CAS D’ÉVACUATION GÉNÉRALE\n✔Dès le déclenchement du signal d’alerte (sirène à bi tonalité) :\n• Les Equipiers de Première Intervention appliquent leurs consignes.\n•Les travailleurs restent à leur poste de travail et sont attentifs.\n✔Dès le déclenchement du signal d’alarme (sirène continue), il y a lieu de :\n• Garder son calme. \n• Cesser immédiatement le travail. \n• Mettre les installations en sécurité selon la procédure.\n• Evacuer les lieux à pied en fermant les portes derrière soi et se diriger vers la sortie de secours la plus proche et dégagée des fumées, en empruntant le chemin le plus court.\n•Ne jamais utiliser les ascenseurs. • Ne jamais revenir en arrière quelle qu’en soit la raison. \n• Rejoindre à pied le point de rassemblement le plus proche et y attendre les instructions. \n✔Fin de l’alerte / alarme (sirène discontinue) : \n•Les travailleurs reprennent normalement leur travail."]}}  


# Lemmitization

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def Normalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

vectorizer = TfidfVectorizer(tokenizer=Normalize,stop_words = stopwords.words('french'))

def load_doc(jsonFile):
    with open(jsonFile) as file:
        Json_data = json.loads(file.read())
    return Json_data


data = load_doc('data.json')
#responses = load_doc('responses.json')
book = load_doc('book.json')
eclf= joblib.load('eclf.pkl')
df = pd.DataFrame(data, columns = ["Text","Intent"])
x = df['Text']
y = df['Intent']
X = vectorizer.fit_transform(x)

# To get responnse

def response(user_input):
    text_test = [user_input]
    X_test = vectorizer.transform(text_test)
    prediction = eclf.predict(X_test)
    reply = random.choice(responses[prediction[0]]['response'])
    return reply

# To get indent
def intent(user_input):
    text_intent = [user_input]
    X_test_intent = vectorizer.transform(text_intent)
    predicted_intent = eclf.predict(X_test_intent)
    intent_predicted = responses[predicted_intent[0]]['intent']
    return intent_predicted




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
    user_input = st.text_input("You: ","type here")
    return user_input 

def main():
    #couleur du select box
    def style():
        st.markdown("""<style>
        div[data-baseweb="select"]> div {
        background-color: yellow;
        } 
        div[role="listbox"] ul {
        background-color:white;
        }</style>""", unsafe_allow_html=True)
        
    #couleur button
    primaryColor = st.get_option("theme.primaryColor")
    s = f"""
    <style>
    div.stButton > button:first-child {{text-shadow:0px 1px 0px #2f6627;font-size:15px; background-color: #71f9ed;border: 5px solid {primaryColor}; border-radius:5px 5px 5px 5px; }}
    <style>
    """
    st.markdown(s, unsafe_allow_html=True)
    
    #masquer le menu streamlit
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    menu = ["Accueil", "Connexion", "Inscription"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Accueil":
        components.html("""

			<style>
			* {box-sizing: border-box}
			body {font-family: Verdana, sans-serif; margin:0}
			.mySlides {display: none}
			img {vertical-align: middle;}

			/* Slideshow container */
			.slideshow-container {
			  max-width: 1000px;
			  position: relative;
			  margin: auto;
			}

			/* Next & previous buttons */
			.prev, .next {
			  cursor: pointer;
			  position: absolute;
			  top: 50%;
			  width: auto;
			  padding: 16px;
			  margin-top: -22px;
			  color: white;
			  font-weight: bold;
			  font-size: 18px;
			  transition: 0.6s ease;
			  border-radius: 0 3px 3px 0;
			  user-select: none;
			}

			/* Position the "next button" to the right */
			.next {
			  right: 0;
			  border-radius: 3px 0 0 3px;
			}

			/* On hover, add a black background color with a little bit see-through */
			.prev:hover, .next:hover {
			  background-color: rgba(0,0,0,0.8);
			}

			/* Caption text */
			.text {
			  color: #f2f2f2;
			  font-size: 15px;
			  padding: 8px 12px;
			  position: absolute;
			  bottom: 8px;
			  width: 100%;
			  text-align: center;
			}

			/* Number text (1/3 etc) */
			.numbertext {
			  color: #f2f2f2;
			  font-size: 12px;
			  padding: 8px 12px;
			  position: absolute;
			  top: 0;
			}

			/* The dots/bullets/indicators */
			.dot {
			  cursor: pointer;
			  height: 15px;
			  width: 15px;
			  margin: 0 2px;
			  background-color: #bbb;
			  border-radius: 50%;
			  display: inline-block;
			  transition: background-color 0.6s ease;
			}

			.active, .dot:hover {
			  background-color: #717171;
			}

			/* Fading animation */
			.fade {
			  -webkit-animation-name: fade;
			  -webkit-animation-duration: 1.5s;
			  animation-name: fade;
			  animation-duration: 1.5s;
			}

			@-webkit-keyframes fade {
			  from {opacity: .4} 
			  to {opacity: 1}
			}

			@keyframes fade {
			  from {opacity: .4} 
			  to {opacity: 1}
			}

			/* On smaller screens, decrease text size */
			@media only screen and (max-width: 300px) {
			  .prev, .next,.text {font-size: 11px}
			}
			</style>
			</head>
			<body>

			<div class="slideshow-container">

			<div class="mySlides fade">
			  <div class="numbertext">1 / 3</div>
			  <img src="https://cdn.shopify.com/s/files/1/2382/6729/products/SP124958.jpg?v=1536179866" style="width:100%;border-radius:5px;">
			  <div class="text"></div>
			</div>

			<div class="mySlides fade">
			  <div class="numbertext">2 / 3</div>

			  <img src="https://www.hsetrain.org/images/slide1.jpg" style="width:100%;border-radius:5px;">
			  <div class="text"></div>
			</div>

			<div class="mySlides fade">
			  <div class="numbertext">3 / 3</div>
			  <img src="https://www.spc.com.sg/wp-content/uploads/2015/11/banner-community-society-hse.jpg" style="width:100%;border-radius:5px;">
			  <div class="text"></div>
			</div>

			<a class="prev" onclick="plusSlides(-1)">&#10094;</a>
			<a class="next" onclick="plusSlides(1)">&#10095;</a>

			</div>
			<br>

			<div style="text-align:center">
			  <span class="dot" onclick="currentSlide(1)"></span> 
			  <span class="dot" onclick="currentSlide(2)"></span> 
			  <span class="dot" onclick="currentSlide(3)"></span> 
			</div>

			<script>
			var slideIndex = 1;
			showSlides(slideIndex);

			function plusSlides(n) {
			  showSlides(slideIndex += n);
			}

			function currentSlide(n) {
			  showSlides(slideIndex = n);
			}

			function showSlides(n) {
			  var i;
			  var slides = document.getElementsByClassName("mySlides");
			  var dots = document.getElementsByClassName("dot");
			  if (n > slides.length) {slideIndex = 1}    
			  if (n < 1) {slideIndex = slides.length}
			  for (i = 0; i < slides.length; i++) {
			      slides[i].style.display = "none";  
			  }
			  for (i = 0; i < dots.length; i++) {
			      dots[i].className = dots[i].className.replace(" active", "");
			  }
			  slides[slideIndex-1].style.display = "block";  
			  dots[slideIndex-1].className += " active";
			}
			</script>


			""")
        html_temp = """
		<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:3px;">
		<h2 style="color:white;text-align:center;"><b>HSE KPI RECORDER</b></h2>
		<h3 style="color:white;text-align:center;">Application d'analyse et de suivi des indicateurs de performance HSE</h3>
		</div>
		"""
        #components.html(html_temp)
        st.markdown(html_temp, unsafe_allow_html = True)
        col1, col2, col3 = st.beta_columns([1,6,1])
        with col2:
            st.image("https://i0.wp.com/www.aprentiv.com/wp-content/uploads/2017/04/Pr%C3%A9sentation-des-normes-dhygi%C3%A8ne-et-s%C3%A9curit%C3%A9-%C3%A0-respecter-en-entreprise.png",width=400,)
        

        user_input = get_text()
        response = bot_initialize(user_msg)
        st.text_area("Bot:", value=response, height=200, max_chars=None, key=None)

    elif choice == "Connexion":
        st.subheader("Section Connexion")
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Mot de passe",type='password')
        if st.sidebar.checkbox("Connexion"):
            # if password == '12345':
            create_table()
            hashed_pswd = make_hashes(password)



            result = login_user(email,check_hashes(password,hashed_pswd))
            if result:
                st.success("Connecté en tant que {}".format(email))
                #task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
                task = ""
                if task == "":
                    st.subheader("")
                    
                    image_temp ="""
                    <div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
		    <img src="https://1tpecash.fr/wp-content/uploads/elementor/thumbs/Renaud-Louis-osf6t5lcki4q31uzfafpi9yx3zp4rrq7je8tj6p938.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
		    <br/>
		    <p style="color:white;text-align:justify">Bienvenue ! Je vous souhaite une bonne expérience, ce travail est le fruit de mes expériences en tant que Manager HSE et Data scientist vos avis à propos sont les bienvenues.</p>
		    </div>
                    """
                    title_temp = """
                	<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
                	<h1 style ="color:white;text-align:center;"> GESTION DES INDICATEURS HSE </h1>
                	</div>
                	"""
                    st.markdown(image_temp, unsafe_allow_html = True)
                    st.markdown(title_temp, unsafe_allow_html = True)
                    #st.markdown('### GESTION DES INDICATEURS HSE')
                    style()
                    choix = st.selectbox("", ["AJOUTER", "AFFICHER", "METTRE À JOUR", "SUPPRIMER"])
                    if choix == "AJOUTER":
                        st.subheader("AJOUTER DES DONNÉES")
                        col1, col2= st.beta_columns(2)
                        with col1:
                            st.subheader("CIBLE A ENREGISTRER")
                            
                            style()
                            cible = st.selectbox('', ['Accueil sécurité','Briefing de sécurité( TBM)','Non conformité','Changements enregistrés','Anomalies','Analyse des risques réalisés(JSA)','Incident & Accident',"Audit-Inspection-Exercice d'urgence"])
                            #connexion à l'interface et recupération des données
                            if cible == 'Accueil sécurité':
                                with col1:
                                    Nbre_Arrivant =inputcheck(st.text_input("Nombre Arrivant",value=0))
                                    Nbre_induction = inputcheck(st.text_input("Nombre d'induction",value=0))
                                    IDD=email
                                with col2:
                                    st.subheader("DATE ET NOM DU CHANTIER")
                                    Date = st.date_input("Date")
                                    Chantier = st.text_input("Chantier")
                                    button1=st.button("AJOUTER LES DÉTAILS")
                                if button1:
                                    add_Accueil(IDD,Chantier,Nbre_Arrivant,Nbre_induction,Date)
                                    st.success("AJOUTÉ AVEC SUCCÈS: {}".format(Chantier))

                            elif cible == 'Briefing de sécurité( TBM)':
                                with col1:
                                    Nbre_chantier =inputcheck(st.text_input("Nombre de chantier",value=0))
                                    Nbre_TBM = inputcheck(st.text_input("Nombre de TBM",value=0))
                                    IDD=email
                                with col2:
                                    st.subheader("DATE ET NOM DU CHANTIER")
                                    Date = st.date_input("Date")
                                    Chantier = st.text_input("Chantier")
                                    button2=st.button("AJOUTER LES DÉTAILS")
                                if button2:
                                    add_TBM(IDD,Chantier,Nbre_chantier,Nbre_TBM,Date)
                                    st.success("AJOUTÉ AVEC SUCCÈS: {}".format(Chantier))
                            elif cible == 'Non conformité':
                                with col1:
                                    NCR = inputcheck(st.text_input("Nombre de Non conformité remontée",value=0,key=0))
                                    FNCR = inputcheck(st.text_input("Nombre de fiche de Non conformité remontée",value=0,key=1))
                                    NCC = inputcheck(st.text_input("Nombre de Non conformité cloturée",value=0,key=2))
                                    FNCC= inputcheck(st.text_input("Nombre de fiche de Non conformité cloturée",value=0, key=3))
                                    IDD=email
                                with col2:
                                    st.subheader("DATE ET NOM DU CHANTIER")
                                    Date = st.date_input("Date")
                                    Chantier = st.text_input("Chantier")
                                    button3=st.button("AJOUTER LES DÉTAILS")
                                if button3:
                                    add_NC(IDD,Chantier,NCR,FNCR,NCC,FNCC,Date)
                                    st.success("AJOUTÉ AVEC SUCCÈS: {}".format(Chantier))
                            elif cible == "Changements enregistrés":
                                with col1:
                                    NCH = inputcheck(st.text_input("Nombre de Changement enregistrés",value=0))
                                    FNCH = inputcheck(st.text_input("Nombre de fiche de Changements enregistrés",value=0))
                                    NCHC  = inputcheck(st.text_input("Nombre de Changements cloturés",value=0))
                                    FNCHC= inputcheck(st.text_input("Nombre de fiche de  Changements suivis et cloturés",value=0))
                                    IDD=email
                                with col2:
                                    st.subheader("DATE ET NOM DU CHANTIER")
                                    Date = st.date_input("Date")
                                    Chantier = st.text_input("Chantier")
                                    button4=st.button("AJOUTER LES DÉTAILS")
                                if button4:
                                    add_Changements(IDD,Chantier,NCH,FNCH,NCHC,FNCHC,Date)
                                    st.success("AJOUTÉ AVEC SUCCÈS: {}".format(Chantier))
                            elif cible == "Anomalies":
                                with col1:
                                    NA = inputcheck(st.text_input("Nombre d'Anomalies Remontées",value=0))
                                    FNA = inputcheck(st.text_input("Nombre de fiche d'Anomalies Remontées",value=0))
                                    NAC = inputcheck(st.text_input("Nombre d' Anomalies cloturés",value=0))
                                    FNAC = inputcheck(st.text_input("Nombre de fiche de  Anomalies Corrigées",value=0))
                                    IDD=email
                                with col2:
                                    st.subheader("DATE ET NOM DU CHANTIER")
                                    Date = st.date_input("Date")
                                    Chantier = st.text_input("Chantier")
                                    button5=st.button("AJOUTER LES DÉTAILS")
                                if button5:
                                    add_Anomalies(IDD,Chantier,NA,FNA,NAC,FNAC,Date)
                                    st.success("AJOUTÉ AVEC SUCCÈS: {}".format(Chantier))
                            elif cible == "Analyse des risques réalisés(JSA)":
                                with col1:
                                    NAct = inputcheck(st.text_input("Nombre d'Activite",value=0))
                                    NJSA = inputcheck(st.text_input("Nombre de fiche JSA",value=0))
                                    IDD=email
                                with col2:
                                    st.subheader("DATE ET NOM DU CHANTIER")
                                    Date = st.date_input("Date")
                                    Chantier = st.text_input("Chantier")
                                    button6=st.button("AJOUTER LES DÉTAILS")
                                if button6:
                                    add_JSA(IDD,Chantier,NAct,NJSA,Date)
                                    st.success("AJOUTÉ AVEC SUCCÈS: {}".format(Chantier))
                            elif cible == "Incident & Accident":
                                with col1:
                                    AAA = inputcheck(st.text_input("Accident Avec Arrêt",value=0))
                                    NJP = inputcheck(st.text_input("Nombre de jours perdus",value=0))
                                    ASA = inputcheck(st.text_input("Accident Sans Arrêt",value=0))
                                    AT = inputcheck(st.text_input("Nombre d'accident de trajet",value=0))
                                    NInc = inputcheck(st.text_input("Incident",value=0))
                                    IDD=email
                                with col2:
                                    st.subheader("DATE ET NOM DU CHANTIER")
                                    Date = st.date_input("Date")
                                    Chantier = st.text_input("Chantier")
                                    button7=st.button("AJOUTER LES DÉTAILS")
                                if button7:
                                    add_Incident_Accident(IDD,Chantier,NInc,AAA,ASA,AT,NJP,Date)
                                    st.success("AJOUTÉ AVEC SUCCÈS: {}".format(Chantier))
                            elif cible == "Audit-Inspection-Exercice d'urgence":
                                with col1:
                                    AC= inputcheck(st.text_input("Nombre d'audit",value=0))
                                    VC= inputcheck(st.text_input("Nombre de Visite Conjointe",value=0))
                                    NEU= inputcheck(st.text_input("Nombre d'exercice d'urgence",value=0))
                                    SMPAR= inputcheck(st.text_input("Sensibilisation au modes de prévention des activités à risques",value=0))
                                    PR= inputcheck(st.text_input("Procedures réalisées",value=0))
                                    IE= inputcheck(st.text_input("Inspections Environnementales",value=0))
                                    IDD=email
                                with col2:
                                    st.subheader("DATE ET NOM DU CHANTIER")
                                    Date = st.date_input("Date")
                                    Chantier = st.text_input("Chantier")
                                    button8=st.button("AJOUTER LES DÉTAILS")
                                if button8:
                                    add_Audit(IDD,Chantier,AC,VC,NEU,SMPAR,PR,IE,Date)
                                    st.success("AJOUTÉ AVEC SUCCÈS: {}".format(Chantier))

                    #visualisation des données
                    elif choix == "AFFICHER":
                        st.subheader("AFFICHEZ VOS DONNÉES")
                        st.warning("Si vous faites des enregistrements à une date antérieure à celle de votre inscription veuillez spécifier l'intervalle de date, car l'affichage des données est par défaut à partir de votre jour d'inscription.")
                        ACCUEIL_exp= st.beta_expander("ACCUEIL SECURITÉ")
                        with ACCUEIL_exp:
                            df_Accueil = pd.DataFrame(view_Accueil(), columns=["id","IDD","Chantier","Nbre_Arrivant","Nbre_induction","Date"])

                            #pour voir uniquement les donnée de l'user connecté
                            IDD2 = email.strip('][').split(', ')

                            #ACCUEIL
                            @st.cache
                            def Accueil_2(df_Accueil: pd.DataFrame) -> pd.DataFrame:
                                df_Accueil2 = df_Accueil[(df_Accueil["IDD"].isin(IDD2))]
                                return df_Accueil2.loc[1:, ["id","Chantier","Nbre_Arrivant","Nbre_induction","Date"]]

                            # Pour empêcher l'affichage d'erreur en cas de donnée vide
                            try:
                                df_Accueil1 = Accueil_2(df_Accueil)
                            except:
                                st.error("Nous ne pouvons afficher, car vous n'avez pas de donnée enregistrée.")
                                st.stop()

                            df_Accueil1['Date'] = pd.to_datetime(df_Accueil1['Date']).apply(lambda x: x.date())
                            df_Accueil1.sort_values(by=['Date'], inplace=True)

                            #intervalle de date
                            st.write('SELECTIONNEZ UN INTERVALLE DE DATE POUR VOTRE GRILLE')
                            try:
                                miny= st.date_input('MinDate',min(df_Accueil1['Date']))
                                maxy= st.date_input('MaxDate',max(df_Accueil1['Date']))
                            except:
                                st.error("Nous ne pouvons afficher, car vous n'avez pas au moins deux dates enregistrées.")
                                st.stop()


                            #filtrage par chantier
                            splitted_df_Accueil1 = df_Accueil1['Chantier'].str.split(',')
                            unique_vals1 = list(dict.fromkeys([y for x in splitted_df_Accueil1  for y in x]).keys())
                            filtrechantier = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals1,key=0)
                            
                            mask = (df_Accueil1['Date'] > miny) & (df_Accueil1['Date'] <= maxy) & (df_Accueil1['Chantier'] == filtrechantier)
                            df_filter1=df_Accueil1.loc[mask]
                            st.dataframe(df_filter1)
                            st.text("*Nbre_Arrivant: Nombre d'arrivant\n*Nbre_induction: Nombre d'induction")

                            if st.button("Télécharger",key=0):
                                st.markdown(get_table_download_link(df_filter1), unsafe_allow_html=True)
                            #figure
                            df_filter1['Nbre_Arrivant'] = pd.to_numeric(df_filter1['Nbre_Arrivant'])
                            df_filter1['Nbre_induction'] = pd.to_numeric(df_filter1['Nbre_induction'])
                            Objectf_fixé= df_filter1['Nbre_Arrivant'].sum()
                            Objectif_atteint = df_filter1['Nbre_induction'].sum()
                            df_filter1_df = pd.DataFrame(columns=["Nombre d'arrivant", "Nombre d'induction"])
                            df_filter1_df.at[0, "Nombre d'arrivant"] = Objectf_fixé
                            df_filter1_df.at[0, "Nombre d'induction"] = Objectif_atteint
                            df_filter1_df_melt = pd.melt(df_filter1_df)
                            df_filter1_df_melt.columns = ['variable', 'valeur']

                            st.dataframe(df_filter1_df_melt)

                            fig = px.bar(df_filter1_df_melt, x = 'variable', y = 'valeur',color="variable")
                            st.plotly_chart(fig, use_container_width=True)


                        BRIEFING_exp= st.beta_expander("BRIEFING DE SÉCURITÉ( TBM)")
                        with BRIEFING_exp:
                            #TMB
                            df_TBM = pd.DataFrame(view_TBM(), columns=["id","IDD","Chantier","Nbre_chantier","Nbre_TBM","Date"])
                            IDD2 = email.strip('][').split(', ')
			    
                            @st.cache
                            def TBM_2(df_TBM: pd.DataFrame) -> pd.DataFrame:
                                df_TBM2 = df_TBM[(df_TBM["IDD"].isin(IDD2))]
                                return df_TBM2.loc[1:, ["id","Chantier","Nbre_chantier","Nbre_TBM","Date"]]

                            # Pour empêcher l'affichage d'erreur en cas de donnée vide
                            try:
                                df_TBM1 = TBM_2(df_TBM)
                            except:
                                st.error("Nous ne pouvons afficher, car vous n'avez pas de donnée enregistrée.")
                                st.stop()


                            df_TBM1['Date'] = pd.to_datetime(df_TBM1['Date']).apply(lambda x: x.date())
                            df_TBM1.sort_values(by=['Date'], inplace=True)

                            #intervalle de date
                            st.write('SELECTIONNEZ UN INTERVALLE DE DATE POUR VOTRE GRILLE')
                            try:
                                miny= st.date_input('MinDate',min(df_TBM1['Date']),key=0)
                                maxy= st.date_input('MaxDate',max(df_TBM1['Date']),key=0)
                            except:
                                st.error("Nous ne pouvons afficher, car vous n'avez pas au moins deux dates enregistrées.")
                                st.stop()

                            #filtrage par chantier
                            splitted_df_TBM1 = df_TBM1['Chantier'].str.split(',')
                            unique_vals2 = list(dict.fromkeys([y for x in splitted_df_TBM1  for y in x]).keys())
                            filtrechantier2 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals2,key=1)
                            
                            mask = (df_TBM1['Date'] > miny) & (df_TBM1['Date'] <= maxy) & (df_TBM1['Chantier'] == filtrechantier2)
                            df_filter2=df_TBM1.loc[mask]
                            st.dataframe(df_filter2)
                            st.text("*Nbre_chantier: Nombre de chantier\n*Nbre_TBM: Nombre de TBM")

                            if st.button("Télécharger", key=1):
                                st.markdown(get_table_download_link(df_filter2), unsafe_allow_html=True)
                            #figure
                            df_filter2['Nbre_chantier'] = pd.to_numeric(df_filter2['Nbre_chantier'])
                            df_filter2['Nbre_TBM'] = pd.to_numeric(df_filter2['Nbre_TBM'])
                            Objectf_fixé2= df_filter2['Nbre_chantier'].sum()
                            Objectif_atteint2 = df_filter2['Nbre_TBM'].sum()
                            df_filter2_df = pd.DataFrame(columns=["Nombre de chantier", "Nombre de TBM"])
                            df_filter2_df.at[0, "Nombre de chantier"] = Objectf_fixé2
                            df_filter2_df.at[0, "Nombre de TBM"] = Objectif_atteint2
                            df_filter2_df_melt = pd.melt(df_filter2_df)
                            df_filter2_df_melt.columns = ['variable', 'valeur']

                            st.dataframe(df_filter2_df_melt)

                            figTBM = px.bar(df_filter2_df_melt, x = 'variable', y = 'valeur',color="variable")
                            st.plotly_chart(figTBM, use_container_width=True)


                        CONFORMITÉ_exp= st.beta_expander("NON CONFORMITÉ")
                        with CONFORMITÉ_exp:
                            #NON CONFORMITÉ
                            df_NC = pd.DataFrame(view_NC(), columns=["id","IDD","Chantier","NCR","FNCR","NCC","FNCC","Date"])
                            IDD2 = email.strip('][').split(', ')

			    
                            @st.cache
                            def NC_2(df_NC: pd.DataFrame) -> pd.DataFrame:
                                df_NC2 = df_NC[(df_NC["IDD"].isin(IDD2))]
                                return df_NC2.loc[1:, ["id","Chantier","NCR","FNCR","NCC","FNCC","Date"]]

                            # Pour empêcher l'affichage d'erreur en cas de donnée vide
                            try:
                                df_NC1 = NC_2(df_NC)
                            except:
                                st.error("Nous ne pouvons afficher, car vous n'avez pas de donnée enregistrée.")
                                st.stop()

                            df_NC1['Date'] = pd.to_datetime(df_NC1['Date']).apply(lambda x: x.date())
                            df_NC1.sort_values(by=['Date'], inplace=True)

                            #intervalle de date
                            st.write('SELECTIONNEZ UN INTERVALLE DE DATE POUR VOTRE GRILLE')
                            try:
                                miny= st.date_input('MinDate',min(df_NC1['Date']),key=1)
                                maxy= st.date_input('MaxDate',max(df_NC1['Date']),key=1)

                            except:
                                st.error("Nous ne pouvons afficher car vous n'avez pas aumoins deux dates enrégistrées.")
                                st.stop()



                            #filtrage par chantier
                            splitted_df_NC1 = df_NC1['Chantier'].str.split(',')
                            unique_vals3 = list(dict.fromkeys([y for x in splitted_df_NC1  for y in x]).keys())
                            filtrechantier3 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals3,key=2)
                            
                            mask = (df_NC1['Date'] > miny) & (df_NC1['Date'] <= maxy) & (df_NC1['Chantier'] == filtrechantier3)
                            df_filter3=df_NC1.loc[mask]
                            st.dataframe(df_filter3)
                            st.text("*NCR: Non conformité remontée\n*FNCR: Nombre de fiche de Non conformité remontée\n*NCC: Nombre de Non conformité cloturée\n*FNCC:Nombre de fiche de Non conformité cloturée")


                            if st.button("Télécharger", key=2):
                                st.markdown(get_table_download_link(df_filter3), unsafe_allow_html=True)
                            #figure
                            df_filter3['NCR'] = pd.to_numeric(df_filter3['NCR'])
                            df_filter3['NCC'] = pd.to_numeric(df_filter3['NCC'])
                            df_filter3['FNCR'] = pd.to_numeric(df_filter3['FNCR'])
                            df_filter3['FNCC'] = pd.to_numeric(df_filter3['FNCC'])

                            Objectf_fixe3 = df_filter3['NCR'].sum()
                            Objectif_atteint3 = df_filter3['NCC'].sum()
                            Objectf_fixe4= df_filter3['FNCR'].sum()
                            Objectif_atteint4 = df_filter3['FNCC'].sum()

                            df_filter3_df1 = pd.DataFrame(columns=["NCR", "NCC"])
                            df_filter3_df2 = pd.DataFrame(columns=["FNCR", "FNCC"])

                            df_filter3_df1.at[0, "NCR"] = Objectf_fixe3
                            df_filter3_df1.at[0, "NCC"] = Objectif_atteint3
                            df_filter3_df2.at[0, "FNCR"] = Objectf_fixe4
                            df_filter3_df2.at[0, "FNCC"] = Objectif_atteint4

                            df_filter3_df_melt1 = pd.melt(df_filter3_df1)
                            df_filter3_df_melt2 = pd.melt(df_filter3_df2)

                            df_filter3_df_melt1.columns = ['variable', 'valeur']
                            df_filter3_df_melt2.columns = ['variable', 'valeur']

                            st.dataframe(df_filter3_df_melt1)
                            st.dataframe(df_filter3_df_melt2)

                            figNC1 = px.bar(df_filter3_df_melt1, x = 'variable', y = 'valeur',color="variable")
                            figNC2 = px.bar(df_filter3_df_melt2, x = 'variable', y = 'valeur',color="variable")

                            st.plotly_chart(figNC1, use_container_width=True)
                            st.plotly_chart(figNC2, use_container_width=True)



                        CHANGEMENTS_exp= st.beta_expander("CHANGEMENTS ENREGISTRÉS")
                        with CHANGEMENTS_exp:
                            #CHANGEMENTS
                            df_Changements = pd.DataFrame(view_Changements(), columns=["id","IDD","Chantier","NCH","FNCH","NCHC","FNCHC","Date"])
                            IDD2 = email.strip('][').split(', ')
			
                            @st.cache
                            def Changements_2(df_Changements: pd.DataFrame) -> pd.DataFrame:
                                df_Changements2 = df_Changements[(df_Changements["IDD"].isin(IDD2))]
                                return df_Changements2.loc[1:, ["id","Chantier","NCH","FNCH","NCHC","FNCHC","Date"]]

                            # Pour empêcher l'affichage d'erreur en cas de donnée vide
                            try:
                                df_Changements1 = Changements_2(df_Changements)
                            except:
                                st.error("Nous ne pouvons afficher, car vous n'avez pas de donnée enregistrée.")
                                st.stop()

                            df_Changements1['Date'] = pd.to_datetime(df_Changements1['Date']).apply(lambda x: x.date())
                            df_Changements1.sort_values(by=['Date'], inplace=True)

                            #intervalle de date
                            st.write('SELECTIONNEZ UN INTERVALLE DE DATE POUR VOTRE GRILLE')
                            try:
                                miny= st.date_input('MinDate',min(df_Changements1['Date']),key=2)
                                maxy= st.date_input('MaxDate',max(df_Changements1['Date']),key=2)
                            except:
                                st.error("Nous ne pouvons afficher car vous n'avez pas aumoins deux dates enrégistrées")
                                st.stop()


                            #filtrage par chantier
                            splitted_df_Changements1 = df_Changements1['Chantier'].str.split(',')
                            unique_vals4 = list(dict.fromkeys([y for x in splitted_df_Changements1  for y in x]).keys())
                            filtrechantier4 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals4,key=3)
                            
                            mask = (df_Changements1['Date'] > miny) & (df_Changements1['Date'] <= maxy) & (df_Changements1['Chantier'] == filtrechantier4)
                            df_filter4=df_Changements1.loc[mask]
                            st.dataframe(df_filter4)
                            st.text("*NCH: Nombre de Changement enregistrés\n*FNCH: Nombre de fiche de Changements enregistrés\n*NCHC: Nombre de Changements cloturés\n*FNCHC:Nombre de fiche de Changements suivis et cloturés")



                            if st.button("Télécharger", key=3):
                                st.markdown(get_table_download_link(df_filter4), unsafe_allow_html=True)
                            #figure
                            df_filter4['NCH'] = pd.to_numeric(df_filter4['NCH'])
                            df_filter4['NCHC'] = pd.to_numeric(df_filter4['NCHC'])
                            df_filter4['FNCH'] = pd.to_numeric(df_filter4['FNCH'])
                            df_filter4['FNCHC'] = pd.to_numeric(df_filter4['FNCHC'])

                            Objectf_fixe4 = df_filter4['NCH'].sum()
                            Objectif_atteint4 = df_filter4['NCHC'].sum()
                            Objectf_fixe5= df_filter4['FNCH'].sum()
                            Objectif_atteint5 = df_filter4['FNCHC'].sum()

                            df_filter4_df1 = pd.DataFrame(columns=["NCH", "NCHC"])
                            df_filter4_df2 = pd.DataFrame(columns=["FNCH", "FNCHC"])

                            df_filter4_df1.at[0, "NCH"] = Objectf_fixe4
                            df_filter4_df1.at[0, "NCHC"] = Objectif_atteint4
                            df_filter4_df2.at[0, "FNCH"] = Objectf_fixe5
                            df_filter4_df2.at[0, "FNCHC"] = Objectif_atteint5

                            df_filter4_df_melt1 = pd.melt(df_filter4_df1)
                            df_filter4_df_melt2 = pd.melt(df_filter4_df2)

                            df_filter4_df_melt1.columns = ['variable', 'valeur']
                            df_filter4_df_melt2.columns = ['variable', 'valeur']

                            st.dataframe(df_filter4_df_melt1)
                            st.dataframe(df_filter4_df_melt2)

                            figCH1 = px.bar(df_filter4_df_melt1, x = 'variable', y = 'valeur',color="variable")
                            figCH2 = px.bar(df_filter4_df_melt2, x = 'variable', y = 'valeur',color="variable")

                            st.plotly_chart(figCH1, use_container_width=True)
                            st.plotly_chart(figCH2, use_container_width=True)

                        ANOMALIES_exp= st.beta_expander("ANOMALIES")
                        with ANOMALIES_exp:
                            #ANOMALIES
                            df_Anomalies = pd.DataFrame(view_Anomalies(), columns=["id","IDD","Chantier","NA","FNA","NAC","FNAC","Date"])
                            IDD2 = email.strip('][').split(', ')
			    
                            @st.cache
                            def Anomalies_2(df_Anomalies: pd.DataFrame) -> pd.DataFrame:
                                df_Anomalies2 = df_Anomalies[(df_Anomalies["IDD"].isin(IDD2))]
                                return df_Anomalies2.loc[1:, ["id","Chantier","NA","FNA","NAC","FNAC","Date"]]

                            # Pour empêcher l'affichage d'erreur en cas de donnée vide
                            try:
                                df_Anomalies1 = Anomalies_2(df_Anomalies)
                            except:
                                st.error("Nous ne pouvons afficher, car vous n'avez pas de donnée enregistrée.")
                                st.stop()

                            df_Anomalies1['Date'] = pd.to_datetime(df_Anomalies1['Date']).apply(lambda x: x.date())
                            df_Anomalies1.sort_values(by=['Date'], inplace=True)

                            #intervalle de date
                            st.write('SELECTIONNEZ UN INTERVALLE DE DATE POUR VOTRE GRILLE')
                            try:
                                miny= st.date_input('MinDate',min(df_Anomalies1['Date']),key=3)
                                maxy= st.date_input('MaxDate',max(df_Anomalies1['Date']),key=3)
                            except:
                                st.error("Nous ne pouvons afficher car vous n'avez pas aumoins deux dates enrégistrées")
                                st.stop()


                            #filtrage par chantier
                            splitted_df_Anomalies1 = df_Anomalies1['Chantier'].str.split(',')
                            unique_vals5 = list(dict.fromkeys([y for x in splitted_df_Anomalies1  for y in x]).keys())
                            filtrechantier5 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals5,key=4)
                            
                            mask = (df_Anomalies1['Date'] > miny) & (df_Anomalies1['Date'] <= maxy) & (df_Anomalies1['Chantier'] == filtrechantier5)
                            df_filter5=df_Anomalies1.loc[mask]
                            st.dataframe(df_filter5)
                            st.text("*NA: Nombre d'anomalies enregistrés\n*FNA: Nombre de fiche d'anomalies enregistrés\n*NAC: Nombre d'anomalies Corrigées\n*FNAC:Nombre de fiche d'anomalies Corrigées")

                            if st.button("Télécharger", key=4):
                                st.markdown(get_table_download_link(df_filter5), unsafe_allow_html=True)
                            #figure
                            df_filter5['NA'] = pd.to_numeric(df_filter5['NA'])
                            df_filter5['NAC'] = pd.to_numeric(df_filter5['NAC'])
                            df_filter5['FNA'] = pd.to_numeric(df_filter5['FNA'])
                            df_filter5['FNAC'] = pd.to_numeric(df_filter5['FNAC'])

                            Objectf_fixe5 = df_filter5['NA'].sum()
                            Objectif_atteint5 = df_filter5['NAC'].sum()
                            Objectf_fixe6= df_filter5['FNA'].sum()
                            Objectif_atteint6 = df_filter5['FNAC'].sum()

                            df_filter5_df1 = pd.DataFrame(columns=["NA", "NAC"])
                            df_filter5_df2 = pd.DataFrame(columns=["FNA", "FNAC"])

                            df_filter5_df1.at[0, "NA"] = Objectf_fixe5
                            df_filter5_df1.at[0, "NAC"] = Objectif_atteint5
                            df_filter5_df2.at[0, "FNA"] = Objectf_fixe6
                            df_filter5_df2.at[0, "FNAC"] = Objectif_atteint6

                            df_filter5_df_melt1 = pd.melt(df_filter5_df1)
                            df_filter5_df_melt2 = pd.melt(df_filter5_df2)

                            df_filter5_df_melt1.columns = ['variable', 'valeur']
                            df_filter5_df_melt2.columns = ['variable', 'valeur']

                            st.dataframe(df_filter5_df_melt1)
                            st.dataframe(df_filter5_df_melt2)

                            figNA1 = px.bar(df_filter5_df_melt1, x = 'variable', y = 'valeur',color="variable")
                            figNA2 = px.bar(df_filter5_df_melt2, x = 'variable', y = 'valeur',color="variable")

                            st.plotly_chart(figNA1, use_container_width=True)
                            st.plotly_chart(figNA2, use_container_width=True)

                        ANALYSE_exp= st.beta_expander("ANALYSE DES RISQUES RÉALISÉS(JSA)")
                        with ANALYSE_exp:
                            #JSA
                            df_JSA = pd.DataFrame(view_JSA(), columns=["id","IDD","Chantier","NAct","NJSA","Date"])
                            IDD2 = email.strip('][').split(', ')
			    
                            @st.cache
                            def JSA_2(df_JSA: pd.DataFrame) -> pd.DataFrame:
                                df_JSA2 = df_JSA[(df_JSA["IDD"].isin(IDD2))]
                                return df_JSA2.loc[1:, ["id","Chantier","NAct","NJSA","Date"]]

                            # Pour empêcher l'affichage d'erreur en cas de donnée vide
                            try:
                                df_JSA1 = JSA_2(df_JSA)
                            except:
                                st.error("Nous ne pouvons afficher, car vous n'avez pas de donnée enregistrée.")
                                st.stop()


                            df_JSA1['Date'] = pd.to_datetime(df_JSA1['Date']).apply(lambda x: x.date())
                            df_JSA1.sort_values(by=['Date'], inplace=True)

                            #intervalle de date
                            st.write('SELECTIONNEZ UN INTERVALLE DE DATE POUR VOTRE GRILLE')
                            try:
                                miny= st.date_input('MinDate',min(df_JSA1['Date']),key=4)
                                maxy= st.date_input('MaxDate',max(df_JSA1['Date']),key=4)

                            except:
                                st.error("Nous ne pouvons afficher, car vous n'avez pas au moins deux dates enregistrées.")
                                st.stop()

                            #filtrage par chantier
                            splitted_df_JSA1 = df_JSA1['Chantier'].str.split(',')
                            unique_vals6 = list(dict.fromkeys([y for x in splitted_df_JSA1  for y in x]).keys())
                            filtrechantier6 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals6,key=5)
                            
                            mask = (df_JSA1['Date'] > miny) & (df_JSA1['Date'] <= maxy) & (df_JSA1['Chantier'] == filtrechantier6)
                            df_filter6=df_JSA1.loc[mask]
                            st.dataframe(df_filter6)
                            st.text("*NAct: Nombre d'activité\n*NJSA: Analyse des risques réalisés")

                            if st.button("Télécharger", key=5):
                                st.markdown(get_table_download_link(df_filter6), unsafe_allow_html=True)
                            #figure
                            df_filter6['NAct'] = pd.to_numeric(df_filter6['NAct'])
                            df_filter6['NJSA'] = pd.to_numeric(df_filter6['NJSA'])
                            Objectf_fixé6= df_filter6['NAct'].sum()
                            Objectif_atteint6 = df_filter6['NJSA'].sum()
                            df_filter6_df = pd.DataFrame(columns=["NAct", "NJSA"])
                            df_filter6_df.at[0, "NAct"] = Objectf_fixé6
                            df_filter6_df.at[0, "NJSA"] = Objectif_atteint6
                            df_filter6_df_melt = pd.melt(df_filter6_df)
                            df_filter6_df_melt.columns = ['variable', 'valeur']

                            st.dataframe(df_filter6_df_melt)

                            figJSA = px.bar(df_filter6_df_melt, x = 'variable', y = 'valeur',color="variable")
                            st.plotly_chart(figJSA, use_container_width=True)



                        INCIDENT_exp= st.beta_expander("INCIDENT & ACCIDENT")
                        with INCIDENT_exp:

                            #IA
                            df_IA = pd.DataFrame(view_Incident_Accident(), columns=["id","IDD","Chantier","NInc","AAA","ASA","AT","NJP","Date"])
                            IDD2 = email.strip('][').split(', ')
			    
                            @st.cache
                            def IA_2(df_IA: pd.DataFrame) -> pd.DataFrame:
                                df_IA = df_IA[(df_IA["IDD"].isin(IDD2))]
                                return df_IA.loc[1:, ["id","Chantier","NInc","AAA","ASA","AT","NJP","Date"]]

                            # Pour empêcher l'affichage d'erreur en cas de donnée vide
                            try:
                                df_IA1 = IA_2(df_IA)
                            except:
                                st.error("Nous ne pouvons afficher, car vous n'avez pas de donnée enregistrée.")
                                st.stop()

                            df_IA1['Date'] = pd.to_datetime(df_IA1['Date']).apply(lambda x: x.date())
                            df_IA1.sort_values(by=['Date'], inplace=True)

                            #intervalle de date
                            st.write('SELECTIONNEZ UN INTERVALLE DE DATE POUR VOTRE GRILLE')
                            try:
                                miny= st.date_input('MinDate',min(df_IA1['Date']),key=5)
                                maxy= st.date_input('MaxDate',max(df_IA1['Date']),key=5)
                            except:
                                st.error("Nous ne pouvons afficher car vous n'avez pas aumoins deux dates enrégistrées")
                                st.stop()


                            #filtrage par chantier
                            splitted_df_IA1 = df_IA1['Chantier'].str.split(',')
                            unique_vals7 = list(dict.fromkeys([y for x in splitted_df_IA1  for y in x]).keys())
                            filtrechantier7 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals7,key=6)
                            
                            mask = (df_IA1['Date'] > miny) & (df_IA1['Date'] <= maxy) & (df_IA1['Chantier'] == filtrechantier7)
                            df_filter7=df_IA1.loc[mask]
                            st.dataframe(df_filter7)
                            st.text("*NInc: Incident\n*AAA: Accident avec arrêt\n*ASA: Accident sans arrêt\n*AT:Accident de trajet\n*NJP:Nombre de jours perdus")

                            if st.button("Télécharger", key=6):
                                st.markdown(get_table_download_link(df_filter7), unsafe_allow_html=True)
                            #figure
                            df_filter7['NInc'] = pd.to_numeric(df_filter7['NInc'])
                            df_filter7['AAA'] = pd.to_numeric(df_filter7['AAA'])
                            df_filter7['ASA'] = pd.to_numeric(df_filter7['ASA'])
                            df_filter7['AT'] = pd.to_numeric(df_filter7['AT'])
                            df_filter7['NJP'] = pd.to_numeric(df_filter7['NJP'])



                            Objectf_fixe6 = df_filter7['NInc'].sum()
                            Objectf_fixe7 = df_filter7['AAA'].sum()
                            Objectf_fixe8= df_filter7['ASA'].sum()
                            Objectf_fixe9= df_filter7['AT'].sum()
                            Objectf_fixe10 = df_filter7['NJP'].sum()


                            df_filter7_df1 = pd.DataFrame(columns=["NInc","AAA","ASA","AT","NJP"])


                            df_filter7_df1.at[0, "NInc"] = Objectf_fixe6
                            df_filter7_df1.at[0, "AAA"] = Objectf_fixe7
                            df_filter7_df1.at[0, "ASA"] = Objectf_fixe8
                            df_filter7_df1.at[0, "AT"] = Objectf_fixe9
                            df_filter7_df1.at[0, "NJP"] = Objectf_fixe10


                            df_filter7_df_melt1 = pd.melt(df_filter7_df1)


                            df_filter7_df_melt1.columns = ['variable', 'valeur']


                            st.dataframe(df_filter7_df_melt1)


                            figIA = px.bar(df_filter7_df_melt1, x = 'variable', y = 'valeur',color="variable")


                            st.plotly_chart(figIA, use_container_width=True)





                        AUDIT_exp= st.beta_expander("AUDIT CHANTIER; VISITE CONJOINTE;  PRÉVENTION ET INSPECTION")
                        with AUDIT_exp:
                            #Audit
                            df_Audit = pd.DataFrame(view_Audit(), columns=["id","IDD","Chantier","AC","VC","NEU","SMPAR","NPR","IE","Date"])
                            IDD2 = email.strip('][').split(', ')
			    
                            @st.cache
                            def Audit_2(df_Audit: pd.DataFrame) -> pd.DataFrame:
                                df_Audit = df_Audit[(df_Audit["IDD"].isin(IDD2))]
                                return df_Audit.loc[1:, ["id","Chantier","AC","VC","NEU","SMPAR","NPR","IE","Date"]]

                            # Pour empêcher l'affichage d'erreur en cas de donnée vide
                            try:
                                df_Audit1 = Audit_2(df_Audit)
                            except:
                                st.error("Nous ne pouvons afficher, car vous n'avez pas de donnée enregistrée.")
                                st.stop()

                            df_Audit1['Date'] = pd.to_datetime(df_Audit1['Date']).apply(lambda x: x.date())
                            df_Audit1.sort_values(by=['Date'], inplace=True)

                            #intervalle de date
                            st.write('SELECTIONNEZ UN INTERVALLE DE DATE POUR VOTRE GRILLE')
                            try:
                                miny= st.date_input('MinDate',min(df_Audit1['Date']),key=6)
                                maxy= st.date_input('MaxDate',max(df_Audit1['Date']),key=6)
                            except:
                                st.error("Nous ne pouvons afficher car vous n'avez pas aumoins deux dates enrégistrées")
                                st.stop()


                            #filtrage par chantier
                            splitted_df_Audit1 = df_Audit1['Chantier'].str.split(',')
                            unique_vals8 = list(dict.fromkeys([y for x in splitted_df_Audit1  for y in x]).keys())
                            filtrechantier8 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals8,key=7)
                            
                            mask = (df_Audit1['Date'] > miny) & (df_Audit1['Date'] <= maxy) & (df_Audit1['Chantier'] == filtrechantier8)
                            df_filter8=df_Audit1.loc[mask]
                            st.dataframe(df_filter8)
                            st.text("*AC: Audit Chantier\n*VC:Visite conjointe\n*NEU:Nombre d'exercice d'urgence\n*SMPAR:Sensibilisation au modes de prévention des activités à risques\n*NPR:Nombre de procedures réalisées\n*IE:Inspections Environne-mentales")

                            if st.button("Télécharger", key=7):
                                st.markdown(get_table_download_link(df_filter8), unsafe_allow_html=True)
                            #figure
                            df_filter8['AC'] = pd.to_numeric(df_filter8['AC'])
                            df_filter8['VC'] = pd.to_numeric(df_filter8['VC'])
                            df_filter8['NEU'] = pd.to_numeric(df_filter8['NEU'])
                            df_filter8['SMPAR'] = pd.to_numeric(df_filter8['SMPAR'])
                            df_filter8['NPR'] = pd.to_numeric(df_filter8['NPR'])
                            df_filter8['IE'] = pd.to_numeric(df_filter8['IE'])

                            Objectf_fixe12 = df_filter8['AC'].sum()
                            Objectf_fixe13 = df_filter8['VC'].sum()
                            Objectf_fixe14= df_filter8['NEU'].sum()
                            Objectf_fixe15= df_filter8['SMPAR'].sum()
                            Objectf_fixe16 = df_filter8['NPR'].sum()
                            Objectf_fixe17 = df_filter8['IE'].sum()

                            df_filter8_df1 = pd.DataFrame(columns=["AC", "VC","NEU","SMPAR","NPR","IE"])


                            df_filter8_df1.at[0, "AC"] = Objectf_fixe12
                            df_filter8_df1.at[0, "VC"] = Objectf_fixe13
                            df_filter8_df1.at[0, "NEU"] = Objectf_fixe14
                            df_filter8_df1.at[0, "SMPAR"] = Objectf_fixe15
                            df_filter8_df1.at[0, "NPR"] = Objectf_fixe16
                            df_filter8_df1.at[0, "IE"] = Objectf_fixe17

                            df_filter8_df_melt1 = pd.melt(df_filter8_df1)


                            df_filter8_df_melt1.columns = ['variable', 'valeur']

                            st.dataframe(df_filter8_df_melt1)
                            figAC1 = px.bar(df_filter8_df_melt1, x = 'variable', y = 'valeur',color="variable")
                            st.plotly_chart(figAC1, use_container_width=True)

                    #Modification
                    elif choix == "METTRE À JOUR":
                        st.subheader("MODIFIER DES DONNÉES")
                        with st.beta_expander("ACCUEIL SECURITÉ"):
                            st.markdown('### DONNÉE ACTUELLE')
                            df_Accueil = pd.DataFrame(view_Accueil(), columns=["id","IDD","Chantier","Nbre_Arrivant","Nbre_induction","Date"])

                            #pour voir uniquement les donnée de l'user connecté
                            IDD2 = email.strip('][').split(', ')

                            #ACCUEIL

                            @st.cache
                            def Accueil_2(df_Accueil: pd.DataFrame) -> pd.DataFrame:
                                df_Accueil2 = df_Accueil[(df_Accueil["IDD"].isin(IDD2))]
                                return df_Accueil2.loc[1:, ["id","Chantier","Nbre_Arrivant","Nbre_induction","Date"]]

                            df_Accueil1 = Accueil_2(df_Accueil)
                            
                            #filtrage par chantier
                            splitted_df_Accueil1 = df_Accueil1['Chantier'].str.split(',')
                            unique_vals1 = list(dict.fromkeys([y for x in splitted_df_Accueil1  for y in x]).keys())
                            filtrechantier = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals1,key=9)
                            mask =  (df_Accueil1['Chantier'] == filtrechantier)
                            df_filter1=df_Accueil1.loc[mask]
                            st.dataframe(df_filter1)


                            
                            idval = list(df_filter1['id'])
                            selected_id = st.selectbox("SELECTIONEZ l'ID DE LA LIGNE À MODIFIER", idval)
                            name_result = get_id_Accueil(selected_id)

                            if name_result:
                                id = name_result[0][0]
                                Chantier = name_result[0][2]
                                NArrivant = name_result[0][3]
                                Ninduction = name_result[0][4]
                                
                                col1, col2= st.beta_columns(2)
                                with col1:
                                    st.subheader("CIBLE À MODIFIER")
                                with col1:
                                    new_NArrivant =inputcheck(st.text_input("Nombre Arrivant",NArrivant))
                                    new_Ninduction = inputcheck(st.text_input("Nombre d'induction",Ninduction))
                                    id=selected_id
                                    
        
                                with col2:
                                    st.subheader("NOM DU CHANTIER")
                                    new_Chantier = st.text_input("Chantier",Chantier)
                                    
                                button1=st.button("MODIFIER LES DÉTAILS")
                                if button1:
                                    edit_Accueil(new_Chantier,new_NArrivant,new_Ninduction,id)
                                    st.success("MODIFIÉ AVEC SUCCÈS: {}".format(new_Chantier))
                                    
                                st.markdown('### DONNÉE MODIFIÉE')

                                df_Accueil = pd.DataFrame(view_Accueil(), columns=["id","IDD","Chantier","Nbre_Arrivant","Nbre_induction","Date"])
                                
                                #pour voir uniquement les donnée de l'user connecté
                                IDD2 = email.strip('][').split(', ')
        
                                #ACCUEIL
        
                                @st.cache
                                def Accueil_2(df_Accueil: pd.DataFrame) -> pd.DataFrame:
                                    df_Accueil2 = df_Accueil[(df_Accueil["IDD"].isin(IDD2))]
                                    return df_Accueil2.loc[1:, ["id","Chantier","Nbre_Arrivant","Nbre_induction","Date"]]
        
                                df_Accueil1 = Accueil_2(df_Accueil)
                                #filtrage par chantier
                                splitted_df_Accueil1 = df_Accueil1['Chantier'].str.split(',')
                                unique_vals1 = list(dict.fromkeys([y for x in splitted_df_Accueil1  for y in x]).keys())
                                filtrechantier = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals1,key=10)
                                mask =  (df_Accueil1['Chantier'] == filtrechantier)
                                df_filter1=df_Accueil1.loc[mask]
                                st.dataframe(df_filter1)
                                    
                        
                        
                        
                        with st.beta_expander("BRIEFING DE SÉCURITÉ( TBM)"):
                            st.markdown('### DONNÉE ACTUELLE')
                            df_TBM = pd.DataFrame(view_TBM(), columns=["id","IDD","Chantier","Nbre_chantier","Nbre_TBM","Date"])
                            IDD2 = email.strip('][').split(', ')

                            @st.cache
                            def TBM_2(df_TBM: pd.DataFrame) -> pd.DataFrame:
                                df_TBM2 = df_TBM[(df_TBM["IDD"].isin(IDD2))]
                                return df_TBM2.loc[1:, ["id","Chantier","Nbre_chantier","Nbre_TBM","Date"]]

                            df_TBM1 = TBM_2(df_TBM)
                            #filtrage par chantier
                            splitted_df_TBM1 = df_TBM1['Chantier'].str.split(',')
                            unique_vals2 = list(dict.fromkeys([y for x in splitted_df_TBM1  for y in x]).keys())
                            filtrechantier2 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals2,key=100)
                            
                            mask =  (df_TBM1['Chantier'] == filtrechantier2)
                            df_filter2=df_TBM1.loc[mask]
                            st.dataframe(df_filter2)
                            


                            
                            idval = list(df_filter2['id'])
                            selected_id = st.selectbox("SELECTIONEZ l'ID DE LA LIGNE À MODIFIER", idval,key=9)
                            name_result = get_id_TBM(selected_id)

                            if name_result:
                                id = name_result[0][0]
                                Chantier = name_result[0][2]
                                NChantier = name_result[0][3]
                                NTBM = name_result[0][4]
                                
                                col1, col2= st.beta_columns(2)
                                with col1:
                                    st.subheader("CIBLE À MODIFIER")
                                with col1:
                                    new_NChantier =inputcheck(st.text_input("Nombre Arrivant",NChantier,key=0))
                                    new_NTBM = inputcheck(st.text_input("Nombre d'induction",NTBM,key=1))
                                    id=selected_id
                                    
        
                                with col2:
                                    st.subheader("NOM DU CHANTIER")
                                    new_Chantier = st.text_input("Chantier",Chantier,key=2)
                                    
                                button1=st.button("MODIFIER LES DÉTAILS",key=0)
                                if button1:
                                     edit_TBM(new_Chantier,new_NChantier,new_NTBM,id)
                                     st.success("MODIFIÉ AVEC SUCCÈS: {}".format(new_Chantier))
                                     
                                st.markdown('### DONNÉE MODIFIÉE')

                                df_TBM = pd.DataFrame(view_TBM(), columns=["id","IDD","Chantier","Nbre_chantier","Nbre_TBM","Date"])
                                IDD2 = email.strip('][').split(', ')
                                @st.cache
                                def TBM_2(df_TBM: pd.DataFrame) -> pd.DataFrame:
                                    df_TBM2 = df_TBM[(df_TBM["IDD"].isin(IDD2))]
                                    return df_TBM2.loc[1:, ["id","Chantier","Nbre_chantier","Nbre_TBM","Date"]]

                                df_TBM1 = TBM_2(df_TBM)
                                #filtrage par chantier
                                splitted_df_TBM1 = df_TBM1['Chantier'].str.split(',')
                                unique_vals2 = list(dict.fromkeys([y for x in splitted_df_TBM1  for y in x]).keys())
                                filtrechantier2 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals2,key=101)
                                mask =  (df_TBM1['Chantier'] == filtrechantier2)
                                df_filter2=df_TBM1.loc[mask]
                                st.dataframe(df_filter2)
                                
                        
                        with st.beta_expander("NON CONFORMITÉ"):
                            st.markdown('### DONNÉE ACTUELLE')
                            df_NC = pd.DataFrame(view_NC(), columns=["id","IDD","Chantier","NCR","FNCR","NCC","FNCC","Date"])
                            IDD2 = email.strip('][').split(', ')


                            @st.cache
                            def NC_2(df_NC: pd.DataFrame) -> pd.DataFrame:
                                df_NC2 = df_NC[(df_NC["IDD"].isin(IDD2))]
                                return df_NC2.loc[1:, ["id","Chantier","NCR","FNCR","NCC","FNCC","Date"]]

                            df_NC1 = NC_2(df_NC)

                            #filtrage par chantier
                            splitted_df_NC1 = df_NC1['Chantier'].str.split(',')
                            unique_vals3 = list(dict.fromkeys([y for x in splitted_df_NC1  for y in x]).keys())
                            filtrechantier3 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals3,key=21)
                            mask =  (df_NC1['Chantier'] == filtrechantier3)
                            df_filter3=df_NC1.loc[mask]
                            st.dataframe(df_filter3)
                            


                            
                            idval = list(df_filter3['id'])
                            selected_id = st.selectbox("SELECTIONEZ l'ID DE LA LIGNE À MODIFIER", idval,key=0)
                            name_result = get_id_NC(selected_id)

                            if name_result:
                                id = name_result[0][0]
                                Chantier = name_result[0][2]
                                NCR = name_result[0][3]
                                FNCR = name_result[0][4]
                                NCC = name_result[0][5]
                                FNCC = name_result[0][6]
                                
                                col1, col2= st.beta_columns(2)
                                with col1:
                                    st.subheader("CIBLE À MODIFIER")
                                with col1:
                                    new_NCR = inputcheck(st.text_input("Nombre de Non conformité remontée",NCR,key=0))
                                    new_FNCR = inputcheck(st.text_input("Nombre de fiche de Non conformité remontée",FNCR,key=1))
                                    new_NCC = inputcheck(st.text_input("Nombre de Non conformité cloturée",NCC,key=2))
                                    new_FNCC= inputcheck(st.text_input("Nombre de fiche de Non conformité cloturée",FNCC, key=3))
                                    
                                with col2:
                                    st.subheader("NOM DU CHANTIER")
                                    new_Chantier = st.text_input("Chantier",Chantier,key=4)
                                    
                                button1=st.button("MODIFIER LES DÉTAILS",key=1)
                                if button1:
                                    edit_NC(new_Chantier,new_NCR,new_FNCR,new_NCC,new_FNCC,id)
                                    st.success("MODIFIÉ AVEC SUCCÈS: {}".format(new_Chantier))
                                    
                                st.markdown('### DONNÉE MODIFIÉE')
                                df_NC = pd.DataFrame(view_NC(), columns=["id","IDD","Chantier","NCR","FNCR","NCC","FNCC","Date"])
                                IDD2 = email.strip('][').split(', ')


                                @st.cache
                                def NC_2(df_NC: pd.DataFrame) -> pd.DataFrame:
                                    df_NC2 = df_NC[(df_NC["IDD"].isin(IDD2))]
                                    return df_NC2.loc[1:, ["id","Chantier","NCR","FNCR","NCC","FNCC","Date"]]

                                df_NC1 = NC_2(df_NC)
                                #filtrage par chantier
                                splitted_df_NC1 = df_NC1['Chantier'].str.split(',')
                                unique_vals3 = list(dict.fromkeys([y for x in splitted_df_NC1  for y in x]).keys())
                                filtrechantier3 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals3,key=22)
                                mask =  (df_NC1['Chantier'] == filtrechantier3)
                                df_filter3=df_NC1.loc[mask]
                                st.dataframe(df_filter3)


                        with st.beta_expander("CHANGEMENTS ENREGISTRÉS"):
                            st.markdown('### DONNÉE ACTUELLE')
                            df_Changements = pd.DataFrame(view_Changements(), columns=["id","IDD","Chantier","NCH","FNCH","NCHC","FNCHC","Date"])
                            IDD2 = email.strip('][').split(', ')

                            @st.cache
                            def Changements_2(df_Changements: pd.DataFrame) -> pd.DataFrame:
                                df_Changements2 = df_Changements[(df_Changements["IDD"].isin(IDD2))]
                                return df_Changements2.loc[1:, ["id","Chantier","NCH","FNCH","NCHC","FNCHC","Date"]]

                            df_Changements1 = Changements_2(df_Changements)
                            #filtrage par chantier
                            splitted_df_Changements1 = df_Changements1['Chantier'].str.split(',')
                            unique_vals4 = list(dict.fromkeys([y for x in splitted_df_Changements1  for y in x]).keys())
                            filtrechantier4 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals4,key=12)
                            mask = (df_Changements1['Chantier'] == filtrechantier4)
                            df_filter4=df_Changements1.loc[mask]
                            st.dataframe(df_filter4)
                            

                            idval = list(df_filter4['id'])
                            selected_id = st.selectbox("SELECTIONEZ l'ID DE LA LIGNE À MODIFIER", idval,key=1)
                            name_result = get_id_Changements(selected_id)

                            if name_result:
                                id = name_result[0][0]
                                Chantier = name_result[0][2]
                                NCH = name_result[0][3]
                                FNCH = name_result[0][4]
                                NCHC = name_result[0][5]
                                FNCHC = name_result[0][6]
                                
                                col1, col2= st.beta_columns(2)
                                with col1:
                                    st.subheader("CIBLE À MODIFIER")
                                with col1:
                                    new_NCH = inputcheck(st.text_input("Nombre de Changement enregistrés",NCH))
                                    new_FNCH = inputcheck(st.text_input("Nombre de fiche de Changements enregistrés",FNCH))
                                    new_NCHC  = inputcheck(st.text_input("Nombre de Changements cloturés",NCHC))
                                    new_FNCHC= inputcheck(st.text_input("Nombre de fiche de  Changements suivis et cloturés",FNCHC))
                                    
                                with col2:
                                    st.subheader("NOM DU CHANTIER")
                                    Chantier = st.text_input("Chantier",Chantier,key=3)
                                    
                                button1=st.button("MODIFIER LES DÉTAILS",key=3)
                                if button1:
                                    edit_Changements(new_Chantier,new_NCH,new_FNCH,new_NCHC,new_FNCHC,id)
                                    st.success("MODIFIÉ AVEC SUCCÈS: {}".format(new_Chantier))
                                    
                                st.markdown('### DONNÉE MODIFIÉE')
                                df_Changements = pd.DataFrame(view_Changements(), columns=["id","IDD","Chantier","NCH","FNCH","NCHC","FNCHC","Date"])
                                IDD2 = email.strip('][').split(', ')

                                @st.cache
                                def Changements_2(df_Changements: pd.DataFrame) -> pd.DataFrame:
                                    df_Changements2 = df_Changements[(df_Changements["IDD"].isin(IDD2))]
                                    return df_Changements2.loc[1:, ["id","Chantier","NCH","FNCH","NCHC","FNCHC","Date"]]

                                df_Changements1 = Changements_2(df_Changements)
                                #filtrage par chantier
                                splitted_df_Changements1 = df_Changements1['Chantier'].str.split(',')
                                unique_vals4 = list(dict.fromkeys([y for x in splitted_df_Changements1  for y in x]).keys())
                                filtrechantier4 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals4,key=13)
                                mask = (df_Changements1['Chantier'] == filtrechantier4)
                                df_filter4=df_Changements1.loc[mask]
                                st.dataframe(df_filter4)


                        with st.beta_expander("ANOMALIES"):
                            st.markdown('### DONNÉE ACTUELLE')
                            df_Anomalies = pd.DataFrame(view_Anomalies(), columns=["id","IDD","Chantier","NA","FNA","NAC","FNAC","Date"])
                            IDD2 = email.strip('][').split(', ')

                            @st.cache
                            def Anomalies_2(df_Anomalies: pd.DataFrame) -> pd.DataFrame:
                                df_Anomalies2 = df_Anomalies[(df_Anomalies["IDD"].isin(IDD2))]
                                return df_Anomalies2.loc[1:, ["id","Chantier","NA","FNA","NAC","FNAC","Date"]]

                            df_Anomalies1 = Anomalies_2(df_Anomalies)
                            #filtrage par chantier
                            splitted_df_Anomalies1 = df_Anomalies1['Chantier'].str.split(',')
                            unique_vals5 = list(dict.fromkeys([y for x in splitted_df_Anomalies1  for y in x]).keys())
                            filtrechantier5 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals5,key=14)
                            mask = (df_Anomalies1['Chantier'] == filtrechantier5)
                            df_filter5=df_Anomalies1.loc[mask]
                            st.dataframe(df_filter5)
                            

                            idval = list(df_filter5['id'])
                            selected_id = st.selectbox("SELECTIONEZ l'ID DE LA LIGNE A MODIFIER", idval,key=4)
                            name_result = get_id_Anomalies(selected_id)

                            if name_result:
                                id = name_result[0][0]
                                Chantier = name_result[0][2]
                                NA = name_result[0][3]
                                FNA = name_result[0][4]
                                NAC = name_result[0][5]
                                FNAC = name_result[0][6]
                                
                                col1, col2= st.beta_columns(2)
                                with col1:
                                    st.subheader("CIBLE À MODIFIER")
                                with col1:
                                    new_NA = inputcheck(st.text_input("Nombre d'Anomalies Remontées",NA))
                                    new_FNA = inputcheck(st.text_input("Nombre de fiche d'Anomalies Remontées",FNA))
                                    new_NAC = inputcheck(st.text_input("Nombre d' Anomalies cloturés",NAC))
                                    new_FNAC = inputcheck(st.text_input("Nombre de fiche de  Anomalies Corrigées",FNAC))
                                    
                                with col2:
                                    st.subheader("NOM DU CHANTIER")
                                    new_Chantier = st.text_input("Chantier",Chantier,key=5)
                                    
                                button1=st.button("MODIFIER LES DÉTAILS",key=5)
                                if button1:
                                    edit_Anomalies(new_Chantier,new_NA,new_FNA,new_NAC,new_FNAC,id)
                                    st.success("MODIFIÉ AVEC SUCCÈS: {}".format(new_Chantier))
                                    
                                st.markdown('### DONNÉE MODIFIÉE')
                                df_Anomalies = pd.DataFrame(view_Anomalies(), columns=["id","IDD","Chantier","NA","FNA","NAC","FNAC","Date"])
                                IDD2 = email.strip('][').split(', ')

                                @st.cache
                                def Anomalies_2(df_Anomalies: pd.DataFrame) -> pd.DataFrame:
                                    df_Anomalies2 = df_Anomalies[(df_Anomalies["IDD"].isin(IDD2))]
                                    return df_Anomalies2.loc[1:, ["id","Chantier","NA","FNA","NAC","FNAC","Date"]]

                                df_Anomalies1 = Anomalies_2(df_Anomalies)
                                #filtrage par chantier
                                splitted_df_Anomalies1 = df_Anomalies1['Chantier'].str.split(',')
                                unique_vals5 = list(dict.fromkeys([y for x in splitted_df_Anomalies1  for y in x]).keys())
                                filtrechantier5 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals5,key=144)
                                
                                df_filter5=df_Anomalies1.loc[mask]
                                st.dataframe(df_filter5)

                        
                        with st.beta_expander("ANALYSE DES RISQUES RÉALISÉS(JSA)"):
                            st.markdown('### DONNÉE ACTUELLE')
                            df_JSA = pd.DataFrame(view_JSA(), columns=["id","IDD","Chantier","NAct","NJSA","Date"])
                            IDD2 = email.strip('][').split(', ')

                            @st.cache
                            def JSA_2(df_JSA: pd.DataFrame) -> pd.DataFrame:
                                df_JSA2 = df_JSA[(df_JSA["IDD"].isin(IDD2))]
                                return df_JSA2.loc[1:, ["id","Chantier","NAct","NJSA","Date"]]

                            df_JSA1 = JSA_2(df_JSA)
                            #filtrage par chantier
                            splitted_df_JSA1 = df_JSA1['Chantier'].str.split(',')
                            unique_vals6 = list(dict.fromkeys([y for x in splitted_df_JSA1  for y in x]).keys())
                            filtrechantier6 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals6,key=166)
                            mask = (df_JSA1['Chantier'] == filtrechantier6)
                            df_filter6=df_JSA1.loc[mask]
                            st.dataframe(df_filter6)

                            idval = list(df_filter6['id'])
                            selected_id = st.selectbox("SELECTIONEZ l'ID DE LA LIGNE À MODIFIER", idval,key=6)
                            name_result = get_id_JSA(selected_id)

                            if name_result:
                                id = name_result[0][0]
                                Chantier = name_result[0][2]
                                NAct = name_result[0][3]
                                NJSA = name_result[0][4]
                               
                                
                                col1, col2= st.beta_columns(2)
                                with col1:
                                    st.subheader("CIBLE À MODIFIER")
                                with col1:
                                    new_NAct = inputcheck(st.text_input("Nombre d'Activite",NAct))
                                    new_NJSA = inputcheck(st.text_input("Nombre de fiche JSA",NJSA))
                                    
                                with col2:
                                    st.subheader("NOM DU CHANTIER")
                                    new_Chantier = st.text_input("Chantier",Chantier,key=6)
                                    
                                button1=st.button("MODIFIER LES DÉTAILS",key=6)
                                if button1:
                                    edit_JSA(new_Chantier,new_NAct,new_NJSA,id)
                                    st.success("MODIFIÉ AVEC SUCCÈS: {}".format(new_Chantier))
                                
                                st.markdown('### DONNÉE MODIFIÉE')
                                df_JSA = pd.DataFrame(view_JSA(), columns=["id","IDD","Chantier","NAct","NJSA","Date"])
                                IDD2 = email.strip('][').split(', ')

                                @st.cache
                                def JSA_2(df_JSA: pd.DataFrame) -> pd.DataFrame:
                                    df_JSA2 = df_JSA[(df_JSA["IDD"].isin(IDD2))]
                                    return df_JSA2.loc[1:, ["id","Chantier","NAct","NJSA","Date"]]

                                df_JSA1 = JSA_2(df_JSA)
                                #filtrage par chantier
                                splitted_df_JSA1 = df_JSA1['Chantier'].str.split(',')
                                unique_vals6 = list(dict.fromkeys([y for x in splitted_df_JSA1  for y in x]).keys())
                                filtrechantier6 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals6,key=177)
                                mask = (df_JSA1['Chantier'] == filtrechantier6)
                                df_filter6=df_JSA1.loc[mask]
                                st.dataframe(df_filter6)



                        with st.beta_expander("INCIDENT & ACCIDENT"):
                            st.markdown('### DONNÉE ACTUELLE')
                            df_IA = pd.DataFrame(view_Incident_Accident(), columns=["id","IDD","Chantier","NInc","AAA","ASA","AT","NJP","Date"])
                            IDD2 = email.strip('][').split(', ')

                            @st.cache
                            def IA_2(df_IA: pd.DataFrame) -> pd.DataFrame:
                                df_IA = df_IA[(df_IA["IDD"].isin(IDD2))]
                                return df_IA.loc[1:, ["id","Chantier","NInc","AAA","ASA","AT","NJP","Date"]]

                            df_IA1 = IA_2(df_IA)

                            #filtrage par chantier
                            splitted_df_IA1 = df_IA1['Chantier'].str.split(',')
                            unique_vals7 = list(dict.fromkeys([y for x in splitted_df_IA1  for y in x]).keys())
                            filtrechantier7 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals7,key=18)
                            mask = (df_IA1['Chantier'] == filtrechantier7)
                            df_filter7=df_IA1.loc[mask]
                            st.dataframe(df_filter7)

                            idval = list(df_filter7['id'])
                            selected_id = st.selectbox("SELECTIONEZ l'ID DE LA LIGNE À MODIFIER", idval,key=7)
                            name_result = get_id_Incident_Accident(selected_id)

                            if name_result:
                                id = name_result[0][0]
                                Chantier = name_result[0][2]
                                NInc = name_result[0][3]
                                AAA = name_result[0][4]
                                ASA = name_result[0][5]
                                AT = name_result[0][6]
                                NJP = name_result[0][7]
                               
                                
                                col1, col2= st.beta_columns(2)
                                with col1:
                                    st.subheader("CIBLE À MODIFIER")
                                with col1:
                                    new_AAA = inputcheck(st.text_input("Accident Avec Arrêt",AAA))
                                    new_NJP = inputcheck(st.text_input("Nombre de jours perdus",NJP))
                                    new_ASA = inputcheck(st.text_input("Accident Sans Arrêt",ASA))
                                    new_AT = inputcheck(st.text_input("Nombre d'accident de trajet",AT))
                                    new_NInc = inputcheck(st.text_input("Incident",NInc))
                                    
                                with col2:
                                    st.subheader("NOM DU CHANTIER")
                                    new_Chantier = st.text_input("Chantier",Chantier,key=7)
                                    
                                button1=st.button("MODIFIER LES DÉTAILS",key=7)
                                if button1:
                                    edit_Incident_Accident(new_Chantier,new_NInc,new_AAA,new_ASA,new_AT,new_NJP,id)
                                    st.success("MODIFIÉ AVEC SUCCÈS: {}".format(new_Chantier))

                                df_IA = pd.DataFrame(view_Incident_Accident(), columns=["id","IDD","Chantier","NInc","AAA","ASA","AT","NJP","Date"])
                                IDD2 = email.strip('][').split(', ')

                                @st.cache
                                def IA_2(df_IA: pd.DataFrame) -> pd.DataFrame:
                                    df_IA = df_IA[(df_IA["IDD"].isin(IDD2))]
                                    return df_IA.loc[1:, ["id","Chantier","NInc","AAA","ASA","AT","NJP","Date"]]

                                df_IA1 = IA_2(df_IA)
                                splitted_df_IA1 = df_IA1['Chantier'].str.split(',')
                                unique_vals7 = list(dict.fromkeys([y for x in splitted_df_IA1  for y in x]).keys())
                                filtrechantier7 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals7,key=19)
                                mask = (df_IA1['Chantier'] == filtrechantier7)
                                df_filter7=df_IA1.loc[mask]
                                st.dataframe(df_filter7)




                        with st.beta_expander("AUDIT CHANTIER; VISITE CONJOINTE;  PRÉVENTION ET INSPECTION"):
                            st.markdown('### DONNÉE ACTUELLE')
                            df_Audit = pd.DataFrame(view_Audit(), columns=["id","IDD","Chantier","AC","VC","NEU","SMPAR","NPR","IE","Date"])
                            IDD2 = email.strip('][').split(', ')

                            @st.cache
                            def Audit_2(df_Audit: pd.DataFrame) -> pd.DataFrame:
                                df_Audit = df_Audit[(df_Audit["IDD"].isin(IDD2))]
                                return df_Audit.loc[1:, ["id","Chantier","AC","VC","NEU","SMPAR","NPR","IE","Date"]]

                            df_Audit1 = Audit_2(df_Audit)
                            #filtrage par chantier
                            splitted_df_Audit1 = df_Audit1['Chantier'].str.split(',')
                            unique_vals8 = list(dict.fromkeys([y for x in splitted_df_Audit1  for y in x]).keys())
                            filtrechantier8 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals8,key=20)
                            mask = (df_Audit1['Chantier'] == filtrechantier8)
                            df_filter8=df_Audit1.loc[mask]
                            st.dataframe(df_filter8)

                            idval = list(df_filter8['id'])
                            selected_id = st.selectbox("SELECTIONEZ l'ID DE LA LIGNE À MODIFIER", idval,key=8)
                            name_result = get_id_Audit(selected_id)

                            if name_result:
                                id = name_result[0][0]
                                Chantier = name_result[0][2]
                                AC = name_result[0][3]
                                VC = name_result[0][4]
                                NEU = name_result[0][5]
                                SMPAR = name_result[0][6]
                                NPR = name_result[0][7]
                                IE = name_result[0][8]
                               
                                
                                col1, col2= st.beta_columns(2)
                                with col1:
                                    st.subheader("CIBLE À MODIFIER")
                                with col1:
                                    new_AC= inputcheck(st.text_input("Nombre d'audit",AC))
                                    new_VC= inputcheck(st.text_input("Nombre de Visite Conjointe",VC))
                                    new_NEU= inputcheck(st.text_input("Nombre d'exercice d'urgence",NEU))
                                    new_SMPAR= inputcheck(st.text_input("Sensibilisation au modes de prévention des activités à risques",SMPAR))
                                    new_NPR= inputcheck(st.text_input("Procedures réalisées",NPR))
                                    new_IE= inputcheck(st.text_input("Inspections Environnementales",IE))
                                    
                                with col2:
                                    st.subheader("NOM DU CHANTIER")
                                    new_Chantier = st.text_input("Chantier")
                                    
                                button1=st.button("MODIFIER LES DÉTAILS",key=8)
                                if button1:
                                    edit_Audit(new_ID,new_Chantier,new_AC,new_VC,new_NEU,new_SMPAR,new_NPR,new_IE,id)
                                    st.success("MODIFIÉ AVEC SUCCÈS: {}".format(new_Chantier))
                                    
                                st.markdown('### DONNÉE MODIFIÉE')
                                df_Audit = pd.DataFrame(view_Audit(), columns=["id","IDD","Chantier","AC","VC","NEU","SMPAR","NPR","IE","Date"])
                                IDD2 = email.strip('][').split(', ')

                                @st.cache
                                def Audit_2(df_Audit: pd.DataFrame) -> pd.DataFrame:
                                    df_Audit = df_Audit[(df_Audit["IDD"].isin(IDD2))]
                                    return df_Audit.loc[1:, ["id","Chantier","AC","VC","NEU","SMPAR","NPR","IE","Date"]]

                                df_Audit1 = Audit_2(df_Audit)
                                #filtrage par chantier
                                splitted_df_Audit1 = df_Audit1['Chantier'].str.split(',')
                                unique_vals8 = list(dict.fromkeys([y for x in splitted_df_Audit1  for y in x]).keys())
                                filtrechantier8 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals8,key=211)
                                mask = (df_Audit1['Chantier'] == filtrechantier8)
                                df_filter8=df_Audit1.loc[mask]
                                st.dataframe(df_filter8)

                    #Suppression des données
                    elif choix ==  "SUPPRIMER":
                        st.subheader("SUPPRIMER DES DONNÉES")
                        with st.beta_expander("ACCUEIL SECURITÉ"):
                            st.markdown('### DONNÉE ACTUELLE')
                            df_Accueil = pd.DataFrame(view_Accueil(), columns=["id","IDD","Chantier","Nbre_Arrivant","Nbre_induction","Date"])

                            #pour voir uniquement les donnée de l'user connecté
                            IDD2 = email.strip('][').split(', ')

                            #ACCUEIL

                            @st.cache
                            def Accueil_2(df_Accueil: pd.DataFrame) -> pd.DataFrame:
                                df_Accueil2 = df_Accueil[(df_Accueil["IDD"].isin(IDD2))]
                                return df_Accueil2.loc[1:, ["id","Chantier","Nbre_Arrivant","Nbre_induction","Date"]]

                            df_Accueil1 = Accueil_2(df_Accueil)
                            
                            #filtrage par chantier
                            splitted_df_Accueil1 = df_Accueil1['Chantier'].str.split(',')
                            unique_vals1 = list(dict.fromkeys([y for x in splitted_df_Accueil1  for y in x]).keys())
                            filtrechantier = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals1,key=22)
                            mask =  (df_Accueil1['Chantier'] == filtrechantier)
                            df_filter1=df_Accueil1.loc[mask]
                            st.dataframe(df_filter1)

                            idval = list(df_filter1['id'])
                            selected_id = st.selectbox("SELECTIONEZ l'ID DE LA LIGNE À SUPPRIMER", idval, key=10)
                            name_delete = get_id_Accueil(selected_id)
                            if name_delete:
                                id = name_delete[0][0]
                                if st.button("SUPPRIMER"):
                                    delete_data_Accueil(id)
                                    st.warning("SUPPRIMER: '{}'".format(name_delete))
                                    
                                st.markdown('### DONNÉE MODIFIÉE')
                                df_Accueil = pd.DataFrame(view_Accueil(), columns=["id","IDD","Chantier","Nbre_Arrivant","Nbre_induction","Date"])

                                #pour voir uniquement les donnée de l'user connecté
                                IDD2 = email.strip('][').split(', ')

                                #ACCUEIL

                                @st.cache
                                def Accueil_2(df_Accueil: pd.DataFrame) -> pd.DataFrame:
                                    df_Accueil2 = df_Accueil[(df_Accueil["IDD"].isin(IDD2))]
                                    return df_Accueil2.loc[1:, ["id","Chantier","Nbre_Arrivant","Nbre_induction","Date"]]

                                df_Accueil1 = Accueil_2(df_Accueil)
                                
                                #filtrage par chantier
                                splitted_df_Accueil1 = df_Accueil1['Chantier'].str.split(',')
                                unique_vals1 = list(dict.fromkeys([y for x in splitted_df_Accueil1  for y in x]).keys())
                                filtrechantier = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals1,key=23)
                                mask =  (df_Accueil1['Chantier'] == filtrechantier)
                                df_filter1=df_Accueil1.loc[mask]
                                st.dataframe(df_filter1)



                        with st.beta_expander("BRIEFING DE SÉCURITÉ( TBM)"):
                            st.markdown('### DONNÉE ACTUELLE')
                            df_TBM = pd.DataFrame(view_TBM(), columns=["id","IDD","Chantier","Nbre_chantier","Nbre_TBM","Date"])
                            IDD2 = email.strip('][').split(', ')

                            @st.cache
                            def TBM_2(df_TBM: pd.DataFrame) -> pd.DataFrame:
                                df_TBM2 = df_TBM[(df_TBM["IDD"].isin(IDD2))]
                                return df_TBM2.loc[1:, ["id","Chantier","Nbre_chantier","Nbre_TBM","Date"]]

                            df_TBM1 = TBM_2(df_TBM)
                            #filtrage par chantier
                            splitted_df_TBM1 = df_TBM1['Chantier'].str.split(',')
                            unique_vals2 = list(dict.fromkeys([y for x in splitted_df_TBM1  for y in x]).keys())
                            filtrechantier2 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals2,key=24)
                            mask =  (df_TBM1['Chantier'] == filtrechantier2)
                            df_filter2=df_TBM1.loc[mask]
                            st.dataframe(df_filter2)

                            
                            idval = list(df_filter2['id'])
                            selected_id = st.selectbox("SELECTIONEZ l'ID DE LA LIGNE À SUPPRIMER", idval,key=41)
                            name_delete = get_id_TBM(selected_id)
                            if name_delete:
                                id = name_delete[0][0]
                                if st.button("SUPPRIMER",key=0):
                                    delete_data_TBM(name_delete)
                                    st.warning("SUPPRIMER: '{}'".format(name_delete))
                                
                                st.markdown('### DONNÉE MODIFIÉE')
                                df_TBM = pd.DataFrame(view_TBM(), columns=["id","IDD","Chantier","Nbre_chantier","Nbre_TBM","Date"])
                                IDD2 = email.strip('][').split(', ')
                                @st.cache
                                def TBM_2(df_TBM: pd.DataFrame) -> pd.DataFrame:
                                    df_TBM2 = df_TBM[(df_TBM["IDD"].isin(IDD2))]
                                    return df_TBM2.loc[1:, ["id","Chantier","Nbre_chantier","Nbre_TBM","Date"]]

                                df_TBM1 = TBM_2(df_TBM)
                                #filtrage par chantier
                                splitted_df_TBM1 = df_TBM1['Chantier'].str.split(',')
                                unique_vals2 = list(dict.fromkeys([y for x in splitted_df_TBM1  for y in x]).keys())
                                filtrechantier2 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals2,key=35)
                                mask =  (df_TBM1['Chantier'] == filtrechantier2)
                                df_filter2=df_TBM1.loc[mask]
                                st.dataframe(df_filter2)


                        with st.beta_expander("NON CONFORMITÉ"):
                            st.markdown('### DONNÉE ACTUELLE')
                            df_NC = pd.DataFrame(view_NC(), columns=["id","IDD","Chantier","NCR","FNCR","NCC","FNCC","Date"])
                            IDD2 = email.strip('][').split(', ')


                            @st.cache
                            def NC_2(df_NC: pd.DataFrame) -> pd.DataFrame:
                                df_NC2 = df_NC[(df_NC["IDD"].isin(IDD2))]
                                return df_NC2.loc[1:, ["id","Chantier","NCR","FNCR","NCC","FNCC","Date"]]

                            df_NC1 = NC_2(df_NC)

                            #filtrage par chantier
                            splitted_df_NC1 = df_NC1['Chantier'].str.split(',')
                            unique_vals3 = list(dict.fromkeys([y for x in splitted_df_NC1  for y in x]).keys())
                            filtrechantier3 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals3,key=25)
                            mask =  (df_NC1['Chantier'] == filtrechantier3)
                            df_filter3=df_NC1.loc[mask]
                            st.dataframe(df_filter3)
                            
                            
                            idval = list(df_filter3['id'])
                            selected_id = st.selectbox("SELECTIONEZ l'ID DE LA LIGNE À SUPPRIMER", idval,key=12)
                            name_delete = get_id_NC(selected_id)
                            if name_delete:
                                id = name_delete[0][0]
                                if st.button("SUPPRIMER",key=1):
                                    delete_data_NC(name_delete)
                                    st.warning("SUPPRIMER: '{}'".format(name_delete))
                                    
                                st.markdown('### DONNÉE MODIFIÉE')
                                df_NC = pd.DataFrame(view_NC(), columns=["id","IDD","Chantier","NCR","FNCR","NCC","FNCC","Date"])
                                IDD2 = email.strip('][').split(', ')


                                @st.cache
                                def NC_2(df_NC: pd.DataFrame) -> pd.DataFrame:
                                    df_NC2 = df_NC[(df_NC["IDD"].isin(IDD2))]
                                    return df_NC2.loc[1:, ["id","Chantier","NCR","FNCR","NCC","FNCC","Date"]]

                                df_NC1 = NC_2(df_NC)

                                #filtrage par chantier
                                splitted_df_NC1 = df_NC1['Chantier'].str.split(',')
                                unique_vals3 = list(dict.fromkeys([y for x in splitted_df_NC1  for y in x]).keys())
                                filtrechantier3 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals3,key=26)
                                mask =  (df_NC1['Chantier'] == filtrechantier3)
                                df_filter3=df_NC1.loc[mask]
                                st.dataframe(df_filter3)

                        with st.beta_expander("CHANGEMENTS ENREGISTRÉS"):
                            st.markdown('### DONNÉE ACTUELLE')
                            df_Changements = pd.DataFrame(view_Changements(), columns=["id","IDD","Chantier","NCH","FNCH","NCHC","FNCHC","Date"])
                            IDD2 = email.strip('][').split(', ')

                            @st.cache
                            def Changements_2(df_Changements: pd.DataFrame) -> pd.DataFrame:
                                df_Changements2 = df_Changements[(df_Changements["IDD"].isin(IDD2))]
                                return df_Changements2.loc[1:, ["id","Chantier","NCH","FNCH","NCHC","FNCHC","Date"]]

                            df_Changements1 = Changements_2(df_Changements)
                            #filtrage par chantier
                            splitted_df_Changements1 = df_Changements1['Chantier'].str.split(',')
                            unique_vals4 = list(dict.fromkeys([y for x in splitted_df_Changements1  for y in x]).keys())
                            filtrechantier4 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals4,key=27)
                            mask = (df_Changements1['Chantier'] == filtrechantier4)
                            df_filter4=df_Changements1.loc[mask]
                            st.dataframe(df_filter4)
                            

                            idval = list(df_filter4['id'])
                            selected_id = st.selectbox("SELECTIONEZ l'ID DE LA LIGNE À SUPPRIMER", idval,key=13)
                            name_delete = get_id_Changements(selected_id)
                            if name_delete:
                                id = name_delete[0][0]
                                if st.button("SUPPRIMER",key=2):
                                    delete_data_Changements(name_delete)
                                    st.warning("SUPPRIMER: '{}'".format(name_delete))
                                    
                                st.markdown('### DONNÉE MODIFIÉE')
                                df_Changements = pd.DataFrame(view_Changements(), columns=["id","IDD","Chantier","NCH","FNCH","NCHC","FNCHC","Date"])
                                IDD2 = email.strip('][').split(', ')

                                @st.cache
                                def Changements_2(df_Changements: pd.DataFrame) -> pd.DataFrame:
                                    df_Changements2 = df_Changements[(df_Changements["IDD"].isin(IDD2))]
                                    return df_Changements2.loc[1:, ["id","Chantier","NCH","FNCH","NCHC","FNCHC","Date"]]

                                df_Changements1 = Changements_2(df_Changements)
                                #filtrage par chantier
                                splitted_df_Changements1 = df_Changements1['Chantier'].str.split(',')
                                unique_vals4 = list(dict.fromkeys([y for x in splitted_df_Changements1  for y in x]).keys())
                                filtrechantier4 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals4,key=28)
                                mask = (df_Changements1['Chantier'] == filtrechantier4)
                                df_filter4=df_Changements1.loc[mask]
                                st.dataframe(df_filter4)


                        with st.beta_expander("ANOMALIES"):
                            st.markdown('### DONNÉE ACTUELLE')
                            df_Anomalies = pd.DataFrame(view_Anomalies(), columns=["id","IDD","Chantier","NA","FNA","NAC","FNAC","Date"])
                            IDD2 = email.strip('][').split(', ')

                            @st.cache
                            def Anomalies_2(df_Anomalies: pd.DataFrame) -> pd.DataFrame:
                                df_Anomalies2 = df_Anomalies[(df_Anomalies["IDD"].isin(IDD2))]
                                return df_Anomalies2.loc[1:, ["id","Chantier","NA","FNA","NAC","FNAC","Date"]]

                            df_Anomalies1 = Anomalies_2(df_Anomalies)
                            #filtrage par chantier
                            splitted_df_Anomalies1 = df_Anomalies1['Chantier'].str.split(',')
                            unique_vals5 = list(dict.fromkeys([y for x in splitted_df_Anomalies1  for y in x]).keys())
                            filtrechantier5 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals5,key=29)
                            mask = (df_Anomalies1['Chantier'] == filtrechantier5)
                            df_filter5=df_Anomalies1.loc[mask]
                            st.dataframe(df_filter5)
                            

                            idval = list(df_filter5['id'])
                            selected_id = st.selectbox("SELECTIONEZ l'ID DE LA LIGNE À SUPPRIMER", idval,key=14)
                            name_delete = get_id_Anomalies(selected_id)
                            if name_delete:
                                id = name_delete[0][0]
                                if st.button("SUPPRIMER",key=3):
                                    delete_data_Anomalies(name_delete)
                                    st.warning("SUPPRIMER: '{}'".format(name_delete))
                                    
                                st.markdown('### DONNÉE MODIFIÉE')
                                df_Anomalies = pd.DataFrame(view_Anomalies(), columns=["id","IDD","Chantier","NA","FNA","NAC","FNAC","Date"])
                                IDD2 = email.strip('][').split(', ')

                                @st.cache
                                def Anomalies_2(df_Anomalies: pd.DataFrame) -> pd.DataFrame:
                                    df_Anomalies2 = df_Anomalies[(df_Anomalies["IDD"].isin(IDD2))]
                                    return df_Anomalies2.loc[1:, ["id","Chantier","NA","FNA","NAC","FNAC","Date"]]

                                df_Anomalies1 = Anomalies_2(df_Anomalies)
                                #filtrage par chantier
                                splitted_df_Anomalies1 = df_Anomalies1['Chantier'].str.split(',')
                                unique_vals5 = list(dict.fromkeys([y for x in splitted_df_Anomalies1  for y in x]).keys())
                                filtrechantier5 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals5,key=30)
                                mask = (df_Anomalies1['Chantier'] == filtrechantier5)
                                df_filter5=df_Anomalies1.loc[mask]
                                st.dataframe(df_filter5)



                        with st.beta_expander("ANALYSE DES RISQUES RÉALISÉS(JSA)"):
                            st.markdown('### DONNÉE ACTUELLE')
                            df_JSA = pd.DataFrame(view_JSA(), columns=["id","IDD","Chantier","NAct","NJSA","Date"])
                            IDD2 = email.strip('][').split(', ')

                            @st.cache
                            def JSA_2(df_JSA: pd.DataFrame) -> pd.DataFrame:
                                df_JSA2 = df_JSA[(df_JSA["IDD"].isin(IDD2))]
                                return df_JSA2.loc[1:, ["id","Chantier","NAct","NJSA","Date"]]

                            df_JSA1 = JSA_2(df_JSA)
                            #filtrage par chantier
                            splitted_df_JSA1 = df_JSA1['Chantier'].str.split(',')
                            unique_vals6 = list(dict.fromkeys([y for x in splitted_df_JSA1  for y in x]).keys())
                            filtrechantier6 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals6,key=31)
                            mask = (df_JSA1['Chantier'] == filtrechantier6)
                            df_filter6=df_JSA1.loc[mask]
                            st.dataframe(df_filter6)

                            idval = list(df_filter6['id'])
                            selected_id = st.selectbox("SELECTIONEZ l'ID DE LA LIGNE À SUPPRIMER", idval,key=15)
                            name_delete = get_id_JSA(selected_id)
                            if name_delete:
                                id = name_delete[0][0]
                                if st.button("SUPPRIMER",key=4):
                                    delete_data_JSA(name_delete)
                                    st.warning("SUPPRIMER: '{}'".format(name_delete))
                                    
                                st.markdown('### DONNÉE MODIFIÉE')
                                df_JSA = pd.DataFrame(view_JSA(), columns=["id","IDD","Chantier","NAct","NJSA","Date"])
                                IDD2 = email.strip('][').split(', ')

                                @st.cache
                                def JSA_2(df_JSA: pd.DataFrame) -> pd.DataFrame:
                                    df_JSA2 = df_JSA[(df_JSA["IDD"].isin(IDD2))]
                                    return df_JSA2.loc[1:, ["id","Chantier","NAct","NJSA","Date"]]

                                df_JSA1 = JSA_2(df_JSA)
                                #filtrage par chantier
                                splitted_df_JSA1 = df_JSA1['Chantier'].str.split(',')
                                unique_vals6 = list(dict.fromkeys([y for x in splitted_df_JSA1  for y in x]).keys())
                                filtrechantier6 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals6,key=32)
                                mask = (df_JSA1['Chantier'] == filtrechantier6)
                                df_filter6=df_JSA1.loc[mask]
                                st.dataframe(df_filter6)


                        with st.beta_expander("INCIDENT & ACCIDENT"):
                            st.markdown('### DONNÉE ACTUELLE')
                            df_IA = pd.DataFrame(view_Incident_Accident(), columns=["id","IDD","Chantier","NInc","AAA","ASA","AT","NJP","Date"])
                            IDD2 = email.strip('][').split(', ')

                            @st.cache
                            def IA_2(df_IA: pd.DataFrame) -> pd.DataFrame:
                                df_IA = df_IA[(df_IA["IDD"].isin(IDD2))]
                                return df_IA.loc[1:, ["id","Chantier","NInc","AAA","ASA","AT","NJP","Date"]]

                            df_IA1 = IA_2(df_IA)

                            #filtrage par chantier
                            splitted_df_IA1 = df_IA1['Chantier'].str.split(',')
                            unique_vals7 = list(dict.fromkeys([y for x in splitted_df_IA1  for y in x]).keys())
                            filtrechantier7 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals7,key=33)
                            mask = (df_IA1['Chantier'] == filtrechantier7)
                            df_filter7=df_IA1.loc[mask]
                            st.dataframe(df_filter7)

                            idval = list(df_filter7['id'])
                            selected_id = st.selectbox("SELECTIONEZ l'ID DE LA LIGNE À SUPPRIMER", idval,key=16)
                            name_delete = get_id_Incident_Accident(selected_id)
                            if name_delete:
                                id = name_delete[0][0]
                                if st.button("SUPPRIMER",key=5):
                                    delete_data_Incident_Accident(name_delete)
                                    st.warning("SUPPRIMER: '{}'".format(name_delete))
                                    
                                st.markdown('### DONNÉE MODIFIÉE')
                                df_IA = pd.DataFrame(view_Incident_Accident(), columns=["id","IDD","Chantier","NInc","AAA","ASA","AT","NJP","Date"])
                                IDD2 = email.strip('][').split(', ')

                                @st.cache
                                def IA_2(df_IA: pd.DataFrame) -> pd.DataFrame:
                                    df_IA = df_IA[(df_IA["IDD"].isin(IDD2))]
                                    return df_IA.loc[1:, ["id","Chantier","NInc","AAA","ASA","AT","NJP","Date"]]

                                df_IA1 = IA_2(df_IA)

                                #filtrage par chantier
                                splitted_df_IA1 = df_IA1['Chantier'].str.split(',')
                                unique_vals7 = list(dict.fromkeys([y for x in splitted_df_IA1  for y in x]).keys())
                                filtrechantier7 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals7,key=34)
                                mask = (df_IA1['Chantier'] == filtrechantier7)
                                df_filter7=df_IA1.loc[mask]
                                st.dataframe(df_filter7)


                        with st.beta_expander("AUDIT CHANTIER; VISITE CONJOINTE;  PRÉVENTION ET INSPECTION"):
                            st.markdown('### DONNÉE ACTUELLE')
                            df_Audit = pd.DataFrame(view_Audit(), columns=["id","IDD","Chantier","AC","VC","NEU","SMPAR","NPR","IE","Date"])
                            IDD2 = email.strip('][').split(', ')

                            @st.cache
                            def Audit_2(df_Audit: pd.DataFrame) -> pd.DataFrame:
                                df_Audit = df_Audit[(df_Audit["IDD"].isin(IDD2))]
                                return df_Audit.loc[1:, ["id","Chantier","AC","VC","NEU","SMPAR","NPR","IE","Date"]]

                            df_Audit1 = Audit_2(df_Audit)
                            #filtrage par chantier
                            splitted_df_Audit1 = df_Audit1['Chantier'].str.split(',')
                            unique_vals8 = list(dict.fromkeys([y for x in splitted_df_Audit1  for y in x]).keys())
                            filtrechantier8 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals8,key=355)
                            mask = (df_Audit1['Chantier'] == filtrechantier8)
                            df_filter8=df_Audit1.loc[mask]
                            st.dataframe(df_filter8)

                            idval = list(df_filter8['id'])
                            selected_id = st.selectbox("SELECTIONEZ l'ID DE LA LIGNE À SUPPRIMER", idval,key=17)
                            name_delete = get_id_Audit(selected_id)
                            if name_delete:
                                id = name_delete[0][0]
                                if st.button("SUPPRIMER",key=6):
                                    delete_data_Audit(name_delete)
                                    st.warning("SUPPRIMER: '{}'".format(name_delete))
                                
                                st.markdown('### DONNÉE MODIFIÉE')
                                df_Audit = pd.DataFrame(view_Audit(), columns=["id","IDD","Chantier","AC","VC","NEU","SMPAR","NPR","IE","Date"])
                                IDD2 = email.strip('][').split(', ')

                                @st.cache
                                def Audit_2(df_Audit: pd.DataFrame) -> pd.DataFrame:
                                    df_Audit = df_Audit[(df_Audit["IDD"].isin(IDD2))]
                                    return df_Audit.loc[1:, ["id","Chantier","AC","VC","NEU","SMPAR","NPR","IE","Date"]]

                                df_Audit1 = Audit_2(df_Audit)
                                #filtrage par chantier
                                splitted_df_Audit1 = df_Audit1['Chantier'].str.split(',')
                                unique_vals8 = list(dict.fromkeys([y for x in splitted_df_Audit1  for y in x]).keys())
                                filtrechantier8 = st.selectbox('AFFICHEZ VOTRE GRILLE EN FONCTION DU CHANTIER', unique_vals8,key=36)
                                mask = (df_Audit1['Chantier'] == filtrechantier8)
                                df_filter8=df_Audit1.loc[mask]
                                st.dataframe(df_filter8)                                    
        

                            

                                                    

                                                       




                                
                























            else:
                st.warning("Veuillez-vous enregistrer")





    elif choice == "Inscription":
        st.subheader("Créer un nouveau compte")
        new_user = st.text_input("Email")
        new_password = st.text_input("Mot de passe",type='password')
        

        if st.button("Inscription"):
            #pour valider l'entrée email
            regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
            if(re.search(regex, new_user)):
                new_user
            else:
                st.error("Email non valide")
                st.stop()
            create_table()
            add_userdata(new_user,make_hashes(new_password))
            #initialisation de la base de donné pour l'application je l'ai incrusté ici rien avoir avec le code login
            IDD=new_user
            Chantier=0
            NArrivant=0
            Ninduction=0
            NChantier=0
            NTBM=0
            NCR=0
            FNCR=0
            NCC=0
            FNCC=0
            NCH=0
            FNCH=0
            NCHC=0
            FNCHC=0
            NA=0
            FNA=0
            NAC=0
            FNAC=0
            NAct=0
            NJSA=0
            NInc=0
            AAA=0
            ASA=0
            AT=0
            NJP=0
            AC=0
            VC=0
            NEU=0
            SMPAR=0
            NPR=0
            IE=0
            
            T1=(datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
            T2=(datetime.now() - timedelta(2)).strftime('%Y-%m-%d')
            Date=T2
            Date2=T1
            c.execute('INSERT INTO Accueil(IDD,Chantier,NArrivant,Ninduction,Date) VALUES (%s,%s,%s,%s,%s)',(IDD,Chantier,NArrivant,Ninduction,Date2))
            conn.commit()
            c.execute('INSERT INTO Accueil(IDD,Chantier,NArrivant,Ninduction,Date) VALUES (%s,%s,%s,%s,%s)',(IDD,Chantier,NArrivant,Ninduction,Date2))
            conn.commit()
            c.execute('INSERT INTO TBM(IDD,Chantier,NChantier,NTBM,Date) VALUES (%s,%s,%s,%s,%s)',(IDD,Chantier,NChantier,NTBM,Date))
            conn.commit()
            c.execute('INSERT INTO TBM(IDD,Chantier,NChantier,NTBM,Date) VALUES (%s,%s,%s,%s,%s)',(IDD,Chantier,NChantier,NTBM,Date2))
            conn.commit()
            c.execute('INSERT INTO NC(IDD,Chantier,NCR,FNCR,NCC,FNCC,Date) VALUES (%s,%s,%s,%s,%s,%s,%s)',(IDD,Chantier,NCR,FNCR,NCC,FNCC,Date))
            conn.commit()

            c.execute('INSERT INTO NC(IDD,Chantier,NCR,FNCR,NCC,FNCC,Date) VALUES (%s,%s,%s,%s,%s,%s,%s)',(IDD,Chantier,NCR,FNCR,NCC,FNCC,Date2))
            conn.commit()
            c.execute('INSERT INTO Changements(IDD,Chantier,NCH,FNCH,NCHC,FNCHC,Date) VALUES (%s,%s,%s,%s,%s,%s,%s)',(IDD,Chantier,NCH,FNCH,NCHC,FNCHC,Date))
            conn.commit()
            c.execute('INSERT INTO Changements(IDD,Chantier,NCH,FNCH,NCHC,FNCHC,Date) VALUES (%s,%s,%s,%s,%s,%s,%s)',(IDD,Chantier,NCH,FNCH,NCHC,FNCHC,Date2))
            conn.commit()
            c.execute('INSERT INTO Anomalies(IDD,Chantier,NA,FNA,NAC,FNAC,Date) VALUES (%s,%s,%s,%s,%s,%s,%s)',(IDD,Chantier,NA,FNA,NAC,FNAC,Date))
            conn.commit()
            c.execute('INSERT INTO Anomalies(IDD,Chantier,NA,FNA,NAC,FNAC,Date) VALUES (%s,%s,%s,%s,%s,%s,%s)',(IDD,Chantier,NA,FNA,NAC,FNAC,Date2))
            conn.commit()
            c.execute('INSERT INTO JSA(IDD,Chantier,NAct,NJSA,Date) VALUES (%s,%s,%s,%s,%s)',(IDD,Chantier,NAct,NJSA,Date))
            conn.commit()
            c.execute('INSERT INTO JSA(IDD,Chantier,NAct,NJSA,Date) VALUES (%s,%s,%s,%s,%s)',(IDD,Chantier,NAct,NJSA,Date2))
            conn.commit()
            c.execute('INSERT INTO Incident_Accident(IDD,Chantier,NInc,AAA,ASA,AT,NJP,Date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(IDD,Chantier,NInc,AAA,ASA,AT,NJP,Date))
            conn.commit()
            c.execute('INSERT INTO Incident_Accident(IDD,Chantier,NInc,AAA,ASA,AT,NJP,Date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(IDD,Chantier,NInc,AAA,ASA,AT,NJP,Date2))
            conn.commit()
            c.execute('INSERT INTO Audit(IDD,Chantier,AC,VC,NEU,SMPAR,NPR,IE,Date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(IDD,Chantier,AC,VC,NEU,SMPAR,NPR,IE,Date))
            conn.commit()
            c.execute('INSERT INTO Audit(IDD,Chantier,AC,VC,NEU,SMPAR,NPR,IE,Date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(IDD,Chantier,AC,VC,NEU,SMPAR,NPR,IE,Date2))
            conn.commit()
            ####fin
            st.success("Votre compte a été créé avec succès")
            st.info("Allez au menu de connexion pour vous connecter")
        col1, col2, col3 = st.beta_columns([1,6,1])
        with col2:
            st.image("http://cabinetnpm.com/wp-content/uploads/2020/02/t%C3%A9l%C3%A9chargement.png",width=200,)





image_ren ="""
<img src="https://1tpecash.fr/wp-content/uploads/elementor/thumbs/Renaud-Louis-osf6t5lcki4q31uzfafpi9yx3zp4rrq7je8tj6p938.png" alt="Avatar" style="vertical-align: middle;width: 100px;height: 100px;border-radius: 50%;" >
"""

st.sidebar.markdown(image_ren, unsafe_allow_html = True)
st.sidebar.markdown('**Auteur: Renaud Louis DAHOU**')
st.sidebar.markdown('Email:dahou.r@yahoo.com')
st.sidebar.markdown('[Linkedin](https://www.linkedin.com/in/dahou-renaud-louis-8958599a/)')

if __name__ == '__main__':
    main()
