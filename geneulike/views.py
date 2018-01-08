# -*- coding: utf-8 -*-

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden, HTTPUnauthorized
from pyramid.security import remember, forget
from pyramid.renderers import render_to_response
from pyramid.response import Response, FileResponse

import unicodedata
import re
import time # delete pour el deploiement seulement pour tester el temps de conversion
import os
import json
from bson import json_util
from bson.objectid import ObjectId
from bson.errors import InvalidId
import jwt
import datetime
import time
import urllib2
import bcrypt
import uuid
import shutil
import zipfile
import tempfile
import copy
import re
import xlrd
from collections import OrderedDict
import simplejson as json
import subprocess
from csv import DictWriter
import string
import logging
import xlsxwriter 
import itertools
import smtplib
import email.utils
import sys
if sys.version < '3':
    from email.MIMEText import MIMEText
else:
    from email.mime.text import MIMEText
from logging.handlers import RotatingFileHandler
 

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.DEBUG)
 
# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
file_handler = RotatingFileHandler('view.log', 'a', 1000000000, 1)
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

@view_config(route_name='home')
def my_view(request):
    return HTTPFound(request.static_url('geneulike:webapp/app/'))


def send_mail(request, email_to, subject, message):
    if not request.registry.settings['mail.smtp.host']:
        logging.error('email smpt host not set')
        return
    port = 25
    if request.registry.settings['mail.smtp.port']:
        port = int(request.registry.settings['mail.smtp.port'])
    mfrom = request.registry.settings['mail.from']
    mto = email_to
    msg = MIMEText(message)
    msg['To'] = email.utils.formataddr(('Recipient', mto))
    msg['From'] = email.utils.formataddr(('Author', mfrom))
    msg['Subject'] = subject
    server = None
    try:
        server = smtplib.SMTP(request.registry.settings['mail.smtp.host'], request.registry.settings['mail.smtp.port'])
        #server.set_debuglevel(1)
        if request.registry.settings['mail.tls'] and request.registry.settings['mail.tls'] == 'true':
            server.starttls()
        if request.registry.settings['mail.user'] and request.registry.settings['mail.user'] != '':
            server.login(request.registry.settings['mail.user'], request.registry.settings['mail.password'])
        server.sendmail(mfrom, [mto], msg.as_string())
    except Exception as e:
            logging.error('Could not send email: '+str(e))
    finally:
        if server is not None:
            server.quit()


def is_authenticated(request):
    # Try to get Authorization bearer with jwt encoded user information
    if request.authorization is not None:
        try:
            (auth_type, bearer) = request.authorization
            secret = request.registry.settings['secret_passphrase']
            # If decode ok and not expired
            user = jwt.decode(bearer, secret, audience='urn:geneulike/api')
            user_id = user['user']['id']
            user_in_db = request.registry.db_mongo['users'].find_one({'id': user_id})
        except Exception as e:
            return None
        return user_in_db
    return None


@view_config(route_name='user_info', renderer='json', request_method='GET')
def user_info(request):
    user = is_authenticated(request)
    if user is None:
        return HTTPUnauthorized('Not authorized to access this resource')
    if not (user['id'] == request.matchdict['id'] or user['id'] in request.registry.admin_list):
        return HTTPUnauthorized('Not authorized to access this resource')
    user_in_db = request.registry.db_mongo['users'].find_one({'id': request.matchdict['id']})
    #user_in_db=
    return user_in_db

@view_config(route_name='getLastSeen', renderer='json', request_method='POST')
def getLastSeen(request):
    
    return {'connected' : 'hello'}

    form = json.loads(request.body, encoding=request.charset)
    
    time=timeBefore
    year=int(time[0:4])
    month=int(time[5:7])
    day=int(time[8:10])
    hour=int(time[11:13])
    minute=int(time[14:16])
    second=int(time[17:19])

    dateNow=datetime.datetime.now()
    
    if(year < int(dateNow.year) and int(dateNow.year) - year == 1):
        return {"connected" :'1 year ago'}
    elif(year < int(dateNow.year) and int(dateNow.year) - year != 1):
        return {"connected" : str(int(dateNow.year) - year) + " years ago"}
    elif(month < int(dateNow.month) and int(dateNow.month) - month == 1):
        return {"connected" : "1 month ago"}
    elif (month < int(dateNow.month) and int(dateNow.month) - month != 1):
        return {"connected" : str(int(dateNow.month) - month) + " months ago"}
    elif(day < int(dateNow.day) and int(dateNow.day) - day == 1):
        return {"connected" : "1 day ago"}
    elif(day < int(dateNow.day) and int(dateNow.day) - day != 1):
        return {"connected" :str(int(dateNow.day) - day) + " days ago"}
    elif(hour < int(dateNow.hour) and int(dateNow.hour) - hour == 1):
        return {"connected" : "1 hour ago"}
    elif(hour < int(dateNow.hour) and int(dateNow.hour) - hour != 1):
        return {"connected" : str(int(dateNow.hour)- hour) + " hours ago"}
    elif(minute < int(dateNow.minute) and int(dateNow.minute) - minute == 1):
        return {"connected" : "1 minute ago"}
    elif(minute < int(dateNow.minute) and int(dateNow.minute) - minute != 1):
        return {"connected" :str(int(dateNow.minute) - minute) + " minutes ago"}
    elif(second < int(dateNow.second) and int(dateNow.second) - second == 1):
        return {"connected" : "1 second ago"}
    else:
        return {"connected" : str(int(dateNow.second) - second) + " seconds ago"}



@view_config(route_name='user_info', renderer='json', request_method='POST')
def user_info_update(request):
    user = is_authenticated(request)
    if user['id'] == request.matchdict['id'] or user['id'] in request.registry.admin_list:
        form = json.loads(request.body, encoding=request.charset)
        tid = form['_id']
        del form['_id']
        request.registry.db_mongo['users'].update({'id': request.matchdict['id']}, form)
        form['_id'] = tid;
        return form
    else : 
        return HTTPUnauthorized('Not authorized to access this resource')

@view_config(route_name='user', renderer='json')
def user(request):
    user = is_authenticated(request)
    if user is None or user['id'] not in request.registry.admin_list:
        return HTTPUnauthorized('Not authorized to access this resource')
    users_in_db = request.registry.db_mongo['users'].find()
    users = []
    for user_in_db in users_in_db:
        users.append(user_in_db)
    return users

@view_config(route_name='user_register', renderer='json', request_method='POST')
def user_register(request):
    form = json.loads(request.body, encoding=request.charset)
    if not form['user_name'] or not form['user_password']:
        return {'msg' : 'emtpy fields, user name and password are mandatory', 'status':'danger'}
    user_in_db = request.registry.db_mongo['users'].find_one({'id': form['user_name']})
    if user_in_db is None :
        if 'address' not in form :
            form['address'] = 'No address'
        secret = request.registry.settings['secret_passphrase']
        token = jwt.encode({'user': {'id': form['user_name'],
                                     'password': bcrypt.hashpw(form['user_password'].encode('utf-8'), bcrypt.gensalt()),
                                     'first_name': form['first_name'],
                                     'last_name': form['last_name'],
                                     'laboratory': form['laboratory'],
                                     'country': form['country']
                                     },
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=36000),
                        'aud': 'urn:geneulike/api'}, secret)
        message = "You requested an account, please click on following link to validate it\n"
        message += request.host_url+'/app/index.html#/login?action=confirm_email&token='+token
        send_mail(request, form['user_name'], '[GeneULike] Please validate your account', message)
        return {'msg' : 'You will receive a confirmation mail. Please click on the link to validate your account.', 'status' : 'success'}
    else :
        return {'msg' : 'This email is already taken.', 'status':'warning'}

@view_config(route_name='user_confirm_email', renderer='json', request_method='POST')
def confirm_email(request):
    form = json.loads(request.body, encoding=request.charset)
    if form and 'token' in form:

        secret = request.registry.settings['secret_passphrase']
        user_id = None
        user_password = None
        try:
            auth = jwt.decode(form['token'], secret, audience='urn:geneulike/api')
            user_id = auth['user']['id']
            user_password = auth['user']['password']
        except Exception:
            return HTTPForbidden()
        status = 'approved'
        msg = 'Email validated, you can now access to your account.'
        if user_id in request.registry.admin_list:
            status = 'approved'
            msg = 'Email validated, you can now log into the application'
        user_in_db = request.registry.db_mongo['users'].find_one({'id' : user_id})
        if user_in_db == None:
            try:
                request.registry.db_mongo['users'].insert({'id': user_id,
                                                            'status': status,
                                                            'password': user_password,
                                                            'first_name': auth['user']['first_name'],
                                                            'last_name': auth['user']['last_name'],
                                                            'laboratory': auth['user']['laboratory'],
                                                            'avatar': "",
                                                            'selectedID':"",
                                                            'project':0,
                                                            'study':0,
                                                            'strategy':0,
                                                            'list':0,
                                                            'joined': str(datetime.datetime.now()),
                                                            'connected':""
                                                            })
            except:
                return{'msg' : 'Failed', 'status': 'danger'}
            upload_path = os.path.join(request.registry.upload_path, user_id, 'dashboard')
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            return {'msg': msg, 'status':'success'}
        else:
            return {'msg' :'You have already validate your account', 'status' : 'warning'}
    else:
        return {'msg' :'Contact the administrator', 'status' : 'danger'}

@view_config(route_name='user_validate', renderer='json')
def user_validate(request):
    session_user = is_authenticated(request)
    form = json.loads(request.body, encoding=request.charset)
    if session_user['id'] not in request.registry.admin_list:
        return HTTPForbidden()
    user_id = form['id']
    #print user_id
    request.registry.db_mongo['users'].update({'id': user_id},{'$set': {'status': 'approved'}})
    return {'msg': 'user '+user_id+'validated'}

@view_config(route_name='user_delete', renderer='json')
def user_delete(request):
    session_user = is_authenticated(request)
    form = json.loads(request.body, encoding=request.charset)
    if session_user['id'] not in request.registry.admin_list:
        return HTTPForbidden()
    user_id = form['id']
    if user_id in request.registry.admin_list:
        return {'msg': 'This user is an administrator. Please delete his administrator privileges before'}
    request.registry.db_mongo['users'].remove({'id': user_id})
    request.registry.db_mongo['datasets'].remove({'owner': user_id})
    request.registry.db_mongo['messages'].remove({'owner': user_id})
    return {'msg': 'user '+user_id+'validated'}


@view_config(route_name='user_confirm_recover', renderer='json', request_method='POST')
def user_confirm_recover(request):
    form = json.loads(request.body, encoding=request.charset)
    secret = request.registry.settings['secret_passphrase']
    try:
        auth = jwt.decode(form['token'], secret, audience='urn:geneulike/recover')
        user_id = auth['user']['id']
        user_in_db = request.registry.db_mongo['users'].find_one({'id': user_id})
        if user_in_db is None:
            return {'msg' : 'User does not exists', 'status' : 'warning'}
        user_password = form['user_password']
        new_password = bcrypt.hashpw(form['user_password'].encode('utf-8'), bcrypt.gensalt())
        request.registry.db_mongo['users'].update({'id': user_id},{'$set': {'password': new_password}})
        return {'msg': 'Your password have been recovered' , 'status' :'success'}
    except Exception:
        return {'msg': 'Contact the administrator' , 'status' :'danger'}


@view_config(route_name='infodatabase', renderer='json', request_method='GET')
def infodatabase(request):
    user = is_authenticated(request)
    if user is None:
        return HTTPUnauthorized('Not authorized to access this resource')
    if not (user['id'] in request.registry.admin_list):
        return HTTPUnauthorized('Not authorized to access this resource')
    project_number = request.registry.db_mongo['projects'].find({'status' :'private'}).count()
    study_number = request.registry.db_mongo['studies'].find({'status' :'private'}).count()
    strategy_number = request.registry.db_mongo['strategies'].find({'status' :'private'}).count()
    list_number = request.registry.db_mongo['lists'].find({'status' :'private'}).count()
    user_request = request.registry.db_mongo['users'].find()
    users = []
    for user in user_request:
        users.append(user)
    pending_request = request.registry.db_mongo['projects'].find({'status' :'pending approval'})
    pendings = []
    for pending in pending_request:
        pendings.append(pending)
    return {'msg':'Database ok','project_number':project_number,'study_number':study_number,'strategy_number': strategy_number,'list_number': list_number, 'users':users, 'pendings':pendings}

@view_config(route_name='validate', renderer='json', request_method='POST')
def validate(request):
    user = is_authenticated(request)
    if user is None:
        return HTTPUnauthorized('Not authorized to access this resource')
    if not (user['id'] in request.registry.admin_list):
        return HTTPUnauthorized('Not authorized to access this resource')

    form = json.loads(request.body, encoding=request.charset)
    if form['project'] != "" and form['project'] != "gohomo" :
        project = form['project']
        pid = project['id']
        stid = project['studies'].split(',')
        aid = project['assays'].split(',')
        sid = project['signatures'].split(',')
        request.registry.db_mongo['projects'].update({'id' :pid},{'$set':{'status':'public'}})
        request.registry.db_mongo['studies'].update({'id':{ '$all': stid } },{'$set':{'status':'public'}})
        request.registry.db_mongo['assays'].update({'id':{ '$all': stid } },{'$set':{'status':'public'}})
        request.registry.db_mongo['signatures'].update({'id':{ '$all': stid } },{'$set':{'status':'public'}})
        cmd = "python %s --signature a --script gopublic --job b --user none" % (os.path.join(request.registry.script_path, 'jobLauncher.py'))
        os.system(cmd)

        proj = request.registry.db_mongo['projects'].find_one({'id' :pid})
        del proj['_id']
        es = elasticsearch.Elasticsearch([config.get('app:main','elastic_host')])
        bulk_insert = ''
        bulk_insert += "{ \"index\" : { \"_index\" : \"toxsign\", \"_type\": \"projects\" , \"_id\" : \""+proj['id']+"\" } }\n"
        bulk_insert += json.dumps(proj)+"\n"
        if bulk_insert:
            es.bulk(body=bulk_insert)

        for stud in stid:
            study = request.registry.db_mongo['studies'].find_one({'id' :stud})
            del study['_id']
            es = elasticsearch.Elasticsearch([config.get('app:main','elastic_host')])
            bulk_insert = ''
            bulk_insert += "{ \"index\" : { \"_index\" : \"toxsign\", \"_type\": \"studies\" , \"_id\" : \""+study['id']+"\" } }\n"
            bulk_insert += json.dumps(study)+"\n"
            if bulk_insert:
                es.bulk(body=bulk_insert)

        for ass in aid:
            assay = request.registry.db_mongo['assays'].find_one({'id' :ass})
            del assay['_id']
            es = elasticsearch.Elasticsearch([config.get('app:main','elastic_host')])
            bulk_insert = ''
            bulk_insert += "{ \"index\" : { \"_index\" : \"toxsign\", \"_type\": \"assays\" , \"_id\" : \""+assay['id']+"\" } }\n"
            bulk_insert += json.dumps(assay)+"\n"
            if bulk_insert:
                es.bulk(body=bulk_insert)

        for sign in sid:
            signature = request.registry.db_mongo['signatures'].find_one({'id' :sign})
            del signature['_id']
            es = elasticsearch.Elasticsearch([config.get('app:main','elastic_host')])
            bulk_insert = ''
            bulk_insert += "{ \"index\" : { \"_index\" : \"toxsign\", \"_type\": \"signatures\" , \"_id\" : \""+signature['id']+"\" } }\n"
            bulk_insert += json.dumps(signature)+"\n"
            if bulk_insert:
                es.bulk(body=bulk_insert)
        return {'msg':'Project status changed : Pending --> public'}

    if form['project'] == "gohomo" :
        cmd = "python %s --signature a --script gohomo --job b --user none" % (os.path.join(request.registry.script_path, 'jobLauncher.py'))
        os.system(cmd)
        return {'msg':'Create annotation file Done'}
    else :
        cmd = "python %s --signature a --script gopublic --job b --user none" % (os.path.join(request.registry.script_path, 'jobLauncher.py'))
        os.system(cmd)
        return {'msg':'Create public.RData Done'}


@view_config(route_name='unvalidate', renderer='json', request_method='POST')
def unvalidate(request):
    user = is_authenticated(request)
    if user is None:
        return HTTPUnauthorized('Not authorized to access this resource')
    if not (user['id'] in request.registry.admin_list):
        return HTTPUnauthorized('Not authorized to access this resource')

    form = json.loads(request.body, encoding=request.charset)
    project = form['project']
    pid = project['id']
    stid = project['studies'].split(',')
    aid = project['assays'].split(',')
    sid = project['signatures'].split(',')
    request.registry.db_mongo['projects'].update({'id' :pid},{'$set':{'status':'private'}})
    request.registry.db_mongo['studies'].update({'id':{ '$all': stid } },{'$set':{'status':'private'}})
    request.registry.db_mongo['assays'].update({'id':{ '$all': stid } },{'$set':{'status':'private'}})
    request.registry.db_mongo['signatures'].update({'id':{ '$all': stid } },{'$set':{'status':'private'}})
    return {'msg':'Project status changed : Pending --> private'}


@view_config(route_name='pending', renderer='json', request_method='POST')
def pending(request):
    user = is_authenticated(request)
    if user is None:
        return HTTPUnauthorized('Not authorized to access this resource')


    form = json.loads(request.body, encoding=request.charset)
    project = form['project']

    if user['id'] != project['owner']:
        return HTTPUnauthorized('Not authorized to access this resource')

    pid = project['id']
    stid = project['studies']
    aid = project['assays']
    sid = project['signatures']
    request.registry.db_mongo['projects'].update({'id' :pid},{'$set':{'status':'pending approval'}})
    request.registry.db_mongo['studies'].update({'id':{ '$all': stid } },{'$set':{'status':'pending approval'}})
    request.registry.db_mongo['assays'].update({'id':{ '$all': stid } },{'$set':{'status':'pending approval'}})
    request.registry.db_mongo['signatures'].update({'id':{ '$all': stid } },{'$set':{'status':'pending approval'}})
    return {'msg':'Your project is now pending approval.'}


 


@view_config(route_name='1', renderer='json', request_method='POST')
def getdata(request):
    form = json.loads(request.body, encoding=request.charset)
    #print form.keys()
    #pprint.pprint(form)
    collection = form['collection']
    select_filter = form['filter']
    field = form['field']
    project_number = 0
    study_number = 0
    strategy_number = 0
    list_number = 0
    #print 'field', field
    #print "select_filter ", select_filter
    if 'all_info' in form :
        print"true"
        project_number = request.registry.db_mongo['projects'].find({field : select_filter}).count()
        study_number = request.registry.db_mongo['studies'].find({field : select_filter}).count()
        strategy_number = request.registry.db_mongo['strategies'].find({field : select_filter}).count()
        list_number = request.registry.db_mongo['lists'].find({field : select_filter}).count()
        print str(project_number), str(study_number), str(strategy_number), str(list_number)
    if 'obs' in form:
        number = request.registry.db_mongo[collection].find({field:select_filter}).count()
        if number>=30:
            result = list(request.registry.db_mongo[collection].find({field:select_filter}).skip(request.registry.db_mongo[collection].count() - 15))
        else:
            result= list(request.registry.db_mongo[collection].find({field:select_filter}).skip(request.registry.db_mongo[collection].count()-number))
        result.reverse()
        return {'msg':'','request':result} 

    if form['from'] == "None" :
        if collection=="projects":
            collec="project"
        else:
            collec=collection
        result = request.registry.db_mongo[collection].find_one({collec + "_id" :select_filter})
        print collection + "_id" +" : "+ select_filter
        #pprint.pprint(result)
        if result is not None :
            if 'edges' in result:
                if result['edges'] is not None :
                    if result['edges'] != "" :
                        dico = json.loads(result['edges'])
                        for i in dico :
                            if dico[i] != [] :
                                dico[i] = dico[i][0].split(',')
                        result['edges'] = dico
            return {'msg':'','request':result}

    else :
        print "here"
        selected = []
        if int(form['from']) < 0 :
            form['from'] = 0
        print collection
        print field
        print select_filter
        
        result = request.registry.db_mongo[collection].find({field :select_filter})
        #pprint.pprint(result)
        for res in result :
            selected.append(res)
        #print selected
        print str(len(selected))
        if len(selected) < int(form['from']) :
            form['from'] = len(selected) - 15
        if len(selected) < int(form['to']) :
            form['to'] = len(selected)

        return {'msg':'ok','request':selected[int(form['from']):int(form['to'])],'project_number':project_number,'study_number':study_number,'strategy_number':strategy_number,'list_number': list_number}

@view_config(route_name='ontologies', renderer='json', request_method='POST')
def ontologies(request):


#######################################################################################################################    
    def getParent(obj):
        # getParent : get all parents labels and synonyms for a selected term
        # obj : selected object from NCBO API
        # WARNING: works only from child to parent (one paent by child)
        # RETURN label : list of all label and synonyms (including selected term label & synonym)
        url = obj["links"]['parents']
        label = []
        label.append(obj["prefLabel"])
        if obj['synonym'] != []:
                    label.extend(obj['synonym'])
        page = get_json(url)
        while page != []:
            for result in page :
                label.append(result['prefLabel'])
                if result['synonym'] != []:
                    label.extend(result['synonym'])
                url = result["links"]['parents']
                page = get_json(url)
        return label

    def get_json(url):
        opener = urllib2.build_opener()
        opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
        return json.loads(opener.open(url).read())

    def stringToDict(string):
        if string == "":
            return {}

        dico={}
        for item in string.split(";")[:-1]:
            dico[item.split(":")[0]]=item.split(":")[1].split(',')

        return dico

    def dictToString(dico):

        if not bool(dico): #if dico is empty
            return ""

        newString="" 

        for key, value in dico.items():
            newString += str(key) + ":" + ",".join(value) +";"
        return newString

#######################################################################################################################


    REST_URL = "http://data.bioontology.org"
    API_KEY = "27f3a22f-92f8-4587-a884-e81953e113e6"
    form = json.loads(request.body, encoding=request.charset)

    if 'label' in form:
        print 'here labellllll'
        #print getParent(form['label'])

    elif 'stringToDict' in form:
        return [stringToDict(form['string'])]

    elif 'dictToString' in form:
        return [dictToString(form['dico'])]
        
    else:
        term = form['search'].replace(' ','+') #%20
        database = form['database']
        search_results = []
        search_results.append(get_json(REST_URL + "/search?q=" + term+'&ontologies=' + database)['collection'])

        return search_results

@view_config(route_name='getjob', renderer='json', request_method='POST')
def getjob(request):
    form = json.loads(request.body, encoding=request.charset)
    job_list = form['job_list']
    if job_list != "" :
        flist = []
        for i in job_list :
            try:
                flist.append(int(i))
            except:
                continue
        running_job = list(request.registry.db_mongo['Jobs'].find( {"id": {'$in': flist}}))

        return {'jobs':running_job}
    if job_list == "" :
        job = request.registry.db_mongo['Jobs'].find_one( {'_id': ObjectId(form['jid'])})
        return {'jobs':job}

@view_config(route_name='convert', renderer='json', request_method='POST')
def convert(request):
    form = json.loads(request.body, encoding=request.charset)
    genes_list = form['genes'].split(',')
    print genes_list
    dataset_in_db = ""

    if form['way'] == 'None' or form['way'] == 'EntrezToHomo' :
        if 'species' in form :
            dataset_in_db = list(request.registry.db_mongo['homoloGene'].find( {"Gene_ID": {'$in': genes_list},'Taxonomy_ID':form['species']},{ "HID": 1, "Gene_ID": 1, "Gene_Symbol":1,'Taxonomy_ID':1,"_id": 0 } ))
            result = []
            for dataset in dataset_in_db:
                if 'NA' not in dataset["HID"]:
                    result.append(dataset)
            return {'converted_list':result}
        else :
            dataset_in_db = list(request.registry.db_mongo['genes'].find( {"GeneID": {'$in': genes_list}},{"HID":1, "_id": 0 } ))
            result = []
            for dataset in dataset_in_db:
                if 'NA' not in dataset["HID"]:
                    result.append(dataset["HID"].replace('\n',''))
            #print result
            return {'converted_list':result}
    else :
        dataset_in_db = list(request.registry.db_mongo['homoloGene'].find( {"HID": {'$in': genes_list},'Taxonomy_ID':form['species']},{ "HID": 1, "Gene_ID": 1, "Gene_Symbol":1,'Taxonomy_ID':1,"_id": 0 } ))
        result = []
        for dataset in dataset_in_db:
            if 'NA' not in dataset["Gene_ID"]:
                result.append(dataset)
        return {'converted_list':result}


@view_config(route_name='readresult', renderer='json', request_method='POST')
def readresult(request):
    form = json.loads(request.body, encoding=request.charset)
    jid = form['job']
    print "readresults"

    job_info = request.registry.db_mongo['Jobs'].find_one({'id':jid})
    result_file = job_info['result']
    param = job_info['arguments'].split(',')
    filter_val = param[0]
    arg_val = param[1]
    value = param[2]
    if job_info['tool'] == "distance analysis" :
        orgafile = {'pvalue':7,'zscore':6,'r':1}
        if os.path.getsize(result_file) == 0 :
            return {'msg':'No enrichment are available','Bp':[],'Disease': [],'Mf':[],'Cc':[] ,'status':"0"}
        else :
            lsg=[]
            fileGo = open(result_file,'r')
            L = fileGo.readlines()
            fileGo.close()

            R = [e.split('\t')  for e in L]#creation list fichier
            #print len(R)
            if arg_val == 'lt' :
                R = [x for x in R if float(x[orgafile[filter_val]])<=float(value)]
                    
            if arg_val == 'gt' :
                R = [x for x in R if float(x[orgafile[filter_val]])>=float(value)]


            for line in R :
                name_sig = request.registry.db_mongo['signatures'].find_one({'id':line[0]})
                dGo = {'name':line[0]+' - '+name_sig['title'],'signature':line[0],'r':int(line[1]),'R':int(line[2]),'n':int(line[3]),'N':int(line[4]),'rR':float(line[5]),'zscore':float(line[6]),'pvalue':float(line[7]),'euclid':float(line[8]),'cor':float(line[9]),'genes':line[10]}
                lsg.append(dGo)
            return {'msg':'Enrichment Done','results':lsg,'status':"0"}

    if job_info['tool'] == "functional analysis" :
        orgafile = {'pvalue':7,'pbh':8,'r':2,'n':4}
        lbp=[]
        lcc=[]
        lds=[]
        lmf=[]
        fileGo = open(result_file,'r')
        L = fileGo.readlines()
        fileGo.close()

        R = [e.split('\t')  for e in L]#creation list fichier
        #print len(R)
        if arg_val == 'lt' :
            R = [x for x in R if float(x[orgafile[filter_val]])<=float(value)]
            
        if arg_val == 'gt' :
            R = [x for x in R if float(x[orgafile[filter_val]])>=float(value)]
        #print len(R)
        for line in R :
            dGo = {'Term':line[1],'r':int(line[2]),'R':int(line[3]),'n':int(line[4]),'N':int(line[5]),'rR':float(line[6]),'pvalue':float(line[7]),'pbh':float(line[8])}
            #print dGo
            if line[0] == 'Process' :
                lbp.append(dGo)
            if line[0] == 'Component' :
                lcc.append(dGo)
            if line[0] == 'Phenotype' :
                lds.append(dGo)
            if line[0] == 'Function' :
                lmf.append(dGo)

        return {'msg':'Enrichment Done','Bp':lbp,'Disease': lds,'Mf':lmf,'Cc':lcc ,'status':"0"}

@view_config(route_name='run', renderer='json', request_method='POST')
def run(request):
    form = json.loads(request.body, encoding=request.charset)
    user_id = form['uid']
    arguments = form['arguments']
    tool = form['tool']
    name = form['name']
    signature = json.loads(form['signature'])


    dt = datetime.datetime.utcnow()
    sdt = time.mktime(dt.timetuple())


    if signature is None :
        return {'msg':'Error - TOXsIgn is not able to find your signature. If the problem persists, please contact administrators'}
    else :
        if signature['type'] != 'Genomic' :
            return {'msg':'Error - Your signature is not a genomics signature.','id':'None'}
        if signature['status'] == 'private' and signature['owner'] != user_id :
            return {'msg':'Error - Your are not authorized to access this resource.','id':'None'}
        file_up = ""
        file_down = ""
        file_interogated =""
        request.registry.db_mongo['Jobs'].update({'id': 1}, {'$inc': {'val': 1}})
        repos = request.registry.db_mongo['Jobs'].find_one({'id': 1})
        jobID = repos['val']
        if name == "" :
            name = 'TOXsIgN job n°'+str(jobID)
        dico = {
            'id': jobID,
            'name':name,
            'status' : 'creating',
            'user': user_id,
            'tool': tool,
            'signature' :signature['id'],
            'time':sdt,
            'stderr':'',
            'arguments':arguments
        }
        request.registry.db_mongo['Jobs'].insert(dico)
        tool = tool.replace(" ","_")
        cmd = "--signature %s,--script %s,--job %s,--user %s" %(signature['id'],tool,jobID, user_id)
        subprocess.Popen(["python", os.path.join(request.registry.script_path, 'jobLauncher.py'),"--signature",str(signature['id']),'--script',tool,'--job',str(jobID),'--user',str(user_id)])
        return {'msg':'Job '+str(jobID)+' submitted','id':jobID}




@view_config(route_name='download', request_method='GET')
def download_data(request):
    session_user = is_authenticated(request)
    dataset_id = request.matchdict['dataset']
    
    result = request.registry.db_mongo['projects'].find_one({'id' :dataset_id})
    if result['status'] == 'public' :
        name = 'TOXsIgN_'+dataset_id+'.xlsx'
        url_file = os.path.join(request.registry.public_path,dataset_id,name)
        (handle, tmp_file) = tempfile.mkstemp('.zip')
        z = zipfile.ZipFile(tmp_file, "w")
        z.write(url_file,os.path.basename(url_file))
        z.close()
        return FileResponse(tmp_file,
                            request=request,
                            content_type='application/zip')

    if result['status'] == 'private':
        if session_user is None:
            token = None
            try:
                token = request.params['token']
                #print 'TOKEN'
                #print token
            except Exception:
                token = None
            auth = None
            try:
                secret = request.registry.settings['secret_passphrase']
                # If decode ok and not expired
                auth = jwt.decode(token, secret, audience='urn:geneulike/api')
            except Exception as e:
                return HTTPUnauthorized('Not authorized to access this resource')
            if auth is None:
                return HTTPForbidden()
        #print 'PRIVATE'
        #print result['owner']
        #print auth

        if auth['user']['id'] == result['owner'] :
            name = 'TOXsIgN_'+dataset_id+'.xlsx'
            url_file = os.path.join(request.registry.upload_path,result['owner'],dataset_id,name)
            (handle, tmp_file) = tempfile.mkstemp('.zip')
            z = zipfile.ZipFile(tmp_file, "w")
            z.write(url_file,os.path.basename(url_file))
            z.close()
            return FileResponse(tmp_file,
                                request=request,
                                content_type='application/zip')
        else :
            return {'msg':'You are not authorized to access this content'}

@view_config(route_name='file_dataset', request_method='GET')
def file_dataset(request):
    print "Get Dataset"
    directory = request.matchdict['dir']
    downfile = request.matchdict['file']
    url_file = os.path.join(request.registry.dataset_path,directory,downfile)
    (handle, tmp_file) = tempfile.mkstemp('.zip')
    z = zipfile.ZipFile(tmp_file, "w")
    z.write(url_file,os.path.basename(url_file))
    z.close()
    return FileResponse(tmp_file,
                        request=request,
                        content_type='application/zip')

@view_config(route_name='file_signature', request_method='GET')
def file_signature(request):
    session_user = is_authenticated(request)
    dataset_id = request.matchdict['project']
    signature_id = request.matchdict['signature']
    file_id = request.matchdict['file']
    
    if signature_id == 'none':
        result = ""
        if 'project' in file_id :
            result = request.registry.db_mongo['projects'].find_one({'id' :dataset_id})
        if 'study' in file_id :
            result = request.registry.db_mongo['studies'].find_one({'id' :dataset_id})
        if 'assay' in file_id :
            result = request.registry.db_mongo['assays'].find_one({'id' :dataset_id})
        if 'signature' in file_id :
            result = request.registry.db_mongo['signatures'].find_one({'id' :dataset_id})
        

        name = file_id+'.csv'
        results = []
        results.append(result)
        header = result.keys()

        file_path = os.path.join(request.registry.upload_path,'tmp')

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        with open(os.path.join(file_path,name),'w') as outfile:
            writer = DictWriter(outfile, header)
            writer.writeheader()
            writer.writerows(results)


        url_file = os.path.join(file_path,name)
        (handle, tmp_file) = tempfile.mkstemp('.zip')
        z = zipfile.ZipFile(tmp_file, "w")
        z.write(url_file,os.path.basename(url_file))
        z.close()
        return FileResponse(tmp_file,
                            request=request,
                            content_type='application/zip')



    result = request.registry.db_mongo['signatures'].find_one({'id' :signature_id})
    if result['status'] == 'public' :
        name = file_id
        url_file = os.path.join(request.registry.public_path,dataset_id,signature_id,name)
        (handle, tmp_file) = tempfile.mkstemp('.zip')
        z = zipfile.ZipFile(tmp_file, "w")
        z.write(url_file,os.path.basename(url_file))
        z.close()
        return FileResponse(tmp_file,
                            request=request,
                            content_type='application/zip')

    if result['status'] == 'private':
        if session_user is None:
            token = None
            try:
                token = request.params['token']
            except Exception:
                token = None
            auth = None
            try:
                secret = request.registry.settings['secret_passphrase']
                # If decode ok and not expired
                auth = jwt.decode(token, secret, audience='urn:geneulike/api')
            except Exception as e:
                return HTTPUnauthorized('Not authorized to access this resource')
            if auth is None:
                return HTTPForbidden()

        if auth['user']['id'] == result['owner'] :
            name = file_id
            url_file = os.path.join(request.registry.upload_path,result['owner'],dataset_id,signature_id,name)
            (handle, tmp_file) = tempfile.mkstemp('.zip')
            z = zipfile.ZipFile(tmp_file, "w")
            z.write(url_file,os.path.basename(url_file))
            z.close()
            return FileResponse(tmp_file,
                                request=request,
                                content_type='application/zip')
        else :
            return {'msg':'You are not authorized to access this content'}


