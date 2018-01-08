from xlrd import open_workbook, XLRDError
import os
import time
import datetime

class templateSave:

	def __ini__(self, name_file, path_file):

		self.name_file = name_file
		self.path_file = path_file
		self.last_update = time.mktime(datetime.datetime.utcnow().timetuple())

	project_number=0

	def insert_project(self, wb, user):
		projects = wb.sheet_by_index(2)
        for row_number in range(5, strategies.nrows):
            row_value  = strategies.row_values(row_number)
            project = {
            	'id' : "GPR" + str(project_number),
           		'title' : row_value[1],
            	'description' : row_value[2],
            	'pubmed' : row_value[3],
            	'contributor' : row_values[4].replace("\n", ' ').replace("\t", ' '),
            	'crosslinks' : row_value[5],
            	'last_update' : self.last_update,
            	'submission_date' : self.last_update,
            	'author' : str(user),
            	'studies' : "",
            	'strategies' : "",
            	'lists' : "",
            	'additional_info' : ""
            	'tags' : "",
            	'status' : 'private'
            }
            

Id. unique
Titre
Description
Identifiant PubMed
Contributeurs
Informations additionnelles
Tag


 'id' : p_project['id'],
                'title' : project_title,
                'description' : project_description,
                'pubmed' : project_pubmed,
                'contributor' : project_contributors,
                'cross_link' : project_crosslink,
                'assays' : "",
                'studies' : "",
                'factors' : "",
                'signatures' :"",
                'last_update' : str(sdt),
                'submission_date' : str(sdt),
                'status' : 'private' ,
                'owner' : user,
                'author' : user ,
                'tags' : "",
                'edges' : "",
                'info' : ','.join(project_error['Info']),
                'warnings' : ','.join(project_error['Warning']),
                'critical' : ','.join(project_error['Critical']),
                'excel_id' : project_id