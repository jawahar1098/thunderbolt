import pymongo
import json
import datetime
from flask import Flask, jsonify
from flask_cors import CORS
# from MongoClinet import CDAT as mongocdat
from datetime import datetime
import re
from MongoClinet import CDAT
mongocdat = CDAT()
import time



class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)


class Cdr_Analysis:
    def __init__(self):
        self.collection_cdrdata = mongocdat.cdrdata
        self.collection_sdrdata = mongocdat.sdrdata
        self.collection_suspect = mongocdat.suspect
        self.collection_cellidchart = mongocdat.cellidchart
        # self.collection_ipdrs = mongocdat.ipdr
        self.collection_gprs = mongocdat.gprs
        self.collection_phone_area = mongocdat.phonearea
        self.collection_tower_data = mongocdat.towercdrdata

    def unique_counts(self):
        # SUSPECT IMEI count & Total Unique IMEI CDR’s*
        pipeline = [
            {"$group": {"_id": None, "unique_imei_numbers": {"$addToSet": "$imei"}}},
            {"$project": {"_id": 0, "unique_imei_numbers": 1}}
        ]

        unique_imei_result = list(self.collection_cdrdata.aggregate(pipeline))

        if unique_imei_result:
            unique_imei_numbers = unique_imei_result[0]['unique_imei_numbers']
            imei_count = len(unique_imei_numbers)
        else:
            imei_count = 0

        pipeline = [
            {"$group": {"_id": None, "unique_phoneprefix": {"$addToSet": "$phoneprefix"}}},
            {"$project": {"_id": 0, "unique_phoneprefix": 1}}
        ]

        unique_phone_number = list(
            self.collection_phone_area.aggregate(pipeline))

        if unique_phone_number:
            unique_phone_numbers = unique_phone_number[0]['unique_phoneprefix']
            source_count2 = len(unique_phone_numbers)
        else:
            source_count2 = 0

        document = self.collection_cellidchart.find_one({}, {'_id': 0, 'lastupdate': 1}, sort=[
                                                        ('lastupdate', pymongo.DESCENDING)]) or {"lastupdate": ""}

        timestamp_last_updated_cellid = document.get("lastupdate", "")

        # Convert timestamp to datetime for last_updated_cellid
        if timestamp_last_updated_cellid:
            dt_object_last_updated_cellid = datetime.utcfromtimestamp(
                timestamp_last_updated_cellid)
            formatted_datetime_last_updated_cellid = dt_object_last_updated_cellid.strftime(
                '%Y-%m-%d %H:%M:%S')
        else:
            formatted_datetime_last_updated_cellid = ""

        result = {
            "imei_count_cdr": imei_count,
            "last_updated_cdr": self.collection_cdrdata.find_one({}, {'_id': 0, 'as_on_date': 1}, sort=[('as_on_date', pymongo.DESCENDING)]) or {"as_on_date": ""},
            "last_updated_suspect": self.collection_suspect.find_one({}, {'_id': 0, 'as_on_datetime': 1}, sort=[('as_on_datetime', pymongo.DESCENDING)]) or {"as_on_datetime": ""},
            'last_updated_sdr': self.collection_sdrdata.aggregate([{'$addFields': {'as_on_date': {'$dateFromString': {'dateString': '$as_on_date', 'format': '%Y-%m-%d'}}}}, {'$sort': {'as_on_date': -1}}, {'$limit': 1}, {'$project': {'_id': 0, 'as_on_date': 1}}]).next()['as_on_date'] if self.collection_sdrdata.count_documents({}) > 0 else "",
            "last_updated_cellid": formatted_datetime_last_updated_cellid,
            "total_unique_source_count_phonearea": source_count2,
            'last_updated_phone_area': self.collection_phone_area.aggregate([{'$addFields': {'asondate': {'$dateFromString': {'dateString': '$asondate', 'format': '%d-%m-%Y %H:%M:%S'}}}}, {'$sort': {'asondate': -1}}, {'$limit': 1}, {'$project': {'_id': 0, 'asondate': 1}}]).next()['asondate'] if self.collection_phone_area.count_documents({}) > 0 else ""
        }

        # if 'last_updated_cellid' in result and result['last_updated_cellid'] is not None:
        #     result['last_updated_cellid']['lastupdate'] = datetime.fromtimestamp(
        #         result['last_updated_cellid']['lastupdate']).strftime("%Y-%m-%d %H:%M:%S")
        print(result, "overall")
        return result

    def state_wise_counts(self):
        # State-wise sdr Source Number
        try:
            pipeline = [
                {
                    '$addFields': {
                        'date_of_activation': {
                            '$dateFromString': {
                                'dateString': '$date_of_activation',
                                'format': '%d-%m-%Y'
                            }
                        }
                    }
                },
                {
                    '$group': {
                        '_id': '$state_key',
                        'count': {'$sum': 1},
                        'max_date_of_activation': {'$max': '$date_of_activation'}
                    }
                },
                {
                    '$project': {
                        '_id': 1,
                        'count': 1,
                        'max_date_of_activation': {
                            '$dateToString': {
                                'format': '%Y-%m-%d',
                                'date': '$max_date_of_activation'
                            }
                        }
                    }
                }
            ]

            cursor = self.collection_sdrdata.aggregate(pipeline)

            state_last_activation_dates_sdr = {}
            for doc in cursor:
                state = doc['_id']
                count = doc['count']
                max_date = doc['max_date_of_activation']
                state_last_activation_dates_sdr[state] = {
                    'count': count, 'last_updated_date': max_date}
        except Exception as e:
            state_last_activation_dates_sdr = {}
            print(f"error in sdr state wise count : {e}")

        # CDRs last updated with states
        pipeline = [
            {
                '$group': {
                    '_id': '$state',
                    'count': {'$sum': 1},
                    'latest_updated_date': {'$max': '$as_on_date'}
                }
            },
            {
                '$project': {
                    '_id': 1,
                    'count': 1,
                    'latest_updated_date': {
                        '$dateToString': {
                            'format': '%Y-%m-%d %H:%M:%S',
                            'date': '$latest_updated_date'
                        }
                    }
                }
            }
        ]
        cursor = list(self.collection_cdrdata.aggregate(pipeline))
        state_last_activation_dates_cdr = {}
        for doc in cursor:
            state = doc['_id']
            count = doc['count']
            latest_as_on_date = doc['latest_updated_date']
            state_last_activation_dates_cdr[state] = {
                'count': count, 'latest_as_on_date': latest_as_on_date}

         # State-wise cell towerid
        state_last_activation_dates_cellid = {}
        pipeline = [
            {
                '$group': {
                    '_id': '$state',
                    'count': {'$sum': 1},
                    'latest_updated_date': {'$max': {'$toDate': {'$multiply': ['$lastupdate', 1000]}}}
                    # Convert integer timestamp to date using $toDate after multiplying by 1000 to get milliseconds
                }
            },
            {
                '$project': {
                    '_id': 1,
                    'count': 1,
                    'latest_updated_date': {
                        '$dateToString': {
                            'format': '%Y-%m-%d %H:%M:%S',  # Date and time format
                            'date': '$latest_updated_date'
                        }
                    }
                }
            }
        ]

        try:
            cursor = self.collection_cellidchart.aggregate(pipeline)
            state_last_activation_dates_cellid = {}
            for doc in cursor:
                state = doc['_id']
                count = doc['count']
                last_update = doc['latest_updated_date']
                state_last_activation_dates_cellid[state] = {
                    'count': count, 'last_update': last_update}
        except Exception as e:
            print(f"error in state wise cellid : {e}")

        # Phonearea statewise
        pipeline = [
            {
                '$addFields': {
                    'asondate': {
                        '$dateFromString': {
                            'dateString': '$asondate',
                            'format': '%d-%m-%Y %H:%M:%S'
                        }
                    }
                }
            },
            {
                '$group': {
                    '_id': '$state',
                    'count': {'$sum': 1},
                    'latest_updated_date': {'$max': '$asondate'}
                }
            },
            {
                '$project': {
                    '_id': 1,
                    'count': 1,
                    'latest_updated_date': {
                        '$dateToString': {
                            'format': '%Y-%m-%d %H:%M:%S',
                            'date': '$latest_updated_date'
                        }
                    }
                }
            }
        ]

        cursor = list(self.collection_phone_area.aggregate(pipeline))
        state_last_activation_dates_phonearea = {}
        for doc in cursor:
            state = doc['_id']
            count = doc['count']
            latest_as_on_date = doc['latest_updated_date']
            state_last_activation_dates_phonearea[state] = {
                'count': count, 'latest_as_on_date': latest_as_on_date}
        # pass
        response = {
            'state_last_updated_dates_sdr': state_last_activation_dates_sdr,
            'state_last_updated_dates_cdr': state_last_activation_dates_cdr,
            'state_last_updated_dates_cellid': state_last_activation_dates_cellid,
            'state_last_updated_dates_phonearea': state_last_activation_dates_phonearea
        }
        return response

    def dashboard_map(self, mode):
        print(mode)
        print(type(mode))

    # Create a regex pattern for the state name

        tic = time.time()
        print(tic,"===================================")
        cdrData = self.collection_cdrdata.count_documents(
            {"state": {"$regex": mode, "$options": "i"}})
        req_toc = time.time() - tic

        print(req_toc,"count of cellid ===================================================")

        tic = time.time()
        sdrData = self.collection_sdrdata.count_documents(
            {"state": {"$regex": mode, "$options": "i"}})
        req_toc = time.time() - tic
        # print(req_toc,"count of sdr")

        
        tic = time.time()
        phoneArea = self.collection_phone_area.count_documents(
            {"new_state": mode})
        req_toc = time.time() - tic
        # print(req_toc,"count of phonearea")

        
        tic = time.time()
        suspect = self.collection_suspect.count_documents(
            {"state": {"$regex": mode, "$options": "i"}})
        req_toc = time.time() - tic
        # print(req_toc,"count of suspect")

        
        # tic = time.time()
        # towerData = self.collection_tower_data.count_documents(
        #     {"state": {"$regex": mode, "$options": "i"}})
        # req_toc = time.time() - tic
        # print(req_toc,"count of towerdata")

        
        tic = time.time()
        cellidChart = self.collection_cellidchart.count_documents(
            {"new_state": mode})
        # print(cellidChart)
        req_toc = time.time() - tic
        # print(req_toc,"count of cellid")

        tic = time.time()
        pipeline = [
            {
                "$match": {
                    "new_state": mode,
                    "lastupdate": {"$exists": True}  
                }
            },
            {
                "$addFields": {
                    "lastupdateDate": {"$toDate": {"$multiply": ["$lastupdate", 1000]}}  
                }
            },
            {
                "$sort": {"lastupdate": -1}
            },
            {
                "$limit": 1 
            },
            {
                "$project": {
                    "_id": 0,
                    "formatted_lastupdate": {
                        "$dateToString": {
                            "format": "%Y-%m-%d %H:%M:%S",  
                            "date": "$lastupdateDate"  
                        }
                    }
                }
            }
        ]

        document = list(self.collection_cellidchart.aggregate(pipeline))
        formatted_datetime_last_updated_cellid = document[0]["formatted_lastupdate"] if document else "" 
        req_toc = time.time() - tic
        # print(req_toc,"lastupdated time for cellid")

        result = [{
            "cdrData": cdrData,
            "SDR Data": sdrData,
            "Phone Area": phoneArea,
            "Suspect": suspect,
            # "Tower Data": towerData,
            "cellId Chart": cellidChart,
            "last_updated_cdr": self.collection_cdrdata.find_one({"state": {"$regex": mode, "$options": "i"}}, {'_id': 0, 'as_on_date': 1}, sort=[('as_on_date', pymongo.DESCENDING)]) or {"as_on_date": ""},
            "last_updated_suspect": self.collection_suspect.find_one({"state": {"$regex": mode, "$options": "i"}}, {'_id': 0, 'as_on_datetime': 1}, sort=[('as_on_datetime', pymongo.DESCENDING)]) or {"as_on_datetime": ""},
            'last_updated_sdr': self.collection_sdrdata.aggregate([
                {'$match': {'state': {"$regex": mode, "$options": "i"}}},
                {'$addFields': {'as_on_date': {'$dateFromString': {
                    'dateString': '$as_on_date', 'format': '%Y-%m-%d'}}}},
                {'$sort': {'as_on_date': -1}},
                {'$limit': 1},
                {'$project': {'_id': 0, 'as_on_date': 1}}
            ]).next()['as_on_date'] if self.collection_sdrdata.count_documents({'state': {"$regex": mode, "$options": "i"}}) > 0 else "",
            "last_updated_cellid": formatted_datetime_last_updated_cellid,
            'last_updated_phone_area': self.collection_phone_area.aggregate([
                {'$match': {'state': mode}},
                {'$addFields': {'asondate': {'$dateFromString': {
                    'dateString': '$asondate', 'format': '%d-%m-%Y %H:%M:%S'}}}},
                {'$sort': {'asondate': -1}},
                {'$limit': 1},
                {'$project': {'_id': 0, 'asondate': 1}}
            ]).next()['asondate'] if self.collection_phone_area.count_documents({"state": mode}) > 0 else "",
        }]
        print("---response dashnor--")
        return result

    def pieChart(self):
        tic = time.time()
        result = {'cdat_cdr': self.collection_cdrdata.count_documents({}),
                  'cdat_suspect': self.collection_suspect.count_documents({}),
                  'cdat_cellidchart_sample': self.collection_cellidchart.count_documents({}),
                  'cdat_phonearea': self.collection_phone_area.count_documents({}),
                  'cdat_towerdata': self.collection_tower_data.count_documents({})
                  }
        print(result, "result")
        return result
    
    def cdrcounts(self):
        # print("?"*200)
        cdr_count = self.collection_cdrdata.count_documents({})
        sdr_count = self.collection_sdrdata.count_documents({})
        suspect_count = self.collection_suspect.count_documents({})
        cellidchart_count = self.collection_cellidchart.count_documents({})
        gprs_count = self.collection_gprs.count_documents({})
        phonearea_count = self.collection_phone_area.count_documents({})
        towerdata_count = self.collection_tower_data.count_documents({})

        result = {
            "cdrdata_count": cdr_count,
            "sdrdata_count": sdr_count,
            "suspect_count": suspect_count,
            "cellidchart_count": cellidchart_count,
            "gprs_count": gprs_count,
            "phonearea_count": phonearea_count,
            "towerdata_count": towerdata_count,
        }
        print(result, "result")
        return result