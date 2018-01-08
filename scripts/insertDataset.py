#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
#
#  Project : TOXsIgN
#  GenOuest / IRSET
#  35000 Rennes
#  France
#
# -----------------------------------------------------------
#  Created on 1 jul. 2016
#  Author: tdarde <thomas.darde@inria.fr>
#  Last Update : 20 jul. 2016
########################################################################
#                                                                      #
#  Insert ChemPsy data in Toxsign (Rat and Human) and index information#
#  Require :                                                           #
#   ChemPSy_MESH.tsv (Rat and Human)                                   #
#   Ontology files (Chebi and chemical.tab                             #
#   condInfo.txt (each condition information)                          #
#   sampleInfo (for each condition nb cond and control)                #
#                                                                      #
#                                                                      #
########################################################################

########################################################################
#                                Import                                #
########################################################################
import argparse
import sys
import datetime
import time
from hashlib import sha1
from random import randint
import bcrypt
import ConfigParser, os
from hashlib import sha1
from pymongo import MongoClient
import elasticsearch
import copy
import json



########################################################################
#                                Arg parse                             #
########################################################################
parser = argparse.ArgumentParser(description='Initialize database content.')
parser.add_argument('--config')
#parser.add_argument('--pwd')
#parser.add_argument('--email')
args = parser.parse_args()

if not args.config:
    print "config argument is missing"
    sys.exit(2)

config = ConfigParser.ConfigParser()
config.readfp(open(args.config))

########################################################################
#                                DB connection                         #
########################################################################

mongo = MongoClient(config.get('app:main','db_uri'))
db = mongo[config.get('app:main','db_name')]

########################################################################
#                                Functions                             #
########################################################################


def get_Index(dbinsert):
    if dbinsert == "project":
        db['project'].update({'id': 1}, {'$inc': {'val': 1}})
        repos = db['project'].find({'id': 1})
        for i in repos :
            return i['val']
    if dbinsert =="study":
        db['study'].update({'id': 1}, {'$inc': {'val': 1}})
        repos = db['study'].find({'id': 1})
        for i in repos :
            return i['val']
    if dbinsert =="condition":
        db['condition'].update({'id': 1}, {'$inc': {'val': 1}})
        repos = db['condition'].find({'id': 1})
        for i in repos :
            return i['val']
    if dbinsert =="signature":
        db['signature'].update({'id': 1}, {'$inc': {'val': 1}})
        repos = db['signature'].find({'id': 1})
        for i in repos :
            return i['val']

def condDico():
    fileCond = open('condInfo.txt','r')
    dico_cond={}
    for lines in fileCond.readlines():
        val = lines.split('\t')
        cond_name = val[0]
        if cond_name not in dico_cond :
            dico_cond[cond_name] = val
    return dico_cond

def NewcondDico():
    fileCond = open('condInfo_Human_GSE.txt','r')
    dico_cond={}
    for lines in fileCond.readlines():
        val = lines.split('\t')
        cond_name = val[0]
        if cond_name not in dico_cond :
            dico_cond[cond_name] = val
    return dico_cond


def get_tag(index,val) :
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

def dicoChemical():
    #chebiTab = open('/opt/toxsign/Data/Ontology/chebi.obo.tab','r')
    chebiTab = open('chebi.obo.tab','r')
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

def getFileCas(fileCond):
    casTab = open('ChemPSy_MESH.tsv','r')
    dChemical = {}
    for lines in casTab.readlines():
        val = lines.split('\t')
        fileName = val[0]
        CAS = val[4].split('|')[0]
        dChemical[fileName] = CAS
    return dChemical[fileCond]

def getFileCasHuman(fileCond):
    casTab = open('ChemPSy_MESH_human.tsv','r')
    dChemical = {}
    for lines in casTab.readlines():
        val = lines.split('\t')
        fileName = val[0]
        CAS = val[4].split('|')[0]
        dChemical[fileName] = CAS
    return dChemical[fileCond]

def getCAS():
    #chebiTab = open('/opt/toxsign/Data/Ontology/chemical.tab','r')
    chebiTab = open('chemical.tab','r')
    dCAS = {}
    for lines in chebiTab.readlines():
        val = lines.split('\t')
        ID = val[0]
        name = val[2]
        CAS = name.split('CAS:')[1]
        dCAS[CAS] = [name,ID]
    return dCAS

