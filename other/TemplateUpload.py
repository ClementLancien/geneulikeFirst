# -*- coding: utf-8 -*-
"""
Created on Wed May 24 09:20:52 2017

@author: clancien
"""

from xlrd import open_workbook, XLRDError
class TemplateUpload:
    """Classe définissant notre fichier template"""
    
    def __init__(self, name_file, path_file, type_file):
        """Constructeur :on abesoin de connaitre le nom et chemin d'accès du fichier 
        ainsi que du type de fichier (csv ou xls)"""
    
        self.file_name = name_file
        self.upload_path = path_file
        self.type_file = type_file
        self.critical = 0
        self.projects_identifiers=[]
        self.studies_identifiers=[]
        self.strategies_identifiers = []
        self.lists_identifiers = []
        self.idLists_identifiers = []
        self.projects_errors = { 'Critical':[], 'Warning':[], 'Info':[] }
        self.studies_errors = { 'Critical':[], 'Warning':[], 'Info':[] }
        self.strategies_errors = { 'Critical':[], 'Warning':[], 'Info':[] }
        self.lists_errors = { 'Critical':[], 'Warning':[], 'Info':[] }
        self.idLists_error = { 'Critical':[], 'Warning':[], 'Info':[] }
        
        
    def is_Excel(self):
        try:
            open_workbook(self.file_name)
        except XLRDError:
            return False
        else:
            return True
    
    def is_Sheet_Number(self):
        return (open_workbook(str(self.name_file)) == [u'projects', u'Studies', u'Strategies', u'Lists', u'idLists', u'Help'])
    
    def is_project_identifier(self, row_value_identifier):
        return row_value_identifier == ""
    
    def is_project_title(self, row_value_title):
        return row_value_title == ""
        
    def is_project_description(self, row_value_description):
        return row_value_description == ""        
        
    def is_project_pubmed(self, row_value_pubmed):
        return row_value_pubmed == ""
    
    def is_project_contributor(self, row_value_contributor):
        return row_value_contributor == ""
    
    def is_project_error(self, identifier, title, description, pubmed, contributor, row_number):
        """Si il existe des erreurs, c'est erreurs sont consignés dans l'attribut projects_errors"""
        if(identifier):
            self.projects_errors['Critical'].append("Line " + str(row_number) + " in your Projects Sheet has no ProjectID")
            self.critical += 1
        if(title):
            self.projects_errors['Critical'].append("Line " + str(row_number) + " in your Projects Sheet has no Title")
            self.critical += 1
        if(description):
            self.projects_errors['Warning'].append("Line " + str(row_number) + " in your Projects Sheet has no Description")
        if(pubmed):
            self.projects_errors['Warning'].append("Line " + str(row_number) + " in your Projects Sheet has no PubMed DOI")
        if(contributor):
            self.projects_errors['Info'].append("Line " + str(row_number) + " in your Projects Sheet has no Contributor(s)")
        
    def is_project_row(self, row_value, row_number):
        
        self.is_project_error(self.is_project_identifier(row_value[0]) , self.is_project_title(row_value[1]),\
                            self.is_project_description(row_value[2]), self.is_project_pubmed(row_value[3]),\
                            self.is_project_contributor(row_value[4]), row_number)
                            
        if (not self.is_project_identifier(row_value[0]) ):
            self.projects_identifiers.append(str(row_value[0]))
               
    def projects_sheet(self, wb):
        
        #wb = open_workbook(os.path.join(self.upload_path, self.file_name),encoding_override="cp1251")
        projects = wb.sheet_by_index(0)
        for row_number in range(5, projects.nrows):
            self.is_project_row(self, projects.row_values(row_number) , row_number)
    
    
    def is_study_identifier(self, row_value_identifier):
        return row_value_identifier == ""
    
    def is_study_associated_project_identifier(self, row_value_associated_project_identifier):
        return row_value_associated_project_identifier not in self.projects_identifiers 
    
    def is_study_title(self, row_value_title):
        return row_value_title == ""
    
    def is_study_description(self, row_value_description):
        return row_value_description == ""
    
    def is_study_phenotype_desease(self, row_value_phenotype_desease):
        return row_value_phenotype_desease == ""

    def is_study_go_terms(self, row_value_go_terms):
        return row_value_go_terms == ""
    
    def is_study_organism(self, row_value_organism):
        return row_value_organism == ""
    
    def is_study_development_stage(self, row_value_development_stage):
        return row_value_development_stage == ""
    
    def is_study_error(self, identifier, associated_project_identifier, title, description, \
                        phenotype_desease, go_terms, organism, development_stage, row_number):
                            
        if(identifier):
            self.studies_errors['Critical'].append("Line " + str(row_number) + " in your Studies Sheet has no StudyID")
            self.critical += 1
        if(associated_project_identifier):
            self.studies_errors['Critical'].append("Line " + str(row_number) + " in your Studies Sheet has no Associated ProjectID")
            self.critical += 1
        if(title):
            self.studies_errors['Critical'].append("Line " + str(row_number) + " in your Studies Sheet has no Title")
            self.critical += 1
        if(description):
            self.studies_errors['Warning'].append("Line " + str(row_number) + " in your Studies Sheet has no Description")
        if(phenotype_desease):
            self.studies_errors['Info'].append("Line " + str(row_number) + " in your Studies Sheet has no Phenotype/Desease")
        if(go_terms):
            self.studies_errors['Info'].append("Line " + str(row_number) + " in your Studies Sheet has no Go terms"))
        if(organism):
            self.studies_errors['Info'].append("Line " + str(row_number) + " in your Studies Sheet has no Organism")
        if(development_stage):
            self.studies_errors['Info'].append("Line " + str(row_number) + " in your Studies Sheet has no Development Stage")
            
    def is_study_row(self, row_value, row_number):
            
        self.is_study_error(self.is_study_identifier(row_value[0]),\
                            self.is_study_associated_project_identifier(row_value[1]),\
                            self.is_study_title(row_value[2]),\
                            self.is_study_description(row_value[3]),\
                            self.is_study_phenotype_desease(row_value[4]),\
                            self.is_study_go_terms(row_value[5]),\
                            self.is_study_organism(row_value[6]),\
                            self.is_study_development_stage(row_value[7]), row_number)
                            
        if(not self.is_study_identifier(row_value[0])):
            self.studies_identifiers(str(row_value(0)))
    
    def studies_sheet(self, wb):
        #wb = open_workbook(os.path.join(self.upload_path, self.file_name),encoding_override="cp1251")
        studies = wb.sheet_by_index(1)
        for row_number in range(5, studies.nrows):
            self.is_study_row(studies.row_values(row_number) , row_number)
    
    def is_strategy_identifier(self , row_value_identifier):
        return row_value_identifier == ""
    
    def is_strategy_associated_study_identifier(self, row_value_associated_study_identifier):
        return row_value_associated_study_identifier not in self.studies_identifiers
    
    def is_strategy_title(self, row_value_title):
        return row_value_title == ""
    
    def is_strategy_description(self, row_value_description):
        return row_value_description == ""
    
    def is_strategy_type_of_experiment(self, row_value_type_of_experiment):
        return row_value_type_of_experiment == ""
    
    def is_strategy_technology(self, row_value_technology):
        return row_value_technology == ""
    
    def is_strategy_process(self, row_value_process):
        return row_value_process == ""
    
    
    def is_strategy_error(self, identifier, associated_study_identifier, title, description,\
                            type_of_experiment, technology, process, row_number):
        if(identifier):
            self.strategy_erro['Critical'].append("Line " + str(row_number) + " in your Strategies Sheet has no StrategyID")
            self.critical += 1
        if(associated_study_identifier):
            self.strategies_errors['Critical'].append("Line " + str(row_number) + " in your Strategies Sheet has no Associated StudyID")
            self.critical += 1
        if(title):
            self.strategies_errors['Critical'].append("Line " + str(row_number) + " in your Strategies Sheet has no Title")
            self.critical += 1
        if(description):
            self.strategies_errors['Warning'].append("Line " + str(row_number) + " in your Strategies Sheet has no Description")
        if(type_of_experiment):
            self.strategies_errors['Warning'].append("Line " + str(row_number) + " in your Strategies Sheet has no Type of Experiment")
        if(technology):
            self.strategies_errors['Warning'].append("Line " + str(row_number) + " in your Strategies Sheet has no Technology")
        if(process):
            self.strategies_errors['Warning'].append("Line " + str(row_number) + " in your Strategies Sheet has no Process")
    
    def is_strategy_row(self, row_value, row_number):
        
        self._strategy_error(self.is_strategy_identifier(row_value[0]),\
                                self.is_strategy_associated_study_identifier(row_value[1]),\
                                self.is_strategy_title(row_value[2]),\
                                self.is_strategy_description(row_value[3]),\
                                self.is_strategy_type_of_experiment(row_value[4]),\
                                self.is_strategy_technology(row_value[5]),\
                                self.is_strategy_process(row_value[6]),\
                                row_number)
                                
        if(not self.is_strategy_identifier(row_value[0])):
            self.strategies_identifiers.append(str(row_value[0]))
    
    def strategies_sheet(self, wb):
        strategies = wb.sheet_by_index(2)
        for row_number in range(5, strategies.nrows):
            self.is_strategy_row(strategies.row_values(row_number), row_number)
            
    
    def is_list_identifier(self, row_value_identifier):
        return row_value_identifier == ""
    
    def is_list_associated_strategy_identifier(self, row_value_associated_strategy_identifier):
        return row_value_associated_strategy_identifier not in self.strategies_identifiers
    
    def is_list_title(self, row_value_title):
        return row_value_title == ""
    
    def is_list_description(self, row_value_description):
        return row_value_description == ""
    
    def is_list_type_of_identifier(self, row_value_type_of_identifier):
        return row_value_type_of_identifier == ""
    
    def is_list_extended_type_of_identifier(self, row_value_extended_type_of_identifier, row_value_type_of_identifier):
        return (row_value_extended_type_of_identifier == "" and row_value_type_of_identifier[:3] == "GPL")
    
    def is_list_parent_list_identifier(self, row_value_parent_list_identifier):
        return row_value_parent_list_identifier == ""
    
    def is_list_child_list_identifier(self, row_value_child_list_identifier):
        return row_value_child_list_identifier == ""
    
    def is_list_error(self, identifier, associated_study_identifier, title, description,\
                        type_of_identifier,extended_type_of_identifier,\
                        parent_list_identifier, child_list_identifier, row_number):
        if(identifier):
            self.lists_errors['Critical'].append("Line " + str(row_number) + " in your Lists Sheet has no ListID")
            self.critical += 1
        if(associated_study_identifier):
            self.lists_errors['Critical'].append("Line " + str(row_number) + " in your Lists Sheet has no Associated StrategyID")
            self.critical += 1
        if(title):
            self.lists_errors['Critical'].append("Line " + str(row_number) + " in your Lists Sheet has no Title")
            self.critical += 1
        if(description):
            self.lists_errors['Warning'].append("Line " + str(row_number) + " in your Lists Sheet has no Description")
        if(type_of_identifier):
            self.lists_errors['Critical'].append("Line " + str(row_number) + " in your Lists Sheet has no Type of identifier")
            self.critical += 1
        if(extended_type_of_identifier):
            self.lists_errors['Critical'].append("Line " + str(row_number) + "in your Lists Sheet has no Extended Type of Identifier. ",\
            + "This field is required since you have selected a GPL identifier in the previoyus column")
            self.critical += 1
        if(parent_list_identifier):
            self.lists_errors['Info'].append("Line " + str(row_number) + " in your Lists Sheet has no ListParentID")
        if(child_list_identifier):
            self.lists_errors['Info'].append("Line " + str(row_number) + " in your Lists Sheet has no ListChildID")
    
    def is_list_row(self, row_value, row_number):
        
        self.is_list_error(self.is_list_identifier(row_value[0]),\
                            self.is_list_associated_strategy_identifier(row_value[1]),\
                            self.is_list_title(row_value[2]),\
                            self.is_list_description(row_value[3]),\
                            self.is_list_description(row_value[4]),\
                            self.is_list_extended_type_of_identifier(row_value[5], row_value[4]),\
                            self.is_list_parent_list_identifier(row_value[6]),\
                            self.is_list_child_list_identifier(row_value[7]))
        
        if(not self.is_list_identifier(row_value[0]) and row_value[8] == "Yes"):
            self.lists_identifiers.append(str(row_value(0)))
    
    
    def lists_sheet(self, wb):
        lists = wb.sheet_by_index(3)
        for row_number in range(5, lists.nrows):
            self.is_strategy_row(lists.row_values(row_number) , row_number)
    
    def is_idList_identifier(self, col_value_identifier):
        return col_value_identifier not in self.lists_identifiers
    
    def is_idList_list(self, col_value_list):
        return col_value_list.__len__() == 0
        
    def is_idList_error(self, identifier, idlist, col_number):
        if(identifier):
            self.idLists_error['Critical'].append("Column " + str(col_number) = " in your idLists Sheet has no known Identifier")
            self.critical += 1
        if(idList):
            self.idLists_error['Critical'].append("Column " + str(col_number) + " in your idLists Sheet has no List associated with")
    
    def is_idList_row(self, col_value, col_number):
        
        self.is_idList_error(self.is_idList_identifier(col_value[0]),\
                             self.is_idList_list(col_value[1:]), 
                             col_number)
        if(not self.is_idList_identifier(self,col_value[0])):
            self.idLists_identifiers.append(col_value[0])
    
    def get_absent_identifier_in_idLists(self):
        absent_identifier_in_idList_sheet = []
        for identifier in self.idLists_identifiers:
            if identifier not in self.lists_identifiers:
                absent_identifier_in_idList_sheet.append(identifier)
                
        return absent_identifier_in_idList_sheet
        
    def get_absent_identifier_in_Lists(self): 
        absent_identifier_in_lists_sheet = []
        for identifier in self.lists_identifiers:
            if identifier not in self.idLists_identifiers:
                absent_identifier_in_lists_sheet.append(identifier)
                
        return absent_identifier_in_lists_sheet
    
    def is_absent_identifier_in_idLists(self, absent_identifier_in_idList_sheet):
        return absent_identifier_in_idList_sheet.__len__() != 0
    
    def is_absent_identifier_in_lists(self,  absent_identifier_in_lists_sheet):
        return absent_identifier_in_lists_sheet.__len__() != 0
    
    def is_absent_error(self, bool_absent_identifier_in_idList_sheet,  absent_identifier_in_idList_sheet, bool_absent_identifier_in_lists_sheet, absent_identifier_in_lists_sheet):
        if(bool_absent_identifier_in_idList_sheet):
            for identifier in absent_identifier_in_idList_sheet:
                self.idLists_error['Critical'].append("List : " + str(identifier) + " is present in your idList Sheet but is absent in your Lists Sheet ")
                self.critical += 1
        if(bool_absent_identifier_in_lists_sheet):
            for identifier in absent_identifier_in_lists_sheet:
                self.idLists_error['Critical'].append("List : " + str(identifier) + "is present in your Lists Sheet but is absent in your idList Sheet" )

    def idLists_sheet(self, wb):
        lists = wb.sheet_by_index(3)
        for col_number in range(5, lists.ncols):
            self.is_strategy_row(self, lists.col_values(col_number) , col_number)
            
        absent_list = get_absent_identifier_in_Lists(self)
        absent_idList = get_absent_identifier_in_idLists(self)
        
        self.is_absent_error(is_absent_identifier_in_idLists(absent_idList), absent_idList, is_absent_identifier_in_lists(absent_list), absent_list)

    def all_sheets_browse(self):
        wb = open_workbook(os.path.join(self.upload_path, self.file_name),encoding_override="cp1251")
        if self.is_Excel():
            if self.is_Sheet_Number():
                self.projects_sheet(wb)
                self.studies_sheet(wb)
                self.strategies_sheet(wb)
                self.lists_sheet(wb)
                self.idLists_sheet(wb)
                return {'msg': "File checked and uploded !",
                        'error_project': self.projects_errors, 
                        'error_study':  self.studies_errors, 
                        'error_assay': self.strategies_errors, 
                        'error_factor': self.lists_errors, 
                        'error_signature': self.idLists_error, 
                        'critical': str(self.critical),
                        'file': os.path.join(self.upload_path, self.file_name),
                        'status':'0' 
                }
            else:
                {'error' : 'This workbook has not at least one on the following sheet : Projects, Studies, Strategies, Lists, idLists, Help' }

        else:
            return {'error': 'This file format is not .xls'}