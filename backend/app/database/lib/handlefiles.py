import os
import re
import json
from glob import glob
import pyzipper
from MongoClinet import Database
from MongoClinet import CDAT
from MongoClinet import thunderbolt
import datetime
from datetime import datetime as datetimee
from datetime import datetime, timedelta
from datetime import timedelta
from loguru import logger
import zipfile
import pymongo
import hashlib
from math import ceil
from flask import request
# from pymongo import MongoClient
# client = MongoClient('mongodb://localhost:27017/')
# mongocdat = client['CDAT']
# caffiles = mongocdat['caf_data']

mongodata = Database()
mongocdat = CDAT()
mongothunder = thunderbolt()

def calculate_file_hash(file_path, hash_algorithm='sha256'):
        hasher = hashlib.new(hash_algorithm)
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(65536)  # Read the file in 64KB chunks
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()


def unzip_files(path):
    print(path, "=============+++++++++++++=======================filenamemra")
    # get_files = glob(path, recursive=True)

    zipname = path.split("/")[-1]
    zipname = zipname.replace(".zip", "")
    extract_dir = f'{os.getcwd()}/app/database/parse_files/{zipname}'
    # extract_dir = f'/home/vasanth_rvs/Documents/Ingestion_files_testing/parse_files/{zipname}'
    # /home/vasanth_rvs/Vjw/Ingestion_files
    password = "sibap_conf"
    # print(path, extract_dir, password, zipname)
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)
    try:
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
    except Exception as e:
        print("An error occurred:", e)
        # shutil.move(zip_file,'/home/vasanth_rvs/Vjw/parse_files/')
    # print(extract_dir, "=====================")
    with open(f'{extract_dir}/metadata.json', 'r') as jsonfile:
        data = json.load(jsonfile)
        updata = []
        if len(data) > 0:
            for _d in data:
                _d['zipfilename'] = zipname
                _d['extract_location'] = extract_dir
                updata.append(_d)
            mongodata.filemanage.insert_many(updata)

    with open(f'{extract_dir}/maildata.json', 'r') as jsonfile:
        data = json.load(jsonfile)
        if len(data) > 0:
            mongodata.emailmanage.insert_many(data)

    return extract_dir


# def redy_to_parse_zipfiles(extract_dir):
#     mode = 'automation'
#     get_files = mongodata.filemanage.find({'database_stat': 'pending'})

#     for _f in get_files:
#         try:
#             if _f['filetype'] in ['cdr', 'imeicdr', 'towercdr']:
#                 file = f'{extract_dir}/{_f["filename"]}'
#                 cdrparser(file, _f['fuuid'], mode, _f['filetype'])

#             if _f['filetype'] == 'ipdr':
#                 file = f'{extract_dir}/{_f["filename"]}'
#                 IPDR_Parser(file, _f['fuuid'], mode)

             
#             if _f['filetype'] == 'caf':
#                 file = f'{extract_dir}/{_f["filename"]}'
#                 cafparser('english').parse(file,_f['fuuid'])
#             if _f['filetype'] == 'RH':
#                 file = f'{extract_dir}/{_f["filename"]}'
#                 rhparser(file,_f['fuuid'],mode)
#             if _f['filetype'] == 'POA':
#                 file = f'{extract_dir}/{_f["filename"]}'
#                 poaparser(file,_f['fuuid'],mode)
#         except Exception as e:
#             logger.info(e)
    # updatetickets_cdr()
    # updatetickets_imei()
    # update_towercdr()

    # get_ipdr = list(mongocli.filemanage.find({'database_stat':'pending','filetype':'ipdr'}))