def dicoRoute(project):
    dRoute ={}
    routeFile = open(project+'.txt','r')   
    for lines in routeFile.readlines():
        val = lines.split('\t')
        chem = val[5].lower()
        route = val[9]
        dRoute[chem] = route
    
    return dRoute

def NewdicoRoute(project):
    dRoute ={}
    routeFile = open(project+'.txt','r')
    lines = routeFile.readlines()
    for i in range(1,len(lines)):
        val = lines[i].split('\t')
        chem = val[8].lower()
        route = val[13]
        dRoute[chem] = route

    return dRoute
    
def dicoCAS():
    casTab = open('ChemPSy_MESH.tsv','r')
    dChemical = {}
    for lines in casTab.readlines():
        val = lines.split('\t')
        fileName = val[0]
        name = val[1]
        dChemical[fileName] = name
    return dChemical

def dicoSample():
    files = open('ChemPSySampleNumber.txt','r')
    dSample = {}
    for lines in files.readlines():
        val = lines.split('\t')
        name = val[0]
        nb_sample = val[1]
        nb_control = val[2]
        dSample[name] = [nb_sample,nb_control]
    return dSample

def dicoSampleHuman():
    files = open('ChemPSySampleNumberHuman.txt','r')
    dSample = {}
    for lines in files.readlines():
        val = lines.split('\t')
        name = val[0]
        nb_sample = val[1]
        nb_control = val[2]
        dSample[name] = [nb_sample,nb_control]
    return dSample


def toxOrg(pro):
    toxF = open('ChemPSy_MESH.tsv','r')
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

def human_toxOrg(pro):
    toxF = open('ChemPSy_MESH_human.tsv','r')
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


########################################################################
#                                Main Functions                        #
########################################################################

def insert(projectPath,projectName):
    #LOAD DICTIONNARIES
    dChemical = dicoCAS()
    dDataset = {}
    dRoute = dicoRoute(projectName)
    dCAS = dicoCAS()
    dSample=dicoSample()
    dName = {}
    nb_dataset = 0
    nb_study = 0
    nb_cond = 0
    orga = toxOrg('GSE578')



    #DEFINITION DES CONDITIONS PAR CHEMICAL
    for files in os.listdir(projectPath+'Conditions'):
        name = files.replace('_down.txt','').replace('_up.txt','').replace('_noeffects.txt','')
        if 'GSE578' in name :
            if name not in dDataset :
                dDataset[name] =[]

    for project in orga :
        print project

        Dataset_authors = 'Scott S. Auerbach'
        Dataset_email = 'auerbachs@niehs.nih.gov'
        Dataset_conditions = []
        Dataset_confidence = ""
        Dataset_contributors=['TOXsIgN Team']
        Dataset_pubmed = ['http://www.ncbi.nlm.nih.gov/pubmed/16005536','http://www.ncbi.nlm.nih.gov/pubmed/25058030']
        Dataset_extlink = "http://www.niehs.nih.gov/research/atniehs/labs/bmsb/toxico/index.cfm|https://ntp.niehs.nih.gov/drugmatrix/index.html|http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE57800|http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE57805|http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE57811|http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE57815|http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE57816".split('|')
        Dataset_description = "DrugMatrix is the scientific communities' largest molecular toxicology reference database and informatics system. DrugMatrix is populated with the comprehensive results of thousands of highly controlled and standardized toxicological experiments in which rats or primary rat hepatocytes were systematically treated with therapeutic, industrial, and environmental chemicals at both non-toxic and toxic doses."
        Dataset_overall = ""
        Dataset_result = ""
        Dataset_owner = "dardethomas@gmail.com"
        Dataset_status = "public"
        Dataset_studies = []
        Dataset_ID = 'TSP' + str(get_Index("project"))
        Dataset_title = projectName+" - Toxicogenomics signatures after exposure to "+project+" in the rat"

        # DATASET CREATION
        dt = datetime.datetime.utcnow()
            
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
                                'last_updated':time.mktime(dt.timetuple()),
                                'overalldesign':Dataset_overall,
                                'owner':Dataset_owner,
                                'result':Dataset_result,
                                'status':Dataset_status,
                                'studies':Dataset_studies,
                                'submission_date':time.mktime(dt.timetuple()),
        })
        nb_dataset = nb_dataset + 1

        organeList = ['LIVER','KIDNEY','HEART','THIGH-MUSCLE']
        for studorg in organeList  :
            #print study
            if studorg in orga[project]:
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
                Study['id']= 'TSE' + str(get_Index("study"))
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
                    Condition['id'] = 'TST' + str(get_Index("condition"))
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
                    Signature['chemical'].append(Chemicals)
                    Signature['chemicaltag'] = Condition['chemicaltag']
                    Signature['devstage'] = 'Adulthood' 
                    Signature['diseasetag'] = []
                    Signature['time']=Chemicals['time']
                    Signature['generation'] = 'F0'
                    Signature['id'] = 'TSS' + str(get_Index("signature"))
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

                    dirCond = '/opt/toxsign/Data/Public/'+Dataset_ID+"/"+Study['id']+"/"+Condition['id']+"/"+Signature['id']+"/"
                    
                    os.makedirs(dirCond)
                    if prezfile == 1:
                        Genomic['files'] =[condName+'_up.txt',condName+'_down.txt','interrogated_genes.txt']
                        for idline in upFile.readlines():
                           Genomic['up'] = Genomic['up'] + idline
                        upFile.close()
                        
                        
                        for idline in downFile.readlines():
                           Genomic['down'] = Genomic['down'] + idline
                        downFile.close()                        
                        
                        cmd1 = 'cp %s %s' % (projectPath+'Conditions/'+condName.replace('(','\(').replace(')','\)')+'_up.txt',dirCond)
                        cmd2 = 'cp %s %s' % (projectPath+'Conditions/'+condName.replace('(','\(').replace(')','\)')+'_down.txt',dirCond)
                        cmd3 = 'cp %s %s' % (projectPath+'all_genes.txt',dirCond+'interrogated_genes.txt')
                        os.system(cmd1)
                        os.system(cmd2)
                        os.system(cmd3)
                    ##################################### Add Condition ###########################
                    Signature['genomic'].append(Genomic)
                    Treatment['chemicals'].append(Chemicals) #add chemical to treatment
                    Condition['treatment'].append(Treatment) #add treatment to condition
                    Study['conditions'].append(Condition)    #add condition to study
                    Study['signatures'].append(Signature) #add signature info to study
                    nb_cond = nb_cond + 1
                    ###############################################################################

                    #################################### CREATE DB HTTP ##########################
                ########### END for cond ############################
            ############## END for STUDIES ############################

                #print "Update DATASET : " +Dataset_ID
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


