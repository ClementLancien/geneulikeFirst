#-*- coding: utf-8 -*-
# -----------------------------------------------------------
#
#  Project : 
#  GenOuest / IRSET
#  35000 Rennes
#  France
#
# -----------------------------------------------------------
"""
Created on Sat Jun 18 10:39:10 2016
Author: tdarde <thomas.darde@inria.fr>
Last Update : 
"""


########################################################################
#                                                                      #
#    Complete script description here                                  #
#    Don't forget to change the main function arguments                #
#                                                                      #
########################################################################

########################################################################
#                                Import                                #
########################################################################
import argparse
import os,shutil
########################################################################
#                                Functions                             #
# Use this format :                                                    #
#def CreateVersusFile(1,2,3):                                          #
#    """                                                               #
#    Main fonction                                                     #
#    For each projects list all conditions and CAS, create directory   #
#    for condition.                                                    #
#    Create CAS file and treatment.info files                          #
#                                                                      #
#    :param 1: project's path                                          #
#    :param 2: tissue where the studie is performed                    #
#    :param 3: file with a celfile to remove per ligne                 #
#    :type 1: string                                                   #
#    :type 2: string                                                   #
#    :type 3: string                                                   #
#    :return: Condition status                                         #
#    :rtype: string                                                    #
#                                                                      #
#                                                                      #
#    .. todo:: fix error with multi txt files and CAS files            #
#    """                                                               #
#                                                                      #
########################################################################




########################################################################
#                                Main                                  #
########################################################################

import argparse
import sys
from hashlib import sha1
from random import randint
import bcrypt
import ConfigParser, os
from hashlib import sha1
from pymongo import MongoClient
from datetime import date, time
import xlsxwriter

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

#if not args.email:
#    print 'email parameter is missing'
#    sys.exit(1)

#print config.get('app:main','db_uri')
mongo = MongoClient(config.get('app:main','db_uri'))
db = mongo[config.get('app:main','db_name')]
workbook = xlsxwriter.Workbook('data_validate.xlsx', {'strings_to_urls': False})
worksheet = workbook.add_worksheet()


#path="/opt/toxsign/Data/Ontology/"
path="/Users/tdarde/Desktop/Ontology/"
pos = 1
for files in os.listdir(path):
    if files == 'tissue.tab':
        print "INSERT: "+files
        fileIn = open(path+files,'r')
        for lines in fileIn.readlines():
            lines = lines.decode('utf-8').strip()
            ids = lines.split('\t')[0]
            dbs = files
            if dbs == "go.obo.tab" :
                dbs = lines.split('\t')[1]
            name = lines.split('\t')[2]
            cel = 'A'+str(pos)
            worksheet.write(cel, name)
            pos = pos + 1
            #direct_parent = lines.split('\t')[4].split("|")
            #all_parent = lines.split('\t')[5].split("|")
            #all_parent_name = lines.split('\t')[6].split("|")
            #print dbs,ids
            #db[dbs].insert({'id': ids,
            #             'name': name,
            #             'synonyms': synonyms,
            #             'direct_parent': direct_parent,
            #             'all_parent': all_parent,
            #             'all_name': all_parent_name,
            #             })
    
workbook.close()
            
# db['project'].insert({'id': 1,
#                      'val': 0,
#                      })
# db['study'].insert({'id': 1,
#                      'val': 0,
#                      })
# db['condition'].insert({'id': 1,
#                      'val': 0,
#                      })
# db['signature'].insert({'id': 1,
#                      'val': 0,
#                      })
# 
# #Create geneInfo db from geneInfo file
# geneFile = open('gene_info_parse','r')
# for geneLine in geneFile.readlines():
#     if geneLine[0] != '#':
#         tax_id = geneLine.split('\t')[0]
#         GeneID = geneLine.split('\t')[1]
#         Symbol = geneLine.split('\t')[2] 
#         Synonyms = geneLine.split('\t')[4] 
#         description = geneLine.split('\t')[8]
#         db['geneInfo'].insert({'GeneID': GeneID,
#                           'tax_id' : tax_id,
#                           'Symbol': Symbol,
#                           'Synonyms': Synonyms,
#                           'description': description,
#                           })
# geneFile.close()
#          
# #Insert homologene ID from homologene.data.txt file
# homologeneFile = open('homologene.data.txt','r')
# for homoline in homologeneFile.readlines():
#     HID = homoline.split('\t')[0]
#     Taxonomy_ID = homoline.split('\t')[1]
#     Gene_ID = homoline.split('\t')[2]
#     Gene_Symbol = homoline.split('\t')[3]
#     Protein_gi = homoline.split('\t')[4]
#     Protein_accession = homoline.split('\t')[5]
#     db['homoloGene'].insert({'HID': HID,
#                            'Taxonomy_ID' : Taxonomy_ID,
#                            'Gene_ID': Gene_ID,
#                            'Gene_Symbol': Gene_Symbol,
#                            'Protein_gi': Protein_gi,
#                            'Protein_accession': Protein_accession,
#                            })

#Insert Allbank ID from TOXsIgN_geneDB file
# geneFile = open('../../Data/Database/TOXsIgN_geneDB','r')
# for geneLine in geneFile.readlines():
#     if geneLine[0] != '#':
#         tax_id = geneLine.split('\t')[0]
#         GeneID = geneLine.split('\t')[1]
#         Symbol = geneLine.split('\t')[2] 
#         Synonyms = geneLine.split('\t')[4] 
#         description = geneLine.split('\t')[8]
#         HID = geneLine.split('\t')[-1]
#         db['genes'].insert({'GeneID': GeneID,
#                          'tax_id' : tax_id,
#                          'Symbol': Symbol,
#                          'Synonyms': Synonyms,
#                          'description': description,
#                          'HID':HID,
#                          })
# geneFile.close()