@view_config(route_name='file_upload', renderer='json', request_method='POST')
def file_upload(request):
    print "file_upload"
    session_user = is_authenticated(request)
    if session_user is None:
        return 'HTTPForbidden()'
    input_file = None
    try:
        input_file = request.POST['file'].file
    except Exception:
        return HTTPForbidden('no input file')

    signature_selected = request.registry.db_mongo['signatures'].find_one({'id' :request.POST['sid']})
    if signature_selected is None :
        return {'msg':'Something went wrong if the problem persists, please contact administrators'}
    if signature_selected['owner'] !=  request.POST['uid'] :
        return HTTPForbidden('Not authorized to access this resource')

    if signature_selected[request.POST['type']] == "" :
        request.registry.db_mongo['signatures'].update({'id' :request.POST['sid']},{'$set':{request.POST['type']:request.POST['name']}})
    else :
        if request.POST['name'] not in signature_selected[request.POST['type']].split(',') :
            return {'msg':'No file corresponding to your uploaded file. Please update the file name using project updating button'}
        else :
            print request.POST['name']
            print signature_selected[request.POST['type']].split()

    if request.POST['type'] == 'additional_file' :
        tmp_file_name = uuid.uuid4().hex
        file_path = os.path.join('/tmp', '%s.sig' % tmp_file_name)
        temp_file_path = file_path + '~'

        # Finally write the data to a temporary file
        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)
        # Now that we know the file has been fully saved to disk move it into place.

        upload_path = os.path.join(request.registry.upload_path, request.params['uid'], request.params['dataset'], request.params['sid'])
        #print upload_path
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        shutil.move(temp_file_path, os.path.join(upload_path, request.params['name']))
        print 'write file into : '+ upload_path
        return {'msg':'Upload complete'}
    else :
        if signature_selected[request.POST['type']] == "" :
            request.registry.db_mongo['signatures'].update({'id' :request.POST['sid']},{'$set':{request.POST['type']:request.POST['name']}})
        else :
            if request.POST['name'] not in signature_selected[request.POST['type']].split(',') :
                return {'msg':'No file corresponding to your uploaded file. Please update the file name using project updating button'}
            else :
                print request.POST['name']
                print signature_selected[request.POST['type']].split()
        try :
            if signature_selected['genes_identifier'] == 'Entrez genes' :

                tmp_file_name = uuid.uuid4().hex
                print tmp_file_name
                file_path = os.path.join('/tmp', '%s.sig' % tmp_file_name)
                temp_file_path = file_path + '~'

                # Finally write the data to a temporary file
                with open(temp_file_path, 'wb') as output_file:
                    shutil.copyfileobj(input_file, output_file)
                # Now that we know the file has been fully saved to disk move it into place.

                upload_path = os.path.join(request.registry.upload_path, request.params['uid'], 'tmp')
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)
                shutil.move(temp_file_path, os.path.join(upload_path, tmp_file_name))
                check_file = open(os.path.join(upload_path, tmp_file_name),'r')
                lId = []
                for lineID in check_file.readlines():
                    if lineID != '' and lineID != 'NA' and lineID != '-' and lineID != 'na' and lineID != ' ' and lineID != 'Na' :
                        IDs = lineID.replace('\n','\t').replace(',','\t').replace(';','\t')
                        lId.append(IDs.split('\t')[0])
                lId = list(set(lId))
                print lId
                check_file.close()
                dataset_in_db = list(request.registry.db_mongo['genes'].find( {"GeneID": {'$in': lId}},{ "GeneID": 1,"Symbol": 1,"HID":1, "_id": 0 } ))
                lresult = {}
                for i in dataset_in_db:
                    lresult[i['GeneID']]=[i['Symbol'],i['HID']]

                #Create 4 columns signature file
                print 'test si file'
                if os.path.isfile(os.path.join(request.registry.upload_path, request.params['uid'], request.params['dataset'], request.params['sid'],request.params['name'])):
                    print 'Remove car existes'
                    os.remove(os.path.join(request.registry.upload_path, request.params['uid'], request.params['dataset'], request.params['sid'],request.params['name']))

                print 'Remove tmp'
                os.remove(os.path.join(upload_path, tmp_file_name))

                print 'create directory'
                if not os.path.exists(os.path.join(request.registry.upload_path, request.params['uid'], request.params['dataset'], request.params['sid'])):
                    os.makedirs(os.path.join(request.registry.upload_path, request.params['uid'], request.params['dataset'], request.params['sid']))
                
                print 'Create final'
                check_files = open(os.path.join(request.registry.upload_path, request.params['uid'], request.params['dataset'], request.params['sid'],request.params['name']),'a')
                have_wrong = 0
                for ids in lId :
                    if ids in lresult :
                        check_files.write(ids+'\t'+lresult[ids][0]+'\t'+lresult[ids][1].replace('\n','')+'\t1\n')
                    else :
                        check_files.write(ids+'\t'+'NA\tNA'+'\t0\n')  
                        have_wrong = 1                  
                check_files.close()
                print "File checked and uploded !"
                if 'up' in request.params['type'] :
                    request.registry.db_mongo['signatures'].update({'id' :request.POST['sid']},{'$set':{'genes_up':','.join(lId)}})
                if 'down' in request.params['type'] :
                    request.registry.db_mongo['signatures'].update({'id' :request.POST['sid']},{'$set':{'genes_down':','.join(lId)}})
                if have_wrong == 0 :
                    return {'msg':"File checked and uploded !",'status': '0' }
                else : 
                    return {'msg':"Warning ! Some IDs are not EntrezGene ID or are desprecated",'status': '0' }
     
        except :
            print sys.exc_info()[1]
            return {'msg':"TOXsIgN can't read your file. Please make sure you use the correct format. If this error persists, please contact the site administrator.",'status': '1' }

        return {'msg': "TOXsIgN can't read your file. Please make sure you use the correct format. If this error persists, please contact the site administrator."}



    #print user
    #print signature_id


# @view_config(route_name='createExcel', xhr=True, renderer='json', request_method='POST')
# def createExcel(request):
#     print "TOTO"
#     return logging.error("TOTO")
    
    #session_user = is_authenticated(request)
    # print request
    # input_file = request.POST['file'].file
    # tmp_file_name = uuid.uuid4().hex
    # file_path = os.path.join('/tmp', '%s.sig' % tmp_file_name)
    # temp_file_path = file_path + '~'
    # with open(temp_file_path, 'wb') as output_file:
    #     shutil.copyfileobj(input_file, output_file)

    # if session_user == None:
    #     return 'HTTPForbidden()'
    # return {'message' : 'true'}
import unicodedata as ucd


def get_str(string):
    if isinstance(string, float):
        return str(int(string)).encode('utf-8')
    elif string == '':
        return str("").encode('utf-8')
    else:
        return string.encode('utf-8')

@view_config(route_name="addFileNameToObjectFiles", renderer='json', request_method='POST')
def addFileNameToObjectFiles(request):
    session_user = is_authenticated(request)
    if session_user is None:
        return 'HTTPForbidden()'

    form = json.loads(request.body, encoding=request.charset)

    ObjectFiles={}
    try:
        for index in range(1,len(form['data_filename'])):
            if form['data_filename'][index] != "":
                if form['data_available'][index] == 'Yes':
                    filenameRequired=form['data_filename'][index].split('.')[0]
                    ObjectFiles[filenameRequired] = {'identifiant' : form['data_identifiant'][index],'name':"",'file' : None , 'status':"waiting", 'filepath' : "", 'msg':''}

        return {'ObjectFiles' : ObjectFiles}

    except:
        logger.warning("Error - removeFileListUpload - def addFileNameToObjectFiles()")
        logger.warning(upload_path)
        logger.warning(sys.exc_info())
        return {'ObjectFiles': ObjectFiles, 'msg': "An error has occured. Please contact the administrator !"}

@view_config(route_name="getGPLnumber", renderer='json', request_method='POST')
def getGPLnumber(request):
    session_user = is_authenticated(request)
    if session_user is None:
        return 'HTTPForbidden()'

    form = json.loads(request.body, encoding=request.charset)
    gpl = form['GPL']
    path = 'Template/GPL'
    listGPL=[]
    try:
        with open(os.path.join(path,gpl), 'r') as output:   
            for item in output:
                listGPL.append({'id':str(item.split('\n')[0]), 'name': str(item.split('\n')[0])})
        return listGPL
    except:
        logger.warning("Error - removeFileListUpload - def getGPLnumber()")
        logger.warning(upload_path)
        logger.warning(sys.exc_info())
        return ['An error','has occured.', "Please contact", "the administrator!"]

@view_config(route_name="removeFileListUpload", renderer='json', request_method='POST')
def removeFileListUpload(request):
    session_user = is_authenticated(request)
    if session_user is None:
        return 'HTTPForbidden()'

    form=json.loads(request.body, encoding=request.charset)
    try:
        os.remove(form['filepath'])
        return {'msg' : "This file has been removed. Add a new one.", 'boolean' : True}
    except:
        logger.warning("Error - removeFileListUpload - def removeFileListUpload()")
        logger.warning(form['filepath'])
        logger.warning(sys.exc_info())
        return {'msg': "This file has not been removed. Try Again. If this error persist please contact the adminastrator", 'boolean' : False}



@view_config(route_name="fileListUpload", renderer='json', request_method='POST')
def fileListUpload(request):
    session_user = is_authenticated(request)
    if session_user is None:
        return 'HTTPForbidden()'

    input_file = None
    try:
        input_file = request.POST['file'].file
        number=json.loads(request.POST['data'], encoding=request.charset)['info']

    except Exception:
        return HTTPForbidden('no input file')

    try :
        tmp_file_name = uuid.uuid4().hex +".txt"
        file_path = os.path.join('/tmp', '%s.sig' % tmp_file_name)
        temp_file_path = file_path + '~'

        # Finally write the data to a temporary file
        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)
        # Now that we know the file has been fully saved to disk move it into place.

        upload_path = os.path.join(request.registry.upload_path, request.params['uid'], request.params['dataset'])

        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        shutil.move(temp_file_path, os.path.join(upload_path, tmp_file_name))

        return {'filepath' : os.path.join(upload_path, tmp_file_name) , 'status' : 'success', 'number':number ,'msg':'File Uploaded and conform'}
    except:
        logger.warning("Error - Upload path - def fileListUpload()")
        logger.warning(upload_path)
        logger.warning(sys.exc_info())
        return {'msg':'An error occurred while uploading your file. If the error persists please contact GeneULike support ','status':'warning', 'number':number}


################HERE###########
@view_config(route_name='excel_upload', renderer='json', request_method='POST')
def excel_signature_upload(request):
    #print "excel_signature_upload"

    session_user = is_authenticated(request)
    if session_user is None:
        return 'HTTPForbidden()'

    input_file = None
    try:
        input_file = request.POST['file'].file
    except Exception:
        return HTTPForbidden('no input file')

    try :
        tmp_file_name = uuid.uuid4().hex +".xls"
        file_path = os.path.join('/tmp', '%s.sig' % tmp_file_name)
        temp_file_path = file_path + '~'

        # Finally write the data to a temporary file
        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)
        # Now that we know the file has been fully saved to disk move it into place.

        upload_path = os.path.join(request.registry.upload_path, request.params['uid'], request.params['dataset'])


        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        shutil.move(temp_file_path, os.path.join(upload_path, tmp_file_name))

    except:
        logger.warning("Error - Upload path - def excel_signature_upload()")
        logger.warning(upload_path)
        logger.warning(sys.exc_info())
        return {'msg':'An error occurred while uploading your file. If the error persists please contact GeneULike support ','status':'1'}

