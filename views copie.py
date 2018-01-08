# -*- coding: utf-8 -*-

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden, HTTPUnauthorized
from pyramid.security import remember, forget
from pyramid.renderers import render_to_response
from pyramid.response import Response, FileResponse

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

import logging

import smtplib
import email.utils
import sys
if sys.version < '3':
    from email.MIMEText import MIMEText
else:
    from email.mime.text import MIMEText


@view_config(route_name='home')
def my_view(request):
    return HTTPFound(request.static_url('chemsign:webapp/app/'))

@view_config(route_name='count', renderer='json', request_method='GET')
def data_count(request):
    res_project = request.registry.db_mongo['project'].find_one({'id': 1})
    res_study = request.registry.db_mongo['study'].find_one({'id': 1})
    res_condition = request.registry.db_mongo['condition'].find_one({'id': 1})
    res_signature = request.registry.db_mongo['signature'].find_one({'id': 1})
    return res_project,res_study,res_condition,res_signature

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
            user = jwt.decode(bearer, secret, audience='urn:chemsign/api')
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
    return user_in_db

@view_config(route_name='user_message', renderer='json', request_method='POST')
def message_info(request):
    form = json.loads(request.body, encoding=request.charset)
    #print form
    formType = form['type']
    #print formType
    if formType == 'project' :
        request.registry.db_mongo['project'].update({'id': 1}, {'$inc': {'val': 1}})
        repos = request.registry.db_mongo['project'].find({'id': 1})
        result = []
        for res in repos:
            result.append(res)
        return result
    if formType == 'study' :
        request.registry.db_mongo['study'].update({'id': 1}, {'$inc': {'val': 1}})
        repos = request.registry.db_mongo['study'].find({'id': 1})
        result = []
        for res in repos:
            result.append(res)
        return result
    if formType == 'condition' :
        request.registry.db_mongo['condition'].update({'id': 1}, {'$inc': {'val': 1}})
        repos = request.registry.db_mongo['condition'].find({'id': 1})
        result = []
        for res in repos:
            result.append(res)
        return result
    if formType == 'signature' :
        request.registry.db_mongo['signature'].update({'id': 1}, {'$inc': {'val': 1}})
        repos = request.registry.db_mongo['signature'].find({'id': 1})
        result = []
        for res in repos:
            result.append(res)
        return result

@view_config(route_name='user_info', renderer='json', request_method='POST')
def user_info_update(request):
    user = is_authenticated(request)
    if user is None or user['id'] not in request.registry.admin_list:
        return HTTPUnauthorized('Not authorized to access this resource')
    if user['id'] != request.matchdict['id'] and user['id'] not in request.registry.admin_list:
        return HTTPUnauthorized('Not authorized to access this resource')
    form = json.loads(request.body, encoding=request.charset)
    tid = form['_id']
    del form['_id']
    request.registry.db_mongo['users'].update({'id': request.matchdict['id']}, form)
    form['_id'] = tid;
    return form

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
        return {'msg': 'emtpy fields, user name and password are mandatory'}
    user_in_db = request.registry.db_mongo['users'].find_one({'id': form['user_name']})
    print user_in_db
    if user_in_db is None :
        secret = request.registry.settings['secret_passphrase']
        token = jwt.encode({'user': {'id': form['user_name'],
                                     'password': bcrypt.hashpw(form['user_password'].encode('utf-8'), bcrypt.gensalt()),
                                     'first_name': form['first_name'],
                                     'last_name': form['last_name'],
                                     'institute': form['institute'],
                                     'laboratory': form['laboratory'],
                                     'country': form['country'],
                                     'address': form['address'],
                                     'referent': form['referent']
                                     },
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=36000),
                        'aud': 'urn:chemsign/api'}, secret)
        message = "You requested an account, please click on following link to validate it\n"
        message += request.host_url+'/app/index.html#/login?action=confirm_email&token='+token
        send_mail(request, form['user_name'], '[ToxSigN] Please validate your account', message)
        return {'msg': 'You will receive a confirmation email. Please click the link to verify your account.'}
    else :
        msg = 'This email is already taken.'
        return {'msg': msg}

@view_config(route_name='user_confirm_email', renderer='json', request_method='POST')
def confirm_email(request):
    form = json.loads(request.body, encoding=request.charset)
    if form and 'token' in form:
        secret = request.registry.settings['secret_passphrase']
        user_id = None
        user_password = None
        try:
            auth = jwt.decode(form['token'], secret, audience='urn:chemsign/api')
            user_id = auth['user']['id']
            user_password = auth['user']['password']
        except Exception:
            return HTTPForbidden()
        status = 'approved'
        msg = 'Email validated, you can now access to your account.'
        if user_id in request.registry.admin_list:
            status = 'approved'
            msg = 'Email validated, you can now log into the application'
        request.registry.db_mongo['users'].insert({'id': user_id,
                                                    'status': status,
                                                    'password': user_password,
                                                    'first_name': auth['user']['first_name'],
                                                    'last_name': auth['user']['last_name'],
                                                    'institute': auth['user']['institute'],
                                                    'laboratory': auth['user']['laboratory'],
                                                    'address': auth['user']['address'],
                                                    'referent': auth['user']['referent'],
                                                    'tool_history': [],
                                                    'selectedID':[]
                                                    })
        upload_path = os.path.join(request.registry.upload_path, user_id, 'dashboard')
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        return {'msg': msg}
    else:
        return HTTPForbidden()

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
        auth = jwt.decode(form['token'], secret, audience='urn:chemsign/recover')
        user_id = auth['user']['id']
        user_in_db = request.registry.db_mongo['users'].find_one({'id': user_id})
        if user_in_db is None:
            return HTTPNotFound('User does not exists')
        user_password = form['user_password']
        new_password = bcrypt.hashpw(form['user_password'].encode('utf-8'), bcrypt.gensalt())
        request.registry.db_mongo['users'].update({'id': user_id},{'$set': {'password': new_password}})
    except Exception:
        return HTTPForbidden()
    return {'msg': 'password updated'}


@view_config(route_name='message', renderer='json', request_method='POST')
def message_add(request):
    session_user = is_authenticated(request)
    if session_user is None:
        return HTTPForbidden()
    if session_user['status'] != 'approved':
        return {'msg': 'Your account needs to be approved first by administrator'}
    form = json.loads(request.body, encoding=request.charset)
    mess = {
        'title': form['title']
    }
    if 'message' in form:
        mess['message'] = form['message']
    if 'priority' in form:
        mess['priority'] = form['priority']
    if 'description' in form:
        mess['description'] = form['description']
    dt = datetime.datetime.utcnow()
    mess['submission_date'] = time.mktime(dt.timetuple())
    mess['last_updated'] = mess['submission_date']
    mess['status'] = 'private'
    mess['owner']= session_user['id']
    mess = request.registry.db_mongo['messages'].insert(mess)
    return {'msg': 'Message send.'}

@view_config(route_name='message_delete', renderer='json')
def message_delete(request):
    session_user = is_authenticated(request)
    form = json.loads(request.body, encoding=request.charset)
    if session_user['id'] not in request.registry.admin_list:
        return HTTPForbidden()
    dataset_id = form['_id']['$oid']
    request.registry.db_mongo['messages'].remove({'_id': ObjectId(dataset_id)})
    return {'msg': 'Message '+dataset_id+' removed'}

@view_config(route_name='admin_message', renderer='json', request_method='POST')
def message_update(request):
    session_user = is_authenticated(request)
    form = json.loads(request.body, encoding=request.charset)
    if session_user['id'] not in request.registry.admin_list:
        return HTTPForbidden()
    dataset_id = form['_id']['$oid']
    tid = form['_id']
    del form['_id']
    request.registry.db_mongo['messages'].update({'_id': ObjectId(dataset_id)}, form)
    form['_id'] = tid;
    return form

@view_config(route_name='datasets', renderer='json', request_method='GET')
def datasets(request):
    session_user = is_authenticated(request)
    if session_user is None:
        return {'msg': 'Your account needs to be approved first by administrator'}
    else:
        datasets = request.registry.db_mongo['datasets'].find({'$or': [
                                {'owner': session_user['id']},
                                {'collaborators': session_user['id']}
                                ]})
    result = []
    for dataset in datasets:
        result.append(dataset)
    return result


@view_config(route_name='datasets', renderer='json', request_method='POST')
def datasets_add(request):
    session_user = is_authenticated(request)
    if session_user is None:
        return HTTPForbidden()
    if session_user['status'] != 'approved':
        return {'msg': 'Your account needs to be approved first by administrator'}
    form = json.loads(request.body, encoding=request.charset)
    dataset = {
        'title': form['title']
    }
    if 'contributors' in form:
        dataset['contributors'] = form['contributors']
    if 'citations' in form:
        dataset['citations'] = form['citations']
    if 'description' in form:
        dataset['description'] = form['description']
    if 'result' in form:
        dataset['result'] = form['result']
    if 'overalldesign' in form:
        dataset['overalldesign'] = form['overalldesign']
    if 'ext_link' in form:
        dataset['ext_link'] = form['ext_link']
    dt = datetime.datetime.utcnow()
    dataset['id'] = form['id']
    dataset['submission_date'] = time.mktime(dt.timetuple())
    dataset['last_updated'] = dataset['submission_date']
    dataset['status'] = 'private'
    dataset['owner']= session_user['id']
    dataset['studies'] = []
    dataset['conditions'] = []
    dataset['confidence'] = ''
    dataset = request.registry.db_mongo['datasets'].insert(dataset)
    return dataset

