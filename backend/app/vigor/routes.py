from pymongo import MongoClient
# import jsonify
from collections import Counter
from flask import Flask, request, jsonify
from app.vigor import vigor_bp
import pandas as pd
import re
from datetime import datetime
from app.vigor.lib.models_v import *
from app.auth.routes import token_required
import flask_cors
from MongoClinet import VIGOR,CDAT
import flask
mongovigor = VIGOR()
mongocdat = CDAT()

cors_allowed_ip = "*"


@vigor_bp.route("/findcalls", methods=['POST'])
def findcalls():
    print(request.form)
    data = request.get_json('number')
    print(data)
    response = cdrcalls(str(data['number']),data['fromdate'])
    return response
    


@vigor_bp.route('/vigor', methods=['GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def process_without_phone(current_user):
    output = {}
    pipeline = [{"$group": {"_id": "$filename", "count": {"$sum": 1} }}]
    result = list(mongovigor.cri_meta.aggregate(pipeline))
    field_list = [item['_id'] for item in result]
    Enc_files = field_list
    # print(Enc_files)
    output['Enc_Files'] = len(field_list)

    pipeline = [
    {"$group": {
        "_id": "$filename",
        "count": {"$sum": 1},
        "filenames": {"$addToSet": "$filename"} 
    }}]

    result = list(col4.aggregate(pipeline))
    field_list = [item['_id'] for item in result]

    unique_filenames_set = set()   
    for item in result:
        unique_filenames_set.update(item['filenames'])
    Speakers = unique_filenames_set
    # print(Speakers)
    output['speakers'] = len(unique_filenames_set)
    pipeline = [
    {"$match": {"status": "Processed"}},  
    {"$group": {
        "_id": "$status", 
        "count": {"$sum": 1},
        "filenames": {"$push": "$filename"} 
    }}]
    result = list(col2.aggregate(pipeline))
    unique_filenames = set(result[0]['filenames']) if result else set()
    output['predicted_files'] = len(unique_filenames)
    # predicted_files =  set(result[0]['filenames'])
    # print(predicted_files)
    return jsonify(output)



# # @app.route('/vigor/<phone>', methods=['GET'])
# # def process_with_phone(phone):
# #     output = {}
# #     data = {"Target_no": phone}
# #     meta = col1.find(data)
# #     field_name = "Enc_file"
# #     filtered_docs = list(map(lambda doc: doc[field_name], filter(lambda doc: field_name in doc, meta)))
# #     results_list = []

# #     for i in filtered_docs:
# #         data = {"filename": i}
# #         dat1 = col2.find(data)
# #         results_list.extend(list(dat1))

# #     names = []
# #     priority = []

# #     for document in results_list:
# #         confidence = float(document.get("confidence", 0))
# #         report = document.get("report", [])
        
# #         for speaker_info in report:
# #             confidence = float(speaker_info.get("confidence", 0))

# #             if confidence >= 0.75:
# #                 filename = document.get("filename", "N/A")
# #                 priority.append(filename)
# #                 speaker_name = speaker_info.get("speaker_name", "N/A")
# #                 names.append(speaker_name)

# #     output['Enc Files'] = len(filtered_docs)
# #     output['High Priority'] = len(priority)
# #     # output['low_priority_files_count'] = len(results_list) - len(priority)    
# #     output['Speaker_counts'] = {name: count for name, count in Counter(names).items()}

# #     return jsonify(output)



# @vigor_bp.route('/numberserach', methods=['GET', 'POST'])
# def show_table():
#     if request.method == 'POST':
#         print(request.form,"===============================fffffffffffffs=============")
#         no = request.form.get('number')
#         # no = '7702003961'
#         l, kla = [], []

#         # Perform aggregation pipeline for c1
#         pipeline_c1 = [
#             {"$match": {"TXT_REC_SRV_TARGET_NUMBER": str(no)}},
#             {"$project": {"TXT_REC_SRV_FILE_NAME": 1, "_id": 0}}
#         ]
#         documents_c1 = co1.aggregate(pipeline_c1)
        
#         for document in documents_c1:
#             kla.append(document.get("TXT_REC_SRV_FILE_NAME"))

#         # Perform aggregation pipeline for c2
#         pipeline_c2 = [
#             {"$match": {"TXT_TARGET_NUMBER": str(no)}},
#             {"$project": {
#                 "TXT_CALLED_NUMBER": 1,
#                 "TXT_IMEI_A": 1,
#                 "TXT_IMSI_A": 1,
#                 "TXT_IMEI_B": 1,
#                 "TXT_IMSI_B": 1,
#                 "TXT_LBS_LATITUDE": 1,
#                 "TXT_LBS_LONGITUDE": 1,
#                 "TXT_CELL_ID_A": 1,
#                 "_id": 0
#             }}
#         ]
#         documents_c2 = co2.aggregate(pipeline_c2)

#         for document in documents_c2:
#             l.append({
#                 "B-party": document.get("TXT_CALLED_NUMBER"),
#                 "Imei-A": document.get("TXT_IMEI_A"),
#                 "Imsi-A": document.get("TXT_IMSI_A"),
#                 "Imei-B": document.get("TXT_IMEI_B"),
#                 "Imsi-B": document.get("TXT_IMSI_B"),
#                 "Lat": document.get("TXT_LBS_LATITUDE"),
#                 "Long": document.get("TXT_LBS_LONGITUDE"),
#                 "Cellid_A": document.get("TXT_CELL_ID_A")
#             })

#         # Rest of your logic for DataFrame and rendering HTML table remains the same...
#         df = pd.DataFrame(l)
#         list_of_dicts = df.to_dict(orient='records')    
#         try:
#             speaker_name1 = [] 
#             filename1 =[]
#             # high_confidence_records = []
#             for i in kla: 
#                 for document in collection.find({"filename":str(i)}):
#                     report = document.get("report", [])
#                     for speaker_info in report:
#                         confidence = float(speaker_info.get("confidence", 0))
#                         if confidence >= 0.75:
#                             filename = document.get("filename", "N/A")
#                             speaker_name = speaker_info.get("speaker_name", "N/A")
#                             filename1.append(filename)
#                             speaker_name1.append(speaker_name)
#             for text in filename1:
#                 date = text.split('-')[4]
#                 parsed_date = datetime.strptime(date, "%Y%m%d")
#                 formatted_date = parsed_date.strftime("%d-%m-%Y")
#                 # print(formatted_date)
#             df1 = pd.DataFrame({"File":filename1,"Speaker":speaker_name1,"Date_Time":formatted_date})
#             d3 = pd.concat([df,df1],axis=1)
#             d3.fillna("",inplace=True)
#             list_of_dicts = d3.to_dict(orient='records')  
#         except: 
#             print("**********************************")
#         try:
#             l = []
#             # no = request.form['number']
#             pipeline_c1 = [
#                 {"$match": {"source_number": no}},
#                 {"$group": {"_id": None, "first_cgid": {"$push": "$first_cgid"}}}
#             ]
#             documents_c1 = c1.aggregate(pipeline_c1)
#             l.extend(documents_c1.next()["first_cgid"])
#             pipeline_c2 = [
#                 {"$match": {"cell_id": {"$in": l}}},
#                 {"$project": {"domain": 1, "country": 1, "city": 1, "company": 1, "_id": 0}}
#             ]
#             documents_c2 = c2.aggregate(pipeline_c2)
#             l1 = list(documents_c2)
#             pipeline_c3 = [
#                 {"$match": {"celltowerid": {"$in": l}}},
#                 {"$project": {"lat": 1, "long": 1, "areadescription": 1, "_id": 0}}
#             ]
#             documents_c3 = c3.aggregate(pipeline_c3)
#             l4 = list(documents_c3)
#             pipeline_c4 = [
#                 {"$match": {"first_cgid": {"$in": l}}},
#                 {"$project": {"destination_number": 1, "_id": 0}}
#             ]
#             documents_c4 = c1.aggregate(pipeline_c4)
#             l2 = [doc["destination_number"] for doc in documents_c4]
#             pipeline_c5 = [
#                 {"$match": {"TXT_CELL_ID_A": {"$in": l}}},
#                 {"$project": {"TXT_CALLED_NUMBER": 1, "_id": 0}}
#             ]
#             pattern = re.compile(r'[A-Za-z]+')
#             l2 = [s for s in l2 if not pattern.match(s)]
#             # print(filtered_list)
#             documents_c5 = c4.aggregate(pipeline_c5)
#             l2.extend(doc["TXT_CALLED_NUMBER"] for doc in documents_c5)
#             pipeline_c6 = [
#                 {"$match": {"phone": {"$exists": True}}},
#                 {"$project": {"phone": 1, "_id": 0}}
#             ]

#             documents_c6 = c6.aggregate(pipeline_c6)
#             l3 = [doc["phone"] for doc in documents_c6]

#             l_final = [item for item in l2 if item in l3]

#             df = pd.DataFrame(l1, columns=["domain", "city", "country", "company"])
#             df1 = pd.DataFrame(l4, columns=["lat", "long", "areadescription"])
#             df2 = pd.DataFrame(l2, columns=["destination_number"])
#             df3 = pd.DataFrame(l_final, columns=["l_final"])
#             df = df.reset_index(drop=True)
#             df1 = df1.reset_index(drop=True)
#             # df2 = df2.reset_index(drop=True)
#             df3 = df3.reset_index(drop=True)
#             result = pd.concat([df, df1,df3], axis=1)
#             result.rename(columns={"domain": "Domain", "city": "City","country":"Country","company":"Company","lat":"Latitude","long":"Longitude",
#                                    "areadescription":"Location","l_final":"Suspected List"},inplace=True)
#             result.fillna("",inplace=True)
#             list_of_dicts1 = result.to_dict(orient='records')

#             # print(result)
#         except:
#             print("skipping")
#         try:
#             return jsonify({'table':list_of_dicts,'table1':list_of_dicts1})
#         except: 
#             return jsonify({'table':list_of_dicts})

#     return jsonify({'table':'No data'})