def direct_files(path, filetype, fuuid, username,mode,ext_path,casename=False):
    # print(filetype, ",+++++++++++++++++++++++++++++++++")
    # status = 'somthing went wrong'
    mode = mode#'manual'
    filehash = calculate_file_hash(path)
    
    query = {'filename': path.split("/")[-1], 'file_location': path, 'filetype': filetype, 'provider': "", 'parsing_status': 'not_parsed','extract_location':ext_path,
                'inserted_doc': '','casename':casename,'user':username, 'duplicates': '', 'total_doc': '', 'file_hash': filehash, 'fuuid': fuuid, 'mode': mode,'database_stat':'pending'}
    mongodata.filemanage.insert_one(query)

    # try:
    #     if filetype in ['cdr', 'imeicdr', 'towercdr']:
    #         print("00)))))))))))))))))))))))))))))))))))))))))))))))))))))))")
    #         status = cdrparser(path, fuuid, mode, filetype)

    #         print(status, "0473888888888888888880")
    #     if filetype == 'ipdr':
    #         status = IPDR_Parser(path, fuuid, mode)
    #     if filetype == 'caf':
    #         status = cafparser('english').parse(path, fuuid)
    #     if filetype == 'rh':
    #         status = rhparser(path, fuuid, mode)
    #     if filetype == 'poa':
    #         status = poaparser(path, fuuid, mode)
    #     if filetype == 'gprs':
    #         print("gprs")
    #         status = gprsparser(path, fuuid, mode)

    # except Exception as e:
    #     logger.info(str(e))
    #     print(str(e), "----in error except------")

    # if filetype == 'cdr':
    #     cdrparser(path, fuuid, mode )

    # if filetype == 'towercdr':
    #     towercdrparser(path,fuuid,mode)

    # if filetype == 'imeicdr':
    #     imeicdrparser(path,fuuid,mode)

    # if filetype == 'ipdr':
    #     IPDR_Parser(path)
    return None




def get_start_of_week():
    today = datetime.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    print(start_of_week, "------------")
    return start_of_week


def get_start_of_month():
    today = datetime.today()
    
    start_of_month = datetime.date(today.year, today.month, 1)
    print(start_of_month)
    return start_of_month


def get_day_files():
    today = datetime.today()
    gt_files = list(mongodata.filemanage.find({
        'parsing_time': {
            '$gte': datetime.datetime.combine(get_start_of_month(), datetime.time.min),
            '$lte': datetime.datetime.combine(today, datetime.time.max)}, 'mode': 'automation'}, {'_id': 0}))
    # print(gt_files)

    return gt_files


def get_manual_files():
    today = datetime.today()

    gt_files = list(mongodata.filemanage.find({
        'parsing_time': {
            '$gte': datetime.datetime.combine(get_start_of_month(), datetime.time.min),
            '$lte': datetime.datetime.combine(today, datetime.time.max)}, 'mode': 'manual'
    }, {'_id': 0}))
    # print(gt_files)

    return gt_files


def retrieve_data(mode, start_date, end_date, currentpage=False, items=False, type_data=False):
    print("entered into retrieve_data", mode,
          start_date, end_date, currentpage, items)
    total_parsed_pages = 0
    total_not_parsed_pages = 0
    total_already_pages = 0
    total_nil_pages = 0
    total_pages = 0  # Initialize total_pages variable

    if items is False:
        items_per_page = False
        current_page = False
    else:
        items_per_page = int(items)
        current_page = int(currentpage)

    # print(items_per_page, current_page, "Page View")
    print(start_date, end_date, "------------")

    if start_date and end_date:
        parsing_time = {"$gte": start_date, "$lte": end_date}
    elif start_date:
        parsing_time = {"$gte": start_date}
    else:
        # If no date range is specified, assume the current month
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_month = today.replace(day=1)
        parsing_time = {"$gte": start_of_month,
                        "$lt": today + timedelta(days=1)}
        parsing_time = {'$exists': True}

    projection = {'_id': 0}

    if items_per_page is False and current_page is False:
        query = {'parsing_time': parsing_time, 'mode': mode}

        parsed_cursor = mongodata.filemanage.find(
            {'parsing_status': 'parsed', **query}, projection).sort('parsing_time', pymongo.DESCENDING)
        not_parsed_cursor = mongodata.filemanage.find(
            {'parsing_status': 'not_parsed', **query}, projection).sort('parsing_time', pymongo.DESCENDING)
        already_exists_cursor = mongodata.filemanage.find(
            {'parsing_status': 'already_exists', **query}, projection).sort('parsing_time', pymongo.DESCENDING)
        nil_data_cursor = mongodata.filemanage.find(
            {'NIL_DATA': 'parsed', **query}, projection)

        parsed = list(parsed_cursor)
        not_parsed = list(not_parsed_cursor)
        already_exists = list(already_exists_cursor)
        nil_data = list(nil_data_cursor)

        result = {
            'parsed': {
                'data': parsed,
                'total_pages': total_parsed_pages
            },
            'not_parsed': {
                'data': not_parsed,
                'total_pages': total_not_parsed_pages
            },
            'already_exists': {
                'data': already_exists,
                'total_pages': total_already_pages
            },
            'nil_data': {
                'data': nil_data,
                'total_pages': total_nil_pages
            },
            'total_pages': total_pages  # Include total_pages in the result
        }
        print(result, "Dataaaaaaaaa")

    else:
        query = {'parsing_time': parsing_time, 'mode': mode}

        # Count the total number of documents for pagination
        total_parsed_count = mongodata.filemanage.count_documents(
            {'parsing_status': 'parsed', **query})
        total_already_count = mongodata.filemanage.count_documents(
            {'parsing_status': 'already_exists', **query})
        total_not_parsed_count = mongodata.filemanage.count_documents(
            {'parsing_status': 'not_parsed', **query})
        total_nil_count = mongodata.filemanage.count_documents(
            {'NIL_DATA': 'parsed', **query})
        parsed_cursor = []
        not_parsed_cursor = []
        already_exists_cursor = []
        nil_data_cursor = []
        if type_data == "parsed":
            if current_page > 0:
                skip_doc = (current_page - 1) * items_per_page
            parsed_cursor = mongodata.filemanage.find({'parsing_status': 'parsed', **query}, projection).sort(
                'parsing_time', pymongo.DESCENDING).skip(skip_doc).limit(items_per_page)
        elif type_data == "not_parsed":
            if current_page > 0:
                skip_doc = (current_page - 1) * items_per_page
            not_parsed_cursor = mongodata.filemanage.find({'parsing_status': 'not_parsed', **query}, projection).sort(
                'parsing_time', pymongo.DESCENDING).skip(skip_doc).limit(items_per_page)
        elif type_data == "already_exists":
            if current_page > 0:
                skip_doc = (current_page - 1) * items_per_page
            already_exists_cursor = mongodata.filemanage.find({'parsing_status': 'already_exists', **query}, projection).sort(
                'parsing_time', pymongo.DESCENDING).skip(skip_doc).limit(items_per_page)
        elif type_data == "nil":
            if current_page > 0:
                skip_doc = (current_page - 1) * items_per_page
            nil_data_cursor = mongodata.filemanage.find({'NIL_DATA': 'parsed', **query}, projection).sort(
                'parsing_time', pymongo.DESCENDING).skip(skip_doc).limit(items_per_page)

