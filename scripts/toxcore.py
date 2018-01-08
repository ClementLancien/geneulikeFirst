#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 5 dec. 2016

@author: tdarde
'''



"""
    Create Toxsign database.
    Allow to create projects,studies,conditions and signatures collection.
    Also give the opportunity to fill database with ChemPSy Data
    Upload GeneInfo,HomoloGenes and all_info files data
    Call by setup.py
"""
import argparse
import sys
import datetime
from time import *
from hashlib import sha1
from random import randint
import bcrypt
import ConfigParser, os
from hashlib import sha1
from pymongo import MongoClient
import elasticsearch
import copy
import json
import logging
from logging.handlers import RotatingFileHandler
 
# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.DEBUG)
 
# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
file_handler = RotatingFileHandler('TOXsIgN_database_creation.log', 'a', 1000000000, 1)
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
 
# création d'un second handler qui va rediriger chaque écriture de log
# sur la console
steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG)
logger.addHandler(steam_handler)




#Functions used for data insertion
#This functions required information from config file
#By default all config information are load from ../tox_install.ini file
#To modifie information please set value in thise file
#DO NOT MODIFIE the tox_install.ini file location 
config = ConfigParser.ConfigParser()
config.readfp(open('../tox_install.ini'))

mongo = MongoClient(config.get('app:main','db_uri'))
db = mongo[config.get('app:main','db_name')]
onto_path = config.get('setup','onto_path')
data_path = config.get('setup','data_path')
admin_path = config.get('setup','admin_path')
public_path = config.get('setup','public_path')
drugmatrix_path = config.get('setup','drugmatrix_path')
tggate_path = config.get('setup','tggate_path')
tggatehuman_path = config.get('setup','tggatehuman_path')
human_path = config.get('setup','human_path')



def get_Index(type):
    try:
        logger.debug('Get_Index')
        db[type].update({'id': 1}, {'$inc': {'val': 1}})
        repos = db[type].find({'id': 1})
        for i in repos :
            return i['val']
    
    except:
        logger.debug('Get_Index')
        logger.error(sys.exc_info()[1])


def get_tag(index,val) :
    try:
        logger.debug('get_tag')
        result=[]
        repos = []
        repo = db[index].find({'id': val})
        for val in repo :
            repos = val
        result.append(repos['id'])
        result.append(repos['name'])
        for i in repos['synonyms'] :
            result.append(i)
        for j in repos['direct_parent'] :
            result.append(j)
        for k in repos['all_parent'] :
            result.append(k)
        for z in repos['all_name'] :
            result.append(z)
        return result
    
    except:
        logger.debug('get_tag')
        logger.error(sys.exc_info()[1])

def dicoChemical():
    try :
        logger.debug('dicoChemical')
        chebiTab = open(data_path+'chebi.obo.tab','r')
        dChemical = {}
        for lines in chebiTab.readlines():
            val = lines.split('\t')
            ID = val[0]
            name = val[2]
            syno = val[3].split('|')
            for i in syno :
                dChemical[i] = ID
            dChemical[name] = ID
        return dChemical
    except:
        logger.debug('dicoChemical')
        logger.error(sys.exc_info()[1])

def NewcondDico():
    fileCond = open(data_path+'/condInfo_Human_GSE.txt','r')
    dico_cond={}
    for lines in fileCond.readlines():
        val = lines.split('\t')
        cond_name = val[0]
        if cond_name not in dico_cond :
            dico_cond[cond_name] = val
    return dico_cond

def getFileCas(fileCond):
    try:
        logger.debug('getFileCas')
        casTab = open(data_path+'ChemPSy_MESH.tsv','r')
        dChemical = {}
        for lines in casTab.readlines():
            val = lines.split('\t')
            fileName = val[0]
            CAS = val[4].split('|')[0]
            dChemical[fileName] = CAS
        return dChemical[fileCond]
    except:
        logger.debug('getFileCas')
        logger.error(sys.exc_info()[1])


def getCAS():
    try:
        logger.debug('getCas')
        chebiTab = open(onto_path+'chemical.tab','r')
        dCAS = {}
        for lines in chebiTab.readlines():
            val = lines.split('\t')
            ID = val[0]
            name = val[2]
            CAS = name.split('CAS:')[1]
            dCAS[CAS] = [name,ID]
        return dCAS
    except:
        logger.debug('getCas')
        logger.error(sys.exc_info()[1])


def dicoRoute(project):
    try:
        logger.debug('dicoRoute')
        dRoute ={}
        routeFile = open(project+'.txt','r')   
        for lines in routeFile.readlines():
            val = lines.split('\t')
            chem = val[5].lower()
            route = val[9]
            dRoute[chem] = route
        
        return dRoute
    except:
        logger.debug('dicoRoute')
        logger.error(sys.exc_info()[1])


def NewdicoRoute(project):
    dRoute ={}
    routeFile = open(human_path+'/'+project+'.txt','r')
    lines = routeFile.readlines()
    for i in range(1,len(lines)):
        val = lines[i].split('\t')
        chem = val[8].lower()
        route = val[13]
        dRoute[chem] = route

    return dRoute

def dicoCAS():
    try:
        logger.debug('dicoCas')
        casTab = open(data_path+'ChemPSy_MESH.tsv','r')
        dChemical = {}
        for lines in casTab.readlines():
            val = lines.split('\t')
            fileName = val[0]
            name = val[1]
            dChemical[fileName] = name
        return dChemical
    except:
        logger.debug('dicoCas')
        logger.error(sys.exc_info()[1])


def dicoSample():
    try:
        logger.debug('dicoSample')
        files = open(data_path+'ChemPSySampleNumber.txt','r')
        dSample = {}
        for lines in files.readlines():
            val = lines.split('\t')
            name = val[0]
            nb_sample = val[1]
            nb_control = val[2]
            dSample[name] = [nb_sample,nb_control]
        return dSample
    except:
        logger.debug('dicoSample')
        logger.error(sys.exc_info()[1])
        
def dicoSampleHuman():
    try:
        logger.debug('dicoSample')
        files = open(data_path+'ChemPSySampleNumberHuman.txt','r')
        dSample = {}
        for lines in files.readlines():
            val = lines.split('\t')
            name = val[0]
            nb_sample = val[1]
            nb_control = val[2]
            dSample[name] = [nb_sample,nb_control]
        return dSample
    except:
        logger.debug('dicoSample')
        logger.error(sys.exc_info()[1])

def condDico():
    fileCond = open(data_path+'condInfo.txt','r')
    dico_cond={}
    for lines in fileCond.readlines():
        val = lines.split('\t')
        cond_name = val[0]
        if cond_name not in dico_cond :
            dico_cond[cond_name] = val
    return dico_cond

def getFileCasHuman(fileCond):
    casTab = open(data_path+'ChemPSy_MESH_human.tsv','r')
    dChemical = {}
    for lines in casTab.readlines():
        val = lines.split('\t')
        fileName = val[0]
        CAS = val[4].split('|')[0]
        dChemical[fileName] = CAS
    return dChemical[fileCond]


def toxOrg(pro):
    try:
        logger.debug('toxOrg')
        toxF = open(data_path+'ChemPSy_MESH.tsv','r')
        dChemical = {}
        for lines in toxF.readlines():
            if pro in lines :
                name = lines.split('\t')[0]
                study = lines.split('\t')[0].split('+')[1]
                cond = lines.split('\t')[0].split('+')[4]+"+"+lines.split('\t')[0].split('+')[5]
                project = lines.split('\t')[1]
                if project not in dChemical :
                    dChemical[project]={}
                if study not in dChemical[project] :
                    dChemical[project][study] = {}
                if cond not in dChemical[project][study] :
                    dChemical[project][study][cond] = name
        return dChemical
    except:
        logger.debug('toxOrg')
        logger.error(sys.exc_info()[1])

def human_toxOrg(pro):
    try:
        logger.debug('toxOrg Human')
        toxF = open(data_path+'ChemPSy_MESH_human.tsv','r')
        dChemical = {}
        for lines in toxF.readlines():
            if pro in lines :
                name = lines.split('\t')[0]
                study = lines.split('\t')[0].split('+')[1]
                cond = lines.split('\t')[0].split('+')[4]+"+"+lines.split('\t')[0].split('+')[5]
                project = lines.split('\t')[1]
                if project not in dChemical :
                    dChemical[project]={}
                if study not in dChemical[project] :
                    dChemical[project][study] = {}
                if cond not in dChemical[project][study] :
                    dChemical[project][study][cond] = name
        return dChemical
    except:
        logger.debug('toxOrg Human')
        logger.error(sys.exc_info()[1])


"""
    ------  Create demo user  ------
    Create a demonstration user for TOXsIgN collections
    
"""
def CreateDemoUser():
    try :
        logger.debug('CreateDemoUser')
        user_id = "demo@toxsign.genouest.org"
        status = "approved"
        password = "XaOP13atGK@@13"
        first_name = "Demo 1"
        last_name = ""
        institute = "INSERM"
        laboratory = "IRSET"
        address = "9 avenue du professeur Léon Bernard"
        referent = ""
        user_password = bcrypt.hashpw(password, bcrypt.gensalt())
        db['users'].insert({'id': user_id,
                        'status': status,
                        'password': user_password,
                        'first_name': first_name,
                        'last_name': last_name,
                        'institute': institute,
                        'laboratory': laboratory,
                        'address': address,
                        'referent': referent,
                        'tool_history': [],
                        'selectedID':[]
                    })
    except:
        logger.debug('CreateDemoUser')
        logger.error(sys.exc_info()[1])
    
"""
    ------  Collections creation  ------
    Create TOXsIgN collections
    Use parsed and formated file for ontologies
    Need genes.info, homologenes.txt and TOXsIgN_geneDB files
"""
def createCounters():
    try :
        logger.debug('CreateCollection - Create projects counters')
        db['project'].insert({'id': 1,
                             'val': 0,
                             })
        db['study'].insert({'id': 1,
                             'val': 0,
                             })
        db['assay'].insert({'id': 1,
                             'val': 0,
                             })
        db['factor'].insert({'id': 1,
                             'val': 0,
                             })
                             
        db['signature'].insert({'id': 1,
                             'val': 0,
                             })
    except:
        logger.debug('CreateCollection - Create projects counters')
        logger.error(sys.exc_info()[1])


def chemicalDB():
    try:
        logger.debug('CreateCollection - insert ontologies')
        for files in os.listdir(onto_path):
            if files == 'chemical.tab':
                print "INSERT: "+files
                fileIn = open(onto_path+files,'r')
                for lines in fileIn.readlines():
                    ids = lines.split('\t')[0]
                    dbs = files
                    if dbs == "go.obo.tab" :
                        dbs = lines.split('\t')[1]
                    name = lines.split('\t')[2]
                    synonyms = lines.split('\t')[3].split("|")
                    direct_parent = lines.split('\t')[4].split("|")
                    all_parent = lines.split('\t')[5].split("|")
                    all_parent_name = lines.split('\t')[6].split("|")
                    #print dbs,ids
                    db[dbs].insert({'id': ids,
                                 'name': name,
                                 'synonyms': synonyms,
                                 'direct_parent': direct_parent,
                                 'all_parent': all_parent,
                                 'all_name': all_parent_name,
                                 })
    except:
        logger.debug('chemicalDB - insert ontologies')
        logger.error(sys.exc_info()[1])
def createCollections():

    
    try:
        logger.debug('CreateCollection - insert ontologies')
        for files in os.listdir(onto_path):
            if files != '.DS_Store':
                print "INSERT: "+files
                fileIn = open(onto_path+files,'r')
                for lines in fileIn.readlines():
                    ids = lines.split('\t')[0]
                    dbs = files
                    if dbs == "go.obo.tab" :
                        dbs = lines.split('\t')[1]
                    name = lines.split('\t')[2]
                    synonyms = lines.split('\t')[3].split("|")
                    direct_parent = lines.split('\t')[4].split("|")
                    all_parent = lines.split('\t')[5].split("|")
                    all_parent_name = lines.split('\t')[6].split("|")
                    #print dbs,ids
                    db[dbs].insert({'id': ids,
                                 'name': name,
                                 'synonyms': synonyms,
                                 'direct_parent': direct_parent,
                                 'all_parent': all_parent,
                                 'all_name': all_parent_name,
                                 })
    except:
        logger.debug('CreateCollection - insert ontologies')
        logger.error(sys.exc_info()[1])
    
    try:
        logger.debug('CreateCollection - create geneInfo collection')
        #Create geneInfo db from geneInfo file
        geneFile = open(data_path+'gene_info_parse','r')
        for geneLine in geneFile.readlines():
            if geneLine[0] != '#':
                tax_id = geneLine.split('\t')[0]
                GeneID = geneLine.split('\t')[1]
                Symbol = geneLine.split('\t')[2] 
                Synonyms = geneLine.split('\t')[4] 
                description = geneLine.split('\t')[8]
                db['geneInfo'].insert({'GeneID': GeneID,
                                  'tax_id' : tax_id,
                                  'Symbol': Symbol,
                                  'Synonyms': Synonyms,
                                  'description': description,
                                  })
        geneFile.close()
    except:
        logger.debug('CreateCollection - create geneInfo collection')
        logger.error(sys.exc_info()[1])
    
    try:
        logger.debug('CreateCollection - create homoloGene collection')
        #Insert homologene ID from homologene.data.txt file
        homologeneFile = open(data_path+'homologene.data.txt','r')
        for homoline in homologeneFile.readlines():
            HID = homoline.split('\t')[0]
            Taxonomy_ID = homoline.split('\t')[1]
            Gene_ID = homoline.split('\t')[2]
            Gene_Symbol = homoline.split('\t')[3]
            Protein_gi = homoline.split('\t')[4]
            Protein_accession = homoline.split('\t')[5]
            db['homoloGene'].insert({'HID': HID,
                                   'Taxonomy_ID' : Taxonomy_ID,
                                   'Gene_ID': Gene_ID,
                                   'Gene_Symbol': Gene_Symbol,
                                   'Protein_gi': Protein_gi,
                                   'Protein_accession': Protein_accession,
                                   })
        homologeneFile.close()
    except:
        logger.debug('CreateCollection - create homoloGene collection')
        logger.error(sys.exc_info()[1])
    
    
    try :
        logger.debug('CreateCollection - create TOXsIgN_geneDB collection')
        #Insert Allbank ID from TOXsIgN_geneDB file
        geneFile = open(data_path+'TOXsIgN_geneDB','r')
        for geneLine in geneFile.readlines():
            if geneLine[0] != '#':
                tax_id = geneLine.split('\t')[0]
                GeneID = geneLine.split('\t')[1]
                Symbol = geneLine.split('\t')[2] 
                Synonyms = geneLine.split('\t')[4] 
                description = geneLine.split('\t')[8]
                HID = geneLine.split('\t')[-1]
                db['genes'].insert({'GeneID': GeneID,
                                 'tax_id' : tax_id,
                                 'Symbol': Symbol,
                                 'Synonyms': Synonyms,
                                 'description': description,
                                 'HID':HID,
                                 })
        geneFile.close()
    except:
        logger.debug('CreateCollection - create TOXsIgN_geneDB collection')
        logger.error(sys.exc_info()[1])
    
"""
    ------  Insertion part  ------
    There is 3 kind of insertion : 
        insertDM : Insert all signatures from DrugMatrix project
        insertTG : Insert TGGates signatures performed on the rat
        insertHumanTG : Insert TGGates signatures performed on the human
    TO DO : (modifie) insertHuman information from GEO dowload and processing signatures
    For database insertion issue, projects are organized as describe : chemical tested > organes where the chemical is tested
"""

def insertDM():
    """
        Insert signatures extrated from ChemPSY processing
        To insert informations please make sur that the following repository is correctlly filled :
            - all_genes_converted files
            - Conditions repository with all individuals conditions
            - Description.txt file
            - projectName.txt file 
            - Studies directory
        This function also required :
            - Individual sample file (Data/files/ChemPSySampleNumber.txt)
            - ChemPSy_MESH.tsv file (Data/files/ChemPSy_MESH.tsv)
    """
    logger.debug('InsertDM - Load dictionnaries')
    projectPath = drugmatrix_path
    projectName = 'DrugMatrix'
    dChemical = dicoCAS()
    dDataset = {}
    dRoute = dicoRoute(drugmatrix_path+'/'+projectName)
    dCAS = dicoCAS()
    dSample=dicoSample()
    dName = {}
    nb_dataset = 0
    nb_study = 0
    nb_cond = 0
    orga = toxOrg('GSE578')



    #DEFINITION DES CONDITIONS PAR CHEMICAL
    logger.debug('InsertDM - Create dico condition')
    for files in os.listdir(projectPath+'Conditions'):
        name = files.replace('_down.txt','').replace('_up.txt','').replace('_noeffects.txt','')
        if 'GSE578' in name :
            if name not in dDataset :
                dDataset[name] =[]

    logger.debug('InsertDM - Insert project')
    for project in orga :
        logger.info(project)
        #print project

        Dataset_authors = 'Scott S. Auerbach'
        Dataset_email = 'auerbachs@niehs.nih.gov'
        Dataset_conditions = []
        Dataset_confidence = ""
        Dataset_contributors=['TOXsIgN Team']
        Dataset_pubmed = ['https://www.ncbi.nlm.nih.gov/pubmed/16005536','http://www.ncbi.nlm.nih.gov/pubmed/25058030']
        Dataset_extlink = "https://www.niehs.nih.gov/research/atniehs/labs/bmsb/toxico/index.cfm|https://ntp.niehs.nih.gov/drugmatrix/index.html|http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE57800|http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE57805|http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE57811|http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE57815|http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE57816".split('|')
        Dataset_description = "DrugMatrix is the scientific communities' largest molecular toxicology reference database and informatics system. DrugMatrix is populated with the comprehensive results of thousands of highly controlled and standardized toxicological experiments in which rats or primary rat hepatocytes were systematically treated with therapeutic, industrial, and environmental chemicals at both non-toxic and toxic doses."
        Dataset_overall = ""
        Dataset_result = ""
        Dataset_owner = 'auerbachs@niehs.nih.gov'
        Dataset_status = "public"
        Dataset_studies = []
        Dataset_ID = 'TSP' + str(get_Index('project'))
        Dataset_title = projectName+" - Toxicogenomics signatures after exposure to "+project+" in the rat"

        # DATASET CREATION
        dt = datetime.datetime.utcnow()
        ztime = mktime(dt.timetuple())
        db['datasets'].insert({'id': Dataset_ID,
                            'title': Dataset_title,
                            'email' : Dataset_email,
                            'authors': Dataset_authors,
                            'conditions': Dataset_conditions,
                            'confidence': Dataset_confidence,
                            'contributors': Dataset_contributors,
                            'pubmed':Dataset_pubmed,
                            'description': Dataset_description,
                            'ext_link':Dataset_extlink,
                            'last_updated':ztime,
                            'overalldesign':Dataset_overall,
                            'owner':Dataset_owner,
                            'result':Dataset_result,
                            'status':Dataset_status,
                            'studies':Dataset_studies,
                            'submission_date':ztime,
        })
        logger.debug('InsertDM - Project inserted')
        nb_dataset = nb_dataset + 1

        organeList = ['LIVER','KIDNEY','HEART','THIGH-MUSCLE']
        for studorg in organeList  :

            if studorg in orga[project]:
                logger.info(studorg)
                print studorg

                study = studorg
                tissue_name = ''
                tissue_ID = ''
                study_description = ''
                if study == 'LIVER' :
                    tissue_name = 'Liver'
                    tissue_ID = 'FMA:7197'
                    study_description = "Complete Drug Matrix dataset for rat liver."
                if study == 'KIDNEY' :
                    tissue_name = 'Kidney'
                    tissue_ID = 'FMA:7203'
                    study_description = "Complete Drug Matrix dataset for rat kidney."
                if study == 'HEART' :
                    tissue_name = 'Heart'
                    tissue_ID = 'FMA:7088'
                    study_description = "Complete Drug Matrix dataset for rat heart."
                if study == 'THIGH-MUSCLE' :
                    tissue_name = 'Skeletal muscle tissue'
                    tissue_ID = 'FMA:14069'
                    study_description = "Complete Drug Matrix dataset for rat thigh muscle."

                Study = {}
                Study['conditions']=[]
                Study['id']= 'TSE' + str(get_Index('study'))
                Study['asso'] = Dataset_ID
                Study['type'] = 'interventional'
                Study['orgatag'] = get_tag('species.tab','NCBITaxon:10116')
                Study['signatures'] = []
                Study['interventional_title'] = projectName+" - Toxicogenomics signatures of "+tissue_name+" after exposure to "+project+" in the rat"
                Study['interventional_design'] = "Approximately 600 different compounds were profiled in up to 7 different rat tissues by obtaining tissue samples from test compound-treated and vehicle control-treated rats in biological triplicates for gene expression analysis after 0.25, 1, 3, and 5 days of exposure with daily dosing. In a few studies (1.8%), 7 days of exposure was substituted for 5 days of exposure. Samples were hybridized to whole genome RG230_2.0 GeneChip arrays (Affymetrix, CA).  DrugMatrix is a comprehensive rat toxicogenomics database and analysis tool developed to facilitate the integration of toxicogenomics into hazard assessment. Using the whole genome and a diverse set of compounds allows a comprehensive view of most pharmacological and toxicological questions and is applicable to other situations such as disease and development. Male Sprague–Dawley (Crl:CD (SD)|GS BR) rats(aged 6–8 weeks) were purchased from Charles River Laboratories (Wilmington, MA). They were housed in plastic cages for 1 week for acclimation to the laboratory environment of a ventilated room (temperature, 22 +- 3 C; humidity 30–70%; 12-h light:12-h dark cycle per day, 6:00 a.m.- 6:00 p.m.) until use. Certified Rodent Diet #5002 (PMI Feeds Inc.) and chlorinated tap water was available ad libitum."
                Study['interventional_description'] = study_description
                Study['interventional_results'] = ""
                Study['interventional_experimental_type'] = 'in_vivo'
                Study['tissuetag'] = []
                Study['celltag'] =[]
                Study['interventional_vivo'] = {}
                Study['interventional_vitro'] = {}
                Study['interventional_exvivo'] = {}
                Study['interventional_other'] = {}
                Study['interventional_vivo']['organism'] = 'Rattus norvegicus'
                Study['interventional_vivo']['strain'] = 'Sprague–Dawley'
                Study['interventional_vivo']['sex'] = 'male'
                Study['interventional_vivo']['devstage'] = 'Adulthood'

                nb_study = nb_study + 1

                for cond in orga[project][studorg] :

                    Chemicals = {}
                    dose = cond.split('+')[0]
                    temps = cond.split('+')[1]
                    #CREATION INFORMATION CONDITION

                    #RECUPERATION NOM | CAS | ROUTE DU CHEMICAL
                    condName = orga[project][studorg][cond]
                    prezfile = 1
                    if condName in dDataset :
                        upFile = open(drugmatrix_path+'Conditions/'+condName+'_up.txt','r')
                        downFile = open(drugmatrix_path+'Conditions/'+condName+'_down.txt','r')
                    else :
                        prezfile = 0

                    CAS = getFileCas(condName)
                    dCas = getCAS()
                    print CAS
                    if CAS.rstrip() not in dCas :
                        chemName = condName.split('+')[2]+' CAS:NA'
                        chemID = ""
                    else :
                        chemName = dCas[CAS.rstrip()][0]
                        chemID = dCas[CAS.rstrip()][1]
                        
                        
                    chemRoute = ""
                    if condName in dCAS :
                        if dCAS[condName] in dRoute :
                            chemRoute = dRoute[dCAS[condName]]
                        else :
                            chemRoute = "other"

                    Condition = {}
                    Condition['id'] = 'TST' + str(get_Index('condition'))
                    Condition['study'] = Study['id']
               
                    Condition['treatment']=[]
                    if chemID != "" :
                         Condition['chemicaltag'] = get_tag('chemical.tab',chemID)
                    else : 
                        Condition['chemicaltag']=[chemName]
                  
                    Treatment = {}
                    Treatment['chemicals']= []

                    doses = dose.split('_')[0]
                    dose_unit = dose.split('_')[1]
                    exposure = temps.split('_')[0]
                    logger.debug("EXPOSURE")
                    logger.debug(exposure)
                    exposure_unit = temps.split('_')[1]
                    time = 0
                    # CHANGE TIME UNIT
                    if exposure_unit == 'd' :
                        exposure_unit = "days"
                        times = float(exposure) * 1440
                    if exposure_unit == 'hr' :
                        exposure_unit = "hours"
                        times = float(exposure) * 60
                    if exposure_unit == 'h' :
                        exposure_unit = "hours"
                        times = float(exposure) * 60
                    if exposure_unit == 'min' :
                        exposure_unit = "minutes"
                        times = float(exposure) * 1

                    Condition['title'] = projectName+" - Toxicogenomics signatures of "+tissue_name+" after exposure to "+project+" ("+doses+" "+dose_unit+", "+exposure+" "+exposure_unit+") in the rat"

                    #############################
                    Chemicals['time']=times
                    Chemicals['dose']=doses
                    Chemicals['dose_unit'] = dose_unit
                    Chemicals['exposure_duration'] = exposure
                    Chemicals['exposure_duration_unit'] = exposure_unit
                    Chemicals['exposure_frequency'] = ''
                    Chemicals['info'] = "The 0.25 and 1-day time points were harvested starting at 1:00 p.m. and completed within 1–2 h, whereas the 3 and 5-day time points were harvested starting at 7:00 a.m. and completed within 2–4 h; all harvests used an appropriately staggered schedule so that the harvest times were accurate to 30 min of the designed dose-to-harvest interval."
                    Chemicals['name'] = chemName
                    Chemicals['route'] = chemRoute
                
                    ###############################################################################
                    
                    ############################## Create signature ###############################
                    Signature = {}
                    Signature['asso_cond'] = Condition['id']
                    Signature['chemical'] = []
                    Signature['time']=Chemicals['time']
                    Signature['chemical'].append(Chemicals['name'])
                    Signature['chemicaltag'] = Condition['chemicaltag']
                    Signature['devstage'] = 'Adulthood' 
                    Signature['diseasetag'] = []
                    Signature['generation'] = 'F0'
                    Signature['id'] = 'TSS' + str(get_Index('signature'))
                    #print Dataset_ID,Study['id'],Condition['id'],Signature['id']
                    Signature['organism'] = 'Rattus norvegicus'
                    Signature['orgatag'] = Study['orgatag']
                    Signature['route'] = chemRoute
                    Signature['sex'] = 'male'
                    Signature['tissue'] = tissue_name
                    if Study['tissuetag'] == []:
                        Signature['tissuetag'] = get_tag('tissue.tab',tissue_ID)
                    else :
                        Signature['tissuetag'] = Study['tissuetag']
                    
                    Signature['celltag'] = Study['celltag']
                    Signature['title'] = Condition['title']
                    Signature['type'] = Study['interventional_experimental_type']
                    Signature['genomic'] =[]
                    Signature['physio'] = []
                    Signature['molecular'] = []
                    Signature['files'] =[]
                    Signature['supfile'] =[]
                    
                    Genomic={}
                    Genomic['statistical'] = 'Affymetrix GeneChip data were quality controlled and normalized using using the RMA package with the custom CDF (GPL1355) provided by the BRAINARRAY resource. Next, data analysis was carried out using the Annotation, Mapping, Expression and Network (AMEN) analysis suite of tools (Chalmel & Primig, 2008). Briefly, genes yielding a signal higher than the detection threshold (median of the normalized dataset) and a fold-change >1.5 between exposed and control samples were selected. A Linear Model for Microarray Data (LIMMA) statistical test (F-value adjusted with the False Discovery Rate method: p < 0.05) was employed to identify significantly differentially expressed genes.'
                    Genomic['techno'] = 'Microarray'
                    Signature['technotag'] = get_tag('experiment.tab','OBI:0400147')
                    Genomic['plateform'] = 'GPL1355'
                    Genomic['pvalue'] = '0.05'
                    Genomic['obs_effect'] = 'Entrez'
                    Genomic['control'] = dSample[condName][0]
                    Genomic['sample'] = dSample[condName][1]
                    Genomic['expe_info'] = ""
                    Genomic['up'] =""
                    Genomic['down'] =""
                    
                    
                    
                    
                    logger.debug('InsertDM - Create signature files')
                    dirCond = public_path+Dataset_ID+"/"+Study['id']+"/"+Condition['id']+"/"+Signature['id']
                
                    os.makedirs(dirCond)
                    if prezfile == 1:
                        Signature['files'].append('genomic_upward.txt')
                        lId = []
                        for idline in upFile.readlines():
                            IDs = idline.replace('\n','\t').replace(',','\t').replace(';','\t')
                            lId.append(IDs.split('\t')[0])
                            Genomic['up'] = Genomic['up'] + idline
                        lId = list(set(lId))
                        upFile.close()
                        dataset_in_db = list(db['genes'].find( {"GeneID": {'$in': lId}},{ "GeneID": 1,"Symbol": 1,"HID":1, "_id": 0 } ))
                        lresult = {}
                        for i in dataset_in_db:
                            lresult[i['GeneID']]=[i['Symbol'],i['HID']]
                        #Create 4 columns signature file
                        if os.path.isfile(os.path.join(dirCond,'genomic_upward.txt')):
                            os.remove(os.path.join(dirCond,'genomic_upward.txt'))
            
                        check_files = open(os.path.join(dirCond,'genomic_upward.txt'),'a')
                        for ids in lId :
                            if ids in lresult :
                                check_files.write(ids+'\t'+lresult[ids][0]+'\t'+lresult[ids][1].replace('\n','')+'\t1\n')
                            else :
                                check_files.write(ids+'\t'+'NA\tNA'+'\t0\n')                
                        check_files.close()
                        
                        
                        
                        Signature['files'].append('genomic_downward.txt')
                        lId = []
                        for idline in downFile.readlines():
                            IDs = idline.replace('\n','\t').replace(',','\t').replace(';','\t')
                            lId.append(IDs.split('\t')[0])
                            Genomic['down'] = Genomic['down'] + idline
                        downFile.close()
                        lId = list(set(lId))
                        dataset_in_db = list(db['genes'].find( {"GeneID": {'$in': lId}},{ "GeneID": 1,"Symbol": 1,"HID":1, "_id": 0 } ))
                        lresult = {}
                        for i in dataset_in_db:
                            lresult[i['GeneID']]=[i['Symbol'],i['HID']]
                        #Create 4 columns signature file
                        if os.path.isfile(os.path.join(dirCond,'genomic_downward.txt')):
                            os.remove(os.path.join(dirCond,'genomic_downward.txt'))
            
                        check_files = open(os.path.join(dirCond,'genomic_downward.txt'),'a')
                        for ids in lId :
                            if ids in lresult :
                                check_files.write(ids+'\t'+lresult[ids][0]+'\t'+lresult[ids][1].replace('\n','')+'\t1\n')
                            else :
                                check_files.write(ids+'\t'+'NA\tNA'+'\t0\n')                  
                        check_files.close() 
               
            
                        
                        
                        
                    if os.path.isfile(os.path.join(dirCond,'genomic_interrogated_genes.txt')):
                        os.remove(os.path.join(dirCond,'genomic_interrogated_genes.txt'))
                    Signature['files'].append('genomic_interrogated_genes.txt')
                    cmd3 = 'cp %s %s' % (projectPath+'all_genes_converted.txt',dirCond+'/genomic_interrogated_genes.txt')
                    os.system(cmd3)
                    
                    
                    
                    upload_path = admin_path
                    all_name = Dataset_ID+'_'+Signature['id']+'.sign'
                    adm_path_signame = os.path.join(upload_path,'signatures_data',all_name)
                    #admin
                    if not os.path.exists(os.path.join(upload_path,'signatures_data')):
                        os.makedirs(os.path.join(upload_path,'signatures_data'))
                    if os.path.isfile(adm_path_signame):
                        os.remove(adm_path_signame)
                
                    check_files = open(adm_path_signame,'a')
                    lfiles = {'genomic_upward.txt':'1','genomic_downward.txt':'-1','genomic_interrogated_genes.txt':'0'}
                    val_geno = 0
                    for filesUsr in os.listdir(dirCond) :
                        if filesUsr in lfiles:
                            fileAdmin = open(dirCond +'/'+filesUsr,'r')
                            print dirCond +'/'+filesUsr
                            for linesFile in fileAdmin.readlines():
                                check_files.write(linesFile.replace('\n','')+'\t'+lfiles[filesUsr]+'\n')
                            fileAdmin.close()
                    check_files.close()

                    
                    #Create Admin files
                    ##################################### Add Condition ###########################
                    Signature['genomic'].append(Genomic)
                    Signature['gene_up'] = Genomic['up']
                    Signature['gene_down'] = Genomic['down']
                    Signature['signature_type'] = 'genomic'
                    Treatment['chemicals'].append(Chemicals) #add chemical to treatment
                    Condition['treatment'].append(Treatment) #add treatment to condition
                    Study['conditions'].append(Condition)    #add condition to study
                    Study['signatures'].append(Signature) #add signature info to study
                    nb_cond = nb_cond + 1
                    ###############################################################################

                    #################################### CREATE DB HTTP ##########################
                ########### END for cond ############################
            ############## END for STUDIES ############################

                logger.info("Update DATASET : %s" % Dataset_ID)
                
                form = db['datasets'].find_one({'id': Dataset_ID})
                del form['_id']
                form['studies'].append(Study)
                db['datasets'].update({'id': Dataset_ID}, form)

                es = elasticsearch.Elasticsearch([config.get('app:main','elastic_host')])
                eform = db['datasets'].find_one({'id': Dataset_ID})
                del eform['_id']
                

                #print "INDEX DATASET : " +Dataset_ID
                bulk_insert = ''
                for study in eform['studies']:
                    for sig in study['signatures']:
                        bulk_insert += "{ \"index\" : { \"_index\" : \"toxsign\", \"_type\": \"signature\" , \"_id\" : \""+Dataset_ID+"_"+study['id']+'_'+sig['id']+"\" } }\n"
                        mysig = copy.deepcopy(eform)
                        mystudy = copy.deepcopy(study)
                        mystudy['signatures']  = [sig]
                        mysig['studies'] = [mystudy]
                        mysig['dataset'] = Dataset_ID
                        bulk_insert += json.dumps(mysig)+"\n"
                if bulk_insert:
                    es.bulk(body=bulk_insert)
    print nb_dataset,nb_study,nb_cond
    
    
def insertTGGATE():
    """
        Insert signatures extrated from ChemPSY processing
        To insert informations please make sur that the following repository is correctlly filled :
            - all_genes_converted files
            - Conditions repository with all individuals conditions
            - Description.txt file
            - projectName.txt file 
            - Studies directory
        This function also required :
            - Individual sample file (Data/files/ChemPSySampleNumber.txt)
            - ChemPSy_MESH.tsv file (Data/files/ChemPSy_MESH.tsv)
    """
    logger.debug('InsertTGGATE - Load dictionnaries')
    projectPath = tggate_path
    projectName = 'TGGATE'
    dChemical = dicoCAS()
    dDataset = {}
    dRoute = dicoRoute(tggate_path+'/'+projectName)
    dCAS = dicoCAS()
    dSample=dicoSample()
    dName = {}
    nb_dataset = 0
    nb_study = 0
    nb_cond = 0
    orga = toxOrg('TGGATE')



    #DEFINITION DES CONDITIONS PAR CHEMICAL
    for files in os.listdir(projectPath+'Conditions'):
        name = files.replace('_down.txt','').replace('_up.txt','').replace('_noeffects.txt','')
        if 'TGGATE' in name :
            if name not in dDataset :
                dDataset[name] =[]

    for project in orga :
        print project
        if project == "1pc cholesterol and 0.25pc sodium cholate":
            print project
        else:

            Dataset_authors = 'Hiroshi Yamada'
            Dataset_email = 'h-yamada@nibio.go.jp'
            Dataset_conditions = []
            Dataset_confidence = ""
            Dataset_contributors=[]
            Dataset_pubmed = ['http://www.ncbi.nlm.nih.gov/pubmed/25313160']
            Dataset_extlink = "https://www.nibiohn.go.jp/english/part/fundamental/detail13.html|http://toxico.nibiohn.go.jp/english/".split('|')
            Dataset_description = "Open TG-GATEs is a public toxicogenomics database developed so that a wider community of researchers could utilize the fruits of TGP and TGP2 research. This database provides public access to data on 170 of the compounds catalogued in TG-GATEs. Data searching can be refined using either the name of a compound or the pathological findings by organ as the starting point. Gene expression data linked to phenotype data in pathology findings can also be downloaded as a CEL(*)file. "
            Dataset_overall = ""
            Dataset_result = ""
            Dataset_owner = 'h-yamada@nibio.go.jp'
            Dataset_status = "public"
            Dataset_studies = []
            Dataset_ID = 'TSP' + str(get_Index('project'))
            Dataset_title = "Open TG-GATEs - Toxicogenomics signatures after exposure to "+project+" in the rat"
    
            # DATASET CREATION
            dt = datetime.datetime.utcnow()
                
            db['datasets'].insert({'id': Dataset_ID,
                                    'title': Dataset_title,
                                    'email':Dataset_email,
                                    'authors': Dataset_authors,
                                    'conditions': Dataset_conditions,
                                    'confidence': Dataset_confidence,
                                    'contributors': Dataset_contributors,
                                    'pubmed':Dataset_pubmed,
                                    'description': Dataset_description,
                                    'ext_link':Dataset_extlink,
                                    'last_updated':mktime(dt.timetuple()),
                                    'overalldesign':Dataset_overall,
                                    'owner':Dataset_owner,
                                    'result':Dataset_result,
                                    'status':Dataset_status,
                                    'studies':Dataset_studies,
                                    'submission_date':mktime(dt.timetuple()),
            })
            nb_dataset = nb_dataset + 1
    
    
            organeList = ['LIVER','KIDNEY']
            for studorg in organeList  :
                if studorg in orga[project]:
                    print studorg
    
                    study = studorg
                    #print study
    
    
                    tissue_name = ''
                    tissue_ID = ''
                    study_description = ''
                    if study == 'LIVER' :
                        tissue_name = 'Liver'
                        tissue_ID = 'FMA:7197'
                        study_description = "Complete Drug Matrix dataset for rat liver."
                    if study == 'KIDNEY' :
                        tissue_name = 'Kidney'
                        tissue_ID = 'FMA:7203'
                        study_description = "Complete Drug Matrix dataset for rat kidney."
                    if study == 'HEART' :
                        tissue_name = 'Heart'
                        tissue_ID = 'FMA:7088'
                        study_description = "Complete Drug Matrix dataset for rat heart."
                    if study == 'THIGH-MUSCLE' :
                        tissue_name = 'Skeletal muscle tissue'
                        tissue_ID = 'FMA:14069'
                        study_description = "Complete Drug Matrix dataset for rat thigh muscle."
    
                    Study = {}
                    Study['conditions']=[]
                    Study['id']= 'TSE' + str(get_Index('study'))
                    Study['asso'] = Dataset_ID
                    Study['type'] = 'interventional'
                    Study['orgatag'] = get_tag('species.tab','NCBITaxon:10116')
                    Study['signatures'] = []
                    Study['interventional_title'] = "Open TG-GATEs - Toxicogenomics signatures of "+tissue_name+" after exposure to "+project+" in the rat"
                    Study['interventional_design'] = "Animal experiments were conducted by four different contract research organizations. The studies used male Crl:CD Sprague-Dawley (SD) rats purchased from Charles River Japan, Inc. (Hino or Atsugi, Japan) as 5-week-old animals. After a 7-day quarantine and acclimatization period, the animals were allocated into groups of 20 animals each using a computerized stratified random grouping method based on body weight. Each animal was allowed free access to water and pelleted food (radiation-sterilized CRF-1; Oriental Yeast Co., Tokyo, Japan). For single-dose experiments, groups of 20 animals were administered a compound and then fivw animals/time point were sacrificed at 3, 6, 9 or 24 h after administration. For repeated-dose experiments, groups of 20 animals received a single dose per day of a compound and five animals/time point were sacrificed at 4, 8, 15 or 29 days (i.e. 24 h after the respective final administration at 3, 7, 14 or 28 days). Animals were not fasted before being sacrificed. To avoid effects of diurnal cycling, the animals were sacrificed and necropsies were performed between 9:00 a.m. and 11:00 a.m. for the repeated-dose studies. Blood samples for routine biochemical analyses were collected into heparinized tubes under ether anesthesia from the abdominal aorta at the time of sacrifice."
                    Study['interventional_description'] = study_description
                    Study['interventional_results'] = ""
                    Study['interventional_experimental_type'] = 'in_vivo'
                    Study['tissuetag'] = []
                    Study['celltag'] =[]
                    Study['interventional_vivo'] = {}
                    Study['interventional_vitro'] = {}
                    Study['interventional_exvivo'] = {}
                    Study['interventional_other'] = {}
                    Study['interventional_vivo']['organism'] = 'Rattus norvegicus'
                    Study['interventional_vivo']['strain'] = 'Sprague–Dawley'
                    Study['interventional_vivo']['sex'] = 'male'
                    Study['interventional_vivo']['devstage'] = 'Adulthood'
    
                    nb_study = nb_study + 1
    
                    for cond in orga[project][studorg] :
    
                        Chemicals = {}
                        dose = cond.split('+')[0]
                        print cond
                        temps = cond.split('+')[1]
                        print temps
                         #CREATION INFORMATION CONDITION
    
                         #RECUPERATION NOM | CAS | ROUTE DU CHEMICAL
                        condName = orga[project][studorg][cond]
                        prezfile = 1
                        if condName in dDataset :
                            upFile = open(projectPath+'Conditions/'+condName+'_up.txt','r')
                            downFile = open(projectPath+'Conditions/'+condName+'_down.txt','r')
                        else :
                            prezfile = 0
    
                        CAS = getFileCas(condName)
                        dCas = getCAS()
                        if CAS.rstrip() not in dCas :
                            chemName = files.split('+')[2]+' CAS:NA'
                            chemID = ""
                        else :
                            chemName = dCas[CAS.rstrip()][0]
                            chemID = dCas[CAS.rstrip()][1]
                        chemRoute = ""
                        if condName in dCAS :
                            if dCAS[condName] in dRoute :
                                chemRoute = dRoute[dCAS[condName]]
                            else :
                                chemRoute = "other"
    
                        Condition = {}
                        Condition['id'] = 'TST' + str(get_Index('condition'))
                        Condition['study'] = Study['id']
                       
                        Condition['treatment']=[]
                        if chemID != "" :
                             Condition['chemicaltag'] = get_tag('chemical.tab',chemID)
                        else : 
                            Condition['chemicaltag']=[chemName]
                      
                        Treatment = {}
                        Treatment['chemicals']= []
    
                        doses = dose.split('_')[0]
                        dose_unit = dose.split('_')[1]
                        exposure = temps.split('_')[0]
                        exposure_unit = temps.split('_')[1]
                        timeexpo = 0
                        # CHANGE TIME UNIT
                        if exposure_unit == 'd' :
                            exposure_unit = "days"
                            timeexpo = float(exposure) * 1440
                        if exposure_unit == 'hr' :
                            exposure_unit = "hours"
                            timeexpo = float(exposure) * 60
                        if exposure_unit == 'h' :
                            exposure_unit = "hours"
                            timeexpo = float(exposure) * 60
                        if exposure_unit == 'min' :
                            exposure_unit = "minutes"
                            timeexpo = float(exposure) * 1
    
                        Condition['title'] = "Open TG-GATEs  - Toxicogenomics signatures of "+tissue_name+" after exposure to "+project+" ("+doses+" "+dose_unit+", "+exposure+" "+exposure_unit+") in the rat"
    
                        #############################
                        Chemicals['time']=timeexpo
                        Chemicals['dose']=doses
                        Chemicals['dose_unit'] = dose_unit
                        Chemicals['exposure_duration'] = exposure
                        Chemicals['exposure_duration_unit'] = exposure_unit
                        Chemicals['exposure_frequency'] = ''
                        Chemicals['info'] = "For the in vivo studies, the highest dose was selected to match the level demonstrated to induce the minimum toxic effect over the course of a 4-week toxicity study. In principle, the ratio of the concentrations for the low, middle and high dose levels was set as 1:3:10. "
                        Chemicals['name'] = chemName
                        Chemicals['route'] = chemRoute
                        
                        ###############################################################################
                        
                        ############################## Create signature ###############################
                        Signature = {}
                        Signature['time'] = Chemicals['time']
                        Signature['asso_cond'] = Condition['id']
                        Signature['chemical'] = []
                        Signature['chemical'].append(Chemicals['name'])
                        Signature['chemicaltag'] = Condition['chemicaltag']
                        Signature['devstage'] = 'Adulthood' 
                        Signature['diseasetag'] = []
                        Signature['generation'] = 'F0'
                        Signature['id'] = 'TSS' + str(get_Index('signature'))
                        print Dataset_ID,Study['id'],Condition['id'],Signature['id']
                        Signature['organism'] = 'Rattus norvegicus'
                        Signature['orgatag'] = Study['orgatag']
                        Signature['route'] = chemRoute
                        Signature['sex'] = 'male'
                        Signature['tissue'] = tissue_name
                        if Study['tissuetag'] == []:
                            Signature['tissuetag'] = get_tag('tissue.tab',tissue_ID)
                        else :
                            Signature['tissuetag'] = Study['tissuetag']
                        
                        Signature['celltag'] = Study['celltag']
                        Signature['title'] = Condition['title']
                        Signature['type'] = Study['interventional_experimental_type']
                        Signature['genomic'] =[]
                        Signature['physio'] = []
                        Signature['molecular'] = []
                        Signature['files'] =[]
                        Signature['supfile'] =[]
                        
                        Genomic={}
                        Genomic['statistical'] = 'Affymetrix GeneChip data were quality controlled and normalized using using the RMA package with the custom CDF (GPL1355) provided by the BRAINARRAY resource. Next, data analysis was carried out using the Annotation, Mapping, Expression and Network (AMEN) analysis suite of tools (Chalmel & Primig, 2008). Briefly, genes yielding a signal higher than the detection threshold (median of the normalized dataset) and a fold-change >1.5 between exposed and control samples were selected. A Linear Model for Microarray Data (LIMMA) statistical test (F-value adjusted with the False Discovery Rate method: p < 0.05) was employed to identify significantly differentially expressed genes.'
                        Genomic['techno'] = 'Microarray'
                        Signature['technotag'] = get_tag('experiment.tab','OBI:0400147')
                        Genomic['plateform'] = 'GPL1355'
                        Genomic['pvalue'] = '0.05'
                        Genomic['obs_effect'] = 'Entrez'
                        Genomic['control'] = dSample[condName][0]
                        Genomic['sample'] = dSample[condName][1]
                        Genomic['expe_info'] = ""
                        Genomic['up'] =""
                        Genomic['down'] =""
                        Genomic['files'] =[]
                        
                        
                        
                        logger.debug('InsertDM - Create signature files')
                        dirCond = public_path+Dataset_ID+"/"+Study['id']+"/"+Condition['id']+"/"+Signature['id']
                    
                        os.makedirs(dirCond)
                        if prezfile == 1:
                            Signature['files'].append('genomic_upward.txt')
                            lId = []
                            for idline in upFile.readlines():
                                IDs = idline.replace('\n','\t').replace(',','\t').replace(';','\t')
                                lId.append(IDs.split('\t')[0])
                                Genomic['up'] = Genomic['up'] + idline
                            lId = list(set(lId))
                            upFile.close()
                            dataset_in_db = list(db['genes'].find( {"GeneID": {'$in': lId}},{ "GeneID": 1,"Symbol": 1,"HID":1, "_id": 0 } ))
                            lresult = {}
                            for i in dataset_in_db:
                                lresult[i['GeneID']]=[i['Symbol'],i['HID']]
                            #Create 4 columns signature file
                            if os.path.isfile(os.path.join(dirCond,'genomic_upward.txt')):
                                os.remove(os.path.join(dirCond,'genomic_upward.txt'))
                
                            check_files = open(os.path.join(dirCond,'genomic_upward.txt'),'a')
                            for ids in lId :
                                if ids in lresult :
                                    check_files.write(ids+'\t'+lresult[ids][0]+'\t'+lresult[ids][1].replace('\n','')+'\t1\n')
                                else :
                                    check_files.write(ids+'\t'+'NA\tNA'+'\t0\n')                
                            check_files.close()
                            
                            
                            
                            Signature['files'].append('genomic_downward.txt')
                            lId = []
                            for idline in downFile.readlines():
                                IDs = idline.replace('\n','\t').replace(',','\t').replace(';','\t')
                                lId.append(IDs.split('\t')[0])
                                Genomic['down'] = Genomic['down'] + idline
                            downFile.close()
                            lId = list(set(lId))
                            dataset_in_db = list(db['genes'].find( {"GeneID": {'$in': lId}},{ "GeneID": 1,"Symbol": 1,"HID":1, "_id": 0 } ))
                            lresult = {}
                            for i in dataset_in_db:
                                lresult[i['GeneID']]=[i['Symbol'],i['HID']]
                            #Create 4 columns signature file
                            if os.path.isfile(os.path.join(dirCond,'genomic_downward.txt')):
                                os.remove(os.path.join(dirCond,'genomic_downward.txt'))
                
                            check_files = open(os.path.join(dirCond,'genomic_downward.txt'),'a')
                            for ids in lId :
                                if ids in lresult :
                                    check_files.write(ids+'\t'+lresult[ids][0]+'\t'+lresult[ids][1].replace('\n','')+'\t1\n')
                                else :
                                    check_files.write(ids+'\t'+'NA\tNA'+'\t0\n')                  
                            check_files.close() 
                   
                
                            
                            
                            
                        if os.path.isfile(os.path.join(dirCond,'genomic_interrogated_genes.txt')):
                            os.remove(os.path.join(dirCond,'genomic_interrogated_genes.txt'))
                        Signature['files'].append('genomic_interrogated_genes.txt')
                        cmd3 = 'cp %s %s' % (projectPath+'all_genes_converted.txt',dirCond+'/genomic_interrogated_genes.txt')
                        os.system(cmd3)
                        
                        
                        
                        upload_path = admin_path
                        all_name = Dataset_ID+'_'+Signature['id']+'.sign'
                        adm_path_signame = os.path.join(upload_path,'signatures_data',all_name)
                        #admin
                        if not os.path.exists(os.path.join(upload_path,'signatures_data')):
                            os.makedirs(os.path.join(upload_path,'signatures_data'))
                        if os.path.isfile(adm_path_signame):
                            os.remove(adm_path_signame)
                    
                        check_files = open(adm_path_signame,'a')
                        lfiles = {'genomic_upward.txt':'1','genomic_downward.txt':'-1','genomic_interrogated_genes.txt':'0'}
                        val_geno = 0
                        for filesUsr in os.listdir(dirCond) :
                            if filesUsr in lfiles:
                                fileAdmin = open(dirCond +'/'+filesUsr,'r')
                                print dirCond +'/'+filesUsr
                                for linesFile in fileAdmin.readlines():
                                    check_files.write(linesFile.replace('\n','')+'\t'+lfiles[filesUsr]+'\n')
                                fileAdmin.close()
                        check_files.close()
                        
    
                        ##################################### Add Condition ###########################
                        Signature['genomic'].append(Genomic)
                        Signature['gene_up'] = Genomic['up']
                        Signature['gene_down'] = Genomic['down']
                        Signature['signature_type'] = 'genomic'
                        Treatment['chemicals'].append(Chemicals) #add chemical to treatment
                        Condition['treatment'].append(Treatment) #add treatment to condition
                        Study['conditions'].append(Condition)    #add condition to study
                        Study['signatures'].append(Signature) #add signature info to study
                        nb_cond = nb_cond + 1
                        ###############################################################################
                    ########### END for cond ############################
                    ############## END for STUDIES ############################
                    print "Update DATASET : " +Dataset_ID
                    form = db['datasets'].find_one({'id': Dataset_ID})
                    del form['_id']
                    form['studies'].append(Study)
                    db['datasets'].update({'id': Dataset_ID}, form)
    
                    es = elasticsearch.Elasticsearch([config.get('app:main','elastic_host')])
                    eform = db['datasets'].find_one({'id': Dataset_ID})
                    del eform['_id']
                    
                    #print "INDEX DATASET : " +Dataset_ID
                    bulk_insert = ''
                    for study in eform['studies']:
                        for sig in study['signatures']:
                            bulk_insert += "{ \"index\" : { \"_index\" : \"toxsign\", \"_type\": \"signature\" , \"_id\" : \""+Dataset_ID+"_"+study['id']+'_'+sig['id']+"\" } }\n"
                            mysig = copy.deepcopy(eform)
                            mystudy = copy.deepcopy(study)
                            mystudy['signatures']  = [sig]
                            mysig['studies'] = [mystudy]
                            mysig['dataset'] = Dataset_ID
                            bulk_insert += json.dumps(mysig)+"\n"
                    if bulk_insert:
                        es.bulk(body=bulk_insert)
    print nb_dataset,nb_study,nb_cond





def insertHumanTG():
    """
        Insert signatures extrated from ChemPSY processing
        To insert informations please make sur that the following repository is correctlly filled :
            - all_genes_converted files
            - Conditions repository with all individuals conditions
            - Description.txt file
            - projectName.txt file 
            - Studies directory
        This function also required :
            - Individual sample file (Data/files/ChemPSySampleNumber.txt)
            - ChemPSy_MESH.tsv file (Data/files/ChemPSy_MESH.tsv)
    """
    #LOAD DICTIONNARIES
    logger.debug('insertHumanTG - Load dictionnaries')
    projectPath = tggatehuman_path
    projectName = 'TGGATE_human'
    dChemical = dicoCAS()
    dDataset = {}
    dico_cond = condDico()
    dRoute = dicoRoute(tggatehuman_path+'/'+projectName)
    dCAS = dicoCAS()
    dSample=dicoSampleHuman()
    dName = {}
    nb_dataset = 0
    nb_study = 0
    nb_cond = 0
    orga = human_toxOrg('TGGATE')



    #DEFINITION DES CONDITIONS PAR CHEMICAL
    for files in os.listdir(projectPath+'Conditions'):
        name = files.replace('_down.txt','').replace('_up.txt','').replace('_noeffects.txt','')
        if 'TGGATE' in name :
            if name not in dDataset :
                dDataset[name] =[]

    for project in orga :
        print project
        if project == "1pc cholesterol and 0.25pc sodium cholate":
            print project
        else:

            Dataset_authors = 'Hiroshi Yamada'
            Dataset_email = 'h-yamada@nibio.go.jp'
            Dataset_conditions = []
            Dataset_confidence = ""
            Dataset_contributors=[]
            Dataset_pubmed = ['http://www.ncbi.nlm.nih.gov/pubmed/25313160']
            Dataset_extlink = "https://www.nibiohn.go.jp/english/part/fundamental/detail13.html|http://toxico.nibiohn.go.jp/english/".split('|')
            Dataset_description = "Open TG-GATEs is a public toxicogenomics database developed so that a wider community of researchers could utilize the fruits of TGP and TGP2 research. This database provides public access to data on 170 of the compounds catalogued in TG-GATEs. Data searching can be refined using either the name of a compound or the pathological findings by organ as the starting point. Gene expression data linked to phenotype data in pathology findings can also be downloaded as a CEL(*)file. "
            Dataset_overall = ""
            Dataset_result = ""
            Dataset_owner = "h-yamada@nibio.go.jp"
            Dataset_status = "public"
            Dataset_studies = []
            Dataset_ID = 'TSP' + str(get_Index("project"))
            Dataset_title = "Open TG-GATEs - Toxicogenomics signatures after exposure to "+project+" in human"
            # DATASET CREATION
            dt = datetime.datetime.utcnow()
                
            db['datasets'].insert({'id': Dataset_ID,
                                    'title': Dataset_title,
                                    'email':Dataset_email,
                                    'authors': Dataset_authors,
                                    'conditions': Dataset_conditions,
                                    'confidence': Dataset_confidence,
                                    'contributors': Dataset_contributors,
                                    'pubmed':Dataset_pubmed,
                                    'description': Dataset_description,
                                    'ext_link':Dataset_extlink,
                                    'last_updated':mktime(dt.timetuple()),
                                    'overalldesign':Dataset_overall,
                                    'owner':Dataset_owner,
                                    'result':Dataset_result,
                                    'status':Dataset_status,
                                    'studies':Dataset_studies,
                                    'submission_date':mktime(dt.timetuple()),
            })
            nb_dataset = nb_dataset + 1
    
    
            organeList = ['LIVER','KIDNEY']
            for studorg in organeList  :
                if studorg in orga[project]:
                    print studorg
    
                    study = studorg
                    #print study
    
    
                    tissue_name = ''
                    tissue_ID = ''
                    study_description = ''
                    if study == 'LIVER' :
                        tissue_name = 'Liver'
                        tissue_ID = 'FMA:7197'
                        study_description = "Complete Drug Matrix dataset for human liver."
                    if study == 'KIDNEY' :
                        tissue_name = 'Kidney'
                        tissue_ID = 'FMA:7203'
                        study_description = "Complete Drug Matrix dataset for human kidney."
                    if study == 'HEART' :
                        tissue_name = 'Heart'
                        tissue_ID = 'FMA:7088'
                        study_description = "Complete Drug Matrix dataset for human heart."
                    if study == 'THIGH-MUSCLE' :
                        tissue_name = 'Skeletal muscle tissue'
                        tissue_ID = 'FMA:14069'
                        study_description = "Complete Drug Matrix dataset for human thigh muscle."
    
                    Study = {}
                    Study['conditions']=[]
                    Study['id']= 'TSE' + str(get_Index('study'))
                    Study['asso'] = Dataset_ID
                    Study['type'] = 'interventional'
                    Study['orgatag'] = get_tag('species.tab','NCBITaxon:9606')
                    Study['signatures'] = []
                    Study['interventional_title'] = "Open TG-GATEs - Toxicogenomics signatures of "+tissue_name+" after exposure to "+project+" in human"
                    Study['interventional_design'] = "Human cryopreserved hepatocytes were purchased from Tissue Transformation Technologies, Inc. (Edison, NJ, USA) and CellzDirect, Inc. (Pittsboro, NC, USA). Six lots of human hepatocytes were used during the course of the project."
                    Study['interventional_description'] = study_description
                    Study['interventional_results'] = ""
                    Study['interventional_experimental_type'] = 'in_vitro'
                    Study['tissuetag'] = get_tag('tissue.tab',tissue_ID)
                    Study['celltag'] =[]
                    Study['interventional_vivo'] = {}
                    Study['interventional_vitro'] = {}
                    Study['interventional_exvivo'] = {}
                    Study['interventional_other'] = {}
                    Study['interventional_vitro']['organism'] = 'Homo sapiens'
                    Study['interventional_vitro']['tissue'] = 'Liver'
                    Study['interventional_vitro']['experimental'] = 'primary_cell_culture'
                    Study['interventional_vitro']['cell_name'] = 'Hepatocytes'
                    Study['interventional_vitro']['generation'] = 'f0'
                    Study['interventional_vitro']['strain'] = ''
                    Study['interventional_vitro']['sex'] = 'Male'
                    Study['interventional_vitro']['passage']='na'
    
                    nb_study = nb_study + 1
    
                    for cond in orga[project][studorg] :
    
                        Chemicals = {}
                        dose = cond.split('+')[0]
                        print cond
                        temps = cond.split('+')[1]
                        print temps
                         #CREATION INFORMATION CONDITION
    
                         #RECUPERATION NOM | CAS | ROUTE DU CHEMICAL
                        condName = orga[project][studorg][cond]
                        info = dico_cond[condName]

                        Study['interventional_vitro']['sex'] = info[14]

                        prezfile = 1
                        if condName in dDataset :
                            upFile = open(projectPath+'Conditions/'+condName+'_up.txt','r')
                            downFile = open(projectPath+'Conditions/'+condName+'_down.txt','r')
                        else :
                            prezfile = 0
    
                        CAS = getFileCasHuman(condName)
                        dCas = getCAS()
                        if CAS.rstrip() not in dCas :
                            chemName = files.split('+')[2]+' CAS:NA'
                            chemID = ""
                        else :
                            chemName = dCas[CAS.rstrip()][0]
                            chemID = dCas[CAS.rstrip()][1]
                        chemRoute = ""
                        if condName in dCAS :
                            if dCAS[condName] in dRoute :
                                chemRoute = dRoute[dCAS[condName]]
                            else :
                                chemRoute = "other"
    
                        Condition = {}
                        Condition['id'] = 'TST' + str(get_Index('condition'))
                        Condition['study'] = Study['id']
                       
                        Condition['treatment']=[]
                        if chemID != "" :
                             Condition['chemicaltag'] = get_tag('chemical.tab',chemID)
                        else : 
                            Condition['chemicaltag']=[chemName]
                      
                        Treatment = {}
                        Treatment['chemicals']= []
    
                        doses = dose.split('_')[0]
                        dose_unit = dose.split('_')[1]
                        exposure = temps.split('_')[0]
                        exposure_unit = temps.split('_')[1]
                        timeexpo = 0
                        # CHANGE TIME UNIT
                        if exposure_unit == 'd' :
                            exposure_unit = "days"
                            timeexpo = float(exposure) * 1440
                        if exposure_unit == 'hr' :
                            exposure_unit = "hours"
                            timeexpo = float(exposure) * 60
                        if exposure_unit == 'h' :
                            exposure_unit = "hours"
                            timeexpo = float(exposure) * 60
                        if exposure_unit == 'min' :
                            exposure_unit = "minutes"
                            timeexpo = float(exposure) * 1
    
                        Condition['title'] = "Open TG-GATEs  - Toxicogenomics signatures of "+tissue_name+" after exposure to "+project+" ("+doses+" "+dose_unit+", "+exposure+" "+exposure_unit+") in human"
    
                        #############################
                        Chemicals['time']=timeexpo
                        Chemicals['dose']=doses
                        Chemicals['dose_unit'] = dose_unit
                        Chemicals['exposure_duration'] = exposure
                        Chemicals['exposure_duration_unit'] = exposure_unit
                        Chemicals['exposure_frequency'] = ''
                        Chemicals['info'] = "For the in vitro studies, the highest concentration was defined as the dose level yielding an 80–90% relative survival ratio. However, for compounds that dissolved poorly in the vehicle, the highest concentration was defined by the maximum solubility of the compound. In principle, the ratio of the concentrations for the low, middle and high dose levels was 1:5:25."
                        Chemicals['name'] = chemName
                        Chemicals['route'] = chemRoute
                        
                        ###############################################################################
                        
                        ############################## Create signature ###############################
                        Signature = {}
                        Signature['time'] = Chemicals['time']
                        Signature['asso_cond'] = Condition['id']
                        Signature['chemical'] = []
                        Signature['chemical'].append(Chemicals['name'])
                        Signature['chemicaltag'] = Condition['chemicaltag']
                        Signature['devstage'] = 'Adulthood' 
                        Signature['diseasetag'] = []
                        Signature['generation'] = 'F0'
                        Signature['id'] = 'TSS' + str(get_Index('signature'))
                        print Dataset_ID,Study['id'],Condition['id'],Signature['id']
                        Signature['organism'] = 'Homo sapiens'
                        Signature['orgatag'] = Study['orgatag']
                        Signature['route'] = chemRoute
                        Signature['sex'] = 'male'
                        Signature['tissue'] = tissue_name
                        if Study['tissuetag'] == []:
                            Signature['tissuetag'] = get_tag('tissue.tab',tissue_ID)
                        else :
                            Signature['tissuetag'] = Study['tissuetag']
                        
                        Signature['celltag'] = Study['celltag']
                        Signature['title'] = Condition['title']
                        Signature['type'] = Study['interventional_experimental_type']
                        Signature['genomic'] =[]
                        Signature['physio'] = []
                        Signature['molecular'] = []
                        Signature['files'] =[]
                        Signature['supfile'] =[]
                        
                        Genomic={}
                        Genomic['statistical'] = 'Affymetrix GeneChip data were quality controlled and normalized using using the RMA package with the custom CDF (GPL1355) provided by the BRAINARRAY resource. Next, data analysis was carried out using the Annotation, Mapping, Expression and Network (AMEN) analysis suite of tools (Chalmel & Primig, 2008). Briefly, genes yielding a signal higher than the detection threshold (median of the normalized dataset) and a fold-change >1.5 between exposed and control samples were selected. A Linear Model for Microarray Data (LIMMA) statistical test (F-value adjusted with the False Discovery Rate method: p < 0.05) was employed to identify significantly differentially expressed genes.'
                        Genomic['techno'] = 'Microarray'
                        Signature['technotag'] = get_tag('experiment.tab','OBI:0400147')
                        Genomic['plateform'] = 'GPL1355'
                        Genomic['pvalue'] = '0.05'
                        Genomic['obs_effect'] = 'Entrez'
                        Genomic['control'] = dSample[condName][0]
                        Genomic['sample'] = dSample[condName][1]
                        Genomic['expe_info'] = ""
                        Genomic['up'] =""
                        Genomic['down'] =""
                        Genomic['files'] =[]
                        
                        
                        
                        logger.debug('InsertDM - Create signature files')
                        dirCond = public_path+Dataset_ID+"/"+Study['id']+"/"+Condition['id']+"/"+Signature['id']
                    
                        os.makedirs(dirCond)
                        if prezfile == 1:
                            Signature['files'].append('genomic_upward.txt')
                            lId = []
                            for idline in upFile.readlines():
                                IDs = idline.replace('\n','\t').replace(',','\t').replace(';','\t')
                                lId.append(IDs.split('\t')[0])
                                Genomic['up'] = Genomic['up'] + idline
                            lId = list(set(lId))
                            upFile.close()
                            dataset_in_db = list(db['genes'].find( {"GeneID": {'$in': lId}},{ "GeneID": 1,"Symbol": 1,"HID":1, "_id": 0 } ))
                            lresult = {}
                            for i in dataset_in_db:
                                lresult[i['GeneID']]=[i['Symbol'],i['HID']]
                            #Create 4 columns signature file
                            if os.path.isfile(os.path.join(dirCond,'genomic_upward.txt')):
                                os.remove(os.path.join(dirCond,'genomic_upward.txt'))
                
                            check_files = open(os.path.join(dirCond,'genomic_upward.txt'),'a')
                            for ids in lId :
                                if ids in lresult :
                                    check_files.write(ids+'\t'+lresult[ids][0]+'\t'+lresult[ids][1].replace('\n','')+'\t1\n')
                                else :
                                    check_files.write(ids+'\t'+'NA\tNA'+'\t0\n')                
                            check_files.close()
                            
                            
                            
                            Signature['files'].append('genomic_downward.txt')
                            lId = []
                            for idline in downFile.readlines():
                                IDs = idline.replace('\n','\t').replace(',','\t').replace(';','\t')
                                lId.append(IDs.split('\t')[0])
                                Genomic['down'] = Genomic['down'] + idline
                            downFile.close()
                            lId = list(set(lId))
                            dataset_in_db = list(db['genes'].find( {"GeneID": {'$in': lId}},{ "GeneID": 1,"Symbol": 1,"HID":1, "_id": 0 } ))
                            lresult = {}
                            for i in dataset_in_db:
                                lresult[i['GeneID']]=[i['Symbol'],i['HID']]
                            #Create 4 columns signature file
                            if os.path.isfile(os.path.join(dirCond,'genomic_downward.txt')):
                                os.remove(os.path.join(dirCond,'genomic_downward.txt'))
                
                            check_files = open(os.path.join(dirCond,'genomic_downward.txt'),'a')
                            for ids in lId :
                                if ids in lresult :
                                    check_files.write(ids+'\t'+lresult[ids][0]+'\t'+lresult[ids][1].replace('\n','')+'\t1\n')
                                else :
                                    check_files.write(ids+'\t'+'NA\tNA'+'\t0\n')                  
                            check_files.close() 
                   
                
                            
                            
                            
                        if os.path.isfile(os.path.join(dirCond,'genomic_interrogated_genes.txt')):
                            os.remove(os.path.join(dirCond,'genomic_interrogated_genes.txt'))
                        Signature['files'].append('genomic_interrogated_genes.txt')
                        cmd3 = 'cp %s %s' % (projectPath+'all_genes_converted.txt',dirCond+'/genomic_interrogated_genes.txt')
                        os.system(cmd3)
                        
                        
                        
                        upload_path = admin_path
                        all_name = Dataset_ID+'_'+Signature['id']+'.sign'
                        adm_path_signame = os.path.join(upload_path,'signatures_data',all_name)
                        #admin
                        if not os.path.exists(os.path.join(upload_path,'signatures_data')):
                            os.makedirs(os.path.join(upload_path,'signatures_data'))
                        if os.path.isfile(adm_path_signame):
                            os.remove(adm_path_signame)
                    
                        check_files = open(adm_path_signame,'a')
                        lfiles = {'genomic_upward.txt':'1','genomic_downward.txt':'-1','genomic_interrogated_genes.txt':'0'}
                        val_geno = 0
                        for filesUsr in os.listdir(dirCond) :
                            if filesUsr in lfiles:
                                fileAdmin = open(dirCond +'/'+filesUsr,'r')
                                print dirCond +'/'+filesUsr
                                for linesFile in fileAdmin.readlines():
                                    check_files.write(linesFile.replace('\n','')+'\t'+lfiles[filesUsr]+'\n')
                                fileAdmin.close()
                        check_files.close()
                        
    
                        ##################################### Add Condition ###########################
                        Signature['genomic'].append(Genomic)
                        Signature['gene_up'] = Genomic['up']
                        Signature['gene_down'] = Genomic['down']
                        Signature['signature_type'] = 'genomic'
                        Treatment['chemicals'].append(Chemicals) #add chemical to treatment
                        Condition['treatment'].append(Treatment) #add treatment to condition
                        Study['conditions'].append(Condition)    #add condition to study
                        Study['signatures'].append(Signature) #add signature info to study
                        nb_cond = nb_cond + 1
                        ###############################################################################
                    ########### END for cond ############################
                    ############## END for STUDIES ############################
                    print "Update DATASET : " +Dataset_ID
                    form = db['datasets'].find_one({'id': Dataset_ID})
                    del form['_id']
                    form['studies'].append(Study)
                    db['datasets'].update({'id': Dataset_ID}, form)
    
                    es = elasticsearch.Elasticsearch([config.get('app:main','elastic_host')])
                    eform = db['datasets'].find_one({'id': Dataset_ID})
                    del eform['_id']
                    
                    #print "INDEX DATASET : " +Dataset_ID
                    bulk_insert = ''
                    for study in eform['studies']:
                        for sig in study['signatures']:
                            bulk_insert += "{ \"index\" : { \"_index\" : \"toxsign\", \"_type\": \"signature\" , \"_id\" : \""+Dataset_ID+"_"+study['id']+'_'+sig['id']+"\" } }\n"
                            mysig = copy.deepcopy(eform)
                            mystudy = copy.deepcopy(study)
                            mystudy['signatures']  = [sig]
                            mysig['studies'] = [mystudy]
                            mysig['dataset'] = Dataset_ID
                            bulk_insert += json.dumps(mysig)+"\n"
                    if bulk_insert:
                        es.bulk(body=bulk_insert)
    print nb_dataset,nb_study,nb_cond
    
    
    
    
    
"""
Insert all other human data (extracted by Fred)   
"""
def otherHuman():
    #LOAD DICTIONNARIES
    """
        Insert signatures extrated from ChemPSY processing
        To insert informations please make sur that the following repository is correctlly filled :
            - all_genes_converted files
            - Conditions repository with all individuals conditions
            - Description.txt file
            - projectName.txt file 
            - Studies directory
        This function also required :
            - Individual sample file (Data/files/ChemPSySampleNumber.txt)
            - ChemPSy_MESH.tsv file (Data/files/ChemPSy_MESH.tsv)
    """
    
    # Create dico for all projects
    projectPath = human_path
    all = open(data_path+"/condInfo_Human_GSE.txt",'r')
    dicoGSE = {}
    for lines in all.readlines():
        cond = lines.split('\t')[0]
        GSE = cond.split('+')[0]
        if GSE not in dicoGSE :
            if GSE != "TGGATE":
                dicoGSE[GSE] = []
    condall = open(data_path+"/condInfo_Human_GSE.txt",'r')
    dicoInfoGSE = {}
    for linesInfo in condall.readlines():
        GSE = linesInfo.split('\t')[17]
        if GSE not in dicoInfoGSE :
            if GSE != "TGGATE":
                dicoInfoGSE[GSE] = linesInfo.split('\t')
                
    # for each project
    for projectName in dicoGSE :
        dChemical = dicoCAS()
        dDataset = {}
        dico_cond = NewcondDico()
        dRoute = NewdicoRoute(projectName)
        dCAS = dicoCAS()
        dSample=dicoSampleHuman()
        dName = {}
        nb_dataset = 0
        nb_study = 0
        nb_cond = 0
        orga = human_toxOrg(projectName)
        #DEFINITION DES CONDITIONS PAR CHEMICAL
        for files in os.listdir(projectPath+'Conditions'):
            name = files.replace('_down.txt','').replace('_up.txt','').replace('_noeffects.txt','')
            if projectName in name :
                if name not in dDataset :
                    dDataset[name] =[]

        for project in orga :
            print project

            Dataset_authors = dicoInfoGSE[projectName][20]
            Dataset_email = dicoInfoGSE[projectName][20]
            Dataset_conditions = []
            Dataset_confidence = ""
            Dataset_contributors=[]
            Dataset_pubmed = ['http://www.ncbi.nlm.nih.gov/pubmed/%s' % (dicoInfoGSE[projectName][16])]
            Dataset_extlink = ["http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=%s" % (dicoInfoGSE[projectName][17])]
            Dataset_description = ""
            Dataset_overall = ""
            Dataset_result = ""
            Dataset_owner = Dataset_email
            Dataset_status = "public"
            Dataset_studies = []
            Dataset_ID = 'TSP' + str(get_Index("project"))
            Dataset_title = "Toxicogenomics signatures after exposure to "+project+" in human"

            # DATASET CREATION
            dt = datetime.datetime.utcnow()
            dt = datetime.datetime.utcnow()
            ztime = mktime(dt.timetuple())
            db['datasets'].insert({'id': Dataset_ID,
                                    'title': Dataset_title,
                                    'email':Dataset_email,
                                    'authors': Dataset_authors,
                                    'conditions': Dataset_conditions,
                                    'confidence': Dataset_confidence,
                                    'contributors': Dataset_contributors,
                                    'pubmed':Dataset_pubmed,
                                    'description': Dataset_description,
                                    'ext_link':Dataset_extlink,
                                    'last_updated':ztime,
                                    'overalldesign':Dataset_overall,
                                    'owner':Dataset_owner,
                                    'result':Dataset_result,
                                    'status':Dataset_status,
                                    'studies':Dataset_studies,
                                    'submission_date':ztime,
            })
            nb_dataset = nb_dataset + 1


            organeList = ['HEPATOCYTES','HK-2','ISHIKAWA_CELLS','JURKAT_CELLS','MCF-7']
            for studorg in organeList  :
                if studorg in orga[project]:
                    print studorg

                    study = studorg
                    #print study


                    tissue_name = ''
                    tissue_ID = ''
                    study_description = ''
                    if study == 'LIVER' :
                        tissue_name = 'Liver'
                        tissue_ID = 'FMA:7197'
                        cell_ID = ""
                        study_description = "Complete dataset for human liver."

                    if study == 'HEPATOCYTES' :
                        cell_name = 'Hepatocytes'
                        tissue_name='Liver'
                        tissue_ID = 'FMA:7197'
                        cell_ID = ""
                        study_description = "Complete dataset for human hepatocytes."

                    if study == 'ISHIKAWA_CELLS' :
                        cell_name = 'Ishikawa cell'
                        tissue_name = 'Uterus'
                        tissue_ID = 'FMA:17558'
                        cell_ID = 'BTO:0003575'
                        study_description = "Complete dataset for human ishikawa cells."

                    if study == 'HK-2' :
                        cell_name = 'HK-2 cell'
                        tissue_name = 'Kidney'
                        tissue_ID = 'FMA:7203'
                        cell_ID = 'BTO:0003041'
                        study_description = "Complete dataset for human HK-2 cells."

                    if study == 'JURKAT_CELLS' :
                        cell_name = 'JURKAT cell'
                        tissue_name = 'T lymphocyte'
                        tissue_ID = 'FMA:62870'
                        cell_ID = 'BTO:0000661'
                        study_description = "Complete dataset for human JURKAT cells."

                    if study == 'MCF-7' :
                        cell_name = 'MCF-7 cell'
                        tissue_name = 'Breast'
                        tissue_ID = 'FMA:9601'
                        cell_ID = 'BTO:0000093'
                        study_description = "Complete dataset for human MCF-7 cells."


                    Study = {}
                    Study['conditions']=[]
                    Study['id']= 'TSE' + str(get_Index("study"))
                    Study['asso'] = Dataset_ID
                    Study['type'] = 'interventional'
                    Study['orgatag'] = get_tag('species.tab','NCBITaxon:9606')
                    Study['signatures'] = []
                    Study['interventional_title'] = "Toxicogenomics signatures of "+tissue_name+" "+cell_name+" after exposure to "+project+" in human"
                    Study['interventional_design'] = dicoInfoGSE[projectName][25]
                    Study['interventional_description'] = study_description
                    Study['interventional_results'] = ""
                    Study['interventional_experimental_type'] = 'in_vitro'
                    Study['tissuetag'] =  get_tag('tissue.tab',tissue_ID)
                    Study['celltag'] = []
                    if cell_ID != "":
                        Study['celltag'] = get_tag('cell_line.tab',cell_ID)
                    Study['interventional_vivo'] = {}
                    Study['interventional_vitro'] = {}
                    Study['interventional_exvivo'] = {}
                    Study['interventional_other'] = {}
                    Study['interventional_vitro']['organism'] = 'Homo sapiens'
                    Study['interventional_vitro']['tissue'] = tissue_name
                    Study['interventional_vitro']['experimental'] = 'cell_line'
                    Study['interventional_vitro']['cell_line'] = cell_name
                    Study['interventional_vitro']['generation'] = 'f0'
                    Study['interventional_vitro']['strain'] = ''
                    Study['interventional_vitro']['passage']='na'

                    nb_study = nb_study + 1

                    for cond in orga[project][studorg] :

                        Chemicals = {}
                        dose = cond.split('+')[0]
                        temps = cond.split('+')[1]
                        #CREATION INFORMATION CONDITION

                        #RECUPERATION NOM | CAS | ROUTE DU CHEMICAL
                        condName = orga[project][studorg][cond]
                        #print dico_cond[condName]
                        info = dico_cond[condName]

                        Study['interventional_vitro']['sex'] = info[14]

                        condName = orga[project][studorg][cond]
                        prezfile = 1
                        if condName in dDataset :
                            upFile = open(projectPath+'Conditions/'+condName+'_up.txt','r')
                            print upFile
                            downFile = open(projectPath+'Conditions/'+condName+'_down.txt','r')
                        else :
                            prezfile = 0

                        CAS = getFileCasHuman(condName)
                        dCas = getCAS()
                        if CAS.rstrip() not in dCas :
                            chemName = files.split('+')[2]+' CAS:NA'
                            chemID = ""
                        else :
                            chemName = dCas[CAS.rstrip()][0]
                            chemID = dCas[CAS.rstrip()][1]
                        chemRoute = ""
                        if condName in dCAS :
                            if dCAS[condName] in dRoute :
                                chemRoute = dRoute[dCAS[condName]]
                            else :
                                chemRoute = "other"

                        Condition = {}
                        Condition['id'] = 'TST' + str(get_Index("condition"))
                        Condition['study'] = Study['id']

                        Condition['treatment']=[]
                        if chemID != "" :
                             Condition['chemicaltag'] = get_tag('chemical.tab',chemID)
                        else :
                            Condition['chemicaltag']=[chemName]

                        Treatment = {}
                        Treatment['chemicals']= []

                        if dose =="NA" or dose=='High' or dose=="Low":
                            doses = 0
                            dose_unit = "NA"
                        else :
                            dose_unit = dose[-2:]
                            doses = dose.replace(dose_unit,"")

                        exposure = int(temps.split('_')[0])
                        exposure_unit = temps.split('_')[1]
                        # CHANGE TIME UNIT
                        if exposure_unit == 'd' :
                            exposure_unit = "days"
                            times = exposure * 1440
                        if exposure_unit == 'hr' :
                            exposure_unit = "hours"
                            times = exposure * 60
                        if exposure_unit == 'h' :
                            exposure_unit = "hours"
                            times = exposure * 60
                        if exposure_unit == 'min' :
                            exposure_unit = "minutes"
                            times = exposure * 1

                        Condition['title'] = "Toxicogenomics signatures of "+tissue_name+" "+cell_name+" after exposure to "+project+" ("+str(doses)+" "+str(dose_unit)+", "+str(exposure)+" "+str(exposure_unit)+") in human"

                        #############################
                        Chemicals['time']=times
                        Chemicals['dose']=doses
                        Chemicals['dose_unit'] = dose_unit
                        Chemicals['exposure_duration'] = exposure
                        Chemicals['exposure_duration_unit'] = exposure_unit
                        Chemicals['exposure_frequency'] = ''
                        Chemicals['info'] = dicoInfoGSE[projectName][25]
                        Chemicals['name'] = chemName
                        Chemicals['route'] = chemRoute

                        ###############################################################################

                        ############################## Create signature ###############################
                        Signature = {}
                        Signature['asso_cond'] = Condition['id']
                        Signature['chemical'] = []
                        Signature['chemical'].append(Chemicals['name'])
                        Signature['chemicaltag'] = Condition['chemicaltag']
                        Signature['devstage'] = 'na'
                        Signature['diseasetag'] = []
                        Signature['generation'] = 'f0'
                        Signature['id'] = 'TSS' + str(get_Index("signature"))
                        print Dataset_ID,Study['id'],Condition['id'],Signature['id']
                        Signature['organism'] = 'Homo sapiens'
                        Signature['orgatag'] = Study['orgatag']
                        Signature['route'] = chemRoute
                        Signature['sex'] = 'male'
                        Signature['time']=Chemicals['time']
                        Signature['tissue'] = tissue_name
                        if Study['tissuetag'] == []:
                            Signature['tissuetag'] = get_tag('tissue.tab',tissue_ID)
                        else :
                            Signature['tissuetag'] = Study['tissuetag']

                        Signature['celltag'] = Study['celltag']
                        Signature['title'] = Condition['title']
                        Signature['type'] = Study['interventional_experimental_type']
                        Signature['genomic'] =[]
                        Signature['physio'] = []
                        Signature['molecular'] = []
                        Signature['files'] =[]
                        Signature['supfile'] =[]

                        Genomic={}
                        Genomic['statistical'] = 'Affymetrix GeneChip data were quality controlled and normalized using using the RMA package with the custom CDF (GPL1355) provided by the BRAINARRAY resource. Next, data analysis was carried out using the Annotation, Mapping, Expression and Network (AMEN) analysis suite of tools (Chalmel & Primig, 2008). Briefly, genes yielding a signal higher than the detection threshold (median of the normalized dataset) and a fold-change >1.5 between exposed and control samples were selected. A Linear Model for Microarray Data (LIMMA) statistical test (F-value adjusted with the False Discovery Rate method: p < 0.05) was employed to identify significantly differentially expressed genes.'
                        Genomic['techno'] = 'Microarray'
                        Signature['technotag'] = get_tag('experiment.tab','OBI:0400147')
                        Genomic['plateform'] = 'GPL570'
                        Genomic['pvalue'] = '0.05'
                        Genomic['obs_effect'] = 'Entrez'
                        Genomic['control'] = dSample[condName][0]
                        Genomic['sample'] = dSample[condName][1]
                        Genomic['expe_info'] = ""
                        Genomic['up'] =""
                        Genomic['down'] =""
                        Genomic['files'] =[]
                        



                        logger.debug('InsertDM - Create signature files')
                        dirCond = public_path+Dataset_ID+"/"+Study['id']+"/"+Condition['id']+"/"+Signature['id']
                    
                        os.makedirs(dirCond)
                        if prezfile == 1:
                            Signature['files'].append('genomic_upward.txt')
                            lId = []
                            for idline in upFile.readlines():
                                IDs = idline.replace('\n','\t').replace(',','\t').replace(';','\t')
                                lId.append(IDs.split('\t')[0])
                                Genomic['up'] = Genomic['up'] + idline
                            lId = list(set(lId))
                            upFile.close()
                            dataset_in_db = list(db['genes'].find( {"GeneID": {'$in': lId}},{ "GeneID": 1,"Symbol": 1,"HID":1, "_id": 0 } ))
                            lresult = {}
                            for i in dataset_in_db:
                                lresult[i['GeneID']]=[i['Symbol'],i['HID']]
                            #Create 4 columns signature file
                            if os.path.isfile(os.path.join(dirCond,'genomic_upward.txt')):
                                os.remove(os.path.join(dirCond,'genomic_upward.txt'))
                
                            check_files = open(os.path.join(dirCond,'genomic_upward.txt'),'a')
                            for ids in lId :
                                if ids in lresult :
                                    check_files.write(ids+'\t'+lresult[ids][0]+'\t'+lresult[ids][1].replace('\n','')+'\t1\n')
                                else :
                                    check_files.write(ids+'\t'+'NA\tNA'+'\t0\n')                
                            check_files.close()
                            
                            
                            
                            Signature['files'].append('genomic_downward.txt')
                            lId = []
                            for idline in downFile.readlines():
                                IDs = idline.replace('\n','\t').replace(',','\t').replace(';','\t')
                                lId.append(IDs.split('\t')[0])
                                Genomic['down'] = Genomic['down'] + idline
                            downFile.close()
                            lId = list(set(lId))
                            dataset_in_db = list(db['genes'].find( {"GeneID": {'$in': lId}},{ "GeneID": 1,"Symbol": 1,"HID":1, "_id": 0 } ))
                            lresult = {}
                            for i in dataset_in_db:
                                lresult[i['GeneID']]=[i['Symbol'],i['HID']]
                            #Create 4 columns signature file
                            if os.path.isfile(os.path.join(dirCond,'genomic_downward.txt')):
                                os.remove(os.path.join(dirCond,'genomic_downward.txt'))
                
                            check_files = open(os.path.join(dirCond,'genomic_downward.txt'),'a')
                            for ids in lId :
                                if ids in lresult :
                                    check_files.write(ids+'\t'+lresult[ids][0]+'\t'+lresult[ids][1].replace('\n','')+'\t1\n')
                                else :
                                    check_files.write(ids+'\t'+'NA\tNA'+'\t0\n')                  
                            check_files.close() 
                   
                
                            
                            
                            
                        if os.path.isfile(os.path.join(dirCond,'genomic_interrogated_genes.txt')):
                            os.remove(os.path.join(dirCond,'genomic_interrogated_genes.txt'))
                        Signature['files'].append('genomic_interrogated_genes.txt')
                        cmd3 = 'cp %s %s' % (projectPath+'all_genes_converted.txt',dirCond+'/genomic_interrogated_genes.txt')
                        os.system(cmd3)
                        
                        
                        
                        upload_path = admin_path
                        all_name = Dataset_ID+'_'+Signature['id']+'.sign'
                        adm_path_signame = os.path.join(upload_path,'signatures_data',all_name)
                        #admin
                        if not os.path.exists(os.path.join(upload_path,'signatures_data')):
                            os.makedirs(os.path.join(upload_path,'signatures_data'))
                        if os.path.isfile(adm_path_signame):
                            os.remove(adm_path_signame)
                    
                        check_files = open(adm_path_signame,'a')
                        lfiles = {'genomic_upward.txt':'1','genomic_downward.txt':'-1','genomic_interrogated_genes.txt':'0'}
                        val_geno = 0
                        for filesUsr in os.listdir(dirCond) :
                            if filesUsr in lfiles:
                                fileAdmin = open(dirCond +'/'+filesUsr,'r')
                                print dirCond +'/'+filesUsr
                                for linesFile in fileAdmin.readlines():
                                    check_files.write(linesFile.replace('\n','')+'\t'+lfiles[filesUsr]+'\n')
                                fileAdmin.close()
                        check_files.close()





                        

                        ##################################### Add Condition ###########################
                        Signature['genomic'].append(Genomic)
                        Signature['gene_up'] = Genomic['up']
                        Signature['gene_down'] = Genomic['down']
                        Signature['signature_type'] = 'genomic'
                        Treatment['chemicals'].append(Chemicals) #add chemical to treatment
                        Condition['treatment'].append(Treatment) #add treatment to condition
                        Study['conditions'].append(Condition)    #add condition to study
                        Study['signatures'].append(Signature) #add signature info to study
                        nb_cond = nb_cond + 1
                        ###############################################################################
                    ########### END for cond ############################
                    ############## END for STUDIES ############################
                    print "Update DATASET : " +Dataset_ID
                    form = db['datasets'].find_one({'id': Dataset_ID})
                    del form['_id']
                    form['studies'].append(Study)
                    db['datasets'].update({'id': Dataset_ID}, form)

                    es = elasticsearch.Elasticsearch([config.get('app:main','elastic_host')])
                    eform = db['datasets'].find_one({'id': Dataset_ID})
                    del eform['_id']

                    #print "INDEX DATASET : " +Dataset_ID
                    bulk_insert = ''
                    for study in eform['studies']:
                        for sig in study['signatures']:
                            bulk_insert += "{ \"index\" : { \"_index\" : \"toxsign\", \"_type\": \"signature\" , \"_id\" : \""+Dataset_ID+"_"+study['id']+'_'+sig['id']+"\" } }\n"
                            mysig = copy.deepcopy(eform)
                            mystudy = copy.deepcopy(study)
                            mystudy['signatures']  = [sig]
                            mysig['studies'] = [mystudy]
                            mysig['dataset'] = Dataset_ID
                            bulk_insert += json.dumps(mysig)+"\n"
                    if bulk_insert:
                        es.bulk(body=bulk_insert)
        print nb_dataset,nb_study,nb_cond    