@view_config(route_name='6', renderer='json', request_method='POST')
def dataset_signature_download(request):
    form = json.loads(request.body, encoding=request.charset)

    if form['status'] == 'public':
        upload_path = os.path.join(request.registry.public_path,form['dataset'],form['study'],form['condition'], form['signature'],form['file'])
        return {'url':upload_path}

    if form['status'] == 'private':
        session_user = is_authenticated(request)
        if session_user is None:
            return 'HTTPForbidden()'
        dataset = request.registry.db_mongo['datasets'].find_one({'id': form['dataset']})
        if dataset['status'] != 'public':
            if dataset['owner'] == session_user['id'] :
                upload_path = os.path.join(request.registry.upload_path,session_user['id'],form['dataset'],form['study'],form['condition'], form['signature'],form['file'])
                return {'url':upload_path}

    if form['status'] == 'dashboard':
        session_user = is_authenticated(request)
        if session_user is None:
            return 'HTTPForbidden()'
        upload_path = os.path.join("var","upload",session_user['id'],"documents",form['file'])
        print upload_path
        return {'url':upload_path}



    #dataset_id = request.matchdict['dataset']
    #dataset = request.registry.db_mongo['datasets'].find_one({'_id': ObjectId(dataset_id)})
    #if dataset['status'] == 'private':
        # Check if user is authenticated or provides a valid token
    #    session_user = is_authenticated(request)
    #    if session_user is None:
    #        token = None
    #        try:
    #            token = request.params['token']
    #        except Exception:
    #            token = None
    #        auth = None
    #        try:
    #            secret = request.registry.settings['secret_passphrase']
    #           # If decode ok and not expired
    #            auth = jwt.decode(token, secret, audience='urn:chemsign/api')
    #        except Exception as e:
    #            return HTTPUnauthorized('Not authorized to access this resource')
    #        if auth is None:
    #            return HTTPForbidden()
    #for study in dataset['treatments']:
    #    if study['title'] == request.matchdict['study']:
    #        signature = None
    #        for sig in study['signatures']:
    #            if sig['id'] == request.matchdict['signature']:
    #                signature = sig
    #                break
    #        (handle, tmp_file) = tempfile.mkstemp('.zip')
    #        z = zipfile.ZipFile(tmp_file, "w")
    #        for sig in signature['physio']:
    #            sig_file_id = sig['id']
    #            upload_path = os.path.join(request.registry.upload_path, request.matchdict['uid'], dataset_id)
    #            z.write(os.path.join(upload_path,sig_file_id), os.path.basename(sig_file_id))
    #        for sig in signature['genomic']:
    #            sig_file_id = sig['id']
    #            upload_path = os.path.join(request.registry.upload_path, request.matchdict['uid'], dataset_id)
    #            z.write(os.path.join(upload_path,sig_file_id), os.path.basename(sig_file_id))
    #        z.close()
    #        break
    #return FileResponse(tmp_file,
    #                            request=request,
    #                            content_type='application/zip')