###Test###

    #Read excel file
    wb = xlrd.open_workbook(os.path.join(upload_path, tmp_file_name),encoding_override="cp1251")

    projects=[]
    strategies=[]
    lists=[] 
    for row_number in range(wb.sheet_by_index(0).nrows):
        projects.append(wb.sheet_by_index(0).row_values(row_number,start_colx=0, end_colx=101))
    for row_number in range(wb.sheet_by_index(2).nrows):
        strategies.append(wb.sheet_by_index(2).row_values(row_number,start_colx=0, end_colx=201))
    strategies.append([ '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

    for row_number in range(wb.sheet_by_index(1).nrows):
            lists.append(wb.sheet_by_index(1).row_values(row_number,start_colx=0, end_colx=1001))

    try:
        os.remove(os.path.join(upload_path,tmp_file_name))
    except:
        logger.warning("Error - Can't delete upload file - def excel_signature_upload()")
        logger.warning(os.path.join(upload_path,tmp_file_name))
        logger.warning(sys.exc_info())
       
           
    return{'projects':projects, 'strategies':strategies, 'lists':lists}




#     # for line in wb.sheet_by_index(0).row_values(row_number, start_colx=0, end_colx=101):
#     #     for i in line:
#     #         print i

#     #remove file

#     # return

#     # add_project(wb.sheet_by_index(0)) 
        
#     # add_study(wb.sheet_by_index(1))
        
#     # add_strategy(wb.sheet_by_index(2))
        
#     # add_list(wb.sheet_by_index(3),wb.sheet_by_index(4))
# ###End#Test####



#     #Create error list
#     projects_errors = {'Critical':[],'Warning':[],'Info':[]}
#     studies_errors = {'Critical':[],'Warning':[],'Info':[]}
#     strategies_errors = {'Critical':[],'Warning':[],'Info':[]}
#     lists_errors = {'Critical':[],'Warning':[],'Info':[]}
#     idLists_errors = {'Critical':[],'Warning':[],'Info':[]}

#     projects_identifiers = []
#     studies_identifiers = []
#     strategies_identifiers = []
#     lists_identifiers = []
#     idLists_identifiers = []
#     has_identifier =[]
#     global critical
#     critical=0



#     zorro = 1
#     def is_empty(row_value):
#         boolean=False
#        # print row_value
#         for i in row_value:
#             #print str(i)
#             if row_value != "":
#                 return True
#         return boolean

# #Project sheet
#     # def is_project_identifier(row_value_identifier):
#     #     return row_value_identifier == ""
    
#     # def is_project_title(row_value_title):
#     #     return row_value_title == ""
        
#     # def is_project_description(row_value_description):
#     #     return row_value_description == ""        
        
#     # def is_project_pubmed(row_value_pubmed):
#     #     return row_value_pubmed == ""
    
#     # def is_project_contributor(row_value_contributor):
#     #     return row_value_contributor == ""

#     def is_project_error(identifier, title, description, pubmed, contributor, row_number):
#         """Si il existe des erreurs, c'est erreurs sont consignés dans le dico projects_errors"""
#         global critical
#         if not identifier:
#             #print True
#             projects_errors['Critical'].append("Line " + str(row_number+1) + " - no ProjectID")
#             critical += 1
#         if not title:
#             projects_errors['Critical'].append("Line " + str(row_number+1) + " -  no Title")
#             critical += 1
#         if not description:
#             projects_errors['Warning'].append("Line " + str(row_number+1) + " -  no Description")
#         if not pubmed:
#             projects_errors['Warning'].append("Line " + str(row_number+1) + " - no PubMed DOI")
#         if not contributor:
#             projects_errors['Info'].append("Line " + str(row_number+1) + " - no Contributor(s)")
#         if identifier in projects_identifiers:
#             projects_errors['Critical'].append("Line " + str(row_number+1) + " -  2 identical ProjectID")
#             critical += 1
#     def is_project_row(row_value, row_number):
#         if is_empty(row_value): 
#             is_project_error(   (row_value[0]),\
#                                 (row_value[1]),\
#                                 (row_value[2]),\
#                                 (row_value[3]),\
#                                 (row_value[4]),\
#                                 row_number)

#             if str(row_value[0]):
#                 projects_identifiers.append(str(row_value[0]))
#                 has_identifier.append([str(row_value[0]), "", "", ""])
               
#     def projects_sheet(projects):
        
#         #wb = open_workbook(os.path.join(self.upload_path, self.file_name),encoding_override="cp1251")
#         #projects = 
#         for row_number in range(5, projects.nrows):
#             is_project_row( projects.row_values(row_number, start_colx=0, end_colx=None), row_number)

#     # def get_plain_text(_list):
#     #     newList=[]
#     #     print _list
#     #     for elt in _list:
#     #         if elt == '':
#     #             newList.append(str(""))
#     #         elif isinstance(elt, float ):
#     #             newList.append(str(int(elt)))
#     #         else:
#     #             newList.append(str(elt.encode("utf-8")))
#     #     print newList
#     #     return newList
# # title = u"Klüft ć skräms inför på fédéral électoral große"

# # print str(unicodedata.normalize('NFKD', title).encode('ascii','ignore'))

# #Studies sheet

#     # def is_study_identifier(row_value_identifier):
#     #     return row_value_identifier == ""
    
#     def is_study_associated_project_identifier(row_value_associated_project_identifier):
#         return str(row_value_associated_project_identifier) not in projects_identifiers

#     # def is_study_title(row_value_title):
#     #     return row_value_title == ""
    
#     # def is_study_description(row_value_description):
#     #     return row_value_description == ""
    
#     # def is_study_phenotype_desease(row_value_phenotype_desease):
#     #     return row_value_phenotype_desease == ""

#     # def is_study_go_terms(row_value_go_terms):
#     #     return row_value_go_terms == ""
    
#     # def is_study_organism(row_value_organism):
#     #     return row_value_organism == ""
    
#     # def is_study_development_stage(row_value_development_stage):
#     #     return row_value_development_stage == ""

#     # def is_study_pubmed(row_value_pubmed):
#     #     return row_value_pubmed == ""

#     def get_unicode_to_str(_lists):

#         newList = []
#         #print _lists
#         for x in _lists:
#             if x == '':
#                 newList.append(str(""))

#             elif isinstance(x, float):
#                 newList.append(str(int(x)))
#             else:
#                 newList.append(x.decode("utf-8"))

#             #print x.encode('utf-8')
#             #if isinstance(x, unicode):
#                 #newList.append(x.encode('utf-8'))
#                 #ucd.name(x)
#                 #newList.append(unicodedata.normalize('NFKD', x).encode('ascii','ignore'))
#             #if 
#             #else:
#             #    newList.append(x)
#             #x.replace('\u2018','\'')
#             #x.replace('\u2019','\'')
#             #print x      
#             #strList.append(str(x))
#         #for x in newList:
#             #print get_str(x) 
#         #print strList
#         return newList

#     def get_str(element):
#         return element.encode('utf-8')

#     def is_study_error(identifier, associated_project_identifier, title, description, \
#                         phenotype_desease, go_terms, organism, development_stage, pubmed, row_number):
        
#         global critical

#         if not identifier:
#             studies_errors['Critical'].append("Line " + str(row_number+1) + " - no StudyID")
#             critical += 1
#         if(associated_project_identifier):
#             studies_errors['Critical'].append("Line " + str(row_number+1) + " - no Associated ProjectID")
#             critical += 1
#         if not title:
#             studies_errors['Critical'].append("Line " + str(row_number+1) + " - no Title")
#             critical += 1
#         if not description:
#             studies_errors['Warning'].append("Line " + str(row_number+1) + " - no Description")
#         if not phenotype_desease:
#             studies_errors['Info'].append("Line " + str(row_number+1) + " - no Phenotype/Desease")
#         if not go_terms:
#             studies_errors['Info'].append("Line " + str(row_number+1) + " - no Go terms")
#         if not organism:
#             studies_errors['Info'].append("Line " + str(row_number+1) + " - no Organism")
#         if not development_stage:
#             studies_errors['Info'].append("Line " + str(row_number+1) + " - no Development Stage")
#         if not pubmed:
#             studies_errors['Info'].append("Line " + str(row_number+1) + " - no Pubmed")
#         if identifier in studies_identifiers:
#             studies_errors['Critical'].append("Line " + str(row_number+1) + " -  2 identical StudiesID")
#             critical += 1

#     def is_study_row(row_value, row_number):
#         if is_empty(row_value):    
#             is_study_error( (row_value[0]),\
#                             is_study_associated_project_identifier((row_value[1])),\
#                             (row_value[2]),\
#                             (row_value[3]),\
#                             (row_value[4]),\
#                             (row_value[5]),\
#                             (row_value[6]),\
#                             (row_value[7]),\
#                             (row_value[8]),\
#                             row_number)
                                
#             if(str(row_value[0])):
#                 studies_identifiers.append((row_value[0]))
#                 for i in range(len(has_identifier)):
#                     if has_identifier[i][0] == (row_value[1]):
#                         has_identifier[i][1] += (row_value[0])

#     def studies_sheet(studies):
#         #wb = open_workbook(os.path.join(self.upload_path, self.file_name),encoding_override="cp1251")
#         #studies = wb.sheet_by_index(1)
#         #print studies
#         for row_number in range(5, studies.nrows):
#             #print studies.row_values(row_number, start_colx=0, end_colx=None)
#             #is_study_row(studies.row_values(row_number, start_colx=0, end_colx=None), row_number)
#             #is_study_row([str(unicodedata.normalize('NFKD', str(x)).encode('ascii','ignore')) for x in studies.row_values(row_number, start_colx=0, end_colx=None)], row_number)
#             is_study_row((studies.row_values(row_number, start_colx=0, end_colx=None)), row_number)




# #Strategies sheet

#     # def is_strategy_identifier(row_value_identifier):
#     #     return row_value_identifier == ""
    
#     def is_strategy_associated_study_identifier(row_value_associated_study_identifier):
#         return row_value_associated_study_identifier not in studies_identifiers
    
#     # def is_strategy_title(row_value_title):
#     #     return row_value_title == ""
    
#     # def is_strategy_description(row_value_description):
#     #     return row_value_description == ""
    
#     # def is_strategy_type_of_experiment(row_value_type_of_experiment):
#     #     return row_value_type_of_experiment == ""
    
#     # def is_strategy_technology(row_value_technology):
#     #     return row_value_technology == ""
    
#     # def is_strategy_process(row_value_process):
#     #     return row_value_process == ""
    
    
#     def is_strategy_error(identifier, associated_study_identifier, title, description,\
#                             type_of_experiment, technology, process, row_number):
#         global critical
#         if not identifier:
#             strategies_errors['Critical'].append("Line " + str(row_number+1) + " - no StrategyID")
#             critical += 1
#         if(associated_study_identifier):
#             strategies_errors['Critical'].append("Line " + str(row_number+1) + " - no Associated StudyID")
#             critical += 1
#         if not title:
#             strategies_errors['Critical'].append("Line " + str(row_number+1) + " - no Title")
#             critical += 1
#         if not description:
#             strategies_errors['Warning'].append("Line " + str(row_number+1) + " - no Description")
#         if not type_of_experiment:
#             strategies_errors['Warning'].append("Line " + str(row_number+1) + " - no Type of Experiment")
#         if not technology:
#             strategies_errors['Warning'].append("Line " + str(row_number+1) + " - no Technology")
#         if not process:
#             strategies_errors['Warning'].append("Line " + str(row_number+1) + " - no Process")
#         if identifier in strategies_identifiers:
#             strategies_errors['Critical'].append("Line " + str(row_number+1) + " -  2 identical StrategyID")
#             critical += 1

#     def is_strategy_row(row_value, row_number):
#         if is_empty(row_value): 
#             is_strategy_error(  (row_value[0]),\
#                                 is_strategy_associated_study_identifier((row_value[1])),\
#                                 (row_value[2]),\
#                                 (row_value[3]),\
#                                 (row_value[4]),\
#                                 (row_value[5]),\
#                                 (row_value[6]),\
#                                 row_number)
                                    
#             if(str(row_value[0])):
#                 strategies_identifiers.append((row_value[0]))
#                 for i in range(len(has_identifier)):
#                     if has_identifier[i][1] == (row_value[1]):
#                         has_identifier[i][2] += (row_value[0])


#     def strategies_sheet(strategies):
#         for row_number in range(5, strategies.nrows):
#             is_strategy_row((strategies.row_values(row_number, start_colx=0, end_colx=None)), row_number)



# #lists sheet
#     # def is_list_identifier(row_value_identifier):
#     #     return row_value_identifier == ""
    
#     def is_list_associated_strategy_identifier(row_value_associated_strategy_identifier):
#         return row_value_associated_strategy_identifier not in strategies_identifiers
    
#     # def is_list_title(row_value_title):
#     #     return row_value_title == ""
    
#     # def is_list_description(row_value_description):
#     #     return row_value_description == ""
    
#     # def is_list_type_of_identifier(row_value_type_of_identifier):
#     #     return row_value_type_of_identifier == ""
    
#     def is_list_extended_type_of_identifier(row_value_extended_type_of_identifier, row_value_type_of_identifier):
#         return (row_value_extended_type_of_identifier == "" and row_value_type_of_identifier[:3] == "GPL")
    
#     # def is_list_parent_list_identifier(row_value_parent_list_identifier):
#     #     return row_value_parent_list_identifier == ""
    
#     # def is_list_child_list_identifier(row_value_child_list_identifier):
#     #     return row_value_child_list_identifier == ""
    
#     def is_list_error(identifier, associated_study_identifier, title, description,\
#                         type_of_identifier,extended_type_of_identifier,\
#                         parent_list_identifier, child_list_identifier, row_number):
        
#         global critical

#         if not identifier:
#             lists_errors['Critical'].append("Line " + str(row_number+1) + " - no ListID")
#             critical += 1
#         if(associated_study_identifier):
#             lists_errors['Critical'].append("Line " + str(row_number+1) + " - no Associated StrategyID")
#             critical += 1
#         if not title:
#             lists_errors['Critical'].append("Line " + str(row_number+1) + " - no Title")
#             critical += 1
#         if not description:
#             lists_errors['Warning'].append("Line " + str(row_number+1) + " - no Description")
#         if not type_of_identifier:
#             lists_errors['Critical'].append("Line " + str(row_number+1) + " - no Type of identifier")
#             critical += 1
#         if(extended_type_of_identifier):
#             lists_errors['Critical'].append("Line " + str(row_number+1) + "- no Extended Type of Identifier. ",\
#             + "This field is required since you have selected a GPL identifier in the previoyus column")
#             critical += 1
#         if not parent_list_identifier:
#             lists_errors['Info'].append("Line " + str(row_number+1) + " - no ListParentID")
#         if not child_list_identifier:
#             lists_errors['Info'].append("Line " + str(row_number+1) + " - no ListChildID")
    
#     def is_list_row(row_value, row_number):
#         if is_empty(row_value):
#             print"True"
#         else:
#             print "Flase"
#         if is_empty(row_value): 
#             is_list_error(  (row_value[0]),\
#                             is_list_associated_strategy_identifier((row_value[1])),\
#                             (row_value[2]),\
#                             (row_value[3]),\
#                             (row_value[4]),\
#                             is_list_extended_type_of_identifier((row_value[5]), (row_value[4])),\
#                             (row_value[6]),\
#                             (row_value[7]),\
#                             row_number)
            
#             if(str(row_value[0]) and str(row_value[8]) == "Yes"):
#                 lists_identifiers.append(str(row_value[0]))
#                 for i in range(len(has_identifier)):
#                     if has_identifier[i][2] == (row_value[1]):
#                         has_identifier[i][3] += (row_value[0])
      
#     def lists_sheet(lists):
#         for row_number in range(5, lists.nrows):
#             is_list_row(get_unicode_to_str(lists.row_values(row_number, start_colx=0, end_colx=None)) , row_number)

# #idlist sheet

#     def is_idList_identifier(col_value_identifier):
#         return col_value_identifier not in lists_identifiers
    
#     def is_idList_list(col_value_list):
#         return len(col_value_list) == 0
        
#     def is_idList_error(identifier, idList, col_number):
#         global critical
#         if(identifier):
#             idLists_errors['Critical'].append("Column " + str(col_number+1) + " in your idLists Sheet has no known Identifier")
#             critical += 1
#         if(idList):
#             idLists_errors['Critical'].append("Column " + str(col_number+1) + " in your idLists Sheet has no List associated with")
    
#     def is_idList_row(col_value, col_number):
#         #print col_value[1:]
#         if is_empty(col_value): 
#             is_idList_error(is_idList_identifier((col_value[0])),\
#                                  is_idList_list(col_value[1:]), 
#                                  col_number)
#             if(is_idList_identifier(col_value[0]) == False):
#                 idLists_identifiers.append(str(col_value[0]))
    
#     def get_absent_identifier_in_idLists():
#         absent_identifier_in_idList_sheet = []
#         for identifier in idLists_identifiers:
#             if identifier not in lists_identifiers:
#                 absent_identifier_in_idList_sheet.append(identifier)
                
#         return absent_identifier_in_idList_sheet
        
#     def get_absent_identifier_in_Lists(): 
#         absent_identifier_in_lists_sheet = []
#         for identifier in lists_identifiers:
#             if identifier not in idLists_identifiers:
#                 absent_identifier_in_lists_sheet.append(identifier)
                
#         return absent_identifier_in_lists_sheet
    
#     def is_absent_identifier_in_idLists(absent_identifier_in_idList_sheet):
#         return len(absent_identifier_in_idList_sheet) != 0
    
#     def is_absent_identifier_in_lists(absent_identifier_in_lists_sheet):
#         return len(absent_identifier_in_lists_sheet) != 0
    
#     def is_absent_error(bool_absent_identifier_in_idList_sheet,  absent_identifier_in_idList_sheet, bool_absent_identifier_in_lists_sheet, absent_identifier_in_lists_sheet):
#         global critical
#         if(bool_absent_identifier_in_idList_sheet):
#             for identifier in absent_identifier_in_idList_sheet:
#                 idLists_errors['Critical'].append("IdList \"" + str(identifier) + "\" is present in your idList Sheet but is absent in your Lists Sheet ")
#                 critical += 1
#         if(bool_absent_identifier_in_lists_sheet):
#             for identifier in absent_identifier_in_lists_sheet:
#                 idLists_errors['Critical'].append("ListID \"" + str(identifier) + "\" is present in your Lists Sheet but is absent in your idList Sheet" )

#     def idLists_sheet(idLists):

#         for col_number in range(0, idLists.ncols):
#             _list = [str(element).split(".")[0] for element in idLists.col_values(col_number, start_rowx=0, end_rowx=None)]
#             is_idList_row(_list, col_number)

#         absent_list = get_absent_identifier_in_Lists()
#         absent_idList = get_absent_identifier_in_idLists()
        
#         is_absent_error(is_absent_identifier_in_idLists(absent_idList), absent_idList, is_absent_identifier_in_lists(absent_list), absent_list)

#     #Read excel file


#     def is_absent():
#         global critical
#         for i in range(len(has_identifier)):
#             #print has_identifier[i]
#             if not has_identifier[i][1]:
#                 projects_errors['Critical'].append("Project " + str(has_identifier[i][0]) + " has no study associated with")
#                 critical += 1
#             elif not has_identifier[i][2]:
#                 projects_errors['Critical'].append("Project " + str(has_identifier[i][0]) + " has no Strategy associated with")
#                 critical += 1
#             elif not has_identifier[i][3]:
#                 projects_errors['Critical'].append("Project " + str(has_identifier[i][0]) + " has no Lists associated with")
#                 critical += 1

#     try :
#         input_file.seek(0)
#         wb = xlrd.open_workbook(os.path.join(upload_path, tmp_file_name),encoding_override="cp1251")
        
#         # book = xlrd.open_workbook(os.path.join(upload_path, tmp_file_name))
#         # sheet = book.sheet_by_index(0)
#         # print "start"
#         # print sheet.cell(5, 2)  # prints text:u'Andrea Bargnani'
#         # print sheet.cell(5, 2).value
#         # print isinstance(sheet.cell(5, 2).value, basestring) #str(sheet.cell(5, 2).value).encode("utf-8")
#         # print str()
#         # print "end"



#         # print "here"
#         # print wb.cell(5, 2).value
#         # print [x.value for x in wb.sheet_by_index(0).row_values(5)]
#         # with open("/home/clancien/test.txt", 'w') as output:
#         #     for x in wb.sheet_by_index(0).row_values(5):
#         #         output.write(x + "\n")
#         #print wb.biff_version, wb.codepage, wb.encoding

#         #Read project


#         projects = wb.sheet_by_index(0)
#         studies = wb.sheet_by_index(1)
#         strategies = wb.sheet_by_index(2)
#         lists = wb.sheet_by_index(3)
#         idLists=wb.sheet_by_index(4)
#         #print lists

#         projects_sheet(projects)
#         studies_sheet(studies)
#         strategies_sheet(strategies)
#         lists_sheet(lists)
#         idLists_sheet(idLists)
#         is_absent()
#         #print idLists_errors
#         #print has_identifier
#         #print len(has_identifier)
#         #add if
#         #print "critical : " + str(critical)
#         if critical != 0:
#             print "create path"
#             os.remove(os.path.join(upload_path, tmp_file_name))
#         return {'msg':"File checked and uploded !",
#                 'error_project': projects_errors,
#                 'error_study':studies_errors,
#                 'error_strategy':strategies_errors,
#                 'error_list': lists_errors,
#                 'error_idList':idLists_errors,
#                 'critical':str(critical),
#                 'file': os.path.join(upload_path, tmp_file_name),
#                 'status':'0' }
        
#     except:
#         logger.warning("Error - Read excel file")
#         logger.warning(sys.exc_info())
#         return {'msg':'An error occurred while saving your file. If the error persists please contact TOXsIgN support ','status':'1'}



@view_config(route_name='checkData', renderer='json', request_method='POST')
def checkData(request):
    session_user = is_authenticated(request)
    if session_user is None:
        return 'HTTPForbidden()'

    input_file = None
    form = json.loads(request.body, encoding=request.charset)
    data = form['data']


    projects_errors = {'Critical':[],'Warning':[],'Info':[]}
    strategies_errors = {'Critical':[],'Warning':[],'Info':[]}
    lists_errors = {'Critical':[],'Warning':[],'Info':[]}


    listprojectID =["Root","GUP0","GUP1","GUP2","GUP3","GUP4","GUP5","GUP6","GUP7","GUP8","GUP9","GUP10","GUP11","GUP12","GUP13","GUP14","GUP15","GUP16","GUP17","GUP18","GUP19","GUP20","GUP21","GUP22","GUP23","GUP24","GUP25","GUP26","GUP27","GUP28","GUP29","GUP30","GUP31","GUP32","GUP33","GUP34","GUP35","GUP36","GUP37","GUP38","GUP39","GUP40","GUP41","GUP42","GUP43","GUP44","GUP45","GUP46","GUP47","GUP48","GUP49","GUP50","GUP51","GUP52","GUP53","GUP54","GUP55","GUP56","GUP57","GUP58","GUP59","GUP60","GUP61","GUP62","GUP63","GUP64","GUP65","GUP66","GUP67","GUP68","GUP69","GUP70","GUP71","GUP72","GUP73","GUP74","GUP75","GUP76","GUP77","GUP78","GUP79","GUP80","GUP81","GUP82","GUP83","GUP84","GUP85","GUP86","GUP87","GUP88","GUP89","GUP90","GUP91","GUP92","GUP93","GUP94","GUP95","GUP96","GUP97","GUP98","GUP99","GUP100"]

    parentProjectID=[]
    projectID=[]
    root=[]

    listID=[]


    associatedProjectID=[]
    _input={}
    _output={}

    global isEmpty
    isEmpty=True

    global critical
    critical=0

    


    def project_sheet(projects):#list[0]
        for index in range(1, len(projects[0])):
            """
                0 : Project ID(s)
                1 : Parent project ID
                2 : Contributors (comma or semicolon separated)
                3 : Title
                4 : Description
                5 : Project’s controlled vocabularies (please paste the text from the ontology blabla)
                6 : Crosslink(s) (comma or semicolon separated)
                7 : Additional Information
                8 : PubMedID(s)  (comma or semicolon separated)

            """
            is_project( [projects[0][index],\
                        projects[1][index],\
                        projects[2][index],\
                        projects[3][index],\
                        projects[4][index],\
                        projects[5][index],\
                        projects[6][index],\
                        projects[7][index],\
                        projects[8][index]],
                        index)


    def is_not_empty(_list):

        for element in _list[1:]:
            if element != "":
                return True
        return False

    def is_project(project, index):
        global isEmpty
        if is_not_empty(project):
            has_project_error(project, str(xlsxwriter.utility.xl_col_to_name(index)))

            projectID.append(project[0])
            if project[1] != "":
                parentProjectID.append(project[1])

            if isEmpty:
                isEmpty=False

    def is_not_ProjectID(identifiant):
        if identifiant not in listprojectID:
            return True
        return False

    def has_project_error(project, index):
            """Si il existe des erreurs, c'est erreurs sont consignés dans le dico projects_errors"""
            global critical
            if not project[0]: # projectID
                projects_errors['Critical'].append("Column " + index + " - no ProjectID")
                critical += 1

            if not project[1]: # Parent project ID
                projects_errors['Critical'].append("Column " + index + " -  no Parent ProjectID")
                critical += 1

            if project[1] == "Root":
                root.append(project[0])

            if project[0] == project[1]:
                projects_errors['Critical'].append("Column " + index + " -  Parent ProjectID can't be identical with ProjectID")
                critical += 1

            if is_not_ProjectID(project[1]):
                projects_errors['Critical'].append("Column " + index + " -  no Parent ProjectID Found")
                critical += 1

            if not project[2]: #Contributors (comma or semicolon separated)
                projects_errors['Info'].append("Column " + index + " - no Contributor(s)")

            if not project[3]: # Title
                projects_errors['Critical'].append("Column " + index + " -  no Title")
                critical += 1
            
            if not project[4]: #Description
                projects_errors['Warning'].append("Column " + index + " -  no Description")

            if not project[5]: #Project’s controlled vocabularies (please paste the text from the ontology blabla)
                projects_errors['Warning'].append("Column " + index + " -  no Ontologies")

            if not project[6]: #Crosslink(s) (comma or semicolon separated)
                projects_errors['Info'].append("Column " + index + " - no Crosslink(s)")

            if not project[7]: #Additional Information
                projects_errors['Info'].append("Column " + index + " - no Additional Information")

            if not project[8]:  #PubMedID(s)  (comma or semicolon separated)
                projects_errors['Warning'].append("Column " + index + " -  no PubMed ID")

    def projectHasStrategy():
        global critical
        for project in projectID:
            if project not in associatedProjectID:
                projects_errors['Critical'].append("Column " + str(xlsxwriter.utility.xl_col_to_name(int(project[3:]))) +" - no Strategy Associated with this ProjectID")
                critical += 1

    def list_sheet(_list): # list[2]
        """ 
            0 : List ID(s)
            1 : Title
            2 : Description
            3 : Results and interpretation
            4 : List’s controlled vocabularies (please paste the text from the ontology blabla) gene meiotique
            5 : Database(onglet)
            6 : Additional Information
            7 : Make it available for comparison!
            8 : FileName"""
        for index in range(1,len(_list[2])):
            is_list([_list[0][index],\
                    _list[1][index],\
                    _list[2][index],\
                    _list[3][index],\
                    _list[4][index],\
                    _list[5][index],\
                    _list[6][index],\
                    _list[7][index],\
                    _list[8][index]],
                    index)

    def is_list(_list, index):
        global isEmpty
        if is_not_empty(_list):
            has_list_error(_list , str(xlsxwriter.utility.xl_col_to_name(index)))
            listID.append(_list[0])

            if isEmpty:
                isEmpty=False

    def has_list_error(_list , index):
        global critical

        if not _list[0]: #List ID(s)
            lists_errors['Critical'].append("Column " + index + " - no ListID")
            critical += 1
        if not _list[1]: # Title
            lists_errors['Critical'].append("Column " + index + " - no Title")
            critical += 1

        if not _list[2]: #Description
            lists_errors['Warning'].append("Column " + index + " - no Description")

        if not _list[3]: # Results and interpretation
            lists_errors['Warning'].append("Column " + index + " - no Results and interpretation")

        if not _list[4]: #List’s controlled vocabularies (please paste the text from the ontology blabla) gene meiotique
            lists_errors['Warning'].append("Column " + index + " - no Ontologies")

        if not _list[5]: #Database(onglet)
            lists_errors['Critical'].append("Column " + index + " - no Database")
            critical += 1

        if not _list[6]: #Additional Information
            lists_errors['Info'].append("Column " + index + " - no Additional Informations")

        if not _list[7] and _list[7] != "Yes" and _list[7] != "No": #Make it available for comparison!
            lists_errors['Critical'].append("Column " + index + " - no Comparaison available. ('Yes' or 'No')")
            critical += 1

        if _list[7] == "Yes" and not _list[8]:
            lists_errors['Critical'].append("Column " + index + " - no Filename")
            critical += 1


    def allListAssociatedWithStrategy():
        global critical
        comparaison = set(itertools.chain.from_iterable(_input.values())).union(set(itertools.chain.from_iterable(_output.values())))
        for onelist in listID:
            if onelist not in comparaison:
                lists_errors['Critical'].append("Column " + str(xlsxwriter.utility.xl_col_to_name(int(onelist[3:]))) + " - no Strategy are associated with this ListID : " + str(onelist))
                critical += 1

    def strategy_sheet(strategy): # list[1]
        """ 
            0 : Strategy ID(s)
            1 : Associated project ID(s)
            2 : Input list ID(s) (comma or semicolon separated)
            3 : Output list ID(s) (comma or semicolon separated)
            4 : Title
            5 : Material and methods
            6 : Strategy’s controlled vocabularies (please paste the text from the ontology blabla)
            7 : Additional Information"""

        for index in range (1, len(strategy[0])):
            is_strategy( [strategy[0][index],\
                                strategy[1][index],\
                                strategy[2][index],\
                                strategy[3][index],\
                                strategy[4][index],\
                                strategy[5][index],\
                                strategy[6][index],\
                                strategy[7][index]],
                                index)

    def is_strategy(strategy, index):
        global isEmpty
        if is_not_empty(strategy):
            has_strategy_error(strategy, str(xlsxwriter.utility.xl_col_to_name(index)))
            associatedProjectID.append(strategy[1])

            if len(strategy[2].split(',')) == 0:
                _input[str(xlsxwriter.utility.xl_col_to_name(index))] = ""
            else:
                if strategy[2] == 'Root':
                    _input[str(xlsxwriter.utility.xl_col_to_name(index))] = strategy[2]
                else:
                    _input[str(xlsxwriter.utility.xl_col_to_name(index))] = strategy[2].split(',')

            if len(strategy[3].split(',')) == 0:
                _output[str(xlsxwriter.utility.xl_col_to_name(index))] = ""
            else:
                _output[str(xlsxwriter.utility.xl_col_to_name(index))] = strategy[3].split(',')

            if isEmpty:
                isEmpty=False

    def error_inputOrOutput(_list):
        if _list == "":
            return []
        else:
            newList=_list.split(",")
            elementNotFound=[]
            for element in newList:
                if element not in listID:
                    elementNotFound.append(element)
            return elementNotFound
    def twoListInAndOut(_input,_output):
        elements=[]
        for element in _input.split(','):
            if element in _output.split(','):
                elements.append(element)
        return elements

    def is_root(associatedProjectID):
        if associatedProjectID in root:
            return True
        else:
            return False

    def has_strategy_error(strategy, index):
        global critical
        if not strategy[0]: # Strategy ID(s)
            strategies_errors['Critical'].append("Column " + index + " - no StrategyID")
            critical += 1

        if not strategy[1]: # Associated project ID(s)
            strategies_errors['Critical'].append("Column " + index + " - no Associated Project ID")
            critical += 1

        if is_not_ProjectID(strategy[1]):
            strategies_errors['Critical'].append("Column " + index + " - no Associated Project ID Found in Project Sheet")
            critical += 1

        if not strategy[2]: #Input list ID(s) (comma or semicolon separated)
            strategies_errors['Critical'].append("Column " + index + " - no Input list ID(s)")
            critical += 1

        if not strategy[3]: # Output list ID(s) (comma or semicolon separated)
            strategies_errors['Critical'].append("Column " + index + " - no Output list ID(s)")
            critical += 1

        if is_root(strategy[1]):
            if strategy[2] != "Root":
                strategies_errors['Critical'].append("Column " + index + " Associated Project ID is root. So your Input list ID(s) have to be equal to Root")
                critical += 1

            elementNotFoundInInput =  error_inputOrOutput(strategy[3])

            if len(elementNotFoundInInput) != 0:
                for element in elementNotFoundInInput:
                    strategies_errors['Critical'].append("Column " + index + " - Output Lists ID(s) : " + str(element) + " - not defined in your lists sheet")
                    critical += 1

        else: # Regarder si chaque list dans Input est bien present dans le feuille Lists (idem pour output)
              # Regarder si liste presente a la fois dans input et ouput si cest le cas error

            elementNotFoundInInput =  error_inputOrOutput(strategy[2])

            if len(elementNotFoundInInput) != 0:
                for element in elementNotFoundInInput:
                    print 'here',element
                    strategies_errors['Critical'].append("Column " + index + " - " + str(element) + " Input Lists ID(s) - not defined in your lists sheet")
                    critical += 1

            elementNotFoundInInput =  error_inputOrOutput(strategy[3])

            if len(elementNotFoundInInput) != 0:
                for element in elementNotFoundInInput:
                    strategies_errors['Critical'].append("Column " + index + " - Output Lists ID(s) : " + str(element) + " - not defined in your lists sheet")
                    critical += 1

            elements = twoListInAndOut(strategy[2],strategy[3])

            if len(elements) != 0:
                for element in elements:
                    strategies_errors['Critical'].append("Column " + index + " - " + str(element) + " - found in your input and output lists ID")
                    critical += 1

        if not strategy[4]: #Title
            strategies_errors['Critical'].append("Column " + index + " - no Title")
            critical += 1

        if not strategy[5]: #Material and methods
            strategies_errors['Warning'].append("Column " + index + " - no Material and methods")

        if not strategy[6]: # Strategy’s controlled vocabularies (please paste the text from the ontology blabla)
            strategies_errors['Warning'].append("Column " + index + " - no Ontologies")

        if not strategy[7]: # Additional Information
            strategies_errors['Info'].append("Column " + index + " - no Additional Information")


    try:
        project_sheet(data[0])
        list_sheet(data[1])
        strategy_sheet(data[2])
        projectHasStrategy()
        allListAssociatedWithStrategy()
        if isEmpty:
            return{'empty' : "You have no Data!"}
        else:
            return {'project' : projects_errors, 'strategy' : strategies_errors , 'list' : lists_errors , 'critical' : critical}

    except:
        logger.warning("Error - Check Data (Create new)")
        logger.warning(sys.exc_info())
        return {'msg' : 'An error has occured. Please contact the administrator of GeneUlike'}



@view_config(route_name='canSubmit', renderer='json', request_method='POST')
def canSubmit(request):
    session_user = is_authenticated(request)
    if session_user is None:
        return 'HTTPForbidden()'

    #print 'herer'
    form=json.loads(request.body, encoding=request.charset)

    for (key, values) in form['objectFiles'].items():
        if values['status'] != 'success':
            return {'canSubmit' : False}

    return {'canSubmit' : True}


class Ontology():
    """ use to get all paernt and synonyms from a string of ontology
    
        Example : "CHEBI:phosphatoquinone A;NCBITAXON:Rattus,Rattus Novergicus;"
            
    """


    def __init__(self, ontology): #string ontology can be project, strategy or list
        self.ontology = ontology
        self.dictOntology = self.stringToDict()
        self.REST_URL = "http://data.bioontology.org"
        self.API_KEY = "27f3a22f-92f8-4587-a884-e81953e113e6"

        

    def stringToDict(self):
        
        if self.ontology == "":
            return {}

        dico={}
        for item in self.ontology.split(";")[:-1]:
            dico[item.split(":")[0]]=item.split(":")[1].split(',')

        return dico

    def get_json(self, url):
        
        try:

            opener = urllib2.build_opener()
            opener.addheaders = [('Authorization', 'apikey token=' + self.API_KEY)]
            return json.loads(opener.open(url).read())
        except:
            print "Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno)
            print sys.exc_info()

    

    def get_Ontology(self):
        """From label get synonym and parent"""
        syn = ""
        lab = ""
        try:
            preflabel= self.stringToDict()
            for key, value in preflabel.items():
                syn += key + ":"
                lab += key +":"
                for val in value: #val is preflabel
                    obj = self.get_Object(val, self.get_json(self.REST_URL + "/search?q=" + val.replace(" ","+")+'&ontologies=' + key)['collection'])
                    synonyme, label = self.get_Parent(obj)
                    syn += "/".join(synonyme) + ";"
                    lab += "/".join(label) + ";"
            return syn[:-1], lab[:-1]

        except:
            print "Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno)
            print sys.exc_info()

    def get_Object(self, preflabel, dictionnary): # dictionnary contains all result from our match
        """ retrieve our object which match our preflabel """

        try:
            for obj in  dictionnary:
                if obj['prefLabel'] == preflabel:
                    return obj
        except:
            print "Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno)
            print sys.exc_info()




    def get_Parent(self, obj):
        # getParent : get all parents labels and synonyms for a selected term
        # obj : selected object from NCBO API
        # WARNING: works only from child to parent (one paent by child)
        # RETURN label : list of all label and synonyms (including selected term label & synonym)
        try:
            url = obj["links"]['parents']
            label = []
            synonym=[]
            label.append(obj["prefLabel"])
            if "synonym" in obj.keys():
                obj['synonym'] != []

                if obj['synonym'] != []:
                    t0 = time.time()
                    syno=""
                    for syn in obj['synonym']:
                        syno+= syn + ','

                    synonym.append(syno[:-1])
                    
                
                else:
                    synonym.append('-')
            else:

                synonym.append('-')


            page = self.get_json(url)

            while page != []:

                for result in page :

                    label.append(result['prefLabel'])
                    if "synonym" in obj.keys():

                        if obj['synonym'] != []:
                            syno=""
                            for syn in obj['synonym']:
                                syno+= syn + ','

                            synonym.append(syno[:-1])
                        
                        else:
                            synonym.append('-')
                    else:
                        synonym.append('-')
                    url = result["links"]['parents']
                    page = self.get_json(url)

            return synonym,label

        except:
            print "Exception at the line : {}".format(sys.exc_info()[-1].tb_lineno)
            print sys.exc_info()


# def getParent(obj):
#         # getParent : get all parents labels and synonyms for a selected term
#         # obj : selected object from NCBO API
#         # WARNING: works only from child to parent (one paent by child)
#         # RETURN label : list of all label and synonyms (including selected term label & synonym)
#         url = obj["links"]['parents']
#         label = []
#         label.append(obj["prefLabel"])
#         if obj['synonym'] != []:
#                     label.extend(obj['synonym'])
#         page = get_json(url)
#         while page != []:
#             for result in page :
#                 label.append(result['prefLabel'])
#                 if result['synonym'] != []:
#                     label.extend(result['synonym'])
#                 url = result["links"]['parents']
#                 page = get_json(url)
#         return label

#     def get_json(url):
#         opener = urllib2.build_opener()
#         opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
#         return json.loads(opener.open(url).read())

#     def stringToDict(string):
#         if string == "":
#             return {}

#         dico={}
#         for item in string.split(";")[:-1]:
#             dico[item.split(":")[0]]=item.split(":")[1].split(',')

#         return dico

#     def dictToString(dico):

#         if not bool(dico): #if dico is empty
#             return ""

#         newString="" 

#         for key, value in dico.items():
#             newString += str(key) + ":" + ",".join(value) +";"
#         return newString

# #######################################################################################################################


#     REST_URL = "http://data.bioontology.org"
#     API_KEY = "27f3a22f-92f8-4587-a884-e81953e113e6"
#     form = json.loads(request.body, encoding=request.charset)

#     if 'label' in form:
#         print 'here labellllll'
#         #print getParent(form['label'])

#     elif 'stringToDict' in form:
#         return [stringToDict(form['string'])]

#     elif 'dictToString' in form:
#         return [dictToString(form['dico'])]
        
#     else:
#         term = form['search'].replace(' ','+') #%20
#         database = form['database']
#         search_results = []
#         search_results.append(get_json(REST_URL + "/search?q=" + term+'&ontologies=' + database)['collection'])

#         return search_results



class Project:

    compteur_project=0
    def __init__(self, parent_project_id, contributors, title,\
                 description, ontologies, crosslink, add_info, \
                 pubmed_id, filepathExcel, last_update, submission_date, author, identifiant ):

        self.project_id = "GUP" + str(Project.compteur_project)
        self.parent_project_id = parent_project_id
        self.project_parent = ""
        self.project_child = ""
        self.strategies_id = ""
        self.output_lists_id = ""
        self.contributors = contributors
        self.title = title
        self.description = description
        self.ontologies = ontologies
        self.crosslink = crosslink
        self.add_info = add_info
        self.pubmed_id = pubmed_id
        self.filepathExcel = filepathExcel
        self.status= "private"
        self.last_update = last_update
        self.submission_date = submission_date
        self.author = author
        self.identifiant = identifiant
        self.tags = ""
        Project.compteur_project += 1


    def lire(self):
        pprint.pprint({
                            'project_id'            :   self.project_id,
                            'parent_project_id'     :   self.parent_project_id,
                            'project_parent'        :   self.project_parent,
                            'project_child'         :   self.project_child,
                            'strategies_id'         :   self.strategies_id,
                            'contributors'          :   self.contributors,
                            'title'                 :   self.title,
                            'description'           :   self.description,
                            'ontologies'            :   self.ontologies,
                            'crosslink'             :   self.crosslink,
                            'add_info'              :   self.add_info,
                            'pubmed_id'             :   self.pubmed_id,
                            'filepathExcel'         :   self.filepathExcel,
                            'status'                :   self.status,
                            'last_update'           :   self.last_update,
                            'submission_date'       :   self.submission_date,
                            'author'                :   self.author,
                            'identifiant'           :   self.identifiant,
                            'tags'                  :   self.tags
            }, width=1)


    def get_dico(self):

        syn, lab = Ontology(self.ontologies).get_Ontology()

        return {
                    'project_id'            :   self.project_id,
                    'parent_project_id'     :   self.parent_project_id,
                    'project_parent'        :   self.project_parent,
                    'project_child'         :   self.project_child,
                    'strategies_id'         :   self.strategies_id,
                    'contributors'          :   self.contributors,
                    'title'                 :   self.title,
                    'description'           :   self.description,
                    'ontologies'            :   self.ontologies,
                    'ontologiesSynonym'     :   syn,
                    'ontologiesLabel'       :   lab,
                    'crosslink'             :   self.crosslink,
                    'add_info'              :   self.add_info,
                    'pubmed_id'             :   self.pubmed_id,
                    'filepathExcel'         :   self.filepathExcel,
                    'status'                :   self.status,
                    'last_update'           :   self.last_update,
                    'submission_date'       :   self.submission_date,
                    'author'                :   self.author,
                    'identifiant'           :   self.identifiant,
                    'tags'                  :   self.tags
        }

    






class Strategy:

    compteur_strategy=0
    def __init__(   self, associated_project_id, input_list_id, output_list_id, title,\
                    material_and_method, ontologies, add_info, \
                    filepathExcel, last_update, submission_date, author, identifiant ):

        self.strategy_id = "GUS" + str(Strategy.compteur_strategy)
        self.associated_project_id = associated_project_id
        self.input_list_id = input_list_id
        self.output_list_id = output_list_id
        self.title = title
        self.material_and_method = material_and_method
        self.ontologies = ontologies

        self.add_info = add_info

        self.filepathExcel = filepathExcel

        self.status= "private"
        self.last_update = last_update
        self.submission_date = submission_date
        self.author = author
        self.identifiant = identifiant
        self.tags = ""
        Strategy.compteur_strategy += 1

        self.project_parent = ""

    def lire(self):

        pprint.pprint({
                        'strategy_id'             :   self.strategy_id,
                        'associated_project_id'   :   self.associated_project_id,
                        'project_parent'          :   self.project_parent,
                        'input_list_id'           :   self.input_list_id,
                        'output_list_id'          :   self.output_list_id,
                        'title'                   :   self.title,
                        'material_and_method'     :   self.material_and_method,
                        'ontologies'              :   self.ontologies,
                        'add_info'                :   self.add_info,
                        'filepathExcel'           :   self.filepathExcel,
                        'status'                  :   self.status,
                        'last_update'             :   self.last_update,
                        'submission_date'         :   self.submission_date,
                        'author'                  :   self.author,
                        'identifiant'             :   self.identifiant,
                        'tags'                    :   self.tags
        },width=1)


    def get_dico(self):

        syn, lab = Ontology(self.ontologies).get_Ontology()

        return {
                    'strategy_id'             :   self.strategy_id,
                    'associated_project_id'   :   self.associated_project_id,
                    'project_parent'          :   self.project_parent,
                    'input_list_id'           :   ";".join(self.input_list_id),
                    'output_list_id'          :   ";".join(self.output_list_id),
                    'title'                   :   self.title,
                    'material_and_method'     :   self.material_and_method,
                    'ontologies'              :   self.ontologies,
                    'ontologiesSynonym'       :   syn,
                    'ontologiesLabel'         :   lab,
                    'add_info'                :   self.add_info,
                    'filepathExcel'           :   self.filepathExcel,
                    'status'                  :   self.status,
                    'last_update'             :   self.last_update,
                    'submission_date'         :   self.submission_date,
                    'author'                  :   self.author,
                    'identifiant'             :   self.identifiant,
                    'tags'                    :   self.tags
        }


class List:

    compteur_list=0
    def __init__(   self, title, description, results_and_interpretation,\
                    ontologies, database, add_info, make_it_available, filepathExcel, \
                    filepathList, last_update, submission_date, author, identifiant ):

        self.list_id = "GUL" + str(List.compteur_list)
        self.title = title
        self.description = description
        self.results_and_interpretation = results_and_interpretation
        self.ontologies = ontologies
        self.database = database
        self.add_info = add_info
        self.make_it_available = make_it_available
        self.filepathExcel = filepathExcel
        self.filepathList = filepathList
        self.filepathListConvert= ""

        self.status= "private"
        self.last_update = last_update
        self.submission_date = submission_date
        self.author = author
        self.identifiant = identifiant
        self.tags = ""
        List.compteur_list += 1

        self.strategy_id=""
        self.strategy_output_id=""  #siblings
        self.project_id=""
        self.project_parent=""  #path



    def lire(self):

        pprint.pprint({
                        'list_id'                     :       self.list_id,
                        'title'                       :       self.title,
                        'description'                 :       self.description,
                        'results_and_interpretation'  :       self.results_and_interpretation,
                        'ontologies'                  :       self.ontologies,
                        'database'                    :       self.database,
                        'add_info'                    :       self.add_info,
                        'make_it_available'           :       self.make_it_available,
                        'filepathExcel'               :       self.filepathExcel,
                        'filepathList'                :       self.filepathList,
                        'filepathListConvert'         :       self.filepathListConvert,
                        'status'                      :       self.status,
                        'last_update'                 :       self.last_update,
                        'submission_date'             :       self.submission_date,
                        'author'                      :       self.author,
                        'identifiant'                 :       self.identifiant,
                        'tags'                        :       self.tags,
                        'strategy_id'                 :       self.strategy_id,
                        'strategy_output_id'          :       self.strategy_output_id,
                        'project_id'                  :       self.project_id,
                        'project_parent'              :       self.project_parent
            },width=1)

    def get_dico(self):

        syn, lab = Ontology(self.ontologies).get_Ontology()

        return {
                        'list_id'                     :       self.list_id,
                        'title'                       :       self.title,
                        'description'                 :       ";".join(self.description),
                        'results_and_interpretation'  :       ";".join(self.results_and_interpretation),
                        'ontologies'                  :       self.ontologies,
                        'ontologiesSynonym'           :       syn,
                        'ontologiesLabel'             :       lab,
                        'database'                    :       self.database,
                        'add_info'                    :       self.add_info,
                        'make_it_available'           :       self.make_it_available,
                        'filepathExcel'               :       self.filepathExcel,
                        'filepathList'                :       self.filepathList,
                        'filepathListConvert'         :       self.filepathListConvert,
                        'status'                      :       self.status,
                        'last_update'                 :       self.last_update,
                        'submission_date'             :       self.submission_date,
                        'author'                      :       self.author,
                        'identifiant'                 :       self.identifiant,
                        'tags'                        :       self.tags,
                        'strategy_id'                 :       self.strategy_id,
                        'strategy_output_id'          :       ";".join(self.strategy_output_id),
                        'project_id'                  :       self.project_id,
                        'project_parent'              :       self.project_parent
        }


"""We need to reconstruct the association between Super Project and project 
    example :
    Each node is equal to a tuple : ( parent_project_id, project_id )

                                           (Root, GPR1)         (Root, GPR7)
                                               /                     |
                                              /                      |
                                             /                       |
                                            /                        |
                                           /                         |
                                          /                          |
                                         /                           |
                                   (GPR1,GPR2)                  (GPR7, GPR8)
                                       /\ 
                                      /  \
                                     /    \
                                    /      \
                                   /        \
                                  /          \
                                 /            \
        (GRP3, GPR9)-------(GPR2,GRP3)      (GPR2, GPR4)
                               /\
                              /  \
                             /    \
                            /      \
                           /        \
                          /          \
                         /            \
                   (GPR3, GPR5)   (GPR3, GPR6)
                    
    We can have mulitple Root in one Super Project"""
from treelib import Node, Tree
from collections import defaultdict

class Arbre:

    def __init__(self, data_list):
        self.data_list = data_list
        self.tree_dict = defaultdict(Tree) #To understand what is Tree go : http://treelib.readthedocs.io/en/latest/examples.html

        self._root()
        self.for_each_root()
        #self.show()

    def _root(self):
        """ return List of Project which are root  
            and a new Data List without root Project"""

        new_data_list=[]
        i=0
        for index in range(len(self.data_list)):
            if (self.data_list[index]).parent_project_id == 'Root':
                #self.tree_dict["tree"+str(i)] = Tree()
                self.tree_dict["tree"+str(i)].create_node((self.data_list[index]).project_id, (self.data_list[index]).project_id) #root node
                i=i+1
            else:
                new_data_list.append(self.data_list[index])

        self.data_list=new_data_list


    def for_each_root(self):

        for item in self.tree_dict.keys():
            self.create_node_to_root(item)

    def create_node_to_root(self,item):
        boolean=True
        while boolean:
            boolean = self.add_node(item)

    def add_node(self,item):
        boolean=False
        new_data_list=[]
        for child in self.data_list:
            if self.tree_dict[item].contains(child.parent_project_id):
                self.tree_dict[item].create_node(child.project_id, child.project_id, parent=child.parent_project_id)
                boolean=True
            else:
                new_data_list.append(child)
        self.data_list=new_data_list
        return boolean

    def parent_path(self, nodeIdentifier):

        for item in self.tree_dict.keys():
            if self.tree_dict[item].contains(nodeIdentifier):
                boolean=True
                return self.get_parent(nodeIdentifier, item)
                
        
        return False

    def get_parent(self, nodeIdentifier, item):

        if self.is_root(nodeIdentifier, item):
            return nodeIdentifier
        else:
            return  self.get_parent(self.tree_dict[item].parent(nodeIdentifier).identifier,item)+'/'+nodeIdentifier
            # print self.tree_dict[item].parent(nodeIdentifier)
            # print self.tree_dict[item].get_node(nodeIdentifier)
            # path=self.get_parent(self.tree_dict[item].parent(nodeIdentifier),item)+'/'+self.tree_dict[item].get_node(nodeIdentifier).identifier
            # print path
    
    def child_path(self,nodeIdentifier):
        """ Multiple child from one node can exist so mulitple path"""

        for item in self.tree_dict.keys():
            if self.tree_dict[item].contains(nodeIdentifier):
                boolean=True
                return self.get_child(nodeIdentifier, item)

        return False

    def get_child(self, nodeIdentifier,item):
        _list = self.tree_dict[item].subtree(nodeIdentifier).paths_to_leaves()
        paths=""
        for path in _list:
            newPath=""
            for node in path:
                newPath=newPath+node+"/"
            paths = paths+newPath[:-1]+";"
        return paths[:-1]

    def is_root(self, nodeIdentifier, item):
        if self.tree_dict[item].parent(nodeIdentifier) == None:
            return True
        return False

    def show(self):
        for value in self.tree_dict.values():
            value.show()

import unicodedata as ucd

# def file_dataset(request):
#     print "Get Dataset"
#     directory = request.matchdict['dir']
#     downfile = request.matchdict['file']
#     url_file = os.path.join(request.registry.dataset_path,directory,downfile)
#     (handle, tmp_file) = tempfile.mkstemp('.zip')
#     z = zipfile.ZipFile(tmp_file, "w")
#     z.write(url_file,os.path.basename(url_file))
#     z.close()
#     return FileResponse(tmp_file,
#                         request=request,
#                         content_type='application/zip')

@view_config(route_name='createExcelForExport', renderer='json', request_method='POST')
def createExcelForExport(request):

    form=json.loads(request.body, encoding=request.charset)

    data_projects = form['data_projects']
    data_strategies = form['data_strategies']
    data_lists = form['data_lists']
    uid= form['uid']
    filename = uuid.uuid4().hex +".xlsx"
    filepath = os.path.join(request.registry.upload_path, uid, "tmp", filename)

    workbook = xlsxwriter.Workbook(filepath, {'constant_memory': True})

    project_worksheet = workbook.add_worksheet("Project")
    for row in range(len(data_projects)):
        for col in range(len(data_projects[row])):
            project_worksheet.write(row, col, data_projects[row][col])

    strategy_worksheet = workbook.add_worksheet("Strategy")
    for row in range(len(data_strategies)):
        for col in range(len(data_strategies[row])):
            strategy_worksheet.write(row, col, data_strategies[row][col])

    list_worksheet = workbook.add_worksheet("List")
    for row in range(len(data_lists)):
        for col in range(len(data_lists[row])):
            list_worksheet.write(row, col, data_lists[row][col])

    workbook.close()
    return { 'filepath':os.path.join(request.registry.upload_path, uid, "tmp", filename),'uid' : uid, 'tmp': 'tmp', 'filename' : filename}

@view_config(route_name='removeExcel',renderer='json',request_method='GET')
def removeExcel(request):
    print "removeExcel"
    uid = request.matchdict['uid']
    tmp = request.matchdict['tmp']
    filename = request.matchdict['filename']
    
    print os.path.join(request.registry.upload_path,uid,tmp,filename)
    os.remove(os.path.join(request.registry.upload_path,uid,tmp,filename))

@view_config(route_name='exportExcel', request_method='GET')
def exportExcel(request):
    print "herer"
    #upload_path = request.matchdict['upload_path']
    uid = request.matchdict['uid']
    tmp = request.matchdict['tmp']
    filename = request.matchdict['filename']
    filepath= os.path.join(request.registry.upload_path,uid,tmp,filename)



    response = Response(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    response = FileResponse(os.path.abspath(filepath))
    return response

    return FileResponse(filepath,
                         request=request,
                         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    #pprint.pprint(json.loads(request.body, encoding=request.charset))
    # from tempfile import NamedTemporaryFile

    # #uuid.uuid4().hex #+".xlsx"
    # # data_projects, data_strategies, data_lists, path, filename
    # print "here"
    # form=json.loads(request.body, encoding=request.charset)
    # #pprint.pprint(form['data_projects'])
    # #pprint.pprint(request.json.loads(request.body))
    # #form=json.loads(request.POST['data'], encoding=request.charset)
    # #pprint.pprint(form)
    # #pprint.pprint(data_projects)
    # #pprint.pprint(request.POST['method'])
    # #form=json.loads(request.POST['params'], encoding=request.charset)

    # #pprint.pprint(form)
    # #return {'data':"ok"} 
    # #path = os.path.join(request.registry.upload_path, form['uid'], "tmp")
    # response = Response(content_type='application/csv')
    # with NamedTemporaryFile(prefix='XML_Export_%s' % datetime.datetime.now(),
    #                         suffix='.xml', delete=True) as f:
    #     f.write('test')
    #     # this is where I usually put stuff in the file
    #     response.app_iter = f
    #     response.headers['Content-Disposition'] = ("attachment; filename=Export.xml")
    #     return json.dumps({'response': response.app_iter})

    # filename = "toto"#uuid.uuid4().hex #+".xlsx"


    # #your view logic here

    # # create a workbook in memory
    # data_projects = form['data_projects']
    # data_strategies = form['data_strategies']
    # data_lists = form['data_lists']
    # output = StringIO.StringIO()

    # workbook = xlsxwriter.Workbook(output)

    # project_worksheet = workbook.add_worksheet("Project")
    # for row in range(len(data_projects)):
    #     for col in range(len(data_projects[row])):
    #         project_worksheet.write(0, 0, data_projects[row][col])

    # strategy_worksheet = workbook.add_worksheet("Strategy")
    # for row in range(len(data_strategies)):
    #     for col in range(len(data_strategies[row])):
    #         strategy_worksheet.write(0, 0, data_strategies[row][col])

    # list_worksheet = workbook.add_worksheet("List")
    # for row in range(len(data_lists)):
    #     for col in range(len(data_lists[row])):
    #         list_worksheet.write(0, 0, data_lists[row][col])

    # workbook.close()

    # # construct response
    # output.seek(0)
    # #return {"msg":"ok"}
    # return {"file" : output.read()}
    # FileResponse(output.read(),
    #                     request=request)
    #                     #content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # response = HttpResponse(output.read(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    # response['Content-Disposition'] = "attachment; filename="+ filename
    # return response



    # workbook  = xlsxwriter.Workbook(filename)

    # path_filename = os.path(os.join(path,filename))
     
    # project_worksheet = workbook.add_worksheet("Project")
    # for row in range(len(data_projects)):
    #     for col in range(len(data_project[row])):
    #         project_worksheet.write(0, 0, data_project[row][col])

    # strategy_worksheet = workbook.add_worksheet("Strategy")
    # for row in range(len(data_strategies)):
    #     for col in range(len(data_strategies[row])):
    #         strategy_worksheet.write(0, 0, data_strategies[row][col])

    # list_worksheet = workbook.add_worksheet("List")
    # for row in range(len(data_lists)):
    #     for col in range(len(data_lists[row])):
    #         list_worksheet.write(0, 0, data_lists[row][col])

    # workbook.close()

    # return FileResponse(tmp_file,
    #                      request=request,
    #                      content_type='application/zip')

    # # upload_path = os.path.join(request.registry.upload_path, request.params['uid'], request.params['dataset'])
    # # upload_path = os.path.join(request.registry.upload_path, request.params['uid'], request.params['dataset'])
    # # print upload_path
    # # print "request.registry.upload_path : ", request.registry.upload_path
    # # print "uid : ", request.params['uid']
    # # print "tmp : ", request.params['dataset']

import pandas

class ConvertToEntrezGene():

    def __init__(self, ObjectList,request):
        self.list = ObjectList
        self.filepathList = ObjectList.filepathList
        self.filepathListConvert = ObjectList.filepathListConvert
        self.database = ObjectList.database.split(';')
        self.request=request
        self.identifiers = []
        self.dataframe= None


        self.get_conversion()

    def get_identifiers(self):
        _list=[]
        with open(self.filepathList , 'r') as inputFile:
            for line in inputFile:
                self.identifiers.append(line.split('\n')[0])
        
        self.dataframe = pandas.DataFrame({
                                            'BDID' : list(set(self.identifiers))
                                         })
    def search(self, listID, database):
        
        if database.startswith('GPL'):
            res = list(self.request['GPL'].find({'PLATFORM' : str(database),'BDID':{"$in":list(listID)}},{'EGID' : 1, 'BDID' :1, '_id' :0}))
        
        else:
            res = list(self.request[database].find({'BDID':{"$in" :list(listID)}},{'EGID' : 1, 'BDID' : 1, '_id' :0}))

        not_found=[]
        for elt in res:
            not_found.append(elt['BDID'])
        

        not_found=list(set(listID).symmetric_difference(set(not_found)))  

        return res, not_found

    def loopDatabase(self):
        

        listID = list(self.identifiers)
        resultat = None

        for db in self.database:

            res, not_found = self.search(listID, db)
            resultat = resultat = res
            listID=not_found

        bdid=[]
        egid=[]
        for elt in resultat:
            bdid.append(elt['BDID'])
            egid.append(elt['EGID'])
        self.dataframe = self.dataframe.merge(
                                                 pandas.DataFrame({
                                                                    'BDID' : bdid,
                                                                    'EGID' : egid
                                                                 }),
                                                 how='outer',
                                                 left_on='BDID',
                                                 right_on='BDID',

                                             ).fillna('-')
    def searchInfo(self):
        searchegid = list(self.dataframe['EGID'][ (self.dataframe['EGID'] != '-' )])
        res = list(self.request['GeneInfo'].find(
                                                                {
                                                                    'EGID' :{
                                                                                "$in": searchegid
                                                                            }
                                                                },
                                                                
                                                                {
                                                                    'EGID'          : 1, 
                                                                    'TAXID'         : 1,
                                                                    "SYMBOL"        : 1,
                                                                    "DESCRIPTION"   : 1,
                                                                    "HOMOLOGENE"    : 1,
                                                                    '_id'           : 0
                                                                }
                                                             )
                  )

        egid=[]
        taxid=[]
        symbol=[]
        description=[]
        homologene=[]
        for elt in res:
            egid.append(elt['EGID'])
            taxid.append(elt['TAXID'])
            symbol.append(elt['SYMBOL'])
            description.append(elt['DESCRIPTION'])
            homologene.append(elt['HOMOLOGENE'])

        self.dataframe = self.dataframe.merge(
                                                 pandas.DataFrame({
                                                                    'EGID'        : egid,
                                                                    'TAXID'       : taxid,
                                                                    'SYMBOL'      : symbol,
                                                                    'DESCRIPTION' : description,
                                                                    'HOMOLOGENE'  : homologene
                                                                 }),
                                                 how='left',
                                                 left_on='EGID',
                                                 right_on='EGID',

                                             ).fillna('-')
    def write(self):

        self.dataframe = self.dataframe[['BDID', 'EGID', 'TAXID', 'SYMBOL', 'DESCRIPTION', 'HOMOLOGENE']]
        self.dataframe.to_csv(self.filepathListConvert, header=True, index=None, sep='\t', mode='w')


    def get_conversion(self):
        self.get_identifiers()
        self.loopDatabase()
        self.searchInfo()
        self.write()

        
            

    
# def get_Convert(upload_path):

#         """ajouter une exception pour collections qui sont des entiers naturels positifs"""

#         print "enter get_convert"
#         raw=[]
#         entrez=[]
#         homologene=[]
#         gpl='GPL'

#         for _list in lists:

#             identifiers=_list.identifiers.split(' , ')
#             newIdentifiers = []
           
#             for index in range(len(identifiers)):
#                 if identifiers[index] == 'GPL':
#                     newIdentifiers.append(_list.identifier_extended.split(',')[index])

#                 else:
#                     newIdentifiers.append(identifiers[index])

#             print "newidentfiers : ",newIdentifiers
#             #dico=[]
#             #print _list.list.split(',')

#             #list_identifiers = _list.list.split



#             # t0 = time.time()
#             # list(request.registry.db_mongo[identifiers[index]].find({'BDname' : {"$regex" : str(newIdentifiers[index])},'BDID':{"$in" : _list.list.split(',')}},{'HomoloGene':1, 'BDID' : 1, 'GeneID' : 1 , '_id' :0}))
#             # print time.time() - t0, "seconds wall time"
#             # result=[]
#             # query=list(request.registry.db_mongo['BDname'].find({'BDname' : {"$regex" : str(newIdentifiers[index])},"BDID":{"$nin": _list.list.split(',')}}, {'GeneID' : 1 , '_id' :0}))
#             # for i in query:
#             #     result.append(i['GeneID'])
#             # print str(len(result))

            
#             def search(collection, BDname, _list):

#                 if collection == "GPL":
#                     print BDname
#                     res= list(request.registry.db_mongo[collection].find({'GPLname' : {"$regex" : str(BDname)},'BDID':{"$in":_list}}))#,{'Homologene':1, 'BDID' : 1, 'GeneName':1, 'GeneDescription':1,  'GeneID' : 1 ,'TaxID':1, '_id' :0}))

#                 else:
#                     res = list(request.registry.db_mongo[collection].find({'BDID':{"$in" :_list}},{'HomoloGene':1, 'BDID' : 1, 'GeneID' : 1 , '_id' :0}))
                
#                 not_found=[]
#                 for elt in res:
#                     not_found.append(elt['BDID'])
#                 not_found=list(set(_list).symmetric_difference(set(not_found)))   
#                 # newSearch=[]
#                 # for elt in res:
#                 #     #print elt
#                 #     if elt['GeneID'] not in newSearch:
#                 #         newSearch.append(elt['GeneID'])
#                 # #print newSearch[:5]
#                 # not_found=[]
#                 # for item in _list:
#                 #     if item not in newSearch:
#                 #         not_found.append(str(item))
#                 return res, not_found
                
#             res, not_found =search(identifiers[0], newIdentifiers[0],_list.list.split(','))
#            # print not_found
#             #return
#             if len(identifiers) > 1:
#                 for i in range(1,len(identifiers),1):
#                     if not_found:
#                         break
#                     else:
#                         _res, _not_found= search(identifiers[i], newIdentifiers[i], not_found)
#                     for elt in _res:
#                         res.append(elt)
#                     not_found=_not_found
#                # while next(identifiers) and not_found is :
                    
            
#             with open(os.path.join(upload_path, str(_list.project_id), str(_list.lists_id), str(_list.lists_id))+".txt" , 'w') as output:
#                 for elt in res:
#                     output.write(str(elt['BDID']) + "\t" + str(elt['GeneID']) + "\t" + str(elt['Homologene']) + "\t" + str(elt['GeneName'])+ "\t" + str(elt['GeneDescription'])+ "\t" + str(elt['TaxID'])+"\n" )
#                 for elt in not_found:
#                     output.write(str(elt) + "\t" + "-" + "\t" + "-" +  "\t" + "-" + "\t" + "-" +"\t" + "-" +"\n")

@view_config(route_name='submit', renderer='json', request_method='POST')
def submit(request):
    session_user = is_authenticated(request)
    if session_user is None:
        return 'HTTPForbidden()'

    form=json.loads(request.body, encoding=request.charset)

    data_projects=form['data_projects']
    data_strategies=form['data_strategies'] 
    data_lists=form['data_lists']
    objectFiles=form['objectFiles']

    project_last_new_id={}
    list_last_new_id={}
    user = form['uid']

    dt = datetime.datetime.utcnow()
    date = time.mktime(dt.timetuple())

    projects = []
    projects_location={}
    lists_location={}
    strategies = []
    lists = []

    ####Create excel project
    filename = uuid.uuid4().hex +".xlsx"
    filepathExcel = os.path.join(request.registry.upload_path, user, "tmp", filename)

    workbook = xlsxwriter.Workbook(filepathExcel, {'constant_memory': True})

    project_worksheet = workbook.add_worksheet("Project")
    for row in range(len(data_projects)):
       for col in range(len(data_projects[row])):
           project_worksheet.write(row, col, data_projects[row][col])

    strategy_worksheet = workbook.add_worksheet("Strategy")
    for row in range(len(data_strategies)):
       for col in range(len(data_strategies[row])):
           strategy_worksheet.write(row, col, data_strategies[row][col])

    list_worksheet = workbook.add_worksheet("List")
    for row in range(len(data_lists)):
       for col in range(len(data_lists[row])):
           list_worksheet.write(row, col, data_lists[row][col])
    workbook.close()

    def is_not_empty(_list):

        for element in _list[1:]:
            if element != "":
                return True
        return False
   
    def get_str(string):
        if isinstance(string, float):
            return str(int(string)).encode('utf-8')
        elif string == '':
            return str("").encode('utf-8')
        else:
            return string.encode('utf-8')


    def add_project(data_projects):

        if Project.compteur_project == 0:
            Project.compteur_project = int(request.registry.db_mongo['projects'].find().count())

        for index in range(1,len(data_projects[0])):

            one_project_values = [  data_projects[0][index],
                                    data_projects[1][index],
                                    data_projects[2][index],
                                    data_projects[3][index],
                                    data_projects[4][index],
                                    data_projects[5][index],
                                    data_projects[6][index],
                                    data_projects[7][index],
                                    data_projects[8][index]
                                 ]
            if is_not_empty(one_project_values):

                newProject= Project (   get_str(one_project_values[1]),
                                        get_str(one_project_values[2]),
                                        get_str(one_project_values[3]),
                                        get_str(one_project_values[4]),
                                        get_str(one_project_values[5]),
                                        get_str(one_project_values[6]),
                                        get_str(one_project_values[7]),
                                        get_str(one_project_values[8]),
                                        str(filepathExcel),
                                        str(date),
                                        str(date),
                                        str(user),
                                        get_str(one_project_values[0])
                                    )
 
                project_last_new_id[get_str(one_project_values[0])] = newProject.project_id
                projects.append(newProject)


    def replaceOldParentProjectIDByNEw():
        for project in projects:
            if project.parent_project_id != 'Root':
                project.parent_project_id = project_last_new_id[project.parent_project_id]


    def location():
        for index in range(len(projects)):
            projects_location[projects[index].project_id] = index

    def addChildAndParentPathForProject():
        # self.project_parent = ""
        # self.project_child = ""
        # myTree.parent_path("GPR42") 
        # (myTree.child_path(item).split(";"))[:-1]

        for project in projects:
            parent_path = myTree.parent_path(project.project_id)
            project_child = myTree.child_path(project.project_id)

            if parent_path == project.project_id:
                project.project_parent = "Root"
            else:
                project.project_parent = parent_path

            if project_child == project.project_id:
                project.project_child = "Root"
            else:
                project.project_child = project_child

    def add_strategy(data_strategies):
        if Strategy.compteur_strategy == 0:
            Strategy.compteur_strategy = int(request.registry.db_mongo['strategies'].find().count())

        for index in range(1, len(data_strategies[0])):
            one_strategy_values = [     data_strategies[0][index],
                                        data_strategies[1][index],
                                        data_strategies[2][index],
                                        data_strategies[3][index],
                                        data_strategies[4][index],
                                        data_strategies[5][index],
                                        data_strategies[6][index],
                                        data_strategies[7][index]
                                ]

            if is_not_empty(one_strategy_values):

                strategies.append(Strategy (    get_str(one_strategy_values[1]),
                                                get_str(one_strategy_values[2]).split(','),
                                                get_str(one_strategy_values[3]).split(','),
                                                get_str(one_strategy_values[4]),
                                                get_str(one_strategy_values[5]),
                                                get_str(one_strategy_values[6]),
                                                get_str(one_strategy_values[7]),
                                                str(filepathExcel),
                                                str(date),
                                                str(date),
                                                str(user),
                                                get_str(one_strategy_values[0])
                                            )
                                )

    def replaceOldInputOuputIDByNEw():

        for strategy in strategies:
            newInput=[]
            newOutput=[]

            for item in strategy.input_list_id:
                if item == "Root":
                    newInput.append(item)
                else:
                    newInput.append(list_last_new_id[item])


            strategy.input_list_id=newInput

            for item in strategy.output_list_id:
                if item == "Root":
                    newOutput.append(item)
                else:
                    newOutput.append(list_last_new_id[item])

            strategy.output_list_id=newOutput


    def associateStrategyWithProject():
        """ replace old associated project id by new and add strat id to project.strategies_id and list output"""
        for strategy in strategies:
            ###############################
            #       Add to project        #
            ###############################

            #print strategy.associated_project_id
            strategy.associated_project_id = project_last_new_id[strategy.associated_project_id]
            #print strategy.associated_project_id

            project_location=projects_location[strategy.associated_project_id]

            projects[project_location].strategies_id = projects[project_location].strategies_id + strategy.strategy_id

            #print projects[projects_location[strategy.associated_project_id]].strategies_id

            if projects[project_location].output_lists_id == "":
                projects[project_location].output_lists_id = strategy.output_list_id
            else:
                projects[project_location].output_lists_id = projects[project_location].output_lists_id + ';' +strategy.output_list_id        

            if projects[project_location].project_parent == "":
                strategy.project_parent = "Root"
            else:
                strategy.project_parent = projects[project_location].project_parent

    def associateListWithStrategy():

        ###############################
        #       Add to strategy       #
        ###############################


        # To work need to do Add to error List (see ToDo List)
        for strategy in strategies:
            for item in strategy.output_list_id:

                    lists[lists_location[item]].strategy_id             = strategy.strategy_id

                    lists[lists_location[item]].project_id              = strategy.associated_project_id

                    lists[lists_location[item]].project_parent          = strategy.project_parent
                    lists[lists_location[item]].strategy_output_id      = strategy.output_list_id


    def add_list(data_lists):
        if List.compteur_list == 0:
            List.compteur_list = int(request.registry.db_mongo['lists'].find().count())

        for index in range(1,len(data_lists[0])):
            one_list_values =   [   data_lists[0][index],
                                    data_lists[1][index],
                                    data_lists[2][index],
                                    data_lists[3][index],
                                    data_lists[4][index],
                                    data_lists[5][index],
                                    data_lists[6][index],
                                    data_lists[7][index],
                                    data_lists[8][index]
                                ]

            if is_not_empty(one_list_values):
                if get_str(one_list_values[7]) == 'Yes':
                    filename = objectFiles[one_list_values[8].split('.')[0]]['filepath']

                else:
                    filename=""

                newList = List (    get_str(one_list_values[1]),
                                    get_str(one_list_values[2]).split(','),
                                    get_str(one_list_values[3]).split(','),
                                    get_str(one_list_values[4]),
                                    get_str(one_list_values[5]),
                                    get_str(one_list_values[6]),
                                    get_str(one_list_values[7]),
                                    str(filepathExcel),
                                    str(""),
                                    str(date),
                                    str(date),
                                    str(user),
                                    get_str(one_list_values[0])
                                )

                list_last_new_id[get_str(one_list_values[0])] = newList.list_id

                lists.append(newList)

    def location_list():
        for index in range(len(lists)):
            lists_location[lists[index].list_id] = index

    try:
        add_project(data_projects)
        add_strategy(data_strategies)

        add_list(data_lists)
        location()
        location_list()

        replaceOldParentProjectIDByNEw()
        replaceOldInputOuputIDByNEw() #for each strategy's input and ouput


        myTree = Arbre(projects)
        #myTree.show()
        addChildAndParentPathForProject()

        #pprint.pprint(projects_location)
      
        associateStrategyWithProject()
        associateListWithStrategy()
        

        path = os.path.join(request.registry.upload_path, user, 'dashboard')

        dirname= "-".join(sorted(list(project_last_new_id.values())))
        if not os.path.isdir(os.path.join(path, dirname)):
            os.makedirs(os.path.join(path, dirname))
            os.makedirs(os.path.join(path, dirname, 'raw'))
            os.makedirs(os.path.join(path, dirname, 'convert'))

        #new path for teh excel file in the dashboard directory
        newpathExcel = os.path.join(path, dirname, 'raw', 'ExcelProject_'+filename)

        os.rename(filepathExcel,newpathExcel)


        # rename filepathList and FilepatListConvert 
        # move file pathList to dashboard
        
        for key in objectFiles.keys(): 

            old_filepath=objectFiles[key]['filepath']
            new_filepath=os.path.join(path, dirname, 'raw',objectFiles[key]['identifiant']+ "_" + str(lists[lists_location[list_last_new_id[objectFiles[key]['identifiant']]]].list_id)+ "_" + old_filepath.rsplit('/',1)[1])
            lists[lists_location[list_last_new_id[objectFiles[key]['identifiant']]]].filepathList = new_filepath
            lists[lists_location[list_last_new_id[objectFiles[key]['identifiant']]]].filepathListConvert = os.path.join(path, dirname, 'convert', objectFiles[key]['identifiant']+"_"+str(lists[lists_location[list_last_new_id[objectFiles[key]['identifiant']]]].list_id)+ "_Convert_"  + old_filepath.rsplit('/',1)[1])
            os.rename(old_filepath,new_filepath)

        # rename filepath Excel + for list we convert
        for project in projects:
            project.filepathExcel=newpathExcel

        for strategy in strategies:
            strategy.filepathExcel=newpathExcel

        for _list in lists:
            _list.filepathExcel=newpathExcel
            ConvertToEntrezGene(_list,request.registry.db_mongo)
            #new_filepathExcel
        
        
        ###Add to database 
        ###for better performance include this to previous loop (at the end of the loop)
        for project in projects:
            request.registry.db_mongo['projects'].insert(project.get_dico())


        for strategy in strategies:
            request.registry.db_mongo['strategies'].insert(strategy.get_dico())


        for _list in lists:
            request.registry.db_mongo['lists'].insert(_list.get_dico())
        
        return {'message' : 'Your project has been saved !', 'status':'Success'}
    except:
        return {'message' : 'An error has occured', 'status':'Danger'}

    # upload_path = os.path.join(request.registry.upload_path, user, 'dashboard')
    # for project in projects:
    #     request.registry.db_mongo['projects'].insert(project.get_dico())
    #         #v=os.path.join(upload_path, project.project_id)
    #         #print str(v)
    #     if not os.path.exists(os.path.join(upload_path, project.project_id)):

    #         os.makedirs(os.path.join(upload_path, project.project_id))
    #         print "create project directory"

    # for study in studies:
    #     request.registry.db_mongo['studies'].insert(study.get_dico())

    # for strategy in strategies:
    #     request.registry.db_mongo['strategies'].insert(strategy.get_dico())

    # for _list in lists:
    #     request.registry.db_mongo['lists'].insert(_list.get_dico())
    #         #v=os.path.join(upload_path, project.project_id,_list.lists_id)
    #         #print str(v)
    #     if not os.path.exists(os.path.join(upload_path, _list.project_id,_list.lists_id)):
    #         os.makedirs(os.path.join(upload_path, _list.project_id, _list.lists_id))
    #         #os.rename(os.path.join(upload_path, _list.lists_id, name_file))
    #         #v = get_str(os.path.join(upload_path, _list.project_id, _list.lists_id)) #, namefile))
    #         #print v
    #         #_list.file_path= get_str(os.path.join(upload_path, _list.project_id, _list.lists_id, namefile))
    #         #pprint.pprint(request.registry.db_mongo['lists'].find_one({'project_id' : 'GPR0'}))
    # print "try"
    # #t0 = time.time()
    # get_Convert(upload_path)
    # #print time.time() - t0, "seconds wall time"
    # return {'msg':"File checked and uploded !", 'status':'0'}
    # print "##########################################################"
    # print "Project"
    # print "##########################################################"
    # print ""
    # for project in projects:
    #     project.lire()
    #     print "\n"

    # print ""
    # print "##########################################################"
    # print "Strategy"
    # print "##########################################################"
    # print ""

    # for strategy in strategies:
    #     strategy.lire()
    #     print "\n"

    # print ""
    # print "##########################################################"
    # print "List"
    # print "##########################################################"
    # print ""

    # for _list in lists:
    #     _list.lire()
    #     print "\n"
    
    




    # add_project(data_projects)
    # replaceOldParentProjectIDByNEw()
    # location()
    
    # #pprint.pprint(projects_location)
    # add_strategy(data_strategies)
    # add_list(data_lists)
    # location_list()
    # replaceOldInputOuputIDByNEw() #for each strategy's input and ouput
    # associateStrategyWithProject()
    # associateListWithStrategy()
    
    # myTree = Arbre(projects)
    # myTree.show()
    # addChildAndParentPathForProject()






    # for item in projects:
    #     item.lire()
    # print "Parent"
    # print "GPR42 : " , myTree.parent_path("GPR42") 
    # print "GPR43 : " , myTree.parent_path("GPR43")
    # print "GPR44 : " , myTree.parent_path("GPR44")
    # print "GPR41 : " , myTree.parent_path("GPR41")
    # print "GPR40 : " , myTree.parent_path("GPR40")
    # print "GPR39 : " , myTree.parent_path("GPR39")
    # print "Child"
    # _list= ["GPR40","GPR43","GPR44","GPR41","GPR40", "GPR39"]
    # for item in _list:
    #     paths = (myTree.child_path(item).split(";"))
    #     for path in paths:
    #         print "{} : {}".format(item, path)

    #except:
    #    print "error"

# @view_config(route_name='checkData', renderer='json', request_method='POST')
# def exportToXLXSfile(request)  


import pprint

# class Project:

#     compteur_project= 0
#     def __init__(self,\
#         title,\
#         description,\
#         pubmed,\
#         contributors,\
#         crosslinks,\
#         last_update,\
#         submission_date,\
#         owner,\
#         author,\
#         file_path,\
#         identifiant):

#         self.project_id = "GPR" + str(Project.compteur_project)
#         self.studies_id=[]
#         self.strategies_id=[]
#         self.lists_id=[]
#         self.title = title
#         self.description = description
#         self.pubmed = pubmed
#         self.contributors = contributors
#         self.crosslinks = crosslinks
#         self.last_update = last_update
#         self.submission_date = submission_date
#         self.owner = owner
#         self.author = author
#         self.file_path = file_path
#         self.status= "private"
#         self.tags = ""
#         Project.compteur_project += 1
#         self.id=identifiant

#     def get_dico(self):

#         if len(self.studies_id) == 1:
#             _studies= str(self.studies_id[0])
#         else:
#             _studies= ' , '.join(self.studies_id)

#         if len(self.strategies_id) == 1:
#             _strategies = str(self.strategies_id[0])
#         else:
#             _strategies = ' , '.join(self.strategies_id)

#         if len(self.studies_id) == 1:
#             _studies = str(self.studies_id[0])
#         else:
#             _studies= ' , '.join(self.studies_id)

#         if len(self.lists_id) == 1:
#             _lists = str(self.lists_id[0])
#         else:
#             _lists = ' , '.join(self.lists_id)


#         return {'project_id' : self.project_id,
#                 'studies_id' : _studies,
#                 'strategies_id' : _strategies,
#                 'lists_id' : _lists,
#                 'title' : self.title,
#                 'description' : self.description,
#                 'pubmed' : self.pubmed,
#                 'contributors' : self.contributors,
#                 'crosslinks' : self.crosslinks,
#                 'last_update' : self.last_update,
#                 'submission_date' : self.submission_date,
#                 'owner' : self.owner,
#                 'author' : self.author,
#                 'file_path' : self.file_path,
#                 'status' : self.status,
#                 'tags' : self.tags,
#     }

#     def lire(self):
#         pprint.pprint({'project_id' : self.project_id,
#                 'studies_id' : self.studies_id,
#                 'strategies_id' : self.strategies_id,
#                 'lists_id' : self.lists_id,
#                 'title' : self.title,
#                 'description' : self.description,
#                 'pubmed' : self.pubmed,
#                 'contributors' : self.contributors,
#                 'crosslinks' : self.crosslinks,
#                 'last_update' : self.last_update,
#                 'submission_date' : self.submission_date,
#                 'owner' : self.owner,
#                 'author' : self.author,
#                 'file_path' : self.file_path,
#                 'tags' : self.tags
#     }, width=1)

#     def get_write(self, path_filename):


#         if len(self.studies_id) == 1:
#             _studies= str(self.studies_id[0])
#         else:
#             _studies= ' , '.join(self.studies_id)

#         if len(self.strategies_id) == 1:
#             _strategies = str(self.strategies_id[0])
#         else:
#             _strategies = ' , '.join(self.strategies_id)

#         if len(self.studies_id) == 1:
#             _studies = str(self.studies_id[0])
#         else:
#             _studies= ' , '.join(self.studies_id)

#         if len(self.lists_id) == 1:
#             _lists = str(self.lists_id[0])
#         else:
#             _lists = ' , '.join(self.lists_id)

#         liste = ' , '.join(self.id)

#         with open(path_filename, 'a') as output:
#             output.write(   self.project_id+"\t"+
#                             _studies +"\t"+
#                             _strategies + "\t" +
#                             _lists + "\t" +
#                             self.title + "\t" +
#                             self.description + "\t"+
#                             self.pubmed + "\t"+
#                             self.contributors + "\t"+
#                             self.crosslinks+ "\t"+
#                             self.last_update+ "\t" +
#                             self.submission_date +"\t" +
#                             self.owner +"\t" +
#                             self.author + "\t"+
#                             self.file_path + "\t" +
#                             self.status + "\t" +
#                             self.tags + "\t"+
#                             liste+"\n" )


# class Study:

#     compteur_study=0
#     def __init__(self,\
#         title,\
#         description,\
#         phenotype_desease,\
#         go_term,\
#         organism,\
#         development_stage,\
#         pubmed,\
#         add_info,\
#         last_update,\
#         owner,\
#         file_path,\
#         identifiant):

#         self.project_id = ""
#         self.studies_id="GST" + str(Study.compteur_study)
#         self.strategies_id=[]
#         self.lists_id=[]
#         self.title = title
#         self.description = description
#         self.phenotype_desease = phenotype_desease
#         self.go_term = go_term
#         self.organism = organism
#         self.development_stage = development_stage
#         self.pubmed = pubmed
#         self.add_info = add_info
#         self.last_update = last_update
#         self.owner = owner
#         self.file_path = file_path
#         self.status = "private"
#         self.tags = ""
#         Study.compteur_study += 1
#         self.id=identifiant


#     def get_dico(self):
#         if len(self.strategies_id) == 1:
#             _strategies = str(self.strategies_id[0])
#         else:
#             _strategies = ' , '.join(self.strategies_id)


#         if len(self.lists_id) == 1:
#             _lists = str(self.lists_id[0])
#         else:
#             _lists = ' , '.join(self.lists_id)

#         return {'project_id' : self.project_id,
#                 'studies_id' : self.studies_id,
#                 'strategies_id' : _strategies,
#                 'lists_id' : _lists,
#                 'title' : self.title,
#                 'description' : self.description,
#                 'phenotype_desease' : self.phenotype_desease,
#                 'go_term' : self.go_term,
#                 'organism' : self.organism,
#                 'development_stage' : self.development_stage,
#                 'pubmed' : self.pubmed,
#                 'last_update' : self.last_update,
#                 'add_info' : self.add_info,
#                 'status' : self.status,
#                 'owner' : self.owner,
#                 'file_path' : self.file_path,
#                 'status' : self.status,
#                 'tags' : self.tags,
#         }

#     def get_write(self, path_filename):

#         if len(self.strategies_id) == 1:
#             _strategies = str(self.strategies_id[0])
#         else:
#             _strategies = ' , '.join(self.strategies_id)


#         if len(self.lists_id) == 1:
#             _lists = str(self.lists_id[0])
#         else:
#             _lists = ' , '.join(self.lists_id)

#         liste = ' , '.join(self.id)

#         with open(path_filename, 'a') as output:
#             output.write(   self.project_id+"\t"+
#                             self.studies_id +"\t"+
#                             _strategies + "\t" +
#                             _lists + "\t" +
#                             self.title + "\t" +
#                             self.description + "\t"+
#                             self.phenotype_desease + "\t"+
#                             self.go_term + "\t"+
#                             self.organism+ "\t"+
#                             self.development_stage+ "\t" +
#                             self.pubmed +"\t" +
#                             self.add_info +"\t" +
#                             self.last_update + "\t"+
#                             self.file_path + "\t" +
#                             self.status + "\t" +
#                             self.tags + "\t"+
#                             liste+"\n" )

# class Strategy:

#     compteur_strategy=0
#     def __init__(self,\
#         title,\
#         description,\
#         type_of_experiment,\
#         technology,\
#         process,\
#         add_info,\
#         last_update,\
#         owner,\
#         file_path,\
#         identifiant):

#         self.project_id = ""
#         self.studies_id=""
#         self.strategies_id="GSR" + str(Strategy.compteur_strategy)
#         self.lists_id=[]
#         self.title = title
#         self.description = description
#         self.type_of_experiment = type_of_experiment
#         self.technology = technology
#         self.process = process
#         self.add_info = add_info
#         self.last_update = last_update
#         self.owner = owner,
#         self.file_path = file_path
#         self.status = "private"
#         self.tags = ""
#         Strategy.compteur_strategy += 1
#         self.id=identifiant

#     def get_dico(self):
#         if len(self.lists_id) == 1:
#             _lists = str(self.lists_id[0])
#         else:
#             _lists = ' , '.join(self.lists_id)

#         return {'project_id' : self.project_id,
#                 'studies_id' : self.studies_id,
#                 'strategies_id' : self.strategies_id,
#                 'lists_id' : _lists,
#                 'title' : self.title,
#                 'description' : self.description,
#                 'type_of_experiment' : self.type_of_experiment,
#                 'technology' : self.technology,
#                 'process' : self.process,
#                 'last_update' : self.last_update,
#                 'add_info' : self.add_info,
#                 'status' : self.status,
#                 'owner' : self.owner,
#                 'file_path' : self.file_path,
#                 'status' : self.status,
#                 'tags' : self.tags,
#         }

#     def get_write(self, path_filename):


#         if len(self.lists_id) == 1:
#             _lists = str(self.lists_id[0])
#         else:
#             _lists = ' , '.join(self.lists_id)

#         liste = ' , '.join(self.id)

#         with open(path_filename, 'a') as output:
#             output.write(   self.project_id+"\t"+
#                             self.studies_id +"\t"+
#                             self.strategies_id + "\t" +
#                             _lists + "\t" +
#                             self.title + "\t" +
#                             self.description + "\t"+
#                             self.type_of_experiment + "\t"+
#                             self.technology + "\t"+
#                             self.process+ "\t"+
#                             self.add_info+ "\t" +
#                             self.last_update + "\t"+
#                             self.file_path + "\t" +
#                             self.status + "\t" +
#                             self.tags + "\t"+
#                             liste+"\n" )



# class List:

#     compteur_list=0
#     def __init__(self,\
#         title,\
#         description,\
#         identifiers,\
#         identifier_extended,\
#         list_parent_id,\
#         list_child_id,\
#         comparable,\
#         _list,\
#         add_info,\
#         last_update,\
#         owner,\
#         file_path,\
#         identifiant):

#         self.project_id = ""
#         self.studies_id=""
#         self.strategies_id=""
#         self.lists_id="GUL" + str(List.compteur_list)
#         self.title = title
#         self.description = description
#         self.identifiers = identifiers
#         self.identifier_extended = identifier_extended
#         self.list_parent_id = list_parent_id
#         self.list_child_id = list_child_id
#         self.comparable = comparable
#         self.list = _list
#         self.add_info = add_info
#         self.last_update = last_update
#         self.owner = owner
#         self.file_path = file_path
#         self.status = "private"    
#         self.tags = ""
#         List.compteur_list += 1

#         self.id = identifiant

#     def get_dico(self):


            
#         return {'project_id' : self.project_id,
#                 'studies_id' : self.studies_id,
#                 'strategies_id' : self.strategies_id,
#                 'lists_id' : self.lists_id,
#                 'title' : self.title,
#                 'description' : self.description,
#                 'identifiers' : self.identifiers,
#                 'identifier_extended' : self.identifier_extended,
#                 'list_parent_id' : self.list_parent_id,
#                 'list_child_id' : self.list_child_id,
#                 'comparable' : self.comparable,
#                 'list' : self.list,
#                 'last_update' : self.last_update,
#                 'add_info' : self.add_info,
#                 'owner' : self.owner,
#                 'file_path' : self.file_path,
#                 'status' : self.status,
#                 'tags' : self.tags,
#         }

#     def get_write(self, path_filename):

#         with open(path_filename, 'a') as output:
#             output.write(   self.project_id+"\t"+
#                             self.studies_id +"\t"+
#                             self.strategies_id + "\t" +
#                             self.lists_id + "\t" +
#                             self.title + "\t" +
#                             self.description + "\t"+
#                             self.identifiers + "\t"+
#                             self.identifier_extended + "\t"+
#                             self.list_parent_id+ "\t"+
#                             self.list_child_id+ "\t" +
#                             self.comparable + "\t"+
#                             self.add_info+"\t"+
#                             self.last_update+"\t"+
#                             self.file_path + "\t" +
#                             self.status + "\t" +
#                             self.tags +"\n" )




@view_config(route_name='project_up', renderer='json', request_method='POST')
def save_excel(request):
    print "save_excel"
    session_user = is_authenticated(request)
    if session_user is None:
        return 'HTTPForbidden()'

    input_file = None
    form = json.loads(request.body, encoding=request.charset)
    user = form['uid']
  
    try:
        input_file = form['file']
    except Exception:
        return HTTPForbidden('no input file')

    print 'write file into : '+input_file















    # #Read excel file
    # wb = xlrd.open_workbook(input_file,encoding_override="cp1251")

    # projects=[]
    # strategies=[]
    # lists=[] 

    # for line in wb.sheet_by_index(0).row_values(row_number, start_colx=0, end_colx=None):
    #     for i in line:
    #         print i
    # return

    # add_project(wb.sheet_by_index(0)) 
        
    # add_study(wb.sheet_by_index(1))
        
    # add_strategy(wb.sheet_by_index(2))
        
    # add_list(wb.sheet_by_index(3),wb.sheet_by_index(4))


    projects=[]
    #projects={}
    studies=[]
    strategies=[]

    lists=[]

    projects_id =[]
    studies_id = []
    strategies_id = []
    lists_id = []
    dt = datetime.datetime.utcnow()
    date = time.mktime(dt.timetuple())
    #print "date : " + str(datetime.datetime.utcnow())
    #print "date : " + str(date)

    def is_empty(row_value):
        boolean=False
        for i in row_value:
            if row_value != "":
                return True
        return boolean

    def add_project(project_sheet):
        if Project.compteur_project == 0:
            #print str(request.registry.db_mongo['projects'].find().count())
            Project.compteur_project = int(request.registry.db_mongo['projects'].find().count())
        for row_number in range(5, project_sheet.nrows):
            
            row_value = project_sheet.row_values(row_number, start_colx=0, end_colx=None)

            # project[(get_str(row_value[0]), "", "","")] = Project(   get_str(row_value[1]),\
            #                         get_str(row_value[2]),\
            #                         get_str(row_value[3]),\
            #                         get_str(row_value[4]),\
            #                         get_str(row_value[5]),\
            #                         get_str(date),\
            #                         get_str(date),\
            #                         get_str(user),\
            #                         get_str(user),\
            #                         get_str(input_file),\

            if is_empty(row_value):
                projects.append(Project(   get_str(row_value[1]),\
                                        get_str(row_value[2]),\
                                        get_str(row_value[3]),\
                                        get_str(row_value[4]),\
                                        get_str(row_value[5]),\
                                        get_str(date),\
                                        get_str(date),\
                                        get_str(user),\
                                        get_str(user),\
                                        get_str(input_file),\
                                        [get_str(row_value[0]), "", "",""],
                                    ))



    def add_study(study_sheet):
        if Study.compteur_study == 0:
            Study.compteur_study = int(request.registry.db_mongo['studies'].find().count())
        for row_number in range(5, study_sheet.nrows):
            row_value = study_sheet.row_values(row_number, start_colx=0, end_colx=None)

            if is_empty(row_value):
                studies.append(Study(  get_str(row_value[2]),\
                                    get_str(row_value[3]),\
                                    get_str(row_value[4]),\
                                    get_str(row_value[5]),\
                                    get_str(row_value[6]),\
                                    get_str(row_value[7]),\
                                    get_str(row_value[8]),\
                                    get_str(row_value[9]),\
                                    get_str(date),\
                                    get_str(user),\
                                    get_str(input_file),\
                                    [get_str(row_value[1]), get_str(row_value[0]), "", ""],

                                ))

    def add_strategy(strategy_sheet):
        if Strategy.compteur_strategy== 0:
            Strategy.compteur_strategy = int(request.registry.db_mongo['strategies'].find().count())
        for row_number in range(5, strategy_sheet.nrows):
            row_value = strategy_sheet.row_values(row_number, start_colx=0, end_colx=None)
            if is_empty(row_value):
                strategies.append(Strategy( get_str(row_value[2]),\
                                            get_str(row_value[3]),\
                                            get_str(row_value[4]),\
                                            get_str(row_value[5]),\
                                            get_str(row_value[6]),\
                                            get_str(row_value[7]),\
                                            get_str(date),\
                                            get_str(user),\
                                            get_str(input_file),\
                                            ["",get_str(row_value[1]), get_str(row_value[0]), ""],

                                        ))


    def get_Col_List(header_col, list_headers):
        if header_col in list_headers:
            return list_headers.index(header_col)
        # for header in list_headers:
        #     if header_col == header: 
        #         return  list_headers.index(header_col)

    def add_list(list_sheet, idList_sheet):
        if List.compteur_list == 0:
            List.compteur_list = int(request.registry.db_mongo['lists'].find().count())
        idLists = [get_str(list_ID) for list_ID in idList_sheet.row_values(0, start_colx=0, end_colx=None)]
        for row_number in range(5, list_sheet.nrows):
            row_value = (list_sheet.row_values(row_number, start_colx=0, end_colx=None))
            if is_empty(row_value):
                boolean = True
                for _liste in lists:
                    if _liste.id[3] == get_str(row_value[0]):
                        _liste.identifiers = _liste.identifiers + ' , ' + get_str(row_value[4])
                        _liste.identifier_extended = _liste.identifier_extended + ' , ' + get_str(row_value[5])
                        boolean = False
                        break
                if boolean:

                    index_list_identifiants =  get_Col_List(get_str(row_value[0]), idLists)
                    list_identifiants=[]
                    for name in idList_sheet.col_values(index_list_identifiants, start_rowx=1, end_rowx=None):
                        
                        
                        if name != "":
                            a=re.sub(r" ", '', str(name))
                            try:
                                a=int(float(a))
                                list_identifiants.append(str(a))

                            except:
                                list_identifiants.append(str(a))


                    #print list_identifiants
                    list_identifiants = ",".join(str(name) for name in list_identifiants)
                    #print list_identifiants
                    #list_identifiants = re.sub(r" ", '', list_identifiants)
                    #print list_identifiants
                    # list_identifiants=""
                    _list = List( get_str(row_value[2]),\
                                get_str(row_value[3]),\
                                get_str(row_value[4]),\
                                get_str(row_value[5]),\
                                get_str(row_value[6]),\
                                get_str(row_value[7]),\
                                get_str(row_value[8]),\
                                list_identifiants,\
                                get_str(row_value[9]),\
                                get_str(date),\
                                get_str(user),\
                                get_str(input_file),\
                                ["", "", get_str(row_value[1]), get_str(row_value[0])],

                            )
                    add_multiple_id(_list)
                    lists.append(_list)
                    #print _list.list
            
            # print "333333"
            # boolean = True
            # for obj in lists:
            #     if obj.identifiant == _list.identifiant:
            #         obj.identifiant = obj.identifiant + " , " + _list.identifiant
            #         if not _list.identifier_extended:
            #             obj.identifier_extended = obj.identifier_extended + " , " + ""
            #         else:
            #             obj.identifier_extended = obj.identifier_extended + " , " + _list.identifier_extended
            #         boolean=False
            #         break
            # if boolean:
            #     add_multiple_id(_list)
            #     lists.append(_list)



    def add_multiple_id(_list):
        """Modifier list par dico pour eviter les boucles donc gain de temps"""
        _project=None
        _study=None
        _strategy=None
        print "start"
        
        
        print lists
        print "end"
        for strategy in strategies:
            print strategy.id
            if _list.id[2] == strategy.id[2]:
                _strategy=strategy


        for study in studies:
            print study.id
            if _strategy.id[1] == study.id[1]:
                _study=study
        
        for project in projects:
            #pprint.pprint(study)
            if _study.id[0] == project.id[0]:
                _project=project

        if _study.studies_id not in _project.studies_id:
            _project.studies_id.append(_study.studies_id)
        if _strategy.strategies_id not in _project.strategies_id:
            _project.strategies_id.append(_strategy.strategies_id)
        if _list.lists_id not in _project.lists_id:
            _project.lists_id.append(_list.lists_id)

        if _study.project_id == "":
            _study.project_id = _project.project_id
        if _strategy.strategies_id not in _study.strategies_id:
            _study.strategies_id.append(_strategy.strategies_id)
        if _list.lists_id not in _study.lists_id:
            _study.lists_id.append(_list.lists_id)

        if _strategy.project_id == "":
            _strategy.project_id = _project.project_id
        if _strategy.studies_id == "":
            _strategy.studies_id = _study.studies_id
        if _list.lists_id not in _strategy.lists_id:
            _strategy.lists_id.append(_list.lists_id)

        _list.project_id = _project.project_id
        _list.studies_id = _study.studies_id
        _list.strategies_id = _strategy.strategies_id

    def delDoublon(liste):
        newListe=[]
        for element in liste:
            if element not in newListe:
                newListe.append(element)
        return newListe
    def get_Convert(upload_path):

        """ajouter une exception pour collections qui sont des entiers naturels positifs"""

        print "enter get_convert"
        raw=[]
        entrez=[]
        homologene=[]
        gpl='GPL'

        for _list in lists:

            identifiers=_list.identifiers.split(' , ')
            newIdentifiers = []
           
            for index in range(len(identifiers)):
                if identifiers[index] == 'GPL':
                    newIdentifiers.append(_list.identifier_extended.split(',')[index])

                else:
                    newIdentifiers.append(identifiers[index])

            print "newidentfiers : ",newIdentifiers
            #dico=[]
            #print _list.list.split(',')

            #list_identifiers = _list.list.split



            # t0 = time.time()
            # list(request.registry.db_mongo[identifiers[index]].find({'BDname' : {"$regex" : str(newIdentifiers[index])},'BDID':{"$in" : _list.list.split(',')}},{'HomoloGene':1, 'BDID' : 1, 'GeneID' : 1 , '_id' :0}))
            # print time.time() - t0, "seconds wall time"
            # result=[]
            # query=list(request.registry.db_mongo['BDname'].find({'BDname' : {"$regex" : str(newIdentifiers[index])},"BDID":{"$nin": _list.list.split(',')}}, {'GeneID' : 1 , '_id' :0}))
            # for i in query:
            #     result.append(i['GeneID'])
            # print str(len(result))

            
            def search(collection, BDname, _list):

                if collection == "GPL":
                    print BDname
                    res= list(request.registry.db_mongo[collection].find({'GPLname' : {"$regex" : str(BDname)},'BDID':{"$in":_list}}))#,{'Homologene':1, 'BDID' : 1, 'GeneName':1, 'GeneDescription':1,  'GeneID' : 1 ,'TaxID':1, '_id' :0}))

                else:
                    res = list(request.registry.db_mongo[collection].find({'BDID':{"$in" :_list}},{'HomoloGene':1, 'BDID' : 1, 'GeneID' : 1 , '_id' :0}))
                
                not_found=[]
                for elt in res:
                    not_found.append(elt['BDID'])
                not_found=list(set(_list).symmetric_difference(set(not_found)))   
                # newSearch=[]
                # for elt in res:
                #     #print elt
                #     if elt['GeneID'] not in newSearch:
                #         newSearch.append(elt['GeneID'])
                # #print newSearch[:5]
                # not_found=[]
                # for item in _list:
                #     if item not in newSearch:
                #         not_found.append(str(item))
                return res, not_found
                
            res, not_found =search(identifiers[0], newIdentifiers[0],_list.list.split(','))
           # print not_found
            #return
            if len(identifiers) > 1:
                for i in range(1,len(identifiers),1):
                    if not_found:
                        break
                    else:
                        _res, _not_found= search(identifiers[i], newIdentifiers[i], not_found)
                    for elt in _res:
                        res.append(elt)
                    not_found=_not_found
               # while next(identifiers) and not_found is :
                    
            
            with open(os.path.join(upload_path, str(_list.project_id), str(_list.lists_id), str(_list.lists_id))+".txt" , 'w') as output:
                for elt in res:
                    output.write(str(elt['BDID']) + "\t" + str(elt['GeneID']) + "\t" + str(elt['Homologene']) + "\t" + str(elt['GeneName'])+ "\t" + str(elt['GeneDescription'])+ "\t" + str(elt['TaxID'])+"\n" )
                for elt in not_found:
                    output.write(str(elt) + "\t" + "-" + "\t" + "-" +  "\t" + "-" + "\t" + "-" +"\t" + "-" +"\n")

            #print time.time() - t0, "seconds wall time"


           #other way START
            # dico={}
            # t0 = time.time()
            # for _listID in _list.list.split(','):
            #     a=[]
                
            #     for index in range(len(identifiers)):
            #         try:
            #             #print identifiers[index]
            #             if identifiers[index] == "GPL":
            #                 # print "start"
            #                 # print str(identifiers[index])
            #                 # print str(newIdentifiers[index])
            #                 # print str(_listID)
            #                 res = list(request.registry.db_mongo[identifiers[index]].find({'BDname' : {"$regex" : str(newIdentifiers[index])},'BDID':str(_listID)},{'HomoloGene':1, 'BDID' : 1, 'GeneID' : 1 , '_id' :0}))
            #                 # print res
            #                 # print "stop \n"

            #             else:
            #                 res = list(request.registry.db_mongo[identifiers[index]].find({'BDID':str(_listID)},{'HomoloGene':1, 'BDID' : 1, 'GeneID' : 1 , '_id' :0}))
            #             #print res
            #             if res is not None:
            #                 for elt in res:
            #                     a.append(elt)
            #         except:
            #             print "error"
            #             # return
            #     if a:
            #         dico[str(_listID)]=a
            #     else:
            #         dico[str(_listID)] ="-"

            # with open(os.path.join(upload_path, str(_list.project_id), str(_list.lists_id), str(_list.lists_id))+".txt" , 'w') as output:

            #     for elt in dico.keys():
            #         #print elt
            #         if dico[elt] == '-':
            #             output.write(str(elt) + "\t" + "-" + "\t" + "-" + "\n")
            #         else:
            #             for line in dico[elt]:
            #                 print line
            #                 output.write(str(elt) + "\t" + str(line['GeneID']) + "\t" + str(line['HomoloGene']) + "\n" )
            # print time.time() - t0, "seconds wall time"
            #Other way END








            #ajouterune bouckle pour écrire dans un fichier le nom du fichier est égale a GUL (lists_id)

            # dico={}
            # for _listID in _list.list.split(','):
            #     for identifier in newIdentifiers:
            #         Entrez_gene = list(request.registery.db_mongo[identifier].find({"BD" : str(identifer), "BDID" : str(_listID)}, {'GeneID': 1, '_id':0}))
            #         dico1={}
            #         if Entrez_gene is not None:
            #             for elt in Entrez_gene:
            #                 homologene= request.registery.db_mongo['HomoloGene'].find({"BD" : str(identifer), "GeneID" : str(elt)}, {'BDID': 1, '_id':0}).limit(1)
            #                 if homologene is None:
            #                     dico1[str(elt)] = '-'
            #                 else:
            #                     dico1[str(elt)] = str(homologne['BDID'])
            #             dico[_listID]= dico1
            #         else:
            #             dico[str(identifier)] = '-'
            # pprint.pprint(dico)











            # _lists = _list.list.split(",")
            # for _listID in _lists:
            #     Entrez_gene=list(requiest.registry.db_)
        #print 'start'
        #[Rat230_2] Affymetrix Rat Genome 230 2.0 Array
        #[Mouse430_2] Affymetrix Mouse Genome 430 2.0 Array










        # return
        # for _list in lists:
        #     has = _list.list.split(",")

        #     print str(len(has))
        #     ahs=list(request.registry.db_mongo['GPL'].find({"BD" : "[Mouse430_2] Affymetrix Mouse Genome 430 2.0 Array" ,'BDID':{"$in" :has}}, {'GeneID':1, '_id':0}))
        #     print(str(len(ahs)))
        #     ahs=delDoublon(ahs)
        #     print(str(len(ahs)))
        #     entrez=[]

        #     for toto in ahs:
        #         entrez.append(toto['GeneID'])


        #     #print entrez
        #     homolo=[]
        #     hre=list(request.registry.db_mongo['HomoloGene'].find({'GeneID':{"$in" :entrez}}, {'BDID':1, '_id':0}))

        #     for the in hre:
                
        #         homolo.append(the['BDID'])
            
        #         #for the in hre:
        #             #homolo.append(the['BDID'])
        #     with open(os.path.join(upload_path, "MusEntrezGene"+ str(_list.title)) , 'w') as output:
        #         for entre in entrez:

        #             output.write(str(entre)+"\n")

        #     with open(os.path.join(upload_path, "MusHomologene"+ str(_list.title)) , 'w') as output:
        #         for hom in homolo:
  
        #             output.write(str(hom) + "\n")    

        #     print 'name list : ' + str(_list.title)+ " found len : " + str(len(ahs)) + "for original len " + str(len(has)) + "nombre HomologenID : "+ str(len(homolo))
            

















            #ncbi=[]
            #print ahs
            #for entre in ahs:
                #print "ok"
   
                        # print elt["geneID"]
            #print ncbi
                #r=request.registry.db_mongo['HomoloGene'].find({'GeneID':str(entre)}).limit(1)
                #if r!= None:
                    #ncbi.append(r['BDID'])
            # request.registry.db_mongo['GPL'].find({"BDID":{$in:["1769308_at","toto"]}},{"GeneID":1,"BDID":1, _id:0}).limit(1) _list.list.split(',')
            #print _list.list.split(',')
            #ahs = list(request.registry.db_mongo['GPL'].find({'BDID':{'$in':['1769308_at','1769308_at']}}).limit(1))
            #print ahs
            #print 'name list : ' + str(_list.title)+ " found len : " + str(len(ahs)) + "for original len " + str(len(has)) + "nombre HomologenID : "+ str(len(ncbi))
            
        #print 'end'
        # for _list in lists:
        #     print _list.list
        #     identifiants =_list.identifiers.split(',')
        #     identifiants_extended=_list.identifier_extended.split(',')
        #     if (len(identifiants) == 1 and identifiants[0] == 'Other'):
        #         continue

        #     else:
        #         if len(identifiants) == 1:
        #             print "here"
        #             if identifiants[0] == 'Uniprot':
        #                 for name in _list.list.split(','):
        #                     print "name : ",name 
        #                     raw.append(str(name))
        #                     swissprot = get_Entrez_ID('SwissProt', str(name))
        #                     trembl = get_Entrez_ID('trEMBL', str(name))
        #                     entrez_id=""
        #                     if swissprot == None and trembl != None:
        #                         entrez_id= trembl['BDID']
        #                         entrez.append(entrez_id)
        #                     elif swissprot != None and trembl == None:
        #                         entrez_id= swissprot['BDID']
        #                         entrez.append(entrez_id)
        #                     else:
        #                         entrez.append("-")
        #                         print name , ' error'
        #                     if entrez_id != "":
        #                         _homologene = get_HomoloGeneID(entrez_id)
        #                         if _homologene != None:
        #                             homologene_id = _homologene['BDID']
        #                             homologene.append(str(homologene_id))
        #                         else:
        #                             homologene.append("-")
        #                     else:
        #                         homologene.append("-")

        #             elif identifiants[0] == gpl:

        #                 for name in _list.list.split(','):
        #                     raw.append(str(name))
        #                     _gpl =  get_GPL(str(identifiants_extended[0]), str(name))
        #                     if _gpl == None:
        #                         entrez.append('-')
        #                         homologene.append('-')
        #                     else:
        #                         entrez_id = _gpl['GeneID']
        #                         entrez.append(str(entrez_id))
        #                         _homologene=get_HomoloGeneID(str(entrez_id))
        #                         if _homologene == None:
        #                             homologene.append('-')
        #                         else:
        #                             homologene_id= _homologene['GeneID']
        #                             homologene.append(str(homologene_id))

        #             else:
        #                 base = str(identifiants[0])
        #                 if identifiants[0] == "Entrez_name":
        #                     base = "Gene_Symbol"
        #                 print base
        #                 for name in _list.list.split(','):

        #                     raw.append(str(name))
        #                     _entrez = get_Entrez_ID(base, str(name))
        #                     if _entrez == None:
        #                         entrez.append('-')
        #                         homologene.append('-')
        #                     else:
        #                         entrez_id = _entrez['GeneID']
        #                         #pprint.pprint(_entrez)
        #                         entrez.append(str(entrez_id))
        #                         _homologene = get_HomoloGeneID(str(name))
        #                         if _homologene == None:
        #                             homologene.append("-")
        #                         else:
        #                             homologene_id = _homologene['GeneID']
        #                             homologene.append(str(homologene_id))
        #                         print entrez_id
        #                 print "herererer"

        #         else:

        #             for name in _list.list.split(','):

        #                 raw.append(name)
        #                 entrez_identifiant=[]
        #                 entrez_id=""
        #                 for index in range(len(identifiants)):

        #                     if identifiants[index] == 'Uniprot':
        #                         swissprot = get_Entrez_ID('SwissProt', str(name))
        #                         trembl = get_Entrez_ID('trEMBL', str(name))
        #                         entrez_id=""
        #                         if swissprot == None and trembl != None:
        #                             entrez_id= str(trembl['BDID'])
        #                         elif swissprot != None and trembl == None:
        #                             entrez_id= str(swissprot['BDID'])
        #                         else:
        #                             entrez_id = '-'
        #                             print "error"

        #                         entrez_identifiant.append(entrez_id)

        #                     elif identifiants[index] == gpl:
        #                         _entrez = get_Entrez_ID(str(identifiants_extended[index]), name)
        #                         if _entrez == None:
        #                             entrez.append('-')
        #                         else:
        #                             entrez_id = _entrez['GeneID']
        #                             entrez.append(str(entrez_id))
        #                     else:
        #                         base = str(identifiants[index])
        #                         if identifiants[index] == "Entrez_name":
        #                             base = "Gene_Symbol"

        #                         _entrez = get_Entrez_ID(base, str(name))

        #                         if _entrez == None:
        #                             entrez_identifiant.append('-')
        #                         else:
        #                             entrez_id = _entrez['GeneID']
        #                             entrez_identifiant.append(str(entrez_id))

        #                 for entrez in entrez_identifiant:
        #                     if entrez != '-':
        #                         entrez_id=str(entrez)
        #                         entrez.append(entrez_id)
        #                 if entrez_id == "":
        #                     entrez_id="-"

        #                 if entrez_id != "-":
        #                     _homologene = get_HomoloGeneID(entrez_id)
        #                     if _homologene == None:
        #                         homologene.append('-')
        #                     else:
        #                         homologene_id = _homologene['GeneID']
        #                         homologene.append(str(homologene_id))
        #                 else:
        #                      homologene.append('-')






            # print "path"
            # print upload_path
            # print _list.project_id
            # print _list.lists_id
            # print _list.lists_id
            # with open(os.path.join(upload_path, _list.project_id, _list.lists_id, _list.lists_id) , 'w') as output:
            #     for index in range(len(raw)):
            #         output.write(str(raw[index]) + "\t" + str(entrez[index]) + "\t" + str(homologene[index]) + "\n")
            #         print "has write"




    def get_Entrez_ID(base, bdid):
        #db.GPL.find({"BD": "[Yeast_2] Affymetrix Yeast Genome 2.0 Array","BDID":{$in:["1769308_at","toto"]}},{"GeneID":1,"BDID":1, _id:0}).limit(1)
        return request.registry.db_mongo[str(base)].find({"BDID" : str(bdid)})
                
    def get_HomoloGeneID(entrez_id):
        return request.registry.db_mongo['HomoloGene'].find_one({"BDID" : str(entrez_id)})

    def get_GPL(gpl_name, id_name):
         return request.registry.db_mongo['GPL'].find_one({"BD" : str(gpl_name),"BDID" : str(entrez_id)})




    try:
        """Important empecher l'ajout dans la base si multiple id pour projet study et strat"""
        add_project(wb.sheet_by_index(0)) 
        
        add_study(wb.sheet_by_index(1))
        
        add_strategy(wb.sheet_by_index(2))
        
        add_list(wb.sheet_by_index(3),wb.sheet_by_index(4))

        # for project in projects:
        #     print "ok"
        #     project.get_write("/home/clancien/project.txt")
        # for study in studies:
        #     print "ok"
        #     study.get_write("/home/clancien/study.txt")
        # for strategy in strategies:
        #     print "ok"
        #     strategy.get_write("/home/clancien/strategy.txt")
        # for _list in lists:
        #     print "ok"
        #     _list.get_write("/home/clancien/lists.txt")
        upload_path = os.path.join(request.registry.upload_path, user, 'dashboard')
        for project in projects:
            request.registry.db_mongo['projects'].insert(project.get_dico())
            #v=os.path.join(upload_path, project.project_id)
            #print str(v)
            if not os.path.exists(os.path.join(upload_path, project.project_id)):

                os.makedirs(os.path.join(upload_path, project.project_id))
                print "create project directory"

        for study in studies:
            request.registry.db_mongo['studies'].insert(study.get_dico())

        for strategy in strategies:
            request.registry.db_mongo['strategies'].insert(strategy.get_dico())

        for _list in lists:
            request.registry.db_mongo['lists'].insert(_list.get_dico())
            #v=os.path.join(upload_path, project.project_id,_list.lists_id)
            #print str(v)
            if not os.path.exists(os.path.join(upload_path, _list.project_id,_list.lists_id)):
                os.makedirs(os.path.join(upload_path, _list.project_id, _list.lists_id))
            #os.rename(os.path.join(upload_path, _list.lists_id, name_file))
            #v = get_str(os.path.join(upload_path, _list.project_id, _list.lists_id)) #, namefile))
            #print v
            #_list.file_path= get_str(os.path.join(upload_path, _list.project_id, _list.lists_id, namefile))
            #pprint.pprint(request.registry.db_mongo['lists'].find_one({'project_id' : 'GPR0'}))
        print "try"
        #t0 = time.time()
        get_Convert(upload_path)
        #print time.time() - t0, "seconds wall time"
        return {'msg':"File checked and uploded !", 'status':'0'}

    except:
        logger.warning("Error - Save excel file")
        logger.warning(sys.exc_info())
        return {'msg':'An error occurred while uploading your file. If the error persists please contact TOXsIgN support ','status':'1'}


    # sh = wb.sheet_by_index(0)
    # projects={}
    # critical = 0
    

    # try :
    #     for rownum in range(5, sh.nrows):
    #             row_values = sh.row_values(rownum)
    #             if row_values [1] == "" and row_values [2] == "" and row_values [3] =="" :
    #                 continue
    #             project_error = {'Critical':[],'Warning':[],'Info':[]}

    #             project_id = row_values[0]
    #             project_title = ""
    #             project_description = ""
    #             project_pubmed = ""
    #             project_contributors=""
    #             project_crosslink = ""

    #             if row_values[1] != "":
    #                 project_title = row_values[1]
    #             else :
    #                 project_error['Critical'].append("No project title ("+project_id+")")
    #                 critical += 1

    #             if row_values[2] != "":
    #                 project_description = row_values[2]
    #             else :
    #                 project_error['Warning'].append("No project description ("+project_id+")")

    #             if row_values[3] != "" :
    #                 if ';' in str(row_values[3]) or '|' in str(row_values[3]):
    #                     project_error['Critical'].append("Use comma to separate your pubmed ids ("+project_id+")")
    #                     critical += 1
    #                 else :
    #                     project_pubmed = str(row_values[3])
    #             else :
    #                 project_error['Info'].append("No associated pubmed Id(s)")

    #             if row_values[4] != "" :
    #                 if ';' in row_values[4] or '|' in row_values[4]:
    #                     project_error['Critical'].append("Use comma to separate your contributors ("+project_id+")")
    #                     critical += 1
    #                 else :
    #                     project_contributors = row_values[4]
    #             else :
    #                 project_error['Info'].append("No associated contributors ("+project_id+")")

    #             if row_values[5] != "" :
    #                 if ';' in row_values[5] or '|' in row_values[5]:
    #                     project_error['Critical'].append("Use comma to separate your links ("+project_id+")")
    #                     critical += 1
    #                 else :
    #                     project_crosslink = row_values[5]
    #             else :
    #                 project_error['Info'].append("No cross link(s) ("+project_id+")")


    #             #After reading line add all info in dico project
    #             request.registry.db_mongo['project'].update({'id': 1}, {'$inc': {'val': 1}})
    #             repos = request.registry.db_mongo['project'].find({'id': 1})
    #             id_p = ""
    #             for res in repos:
    #                 id_p = res

    #             #Excel id -> databas id
    #             asso_id[project_id] = 'TSP'+str(id_p['val'])
    #             reverse_asso[asso_id[project_id]] = project_id

    #             dico={
    #                 'id' : asso_id[project_id],
    #                 'title' : project_title,
    #                 'description' : project_description,
    #                 'pubmed' : project_pubmed,
    #                 'contributor' : project_contributors,
    #                 'assays' : "",
    #                 'cross_link' : project_crosslink,
    #                 'studies' : "",
    #                 'factors' : "",
    #                 'signatures' :"",
    #                 'last_update' : str(sdt),
    #                 'submission_date' : str(sdt),
    #                 'status' : 'private' ,
    #                 'owner' : user,
    #                 'author' : user ,
    #                 'tags' : "",
    #                 'edges' : "",
    #                 'info' : ','.join(project_error['Info']),
    #                 'warnings' : ','.join(project_error['Warning']),
    #                 'critical' : ','.join(project_error['Critical']),
    #                 'excel_id' : project_id
    #             }
    #             projects[project_id] = dico

    #     # Check studies
    #     sh = wb.sheet_by_index(1)
    #     studies={}
    #     for rownum in range(6, sh.nrows):
    #             row_values = sh.row_values(rownum)
    #             if row_values [1] == "" and row_values [2] == "" and row_values [3] =="" :
    #                 continue
    #             study_error = {'Critical':[],'Warning':[],'Info':[]}

    #             study_id = row_values[0]
    #             study_projects = ""
    #             study_title = ""
    #             study_description=""
    #             study_experimental_design=""
    #             study_results=""
    #             study_type = ""
    #             study_inclusion_periode = ""
    #             study_inclusion = ""
    #             study_exclusion = ""
    #             study_followup = ""
    #             study_pubmed = ""
    #             study_pop_size = ""
    #             study_pubmed = ""

    #             if row_values[1] != "":
    #                 if row_values[1] in projects:
    #                     study_projects = row_values[1]
    #                 else :
    #                     study_error['Critical'].append("Project doesn't exists ("+study_id+")")
    #                     critical += 1
    #             else :
    #                 study_error['Critical'].append("No associated project ("+study_id+")")
    #                 critical += 1

    #             if row_values[2] != "":
    #                 study_title = row_values[2]
    #             else :
    #                 study_error['Critical'].append("No study title ("+study_id+")")
    #                 critical += 1

    #             if row_values[3] != "":
    #                 study_description = row_values[3]
    #             else :
    #                 study_error['Warning'].append("No study description ("+study_id+")")

    #             if row_values[4] != "":
    #                 study_experimental_design = row_values[4]
    #             else :
    #                 study_error['Warning'].append("No experimental design description ("+study_id+")")

    #             if row_values[5] != "":
    #                 study_results = row_values[5]
    #             else :
    #                 study_error['Info'].append("No study results ("+study_id+")")

    #             if row_values[6] != "":
    #                 if row_values[6] == 'Interventional' or row_values[6] == 'Observational' :
    #                     study_type = row_values[6]
    #                 else :
    #                     study_error['Critical'].append("Study type not available ("+study_id+")")
    #                     critical += 1
    #             else :
    #                 study_error['Critical'].append("No study type selected ("+study_id+")")
    #                 critical += 1

    #             if study_type == "Observational" :
    #                 if row_values[7] != "":
    #                     study_inclusion_periode = row_values[7]
    #                 else :
    #                     study_error['Warning'].append("No inclusion period ("+study_id+")")

    #                 if row_values[8] != "":
    #                     study_inclusion = row_values[8]
    #                 else :
    #                     study_error['Warning'].append("No inclusion criteria ("+study_id+")")

    #                 if row_values[9] != "":
    #                     study_exclusion = row_values[9]
    #                 else :
    #                     study_error['Warning'].append("No exclusion criteria ("+study_id+")")

    #                 if row_values[10] != "":
    #                     study_followup = row_values[10]
    #                 else :
    #                     study_error['Warning'].append("No follow up ("+study_id+")")

    #                 if row_values[11] != "":
    #                     study_pop_size = row_values[11]
    #                 else :
    #                     study_error['Warning'].append("No population size ("+study_id+")")

    #                 if row_values[12] != "":
    #                     study_pubmed = row_values[12]
    #                 else :
    #                     study_error['Info'].append("No pubmed ("+study_id+")")


    #             #After reading line add all info in dico project
    #             request.registry.db_mongo['study'].update({'id': 1}, {'$inc': {'val': 1}})
    #             repos = request.registry.db_mongo['study'].find({'id': 1})
    #             id_s = ""
    #             for res in repos:
    #                 id_s = res
                
    #             #Excel id -> databas id
    #             asso_id[study_id] = 'TSE'+str(id_s['val'])
    #             reverse_asso[asso_id[study_id]] = study_id

    #             #Add studies id to associated project
    #             p_stud = projects[study_projects]['studies'].split()
    #             p_stud.append(asso_id[study_id])
    #             projects[study_projects]['studies'] = ','.join(p_stud)

    #             dico={
    #                 'id' : asso_id[study_id],
    #                 'owner' : user,
    #                 'projects' : asso_id[study_projects],
    #                 'assays' : "",
    #                 'factors' : "",
    #                 'signatures' : "",
    #                 'title' : study_title,
    #                 'description' : study_description,
    #                 'experimental_design' : study_experimental_design,
    #                 'results' : study_results,
    #                 'study_type' : study_type,
    #                 'last_update' : str(sdt),
    #                 'inclusion_period': study_inclusion_periode,
    #                 'inclusion': study_inclusion,
    #                 'status' : 'private',
    #                 'followup': study_followup,
    #                 'exclusion' : study_exclusion,
    #                 'pop_size' : study_pop_size,
    #                 'pubmed' : study_pubmed,
    #                 'tags' : "",
    #                 'info' : ','.join(study_error['Info']),
    #                 'warnings' : ','.join(study_error['Warning']),
    #                 'critical' : ','.join(study_error['Critical']),
    #                 'excel_id' : study_id
    #             }      
    #             studies[study_id]=dico

    #     # List of TOXsIgN 'ontologies'
    #     list_developmental_stage = ['Fetal','Embryonic','Larva','Neo-Natal','Juvenile','Pre-pubertal','Pubertal','Adulthood','Elderly','NA']
    #     list_generation = ['f0','f1','f2','f3','f4','f5','f6','f7','f8','f9','f10']
    #     list_experimental = ['in vivo','ex vivo','in vitro','other','NA']
    #     list_sex = ['Male','Female','Both','Other','NA']
    #     list_dose_unit = ['M','mM','µM','g/mL','mg/mL','µg/mL','ng/mL','mg/kg','µg/kg','µg/kg','ng/kg','%']
    #     list_exposure_duration_unit = ['week','day','hour','minute','seconde']
    #     list_exposition_factor = ['Chemical','Physical','Biological']
    #     list_signature_type = ['Physiological','Genomic','Molecular']
    #     list_observed_effect = ['Decrease','Increase','No effect','NA']
        

    #     # Check assay
    #     sh = wb.sheet_by_index(2)
    #     assays={}
    #     for rownum in range(12, sh.nrows):
    #             row_values = sh.row_values(rownum)
    #             if row_values [1] == "" and row_values [2] == "" and row_values [3] =="" :
    #                 continue
    #             assay_error = {'Critical':[],'Warning':[],'Info':[]}

    #             assay_id = row_values[0]
    #             assay_study = ""
    #             assay_title = ""
    #             assay_organism = ""
    #             assay_organism_name = ""
    #             assay_experimental_type = ""
    #             assay_developmental_stage = "" 
    #             assay_generation = ""
    #             assay_sex = ""
    #             assay_tissue = ""
    #             assay_tissue_name = ""
    #             assay_cell = ""
    #             assay_cell_name = ""
    #             assay_cell_line = ""
    #             assay_cell_line_name = ""   
    #             assay_additional_information = "" 
    #             tag = [] 
    #             assay_pop_age = ""
    #             assay_location = ""
    #             assay_reference = ""
    #             assay_matrice = "" 


    #             if row_values[1] != "":
    #                 if row_values[1] in studies:
    #                     assay_study = row_values[1]
    #                 else :
    #                     assay_error['Critical'].append("Studies doesn't exists ("+assay_id+")")
    #                     critical += 1
    #             else :
    #                 study_error['Critical'].append("No associated study ("+assay_id+")")
    #                 critical += 1

    #             if row_values[2] != "":
    #                 assay_title = row_values[2]
    #             else :
    #                 assay_error['Critical'].append("No study title ("+assay_id+")")
    #                 critical += 1

    #             if row_values[4] != "":
    #                 data = request.registry.db_mongo['species.tab'].find_one({'id': row_values[4]})
    #                 if data is None :
    #                     if row_values[3] == "" :
    #                         assay_organism = ""
    #                         assay_error['Critical'].append("Please select an organism in the TOXsIgN ontologies list ("+assay_id+")")
    #                         critical += 1
    #                     else :
    #                         assay_organism_name = row_values[3]
    #                         tag.append(row_values[3])
    #                 else :
    #                     assay_organism = data['name']
    #                     tag.append(data['name'])
    #                     tag.append(data['id'])
    #                     tag.extend(data['synonyms'])
    #                     tag.extend(data['direct_parent'])
    #                     tag.extend(data['all_parent'])
    #                     tag.extend(data['all_name'])
    #                     if row_values[3] != "" :
    #                         assay_organism_name = row_values[3]
    #                         tag.append(row_values[3])
    #             else :
    #                 assay_error['Critical'].append("No organism selected ("+assay_id+")")
    #                 critical += 1

    #             if row_values[5] != "":
    #                 if row_values[5] in  list_developmental_stage :
    #                     assay_developmental_stage = row_values[5]
    #                 else :
    #                     assay_error['Warning'].append("Developmental stage not listed ("+assay_id+")")
    #             else :
    #                 assay_error['Info'].append("No developmental stage selected ("+assay_id+")")
                    

    #             if row_values[6] != "":
    #                 if row_values[6] in  list_generation :
    #                     assay_generation = row_values[6]
    #                 else :
    #                     assay_error['Warning'].append("Generation not listed ("+assay_id+")")
    #             else :
    #                 assay_error['Info'].append("No generation selected ("+assay_id+")")

    #             if row_values[7] != "":
    #                 if row_values[7] in  list_sex :
    #                     assay_sex = row_values[7]
    #                 else :
    #                     assay_error['Warning'].append("Sex not listed ("+assay_id+")")
    #             else :
    #                 assay_error['Info'].append("No sex selected ("+assay_id+")")

    #             if row_values[9] != "":
    #                 data = request.registry.db_mongo['tissue.tab'].find_one({'id': row_values[9]})
    #                 if data is None :
    #                     if row_values[8] != "":
    #                         assay_tissue_name = row_values[8]
    #                         tag.append(assay_tissue_name)
    #                     else :
    #                         assay_tissue = ""
    #                         assay_error['Warning'].append("Please select a tissue in the TOXsIgN ontologies list ("+assay_id+")")
    #                 else :
    #                     assay_tissue = data['name']
    #                     tag.append(data['name'])
    #                     tag.append(data['id'])
    #                     tag.extend(data['synonyms'])
    #                     tag.extend(data['direct_parent'])
    #                     tag.extend(data['all_parent'])
    #                     tag.extend(data['all_name'])
    #                     if row_values[8] != "":
    #                         assay_tissue_name = row_values[8]
    #                         tag.append(assay_tissue_name)

    #             if row_values[11] != "":
    #                 data = request.registry.db_mongo['cell.tab'].find_one({'id': row_values[11]})
    #                 if data is None :
    #                     if row_values[10] != "":
    #                         assay_cell_name = row_values[10]
    #                         tag.append(assay_cell_name)
    #                     else :
    #                         assay_cell = ""
    #                         assay_error['Warning'].append("Please select a cell in the TOXsIgN ontologies list ("+assay_id+")")
    #                 else :
    #                     assay_cell = data['name']
    #                     tag.append(data['name'])
    #                     tag.append(data['id'])
    #                     tag.extend(data['synonyms'])
    #                     tag.extend(data['direct_parent'])
    #                     tag.extend(data['all_parent'])
    #                     tag.extend(data['all_name'])
    #                     if row_values[10] != "":
    #                         assay_cell_name = row_values[10]
    #                         tag.append(assay_cell_name)



    #             if row_values[13] != "":
    #                 data = request.registry.db_mongo['cell_line.tab'].find_one({'id': row_values[13]})
    #                 if data is None :
    #                     if row_values[12] != "":
    #                         assay_cell_line_name = row_values[12]
    #                         tag.append(assay_cell_line_name)
    #                     else :
    #                         assay_cell_line = ""
    #                         assay_error['Warning'].append("Please select a cell line in the TOXsIgN ontologies list ("+assay_id+")")
    #                 else :
    #                     assay_cell_line = data['name']
    #                     tag.append(data['name'])
    #                     tag.append(data['id'])
    #                     tag.extend(data['synonyms'])
    #                     tag.extend(data['direct_parent'])
    #                     tag.extend(data['all_parent'])
    #                     tag.extend(data['all_name'])
    #                     if row_values[12] != "":
    #                         assay_cell_line_name = row_values[12]
    #                         tag.append(assay_cell_line_name)

    #             # Check if at least tissue/cell or cell line are filled
    #             if assay_cell_line == "" and assay_cell == "" and assay_tissue =="" :
    #                 if studies[assay_study]['study_type'] !='Observational' :
    #                     assay_error['Critical'].append("Please select at least a tissue, cell or cell line in the TOXsIgN ontologies list ("+assay_id+")")
    #                     critical += 1

    #             if row_values[14] != "":
    #                 if row_values[14] in  list_experimental :
    #                     assay_experimental_type = row_values[14]


    #             if studies[assay_study]['study_type'] =='Observational' :
    #                 if row_values[15] != "":
    #                     assay_pop_age = row_values[15]
    #                 else :
    #                     assay_error['Info'].append("No population age ("+assay_id+")")

    #                 if row_values[16] != "":
    #                     assay_location = row_values[16]
    #                 else :
    #                     assay_error['Info'].append("No geographical location ("+assay_id+")")

    #                 if row_values[17] != "":
    #                     assay_reference = row_values[17]
    #                 else :
    #                     assay_error['Info'].append("No controle / reference ("+assay_id+")")

    #                 if row_values[18] != "":
    #                     assay_matrice = row_values[18]
    #                 else :
    #                     assay_error['Info'].append("No matrice("+assay_id+")")

    #             if row_values[19] != "":
    #                 assay_additional_information = row_values[19]

    #             #After reading line add all info in dico project
    #             request.registry.db_mongo['assay'].update({'id': 1}, {'$inc': {'val': 1}})
    #             repos = request.registry.db_mongo['assay'].find({'id': 1})
    #             id_a = ""
    #             for res in repos:
    #                 id_a = res
                
    #             #Excel id -> databas id
    #             asso_id[assay_id] = 'TSA'+str(id_a['val'])
    #             reverse_asso[asso_id[assay_id]] = assay_id

    #             #Add assay id to associated study
    #             s_assay = studies[assay_study]['assays'].split()
    #             s_assay.append(asso_id[assay_id])
    #             studies[assay_study]['assays'] = ','.join(s_assay)

    #             #Add assay to the associated project
    #             project_asso = reverse_asso[studies[assay_study]['projects']]

    #             p_assay = projects[project_asso]['assays'].split()
    #             p_assay.append(asso_id[assay_id])
    #             projects[project_asso]['assays'] = ','.join(p_assay)

    #             #After reading line add all info in dico project
    #             dico={
    #                 'id' : asso_id[assay_id] ,
    #                 'studies' : asso_id[assay_study],
    #                 'factors' : "",
    #                 'signatures' : "",
    #                 'projects' : studies[assay_study]['projects'],
    #                 'title' : assay_title,
    #                 'organism' : assay_organism,
    #                 'organism_name' : assay_organism_name,
    #                 'experimental_type' : assay_experimental_type,
    #                 'developmental_stage' : assay_developmental_stage,
    #                 'generation' : assay_generation,
    #                 'sex' : assay_sex,
    #                 'tissue' : assay_tissue,
    #                 'tissue_name' : assay_tissue_name,
    #                 'cell' : assay_cell,
    #                 'cell_name' : assay_cell_name,
    #                 'status' : 'private',
    #                 'last_update' : str(sdt),
    #                 'cell_line' : assay_cell_line,
    #                 'cell_line_name' : assay_cell_line_name,
    #                 'additional_information' : assay_additional_information,
    #                 'population_age' : assay_pop_age,
    #                 'geographical_location':assay_location,
    #                 'reference':assay_reference,
    #                 'matrice':assay_matrice,
    #                 'tags' : ','.join(tag),
    #                 'owner' : user,
    #                 'info' : ','.join(assay_error['Info']),
    #                 'warnings' : ','.join(assay_error['Warning']),
    #                 'critical' : ','.join(assay_error['Critical']),
    #                 'excel_id' : assay_id
    #             }
    #             assays[assay_id] = dico

    #     # Check factor
    #     sh = wb.sheet_by_index(3)
    #     factors={}
    #     for rownum in range(5, sh.nrows):
    #             row_values = sh.row_values(rownum)
    #             if row_values [1] == "" and row_values [2] == "" and row_values [3] =="" and row_values [4] =="" and row_values [5] =="" :
    #                 continue

    #             factor_error = {'Critical':[],'Warning':[],'Info':[]}
        
    #             factor_id = row_values[0]
    #             factor_type = ""
    #             factor_assay = ""
    #             factor_chemical = ""
    #             factor_chemical_name = ""
    #             factor_physical = ""
    #             factor_biological = ""
    #             factor_route = ""
    #             factor_vehicle  = ""
    #             factor_dose = ""
    #             factor_dose_unit = ""
    #             factor_exposure_duration = ""
    #             factor_exposure_duration_unit = ""
    #             factor_exposure_frequecies = ""
    #             factor_additional_information = ""
    #             tag = []


    #             if row_values[1] != "":
    #                 if row_values[1] in assays:
    #                     factor_assay = row_values[1]
    #                 else :
    #                     factor_error['Critical'].append("Assay doesn't exists ("+factor_id+")")
    #                     critical += 1
    #             else :
    #                 factor_error['Critical'].append("No associated study ("+factor_id+")")
    #                 critical += 1

    #             if row_values[2] != "":
    #                 if row_values[2] in  list_exposition_factor :
    #                     factor_type = row_values[2]
    #                 else :
    #                     factor_error['Critical'].append("Exposition factor not listed ("+factor_id+")")
    #                     critical += 1
    #             else :
    #                 factor_error['Critical'].append("No exposition factor selected ("+factor_id+")")
    #                 critical += 1

    #             if row_values[4] != "":
    #                 data = request.registry.db_mongo['chemical.tab'].find_one({'id': row_values[4]})
    #                 if data is None :
    #                     if row_values[3] != "":
    #                         factor_chemical_name = row_values[3]
    #                         tag.append(factor_chemical_name)
    #                     else :
    #                         factor_chemical = ""
    #                         factor_error['Warning'].append("Chemical not in the TOXsIgN ontologies list ("+factor_id+")")
    #                 else :
    #                     factor_chemical = data['name']
    #                     tag.append(data['name'])
    #                     tag.append(data['id'])
    #                     tag.extend(data['synonyms'])
    #                     tag.extend(data['direct_parent'])
    #                     tag.extend(data['all_parent'])
    #                     tag.extend(data['all_name'])
    #                     if row_values[3] != "":
    #                         factor_chemical_name = row_values[3]
    #                         tag.append(factor_chemical_name)      
    #             else :
    #                 assay_error['Warning'].append("No chemical selected ("+factor_id+")")

    #             if row_values[5] != "":
    #                 data = request.registry.db_mongo['chemical.tab'].find_one({'id': row_values[5]})
    #                 if data is None :
    #                     data =  'false'
    #                 else :
    #                     data = 'true'
    #                 if data == 'true' :
    #                     factor_physical = row_values[5]
    #                 else :
    #                     a =1
    #                     #factor_error['Warning'].append("Physical factor not in the TOXsIgN ontologies (not available yet) ("+factor_id+")")
    #             else :
    #                 a =1
    #                 #factor_error['Warning'].append("No physical factor selected (not available yet) ("+factor_id+")")

    #             if row_values[6] != "":
    #                 data = request.registry.db_mongo['chemical.tab'].find_one({'id': row_values[6]})
    #                 if data is None :
    #                     data =  'false'
    #                 else :
    #                     data = 'true'
    #                 if data == 'true' :
    #                     factor_biological = row_values[6]
    #                 else :
    #                     a=1
    #                     f#actor_error['Warning'].append("Biological factor notin the TOXsIgN ontologies (not available yet) ("+factor_id+")")
    #             else :
    #                 a=1
    #                 #factor_error['Warning'].append("No biological factor selected (not available yet) ("+factor_id+")")

    #             if row_values[7] != "":
    #                 factor_route = row_values[7]
    #             else :
    #                 factor_error['Info'].append("No route ("+factor_id+")")

    #             if row_values[8] != "":
    #                 factor_vehicle = row_values[8]
    #             else :
    #                 factor_error['Info'].append("No vehicle ("+factor_id+")")

    #             if row_values[9] != "":
    #                 factor_dose = row_values[9]
    #             else :
    #                 factor_error['Critical'].append("Factor dose required ("+factor_id+")")
    #                 critical += 1
    #             try :
    #                 if row_values[10] != "":
    #                     if str(row_values[10]) in list_dose_unit :
    #                         factor_dose_unit = str(row_values[10])
    #                     else :
    #                         factor_dose_unit = row_values[10]
    #             except:
    #                 factor_dose_unit = row_values[10]

    #             if row_values[11] != "":
    #                 factor_exposure_duration = row_values[11]
    #             else :
    #                 factor_error['Critical'].append("Factor exposure duration required ("+factor_id+")")
    #                 critical += 1

    #             if row_values[12] != "":
    #                 if row_values[12] in list_exposure_duration_unit :
    #                     factor_exposure_duration_unit = row_values[12]
    #                 else :
    #                     factor_exposure_duration_unit = row_values[12]

    #             if row_values[13] != "":
    #                 factor_exposure_frequecies = row_values[13]

    #             if row_values[14] != "":
    #                 factor_additional_information = row_values[14]
        


    #             #After reading line add all info in dico project
    #             request.registry.db_mongo['factor'].update({'id': 1}, {'$inc': {'val': 1}})
    #             repos = request.registry.db_mongo['factor'].find({'id': 1})
    #             id_a = ""
    #             for res in repos:
    #                 id_f = res
                
    #             #Excel id -> databas id
    #             asso_id[factor_id] = 'TSF'+str(id_f['val'])
    #             reverse_asso[asso_id[factor_id]] = factor_id

    #             #Add factor id to associated assay
    #             a_factor = assays[factor_assay]['factors'].split()
    #             a_factor.append(asso_id[factor_id])
    #             assays[factor_assay]['factors'] = ','.join(a_factor)

    #             #Add factor to the associated study
    #             study_asso = reverse_asso[assays[factor_assay]['studies']]

    #             s_factor = studies[study_asso]['factors'].split()
    #             s_factor.append(asso_id[factor_id])
    #             studies[study_asso]['factors'] = ','.join(s_factor)

    #             #Add factor to the associated project
    #             project_asso = reverse_asso[assays[factor_assay]['projects']]

    #             p_factor = projects[project_asso]['factors'].split()
    #             p_factor.append(asso_id[factor_id])
    #             projects[project_asso]['factors'] = ','.join(p_factor)

    #             #up factor tags to associated assy 
    #             tag_assay = assays[factor_assay]['tags'].split(',')
    #             tag_assay.extend(tag)
    #             assays[factor_assay]['tags'] = ','.join(tag_assay)

    #             #After reading line add all info in dico project
    #             try :
    #                 dico={
    #                     'id' : asso_id[factor_id],
    #                     'assays' : asso_id[factor_assay],
    #                     'studies' : assays[factor_assay]['studies'],
    #                     'project' : assays[factor_assay]['projects'],
    #                     'type' : factor_type,
    #                     'chemical' : factor_chemical,
    #                     'chemical_name' : factor_chemical_name,
    #                     'physical' : factor_physical,
    #                     'biological' : factor_biological,
    #                     'route' : factor_route,
    #                     'last_update' : str(sdt),
    #                     'status' : 'private',
    #                     'vehicle' : factor_vehicle,
    #                     'dose' : str(factor_dose) +" "+ factor_dose_unit,
    #                     'exposure_duration' : str(factor_exposure_duration) +" "+ factor_exposure_duration_unit,
    #                     'exposure_frequencies' : factor_exposure_frequecies,
    #                     'additional_information' : factor_additional_information,
    #                     'tags' : ','.join(tag),
    #                     'owner' : user,
    #                     'info' : ','.join(factor_error['Info']),
    #                     'warnings' : ','.join(factor_error['Warning']),
    #                     'critical' : ','.join(factor_error['Critical']),
    #                     'excel_id' : factor_id
    #                 }
    #             except :
    #                 dico={
    #                     'id' : asso_id[factor_id],
    #                     'assays' : asso_id[factor_assay],
    #                     'studies' : assays[factor_assay]['studies'],
    #                     'project' : assays[factor_assay]['projects'],
    #                     'type' : factor_type,
    #                     'chemical' : factor_chemical,
    #                     'chemical_name' : factor_chemical_name,
    #                     'physical' : factor_physical,
    #                     'biological' : factor_biological,
    #                     'route' : factor_route,
    #                     'last_update' : str(sdt),
    #                     'status' : 'private',
    #                     'vehicle' : factor_vehicle,
    #                     'dose' : factor_dose +" "+ factor_dose_unit,
    #                     'exposure_duration' : factor_exposure_duration +" "+ factor_exposure_duration_unit,
    #                     'exposure_frequencies' : factor_exposure_frequecies,
    #                     'additional_information' : factor_additional_information,
    #                     'tags' : ','.join(tag),
    #                     'owner' : user,
    #                     'info' : ','.join(factor_error['Info']),
    #                     'warnings' : ','.join(factor_error['Warning']),
    #                     'critical' : ','.join(factor_error['Critical']),
    #                     'excel_id' : factor_id
    #                 }
    #             factors[factor_id] = dico


    #     # Check signatures
    #     sh = wb.sheet_by_index(4)
    #     signatures={}
    #     for rownum in range(6, sh.nrows):
    #             row_values = sh.row_values(rownum)
    #             if row_values [1] == "" and row_values [2] == "" and row_values [3] =="" and row_values [4] =="" and row_values [5] =="" :
    #                 continue

    #             signature_error = {'Critical':[],'Warning':[],'Info':[]}

    #             signature_id = row_values[0]
    #             signature_associated_study = ""
    #             signature_associated_assay = ""
    #             signature_title = ""
    #             signature_type = ""
    #             signature_organism = ""
    #             signature_organism_name = ""
    #             signature_developmental_stage = ""
    #             signature_generation = ""
    #             signature_sex = ""
    #             signature_tissue = ""
    #             signature_tissue_name = ""
    #             signature_cell = ""
    #             signature_cell_name = "" 
    #             signature_cell_line = ""
    #             signature_cell_line_name = ""
    #             signature_molecule = ""
    #             signature_molecule_name = ""
    #             signature_pathology = ""
    #             signature_technology = ""
    #             signature_technology_name = ""
    #             signature_plateform = ""
    #             signature_observed_effect = ""
    #             signature_control_sample = ""
    #             signature_treated_sample = ""
    #             signature_pvalue = ""
    #             signature_cutoff = "" 
    #             signature_satistical_processing = ""
    #             signature_additional_file = ""
    #             signature_file_up = "" 
    #             signature_file_down = ""
    #             signature_file_interrogated = ""
    #             signature_genes_identifier = ""
    #             signature_study_type= ""
    #             signature_description = ""

    #             signature_controle = ""
    #             signature_case = ""
    #             signature_significance = ""
    #             signature_stat_value = ""
    #             signature_stat_adjust = ""
    #             signature_stat_other = ""
    #             signature_group = ""
    #             signature_pop_age = ""
    #             tag = []

    #             if row_values[1] != "":
    #                 if row_values[1] in studies:
    #                     signature_associated_study = row_values[1]
    #                 else :
    #                     signature_error['Critical'].append("Study doesn't exists ("+signature_id+")")
    #                     critical += 1
    #             else :
    #                 signature_error['Critical'].append("No associated study ("+signature_id+")")
    #                 critical += 1

    #             if row_values[2] != "":
    #                 if row_values[2] in assays:
    #                     signature_associated_assay = row_values[2]
    #                 else :
    #                     signature_error['Critical'].append("Assay doesn't exists ("+signature_id+")")
    #                     critical += 1
    #             else :
    #                 signature_error['Critical'].append("No associated assay ("+signature_id+")")
    #                 critical += 1

    #             if row_values[3] != "":
    #                 signature_title = row_values[3]
    #             else :
    #                 signature_error['Critical'].append("No signature title ("+signature_id+")")
    #                 critical += 1

    #             if row_values[4] != "":
    #                 if row_values[4] in list_signature_type : 
    #                     signature_type = row_values[4]
    #                 else :
    #                     signature_error['Critical'].append("Signature title not in the list ("+signature_id+")")
    #                     critical += 1
    #             else :
    #                 signature_error['Critical'].append("No type of signature ("+signature_id+")")
    #                 critical += 1

    #             if row_values[6] != "":
    #                 data = request.registry.db_mongo['species.tab'].find_one({'id': row_values[6]})
    #                 if data is None :
    #                     if row_values[5] != "":
    #                         signature_organism_name = row_values[5]
    #                         tag.append(signature_organism_name)
    #                     else :
    #                         signature_organism = ""
    #                         signature_error['Critical'].append("Please select an organism in the TOXsIgN ontologies list ("+signature_id+")")
    #                         critical += 1
    #                 else :
    #                     signature_organism = data['name']
    #                     tag.append(data['name'])
    #                     tag.append(data['id'])
    #                     tag.extend(data['synonyms'])
    #                     tag.extend(data['direct_parent'])
    #                     tag.extend(data['all_parent'])
    #                     tag.extend(data['all_name'])
    #                     if row_values[5] != "":
    #                         signature_organism = row_values[5]
    #                         tag.append(signature_organism_name)   
    #             else :
    #                 signature_error['Critical'].append("No organism selected ("+signature_id+")")
    #                 critical += 1

    #             if row_values[7] != "":
    #                 if row_values[7] in  list_developmental_stage :
    #                     signature_developmental_stage = row_values[7]
    #                 else :
    #                     signature_error['Warning'].append("Developmental stage not listed ("+signature_id+")")
    #             else :
    #                 signature_error['Info'].append("No developmental stage selected ("+signature_id+")")
                    

    #             if row_values[8] != "":
    #                 if row_values[8] in  list_generation :
    #                     signature_generation = row_values[8]
    #                 else :
    #                     signature_error['Warning'].append("Generation not listed ("+signature_id+")")
    #             else :
    #                 signature_error['Info'].append("No generation selected ("+signature_id+")")

    #             if row_values[9] != "":
    #                 if row_values[9] in  list_sex :
    #                     signature_sex = row_values[9]
    #                 else :
    #                     signature_error['Warning'].append("Sex not listed ("+signature_id+")")
    #             else :
    #                 signature_error['Info'].append("No sex selected ("+signature_id+")")

    #             if row_values[11] != "":
    #                 data = request.registry.db_mongo['tissue.tab'].find_one({'id': row_values[1]})
    #                 if data is None :
    #                     if row_values[10] != "":
    #                         signature_tissue_name = row_values[10]
    #                         tag.append(signature_tissue_name)
    #                     else :
    #                         signature_tissue = ""
    #                 else :
    #                     signature_tissue = data['name']
    #                     tag.append(data['name'])
    #                     tag.append(data['id'])
    #                     tag.extend(data['synonyms'])
    #                     tag.extend(data['direct_parent'])
    #                     tag.extend(data['all_parent'])
    #                     tag.extend(data['all_name'])
    #                     if row_values[10] != "":
    #                         signature_tissue_name = row_values[10]
    #                         tag.append(signature_tissue_name)  

    #             if row_values[13] != "":
    #                 data = request.registry.db_mongo['cell.tab'].find_one({'id': row_values[13]})
    #                 if data is None :
    #                     if row_values[12] != "":
    #                         signature_cell_name = row_values[12]
    #                         tag.append(signature_cell_name)
    #                     else :
    #                         signature_cell = ""
    #                 else :
    #                     signature_cell = data['name']
    #                     tag.append(data['name'])
    #                     tag.append(data['id'])
    #                     tag.extend(data['synonyms'])
    #                     tag.extend(data['direct_parent'])
    #                     tag.extend(data['all_parent'])
    #                     tag.extend(data['all_name']) 
    #                     if row_values[12] != "":
    #                         signature_cell_name = row_values[12]
    #                         tag.append(signature_cell_name)  

    #             if row_values[15] != "":
    #                 data = request.registry.db_mongo['cell_line.tab'].find_one({'id': row_values[15]})
    #                 if data is None :
    #                     if row_values[14] != "":
    #                         signature_cell_line_name = row_values[14]
    #                         tag.append(signature_cell_line_name)
    #                     else :
    #                         signature_cell_line = ''
    #                 else :
    #                     signature_cell_line = data['name']
    #                     tag.append(data['name'])
    #                     tag.append(data['id'])
    #                     tag.extend(data['synonyms'])
    #                     tag.extend(data['direct_parent'])
    #                     tag.extend(data['all_parent'])
    #                     tag.extend(data['all_name'])
    #                     if row_values[14] != "":
    #                         signature_cell_line_name = row_values[14]
    #                         tag.append(signature_cell_line_name)   

    #             # Check if at least tissue/cell or cell line are filled
    #             if signature_cell_line == "" and signature_cell == "" and signature_tissue =="" :
    #                 if studies[signature_associated_study]['study_type'] != 'Observational' :
    #                     signature_error['Critical'].append("Please select at least a tissue, cell or cell line in the TOXsIgN ontologies list ("+signature_id+")")
    #                     critical += 1

    #             if row_values[17] != "":
    #                 data = request.registry.db_mongo['chemical.tab'].find_one({'id': row_values[17]})
    #                 if data is None :
    #                     if row_values[16] != "" :
    #                         signature_molecule_name = row_values[16]
    #                         tag.append(signature_molecule_name)
    #                     else :
    #                         signature_molecule = ""
    #                 else :
    #                     signature_molecule = data['name']
    #                     tag.append(data['name'])
    #                     tag.append(data['id'])
    #                     tag.extend(data['synonyms'])
    #                     tag.extend(data['direct_parent'])
    #                     tag.extend(data['all_parent'])
    #                     tag.extend(data['all_name'])
    #                     if row_values[16] != "" :
    #                         signature_molecule_name = row_values[16]
    #                         tag.append(signature_molecule_name)   


    #             if row_values[18] != "":
    #                 signature_description = row_values[18]
    #                 tag.extend(signature_description)

    #             if row_values[19] != "":
    #                 data = request.registry.db_mongo['disease.tab'].find_one({'id': row_values[19]})
    #                 if data is None :
    #                     signature_pathology = ""
    #                     signature_error['Warning'].append("Pathology / disease not in TOXsIgN ontology ("+signature_id+")")
    #                 else :
    #                     signature_pathology = data['name']
    #                     tag.append(data['name'])
    #                     tag.append(data['id'])
    #                     tag.extend(data['synonyms'])
    #                     tag.extend(data['direct_parent'])
    #                     tag.extend(data['all_parent'])
    #                     tag.extend(data['all_name'])


    #             if row_values[21] != "":
    #                 data = request.registry.db_mongo['experiment.tab'].find_one({'id': row_values[21]})
    #                 if data is None :
    #                     if row_values[20] != "":
    #                         signature_technology_name = row_values[20]
    #                         tag.append(signature_technology_name)
    #                     else :
    #                         signature_technology = ""
    #                         if signature_type == "Genomic":
    #                             signature_error['Warning'].append("Technology not in TOXsIgN ontology ("+signature_id+")")
    #                 else :
    #                     signature_technology = data['name']
    #                     tag.append(data['name'])
    #                     tag.append(data['id'])
    #                     tag.extend(data['synonyms'])
    #                     tag.extend(data['direct_parent'])
    #                     tag.extend(data['all_parent'])
    #                     tag.extend(data['all_name'])
    #                     if row_values[20] != "":
    #                         signature_technology_name = row_values[20]
    #                         tag.append(signature_technology_name)              
    #             else :
    #                 if signature_type == "Genomic":
    #                     signature_error['Warning'].append("No technology selected ("+signature_id+")")

    #             if row_values[22] != "":
    #                 signature_plateform = row_values[22]
    #             else :
    #                 if signature_type == "Genomic":
    #                     signature_error['Info'].append("No plateform selected ("+signature_id+")")


    #             if row_values[23] != "":
    #                 signature_controle = row_values[23]


    #             if row_values[24] != "":
    #                 signature_case = row_values[24]


    #             if row_values[25] != "":
    #                 signature_group = row_values[25]


    #             if row_values[26] != "":
    #                 signature_group = row_values[26]


    #             if row_values[27] != "":
    #                 if row_values[27] in  list_observed_effect :
    #                     signature_observed_effect= row_values[27]
    #                 else :
    #                     signature_error['Warning'].append("Observed effect not listed ("+signature_id+")")

    #             if row_values[28] != "":
    #                 signature_significance = row_values[28]
    #             else :
    #                 if studies[signature_associated_study]['study_type'] == 'Observational' :
    #                     signature_error['Info'].append("No statistical significance ("+signature_id+")")

    #             if row_values[29] != "":
    #                 signature_stat_value = row_values[29]
    #             else :
    #                 if studies[signature_associated_study]['study_type'] == 'Observational' :
    #                     signature_error['Info'].append("No statistical value ("+signature_id+")")

    #             if row_values[30] != "":
    #                 signature_stat_adjust = row_values[30]
    #             else :
    #                 if studies[signature_associated_study]['study_type'] == 'Observational' :
    #                     signature_error['Info'].append("No statistical adjustment ("+signature_id+")")

    #             if row_values[31] != "":
    #                 signature_stat_other = row_values[31]





    #             if row_values[32] != "":
    #                 signature_control_sample = row_values[32]
    #             else :
    #                 if studies[signature_associated_study]['study_type'] != 'Observational' :
    #                     signature_error['Info'].append("No control sample ("+signature_id+")")

    #             if row_values[33] != "":
    #                 signature_treated_sample = row_values[33]
    #             else :
    #                 if studies[signature_associated_study]['study_type'] != 'Observational' :
    #                     signature_error['Info'].append("No treated sample ("+signature_id+")")

    #             if row_values[34] != "":
    #                 signature_pvalue = row_values[34]
    #             else :
    #                 if studies[signature_associated_study]['study_type'] != 'Observational' :
    #                     signature_error['Info'].append("No pvalue ("+signature_id+")")

    #             if row_values[35] != "":
    #                 signature_cutoff = row_values[36]
    #             else :
    #                 if studies[signature_associated_study]['study_type'] != 'Observational' :
    #                     signature_error['Info'].append("No cutoff ("+signature_id+")")

    #             if row_values[36] != "":
    #                 signature_satistical_processing = row_values[36]
    #             else :
    #                 if studies[signature_associated_study]['study_type'] != 'Observational' :
    #                     signature_error['Info'].append("No statistical processing ("+signature_id+")")

    #             if row_values[37] != "":
    #                 signature_additional_file = row_values[37]
    #             else :
    #                 signature_error['Info'].append("No additional file ("+signature_id+")")

    #             if row_values[38] != "":
    #                 signature_file_up = row_values[38]
    #             else :
    #                 if signature_type == "Genomic":
    #                     signature_error['Critical'].append("No signature file (up genes) ("+signature_id+")")
    #                     critical += 1

    #             if row_values[39] != "":
    #                 signature_file_down = row_values[39]
    #             else :
    #                 if signature_type == "Genomic":
    #                     signature_error['Critical'].append("No signature file (down genes) ("+signature_id+")")
    #                     critical +=1

    #             if row_values[40] != "":
    #                 signature_file_interrogated = row_values[40]
    #             else :
    #                 if signature_type == "Genomic":
    #                     signature_error['Critical'].append("No signature file (interrogated genes) ("+signature_id+")")
    #                     critical += 1

    #             if row_values[41] != "":
    #                 signature_genes_identifier = row_values[41]
    #             else :
    #                 if signature_type == "Genomic":
    #                     signature_error['Info'].append("No gene identifier selected ("+signature_id+")")
    #                     critical += 1

    #             #After reading line add all info in dico project
    #             #After reading line add all info in dico project
    #             request.registry.db_mongo['signature'].update({'id': 1}, {'$inc': {'val': 1}})
    #             repos = request.registry.db_mongo['signature'].find({'id': 1})
    #             id_a = ""
    #             for res in repos:
    #                 id_si = res
                
    #             #Excel id -> databas id
    #             asso_id[signature_id] = 'TSS'+str(id_si['val'])
    #             reverse_asso[asso_id[signature_id]] = signature_id

    #             #Add signature id to associated assay
    #             a_signature = assays[signature_associated_assay]['signatures'].split()

    #             a_signature.append(asso_id[signature_id])
    #             assays[signature_associated_assay]['signatures'] = ','.join(a_signature)

    #             #Add factor to the associated study

    #             s_signature = studies[signature_associated_study]['signatures'].split()
    #             s_signature.append(asso_id[signature_id])
    #             studies[signature_associated_study]['signatures'] = ','.join(s_signature)

    #             #Add factor to the associated project
    #             project_asso = reverse_asso[studies[signature_associated_study]['projects']]

    #             p_signature = projects[project_asso]['signatures'].split()
    #             p_signature.append(asso_id[signature_id])
    #             projects[project_asso]['signatures'] = ','.join(p_signature)

    #             #get factors
    #             tag.extend(assays[signature_associated_assay]['tags'].split(','))
    #             myset = list(set(tag))
    #             tag = myset
                
    #             signature_study_type = studies[signature_associated_study]['study_type']
    #             dico ={
    #                 'id' : asso_id[signature_id],
    #                 'studies' : asso_id[signature_associated_study],
    #                 'assays' : asso_id[signature_associated_assay],
    #                 'projects' : studies[signature_associated_study]['projects'] ,
    #                 'title' : signature_title,
    #                 'type' : signature_type,
    #                 'organism' : signature_organism,
    #                 'organism_name' : signature_organism_name,
    #                 'developmental_stage' : signature_developmental_stage,
    #                 'generation' : signature_generation,
    #                 'sex' : signature_sex,
    #                 'last_update' : str(sdt),
    #                 'tissue' : signature_tissue,
    #                 'tissue_name' : signature_tissue_name,
    #                 'cell' : signature_cell,
    #                 'cell_name' : signature_cell_name,
    #                 'status' : 'private',
    #                 'cell_line' : signature_cell_line,
    #                 'cell_line_name' : signature_cell_line_name,
    #                 'molecule' : signature_molecule,
    #                 'molecule_name' : signature_molecule_name,
    #                 'pathology' : signature_pathology,
    #                 'technology' : signature_technology,
    #                 'description' : signature_description,
    #                 'technology_name' : signature_technology_name,
    #                 'plateform' : signature_plateform,
    #                 'observed_effect' : signature_observed_effect,
    #                 'control_sample' : str(signature_control_sample),
    #                 'treated_sample' : str(signature_treated_sample),
    #                 'pvalue' : str(signature_pvalue),
    #                 'cutoff' : str(signature_cutoff),
    #                 'statistical_processing' : signature_satistical_processing,
    #                 'additional_file' : signature_additional_file,
    #                 'file_up' : signature_file_up,
    #                 'file_down' : signature_file_down,
    #                 'file_interrogated' : signature_file_interrogated,
    #                 'genes_identifier': signature_genes_identifier,
    #                 'controle':signature_controle,
    #                 'case':signature_case,
    #                 'significance':signature_significance,
    #                 'stat_val' : signature_stat_value,
    #                 'stat_adjust' : signature_stat_adjust,
    #                 'stat_other' : signature_stat_other,
    #                 'study_type' :signature_study_type,
    #                 'group' : signature_group,
    #                 'pop_age' : signature_pop_age,
    #                 'tags' : ','.join(tag),
    #                 'owner' : user,
    #                 'info' : ','.join(signature_error['Info']),
    #                 'warnings' : ','.join(signature_error['Warning']),
    #                 'critical' : ','.join(signature_error['Critical']),
    #                 'excel_id' : signature_id,
    #                 'genes_up' : "",
    #                 'genes_down' : ""
    #             }
    #             signatures[signature_id] = dico
        


    #     # Create user project directory + move tmp
    #     for proj in projects :
    #         ID = projects[proj]['id']
    #         projects[proj]['edges']  = {}
    #         for stud in studies:
    #             projects[proj]['edges'][studies[stud]['id']] = studies[stud]['assays'].split()
    #         for ass in assays:
    #             projects[proj]['edges'][assays[ass]['id']] = assays[ass]['signatures'].split()

    #         projects[proj]['edges'] = json.dumps(projects[proj]['edges'])
    #         upload_path = os.path.join(request.registry.upload_path, user, ID)
    #         final_file = 'TOXsIgN_'+ID+'.xlsx'
    #         if not os.path.exists(upload_path):
    #             os.makedirs(upload_path)
    #         os.rename(input_file, os.path.join(upload_path, final_file))
    #         request.registry.db_mongo['projects'].insert(projects[proj])

    #     for stud in studies:
    #         request.registry.db_mongo['studies'].insert(studies[stud])

    #     for ass in assays:
    #         request.registry.db_mongo['assays'].insert(assays[ass])

    #     for fac in factors:
    #         request.registry.db_mongo['factors'].insert(factors[fac])

    #     for sign in signatures:
    #         request.registry.db_mongo['signatures'].insert(signatures[sign])


    #     return {'msg':"File checked and uploded !", 'status':'0'}
    # except:
    #     logger.warning("Error - Save excel file")
    #     logger.warning(sys.exc_info())
    #     return {'msg':'An error occurred while uploading your file. If the error persists please contact TOXsIgN support ','status':'1'}





@view_config(route_name='update_dataset', renderer='json', request_method='POST')
def update_dataset(request):
    session_user = is_authenticated(request)
    if session_user is None:
        return 'HTTPForbidden()'

    input_file = None
    form = json.loads(request.body, encoding=request.charset)
    user = form['uid']
  
    try:
        input_file = form['file']
    except Exception:
        return HTTPForbidden('no input file')
    try:
        pid = form['pid']
    except Exception:
        return HTTPForbidden('no project associated')
    studies = []
    assays = []
    factors = []
    signatres = []

    print 'update file'
    print form['pid']
    p_project = request.registry.db_mongo['projects'].find_one({'id': form['pid']})
    pstudies = p_project['studies'].split(',')
    passays = p_project['assays'].split(',')
    pfactors = p_project['factors'].split(',')
    psignatures = p_project['signatures'].split(',')

    asso_id = {}
    reverse_asso = {}

    #Read excel file
    wb = xlrd.open_workbook(input_file,encoding_override="cp1251")
    #Read project
    sh = wb.sheet_by_index(0)
    projects={}
    critical = 0
    dt = datetime.datetime.utcnow()
    sdt = time.mktime(dt.timetuple())
    try :
        for rownum in range(5, sh.nrows):
            row_values = sh.row_values(rownum)
            if row_values [1] == "" and row_values [2] == "" and row_values [3] =="" :
                continue
            project_error = {'Critical':[],'Warning':[],'Info':[]}

            project_id = row_values[0]
            project_title = ""
            project_description = ""
            project_pubmed = ""
            project_contributors=""
            project_crosslink = ""

            if row_values[1] != "":
                project_title = row_values[1]
            else :
                project_error['Critical'].append("No project title ("+project_id+")")
                critical += 1

            if row_values[2] != "":
                project_description = row_values[2]
            else :
                project_error['Warning'].append("No project description ("+project_id+")")

            if str(row_values[3]) != "" :
                if ';' in str(row_values[3]) or '|' in str(row_values[3]):
                    project_error['Critical'].append("Use comma to separate your pubmed ids ("+project_id+")")
                    critical += 1
                else :
                    project_pubmed = str(row_values[3])
            else :
                project_error['Info'].append("No associated pubmed Id(s)")

            if row_values[4] != "" :
                if ';' in row_values[4] or '|' in row_values[4]:
                    project_error['Critical'].append("Use comma to separate your contributors ("+project_id+")")
                    critical += 1
                else :
                    project_contributors = row_values[4]
            else :
                project_error['Info'].append("No associated contributors ("+project_id+")")

            if row_values[5] != "" :
                if ';' in row_values[5] or '|' in row_values[5]:
                    project_error['Critical'].append("Use comma to separate your links ("+project_id+")")
                    critical += 1
                else :
                    project_crosslink = row_values[5]
            else :
                project_error['Info'].append("No cross link(s) ("+project_id+")")


            #After reading line add all info in dico project

            #Excel id -> databas id
            asso_id[project_id] =  p_project['id']
            reverse_asso[asso_id[project_id]] = project_id

            dico={
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
                }
            
            if p_project['excel_id'] == project_id :
                projects[project_id] = dico
            else :
                return {'msg':'Error in template format (project id ?) '}

        # Check studies
        sh = wb.sheet_by_index(1)
        studies={}
        l_excelId = []
        for stud in pstudies :
            study = request.registry.db_mongo['studies'].find_one({'id': stud})
            if study is not None :
                l_excelId.append(study['excel_id'])


        for rownum in range(6, sh.nrows):
                row_values = sh.row_values(rownum)
                if row_values [1] == "" and row_values [2] == "" and row_values [3] =="" :
                    continue
                study_error = {'Critical':[],'Warning':[],'Info':[]}

                study_id = row_values[0]
                study_projects = ""
                study_title = ""
                study_description=""
                study_experimental_design=""
                study_results=""
                study_type = ""
                study_inclusion_periode = ""
                study_inclusion = ""
                study_exclusion = ""
                study_followup = ""
                study_pubmed = ""
                study_pop_size = ""
                study_pubmed = ""

                if row_values[1] != "":
                    if row_values[1] in projects:
                        study_projects = row_values[1]
                    else :
                        study_error['Critical'].append("Project doesn't exists ("+study_id+")")
                        critical += 1
                else :
                    study_error['Critical'].append("No associated project ("+study_id+")")
                    critical += 1

                if row_values[2] != "":
                    study_title = row_values[2]
                else :
                    study_error['Critical'].append("No study title ("+study_id+")")
                    critical += 1

                if row_values[3] != "":
                    study_description = row_values[3]
                else :
                    study_error['Warning'].append("No study description ("+study_id+")")

                if row_values[4] != "":
                    study_experimental_design = row_values[4]
                else :
                    study_error['Warning'].append("No experimental design description ("+study_id+")")

                if row_values[5] != "":
                    study_results = row_values[5]
                else :
                    study_error['Info'].append("No study results ("+study_id+")")

                if row_values[6] != "":
                    if row_values[6] == 'Interventional' or row_values[6] == 'Observational' :
                        study_type = row_values[6]
                    else :
                        study_error['Critical'].append("Study type not available ("+study_id+")")
                        critical += 1
                else :
                    study_error['Critical'].append("No study type selected ("+study_id+")")
                    critical += 1

                if study_type == "Observational" :
                    if row_values[7] != "":
                        study_inclusion_periode = row_values[7]
                    else :
                        study_error['Warning'].append("No inclusion period ("+study_id+")")

                    if row_values[8] != "":
                        study_inclusion = row_values[8]
                    else :
                        study_error['Warning'].append("No inclusion criteria ("+study_id+")")

                    if row_values[9] != "":
                        study_exclusion = row_values[9]
                    else :
                        study_error['Warning'].append("No exclusion criteria ("+study_id+")")

                    if row_values[10] != "":
                        study_followup = row_values[10]
                    else :
                        study_error['Warning'].append("No follow up ("+study_id+")")

                    if row_values[11] != "":
                        study_pop_size = row_values[11]
                    else :
                        study_error['Warning'].append("No population size ("+study_id+")")

                    if row_values[12] != "":
                        study_pubmed = row_values[12]
                    else :
                        study_error['Info'].append("No pubmed ("+study_id+")")

                if study_id in l_excelId :
                    for stud in pstudies :
                        if study is not None :
                            study = request.registry.db_mongo['studies'].find_one({'id': stud})
                            if study['excel_id'] == study_id :

                                asso_id[study_id] = study['id']
                                reverse_asso[asso_id[study_id]] = study_id 

                                #Add studies id to associated project
                                p_stud = projects[study_projects]['studies'].split()
                                p_stud.append(asso_id[study_id])
                                p_stud = list(set(p_stud))
                                projects[study_projects]['studies'] = ','.join(p_stud)

                                dico={
                                    'id' : study['id'],
                                    'owner' : user,
                                    'projects' : asso_id[study_projects],
                                    'assays' : "",
                                    'factors' : "",
                                    'status' : 'private' ,
                                    'signatures' : study['signatures'],
                                    'title' : study_title,
                                    'description' : study_description,
                                    'experimental_design' : study_experimental_design,
                                    'results' : study_results,
                                    'study_type' : study_type,
                                    'last_update' : str(sdt),
                                    'inclusion_period': study_inclusion_periode,
                                    'inclusion': study_inclusion,
                                    'followup': study_followup,
                                    'exclusion' : study_exclusion,
                                    'pop_size' : study_pop_size,
                                    'pubmed' : study_pubmed,
                                    'tags' : "",
                                    'info' : ','.join(study_error['Info']),
                                    'warnings' : ','.join(study_error['Warning']),
                                    'critical' : ','.join(study_error['Critical']),
                                    'excel_id' : study_id
                                } 
                                    
                                studies[study_id] = dico
                else : 

                    #After reading line add all info in dico project
                    request.registry.db_mongo['study'].update({'id': 1}, {'$inc': {'val': 1}})
                    repos = request.registry.db_mongo['study'].find({'id': 1})
                    id_s = ""
                    for res in repos:
                        id_s = res
                    
                    #Excel id -> databas id
                    asso_id[study_id] = 'TSE'+str(id_s['val'])
                    reverse_asso[asso_id[study_id]] = study_id

                    p_stud = projects[study_projects]['studies'].split()
                    p_stud.append(asso_id[study_id])
                    p_stud = list(set(p_stud))
                    projects[study_projects]['studies'] = ','.join(p_stud)

                   #Excel id -> databas id


                    dico={
                        'id' : asso_id[study_id],
                        'owner' : user,
                        'projects' : asso_id[study_projects],
                        'assays' : "",
                        'factors' : "",
                        'status' : 'private' ,
                        'signatures' : "",
                        'title' : study_title,
                        'description' : study_description,
                        'experimental_design' : study_experimental_design,
                        'results' : study_results,
                        'study_type' : study_type,
                        'last_update' : str(sdt),
                        'inclusion_period': study_inclusion_periode,
                        'inclusion': study_inclusion,
                        'followup': study_followup,
                        'exclusion' : study_exclusion,
                        'pop_size' : study_pop_size,
                        'pubmed' : study_pubmed,
                        'tags' : "",
                        'info' : ','.join(study_error['Info']),
                        'warnings' : ','.join(study_error['Warning']),
                        'critical' : ','.join(study_error['Critical']),
                        'excel_id' : study_id
                    }      
                    studies[study_id]=dico

        # List of TOXsIgN 'ontologies'
        list_developmental_stage = ['Fetal','Embryonic','Larva','Neo-Natal','Juvenile','Pre-pubertal','Pubertal','Adulthood','Elderly','NA']
        list_generation = ['f0','f1','f2','f3','f4','f5','f6','f7','f8','f9','f10']
        list_experimental = ['in vivo','ex vivo','in vitro','other','NA']
        list_sex = ['Male','Female','Both','Other','NA']
        list_dose_unit = ['M','mM','µM','g/mL','mg/mL','µg/mL','ng/mL','mg/kg','µg/kg','µg/kg','ng/kg','%']
        list_exposure_duration_unit = ['week','day','hour','minute','seconde']
        list_exposition_factor = ['Chemical','Physical','Biological']
        list_signature_type = ['Physiological','Genomic','Molecular']
        list_observed_effect = ['Decrease','Increase','No effect','NA']

        # Check assay
        sh = wb.sheet_by_index(2)
        assays={}
        assays_up = {}
        l_excelId = []
        for ass in passays :
            assay = request.registry.db_mongo['assays'].find_one({'id': ass})
            if assay is not None :
                if assay['excel_id'] is not None :
                    l_excelId.append(assay['excel_id'])
        for rownum in range(12, sh.nrows):
            row_values = sh.row_values(rownum)
            if row_values [1] == "" and row_values [2] == "" and row_values [3] =="" :
                continue
            assay_error = {'Critical':[],'Warning':[],'Info':[]}

            assay_id = row_values[0]
            assay_study = ""
            assay_title = ""
            assay_organism = ""
            assay_organism_name = ""
            assay_experimental_type = ""
            assay_developmental_stage = "" 
            assay_generation = ""
            assay_sex = ""
            assay_tissue = ""
            assay_tissue_name = ""
            assay_cell = ""
            assay_cell_name = ""
            assay_cell_line = ""
            assay_cell_line_name = ""   
            assay_additional_information = "" 
            tag = [] 
            assay_pop_age = ""
            assay_location = ""
            assay_reference = ""
            assay_matrice = "" 


            if row_values[1] != "":
                if row_values[1] in studies:
                    assay_study = row_values[1]
                else :
                    assay_error['Critical'].append("Studies doesn't exists ("+assay_id+")")
                    critical += 1
            else :
                study_error['Critical'].append("No associated study ("+assay_id+")")
                critical += 1

            if row_values[2] != "":
                assay_title = row_values[2]
            else :
                assay_error['Critical'].append("No study title ("+assay_id+")")
                critical += 1

            if row_values[4] != "":
                data = request.registry.db_mongo['species.tab'].find_one({'id': row_values[4]})
                if data is None :
                    if row_values[3] == "" :
                        assay_organism = ""
                        assay_error['Critical'].append("Please select an organism in the TOXsIgN ontologies list ("+assay_id+")")
                        critical += 1
                    else :
                        assay_organism_name = row_values[3]
                        tag.append(row_values[3])
                else :
                    assay_organism = data['name']
                    tag.append(data['name'])
                    tag.append(data['id'])
                    tag.extend(data['synonyms'])
                    tag.extend(data['direct_parent'])
                    tag.extend(data['all_parent'])
                    tag.extend(data['all_name'])
                    if row_values[3] != "" :
                        assay_organism_name = row_values[3]
                        tag.append(row_values[3])
            else :
                assay_error['Critical'].append("No organism selected ("+assay_id+")")
                critical += 1

            if row_values[5] != "":
                if row_values[5] in  list_developmental_stage :
                    assay_developmental_stage = row_values[5]
                else :
                    assay_error['Warning'].append("Developmental stage not listed ("+assay_id+")")
            else :
                assay_error['Info'].append("No developmental stage selected ("+assay_id+")")
                

            if row_values[6] != "":
                if row_values[6] in  list_generation :
                    assay_generation = row_values[6]
                else :
                    assay_error['Warning'].append("Generation not listed ("+assay_id+")")
            else :
                assay_error['Info'].append("No generation selected ("+assay_id+")")

            if row_values[7] != "":
                if row_values[7] in  list_sex :
                    assay_sex = row_values[7]
                else :
                    assay_error['Warning'].append("Sex not listed ("+assay_id+")")
            else :
                assay_error['Info'].append("No sex selected ("+assay_id+")")

            if row_values[9] != "":
                data = request.registry.db_mongo['tissue.tab'].find_one({'id': row_values[9]})
                if data is None :
                    if row_values[8] != "":
                        assay_tissue_name = row_values[8]
                        tag.append(assay_tissue_name)
                    else :
                        assay_tissue = ""
  
                else :
                    assay_tissue = data['name']
                    tag.append(data['name'])
                    tag.append(data['id'])
                    tag.extend(data['synonyms'])
                    tag.extend(data['direct_parent'])
                    tag.extend(data['all_parent'])
                    tag.extend(data['all_name'])
                    if row_values[8] != "":
                        assay_tissue_name = row_values[8]
                        tag.append(assay_tissue_name)


            if row_values[11] != "":
                data = request.registry.db_mongo['cell.tab'].find_one({'id': row_values[11]})
                if data is None :
                    if row_values[10] != "":
                        assay_cell_name = row_values[10]
                        tag.append(assay_cell_name)
                    else :
                        assay_cell = ""

                else :
                    assay_cell = data['name']
                    tag.append(data['name'])
                    tag.append(data['id'])
                    tag.extend(data['synonyms'])
                    tag.extend(data['direct_parent'])
                    tag.extend(data['all_parent'])
                    tag.extend(data['all_name'])
                    if row_values[10] != "":
                        assay_cell_name = row_values[10]
                        tag.append(assay_cell_name)



            if row_values[13] != "":
                data = request.registry.db_mongo['cell_line.tab'].find_one({'id': row_values[13]})
                if data is None :
                    if row_values[12] != "":
                        assay_cell_line_name = row_values[12]
                        tag.append(assay_cell_line_name)
                    else :
                        assay_cell_line = ""
                else :
                    assay_cell_line = data['name']
                    tag.append(data['name'])
                    tag.append(data['id'])
                    tag.extend(data['synonyms'])
                    tag.extend(data['direct_parent'])
                    tag.extend(data['all_parent'])
                    tag.extend(data['all_name'])
                    if row_values[12] != "":
                        assay_cell_line_name = row_values[12]
                        tag.append(assay_cell_line_name)

            # Check if at least tissue/cell or cell line are filled
            if assay_cell_line == "" and assay_cell == "" and assay_tissue =="" :
                if studies[assay_study]['study_type'] =='Observational' :
                    assay_error['Critical'].append("Please select at least a tissue, cell or cell line in the TOXsIgN ontologies list ("+assay_id+")")
                    critical += 1

            if row_values[14] != "":
                if row_values[14] in  list_experimental :
                    assay_experimental_type = row_values[14]
                else :
                    assay_error['Warning'].append("Experimental type not listed ("+assay_id+")")


            if studies[assay_study]['study_type'] =='Observational' :
                if row_values[15] != "":
                    assay_pop_age = row_values[15]
                else :
                    assay_error['Info'].append("No population age ("+assay_id+")")

                if row_values[16] != "":
                    assay_location = row_values[16]
                else :
                    assay_error['Info'].append("No geographical location ("+assay_id+")")

                if row_values[17] != "":
                    assay_reference = row_values[17]
                else :
                    assay_error['Info'].append("No controle / reference ("+assay_id+")")

                if row_values[18] != "":
                    assay_matrice = row_values[18]
                else :
                    assay_error['Info'].append("No matrice("+assay_id+")")

            if row_values[19] != "":
                assay_additional_information = row_values[19]
            else :
                assay_error['Info'].append("No additional information ("+assay_id+")")

            if assay_id in l_excelId :
                for ass in passays :
                    assay = request.registry.db_mongo['assays'].find_one({'id': ass})
                    if assay is not None :
                        if assay['excel_id'] == assay_id :

                            asso_id[assay_id] = assay['id']
                            reverse_asso[asso_id[assay_id]] = assay_id

                            #Add assay id to associated study
                            s_assay = studies[assay_study]['assays'].split()
                            s_assay.append(asso_id[assay_id])
                            s_assay = list(set(s_assay))
                            studies[assay_study]['assays'] = ','.join(s_assay)

                            #Add assay to the associated project
                            project_asso = reverse_asso[studies[assay_study]['projects']]

                            p_assay = projects[project_asso]['assays'].split()
                            p_assay.append(asso_id[assay_id])
                            p_assay = list(set(p_assay))
                            projects[project_asso]['assays'] = ','.join(p_assay)

                            dico={
                                'id' : assay['id'] ,
                                'studies' : asso_id[assay_study],
                                'factors' : "",
                                'signatures' : "",
                                'status' : 'private' ,
                                'projects' : studies[assay_study]['projects'],
                                'title' : assay_title,
                                'organism' : assay_organism,
                                'organism_name' : assay_organism_name,
                                'experimental_type' : assay_experimental_type,
                                'developmental_stage' : assay_developmental_stage,
                                'generation' : assay_generation,
                                'sex' : assay_sex,
                                'tissue' : assay_tissue,
                                'tissue_name' : assay_tissue_name,
                                'cell' : assay_cell,
                                'cell_name' : assay_cell_name,
                                'last_update' : str(sdt),
                                'cell_line' : assay_cell_line,
                                'cell_line_name' : assay_cell_line_name,
                                'additional_information' : assay_additional_information,
                                'population_age' : assay_pop_age,
                                'geographical_location':assay_location,
                                'reference':assay_reference,
                                'matrice':assay_matrice,
                                'tags' : ','.join(tag),
                                'owner' : user,
                                'info' : ','.join(assay_error['Info']),
                                'warnings' : ','.join(assay_error['Warning']),
                                'critical' : ','.join(assay_error['Critical']),
                                'excel_id' : assay_id
                            }
                            assays[assay_id] = dico
            else :

                #After reading line add all info in dico project
                request.registry.db_mongo['assay'].update({'id': 1}, {'$inc': {'val': 1}})
                repos = request.registry.db_mongo['assay'].find({'id': 1})
                id_a = ""
                for res in repos:
                    id_a = res
                
                #Excel id -> databas id
                asso_id[assay_id] = 'TSA'+str(id_a['val'])
                reverse_asso[asso_id[assay_id]] = assay_id


                #Add assay id to associated study
                s_assay = studies[assay_study]['assays'].split()
                s_assay.append(asso_id[assay_id])
                s_assay = list(set(s_assay))
                studies[assay_study]['assays'] = ','.join(s_assay)

                #Add assay to the associated project
                project_asso = reverse_asso[studies[assay_study]['projects']]

                p_assay = projects[project_asso]['assays'].split()
                p_assay.append(asso_id[assay_id])
                p_assay = list(set(p_assay))
                projects[project_asso]['assays'] = ','.join(p_assay)

                #After reading line add all info in dico project
                dico={
                    'id' : asso_id[assay_id] ,
                    'studies' : asso_id[assay_study],
                    'factors' : "",
                    'signatures' : "",
                    'projects' : studies[assay_study]['projects'],
                    'title' : assay_title,
                    'organism' : assay_organism,
                    'organism_name' : assay_organism_name,
                    'experimental_type' : assay_experimental_type,
                    'developmental_stage' : assay_developmental_stage,
                    'generation' : assay_generation,
                    'sex' : assay_sex,
                    'tissue' : assay_tissue,
                    'tissue_name' : assay_tissue_name,
                    'cell' : assay_cell,
                    'cell_name' : assay_cell_name,
                    'status' : 'private',
                    'last_update' : str(sdt),
                    'cell_line' : assay_cell_line,
                    'cell_line_name' : assay_cell_line_name,
                    'additional_information' : assay_additional_information,
                    'population_age' : assay_pop_age,
                    'geographical_location':assay_location,
                    'reference':assay_reference,
                    'matrice':assay_matrice,
                    'tags' : ','.join(tag),
                    'owner' : user,
                    'info' : ','.join(assay_error['Info']),
                    'warnings' : ','.join(assay_error['Warning']),
                    'critical' : ','.join(assay_error['Critical']),
                    'excel_id' : assay_id
                }
                assays[assay_id] = dico




        # Check factor
        sh = wb.sheet_by_index(3)
        factors={}

        l_excelId = []
        for fact in pfactors :
            factor = request.registry.db_mongo['factors'].find_one({'id': fact})
            l_excelId.append(factor['excel_id'])

        for rownum in range(5, sh.nrows):
            row_values = sh.row_values(rownum)
            if row_values [1] == "" and row_values [2] == "" and row_values [3] =="" and row_values [4] =="" and row_values [5] =="" :
                continue

            factor_error = {'Critical':[],'Warning':[],'Info':[]}

            factor_id = row_values[0]
            factor_type = ""
            factor_assay = ""
            factor_chemical = ""
            factor_chemical_name = ""
            factor_physical = ""
            factor_biological = ""
            factor_route = ""
            factor_vehicle  = ""
            factor_dose = ""
            factor_dose_unit = ""
            factor_exposure_duration = ""
            factor_exposure_duration_unit = ""
            factor_exposure_frequecies = ""
            factor_additional_information = ""
            tag = []


            if row_values[1] != "":
                if row_values[1] in assays:
                    factor_assay = row_values[1]
                else :
                    factor_error['Critical'].append("Assay doesn't exists ("+factor_id+")")
                    critical += 1
            else :
                factor_error['Critical'].append("No associated study ("+factor_id+")")
                critical += 1

            if row_values[2] != "":
                if row_values[2] in  list_exposition_factor :
                    factor_type = row_values[2]
                else :
                    factor_error['Critical'].append("Exposition factor not listed ("+factor_id+")")
                    critical += 1
            else :
                factor_error['Critical'].append("No exposition factor selected ("+factor_id+")")
                critical += 1

            if row_values[4] != "":
                data = request.registry.db_mongo['chemical.tab'].find_one({'id': row_values[4]})
                if data is None :
                    if row_values[3] != "":
                        factor_chemical_name = row_values[3]
                        tag.append(factor_chemical_name)
                    else :
                        factor_chemical = ""
                else :
                    factor_chemical = data['name']
                    tag.append(data['name'])
                    tag.append(data['id'])
                    tag.extend(data['synonyms'])
                    tag.extend(data['direct_parent'])
                    tag.extend(data['all_parent'])
                    tag.extend(data['all_name'])
                    if row_values[3] != "":
                        factor_chemical_name = row_values[3]
                        tag.append(factor_chemical_name)      

            if row_values[5] != "":
                data = request.registry.db_mongo['chemical.tab'].find_one({'id': row_values[5]})
                if data is None :
                    data =  'false'
                else :
                    data = 'true'
                if data == 'true' :
                    factor_physical = row_values[5]
                else :
                    a =1
                    #factor_error['Warning'].append("Physical factor not in the TOXsIgN ontologies (not available yet) ("+factor_id+")")
            else :
                a =1
                #factor_error['Warning'].append("No physical factor selected (not available yet) ("+factor_id+")")

            if row_values[6] != "":
                data = request.registry.db_mongo['chemical.tab'].find_one({'id': row_values[6]})
                if data is None :
                    data =  'false'
                else :
                    data = 'true'
                if data == 'true' :
                    factor_biological = row_values[6]
                else :
                    a=1
                    f#actor_error['Warning'].append("Biological factor notin the TOXsIgN ontologies (not available yet) ("+factor_id+")")
            else :
                a=1
                #factor_error['Warning'].append("No biological factor selected (not available yet) ("+factor_id+")")

            if row_values[7] != "":
                factor_route = row_values[7]
            else :
                factor_error['Info'].append("No route ("+factor_id+")")

            if row_values[8] != "":
                factor_vehicle = row_values[8]
            else :
                factor_error['Info'].append("No vehicle ("+factor_id+")")

            if row_values[9] != "":
                factor_dose = row_values[9]
            else :
                factor_error['Critical'].append("Factor dose required ("+factor_id+")")
                critical += 1

            try :
                if row_values[10] != "":
                    if str(row_values[10]) in list_dose_unit :
                        factor_dose_unit = row_values[10]
                    else :
                        factor_error['Warning'].append("Dose unit not in list ("+factor_id+")")
                else :
                    factor_error['Critical'].append("Factor dose unit required ("+factor_id+")")
                    critical += 1
            except : 
                 factor_dose_unit = row_values[10]

            if row_values[11] != "":
                factor_exposure_duration = row_values[11]
            else :
                factor_error['Critical'].append("Factor exposure duration required ("+factor_id+")")
                critical += 1

            try : 
                if row_values[12] != "":
                    if str(row_values[12]) in list_exposure_duration_unit :
                        factor_exposure_duration_unit = row_values[12]
                    else :
                        factor_error['Critical'].append("Exposure duration unit not in list ("+factor_id+")")
                        critical += 1
                else :
                    factor_error['Critical'].append("Factor dose unit required ("+factor_id+")")
                    critical += 1
            except :
                factor_exposure_duration_unit = row_values[12]

            if row_values[13] != "":
                factor_exposure_frequecies = row_values[13]
            else :
                factor_error['Warning'].append("No exposure frequencies ("+factor_id+")")

            if row_values[14] != "":
                factor_additional_information = row_values[14]
            else :
                factor_error['Info'].append("No additional information ("+factor_id+")")

            if factor_id in l_excelId :
                for fact in pfactors :
                    factor = request.registry.db_mongo['factors'].find_one({'id': fact})
                    if factor['excel_id'] == factor_id :

                        asso_id[factor_id] = factor['id']
                        reverse_asso[asso_id[factor_id]] = factor_id

                        #Add factor id to associated assay
                        a_factor = assays[factor_assay]['factors'].split()
                        a_factor.append(asso_id[factor_id])
                        a_factor = list(set(a_factor))
                        assays[factor_assay]['factors'] = ','.join(a_factor)

                        #Add factor to the associated study
                        study_asso = reverse_asso[assays[factor_assay]['studies']]

                        s_factor = studies[study_asso]['factors'].split()
                        s_factor.append(asso_id[factor_id])
                        s_factor = list(set(s_factor))
                        studies[study_asso]['factors'] = ','.join(s_factor)

                        #Add factor to the associated project
                        project_asso = reverse_asso[assays[factor_assay]['projects']]

                        p_factor = projects[project_asso]['factors'].split()
                        p_factor.append(asso_id[factor_id])
                        p_factor = list(set(p_factor))
                        projects[project_asso]['factors'] = ','.join(p_factor)

                        #up factor tags to associated assy 
                        tag_assay = assays[factor_assay]['tags'].split(',')
                        tag_assay.extend(tag)
                        tag_assay = list(set(tag_assay))
                        assays[factor_assay]['tags'] = ','.join(tag_assay)

                        dico={
                            'id' : factor['id'],
                            'assays' : asso_id[factor_assay],
                            'studies' : assays[factor_assay]['studies'],
                            'project' : assays[factor_assay]['projects'],
                            'type' : factor_type,
                            'status' : 'private' ,
                            'chemical' : factor_chemical,
                            'chemical_name' : factor_chemical_name,
                            'physical' : factor_physical,
                            'biological' : factor_biological,
                            'route' : factor_route,
                            'last_update' : str(sdt),
                            'vehicle' : factor_vehicle,
                            'dose' : str(factor_dose) +" "+ factor_dose_unit,
                            'exposure_duration' : str(factor_exposure_duration) +" "+ factor_exposure_duration_unit,
                            'exposure_frequencies' : factor_exposure_frequecies,
                            'additional_information' : factor_additional_information,
                            'tags' : ','.join(tag),
                            'owner' : user,
                            'info' : ','.join(factor_error['Info']),
                            'warnings' : ','.join(factor_error['Warning']),
                            'critical' : ','.join(factor_error['Critical']),
                            'excel_id' : factor_id
                        }
                        
                        factors[factor_id] = dico

            else : 

                #After reading line add all info in dico project
                request.registry.db_mongo['factor'].update({'id': 1}, {'$inc': {'val': 1}})
                repos = request.registry.db_mongo['factor'].find({'id': 1})
                id_a = ""
                for res in repos:
                    id_f = res
                
                #Excel id -> databas id
                asso_id[factor_id] = 'TSF'+str(id_f['val'])
                reverse_asso[asso_id[factor_id]] = factor_id

                #Add factor id to associated assay
                a_factor = assays[factor_assay]['factors'].split()
                a_factor.append(asso_id[factor_id])
                a_factor = list(set(a_factor))
                assays[factor_assay]['factors'] = ','.join(a_factor)

                #Add factor to the associated study
                study_asso = reverse_asso[assays[factor_assay]['studies']]

                s_factor = studies[study_asso]['factors'].split()
                s_factor.append(asso_id[factor_id])
                s_factor = list(set(s_factor))
                studies[study_asso]['factors'] = ','.join(s_factor)

                #Add factor to the associated project
                project_asso = reverse_asso[assays[factor_assay]['projects']]

                p_factor = projects[project_asso]['factors'].split()
                p_factor.append(asso_id[factor_id])
                p_factor = list(set(p_factor))
                projects[project_asso]['factors'] = ','.join(p_factor)

                #up factor tags to associated assy 
                tag_assay = assays[factor_assay]['tags'].split(',')
                tag_assay.extend(tag)
                tag_assay = list(set(tag_assay))
                assays[factor_assay]['tags'] = ','.join(tag_assay)

                #After reading line add all info in dico project
                try :
                    dico={
                        'id' : asso_id[factor_id],
                        'assays' : asso_id[factor_assay],
                        'studies' : assays[factor_assay]['studies'],
                        'project' : assays[factor_assay]['projects'],
                        'type' : factor_type,
                        'chemical' : factor_chemical,
                        'chemical_name' : factor_chemical_name,
                        'physical' : factor_physical,
                        'biological' : factor_biological,
                        'route' : factor_route,
                        'last_update' : str(sdt),
                        'status' : 'private',
                        'vehicle' : factor_vehicle,
                        'dose' : str(factor_dose) +" "+ factor_dose_unit,
                        'exposure_duration' : str(factor_exposure_duration) +" "+ factor_exposure_duration_unit,
                        'exposure_frequencies' : factor_exposure_frequecies,
                        'additional_information' : factor_additional_information,
                        'tags' : ','.join(tag),
                        'owner' : user,
                        'info' : ','.join(factor_error['Info']),
                        'warnings' : ','.join(factor_error['Warning']),
                        'critical' : ','.join(factor_error['Critical']),
                        'excel_id' : factor_id
                    }
                except:
                    dico={
                        'id' : asso_id[factor_id],
                        'assays' : asso_id[factor_assay],
                        'studies' : assays[factor_assay]['studies'],
                        'project' : assays[factor_assay]['projects'],
                        'type' : factor_type,
                        'chemical' : factor_chemical,
                        'chemical_name' : factor_chemical_name,
                        'physical' : factor_physical,
                        'biological' : factor_biological,
                        'route' : factor_route,
                        'last_update' : str(sdt),
                        'status' : 'private',
                        'vehicle' : factor_vehicle,
                        'dose' : factor_dose +" "+ factor_dose_unit,
                        'exposure_duration' : factor_exposure_duration +" "+ factor_exposure_duration_unit,
                        'exposure_frequencies' : factor_exposure_frequecies,
                        'additional_information' : factor_additional_information,
                        'tags' : ','.join(tag),
                        'owner' : user,
                        'info' : ','.join(factor_error['Info']),
                        'warnings' : ','.join(factor_error['Warning']),
                        'critical' : ','.join(factor_error['Critical']),
                        'excel_id' : factor_id
                    }
                factors[factor_id] = dico


        # Check signatures
        sh = wb.sheet_by_index(4)
        signatures={}
        l_excelId = []
        for sign in psignatures :
            signature = request.registry.db_mongo['signatures'].find_one({'id': sign})
            l_excelId.append(signature['excel_id'])
        for rownum in range(6, sh.nrows):
            row_values = sh.row_values(rownum)
            if row_values [1] == "" and row_values [2] == "" and row_values [3] =="" and row_values [4] =="" and row_values [5] =="" :
                continue

            signature_error = {'Critical':[],'Warning':[],'Info':[]}

            signature_id = row_values[0]
            signature_associated_study = ""
            signature_associated_assay = ""
            signature_title = ""
            signature_type = ""
            signature_organism = ""
            signature_organism_name = ""
            signature_developmental_stage = ""
            signature_generation = ""
            signature_sex = ""
            signature_tissue = ""
            signature_tissue_name = ""
            signature_cell = ""
            signature_cell_name = "" 
            signature_cell_line = ""
            signature_cell_line_name = ""
            signature_molecule = ""
            signature_molecule_name = ""
            signature_pathology = ""
            signature_technology = ""
            signature_technology_name = ""
            signature_plateform = ""
            signature_observed_effect = ""
            signature_control_sample = ""
            signature_treated_sample = ""
            signature_pvalue = ""
            signature_cutoff = "" 
            signature_satistical_processing = ""
            signature_additional_file = ""
            signature_file_up = "" 
            signature_file_down = ""
            signature_file_interrogated = ""
            signature_genes_identifier = ""
            signature_study_type= ""
            signature_description = ""

            signature_controle = ""
            signature_case = ""
            signature_significance = ""
            signature_stat_value = ""
            signature_stat_adjust = ""
            signature_stat_other = ""
            signature_group = ""
            signature_pop_age = ""
            tag = []

            if row_values[1] != "":
                if row_values[1] in studies:
                    signature_associated_study = row_values[1]
                else :
                    signature_error['Critical'].append("Study doesn't exists ("+signature_id+")")
                    critical += 1
            else :
                signature_error['Critical'].append("No associated study ("+signature_id+")")
                critical += 1

            if row_values[2] != "":
                if row_values[2] in assays:
                    signature_associated_assay = row_values[2]
                else :
                    signature_error['Critical'].append("Assay doesn't exists ("+signature_id+")")
                    critical += 1
            else :
                signature_error['Critical'].append("No associated assay ("+signature_id+")")
                critical += 1

            if row_values[3] != "":
                signature_title = row_values[3]
            else :
                signature_error['Critical'].append("No signature title ("+signature_id+")")
                critical += 1

            if row_values[4] != "":
                if row_values[4] in list_signature_type : 
                    signature_type = row_values[4]
                else :
                    signature_error['Critical'].append("Signature title not in the list ("+signature_id+")")
                    critical += 1
            else :
                signature_error['Critical'].append("No type of signature ("+signature_id+")")
                critical += 1

            if row_values[6] != "":
                data = request.registry.db_mongo['species.tab'].find_one({'id': row_values[6]})
                if data is None :
                    if row_values[5] != "":
                        signature_organism_name = row_values[5]
                        tag.append(signature_organism_name)
                    else :
                        signature_organism = ""
                        signature_error['Critical'].append("Please select an organism in the TOXsIgN ontologies list ("+signature_id+")")
                        critical += 1
                else :
                    signature_organism = data['name']
                    tag.append(data['name'])
                    tag.append(data['id'])
                    tag.extend(data['synonyms'])
                    tag.extend(data['direct_parent'])
                    tag.extend(data['all_parent'])
                    tag.extend(data['all_name'])
                    if row_values[5] != "":
                        signature_organism = row_values[5]
                        tag.append(signature_organism_name)   
            else :
                signature_error['Critical'].append("No organism selected ("+signature_id+")")
                critical += 1

            if row_values[7] != "":
                if row_values[7] in  list_developmental_stage :
                    signature_developmental_stage = row_values[7]
                else :
                    signature_error['Warning'].append("Developmental stage not listed ("+signature_id+")")
            else :
                signature_error['Info'].append("No developmental stage selected ("+signature_id+")")
                

            if row_values[8] != "":
                if row_values[8] in  list_generation :
                    signature_generation = row_values[8]
                else :
                    signature_error['Warning'].append("Generation not listed ("+signature_id+")")
            else :
                signature_error['Info'].append("No generation selected ("+signature_id+")")

            if row_values[9] != "":
                if row_values[9] in  list_sex :
                    signature_sex = row_values[9]
                else :
                    signature_error['Warning'].append("Sex not listed ("+signature_id+")")
            else :
                signature_error['Info'].append("No sex selected ("+signature_id+")")

            if row_values[11] != "":
                data = request.registry.db_mongo['tissue.tab'].find_one({'id': row_values[1]})
                if data is None :
                    if row_values[10] != "":
                        signature_tissue_name = row_values[10]
                        tag.append(signature_tissue_name)
                    else :
                        signature_tissue = ""
                        if studies[signature_associated_study]['study_type'] != 'Observational' :
                            signature_error['Warning'].append("Please select a tissue in the TOXsIgN ontologies list ("+signature_id+")")
                else :
                    signature_tissue = data['name']
                    tag.append(data['name'])
                    tag.append(data['id'])
                    tag.extend(data['synonyms'])
                    tag.extend(data['direct_parent'])
                    tag.extend(data['all_parent'])
                    tag.extend(data['all_name'])
                    if row_values[10] != "":
                        signature_tissue_name = row_values[10]
                        tag.append(signature_tissue_name)  
            else :
                if studies[signature_associated_study]['study_type'] != 'Observational' :
                    signature_error['Warning'].append("No tissue selected ("+signature_id+")")

            if row_values[13] != "":
                data = request.registry.db_mongo['cell.tab'].find_one({'id': row_values[13]})
                if data is None :
                    if row_values[12] != "":
                        signature_cell_name = row_values[12]
                        tag.append(signature_cell_name)
                    else :
                        signature_cell = ""
                        if studies[signature_associated_study]['study_type'] != 'Observational' :
                            signature_error['Warning'].append("Please select a cell in the TOXsIgN ontologies list ("+signature_id+")")
                else :
                    signature_cell = data['name']
                    tag.append(data['name'])
                    tag.append(data['id'])
                    tag.extend(data['synonyms'])
                    tag.extend(data['direct_parent'])
                    tag.extend(data['all_parent'])
                    tag.extend(data['all_name']) 
                    if row_values[12] != "":
                        signature_cell_name = row_values[12]
                        tag.append(signature_cell_name)  
            else :
                if studies[signature_associated_study]['study_type'] != 'Observational' :
                    signature_error['Warning'].append("No cell selected ("+signature_id+")")


            if row_values[15] != "":
                data = request.registry.db_mongo['cell_line.tab'].find_one({'id': row_values[15]})
                if data is None :
                    if row_values[14] != "":
                        signature_cell_line_name = row_values[14]
                        tag.append(signature_cell_line_name)
                    else :
                        signature_cell_line = 'No cell line'
                        if studies[signature_associated_study]['study_type'] != 'Observational' :
                            signature_error['Warning'].append("Please select a cell line in the TOXsIgN ontologies list ("+signature_id+")")
                else :
                    signature_cell_line = data['name']
                    tag.append(data['name'])
                    tag.append(data['id'])
                    tag.extend(data['synonyms'])
                    tag.extend(data['direct_parent'])
                    tag.extend(data['all_parent'])
                    tag.extend(data['all_name'])
                    if row_values[14] != "":
                        signature_cell_line_name = row_values[14]
                        tag.append(signature_cell_line_name)   
            else :
                if studies[signature_associated_study]['study_type'] != 'Observational' :
                    signature_error['Warning'].append("No cell line selected ("+signature_id+")")

            # Check if at least tissue/cell or cell line are filled
            if signature_cell_line == "" and signature_cell == "" and signature_tissue =="" :
                if studies[signature_associated_study]['study_type'] != 'Observational' :
                    signature_error['Critical'].append("Please select at least a tissue, cell or cell line in the TOXsIgN ontologies list ("+signature_id+")")
                    critical += 1

            if row_values[17] != "":
                data = request.registry.db_mongo['chemical.tab'].find_one({'id': row_values[17]})
                if data is None :
                    if row_values[16] != "" :
                        signature_molecule_name = row_values[16]
                        tag.append(signature_molecule_name)
                    else :
                        signature_molecule = ""
                        if studies[signature_associated_study]['study_type'] != 'Observational' :
                            if signature_type == "Molecular":
                                signature_error['Warning'].append("Molecule not in TOXsIgN ontology ("+signature_id+")")
                else :
                    signature_molecule = data['name']
                    tag.append(data['name'])
                    tag.append(data['id'])
                    tag.extend(data['synonyms'])
                    tag.extend(data['direct_parent'])
                    tag.extend(data['all_parent'])
                    tag.extend(data['all_name'])
                    if row_values[16] != "" :
                        signature_molecule_name = row_values[16]
                        tag.append(signature_molecule_name)   
            else :
                if studies[signature_associated_study]['study_type'] != 'Observational' :
                    if signature_type == "Molecular":
                        signature_error['Warning'].append("No molecule selected ("+signature_id+")")

            if row_values[18] != "":
                signature_description = row_values[18]

            if row_values[19] != "":
                data = request.registry.db_mongo['disease.tab'].find_one({'id': row_values[19]})
                if data is None :
                    signature_pathology = ""
                    signature_error['Warning'].append("Pathology / disease not in TOXsIgN ontology ("+signature_id+")")
                else :
                    signature_pathology = data['name']
                    tag.append(data['name'])
                    tag.append(data['id'])
                    tag.extend(data['synonyms'])
                    tag.extend(data['direct_parent'])
                    tag.extend(data['all_parent'])
                    tag.extend(data['all_name'])
                          
            else :
                signature_error['Warning'].append("No pathology / disease selected ("+signature_id+")")

            if row_values[21] != "":
                data = request.registry.db_mongo['experiment.tab'].find_one({'id': row_values[21]})
                if data is None :
                    if row_values[20] != "":
                        signature_technology_name = row_values[20]
                        tag.append(signature_technology_name)
                    else :
                        signature_technology = ""
                        if signature_type == "Genomic":
                            signature_error['Warning'].append("Technology not in TOXsIgN ontology ("+signature_id+")")
                else :
                    signature_technology = data['name']
                    tag.append(data['name'])
                    tag.append(data['id'])
                    tag.extend(data['synonyms'])
                    tag.extend(data['direct_parent'])
                    tag.extend(data['all_parent'])
                    tag.extend(data['all_name'])
                    if row_values[20] != "":
                        signature_technology_name = row_values[20]
                        tag.append(signature_technology_name)              
            else :
                if signature_type == "Genomic":
                    signature_error['Warning'].append("No technology selected ("+signature_id+")")

            if row_values[22] != "":
                signature_plateform = row_values[22]
            else :
                if signature_type == "Genomic":
                    signature_error['Info'].append("No plateform selected ("+signature_id+")")


            if row_values[23] != "":
                signature_controle = row_values[23]
            else :
                if studies[signature_associated_study]['study_type'] == 'Observational':
                    signature_error['Info'].append("No controle ("+signature_id+")")

            if row_values[24] != "":
                signature_case = row_values[24]
            else :
                if studies[signature_associated_study]['study_type'] == 'Observational':
                    signature_error['Info'].append("No case ("+signature_id+")")

            if row_values[25] != "":
                signature_group = row_values[25]
            else :
                if studies[signature_associated_study]['study_type'] == 'Observational' :
                    signature_error['Info'].append("No group ("+signature_id+")")

            if row_values[26] != "":
                signature_group = row_values[26]
            else :
                if studies[signature_associated_study]['study_type'] == 'Observational' :
                    signature_error['Info'].append("No population age ("+signature_id+")")


            if row_values[27] != "":
                if row_values[27] in  list_observed_effect :
                    signature_observed_effect= row_values[27]
                else :
                    signature_error['Warning'].append("Observed effect not listed ("+signature_id+")")

            else :
                signature_error['Warning'].append("No observed effect selected ("+signature_id+")")

            if row_values[28] != "":
                signature_significance = row_values[28]
            else :
                if studies[signature_associated_study]['study_type'] == 'Observational' :
                    signature_error['Info'].append("No statistical significance ("+signature_id+")")

            if row_values[29] != "":
                signature_stat_value = row_values[29]
            else :
                if studies[signature_associated_study]['study_type'] == 'Observational' :
                    signature_error['Info'].append("No statistical value ("+signature_id+")")

            if row_values[30] != "":
                signature_stat_adjust = row_values[30]
            else :
                if studies[signature_associated_study]['study_type'] == 'Observational' :
                    signature_error['Info'].append("No statistical adjustment ("+signature_id+")")

            if row_values[31] != "":
                signature_stat_other = row_values[31]
            else :
                if studies[signature_associated_study]['study_type'] == 'Observational' :
                    signature_error['Info'].append("No statistical information ("+signature_id+")")




            if row_values[32] != "":
                signature_control_sample = row_values[32]
            else :
                if studies[signature_associated_study]['study_type'] != 'Observational' :
                    signature_error['Info'].append("No control sample ("+signature_id+")")

            if row_values[33] != "":
                signature_treated_sample = row_values[33]
            else :
                if studies[signature_associated_study]['study_type'] != 'Observational' :
                    signature_error['Info'].append("No treated sample ("+signature_id+")")

            if row_values[34] != "":
                signature_pvalue = row_values[34]
            else :
                if studies[signature_associated_study]['study_type'] != 'Observational' :
                    signature_error['Info'].append("No pvalue ("+signature_id+")")

            if row_values[35] != "":
                signature_cutoff = row_values[36]
            else :
                if studies[signature_associated_study]['study_type'] != 'Observational' :
                    signature_error['Info'].append("No cutoff ("+signature_id+")")

            if row_values[36] != "":
                signature_satistical_processing = row_values[36]
            else :
                if studies[signature_associated_study]['study_type'] != 'Observational' :
                    signature_error['Info'].append("No statistical processing ("+signature_id+")")

            if row_values[37] != "":
                signature_additional_file = row_values[37]
            else :
                signature_error['Info'].append("No additional file ("+signature_id+")")

            if row_values[38] != "":
                signature_file_up = row_values[38]
            else :
                if signature_type == "Genomic":
                    signature_error['Critical'].append("No signature file (up genes) ("+signature_id+")")
                    critical += 1

            if row_values[39] != "":
                signature_file_down = row_values[39]
            else :
                if signature_type == "Genomic":
                    signature_error['Critical'].append("No signature file (down genes) ("+signature_id+")")
                    critical +=1

            if row_values[40] != "":
                signature_file_interrogated = row_values[40]
            else :
                if signature_type == "Genomic":
                    signature_error['Critical'].append("No signature file (interrogated genes) ("+signature_id+")")
                    critical += 1

            if row_values[41] != "":
                signature_genes_identifier = row_values[41]
            else :
                if signature_type == "Genomic":
                    signature_error['Info'].append("No gene identifier selected ("+signature_id+")")
                    critical += 1

            signature_study_type = studies[signature_associated_study]
            if signature_id in l_excelId :
                for sign in psignatures :
                    signature = request.registry.db_mongo['signatures'].find_one({'id': sign})
                    if signature['excel_id'] == signature_id :

                        asso_id[signature_id] = signature['id']
                        reverse_asso[asso_id[signature_id]] = signature_id

                        a_signature = assays[signature_associated_assay]['signatures'].split()

                        a_signature.append(asso_id[signature_id])
                        a_signature = list(set(a_signature))
                        assays[signature_associated_assay]['signatures'] = ','.join(a_signature)

                        #Add factor to the associated study

                        s_signature = studies[signature_associated_study]['signatures'].split()
                        s_signature.append(asso_id[signature_id])
                        s_signature = list(set(s_signature))
                        studies[signature_associated_study]['signatures'] = ','.join(s_signature)

                        #Add factor to the associated project
                        project_asso = reverse_asso[studies[signature_associated_study]['projects']]

                        p_signature = projects[project_asso]['signatures'].split()
                        p_signature.append(asso_id[signature_id])
                        p_signature = list(set(p_signature))
                        projects[project_asso]['signatures'] = ','.join(p_signature)

                        #get factors
                        tag.extend(assays[signature_associated_assay]['tags'].split(','))
                        myset = list(set(tag))
                        tag = myset


                        dico={
                        'id' : signature['id'],
                        'studies' : asso_id[signature_associated_study],
                        'assays' : asso_id[signature_associated_assay],
                        'projects' : studies[signature_associated_study]['projects'] ,
                        'title' : signature_title,
                        'type' : signature_type,
                        'organism' : signature_organism,
                        'organism_name' : signature_organism_name,
                        'developmental_stage' : signature_developmental_stage,
                        'generation' : signature_generation,
                        'sex' : signature_sex,
                        'last_update' : str(sdt),
                        'tissue' : signature_tissue,
                        'tissue_name' : signature_tissue_name,
                        'cell' : signature_cell,
                        'cell_name' : signature_cell_name,
                        'status' : 'private',
                        'cell_line' : signature_cell_line,
                        'cell_line_name' : signature_cell_line_name,
                        'molecule' : signature_molecule,
                        'molecule_name' : signature_molecule_name,
                        'pathology' : signature_pathology,
                        'technology' : signature_technology,
                        'description' : signature_description,
                        'technology_name' : signature_technology_name,
                        'plateform' : signature_plateform,
                        'observed_effect' : signature_observed_effect,
                        'control_sample' : str(signature_control_sample),
                        'treated_sample' : str(signature_treated_sample),
                        'pvalue' : str(signature_pvalue),
                        'cutoff' : str(signature_cutoff),
                        'statistical_processing' : signature_satistical_processing,
                        'additional_file' : signature_additional_file,
                        'file_up' : signature_file_up,
                        'file_down' : signature_file_down,
                        'file_interrogated' : signature_file_interrogated,
                        'genes_identifier': signature_genes_identifier,
                        'controle':signature_controle,
                        'case':signature_case,
                        'significance':signature_significance,
                        'stat_val' : signature_stat_value,
                        'stat_adjust' : signature_stat_adjust,
                        'stat_other' : signature_stat_other,
                        'study_type' :signature_study_type,
                        'group' : signature_group,
                        'pop_age' : signature_pop_age,
                        'tags' : ','.join(tag),
                        'owner' : user,
                        'info' : ','.join(signature_error['Info']),
                        'warnings' : ','.join(signature_error['Warning']),
                        'critical' : ','.join(signature_error['Critical']),
                        'excel_id' : signature_id,
                        'genes_up' : "",
                        'genes_down' : ""
                        }
                        
                        signatures[signature_id] = dico

            else : 
                #After reading line add all info in dico project
                request.registry.db_mongo['signature'].update({'id': 1}, {'$inc': {'val': 1}})
                repos = request.registry.db_mongo['signature'].find({'id': 1})
                id_a = ""
                for res in repos:
                    id_si = res
                
                #Excel id -> databas id
                asso_id[signature_id] = 'TSS'+str(id_si['val'])
                reverse_asso[asso_id[signature_id]] = signature_id

                a_signature = assays[signature_associated_assay]['signatures'].split()

                a_signature.append(asso_id[signature_id])
                a_signature = list(set(a_signature))
                assays[signature_associated_assay]['signatures'] = ','.join(a_signature)

                #Add factor to the associated study

                s_signature = studies[signature_associated_study]['signatures'].split()
                s_signature.append(asso_id[signature_id])
                s_signature = list(set(s_signature))
                studies[signature_associated_study]['signatures'] = ','.join(s_signature)

                #Add factor to the associated project
                project_asso = reverse_asso[studies[signature_associated_study]['projects']]

                p_signature = projects[project_asso]['signatures'].split()
                p_signature.append(asso_id[signature_id])
                p_signature = list(set(p_signature))
                projects[project_asso]['signatures'] = ','.join(p_signature)

                #get factors
                tag.extend(assays[signature_associated_assay]['tags'].split(','))
                myset = list(set(tag))
                tag = myset

                dico ={
                    'id' : asso_id[signature_id],
                    'studies' : asso_id[signature_associated_study],
                    'assays' : asso_id[signature_associated_assay],
                    'projects' : studies[signature_associated_study]['projects'] ,
                    'title' : signature_title,
                    'type' : signature_type,
                    'organism' : signature_organism,
                    'organism_name' : signature_organism_name,
                    'developmental_stage' : signature_developmental_stage,
                    'generation' : signature_generation,
                    'sex' : signature_sex,
                    'last_update' : str(sdt),
                    'tissue' : signature_tissue,
                    'tissue_name' : signature_tissue_name,
                    'cell' : signature_cell,
                    'cell_name' : signature_cell_name,
                    'status' : 'private',
                    'cell_line' : signature_cell_line,
                    'cell_line_name' : signature_cell_line_name,
                    'molecule' : signature_molecule,
                    'molecule_name' : signature_molecule_name,
                    'pathology' : signature_pathology,
                    'technology' : signature_technology,
                    'description' : signature_description,
                    'technology_name' : signature_technology_name,
                    'plateform' : signature_plateform,
                    'observed_effect' : signature_observed_effect,
                    'control_sample' : str(signature_control_sample),
                    'treated_sample' : str(signature_treated_sample),
                    'pvalue' : str(signature_pvalue),
                    'cutoff' : str(signature_cutoff),
                    'statistical_processing' : signature_satistical_processing,
                    'additional_file' : signature_additional_file,
                    'file_up' : signature_file_up,
                    'file_down' : signature_file_down,
                    'file_interrogated' : signature_file_interrogated,
                    'genes_identifier': signature_genes_identifier,
                    'controle':signature_controle,
                    'case':signature_case,
                    'significance':signature_significance,
                    'stat_val' : signature_stat_value,
                    'stat_adjust' : signature_stat_adjust,
                    'stat_other' : signature_stat_other,
                    'study_type' :signature_study_type,
                    'group' : signature_group,
                    'pop_age' : signature_pop_age,
                    'tags' : ','.join(tag),
                    'owner' : user,
                    'info' : ','.join(signature_error['Info']),
                    'warnings' : ','.join(signature_error['Warning']),
                    'critical' : ','.join(signature_error['Critical']),
                    'excel_id' : signature_id,
                    'genes_up' : "",
                    'genes_down' : ""
                }
                signatures[signature_id] = dico

        


        # Create user project directory + move tmp
        for proj in projects :
            ID = projects[proj]['id']
            projects[proj]['edges']  = {}
            for stud in studies:
                projects[proj]['edges'][studies[stud]['id']] = studies[stud]['assays'].split()
            for ass in assays:
                projects[proj]['edges'][assays[ass]['id']] = assays[ass]['signatures'].split()

            projects[proj]['edges'] = json.dumps(projects[proj]['edges'])
            request.registry.db_mongo['projects'].update({'id': projects[proj]['id']},projects[proj])

        upload_path = os.path.join(request.registry.upload_path, user, form['pid'])
        final_file = 'TOXsIgN_'+form['pid']+'.xlsx'
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        os.rename(input_file, os.path.join(upload_path, final_file))

        for stud in studies:
            get = request.registry.db_mongo['studies'].find_one({'id': studies[stud]['id']})
            if get is None :
                request.registry.db_mongo['studies'].insert(studies[stud])
            else :
                request.registry.db_mongo['studies'].update({'id': studies[stud]['id']},studies[stud])

        for ass in assays:
            get = request.registry.db_mongo['assays'].find_one({'id': assays[ass]['id']})
            if get is None :
                request.registry.db_mongo['assays'].insert(assays[ass])
            else :
                request.registry.db_mongo['assays'].update({'id': assays[ass]['id']},assays[ass])

        for fac in factors:
            get = request.registry.db_mongo['factors'].find_one({'id': factors[fac]['id']})
            if get is None :
                request.registry.db_mongo['factors'].insert(factors[fac])
            else :
                request.registry.db_mongo['factors'].update({'id': factors[fac]['id']},factors[fac])

        for sign in signatures:
            get = request.registry.db_mongo['signatures'].find_one({'id': signatures[sign]['id']})
            if get is None :
                request.registry.db_mongo['signatures'].insert(signatures[sign])
            else :
                request.registry.db_mongo['signatures'].update({'id': signatures[sign]['id']},signatures[sign])


        return {'msg':"File checked and update !" }

    except:
        logger.warning("Error - Upadate excel file")
        logger.warning(sys.exc_info())
        return {'msg':'An error occurred while updating your file. If the error persists please contact TOXsIgN support ','status':'1'}
    











@view_config(route_name='search', renderer='json', request_method='POST')
def search(request):
    form = json.loads(request.body, encoding=request.charset)
    request_query = form['query']
    
    
    size=25

    
    #return {'query':request_query}

    if 'search' in form:
        
        query=form['query']
        pfrom=form['pfrom']
        sfrom=form['sfrom']
        sgfrom=form['sgfrom']
        query_project=changeQuery(query,'projects')
        query_study=changeQuery(query,'studies')
        query_srategy=changeQuery(query,'strategies')
        queyy_list=changeQuery(query,'lists')

        # return {'query_project':query_project, 'query_study':query_study, 'query_signature':query_signature}



        # page=request.registry.es.search(
        #     index = request.registry.es_db,
        #     search_type = 'query_then_fetch',
        #     size = size,
        #     from_= from_val,
        #     body = {"query" : { "query_string" : {"query" :'_type:_all AND ' +request_query,"default_operator":"AND",'analyzer': "standard"}}})
        

        project = request.registry.es.search(
            index = request.registry.es_db,
            search_type = 'query_then_fetch',
            from_= pfrom,
            size = size, 
            body = {"query" : { "query_string" : {"query" :query_project,"default_operator":"AND",'analyzer': "standard"}}})
        
        study = request.registry.es.search(
            index = request.registry.es_db,
            search_type = 'query_then_fetch',
            from_= sfrom,
            size = size,
            body = {"query" : { "query_string" : {"query" :query_study,"default_operator":"AND",'analyzer': "standard"}}})
        
        strategy = request.registry.es.search(
            index = request.registry.es_db,
            search_type = 'query_then_fetch',
            from_= sgfrom,
            size = size,         
            body = {"query" : { "query_string" : {"query" :query_strategy,"default_operator":"AND",'analyzer': "standard"}}})

        _list = request.registry.es.search(
            index = request.registry.es_db,
            search_type = 'query_then_fetch',
            from_= sgfrom,
            size = size,         
            body = {"query" : { "query_string" : {"query" :query_list,"default_operator":"AND",'analyzer': "standard"}}})


        number_project=str(project['hits']['total'])
        if number_project=="0":
            number_project="No Result"

        number_study=str(study['hits']['total'])
        if number_study=="0":
            number_study="No result"

        number_strategy=str(strategy['hits']['total'])
        if number_strategy=="0":
            number_signature="No Result"

        number_list=str(_list['hits']['total'])
        if number_list=="0":
            number_list="No Result"


        return {'projects' : project, 'studies':study , 'strategies' : strategy , 'lists' : _list, 'query': query_project, \
                    'number_project' : number_project, 'number_study' : number_study,\
                    'number_strategy' :number_strategy, 'number_list' : number_list, 'query':query}
        # return page

    request_number_query=form['number_query']
    request_pfrom=form['pfrom']
    request_sfrom=form['sfrom']
    request_stfrom=form['stfrom']
    request_lfrom=form['lfrom']

    if request_pfrom<0:
        request.pfrom=0
    # if 'from' in form :
    #     from_val = form['from']
    # else :
    #     from_val = 0

    if request_query == '(_all:*) ':
        return {'query':request_query}

    elif request_number_query == 1:
        # page= request.registry.es.search(index = request.registry.es_db) \
        # .filter("term", category="search") \
        # .query("kidney", title="title")
        if('projects' in request_query):
            _from=request_pfrom

        elif('studies' in request_query):
            _from=request_sfrom

        elif('strategies' in request_query):
            _from=requesy_stfrom

        else:
            _from=request_lfrom

        page = request.registry.es.search(
            index = request.registry.es_db,
            search_type = 'query_then_fetch',
            from_=_from,
            size=size,
            #from_=#form['from'],
            #size=(form['from']+25),
            body =  {"query" : { "query_string" : {"query" :request_query,"default_operator":"AND",'analyzer': "standard"}}}
        )
        return {'page' : page , 'number': str(page['hits']['total']), 'query' : request_query , 'number_query' :'1'}
    else:
        #return {'ok1111'}
        request_query_dico=form['query_dico']

        projects={}
        studies={}
        strategies={}
        lists={}

        for _type in request_query_dico.keys():
            if("projects" in _type):
                projects[_type]=request_query_dico[_type]
            elif("studies" in _type):
                studies[_type]=request_query_dico[_type]
            elif("strategies" in _type):
                strategies[_type]=request_query_dico[_type]
            elif("lists" in _type ):
                lists[_type]=request_query_dico[_type]
        
        if projects != {}:
            projects_keys = projects.keys()
            projects_values = projects.values()
            projects_query= str(projects_keys[0])
            if(len(projects_keys)!=0):
                for index in range(1,len(projects_keys)):
                    projects_query+= ' '+str(projects_values[index])+ ' ' +str(projects_keys[index])
        else:
            projects_query=None


        if studies != {}:
            studies_keys = studies.keys()
            studies_values = studies.values()
            studies_query= str(studies_keys[0])
            if(len(studies_keys)!=0):
                for index in range(1,len(studies_keys)):
                    studies_query+= ' '+str(studies_values[index])+ ' ' +str(studies_keys[index])
        else:
            studies_query=None

        if strategies !={}:
            strategies_keys = strategies.keys()
            strategies_values = strategies.values()
            strategies_query= str(strategies_keys[0])
            if(len(strategies_keys)!=0):
                for index in range(1,len(strategies_keys)):
                    strategies_query+= ' '+str(strategies_values[index])+ ' ' +str(strategies_keys[index])
        else:
            strategies_query=None

        if lists !={}:
            lists_keys = listss.keys()
            lists_values = lists.values()
            lists_query= str(lists_keys[0])
            if(len(lists_keys)!=0):
                for index in range(1,len(lists_keys)):
                    lists_query+= ' '+str(lists_values[index])+ ' ' +str(lists_keys[index])
        else:
            lists_query=None


        #return{'projects' : projects_query, 'studies' : studies_query, 'signatures': signatures_query}
        #return {'projects':projects_query}
        if projects_query != None:
            project =request.registry.es.search(
                index = request.registry.es_db,
                search_type = 'query_then_fetch',
                from_=request_pfrom,
                size=size,
                #from_=#form['from'],
                #size=(form['from']+25),
                body =  {"query" : { "query_string" : {"query" :projects_query,"default_operator":"AND",'analyzer': "standard"}}}
            )
            number_project=str(project['hits']['total'])
        else:
            project=None
            number_project="0"

        if studies_query !=None:
            study =request.registry.es.search(
                index = request.registry.es_db,
                search_type = 'query_then_fetch',
                from_=request_sfrom,
                size=size,
                #from_=#form['from'],
                #size=(form['from']+25),
                body =  {"query" : { "query_string" : {"query" :studies_query,"default_operator":"AND",'analyzer': "standard"}}}
            )
            number_study=str(study['hits']['total'])
        else:
            study=None
            number_study="0"

        if strategies_query:
            strategy =request.registry.es.search(
                index = request.registry.es_db,
                search_type = 'query_then_fetch',
                from_=request_stfrom,
                size=size,
                #from_=#form['from'],
                #size=(form['from']+25),
                body =  {"query" : { "query_string" : {"query" :strategies_query,"default_operator":"AND",'analyzer': "standard"}}}
            )
            number_strategy=str(strategies['hits']['total'])
        else:
            strategy=None
            number_strategy="0"

        if lists_query:
            _list =request.registry.es.search(
                index = request.registry.es_db,
                search_type = 'query_then_fetch',
                from_=request_lfrom,
                size=size,
                #from_=#form['from'],
                #size=(form['from']+25),
                body =  {"query" : { "query_string" : {"query" :lists_query,"default_operator":"AND",'analyzer': "standard"}}}
            )
            number_strategy=str(strategies['hits']['total'])
        else:
            _list=None
            number_list="0"

 
        return {'projects' : project, 'studies':study , 'signatures' : strategy, 'lists' : _list, 'query': request_query, \
                    'number_project' : number_project, 'number_study' : number_study,\
                    'number_strategy' : number_strategy, 'number_list' : number_list}




    # form = json.loads(request.body, encoding=request.charset)
    # request_query = form['query']
    # if 'from' in form :
    #     from_val = form['from']
    # else :
    #     from_val = 0

    # page = request.registry.es.search(
    # index = request.registry.es_db,
    #   search_type = 'query_then_fetch',
    #   size = 1000,
    #   body =  {"query" : { "query_string" : {"query" :request_query,"default_operator":"AND",'analyzer': "standard"}}})


    # body = {"query" : { "query_string" : {"query" :request_query,"default_operator":"AND",'analyzer': "standard"}}}
    # print body
    # return page
  

    #page = request.registry.es.search(
    #index = request.registry.es_db,
    #  search_type = 'query_then_fetch',
    #  size = 100,
    #  from_= from_val,
    #  body = {"query" : { "query_string" : {"query" :request_query,"default_operator":"AND",'analyzer': "standard"}}})

    #return page



@view_config(route_name='user_recover', renderer='json', request_method='POST')
def user_recover(request):
    form = json.loads(request.body, encoding=request.charset)
    if form['user_name'] is None:
        return {'msg': 'Please fill your email first', 'status' : 'warning'}
    user_in_db = request.registry.db_mongo['users'].find_one({'id': form['user_name']})
    if user_in_db is None:
        return {'msg': 'User not found', 'status' : 'warning'}
    secret = request.registry.settings['secret_passphrase']
    del user_in_db['_id']
    token = jwt.encode({'user': user_in_db,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=36000),
                        'aud': 'urn:geneulike/recover'}, secret)
    message = "You requested a password reset, please click on following link to reset your password:\n"
    message += request.host_url+'/app/index.html#/password_recover?token='+token
    send_mail(request, form['user_name'], '[GeneULike] Password reset request', message)
    logging.info(message)
    return {'msg': 'You will receive an email you must acknowledge it to reset your password.', 'status' : 'success'}


@view_config(route_name='login', renderer='json', request_method='POST')
def login(request):
    form = json.loads(request.body, encoding=request.charset)
    user_in_db = request.registry.db_mongo['users'].find_one({'id': form['user_name']})
    if user_in_db is None:
        return {'msg' : 'Your email is not inside our data' , 'status' : 'warning'}

    if bcrypt.hashpw(form['user_password'].encode('utf-8'), user_in_db['password'].encode('utf-8')) == user_in_db['password']:
        secret = request.registry.settings['secret_passphrase']
        del user_in_db['_id']
        request.registry.db_mongo['users'].update({'id': form['user_name']},{'$set': {'connected': str(datetime.datetime.now())}})
        token = jwt.encode({'user': user_in_db,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=36000),
                            'aud': 'urn:geneulike/api'}, secret)
        return {'token' : token , 'status':'success'}
    else:
        return {'msg' : 'Invalide credentials', 'status': 'warning'}

@view_config(route_name='logged', renderer='json')
def logged(request):
    user = is_authenticated(request)
    if user is None:
        form = json.loads(request.body, encoding=request.charset)
        if form and 'token' in form:
            secret = request.registry.settings['secret_passphrase']
            auth = None
            try:
                auth = jwt.decode(form['token'], secret, audience='urn:geneulike/api')
            except Exception as e:
                return HTTPUnauthorized('Not authorized to access this resource')
            user = {'id': auth['user']['id'], 'token': auth}
            user_in_db = request.registry.db_mongo['users'].find_one({'id': user['id']})
            if user_in_db is None:
                # Create user
                user['status'] = 'pending_approval'
                if user['id'] in request.registry.admin_list:
                    user['status'] = 'approved'
                logging.info('Create new user '+user['id'])
                request.registry.db_mongo['users'].insert({'id': user['id'], 'status': user['status']})
            else:
                user_in_db['token'] = form['token']
                user = user_in_db
        else:
            return HTTPNotFound('Not logged')

    if user is not None and user['id'] in request.registry.admin_list:
        user['admin'] = True

    return user

@view_config(
    context='velruse.AuthenticationComplete',
)
def login_complete_view(request):
    context = request.context
    result = {
        'id': context.profile['verifiedEmail'],
        'provider_type': context.provider_type,
        'provider_name': context.provider_name,
        'profile': context.profile,
        'credentials': context.credentials,
    }
    secret = request.registry.settings['secret_passphrase']
    token = jwt.encode({'user': result,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=36000),
                        'aud': 'urn:geneulike/api'}, secret)
    return HTTPFound(request.static_url('geneulike:webapp/app/')+"index.html#login?token="+token)