def insertTG(projectPath,projectName):
    #LOAD DICTIONNARIES
    dChemical = dicoCAS()
    dico_cond = condDico()
    dDataset = {}
    dRoute = dicoRoute(projectName)
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
        Dataset_owner = "dardethomas@gmail.com"
        Dataset_status = "public"
        Dataset_studies = []
        Dataset_ID = 'TSP' + str(get_Index("project"))
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
                                'last_updated':time.mktime(dt.timetuple()),
                                'overalldesign':Dataset_overall,
                                'owner':Dataset_owner,
                                'result':Dataset_result,
                                'status':Dataset_status,
                                'studies':Dataset_studies,
                                'submission_date':time.mktime(dt.timetuple()),
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
                    study_description = "Complete Open TG-GATEs dataset for rat liver."
                if study == 'KIDNEY' :
                    tissue_name = 'Kidney'
                    tissue_ID = 'FMA:7203'
                    study_description = "Complete Open TG-GATEs dataset for rat kidney."
                if study == 'HEART' :
                    tissue_name = 'Heart'
                    tissue_ID = 'FMA:7088'
                    study_description = "Complete Open TG-GATEs dataset for rat heart."
                if study == 'THIGH-MUSCLE' :
                    tissue_name = 'Skeletal muscle tissue'
                    tissue_ID = 'FMA:14069'
                    study_description = "Complete Open TG-GATEs dataset for rat thigh muscle."

                Study = {}
                Study['conditions']=[]
                Study['id']= 'TSE' + str(get_Index("study"))
                Study['asso'] = Dataset_ID
                Study['type'] = 'interventional'
                Study['orgatag'] = get_tag('species.tab','NCBITaxon:10116')
                Study['signatures'] = []
                Study['interventional_title'] = "Open TG-GATEs - Toxicogenomics signatures of "+tissue_name+" after exposure to "+project+" in the rat"
                Study['interventional_design'] = "Animal experiments were conducted by four different contract research organizations. The studies used male Crl:CD Sprague-Dawley (SD) rats purchased from Charles River Japan, Inc. (Hino or Atsugi, Japan) as 5-week-old animals. After a 7-day quarantine and acclimatization period, the animals were allocated into groups of 20 animals each using a computerized stratified random grouping method based on body weight. Each animal was allowed free access to water and pelleted food (radiation-sterilized CRF-1; Oriental Yeast Co., Tokyo, Japan). For single-dose experiments, groups of 20 animals were administered a compound and then fivw animals/time point were sacrificed at 3, 6, 9 or 24 h after administration. For repeated-dose experiments, groups of 20 animals received a single dose per day of a compound and five animals/time point were sacrificed at 4, 8, 15 or 29 days (i.e. 24 h after the respective final administration at 3, 7, 14 or 28 days). Animals were not fasted before being sacrificed. To avoid effects of diurnal cycling, the animals were sacrificed and necropsies were performed between 9:00 a.m. and 11:00 a.m. for the repeated-dose studies. Blood samples for routine biochemical analyses were collected into heparinized tubes under ether anesthesia from the abdominal aorta at the time of sacrifice."
                Study['interventional_description'] = study_description
                Study['interventional_results'] = ""
                Study['interventional_experimental_type'] = ''
                Study['tissuetag'] = []
                Study['celltag'] =[]
                Study['interventional_vivo'] = {}
                Study['interventional_vitro'] = {}
                Study['interventional_exvivo'] = {}
                Study['interventional_other'] = {}


                nb_study = nb_study + 1

                for cond in orga[project][studorg] :

                    Chemicals = {}
                    dose = cond.split('+')[0]
                    temps = cond.split('+')[1]
                    #CREATION INFORMATION CONDITION

                    #RECUPERATION NOM | CAS | ROUTE DU CHEMICAL
                    condName = orga[project][studorg][cond]
                    info = dico_cond[condName].split('\t')
                    if info[12] == "in vitro":
                        Study['interventional_experimental_type'] = 'in_vitro'
                        Study['interventional_vitro']['organism'] = 'Rattus norvegicus'
                        Study['interventional_vitro']['tissue'] = tissue_name
                        Study['interventional_vitro']['experimental'] = 'primary_cell_culture'
                        if tissue_name == 'Liver':
                            Study['interventional_vitro']['cell_name'] = 'Hepatocytes'
                        if tissue_name == 'Kidney':
                            Study['interventional_vitro']['cell_name'] = 'Nephron'
                        Study['interventional_vitro']['generation'] = 'F0'
                        Study['interventional_vitro']['strain'] = 'Sprague–Dawley'
                        Study['interventional_vitro']['sex'] = info[14]
                        Study['interventional_vitro']['devstage'] = 'Adulthood'

                    if info[12] == "in vivo":
                        Study['interventional_vivo']['organism'] = 'Rattus norvegicus'
                        Study['interventional_vivo']['strain'] = 'Sprague–Dawley'
                        Study['interventional_vivo']['sex'] = info[14]
                        Study['interventional_vivo']['devstage'] = 'Adulthood'


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
                    Condition['id'] = 'TST' + str(get_Index("condition"))
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

                    Condition['title'] = "Open TG-GATEs  - Toxicogenomics signatures of "+tissue_name+" after exposure to "+project+" ("+doses+" "+dose_unit+", "+exposure+" "+exposure_unit+") in the rat"

                    #############################
                    Chemicals['time']=times
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
                    Signature['asso_cond'] = Condition['id']
                    Signature['chemical'] = []
                    Signature['chemical'].append(Chemicals)
                    Signature['chemicaltag'] = Condition['chemicaltag']
                    Signature['devstage'] = 'Adulthood' 
                    Signature['diseasetag'] = []
                    Signature['generation'] = 'F0'
                    Signature['id'] = 'TSS' + str(get_Index("signature"))
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
                    Signature['time']=Chemicals['time']
                    
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
                    dirCond = '/opt/toxsign/Data/Public/'+Dataset_ID+"/"+Study['id']+"/"+Condition['id']+"/"+Signature['id']+"/"
                    
                    os.makedirs(dirCond)
                    if prezfile == 1:
                        Genomic['files'] =[condName+'_up.txt',condName+'_down.txt','interrogated_genes.txt']
                        for idline in upFile.readlines():
                           Genomic['up'] = Genomic['up'] + idline
                        upFile.close()
                        
                        
                        for idline in downFile.readlines():
                           Genomic['down'] = Genomic['down'] + idline
                        downFile.close()                        
                        
                        cmd1 = 'cp %s %s' % (projectPath+'Conditions/'+condName.replace('(','\(').replace(')','\)')+'_up.txt',dirCond)
                        cmd2 = 'cp %s %s' % (projectPath+'Conditions/'+condName.replace('(','\(').replace(')','\)')+'_down.txt',dirCond)
                        cmd3 = 'cp %s %s' % (projectPath+'all_genes.txt',dirCond+'interrogated_genes.txt')
                        os.system(cmd1)
                        os.system(cmd2)
                        os.system(cmd3)

                    ##################################### Add Condition ###########################
                    Signature['genomic'].append(Genomic)
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