@view_config(route_name='excel_signature_upload', renderer='json', request_method='POST')
def excel_signature_upload(request):
    session_user = is_authenticated(request)
    if session_user is None:
        return 'HTTPForbidden()'

    input_file = None
    try:
        input_file = request.POST['file'].file
    except Exception:
        return HTTPForbidden('no input file')
    tmp_file_name = uuid.uuid4().hex
    file_path = os.path.join('/tmp', '%s.sig' % tmp_file_name)
    temp_file_path = file_path + '~'

    # Finally write the data to a temporary file
    with open(temp_file_path, 'wb') as output_file:
        shutil.copyfileobj(input_file, output_file)
    # Now that we know the file has been fully saved to disk move it into place.
    upload_path = os.path.join(request.registry.upload_path, request.params['uid'], request.params['dataset'])
    #print upload_path
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    os.rename(temp_file_path, os.path.join(upload_path, tmp_file_name))

    input_file.seek(0)
    wb = xlrd.open_workbook(os.path.join(upload_path, tmp_file_name),encoding_override="cp1251")
    
 
    # List to hold dictionaries
    projects = []

    # Read first sheet for project information 
    sh = wb.sheet_by_index(0)
 
    # Iterate through each row in worksheet and fetch values into dict
    dt = datetime.datetime.utcnow()
    notaccepted = ['',' ','na','NA','n/a','N/A','none','N/a','n/A']
    try :
        for rownum in range(3, sh.nrows):
            row_values = sh.row_values(rownum)
            project = {}
            if row_values[8] == 'Interventional' or row_values[8] == 'Both' :
                
                request.registry.db_mongo['project'].update({'id': 1}, {'$inc': {'val': 1}})
                repos = request.registry.db_mongo['project'].find({'id': 1})
                result = ""
                for res in repos:
                    result = res
                
                project['title'] = row_values[0]
                project['owner'] = session_user['id']
                project['description'] = row_values[1]
                project['overalldesign'] = row_values[2]
                project['result'] = row_values[3]
                project['authors'] = row_values[4]
                project['pubmed'] = row_values[5].split(',')
                project['contributors'] = []
                project['contributors'].append(row_values[6])
                project['ext_link'] = row_values[7]
                project['studies'] = []
                project['submission_date'] = time.mktime(dt.timetuple())
                project['last_updated'] = project['submission_date']
                project['email'] = session_user['id']
                project['status'] = 'private'
                project['id'] = 'TSP' + str(result['val'])
                print result['val']

                # Read second sheet for interventional study information 
                sh_st = wb.sheet_by_index(1)
                for rownum in range(11, sh_st.nrows):
                    study = {}
                    row_values = sh_st.row_values(rownum)
                    study['Associated project'] = row_values[0]
                    if ( study['Associated project'] == project['title']):
                        request.registry.db_mongo['study'].update({'id': 1}, {'$inc': {'val': 1}})
                        repos = request.registry.db_mongo['study'].find({'id': 1})
                        result = ""
                        for res in repos:
                            result = res
                        study['type'] = 'interventional'
                        study['asso'] = project['id']
                        study['id'] = 'TSE' + str(result['val'])
                        study['interventional_title'] = row_values[1]
                        study['interventional_info'] = row_values[15]
                        study['interventional_design'] = row_values[2]
                        study['interventional_results'] = row_values[3]
                        study['interventional_description'] = row_values[4]
                        study['interventional_experimental_type'] = row_values[5]
                        study['interventional_vitro'] = {}
                        study['interventional_vivo'] = {}
                        study['interventional_exvivo'] = {}
                        study['interventional_other'] = {}
                        sex = row_values[8]
                        organismStud = row_values[6]

                        if (study['interventional_experimental_type'] == 'in vivo'):
                            study['interventional_experimental_type'] = 'in_vivo'
                            resultOrga=[]
                            repos = []
                            if row_values[6] not in notaccepted :
                                repo = request.registry.db_mongo['species.tab'].find({'id': row_values[6]})
                                for val in repo :
                                    repos = val
                                study['interventional_vivo']['organism'] = repos['name']
                                organismStud = repos['name']
                                resultOrga.append(repos['id'])
                                resultOrga.append(repos['name'])
                                for i in repos['synonyms'] :
                                    resultOrga.append(i)
                                for j in repos['direct_parent'] :
                                    resultOrga.append(j)
                                for k in repos['all_parent'] :
                                    resultOrga.append(k)
                                for z in repos['all_name'] :
                                    resultOrga.append(z)
                            else :
                                study['interventional_vivo']['organism'] =''
                            study['orgatag']=resultOrga

                            study['interventional_vivo']['strain'] = row_values[7]
                            study['interventional_vivo']['sex'] = row_values[8]
                            study['interventional_vivo']['devstage'] = row_values[9]


                        if (study['interventional_experimental_type'] == 'ex vivo'):
                            study['interventional_experimental_type'] = 'ex_vivo'
                            study['interventional_exvivo']['strain'] = row_values[7]
                            study['interventional_exvivo']['sex'] = row_values[8]
                            study['interventional_exvivo']['devstage'] = row_values[9]
                            resultOrga=[]
                            repos = []
                            if row_values[6] not in notaccepted :
                                repo = request.registry.db_mongo['species.tab'].find({'id': row_values[6]})
                                for val in repo :
                                    repos = val

                                study['interventional_exvivo']['organism'] = repos['name']
                                organismStud = repos['name']
                                resultOrga.append(repos['id'])
                                resultOrga.append(repos['name'])
                                for i in repos['synonyms'] :
                                    resultOrga.append(i)
                                for j in repos['direct_parent'] :
                                    resultOrga.append(j)
                                for k in repos['all_parent'] :
                                    resultOrga.append(k)
                                for z in repos['all_name'] :
                                    resultOrga.append(z)
                                
                            else :
                                study['interventional_exvivo']['organism'] =''
                            study['orgatag']=resultOrga
                            study['tissuetag'] =[]

                            resultTissue=[]
                            repos = []
                            if row_values[10] not in notaccepted :
                                repo = request.registry.db_mongo['tissue.tab'].find({'id': row_values[10]})
                                for val in repo :
                                    repos = val
                                study['interventional_exvivo']['tissue'] = repos['name']
                                resultTissue.append(repos['id'])
                                resultTissue.append(repos['name'])
                                for i in repos['synonyms'] :
                                    resultTissue.append(i)
                                for j in repos['direct_parent'] :
                                    resultTissue.append(j)
                                for k in repos['all_parent'] :
                                    resultTissue.append(k)
                                for z in repos['all_name'] :
                                    resultTissue.append(z)
                                
                            else:
                                study['interventional_exvivo']['tissue'] =''
                            study['interventional_exvivo']['tissue'] = ''

                        if (study['interventional_experimental_type'] == 'in vitro'):
                            study['interventional_experimental_type'] = 'in_vitro'
                            resultOrga=[]
                            repos = []
                            if row_values[6] not in notaccepted :
                                repo = request.registry.db_mongo['species.tab'].find({'id': row_values[6]})
                                for val in repo :
                                    repos = val
                                study['interventional_vitro']['organism'] = repos['name']
                                organismStud = repos['name']
                                resultOrga.append(repos['id'])
                                resultOrga.append(repos['name'])
                                for i in repos['synonyms'] :
                                    resultOrga.append(i)
                                for j in repos['direct_parent'] :
                                    resultOrga.append(j)
                                for k in repos['all_parent'] :
                                    resultOrga.append(k)
                                for z in repos['all_name'] :
                                    resultOrga.append(z)
                            else :
                                study['interventional_vitro']['organism']=''
                            study['orgatag']=resultOrga

                            study['interventional_vitro']['strain'] = row_values[7]
                            study['interventional_vitro']['sex'] = row_values[8]

                            resultTissue=[]
                            repos = []
                            if row_values[10] not in notaccepted :
                                repo = request.registry.db_mongo['tissue.tab'].find({'id': row_values[10]})
                                for val in repo :
                                    repos = val
                                study['interventional_vitro']['tissue'] = repos['name']
                                resultTissue.append(repos['id'])
                                resultTissue.append(repos['name'])
                                for i in repos['synonyms'] :
                                    resultTissue.append(i)
                                for j in repos['direct_parent'] :
                                    resultTissue.append(j)
                                for k in repos['all_parent'] :
                                    resultTissue.append(k)
                                for z in repos['all_name'] :
                                    resultTissue.append(z)

                            else:
                                study['interventional_vitro']['tissue']=''
                            study['tissuetag']=resultTissue


                            study['interventional_vitro']['generation'] = row_values[11]
                            study['interventional_vitro']['experimental'] = row_values[12]

                            if(study['interventional_vitro']['experimental'] == 'cell line'):
                                study['interventional_vitro']['experimental'] = 'cell_line'

                                #resultCellline=[]
                                #repos = []
                                if row_values[13] not in notaccepted :
                                    repo = request.registry.db_mongo['cell_line.tab'].find({'id': row_values[13]})
                                    for val in repo :
                                        repos = val
                                    print repos['name']
                                    study['interventional_vitro']['cell_line'] = repos['name']
                                    #resultCellline.append(repos['id'])
                                    #resultCellline.append(repos['name'])
                                    #for i in repos['synonyms'] :
                                    #    resultCellline.append(i)
                                    #for j in repos['direct_parent'] :
                                    #    resultCellline.append(j)
                                    #for k in repos['all_parent'] :
                                    #    resultCellline.append(k)
                                    #for z in repos['all_name'] :
                                    #    resultCellline.append(z)
                                    #study['celltag']=resultCellline
                                else :
                                    study['interventional_vitro']['cell_line'] = ''
                                study['interventional_vitro']['passage'] = row_values[14]

                            if(study['interventional_vitro']['experimental'] == 'primary cell culture'):
                                study['interventional_vitro']['experimental'] = 'primary_cell_culture'

                                resultCell=[]
                                repos = []
                                if row_values[13] not in notaccepted :
                                    repo = request.registry.db_mongo['cell.tab'].find({'id': row_values[13]})
                                    for val in repo :
                                        repos = val
                                    study['interventional_vitro']['cell_name'] = repos['name']
                                    resultCell.append(repos['id'])
                                    resultCell.append(repos['name'])
                                    for i in repos['synonyms'] :
                                        resultCell.append(i)
                                    for j in repos['direct_parent'] :
                                        resultCell.append(j)
                                    for k in repos['all_parent'] :
                                        resultCell.append(k)
                                    for z in repos['all_name'] :
                                        resultCell.append(z)
                                else:
                                    study['interventional_vitro']['cell_name'] =''
                                study['celltag']=resultCell


                        if (study['interventional_experimental_type'] == 'other'):
                            resultOrga=[]
                            repos = []
                            if row_values[6] not in notaccepted :
                                repo = request.registry.db_mongo['species.tab'].find({'id': row_values[6]})
                                for val in repo :
                                    repos = val
                                study['interventional_other']['organism'] = repos['name']
                                organismStud = repos['name']
                                resultOrga.append(repos['id'])
                                resultOrga.append(repos['name'])
                                for i in repos['synonyms'] :
                                    resultOrga.append(i)
                                for j in repos['direct_parent'] :
                                    resultOrga.append(j)
                                for k in repos['all_parent'] :
                                    resultOrga.append(k)
                                for z in repos['all_name'] :
                                    resultOrga.append(z)
                            else :
                                study['interventional_other']['organism'] = ''
                            study['orgatag']=resultOrga

                            study['interventional_other']['strain'] = row_values[7]
                            study['interventional_other']['sex'] = row_values[8]
                            resultTissue=[]
                            repos = []
                            if row_values[10] not in notaccepted :
                                repo = request.registry.db_mongo['tissue.tab'].find({'id': row_values[10]})
                                for val in repo :
                                    repos = val
                                study['interventional_other']['tissue'] = repos['name']
                                resultTissue.append(repos['id'])
                                resultTissue.append(repos['name'])
                                for i in repos['synonyms'] :
                                    resultTissue.append(i)
                                for j in repos['direct_parent'] :
                                    resultTissue.append(j)
                                for k in repos['all_parent'] :
                                    resultTissue.append(k)
                                for z in repos['all_name'] :
                                    resultTissue.append(z)
                            else :
                                study['interventional_other']['tissue'] =''
                            
                            study['tissuetag']=resultTissue

                            resultCell=[]
                            repos = []
                            if row_values[13] not in notaccepted :
                                repo = request.registry.db_mongo['cell.tab'].find({'id': row_values[13]})
                                for val in repo :
                                    repos = val
                                study['interventional_other']['cell_name'] = repos['name']
                                resultCell.append(repos['id'])
                                resultCell.append(repos['name'])
                                for i in repos['synonyms'] :
                                    resultCell.append(i)
                                for j in repos['direct_parent'] :
                                    resultCell.append(j)
                                for k in repos['all_parent'] :
                                    resultCell.append(k)
                                for z in repos['all_name'] :
                                    resultCell.append(z)
                                
                            else:
                                study['interventional_other']['cell_name']
                            study['celltag']=resultCell
                            study['interventional_other']['generation'] = row_values[11]

                        study['conditions'] = []
                        study['signatures'] = []

                        # Check all associated conditions
                        sh_cond = wb.sheet_by_index(2)
                        asso ={}
                        sign={}
                        signatures=[]
                        for rownum in range(4, sh_cond.nrows):
                            
                            row_values = sh_cond.row_values(rownum)
                            if row_values[0] == study['interventional_title']:
                                if row_values[1] not in asso :
                                    condtitle = row_values[1]
                                    asso[row_values[1]] = {}
                                    asso[row_values[1]]['condition'] = {}
                                    asso[row_values[1]]['treatment'] = {}
                                    asso[row_values[1]]['signature'] = {}
                                    asso[row_values[1]]['chemname'] = []
                                    request.registry.db_mongo['condition'].update({'id': 1}, {'$inc': {'val': 1}})
                                    repos = request.registry.db_mongo['condition'].find({'id': 1})
                                    result = ""
                                    for res in repos:
                                        result = res
                                    asso[row_values[1]]['condition']['title'] = row_values[1]
                                    asso[row_values[1]]['condition']['treatment'] = []
                                    asso[row_values[1]]['condition']['study'] = study['id']
                                    asso[row_values[1]]['condition']['id'] = 'TST' + str(result['val'])
                                    asso[row_values[1]]['condition']['chemicaltag'] =[]
                                    treatment = {}
                                    treatment['chemicals'] = []
                                    treatment['biological'] = []
                                    treatment['physical'] = []
                                
                                chemical={}
                                if row_values[2] == 'chemical':
                                    
                                    chemical['dose'] = row_values[6]
                                    chemical['dose_unit'] = row_values[7]
                                    chemical['exposure_duration'] = row_values[8]
                                    chemical['exposure_duration_unit'] = row_values[9]
                                    chemical['exposure_frequency'] = row_values[10]
                                    chemical['info'] = row_values[11]


                                    repos = []
                                    
                                    if row_values[3] not in notaccepted:
                                        repo = request.registry.db_mongo['chemical.tab'].find({'id': row_values[3]})
                                        for val in repo :
                                            repos = val
                                        asso[row_values[1]]['condition']['chemicaltag'].append(repos['id'])
                                        asso[row_values[1]]['condition']['chemicaltag'].append(repos['name'])
                                        chemical['name'] = repos['name']
                                        asso[row_values[1]]['chemname'].append(repos['name'])
                                        for i in repos['synonyms'] :
                                            asso[row_values[1]]['condition']['chemicaltag'].append(i)
                                        for j in repos['direct_parent'] :
                                            asso[row_values[1]]['condition']['chemicaltag'].append(j)
                                        for k in repos['all_parent'] :
                                            asso[row_values[1]]['condition']['chemicaltag'].append(k)
                                        for z in repos['all_name'] :
                                            asso[row_values[1]]['condition']['chemicaltag'].append(z)
                                    else :
                                        chemical['name'] = ''

                                    chemical['route'] = row_values[5]
                                    chemical['vehicule'] = row_values[4]
                                    exposure = int(chemical['exposure_duration'])
                                    exposure_unit = chemical['exposure_duration_unit']
                                    times = 0

                                    if exposure_unit == 'days' :
                                        times = exposure * 1440
                                    if exposure_unit == 'hours' :
                                        times = exposure * 60
                                    if exposure_unit == 'hours' :
                                        times = exposure * 60
                                    if exposure_unit == 'minutes' :
                                        times = exposure * 1
                                    if exposure_unit == 'secondes' :
                                        times = exposure/60
                                    chemical['time'] = times 
                                    #treatment['chemicals'].append(chemical)
                                    # Check all associated signature
                                    sh_sign = wb.sheet_by_index(3)
                                    for rownum in range(11, sh_sign.nrows):
                                        row_values = sh_sign.row_values(rownum)
                                        if row_values[0] == study['interventional_title'] and row_values[1] == condtitle:
                                            
                                            sign[condtitle]= []

                                            if True :
                                                signature = {}
                                                signature['celltag'] = []
                                                signature['supfile'] = []
                                                signature['file'] = []
                                                signature['chemical'] = asso[row_values[1]]['chemname']
                                                signature['chemicaltag'] = []
                                                signature['genomic'] = []
                                                signature['molecular'] = []
                                                signature['physio'] = []
                                                signature['orgatag'] = []
                                                signature['technotag'] = []
                                                signature['file'] = []
                                                tmpdir = uuid.uuid4().hex
                                                signature['tmpdir'] = tmpdir
                                                signature['gene_up'] = ""
                                                signature['gene_down'] = ""
                                                signature['signature_type'] = row_values[2]
                                                signature['route'] = []
                                                signature['title'] = row_values[3]
                                                signature['asso_cond'] = asso[condtitle]['condition']['id']
                                                signature['type'] = row_values[2]
                                                if 'celltag' in study :
                                                    signature['chemicaltag'] = study['celltag']
                                                signature['devstage'] = row_values[6]
                                                signature['diseasetag'] = []
                                                
                                                signature['generation'] = row_values[5]
                                                    
                                                if signature['signature_type'] == 'physiological':
                                                    physio = {}
                                                    physio['expe_info'] = row_values[7]
                                                    if row_values[8] not in notaccepted :
                                                        repo = request.registry.db_mongo['disease.tab'].find({'id': row_values[8]})
                                                        for val in repo :
                                                            repos = val
                                                        physio['asso'] = repos['name']
                                                        signature['diseasetag'].append(repos['id'])
                                                        signature['diseasetag'].append(repos['name'])
                                                        for i in repos['synonyms'] :
                                                            signature['diseasetag'].append(i)
                                                        for j in repos['direct_parent'] :
                                                            signature['diseasetag'].append(j)
                                                        for k in repos['all_parent'] :
                                                            signature['diseasetag'].append(k)
                                                        for z in repos['all_name'] :
                                                            signature['diseasetag'].append(z)
                                                    else :
                                                        physio['asso'] = ''
                                                    physio['obs_effect'] = row_values[9]
                                                    physio['sample'] = row_values[10]
                                                    physio['control'] = row_values[11]
                                                    physio['fc'] = row_values[12]
                                                    physio['pvalue'] = row_values[13]
                                                    physio['statistical'] = row_values[14]
                                                    signature['physio'].append(physio)

                                                if signature['signature_type'] == 'genomic':
                                                    geno = {}
                                                    geno['expe_info'] = row_values[7]
                                                    if row_values[7] not in notaccepted :
                                                        repo = request.registry.db_mongo['experiment.tab'].find({'id': row_values[17]})
                                                        for val in repo :
                                                            repos = val
                                                        geno['techno'] = repos['name']
                                                        signature['technotag'].append(repos['id'])
                                                        signature['technotag'].append(repos['name'])
                                                        for i in repos['synonyms'] :
                                                            signature['technotag'].append(i)
                                                        for j in repos['direct_parent'] :
                                                            signature['technotag'].append(j)
                                                        for k in repos['all_parent'] :
                                                            signature['technotag'].append(k)
                                                        for z in repos['all_name'] :
                                                            signature['technotag'].append(z)
                                                    else :
                                                        geno['techno'] =''

                                                    geno['plateform'] = row_values[22]
                                                    geno['obs_effect'] = row_values[18]

                                                    geno['sample'] = row_values[10]
                                                    geno['control'] = row_values[11]
                                                    geno['fc'] = row_values[12]
                                                    geno['pvalue'] = row_values[13]
                                                    geno['statistical'] = row_values[14]
                                                    signature['genomic'].append(geno)

                                                if signature['signature_type'] == 'molecular':
                                                    mol = {}
                                                    if row_values[15] not in notaccepted :
                                                        repo = request.registry.db_mongo['chemical.tab'].find({'id': row_values[15]})
                                                        for val in repo :
                                                            repos = val
                                                        mol['extractedmolecule'] = repos['name']
                                                        signature['chemicaltag'].append(repos['id'])
                                                        signature['chemicaltag'].append(repos['name'])
                                                        for i in repos['synonyms'] :
                                                            signature['chemicaltag'].append(i)
                                                        for j in repos['direct_parent'] :
                                                            signature['chemicaltag'].append(j)
                                                        for k in repos['all_parent'] :
                                                            signature['chemicaltag'].append(k)
                                                        for z in repos['all_name'] :
                                                            signature['chemicaltag'].append(z)
                                                        mol['extractproto'] = row_values[16]
                                                    else:
                                                        mol['extractedmolecule'] =''

                                                    if row_values[17] not in notaccepted :
                                                        repo = request.registry.db_mongo['experiment.tab'].find({'id': row_values[17]})
                                                        for val in repo :
                                                            repostech = val
                                                        mol['techno'] = repostech['name']
                                                        signature['technotag'].append(repos['id'])
                                                        signature['technotag'].append(repos['name'])
                                                        for i in repostech['synonyms'] :
                                                            signature['technotag'].append(i)
                                                        for j in repostech['direct_parent'] :
                                                            signature['technotag'].append(j)
                                                        for k in repostech['all_parent'] :
                                                            signature['technotag'].append(k)
                                                        for z in repostech['all_name'] :
                                                            signature['technotag'].append(z)
                                                    else:
                                                        mol['techno'] =''

                                                    mol['obs_effect'] = row_values[9]
                                                    mol['sample'] = row_values[10]
                                                    mol['control'] = row_values[11]
                                                    mol['fc'] = row_values[12]
                                                    mol['pvalue'] = row_values[13]
                                                    mol['expe_info'] = row_values[7]
                                                    mol['statistical'] = row_values[14]
                                                    signature['molecular'].append(mol)

                                                request.registry.db_mongo['signature'].update({'id': 1}, {'$inc': {'val': 1}})
                                                repos = request.registry.db_mongo['signature'].find({'id': 1})
                                                result = ""
                                                for res in repos:
                                                    result = res
                                                signature['id'] = 'TSS'+str(result['val'])
                                                signature['organism'] = organismStud
                                                signature['orgatag'] = study['orgatag']
                                                signature['sex'] = sex
                                                signature['time'] = chemical['time'] 
                                                signature['tissuetag'] = []
                                                if 'tissuetag' in study :
                                                    signature['tissuetag'] = study['tissuetag']

                                                signature['chemical'].append(chemical['name'])
                                                for i in asso[condtitle]['condition']['chemicaltag'] :
                                                    signature['chemicaltag'].append(i)
                                                signature['route'].append(chemical['route'])
                                            sign[condtitle].append(signature)
                                            signatures.append(signature)


                                treatment['chemicals'].append(chemical)
                                if treatment not in asso[condtitle]['condition']['treatment']:
                                    asso[condtitle]['condition']['treatment'].append(treatment)
                        
                        already_in = [] 
                        for cond in asso :
                            if asso[cond]['condition'] not in study['conditions'] :
                                study['conditions'].append(asso[cond]['condition'])

                        for sgnt in signatures :
                            if sgnt['title'] not in already_in:
                                print sgnt['title']
                                already_in.append(sgnt['title'])
                                study['signatures'].append(sgnt)

                        



                        project['studies'].append(study)

            if row_values[8] == 'Observational' or row_values[8] == 'Both' :
                
                request.registry.db_mongo['project'].update({'id': 1}, {'$inc': {'val': 1}})
                repos = request.registry.db_mongo['project'].find({'id': 1})
                result = ""
                for res in repos:
                    result = res
                
                project['title'] = row_values[0]
                project['owner'] = session_user['id']
                project['description'] = row_values[1]
                project['overalldesign'] = row_values[2]
                project['result'] = row_values[3]
                project['authors'] = row_values[4]
                project['pubmed'] = []
                project['pubmed'] = row_values[5].split(',')
                project['contributors'] = []
                project['contributors'].append(row_values[6])
                project['ext_link'] = row_values[7]
                project['studies'] = []
                project['submission_date'] = time.mktime(dt.timetuple())
                project['last_updated'] = project['submission_date']
                project['email'] = session_user['id']
                project['status'] = 'private'
                project['id'] = 'TSP' + str(result['val'])
                study = {}
                cond={}
                treatment={}
                signature = {}

                # Read second sheet for observational study information 
                sh_st = wb.sheet_by_index(4)
                for rownum in range(8, sh_st.nrows):
                    row_values = sh_st.row_values(rownum)
                    if row_values[0] == project['title'] :
                        sttitle = row_values[1]
                        if sttitle not in study :
                            study[sttitle] ={}
                            request.registry.db_mongo['study'].update({'id': 1}, {'$inc': {'val': 1}})
                            repos = request.registry.db_mongo['study'].find({'id': 1})
                            result = ""
                            for res in repos:
                                result = res
                            study[sttitle]['id'] = 'TSE' + str(result['val'])
                            study[sttitle]['type'] = 'observational'
                            study[sttitle]['observational_title'] = row_values[1]
                            study[sttitle]['observational_description'] = row_values[2]
                            study[sttitle]['observational_pmid'] = row_values[3]
                            study[sttitle]['observational_results'] = row_values[5]
                            study[sttitle]['authors'] = row_values[4]
                            study[sttitle]['observational_inclusion'] = row_values[6]
                            study[sttitle]['observational_exclusion'] = row_values[7]
                            study[sttitle]['observational_population_size'] = row_values[8]
                            study[sttitle]['observational_overalldesign'] = row_values[9]
                            resultOrga=[]
                            repos = []
                            if row_values[10] not in notaccepted :
                                repo = request.registry.db_mongo['species.tab'].find({'id': row_values[10]})
                                for val in repo :
                                    repos = val
                                study[sttitle]['observational_organism'] = repos['name']
                                organismStud = repos['name']
                                resultOrga.append(repos['id'])
                                resultOrga.append(repos['name'])
                                for i in repos['synonyms'] :
                                    resultOrga.append(i)
                                for j in repos['direct_parent'] :
                                    resultOrga.append(j)
                                for k in repos['all_parent'] :
                                    resultOrga.append(k)
                                for z in repos['all_name'] :
                                    resultOrga.append(z)
                            else :
                                study[sttitle]['observational_organism'] = ''
                            study[sttitle]['orgatag']=resultOrga

                            study[sttitle]['observational_inclusion_period'] = row_values[11]
                            study[sttitle]['observational_followup'] = row_values[12]
                            study[sttitle]['observational_adjustment'] = row_values[13]
                            study[sttitle]['signatures'] =[]
                            study[sttitle]['conditions'] =[]
                            cond[sttitle] ={}
                            treatment[sttitle] ={}
                            signature[sttitle] ={}
                            
                        repos = []
                        if row_values[21] not in notaccepted :
                            repo = request.registry.db_mongo['chemical.tab'].find({'id': row_values[21]})
                            for val in repo :
                                repos = val
                            chemname = repos['name']
                        else :
                            chemname = 'None'

                        #Condition
                        if row_values[14] == "":
                            title = row_values[20]+' exposure of '+chemname
                        else:
                            title = row_values[14]
                        if title not in cond[sttitle] :
                            cond[sttitle][title] = {}
                            request.registry.db_mongo['condition'].update({'id': 1}, {'$inc': {'val': 1}})
                            repos = request.registry.db_mongo['condition'].find({'id': 1})
                            result = ""
                            for res in repos:
                                result = res
                                            
                            cond[sttitle][title]['study'] = study[sttitle]['id']
                            cond[sttitle][title]['id'] = 'TST' + str(result['val'])
                            cond[sttitle][title]['title'] = title
                            cond[sttitle][title]['sex'] = row_values[15]
                            cond[sttitle][title]['population_age'] = row_values[16]
                            cond[sttitle][title]['location'] = row_values[17]
                            cond[sttitle][title]['ref'] = row_values[18]
                            cond[sttitle][title]['matrice'] = row_values[19]
                            cond[sttitle][title]['chemicaltag'] = []
                            cond[sttitle][title]['treatment'] = []
                            cond[sttitle][title]['chemicaltag'] = []
                            cond[sttitle][title]['dev']=row_values[26]
                            treatment[sttitle][title] = {}
                            treatment[sttitle][title]['chemicals'] =[]
                            treatment[sttitle][title]['verif'] = []

                            treat = chemname+' '+row_values[22]
                            if treat not in treatment[sttitle][title]['verif'] :
                                treatment[sttitle][title]['verif'].append(treat)
                                if row_values[20] == "Chemical" :
                                    chem = {}
                                    repos = []
                                    if row_values[21] not in notaccepted :
                                        print row_values[21]
                                        repo = request.registry.db_mongo['chemical.tab'].find({'id': row_values[21]})
                                        for val in repo :
                                            repos = val
                                        cond[sttitle][title]['chemicaltag'].append(repos['id'])
                                        cond[sttitle][title]['chemicaltag'].append(repos['name'])
                                        chem['name'] = repos['name']
                                        treatment[sttitle][title]['verif'].append(treat)
                                        for i in repos['synonyms'] :
                                            cond[sttitle][title]['chemicaltag'].append(i)
                                        for j in repos['direct_parent'] :
                                            cond[sttitle][title]['chemicaltag'].append(j)
                                        for k in repos['all_parent'] :
                                            cond[sttitle][title]['chemicaltag'].append(k)
                                        for z in repos['all_name'] :
                                            cond[sttitle][title]['chemicaltag'].append(z)
                                    else :
                                        chem['name'] = ''
                                    chem['dose_unit']=row_values[23]
                                    chem['dose']=row_values[22]
                                    chem['exposure_duration']=row_values[24]
                                    chem['info']=row_values[25]
                                if chem not in treatment[sttitle][title]['chemicals'] :
                                    treatment[sttitle][title]['chemicals'].append(chem)

                        if row_values[27] == "":
                            sigtitle = "Signature of the "+ title
                        else :
                            sigtitle = row_values[27]

                        if sigtitle not in signature[sttitle]:
                            signature[sttitle][sigtitle]={}
                            request.registry.db_mongo['signature'].update({'id': 1}, {'$inc': {'val': 1}})
                            repos = request.registry.db_mongo['signature'].find({'id': 1})
                            result = ""
                            for res in repos:
                                result = res        
                            signature[sttitle][sigtitle]['id'] = 'TSS' + str(result['val'])
                            signature[sttitle][sigtitle]['asso_cond'] = cond[sttitle][title]['id']
                            signature[sttitle][sigtitle]['chemical'] = []
                            signature[sttitle][sigtitle]['file'] = []
                            signature[sttitle][sigtitle]['supfiles'] = ""
                            signature[sttitle][sigtitle]['gene_up'] = ""
                            signature[sttitle][sigtitle]['gene_down'] = ""
                            signature[sttitle][sigtitle]['signature_type'] = "environmental"
                            signature[sttitle][sigtitle]['chemicaltag'] = []
                            signature[sttitle][sigtitle]['diseasetag'] = []
                            for chemi in treatment[sttitle][title]['chemicals'] :
                                signature[sttitle][sigtitle]['chemical'].append(chemi['name'])
                            signature[sttitle][sigtitle]['chemicaltag'].append(cond[sttitle][title]['chemicaltag'])
                            signature[sttitle][sigtitle]['devstage'] = row_values[31]
                            signature[sttitle][sigtitle]['env'] =[]
                            env ={}
                            if row_values[33] not in notaccepted :
                                repo = request.registry.db_mongo['disease.tab'].find({'id': row_values[33]})
                                for val in repo :
                                    repos = val
                                env['asso'] = repos['name']
                                signature[sttitle][sigtitle]['diseasetag'].append(repos['id'])
                                signature[sttitle][sigtitle]['diseasetag'].append(repos['name'])
                                for i in repos['synonyms'] :
                                    signature[sttitle][sigtitle]['diseasetag'].append(i)
                                for j in repos['direct_parent'] :
                                    signature[sttitle][sigtitle]['diseasetag'].append(j)
                                for k in repos['all_parent'] :
                                    signature[sttitle][sigtitle]['diseasetag'].append(k)
                                for z in repos['all_name'] :
                                    signature[sttitle][sigtitle]['diseasetag'].append(z)
                            else :
                                env['asso'] =''
                            env['expe_info'] = row_values[32]
                            env['obs_effect'] = row_values[34]
                            env['outcome'] = row_values[28]
                            env['statsign'] = row_values[35]
                            signature[sttitle][sigtitle]['env'].append(env)
                            signature[sttitle][sigtitle]['generation'] = row_values[30]
                            signature[sttitle][sigtitle]['organism'] = study[sttitle]['observational_organism']
                            signature[sttitle][sigtitle]['orgatag'] = study[sttitle]['orgatag']
                            signature[sttitle][sigtitle]['sex'] = row_values[29]
                           
                            signature[sttitle][sigtitle]['title'] = sigtitle
                            signature[sttitle][sigtitle]['other_stat'] = row_values[36]
                        if treatment[sttitle][title] not in cond[sttitle][title]['treatment']:
                            cond[sttitle][title]['treatment'].append(treatment[sttitle][title])

                for stud in study:
                    for conds in cond[stud]:
                        study[stud]['conditions'].append(cond[stud][conds])
                    for signs in signature[stud] :
                        study[stud]['signatures'].append(signature[stud][signs])
                    project['studies'].append(study[stud])


                #Strain / sub species ID Sex 
                #Developmental stage Tissue ID   Generation  Type    Cell name   Passage

            projects.append(project) 
            dataset = request.registry.db_mongo['datasets'].insert(project)
            eform = request.registry.db_mongo['datasets'].find_one({'id': project['id']})
            del eform['_id']
                    
            #print "INDEX DATASET : " +Dataset_ID
            bulk_insert = ''
            for study in eform['studies']:
                for sig in study['signatures']:
                    bulk_insert += "{ \"index\" : { \"_index\" : \"toxsign\", \"_type\": \"signature\" , \"_id\" : \""+project['id']+"_"+study['id']+'_'+sig['id']+"\" } }\n"
                    mysig = copy.deepcopy(eform)
                    mystudy = copy.deepcopy(study)
                    mystudy['signatures']  = [sig]
                    mysig['studies'] = [mystudy]
                    mysig['dataset'] = project['id']
                    bulk_insert += json.dumps(mysig)+"\n"
            if bulk_insert:
                request.registry.es.bulk(body=bulk_insert)
        os.remove(os.path.join(upload_path, tmp_file_name))

        return projects
    except :
        print sys.exc_info()[1]
        return {'msg': 'ERROR : read excel file. Please make sure you use the correct template. If this error persists, please contact the site administrator.','status':'1'}
    

    

