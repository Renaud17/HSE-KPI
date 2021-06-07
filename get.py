import streamlit as st
import psycopg2
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get('postgres://djmyopoxfiezbi:95b9b8b93a1fabe0440e3d31ffcb6077f55fd04e0ee6061d0c2c5776adc52f89@ec2-35-170-85-206.compute-1.amazonaws.com:5432/dcbt0lh9gd4o55')
con = psycopg2.connect(DATABASE_URL)
c = con.cursor()
#=================================	

	
def get_Chantier(Chantier):
	c.execute('SELECT * FROM Accueil WHERE Chantier="{}"'.format(Chantier))
	data = c.fetchall()
	return data	
	

def get_NArrivant(NArrivant):
	c.execute('SELECT * FROM Accueil WHERE NArrivant="{}"'.format(NArrivant))
	data = c.fetchall()
	return data	
	
	
def get_Ninduction(Ninduction):
	c.execute('SELECT * FROM Accueil WHERE Ninduction="{}"'.format(Ninduction))
	data = c.fetchall()
	return data	


#==========================================================

def get_Chantier(Chantier):
	c.execute('SELECT * FROM TBM WHERE Chantier="{}"'.format(Chantier))
	data = c.fetchall()
	return data
	
def get_NChantier(NChantier):
	c.execute('SELECT * FROM TBM WHERE NChantier="{}"'.format(NChantier))
	data = c.fetchall()
	return data	
	

def get_NArrivant(NTBM):
	c.execute('SELECT * FROM TBM WHERE NTBM="{}"'.format(NTBM))
	data = c.fetchall()
	return data	
	

#===========================

def get_Chantier(Chantier):
	c.execute('SELECT * FROM NC WHERE Chantier="{}"'.format(Chantier))
	data = c.fetchall()
	return data
	

def get_NCR(NCR):
	c.execute('SELECT * FROM NC WHERE NCR="{}"'.format(NCR))
	data = c.fetchall()
	return data


def get_FNCR(FNCR):
	c.execute('SELECT * FROM NC WHERE FNCR="{}"'.format(FNCR))
	data = c.fetchall()
	return data
	
	
def get_NCC(NCC):
	c.execute('SELECT * FROM NC WHERE NCC="{}"'.format(NCC))
	data = c.fetchall()
	return data

	
def get_FNCC(FNCC):
	c.execute('SELECT * FROM NC WHERE FNCC="{}"'.format(FNCC))
	data = c.fetchall()
	return data


#========================================================================

def get_Chantier(Chantier):
	c.execute('SELECT * FROM Changements WHERE Chantier="{}"'.format(Chantier))
	data = c.fetchall()
	return data
	
	
def get_NCH(NCH):
	c.execute('SELECT * FROM Changements WHERE NCH="{}"'.format(NCH))
	data = c.fetchall()
	return data

	
def get_FNCH(FNCH):
	c.execute('SELECT * FROM Changements WHERE FNCH="{}"'.format(FNCH))
	data = c.fetchall()
	return data
	
	
def get_NCHC(NCHC):
	c.execute('SELECT * FROM Changements WHERE NCHC="{}"'.format(NCHC))
	data = c.fetchall()
	return data
	
	
def get_FNCHC(FNCHC):
	c.execute('SELECT * FROM Changements WHERE FNCHC="{}"'.format(FNCHC))
	data = c.fetchall()
	return data
	

#========================================

def get_Chantier(Chantier):
	c.execute('SELECT * FROM Anomalies WHERE Chantier="{}"'.format(Chantier))
	data = c.fetchall()
	return data
	

def get_NA(NA):
	c.execute('SELECT * FROM Anomalies WHERE NA="{}"'.format(NA))
	data = c.fetchall()
	return data

	
def get_FNA(FNA):
	c.execute('SELECT * FROM Anomalies WHERE FNA="{}"'.format(FNA))
	data = c.fetchall()
	return data

	
def get_NAC(NAC):
	c.execute('SELECT * FROM Anomalies WHERE NAC="{}"'.format(NAC))
	data = c.fetchall()
	return data

	
def get_FNAC(FNAC):
	c.execute('SELECT * FROM Anomalies WHERE FNAC="{}"'.format(FNAC))
	data = c.fetchall()
	return data
	

	
#==============================