# Convert cursors to lists, handling None
        parsed = list(parsed_cursor) if parsed_cursor is not None else []
        not_parsed = list(
            not_parsed_cursor) if not_parsed_cursor is not None else []
        already_exists = list(
            already_exists_cursor) if already_exists_cursor is not None else []
        nil_data = list(nil_data_cursor) if nil_data_cursor is not None else []

        # print(parsed_cursor,"")

        total_pages = total_parsed_count + total_not_parsed_count + \
            total_already_count + total_nil_count

        result = {
            'parsed': {
                'data': parsed,
                'total_pages': total_parsed_count  # Update total pages for pagination
            },
            'not_parsed': {
                'data': not_parsed,
                'total_pages': total_not_parsed_count  # Update total pages for pagination
            },
            'already_exists': {
                'data': already_exists,
                'total_pages': total_already_count  # Update total pages for pagination
            },
            'nil_data': {
                'data': nil_data,
                'total_pages': total_nil_count  # Update total pages for pagination
            },
            "total_pages": total_pages
        }

    print(result)
    return result


def get_total_count(conditions):
    pipeline = [
        {"$match": {"$and": conditions}},
        {"$group": {"_id": None, "totalCount": {"$sum": "$count"}}}
    ]
    result = list(mongodata.emailmanage.aggregate(pipeline))
    if result:
        return result[0]['totalCount']
    else:
        return 0


def mail_stat():
    data = mongodata.emailmanage.find()
    request_types = set()
    providers = set()
    teams = set()

    for res in data:
        request_types.add(res['request_type'])
        providers.add(res['Provider_name'])
        teams.add(res['team'])

    request_types = list(request_types)
    providers = list(providers)
    teams = list(teams)
    # print(teams, providers, request_types)
    res = []
    for team in teams:
        for request_type in request_types:
            for provider in providers:
                conditions = [
                    {"team": team},
                    {"Provider_name": provider},
                    {"request_type": request_type}
                ]
                res_dict = {}

                total_count = get_total_count(conditions)
                res_dict['team'] = team
                res_dict['provider'] = provider
                res_dict['req_type'] = request_type
                res_dict['count'] = total_count
                res.append(res_dict)
    return res