@view_config(route_name='dataset_signature_upload', renderer='json', request_method='POST')
def dataset_signature_upload(request):
    session_user = is_authenticated(request)
    if session_user is None:
        return HTTPForbidden()
    print request.params
    assocond = request.params['assocond']
    input_file = None
    try:
        input_file = request.POST['file'].file
    except Exception:
        return HTTPForbidden('no input file')

    tmp_file_name = ""
    if request.params['type'] == '0' :
        tmp_file_name = 'genomic_upward_tmp.txt'
    if request.params['type'] == '1' :
        tmp_file_name = 'genomic_downward_tmp.txt'
    if request.params['type'] == '2' :
        tmp_file_name = 'genomic_interrogated_genes_tmp.txt'
    if request.params['type'] == '3' :
        tmp_file_name = request.params['name']
    file_path = os.path.join('/tmp', '%s.sig' % tmp_file_name)

    if request.params['tmpdir'] == "":
        dir_tmp_name = uuid.uuid4().hex
    else :
        dir_tmp_name = request.params['tmpdir']

    temp_file_path = file_path + '~'

    try :
        # Finally write the data to a temporary file
        input_file.seek(0)
        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)

        # Now that we know the file has been fully saved to disk move it into place.
        upload_path = os.path.join(request.registry.upload_path,request.params['uid'],'tmp', request.params['dataset'],request.params['stud'],assocond,dir_tmp_name)
        #print upload_path
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        os.rename(temp_file_path, os.path.join(upload_path, tmp_file_name))
    except Exception as inst:
        print 'Error occurred while attempting to read the file : '
        print inst
        return {'msg':'An error occurred while attempting to read the file. If this error persists, please contact the site administrator.','status': '1'}
    
    if request.params['type'] == '3' :
        return {'msg':"Additional file checked and uploded !", 'dirname':dir_tmp_name, 'status': '0' }
    #Check file if all entries are in db
    try :
        if request.params['db'] == 'Entrez' :
            check_file = open(os.path.join(upload_path, tmp_file_name),'r')
            lId = []
            for lineID in check_file.readlines():
                if lineID != '' and lineID != 'NA' and lineID != '-' and lineID != 'na' and lineID != ' ' and lineID != 'Na' :
                    IDs = lineID.replace('\n','\t').replace(',','\t').replace(';','\t')
                    lId.append(IDs.split('\t')[0])
            lId = list(set(lId))
            check_file.close()
            dataset_in_db = list(request.registry.db_mongo['genes'].find( {"GeneID": {'$in': lId}},{ "GeneID": 1,"Symbol": 1,"HID":1, "_id": 0 } ))
            lresult = {}
            for i in dataset_in_db:
                lresult[i['GeneID']]=[i['Symbol'],i['HID']]

            #Create 4 columns signature file
            if os.path.isfile(os.path.join(upload_path, tmp_file_name.replace('_tmp',''))):
                os.remove(os.path.join(upload_path, tmp_file_name.replace('_tmp','')))

            os.remove(os.path.join(upload_path, tmp_file_name))
            check_files = open(os.path.join(upload_path, tmp_file_name.replace('_tmp','')),'a')
            have_wrong = 0
            for ids in lId :
                if ids in lresult :
                    check_files.write(ids+'\t'+lresult[ids][0]+'\t'+lresult[ids][1].replace('\n','')+'\t1\n')
                else :
                    check_files.write(ids+'\t'+'NA\tNA'+'\t0\n')  
                    have_wrong = 1                  
            check_files.close()
            print "File checked and uploded !"
            if have_wrong == 0 :
                return {'msg':"File checked and uploded !", 'list':lId, 'dirname':dir_tmp_name, 'status': '0' }
            else : 
                return {'msg':"Warning ! Some IDs are not EntrezGene ID or are desprecated", 'list':lId, 'dirname':dir_tmp_name, 'status': '0' }
 
    except :
        print sys.exc_info()[1]
        return {'msg':"TOXsIgN can't read your file. Please make sure you use the correct format. If this error persists, please contact the site administrator.",'status': '1' }

    return {'msg': "TOXsIgN can't read your file. Please make sure you use the correct format. If this error persists, please contact the site administrator."}