def get_Chantier(Chantier):
	c.execute('SELECT * FROM JSA WHERE Chantier="{}"'.format(Chantier))
	data = c.fetchall()
	return data

	
def get_NAct(NAct):
	c.execute('SELECT * FROM JSA WHERE NAct="{}"'.format(NAct))
	data = c.fetchall()
	return data

	
def get_NJSA(NJSA):
	c.execute('SELECT * FROM JSA WHERE NJSA="{}"'.format(NJSA))
	data = c.fetchall()
	return data
	

#=================================

def get_Chantier(Chantier):
	c.execute('SELECT * FROM Incident_Accident WHERE Chantier="{}"'.format(Chantier))
	data = c.fetchall()
	return data


def get_NInc(NInc):
	c.execute('SELECT * FROM Incident_Accident WHERE NInc="{}"'.format(NInc))
	data = c.fetchall()
	return data

	
def get_AAA(AAA):
	c.execute('SELECT * FROM Incident_Accident WHERE AAA="{}"'.format(AAA))
	data = c.fetchall()
	return data

	
def get_ASA(ASA):
	c.execute('SELECT * FROM Incident_Accident WHERE ASA="{}"'.format(ASA))
	data = c.fetchall()
	return data
	

def get_AT(AT):
	c.execute('SELECT * FROM Incident_Accident WHERE AT="{}"'.format(AT))
	data = c.fetchall()
	return data
	
	
def get_NJP(NJP):
	c.execute('SELECT * FROM Incident_Accident WHERE NJP="{}"'.format(NJP))
	data = c.fetchall()
	return data



	
#==============================

def get_Chantier(Chantier):
	c.execute('SELECT * FROM Audit WHERE Chantier="{}"'.format(Chantier))
	data = c.fetchall()
	return data


def get_AC(AC):
	c.execute('SELECT * FROM Audit WHERE AC="{}"'.format(AC))
	data = c.fetchall()
	return data

	
def get_VC(VC):
	c.execute('SELECT * FROM Audit WHERE VC="{}"'.format(VC))
	data = c.fetchall()
	return data

	
def get_NEU(NEU):
	c.execute('SELECT * FROM Audit WHERE NEU="{}"'.format(NEU))
	data = c.fetchall()
	return data

	
def get_SMPAR(SMPAR):
	c.execute('SELECT * FROM Audit WHERE SMPAR="{}"'.format(SMPAR))
	data = c.fetchall()
	return data

	
def get_NPR(NPR):
	c.execute('SELECT * FROM Audit WHERE NPR="{}"'.format(NPR))
	data = c.fetchall()
	return data

	
def get_IE(IE):
	c.execute('SELECT * FROM Audit WHERE IE="{}"'.format(IE))
	data = c.fetchall()
	return data
	
#====================================
# nous recuperons les email comme ID pour rÃ©fÃ©rencer la base chaque user



def get_IDD(IDD):
	c.execute('SELECT * FROM userstable WHERE email="{}"'.format(email))
	data = c.fetchall()
	return data	


# get_id =================================
def get_id_Accueil(id):
	c.execute('SELECT * FROM Accueil WHERE id="{}"'.format(id))
	data = c.fetchall()
	return data	

def get_id_TBM(id):
	c.execute('SELECT * FROM TBM WHERE id="{}"'.format(id))
	data = c.fetchall()
	return data	

def get_id_NC(id):
	c.execute('SELECT * FROM NC WHERE id="{}"'.format(id))
	data = c.fetchall()
	return data

def get_id_Changements(id):
	c.execute('SELECT * FROM Changements WHERE id="{}"'.format(id))
	data = c.fetchall()
	return data	

def get_id_Anomalies(id):
	c.execute('SELECT * FROM Anomalies WHERE id="{}"'.format(id))
	data = c.fetchall()
	return data

def get_id_JSA(id):
	c.execute('SELECT * FROM JSA WHERE id="{}"'.format(id))
	data = c.fetchall()
	return data

def get_id_Incident_Accident(id):
	c.execute('SELECT * FROM Incident_Accident WHERE id="{}"'.format(id))
	data = c.fetchall()
	return data

def get_id_Audit(id):
	c.execute('SELECT * FROM Audit WHERE id="{}"'.format(id))
	data = c.fetchall()
	return data