def updatetickets_cdr():
    print("updated cdr")
    coll = mongocdat.cdrdata

    coll2 = mongothunder.tickets

    ticket_collection = coll2.find()

    for ticket in ticket_collection:
        newno = ticket.get('newnumber', [])
        result = ticket.get('result', [])
        ostatus=ticket.get('pending',[])
        reqtype= ticket.get('requesttype')
        if reqtype=='CDR' and ostatus == "Mail Under Process":
            successful_updates = 0
            
            if len(result) < 1:
                try:
                    for i in range(len(newno)):
                        result[i]['status']="Data Not Received"
                except:
                    continue
                
            else:    
                for i in range(len(result)):
                    try:
                        if 'status' not  in result[i] or result[i]['status'] == 'Data Not Received':
                            msisdn = result[i].get('MSISDN')
                            fdate = result[i].get('From_Date')
                            tdate = result[i].get('To_Date')
                            print(msisdn,fdate,tdate, ticket.get('token'),"====================================================")

                            if msisdn and fdate and tdate:
                                fromdate = datetime.strptime(fdate, "%d/%m/%Y")
                                todate = datetime.strptime(tdate, "%d/%m/%Y")

                                print(f"Querying MSISDN: {msisdn}, Date Range: {fromdate} to {todate}")


                                if coll.count_documents({
                                    'source_number': msisdn,
                                    'date_format': {
                                        '$gte': fromdate,
                                        '$lte': todate
                                    }
                                }) > 0:
                                    result[i]['status'] = 'Data_Received'
                                    newno[i]['status'] = 'Data_Received'
                                    successful_updates += 1

                                    print('---------------Found data--------------------------------------------------------------------')
                                else:
                                    result[i]['status'] = 'Data Not Received'
                                    newno[i]['status'] = 'Data Not Received'
                        else:
                            result[i]['status'] = 'Data Not Received'
                            newno[i]['status'] = 'Data Not Received'
                    except Exception as e:
                        
                        print(e,'/////////')

                print(f"Only {successful_updates}/{len(result)} documents updated for ticket {ticket['_id']}")
                coll2.update_one(
                    {'_id': ticket['_id']},
                    {'$set': {'result': result, 'newnumber': newno,'status_count':str(successful_updates)}}
                )
                if successful_updates == len(result):
                    coll2.update_one({'_id': ticket['_id']},
                    {'$set': {'pending':'Ticket_Closed','status_count':str(successful_updates)}})
        else:
            print("Ticket not in 'Mail Under Process' status.")


    return None


def updatetickets_imei():
    print("updated imei")
    coll2 = mongothunder.tickets
    coll = mongocdat.imeicdrdata
    ticket_collection = coll2.find({'pending':"Mail Under Process",'requesttype':"IMEI CDR"})

    for ticket in ticket_collection:
        newno = ticket.get('newnumber', [])
        reqtype = ticket.get('requesttype', [])
        ostatus=ticket.get('pending',[])
        if ostatus == "Mail Under Process" and reqtype == "IMEI CDR":
            successful_updates = 0  
            for i in range(len(newno)):
                imei = newno[i].get('IMEI')
                if type(imei)== str:
                    fdate = newno[i].get('From_Date')
                    tdate = newno[i].get('To_Date')
                    if imei and fdate and tdate:
                        try:
                            fromdate = datetime.strptime(fdate, "%d/%m/%Y")
                            todate = datetime.strptime(tdate, "%d/%m/%Y")

                            if coll.count_documents({
                                'imei':imei,
                                'date_format': {
                                    '$gte': fromdate,
                                    '$lte': todate
                                }
                            }) > 0:
                                newno[i]['status'] = 'Data_Received'
                                successful_updates += 1

                                
                                print('---------------------------------Data found--------------------------------------------------')
                            else:
                                newno[i]['status'] = 'Data Not Received'
                        except:
                            continue
    
            print(f"Only {successful_updates}/{len(newno)} documents updated for ticket {ticket['_id']}")
            coll2.update_one(
                {'_id': ticket['_id']},
                {'$set': {'newnumber': newno,'status_count':str(successful_updates)}}
            )
            if successful_updates == len(newno):
                coll2.update_one({'_id': ticket['_id']},
                {'$set': {'pending':'Ticket_Closed','status_count':str(successful_updates)}})
                
        else:
            print("Ticket not in 'Mail Under Process' status.")
    return None