@view_config(route_name='dataset', renderer='json', request_method='GET')
def user_dataset_get(request):

    dataset_id = request.matchdict['dataset']
    session_user = is_authenticated(request)
    dataset = request.registry.db_mongo['datasets'].find_one({'id': dataset_id})
    return dataset

@view_config(route_name='dataset_delete', renderer='json')
def dataset_delete(request):
    session_user = is_authenticated(request)
    form = json.loads(request.body, encoding=request.charset)
    if session_user['id'] not in request.registry.admin_list:
        return HTTPForbidden()
    datasetID = form['id']
    request.registry.db_mongo['datasets'].remove({'id': datasetID,'owner':session_user['id']})
    return {'msg': 'Dataset '+datasetID+'validated'}

@view_config(route_name='search', renderer='json', request_method='POST')
def search(request):
    form = json.loads(request.body, encoding=request.charset)
    request_query = form['query']
    if 'from' in form :
        from_val = form['from']
    else :
        from_val = 0


    page = request.registry.es.search(
    index = request.registry.es_db,
      search_type = 'query_then_fetch',
      size = 100,
      from_=from_val,
      body = {"query" : { "query_string" : {"query" :request_query,"default_operator":"AND",'analyzer': "standard"}}})

    #print {"query" : { "bool" : filter_query}}
    return page

