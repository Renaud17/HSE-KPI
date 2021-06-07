import streamlit as st
#import sqlite3
import psycopg2

#conn = sqlite3.connect('data.db', check_same_thread=False)
#c = conn.cursor()
con = psycopg2.connect(database="dcbt0lh9gd4o55", user="djmyopoxfiezbi", password="95b9b8b93a1fabe0440e3d31ffcb6077f55fd04e0ee6061d0c2c5776adc52f89", host="ec2-35-170-85-206.compute-1.amazonaws.com", port="5432")
c= con.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(id INT PRIMARY KEY,email TEXT UNIQUE,password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS Accueil(id INT PRIMARY KEY,IDD TEXT,Chantier TEXT,NArrivant VARCHAR,Ninduction VARCHAR,Date DATE)')
    c.execute('CREATE TABLE IF NOT EXISTS TBM(id INT PRIMARY KEY,IDD TEXT,Chantier TEXT,NChantier VARCHAR,NTBM VARCHAR,Date DATE)')
    c.execute('CREATE TABLE IF NOT EXISTS NC(id INT PRIMARY KEY,IDD TEXT,Chantier TEXT,NCR VARCHAR,FNCR VARCHAR,NCC VARCHAR,FNCC VARCHAR,Date DATE)')
    c.execute('CREATE TABLE IF NOT EXISTS Changements(id INT PRIMARY KEY,IDD TEXT,Chantier TEXT,NCH VARCHAR,FNCH VARCHAR,NCHC VARCHAR,FNCHC VARCHAR,Date DATE)')
    c.execute('CREATE TABLE IF NOT EXISTS Anomalies(id INT PRIMARY KEY,IDD TEXT,Chantier TEXT,NA VARCHAR,FNA VARCHAR,NAC VARCHAR,FNAC VARCHAR,Date DATE)')
    c.execute('CREATE TABLE IF NOT EXISTS JSA(id INT PRIMARY KEY,IDD TEXT,Chantier TEXT,NAct VARCHAR,NJSA VARCHAR,Date DATE)')
    c.execute('CREATE TABLE IF NOT EXISTS Incident_Accident(id INT PRIMARY KEY,IDD TEXT,Chantier TEXT,NInc VARCHAR,AAA VARCHAR,ASA VARCHAR,AT VARCHAR,NJP VARCHAR,Date DATE)')
    c.execute('CREATE TABLE IF NOT EXISTS Audit(id INT PRIMARY KEY,IDD TEXT,Chantier TEXT,AC VARCHAR,VC VARCHAR,NEU VARCHAR,SMPAR VARCHAR,NPR VARCHAR,IE VARCHAR,Date DATE)')
	
#email,password,	
#========================================================
# les donné que nous souhaitons récupré

def add_Accueil(IDD,Chantier,NArrivant,Ninduction,Date):
	c.execute('INSERT INTO Accueil(IDD,Chantier,NArrivant,Ninduction,Date) VALUES (?,?,?,?,?)',(IDD,Chantier,NArrivant,Ninduction,Date))
	conn.commit()

	
def add_TBM(IDD,Chantier,NChantier,NTBM,Date):
	c.execute('INSERT INTO TBM(IDD,Chantier,NChantier,NTBM,Date) VALUES (?,?,?,?,?)',(IDD,Chantier,NChantier,NTBM,Date))
	conn.commit()	

	
def add_NC(IDD,Chantier,NCR,FNCR,NCC,FNCC,Date):
	c.execute('INSERT INTO NC(IDD,Chantier,NCR,FNCR,NCC,FNCC,Date) VALUES (?,?,?,?,?,?,?)',(IDD,Chantier,NCR,FNCR,NCC,FNCC,Date))
	conn.commit()	


def add_Changements(IDD,Chantier,NCH,FNCH,NCHC,FNCHC,Date):
	c.execute('INSERT INTO Changements(IDD,Chantier,NCH,FNCH,NCHC,FNCHC,Date) VALUES (?,?,?,?,?,?,?)',(IDD,Chantier,NCH,FNCH,NCHC,FNCHC,Date))
	conn.commit()	

	
def add_Anomalies(IDD,Chantier,NA,FNA,NAC,FNAC,Date):
	c.execute('INSERT INTO Anomalies(IDD,Chantier,NA,FNA,NAC,FNAC,Date) VALUES (?,?,?,?,?,?,?)',(IDD,Chantier,NA,FNA,NAC,FNAC,Date))
	conn.commit()	


def add_JSA(IDD,Chantier,NAct,NJSA,Date):
	c.execute('INSERT INTO JSA(IDD,Chantier,NAct,NJSA,Date) VALUES (?,?,?,?,?)',(IDD,Chantier,NAct,NJSA,Date))
	conn.commit()

	
def add_Incident_Accident(IDD,Chantier,NInc,AAA,ASA,AT,NJP,Date):
	c.execute('INSERT INTO Incident_Accident(IDD,Chantier,NInc,AAA,ASA,AT,NJP,Date) VALUES (?,?,?,?,?,?,?,?)',(IDD,Chantier,NInc,AAA,ASA,AT,NJP,Date))
	conn.commit()

	
def add_Audit(IDD,Chantier,AC,VC,NEU,SMPAR,NPR,IE,Date):
	c.execute('INSERT INTO Audit(IDD,Chantier,AC,VC,NEU,SMPAR,NPR,IE,Date) VALUES (?,?,?,?,?,?,?,?,?)',(IDD,Chantier,AC,VC,NEU,SMPAR,NPR,IE,Date))
	conn.commit()
	
#=========================================================================================	
# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib


def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False


def add_userdata(email,password):
    #J'utilise try et except pour chancger le message d'erreur de la base de donnée
    try:
        c.execute('INSERT INTO userstable(email,password) VALUES (?,?)',(email,password))
        conn.commit()
    except:
        st.error("Cet email est déjà utilisé")
        st.stop()
	

def login_user(email,password):
	c.execute('SELECT * FROM userstable WHERE email =? AND password = ?',(email,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
##################################"""""

def view_Accueil():
	c.execute('SELECT * FROM Accueil')
	data = c.fetchall()
	return data
	

def view_TBM():
	c.execute('SELECT * FROM TBM')
	data = c.fetchall()
	return data


def view_NC():
	c.execute('SELECT * FROM NC')
	data = c.fetchall()
	return data
	
	
def view_Changements():
	c.execute('SELECT * FROM Changements')
	data = c.fetchall()
	return data
	

def view_Anomalies():
	c.execute('SELECT * FROM Anomalies')
	data = c.fetchall()
	return data

	
def view_JSA():
	c.execute('SELECT * FROM JSA')
	data = c.fetchall()
	return data
	

def view_Incident_Accident():
	c.execute('SELECT * FROM Incident_Accident')
	data = c.fetchall()
	return data
	

def view_Audit():
	c.execute('SELECT * FROM Audit')
	data = c.fetchall()
	return data
	

#====================================================


def edit_Accueil(new_Chantier,new_NArrivant,new_Ninduction,id):
	c.execute("UPDATE Accueil SET Chantier = ?, NArrivant = ?, Ninduction = ? WHERE id = ?",(new_Chantier,new_NArrivant,new_Ninduction,id))
	conn.commit()
	data = c.fetchall()
	return data

def edit_TBM(new_Chantier,new_NChantier,new_NTBM,id):
	c.execute("UPDATE TBM SET Chantier = ?, NChantier = ?, NTBM = ? WHERE id = ? ",(new_Chantier,new_NChantier,new_NTBM,id))
	conn.commit()
	data = c.fetchall()
	return data
	
	
	
def edit_NC(new_Chantier,new_NCR,new_FNCR,new_NCC,new_FNCC,id):
	c.execute("UPDATE NC SET Chantier = ?, NCR = ?, FNCR = ?, NCC = ?, FNCC = ? WHERE id = ? ",(new_Chantier,new_NCR,new_FNCR,new_NCC,new_FNCC,id))
	conn.commit()
	data = c.fetchall()
	return data
	

def edit_Changements(new_Chantier,new_NCH,new_FNCH,new_NCHC,new_FNCHC,id):
	c.execute("UPDATE Changements SET Chantier = ?, NCH = ?, FNCH = ?, NCHC = ?, FNCHC = ? WHERE id = ? ",(new_Chantier,new_NCH,new_FNCH,new_NCHC,new_FNCHC,id))
	conn.commit()
	data = c.fetchall()
	return data
	

def edit_Anomalies(new_Chantier,new_NA,new_FNA,new_NAC,new_FNAC,id):
	c.execute("UPDATE Anomalies SET Chantier =?, NA = ?, FNA = ?, NAC = ?, FNAC = ? WHERE id = ? ",(new_Chantier,new_NA,new_FNA,new_NAC,new_FNAC,id))
	conn.commit()
	data = c.fetchall()
	return data

	
def edit_JSA(new_Chantier,new_NAct,new_NJSA,id):
	c.execute("UPDATE JSA SET  Chantier = ?, NAct = ?, NJSA = ? WHERE id = ? ",(new_Chantier,new_NAct,new_NJSA,id))
	conn.commit()
	data = c.fetchall()
	return data	
	
	
def edit_Incident_Accident(new_Chantier,new_NInc,new_AAA,new_ASA,new_AT,new_NJP,id):
	c.execute("UPDATE Incident_Accident SET  Chantier =?, NInc = ?, AAA = ?, ASA = ?, AT = ?, NJP = ? WHERE id = ? ",(new_Chantier,new_NInc,new_AAA,new_ASA,new_AT,new_NJP,id))
	conn.commit()
	data = c.fetchall()
	return data	
	
	
def edit_Audit(new_ID,new_Chantier,new_AC,new_VC,new_NEU,new_SMPAR,new_NPR,new_IE,id):
	return data	
	c.execute("UPDATE Audit SET Chantier = ?, AC = ?, VC = ?, NEU = ?, SMPAR = ?, NPR = ?, IE = ? WHERE id = ? ",(new_ID,new_Chantier,new_AC,new_VC,new_NEU,new_SMPAR,new_NPR,new_IE,id))
	conn.commit()
	data = c.fetchall()
	return data	


# delet

def delete_data_Accueil(id):
	c.execute('DELETE FROM Accueil WHERE id="{}"'.format(id))
	conn.commit()

def delete_data_TBM(id):
	c.execute('DELETE FROM TBM WHERE id="{}"'.format(id))
	conn.commit()

def delete_data_TBM(id):
	c.execute('DELETE FROM TBM WHERE id="{}"'.format(id))
	conn.commit()

def delete_data_NC(id):
	c.execute('DELETE FROM NC WHERE id="{}"'.format(id))
	conn.commit()

def delete_data_Changements(id):
	c.execute('DELETE FROM Changements WHERE id="{}"'.format(id))
	conn.commit()

def delete_data_Anomalies(id):
	c.execute('DELETE FROM Anomalies WHERE id="{}"'.format(id))
	conn.commit()

def delete_data_JSA(id):
	c.execute('DELETE FROM JSA WHERE id="{}"'.format(id))
	conn.commit()

def delete_data_Incident_Accident(id):
	c.execute('DELETE FROM Incident_Accident WHERE id="{}"'.format(id))
	conn.commit()


def delete_data_Audit(id):
	c.execute('DELETE FROM Audit WHERE id="{}"'.format(id))
	conn.commit()
