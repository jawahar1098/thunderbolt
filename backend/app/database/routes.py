from app.database import database_bp
from app.database.lib.handlefiles import *
from flask import *
from flask import request, jsonify
import flask
from loguru import logger
import os
from datetime import datetime
import time
from app.cdat.lib.rfi import * 
import requests
from pathlib import Path
from app.auth.routes import token_required
import flask_cors


@database_bp.route('/zipupload', methods=['POST', 'GET'])
@flask_cors.cross_origin(origin="*", supports_credentials=True)
@token_required
def zipupload(current_user):
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    invalidfiles = []
    files = request.files.getlist('files')
    username = request.form.get('username')
    filetype = request.form.get('filetype')
    foldername = datetime.now().strftime("%d%M%Y%H%M%S%f%z")
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/zipupload','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':f'totalfiles{len(files)}'})
    
    zipfiles = []
    if filetype == "zip":
        try:
            for file in files:
                print(file, "======+++++++++++++============")
                originalname = file.filename
                # filepath = '/home/vasanth_rvs/Documents/Ingestion_files_testing/zipfiles/' + foldername
                filepath = f'{os.getcwd()}/app/database/zipfiles/'
                if not os.path.exists(filepath):
                    os.makedirs(filepath)
                file.save(os.path.join(filepath,originalname))
                print(filepath, "----------")
                logger.info("Unzipping files")
                unzip_files(f'{filepath}/{originalname}')
                zipfiles.append(originalname.split(".")[0])
                # logger.info("Initating parser")
                # data = redy_to_parse_zipfiles(zippath)
                # if data == 'Operator not found' or data == 'Invalid file' or data == 'parsing error':
                #     invalidfiles.append(originalname)
            payload = {'zipname':zipfiles,'mode':'automation','user':username}
            response = requests.post('http://ingestion_files:5015/ingestion', json=payload)
            # response = requests.post('http://10.50.50.230:5010/ingestion', json=payload)
            print(response.text)
        except Exception as e:
            logger.error(f"error while ingestion, {str(e)}")
    else:
        for file in files:
            print(file,"ppppppppppppppppppppppppppp")
            originalname = file.filename
            # filepath = Path(f'/home/vasanth_rvs/Documents/Ingestion_files_testing/parse_files/Direct_files/{foldername}').mkdir(parents=True, exist_ok=True)
            # print("filepath : ",filepath)
            # filepath = '/home/vasanth_rvs/Documents/Ingestion_files_testing/parse_files/Direct_files/' + foldername
            filepath = f'{os.getcwd()}/app/database/parse_files/Direct_files/{foldername}'
            print(filepath,"====================================",originalname)
            ext_path = f"Direct_files/{foldername}"
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            
            file.save(os.path.join(filepath,originalname))
            print('svesss')
            fuuid = datetimee.now().strftime("%d%m%Y%H%M%S%f%z")[:17]
            direct_files(f"{filepath}/{originalname}", filetype, fuuid, username,'manual',ext_path)


            # if data == 'Operator not found' or data == 'Invalid file' or data == 'parsing error':
            #     invalidfiles.append(_f.split("/")[-1])
            # print(invalidfiles, "--")
        print("Ingestionnnnnnnnnnnnnnn")
        payload = {'zipname':'','mode':'manual','user':username}
        response = requests.post('http://ingestion_files:5015/ingestion', json=payload)
        # response = requests.post('http://10.50.50.230:5010/ingestion', json=payload)
        print(response.text)
        # logger.error(f"error while ingestion, {str(e)}")

        # upload = towercdr.update_files(casename,filepath,casetype)
        # if upload:

    # updatetickets_cdr()
    # updatetickets_imei()
    # update_towercdr()
    # print(data, "-in routes-----------")
    return jsonify({'message': 'success', 'invalidfiles': invalidfiles})