@view_config(route_name='dataset', renderer='json', request_method='PUT')
def user_dataset_edit(request):
    dataset_id = request.matchdict['dataset']
    session_user = is_authenticated(request)
    if session_user is None :
        return HTTPForbidden()

    dataset_in_db = request.registry.db_mongo['datasets'].find_one({'id': dataset_id})
    if dataset_in_db['status'] != 'public':
        if not (dataset_in_db['owner'] == session_user['id'] or session_user['id'] in request.registry.admin_list or session_user['id'] in dataset_in_db['collaborators']):
            return HTTPForbidden()

    form = json.loads(request.body, encoding=request.charset)
    tid = form['_id']
    del form['_id']

    # Only admin can change status
    if session_user['id'] not in request.registry.admin_list:
        form['status'] = dataset_in_db['status']

    page = request.registry.es.search(
      index = request.registry.es_db,
      scroll = '1m',
      search_type = 'scan',
      size = 1000,
      body = {
        "query": {
            "match" : {
                "dataset" : dataset_id
                }
            }
        }
    )
    sid = page['_scroll_id']
    scroll_size = page['hits']['total']
    bulk_delete = ''
    while (scroll_size > 0):
        page = request.registry.es.scroll(scroll_id = sid, scroll = '1m')
        # Update the scroll ID
        sid = page['_scroll_id']
        # Get the number of results that we returned in the last scroll
        scroll_size = len(page['hits']['hits'])
        for dataset_index in page['hits']['hits']:
            bulk_delete += "{ \"delete\" : { \"_index\": \""+request.registry.es_db+"\", \"_type\": \"signature\", \"_id\" : \""+dataset_index['_id']+"\" } }\n"

    if bulk_delete:
        request.registry.es.bulk(body=bulk_delete)

    request.registry.db_mongo['datasets'].update({'id': dataset_id}, form)

    bulk_insert = ''
    for study in form['studies']:
        for sig in study['signatures']:
            bulk_insert += "{ \"index\" : { \"_index\" : \""+request.registry.es_db+"\", \"_type\": \"signature\" , \"_id\" : \""+dataset_id+"_"+study['id']+'_'+sig['id']+"\" } }\n"
            mysig = copy.deepcopy(form)
            # for ontlogy field x.y.z
            # mongo.find(obo) mysig(x.y.z)
            # mysig(x.y.z) =  (mysig(x.y.z) , obo parents ids, obo parent names)
            mystudy = copy.deepcopy(study)
            mystudy['signatures']  = [sig]
            mysig['studies'] = [mystudy]
            mysig['dataset'] = dataset_id
            bulk_insert += json.dumps(mysig)+"\n"
    if bulk_insert:
        request.registry.es.bulk(body=bulk_insert)

    form['_id'] = tid
    return form

@view_config(route_name='user_recover', renderer='json', request_method='POST')
def user_recover(request):
    form = json.loads(request.body, encoding=request.charset)
    user_in_db = request.registry.db_mongo['users'].find_one({'id': form['user_name']})
    if user_in_db is None:
        return {'msg': 'User not found'}
    secret = request.registry.settings['secret_passphrase']
    del user_in_db['_id']
    token = jwt.encode({'user': user_in_db,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=36000),
                        'aud': 'urn:chemsign/recover'}, secret)
    message = "You requested a password reset, please click on following link to reset your password:\n"
    message += request.host_url+'/app/index.html#/recover?token='+token
    send_mail(request, form['user_name'], '[ToxSigN] Password reset request', message)
    logging.info(message)
    return {'msg': 'You will receive an email you must acknowledge it to reset your password.'}


@view_config(route_name='login', renderer='json', request_method='POST')
def login(request):
    form = json.loads(request.body, encoding=request.charset)
    user_in_db = request.registry.db_mongo['users'].find_one({'id': form['user_name']})
    if user_in_db is None:
        return {'msg': 'Invalid email'}

    if bcrypt.hashpw(form['user_password'].encode('utf-8'), user_in_db['password'].encode('utf-8')) == user_in_db['password']:
        secret = request.registry.settings['secret_passphrase']
        del user_in_db['_id']
        token = jwt.encode({'user': user_in_db,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=36000),
                            'aud': 'urn:chemsign/api'}, secret)
        return {'token': token}
    else:
        return {'msg': 'Invalid credentials'}

@view_config(route_name='logged', renderer='json')
def logged(request):
    user = is_authenticated(request)
    if user is None:
        form = json.loads(request.body, encoding=request.charset)
        if form and 'token' in form:
            secret = request.registry.settings['secret_passphrase']
            auth = None
            try:
                auth = jwt.decode(form['token'], secret, audience='urn:chemsign/api')
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
                        'aud': 'urn:chemsign/api'}, secret)
    return HTTPFound(request.static_url('chemsign:webapp/app/')+"index.html#login?token="+token)




@view_config(route_name='dataset_delete', renderer='json', request_method='POST')
def dataset_delete(request):
    user = is_authenticated(request)
    user_id = user['id']
    form = json.loads(request.body, encoding=request.charset)
    owner = form['owner']
    if user['id'] == owner :
        id = form['id']
        request.registry.db_mongo['datasets'].remove({"id":id})
    #search = form['search']
    #database = form['database']
    #regx = re.compile(search, re.IGNORECASE)
    #repos = request.registry.db_mongo[database].find({"$or":[{'name':regx},{'synonyms':regx}]})
    #result = []
    #for dataset in repos:
    #    result.append(dataset)
    #return result