def update_towercdr():
    print("updated tower inside")

    coll = mongocdat.towercdrdata
    coll2 = mongothunder.tickets
    ticket_collection = coll2.find()

    for ticket in ticket_collection:
        newno = ticket.get('newnumber', [])
        reqtype = ticket.get('requesttype', [])
        ostatus = ticket.get('pending', [])
        if ostatus == "Mail Under Process" and (reqtype == "TOWER CDR" or reqtype == "TOWER GPRS" or reqtype == "TOWER IPDR"):
            # print(ticket)
            successful_updates = 0
            for i in range(len(newno)):
                # print(i)
                cgi = newno[i].get('CGI')
                fdate = newno[i].get('From_Date')
                tdate = newno[i].get('To_Date')
                fdate = fdate.replace("/", "-")
                tdate = tdate.replace("/", "-")
                if cgi and fdate and tdate:
                    fromdate = datetime.strptime(fdate, "%d-%m-%Y")
                    todate = datetime.strptime(tdate, "%d-%m-%Y")

                    logger.info(
                        f"Querying CGI: {cgi}, Date Range: {fromdate} to {todate}")

                    # print(f"Number of documents retrieved: {cdat_documents.count()}")

                    if coll.count_documents({
                        'first_cgid': cgi,
                        'date_format': {
                            '$gte': fromdate,
                            '$lte': todate
                        }
                    }) > 0:
                        newno[i]['status'] = 'Data_Received'
                        successful_updates += 1

                        
                    else:
                        newno[i]['status'] = 'Data Not Received'

            logger.info(
                f"Only {successful_updates}/{len(newno)} documents updated for ticket {ticket['_id']}")
            coll2.update_one(
                {'_id': ticket['_id']},
                {'$set': {'newnumber': newno,
                          'status_count': str(successful_updates)}}
            )
            if successful_updates == len(newno):
                coll2.update_one({'_id': ticket['_id']},
                                 {'$set': { 'pending': 'Ticket_Closed', 'status_count': str(successful_updates)}})
        else:
            logger.info("Ticket not in 'Mail Under Process' status.")

    return None


def profile_img(number):
    print(number)
    data = mongocdat.caffiles.find_one(
        {'phone': number}, {'_id': 0, 'img_path': 1})
    name = mongocdat.sdrdata.find_one(
        {'source_number': number}, {'_id': 0, 'fullname': 1})
    response = {}
    if data:
        img_path = data['img_path'][0]
        response = {'img_path': img_path, 'status': 'success',
                    'message': 'path retrived successfully'}
    else:
        response = {'img_path': [], 'status': 'failure',
                    'message': 'no image found'}
    if name:
        response['name'] = name['fullname']
        response['imgstatus'] = 'success'
    return response


# number = "9546835260"
# profile_img(number)


def ingestion_stat():
    
    zipfilenames = mongodata.filemanage.distinct('zipfilename',{'database_stat':'pending'})
    outlist = []
    for _zip in zipfilenames:
        out = {}
        out['filename'] = _zip
        out['filecounts'] = mongodata.filemanage.count_documents({'zipfilename':_zip})
        out['pendingcounts'] =  out['filecounts'] - mongodata.filemanage.count_documents({'database_stat':'pending','zipfilename':_zip}) 
        out['showprogress'] = 'true'
        outlist.append(out)
    
    return outlist


def get_undefined_files(offset=0, limit=50):
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    skip = (page - 1) * limit

    undefined_files_query = [
        {"$match": {"filetype": "undefined"}},
        {"$project": {"filename": 1, "_id": 0, "server_path": 1, "extract_location": 1,"fuuid":1}},
        {"$skip": skip},
        {"$limit": limit}
    ]

    undefined_files = list(mongodata.filemanage.aggregate(undefined_files_query))
    result = []
    for doc in undefined_files:
        extract_location = doc.get('extract_location', '')
        server_path = doc.get('server_path', '')
        filename = doc.get('filename', '')
        fuuid = doc.get('fuuid','')
        email_received_index = server_path.find("Email_Received")
        if email_received_index != -1:
            final_path = extract_location + server_path[email_received_index + len("Email_Received"):] 
            if not final_path.endswith('.csv'):
                final_path += filename
            doc['final_path'] = final_path
            file_names = {"file_path": doc['final_path'], "filename": filename,"fuuid":fuuid }
            result.append(file_names)
    print(f"fetchiung for {page},limit si {limit}, skipoing i s {skip}")
    print("lenght of records is ",len(result))
    return result