@database_bp.route("/getjson", methods=["POST"])
@flask_cors.cross_origin(origin="*", supports_credentials=True)
@token_required
def jsonfile(current_user):
    print('innnnnnnnnnnnnnnnnnn')
    if request.method == "POST":
        print("IN post database")

        files = request.files.getlist('files')
        casename = request.form.get('casename')
        casetype = request.form.get('filetype')
        user = request.form.get('user')
        caseid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
        print(casename, casetype, user,"=========================")
        invalidfiles = []

        for file in files:
            print(file)
            originalname = file.filename
            filetype = os.path.splitext(originalname)[1]
            print(filetype)
            # folder_path = '/home/vasanth_rvs/Documents/Ingestion_files_testing/case_uploads/'+casetype
            folder_path = f'{os.getcwd()}/app/database/case_uploads/{casetype}'
            ext_path = f"/case_uploads/{casetype}"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            filepath = f'{folder_path}/{originalname}'
            # file.save(filepath)
            file.save(os.path.join(folder_path,originalname))

            # print(filepath, "----------")
            fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:17]
            mode = 'case'
            direct_files(filepath, casetype, fuuid, user,mode,ext_path,casename)
            # query = {'filename': filepath.split("/")[-1], 'file_location': filepath, 'filetype': filetype, 'provider': "",
            #          'parsing_status': 'not_parsed', 'duplicates': '', 'total_doc': '', 'file_hash': '', 'fuuid': fuuid, 'mode': mode}
            # mongodata.filemanage.insert_one(query)
        query = {'casename':casename,'username':user,'casetype':casetype}
        getdata = mongothunder.casedata.find_one(query)
        if getdata is not None:
            updatefiles = getdata.get('file_count') + len(files)
            mongothunder.casedata.update_one(query,{'$set':{'file_count':updatefiles}})
        else:
            in_query = {'casename':casename,'casetype':casetype,'username':user,'caseid':caseid,'file_count':len(files),'rfi':0,'status':'processing','parsed_files':0,'duplicate_files':0}
            mongothunder.casedata.insert_one(in_query)
        
        payload = {'zipname':'','mode':'case','user':user}
        response = requests.post('http://ingestion_files:5015/ingestion', json=payload)
        # response = requests.post('http://0.0.0.0:5015/ingestion', json=payload)
        print(response.text)
            
    # redflag.matched_bparty_contact(casename,casetype,user)
    return jsonify({'message': 'sucess', 'invaild_files': invalidfiles})



@database_bp.route('/filestatus', methods=['POST', 'GET'])
@flask_cors.cross_origin(origin="*", supports_credentials=True)
@token_required
def filestatus():
    # coord = flask.request.get_json('coordinates')
    dates = flask.request.get_json('startdate')
    mode = dates['mode']
    print(dates, "result")
    st_date = dates.get('startdate', "")
    lt_date = dates.get('lastdate', '')
    page_view = dates.get('page_view', False)
    currentpage = dates.get('currentpage', False)
    items = dates.get('items', False)
    type_data = dates.get('parser_type', False)
    st_timestamp = False
    ls_timestamp = False
    print(page_view, "Items")
    if st_date != "":
        startdate = datetime.strptime(dates['startdate'], "%Y-%m-%d")
        startdate = startdate.timestamp()
        st_timestamp = int(startdate)
    if lt_date != "":
        lastdate = datetime.strptime(dates['enddate'], "%Y-%m-%d")
        lastdate = lastdate.timestamp()
        ls_timestamp = int(lastdate)

    get_data = retrieve_data(
        mode, st_timestamp, ls_timestamp, currentpage, items , type_data)

    return jsonify({'status': "success", 'data': get_data})


@database_bp.route('/mail_stat', methods=['POST', 'GET'])
def mail_status():
    get_data = mail_stat()
    return jsonify({'status': "success", 'data': get_data})


@database_bp.route('/picture', methods=['POST', 'GET'])
def get_picture():
    print("---------------get picture-----------")
    tic = time.time()
    data = flask.request.get_json('number')
    print(data, "----------number picture----------")
    req_toc = time.time() - tic
    response = profile_img(data['number'])
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    return response


@database_bp.route("/attach/<path:path>")
def attachment_files(path):
    path = "/" + path
    # print(path)
    # return app.send_static_file(path)
    # print(path)
    return send_file(path)

@database_bp.route('/fileupdate', methods = ['GET','POST'])
def fileupdate():
    getdata = ingestion_stat()
    res = {'data':getdata, 'showprogress':'true' if len(getdata)>0 else 'false'}
    return jsonify(res)



# apr 16_s
@database_bp.route('/get_undefined_count')
@flask_cors.cross_origin(origin="*", supports_credentials=True)
@token_required
def find_undefined_count(current_user):
    undefined_count = mongodata.filemanage.count_documents({"filetype": "undefined"})
    return jsonify({"count":undefined_count})

@database_bp.route('/get_undefined_files')
@flask_cors.cross_origin(origin="*", supports_credentials=True)
@token_required
def find_undefined_files(current_user):
    undefined_files = get_undefined_files()
    return jsonify(undefined_files)

# @database_bp.route('/get_undefined_files/<int:offset>/<int:limit>')
# def find_undefined_files(offset, limit):
#     undefined_files = get_undefined_files(offset, limit)
#     return jsonify(undefined_files)

@database_bp.route('/getfile', methods=['GET'])
def get_file():
    filename = request.args.get('filename')
    filepath = request.args.get('filepath')
    return send_file(filepath, as_attachment=True, download_name=filename)

@database_bp.route('/upload_files', methods=['POST'])
def upload_files():
        data = request.json
        print(data)
        # for file_data in data:
        #     fuuid = file_data['fuuid']
        #     filepath = file_data['filepath']
        #     fileType = file_data['fileType']
        #     print(f"fuuid: {fuuid}, Path: {filepath}, Type: {fileType}")
        print('requesting')
        payload = {'zipname':'', 'mode':'automatioon','data':data}
        response = requests.post('http://ingestion_files:5015/unidentifiedfiles', json=payload)
        print(response.text)
        return 'Files uploaded successfully', 200
 