@view_config(route_name='autocompletion', renderer='json', request_method='POST')
def autocompletion(request):
    form = json.loads(request.body, encoding=request.charset)
    search = form['search']
    database = form['database']
    regx = re.compile(search, re.IGNORECASE)
    repos = request.registry.db_mongo[database].find({"$or":[{'name':regx},{'synonyms':regx}]})
    result = []
    for dataset in repos:
        result.append(dataset)
    return result

@view_config(route_name='getOnto', renderer='json', request_method='POST')
def getOnto(request):
    form = json.loads(request.body, encoding=request.charset)
    search = form['search']
    database = form['database']
    
    regx = re.compile(search, re.IGNORECASE)
    repos = request.registry.db_mongo[database].find({'name': search})
    result = []
    for dataset in repos:
        result.append(dataset)
    return result

@view_config(route_name='database', renderer='json', request_method='POST')
def show_db(request):
    form = json.loads(request.body, encoding=request.charset)
    rangedb = form['to']
    min = int(rangedb.split('-')[0])
    max = int(rangedb.split('-')[1])
    session_user = is_authenticated(request)
    #if session_user is None:
        #return HTTPForbidden()
    res = request.registry.db_mongo['datasets'].find({'status':'public'}).distinct("id")

    result = []
    for i in res :
        result.append(i)
    if max > len(result) :
        pub = list(request.registry.db_mongo['datasets'].find({ 'id': { '$in': result[min:] } } ))
        return pub
    else :
        pub = list(request.registry.db_mongo['datasets'].find({ 'id': { '$in': result[min:max] } } ))
        return pub

@view_config(route_name='pending', renderer='json', request_method='GET')
def get_pending(request):
    session_user = is_authenticated(request)
    if session_user is None:
        return HTTPForbidden()
    res = request.registry.db_mongo['datasets'].find({'status':'pending approval'})
    result = []
    for i in res :
        result.append(i)
    return result

@view_config(route_name='8', renderer='json', request_method='POST')
def switch_public(request):
    session_user = is_authenticated(request)
    form = json.loads(request.body, encoding=request.charset)
    if session_user is None:
        return HTTPForbidden()
    if session_user['id'] not in request.registry.admin_list:
        return HTTPForbidden()
    if form['uid'] != session_user['id']:
        return HTTPForbidden()
    data = form['dataset']
    request.registry.db_mongo['datasets'].update({ 'id': data['id'] },{ '$set': {'status': 'public'} })
    eform = request.registry.db_mongo['datasets'].find_one({'id': data['id']})
    del eform['_id']
                    
    #print "INDEX DATASET : " +Dataset_ID
    bulk_insert = ''
    for study in eform['studies']:
        for sig in study['signatures']:
            bulk_insert += "{ \"index\" : { \"_index\" : \"toxsign\", \"_type\": \"signature\" , \"_id\" : \""+data['id']+"_"+study['id']+'_'+sig['id']+"\" } }\n"
            mysig = copy.deepcopy(eform)
            mystudy = copy.deepcopy(study)
            mystudy['signatures']  = [sig]
            mysig['studies'] = [mystudy]
            mysig['dataset'] = data['id']
            bulk_insert += json.dumps(mysig)+"\n"
    if bulk_insert:
        request.registry.es.bulk(body=bulk_insert)
    return {'msg':"Status changed.",'status': '1' }


@view_config(route_name='myproject', renderer='json', request_method='POST')
def showproject(request):
    form = json.loads(request.body, encoding=request.charset)
    session_user = is_authenticated(request)
    if session_user is None :
        return HTTPForbidden()
    user = session_user['id']
    rangedb = form['to']
    filter_val = form['filter']
    min = int(rangedb.split('-')[0])
    max = int(rangedb.split('-')[1])
    session_user = is_authenticated(request)
    #if session_user is None:
        #return HTTPForbidden()
    if filter_val == "all":
        res = request.registry.db_mongo['datasets'].find({'owner': user})
        result = []
        for i in res :
            result.append(i)
        public =[]
        for dataset in result :
            public.append(dataset)

        if max > len(public) :
            return public[min:]
        else :
            return public[min:max]

    if filter_val == "private":
        res = request.registry.db_mongo['datasets'].find({'owner': user,'status':'private'})
        result = []
        for i in res :
            result.append(i)
        public =[]
        for dataset in result :
            public.append(dataset)

        if max > len(public) :
            return public[min:]
        else :
            return public[min:max]

    if filter_val == "public":
        res = request.registry.db_mongo['datasets'].find({'owner': user,'status':'public'})
        result = []
        for i in res :
            result.append(i)
        public =[]
        for dataset in result :
            public.append(dataset)

        if max > len(public) :
            return public[min:]
        else :
            return public[min:max]

    if filter_val == "pending":
        res = request.registry.db_mongo['datasets'].find({'owner': user,'status':'pending approval'})
        result = []
        for i in res :
            result.append(i)
        public =[]
        for dataset in result :
            public.append(dataset)

        if max > len(public) :
            return public[min:]
        else :
            return public[min:max]

@view_config(route_name='alldatauser', renderer='json', request_method='POST')
def alldatauser(request):
    session_user = is_authenticated(request)
    if session_user is None :
        return HTTPForbidden()
    user = session_user['id']
    res = request.registry.db_mongo['datasets'].find({'owner': user})
    result = []
    for i in res :
        result.append(i)
    return result

@view_config(route_name='getlast', renderer='json', request_method='GET')
def getlast(request):
    res = request.registry.db_mongo['datasets'].find({'status':'public'})
    result = []
    for i in res :
        result.append(i)
    return result[-3:]

@view_config(route_name='getnews', renderer='json', request_method='GET')
def getnews(request):

    newsfile = open('News/news.txt','r')
    result = {}
    for lignes in newsfile.readlines():
        if lignes[0] == '>':
            result['title'] = lignes[1:]
        if lignes[0] == '@':
            result['new'] = lignes[1:]
    return result

@view_config(route_name='savefile', renderer='json', request_method='POST')
def savefile(request):
    form = json.loads(request.body, encoding=request.charset)
    all_name = form['did']+'_'+form['sid']+'.sign'
    upload_path = os.path.join(request.registry.upload_path,form['uid'],'tmp', form['did'],form['eid'],form['cid'],form['sid'])

    old_path = os.path.join(request.registry.upload_path,form['uid'],'tmp', form['did'],form['eid'],form['cid'],form['tmpdir'])
    adm_path_signame = os.path.join(request.registry.admin_path,'signatures_data',all_name)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    for filesTmp in os.listdir(old_path):
        os.rename(old_path+'/'+filesTmp, upload_path+'/'+filesTmp)
    
    #admin
    if not os.path.exists(os.path.join(request.registry.admin_path,'signatures_data')):
        os.makedirs(os.path.join(request.registry.admin_path,'signatures_data'))
    if os.path.isfile(adm_path_signame):
        os.remove(adm_path_signame)

    check_files = open(adm_path_signame,'a')
    lfiles = {'genomic_upward.txt':'1','genomic_downward.txt':'-1','genomic_interrogated_genes.txt':'0'}
    val_geno = 0
    for files in os.listdir(upload_path) :
        if files in lfiles:
            fileIn = open(os.path.join(upload_path,files),'r')
            for linesFile in fileIn.readlines():
                check_files.write(linesFile.replace('\n','')+'\t'+lfiles[files]+'\n')
            fileIn.close()
    check_files.close()

@view_config(route_name='delfile', renderer='json', request_method='POST')
def delfile(request):
    form = json.loads(request.body, encoding=request.charset)
    file_toremove = os.path.join(request.registry.upload_path,form['uid'],'tmp', form['did'],form['eid'],form['cid'],form['sid'],form['file']) 
    print file_toremove
    if os.path.isfile(file_toremove):
        os.remove(file_toremove)
    else :
        return {'msg':"ERROR - File doesn't exist"}

    if form['type'] == 'genomic':
        #Recreate allfile in admin dir
        all_name = form['sid']+'.txt'
        upload_path = os.path.join(request.registry.upload_path,form['uid'],'tmp', form['did'],form['eid'],form['cid'],form['sid'])
        adm_path_signame = os.path.join(request.registry.admin_path,'signatures_data',all_name)
        check_files = open(adm_path_signame,'a')
        lfiles = {'genomic_upward.txt':'1','genomic_downward.txt':'-1','genomic_interrogated_genes.txt':'0'}
        val_geno = 0
        for files in os.listdir(upload_path) :
            if files in lfiles:
                fileIn = open(os.path.join(upload_path,files),'r')
                for linesFile in fileIn.readlines():
                    check_files.write(linesFile.replace('\n','')+'\t'+lfiles[files]+'\n')
                fileIn.close()
        check_files.close()

@view_config(route_name='listfiles', renderer='json', request_method='GET')
def listfiles(request):
    session_user = is_authenticated(request)
    lfile = []
    if session_user is None :
        return lfile
    user = session_user['id']
    document_path = os.path.join(request.registry.upload_path,user,'documents')
    if not os.path.exists(document_path):
        os.makedirs(document_path)
    for files in os.listdir(document_path):
        lfile.append(files)
    return lfile