def insertHumanTG(projectPath,projectName):
    #LOAD DICTIONNARIES
    dChemical = dicoCAS()
    dDataset = {}
    dico_cond = condDico()
    dRoute = dicoRoute(projectName)
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
        Dataset_owner = "dardethomas@gmail.com"
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
                                'last_updated':time.mktime(dt.timetuple()),
                                'overalldesign':Dataset_overall,
                                'owner':Dataset_owner,
                                'result':Dataset_result,
                                'status':Dataset_status,
                                'studies':Dataset_studies,
                                'submission_date':time.mktime(dt.timetuple()),
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
                    study_description = "Complete Open TG-GATEs dataset for human liver."
                if study == 'KIDNEY' :
                    tissue_name = 'Kidney'
                    tissue_ID = 'FMA:7203'
                    study_description = "Complete Open TG-GATEs dataset for human kidney."
                if study == 'HEART' :
                    tissue_name = 'Heart'
                    tissue_ID = 'FMA:7088'
                    study_description = "Complete Open TG-GATEs dataset for human heart."
                if study == 'THIGH-MUSCLE' :
                    tissue_name = 'Skeletal muscle tissue'
                    tissue_ID = 'FMA:14069'
                    study_description = "Complete Open TG-GATEs dataset for human thigh muscle."

                Study = {}
                Study['conditions']=[]
                Study['id']= 'TSE' + str(get_Index("study"))
                Study['asso'] = Dataset_ID
                Study['type'] = 'interventional'
                Study['orgatag'] = get_tag('species.tab','NCBITaxon:9606')
                Study['signatures'] = []
                Study['interventional_title'] = "Open TG-GATEs - Toxicogenomics signatures of "+tissue_name+" after exposure to "+project+" in human"
                Study['interventional_design'] = "Human cryopreserved hepatocytes were purchased from Tissue Transformation Technologies, Inc. (Edison, NJ, USA) and CellzDirect, Inc. (Pittsboro, NC, USA). Six lots of human hepatocytes were used during the course of the project."
                Study['interventional_description'] = study_description
                Study['interventional_results'] = ""
                Study['interventional_experimental_type'] = 'in_vitro'
                Study['tissuetag'] =  get_tag('tissue.tab','FMA:7197')
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

                    doses = dose.split('_')[0]
                    dose_unit = dose.split('_')[1]
                    exposure = temps.split('_')[0]
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

                    Condition['title'] = "Open TG-GATEs  - Toxicogenomics signatures of "+tissue_name+" after exposure to "+project+" ("+doses+" "+dose_unit+", "+exposure+" "+exposure_unit+") in human"

                    #############################
                    Chemicals['time']=times
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
                    Signature['asso_cond'] = Condition['id']
                    Signature['chemical'] = []
                    Signature['chemical'].append(Chemicals)
                    Signature['chemicaltag'] = Condition['chemicaltag']
                    Signature['devstage'] = 'Adulthood'
                    Signature['diseasetag'] = []
                    Signature['generation'] = 'f0'
                    Signature['id'] = 'TSS' + str(get_Index("signature"))
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
                    Signature['time']=Chemicals['time']

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
                    dirCond = '/opt/toxsign/Data/Public/'+Dataset_ID+"/"+Study['id']+"/"+Condition['id']+"/"+Signature['id']+"/"

                    os.makedirs(dirCond)
                    if prezfile == 1:
                        Genomic['files'] =[condName+'_up.txt',condName+'_down.txt','interrogated_genes.txt']
                        for idline in upFile.readlines():
                           Genomic['up'] = Genomic['up'] + idline
                        upFile.close()


                        for idline in downFile.readlines():
                           Genomic['down'] = Genomic['down'] + idline
                        downFile.close()

                        cmd1 = 'cp %s %s' % (projectPath+'Conditions/'+condName.replace('(','\(').replace(')','\)')+'_up.txt',dirCond)
                        cmd2 = 'cp %s %s' % (projectPath+'Conditions/'+condName.replace('(','\(').replace(')','\)')+'_down.txt',dirCond)
                        cmd3 = 'cp %s %s' % (projectPath+'all_genes.txt',dirCond+'interrogated_genes.txt')
                        os.system(cmd1)
                        os.system(cmd2)
                        os.system(cmd3)

                    ##################################### Add Condition ###########################
                    Signature['genomic'].append(Genomic)
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