@view_config(route_name='picksign', renderer='json', request_method='POST')
def picksign(request):
    session_user = is_authenticated(request)
    if session_user is None :
        return HTTPForbidden()
    form = json.loads(request.body, encoding=request.charset)
    if form['uid'] != session_user['id']:
        return HTTPForbidden()
    dashboard = request.registry.db_mongo['datasets'].find_one({'id': form['dataset']})
    try :
        for stud in dashboard['studies']:
            for sign in stud['signatures']:
                if sign['id'] == form['signID']:
                    if sign['genomic'] != []:
                        homoup = []

                        #get homologeneIDs
                        data = list(request.registry.db_mongo['homoloGene'].find( {"Gene_ID": {'$in': sign['genomic'][0]['up'].split('\n')}},{ "HID": 1, "_id": 0 } ))
                        for ids in data :
                            homoup.append(ids["HID"])
                        homodown = []
                        data = list(request.registry.db_mongo['homoloGene'].find( {"Gene_ID": {'$in': sign['genomic'][0]['down'].split('\n')}},{ "HID": 1, "_id": 0 } ))
                        for ids in data :
                            homodown.append(ids["HID"])
                        #Create result
                        dresult = {'id':sign['id'],'up':sign['genomic'][0]['up'].split('\n'),'down':sign['genomic'][0]['down'].split('\n'),'hup':homoup,'hdown':homodown,'title':sign['title'],'adm':form['dataset']+'_'+form['signID']}

        #update information
        request.registry.db_mongo['users'].update({ 'id': form['uid'] },{ '$push': { 'selectedID': dresult } })
        return {'msg':'Signature added to your dashboard','status': '0'}
    except :
        print sys.exc_info()[1]
        return {'msg':"An error has occurred. If this error persists, please contact the site administrator.",'status': '1' }

@view_config(route_name='venn', renderer='json', request_method='POST')
def venn(request):
    session_user = is_authenticated(request)
    if session_user is None :
        return HTTPForbidden()
    form = json.loads(request.body, encoding=request.charset)
    if form['uid'] != session_user['id']:
        return HTTPForbidden()

    if form['from'] == 'venn':
        try :

            ldata = form['data'].split('\n')
            name = ldata[0]
            idList = ldata[1:]
            dt = datetime.datetime.utcnow()
            z = time.mktime(dt.timetuple())
            filename = str(z)+"-" + name.replace(':','').replace(' ','_')
            user = session_user['id']
            document_path = os.path.join(request.registry.upload_path,user,'documents')
            fileIn = open(os.path.join(document_path,filename),'w')
            fileIn.write('\n'.join(idList))
            fileIn.close()
            return {'msg':'File save in your dashboard'}
        except :
            print sys.exc_info()[1]
            return {'msg':"An error has occurred. If this error persists, please contact the site administrator.",'status': '1' }

    if form['from'] == 'compare':
        try :

            name = "Conversion"
            idList = form['data']
            dt = datetime.datetime.utcnow()
            z = time.mktime(dt.timetuple())
            filename = str(z)+"-"+form['type']+"-" + name.replace(':','').replace(' ','_')
            user = session_user['id']
            document_path = os.path.join(request.registry.upload_path,user,'documents')
            fileIn = open(os.path.join(document_path,filename),'w')
            fileIn.write('\n'.join(idList))
            fileIn.close()
            return {'msg':'File save in your dashboard'}
        except :
            print sys.exc_info()[1]
            return {'msg':"An error has occurred. If this error persists, please contact the site administrator.",'status': '1' }

@view_config(route_name='viewfile', renderer='json', request_method='POST')
def selected_file_view(request):
    session_user = is_authenticated(request)
    if session_user is None :
        return HTTPForbidden()
    form = json.loads(request.body, encoding=request.charset)
    if form['uid'] != session_user['id']:
        return HTTPForbidden()
    try :
        file_selected = form['file']
        document_path = os.path.join(request.registry.upload_path,form['uid'],'documents')
        fileIn = open(os.path.join(document_path,file_selected),'r')
        lId = []
        for line in fileIn.readlines():
            lId.append(line.replace('\n',''));
        fileIn.close()
        result = '\n'.join(lId)
        return {'data':result,'msg':'File loadwith success','status':"0"}
    except :
        print sys.exc_info()[1]
        return {'msg':"An error has occurred. If this error persists, please contact the site administrator.",'status': '1' }

@view_config(route_name='2', renderer='json', request_method='POST')
def load_convert_file(request):
    session_user = is_authenticated(request)
    if session_user is None:
        return HTTPForbidden()
    print request.params
    input_file = None
    try:
        input_file = request.POST['file'].file
    except Exception:
        return HTTPForbidden('no input file')

    tmp_file_name = ""
    dt = datetime.datetime.utcnow() + datetime.timedelta(seconds=36000)
    tmp_file_name = str(dt) + request.params['name']
    file_path = os.path.join('/tmp', '%s.sig' % tmp_file_name)
    print file_path
    temp_file_path = file_path + '~'

    try :
        # Finally write the data to a temporary file
        input_file.seek(0)
        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)

        # Now that we know the file has been fully saved to disk move it into place.
        upload_path = os.path.join(request.registry.upload_path,request.params['uid'],'documents')
        #print upload_path
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        os.rename(temp_file_path, os.path.join(upload_path, tmp_file_name))
        fileIn = open(os.path.join(upload_path, tmp_file_name),'r')
        lId = []
        for line in fileIn.readlines():
            lId.append(line.replace('\n',''))
        fileIn.close()
        result = '\n'.join(lId)
        return {'data':result,'msg':'File load with success','status': '0'} 
    except :
        print sys.exc_info()[1]
        print 'Error occurred while attempting to read the file : '
        return {'msg':'An error occurred while attempting to read the file. If this error persists, please contact the site administrator.','status': '1'}

@view_config(route_name='3', renderer='json', request_method='POST')
def getconvert(request):
    session_user = is_authenticated(request)
    if session_user is None :
        return HTTPForbidden()
    form = json.loads(request.body, encoding=request.charset)
    if form['uid'] != session_user['id']:
        return HTTPForbidden()
    try :
        if form['convert'] == 'HE' :
            lHE = []
            data = list(request.registry.db_mongo['homoloGene'].find( {"HID": {'$in': form['data']},'Taxonomy_ID':form['species']},{ "HID": 1, "Gene_ID": 1, "Gene_Symbol":1,'Taxonomy_ID':1,"_id": 0 } ))
            lHE = data
            return {'msg':'Conversion complete','data':lHE,'status': '0'}
        if form['convert'] == 'EH' :
            lEH = []
            data = list(request.registry.db_mongo['homoloGene'].find( {"Gene_ID": {'$in': form['data']},'Taxonomy_ID':form['species']},{ "HID": 1, "Gene_ID": 1, "Gene_Symbol":1,'Taxonomy_ID':1,"_id": 0 } ))
            lEH = data
            return {'msg':'Conversion complete','data':lHE,'status': '0'}

    except :
        print sys.exc_info()[1]
        return {'msg':"An error has occurred. If this error persists, please contact the site administrator.",'status': '1' }


@view_config(route_name='4', renderer='json', request_method='POST')
def enrich(request):
    session_user = is_authenticated(request)
    if session_user is None :
        return HTTPForbidden()
    form = json.loads(request.body, encoding=request.charset)
    print form
    if form['uid'] != session_user['id']:
        return HTTPForbidden()
    try :
        forms = form['filter']
        adm_path_signame = os.path.join(request.registry.admin_path,'signatures_data',form['adm']+'.txt.enr')
        orgafile = {'pvalue':7,'pbh':8,'r':2,'n':4}
        if os.path.isfile(adm_path_signame):
            if os.path.getsize(adm_path_signame) == 0 :
                return {'msg':'No enrichment are available','Bp':[],'Disease': [],'Mf':[],'Cc':[] ,'status':"0"}
            else :
                lbp=[]
                lcc=[]
                lds=[]
                lmf=[]
                fileGo = open(adm_path_signame,'r')
                L = fileGo.readlines()
                fileGo.close()

                R = [e.split('\t')  for e in L]#creation list fichier
                #print len(R)
                for i in forms :
                    if forms[i]['param'] == 'lt' :
                        R = [x for x in R if float(x[orgafile[i]])<=float(forms[i]['value'])]
                        
                    if forms[i]['param'] == 'gt' :
                        R = [x for x in R if float(x[orgafile[i]])>=float(forms[i]['value'])]
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
        else :
            return {'msg':'The enrichment for the selected signature is not calculate yet. Please come back later','status':"0"}

    except :
        print sys.exc_info()[1]
        return {'msg':"An error has occurred. If this error persists, please contact the site administrator.",'status': '1' }

@view_config(route_name='5', renderer='json', request_method='POST')
def delInfo(request):
    session_user = is_authenticated(request)
    if session_user is None :
        return HTTPForbidden()
    form = json.loads(request.body, encoding=request.charset)
    if form['uid'] != session_user['id']:
        return HTTPForbidden()
    if form['type'] == 'file' :
        try :
            file_selected = form['object']
            document_path = os.path.join(request.registry.upload_path,form['uid'],'documents',file_selected)
            os.remove(document_path)
            return {'msg':'File delete with success','status':"0"}
        except :
            print sys.exc_info()[1]
            return {'msg':"An error has occurred. If this error persists, please contact the site administrator.",'status': '1' }
    if form['type'] == 'signature' :
        try :
            request.registry.db_mongo['users'].update({ 'id': form['uid'] },{ '$pull': { 'selectedID': form['object'] } })
            return {'msg':'Signature delete with success','status':"0"}
        except :
            print sys.exc_info()[1]
            return {'msg':"An error has occurred. If this error persists, please contact the site administrator.",'status': '1' }

@view_config(route_name='7', renderer='json', request_method='POST')
def switchstatus(request):
    session_user = is_authenticated(request)
    if session_user is None :
        return HTTPForbidden()
    form = json.loads(request.body, encoding=request.charset)
    if form['uid'] != session_user['id']:
        return HTTPForbidden()
    data = form['dataset']
    request.registry.db_mongo['datasets'].update({ 'id': data['id'] },{ '$set': {'status': 'pending approval'} })
    return {'msg':"Status changed.",'status': '1' }