def otherHuman(projectPath,allFile):
    #LOAD DICTIONNARIES
    all = open(allFile,'r')
    dicoGSE = {}
    for lines in all.readlines():
        cond = lines.split('/')[-2]
        GSE = cond.split('+')[0]
        if GSE not in dicoGSE :
            if GSE != "TGGATE":
                dicoGSE[GSE] = []
    condall = open('condInfo_Human_GSE.txt','r')
    dicoInfoGSE = {}
    for linesInfo in condall.readlines():
        GSE = linesInfo.split('\t')[17]
        if GSE not in dicoInfoGSE :
            if GSE != "TGGATE":
                dicoInfoGSE[GSE] = linesInfo.split('\t')
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
            Dataset_owner = "dardethomas@gmail.com"
            Dataset_status = "public"
            Dataset_studies = []
            Dataset_ID = 'TSP' + str(get_Index("project"))
            Dataset_title = "Toxicogenomics signatures after exposure to "+project+" in human"

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
                                    'last_updated':time.mktime(dt.timetuple()),
                                    'overalldesign':Dataset_overall,
                                    'owner':Dataset_owner,
                                    'result':Dataset_result,
                                    'status':Dataset_status,
                                    'studies':Dataset_studies,
                                    'submission_date':time.mktime(dt.timetuple()),
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
                        Signature['chemical'].append(Chemicals)
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
                        #dirCond = '/opt/toxsign/Data/Public/'+Dataset_ID+"/"+Study['id']+"/"+Condition['id']+"/"+Signature['id']+"/"
                        #
                        # os.makedirs(dirCond)
                        if prezfile == 1:
                            for idline in upFile.readlines():
                                Genomic['up'] = Genomic['up'] + idline
                            upFile.close()
                        #
                        #
                            for idline in downFile.readlines():
                                Genomic['down'] = Genomic['down'] + idline
                            downFile.close()
                        #
                        #     cmd1 = 'cp %s %s' % (projectPath+'Conditions/'+condName.replace('(','\(').replace(')','\)')+'_up.txt',dirCond)
                        #     cmd2 = 'cp %s %s' % (projectPath+'Conditions/'+condName.replace('(','\(').replace(')','\)')+'_down.txt',dirCond)
                        #     cmd3 = 'cp %s %s' % (projectPath+'all_genes.txt',dirCond+'interrogated_genes.txt')
                        #     os.system(cmd1)
                        #     os.system(cmd2)
                        #     os.system(cmd3)

                        ##################################### Add Condition ###########################
                        Signature['genomic'].append(Genomic)
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

########################################################################
#                                Main                                  #
########################################################################

#insert('/opt/toxsign/Data/ChemPsy_data/DrugMatrix/','DrugMatrix')
#insertTG('/opt/toxsign/Data/ChemPsy_data/TGGATE/','TGGATE')
#insertHumanTG('/Users/tdarde/Documents/CloudStation/Projets/ChemPSy/ToxSyn/ChemPsy_data/Human_TGGATE/','TGGATE_human')
otherHuman('/Users/tdarde/Documents/CloudStation/Projets/ChemPSy/ToxSyn/ChemPsy_data/Human_TGGATE/','/Users/tdarde/Documents/CloudStation/Projets/ChemPSy/DATA/ALL.txt')