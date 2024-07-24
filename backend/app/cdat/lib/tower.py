from pymongo import MongoClient
import re
from loguru import logger
from datetime import datetime, timedelta
import time
from bson.json_util import dumps
from datetime import datetime
import time,re
from math import sin, cos, sqrt, atan2, radians
import pymongo
from pprint import pprint
from flask import jsonify, request
from MongoClinet import CDAT 
from MongoClinet import CDAT as mongocdat
mongocdat = CDAT()

class Tower_View():
    def __init__(self):
        self.mongocdat = mongocdat().db 
        self.collection = mongocdat.towercdrdata
        self.cdr_collection = mongocdat.cdrdata
        self.collection_cellidchart = mongocdat.cellidchart
        self.collection_indcase = mongocdat.indcase
        self.collection_ipdr = mongocdat.ipdr
        self.collection_mapdata = self.db['mapdata']

    
    def get_tower_in_polygon(self,coords):
        try:  
            print('coordinate:', coords)
            for coord in coords:
                print(coord,"-------------------")
            start_time = time.time()
            polygon_coords = [{'longitude': float(coord['longitude']), 'latitude': float(coord['latitude'])} for coord in coords]
            print(polygon_coords)
            coords_time = time.time()
            towers_in_polygon = list(self.collection_cellidchart.find({
                'location': {
                    '$geoWithin': {
                        '$geometry': {
                            'type': 'Polygon',
                            'coordinates': [[
                                [coord['longitude'], coord['latitude']] for coord in polygon_coords
                            ]]
                        }
                    }
                }
            },{'_id':0}))
            mongo_time = time.time()

            cdr_in_towers = []
            for tower in towers_in_polygon:
                # tower_key = tower['tower_key']
                tower_id = tower['celltowerid']

                cdr_records = self.cdr_collection.find({'first_cgid': tower_id})
                for cdr_record in cdr_records:
                    cdr_data = {
                        'tower_location': tower['location'],
                        'cdr_data': {
                            'source_number': cdr_record['source_number'],
                            'call_type': cdr_record['call_type'],
                            'timestamp': cdr_record['timestamp'],
                            'destination_number': cdr_record['destination_number'],
                            'first_cgid': cdr_record['first_cgid']
                        }
                    }
                    cdr_in_towers.append(cdr_data)
            loop_time = time.time()
            result = {
                'towers_in_polygon': towers_in_polygon,
                'cdr_in_towers': cdr_in_towers
            }
            result_time=time.time()
            # print(result)
            print(f'Function Execution Time: {result_time - start_time} seconds')
            print(f'Coordinates Processing Time: {coords_time - start_time} seconds')
            print(f'MongoDB Query Time: {mongo_time - coords_time} seconds')
            print(f'Loop Processing Time: {loop_time - mongo_time} seconds')
            print(f'Result Processing Time: {result_time - loop_time} seconds')
            return result

        except Exception as e:
            print('Error:', e)
            # return jsonify({'error': str(e)})
        

    def casedata(self):
        getdistinctcase = self.collection_indcase.distinct('casename')
        result = {}
        for i in getdistinctcase:
            if i not in result:
                result[i] = {}
            result[i]['casename'] = i
            for x in self.collection_indcase.find({'casename': i}).limit(1):
                result[i]['casetype'] = x['casetype'] 
            result[i]['totalDoc'] = self.collection_indcase.count_documents({'casename':i})
            result[i]['totalFiles'] = len(self.collection_indcase.distinct('file_hash',{'casename':i}))
            for x in self.collection_indcase.find({'casename': i}).sort('as_on_date',pymongo.DESCENDING).limit(1):
                result[i]['updatetime'] = x['as_on_date'].strftime("%d-%m-%Y %H:%M:%S")
        # print(result)
        output = list(result.values())
        return output
    
    def get_tower(self,coords):
        try:
            
                
            print('coordinate:', coords)
            for coord in coords:
                print(coord,"-------------------")
            polygon_coords = [{'longitude': float(coord['longitude']), 'latitude': float(coord['latitude'])} for coord in coords]
            print(polygon_coords)
            towers_in_polygon = list(self.collection_cellidchart.find({
                'location': {
                    '$geoWithin': {
                        '$geometry': {
                            'type': 'Polygon',
                            'coordinates': [[
                                [coord['longitude'], coord['latitude']] for coord in polygon_coords
                            ]]
                        }
                    }
                }
            },{'_id':0}))
        except Exception as e:
            pass

        return towers_in_polygon
    
    def imeisummary(self,casename,casetype):
    
    
        pipeline = [
            {
                '$match':{
                    'casename':casename,
                    'casetype':casetype
                }
            },
            {
            '$addFields': {
                'timestamp_in_milliseconds': {'$multiply': ['$timestamp', 1000]}  
                }
            },
            {
                '$group':{
                    '_id':{
                        'imei':'$imei',
                        'source_number':'$source_number'
                    },
                    'first_call': {'$min': {'$toDate': '$timestamp_in_milliseconds'}},
                    'last_call': {'$max': {'$toDate': '$timestamp_in_milliseconds'}},  
                    'doc_count': {'$sum': 1}     
                }
            },
            {
                '$project':{
                    '_id':0,
                    'imei': '$_id.imei',
                    'source_number': '$_id.source_number',
                    'first_call': {
                    '$dateToString': {
                        'format': '%Y-%m-%d %H:%M:%S',  
                        'date': '$first_call'
                    }
                    },
                    'last_call': {
                        '$dateToString': {
                            'format': '%Y-%m-%d %H:%M:%S',  
                            'date': '$last_call'
                        }
                    },
                        'total_rows': '$doc_count'
                    },
            },
                    {
                        '$sort':{
                            'imei':1
                        }
                    }   
        ]
        result = {}
        result['casesummary'] = list(self.collection_indcase.aggregate(pipeline))
        dis_imei = self.collection_indcase.distinct('imei',{'casename':casename,'casetype':casetype})
        ov_sum = pipeline = [
            {
                '$match':{
                    'imei':{'$in':dis_imei}

                }
            },
            {
            '$addFields': {
                'timestamp_in_milliseconds': {'$multiply': ['$timestamp',1000]}  
                }
            },
            {
                '$group':{
                    '_id':{
                        'imei':'$imei',
                        'source_number':'$source_number'
                    },
                    'first_call': {'$min': {'$toDate': '$timestamp_in_milliseconds'}},
                    'last_call': {'$max': {'$toDate': '$timestamp_in_milliseconds'}},  
                    'doc_count': {'$sum': 1}     
                }
            },
            {
                '$project':{
                    '_id':0,
                    'imei': '$_id.imei',
                    'source_number': '$_id.source_number',
                    'first_call': {
                    '$dateToString': {
                        'format': '%d-%m-%Y %H:%M:%S',  
                        'date': '$first_call'
                    }
                    },
                    'last_call': {
                        '$dateToString': {
                            'format': '%d-%m-%Y %H:%M:%S',  
                            'date': '$last_call'
                        }
                    },
                        'total_rows': '$doc_count'
                    },
            },
                    {
                        '$sort':{
                            'imei':1
                        }
                    }   
        ]

        result['overallsummary'] = list(self.collection.aggregate(ov_sum))
        pprint(result)
        return result


    def signlecase(self,casename,casetype,items_per_page,current_page):
        skip_doc = int(items_per_page) *(int(current_page))
        end_doc = skip_doc + items_per_page
        print(skip_doc,"=========",end_doc)
        # getdistinctcase = list(self.collection_indcase.find({'casename':casename,'casetype':casetype}))
        result = {}
        # for i in getdistinctcase:
        i = casename
        result['casename'] = casename
        for x in self.collection_indcase.find({'casename': i}).limit(1):
            result['casetype'] = x['casetype'] 
        result['totalDoc'] = self.collection_indcase.count_documents({'casename':i})
        result['totalFiles'] = len(self.collection_indcase.distinct('file_hash'))
        for x in self.collection_indcase.find({'casename': i}).sort('as_on_date',pymongo.DESCENDING).limit(1):
            result['updatetime'] = x['as_on_date'].strftime("%d-%m-%Y %H:%M:%S")
        unique_coords = self.collection_indcase.aggregate([
            {
                "$match": {
                    "lat": {"$exists": True},
                    "long": {"$exists": True}
                }
            },
            {
                "$group": {
                    "_id": {
                        "lat": "$lat",
                        "lon": "$long"
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "latitude": "$_id.lat",
                    "longitude": "$_id.lon"
                }
            }
        ])

        unique_coords_list = list(unique_coords)
        print(unique_coords_list)
        result['totalTowers'] = len(unique_coords_list)
        towers = {}
        for _tow in unique_coords_list:
            # print(_tow)
            _t = self.collection_cellidchart.find_one({'lat':_tow['latitude'],'long':_tow['longitude']})
            # print(_t)
            if _t is not None:
                towers['cellids'] = _t['celltowerid']
                towers['towername'] = _t['areadescription']
        
        regex_pattern = '^(?:[6-9]\\d{9}|91[6-9]\\d{10})$'
        ind_num = self.collection_indcase.distinct('source_number', {'casename': casename, 'source_number': {'$regex': regex_pattern}})        
        result['distinct_num'] = len(ind_num)
        result['count_pages'] = len(ind_num)
        result['formulaOne'] = [self.tower_profile(ind_num[int(skip_doc):int(end_doc)],casename,casetype)]
        # result['formulaOne'] = []
        # for i_num in ind_num[int(skip_doc):int(end_doc)]:
        #     print(i_num)
        #     result['formulaOne'].append(self.tower_profile(i_num,casename,casetype))
            # break


        # print(result)
        return result
    
    def case_analysis(self,data):
        casename = data['casename']
        casetype = data['casetype']
        getdata = self.collection_indcase.find({'casename':casename,'casetype':casetype})
        resutl= {}
        for _d in getdata:
            if _d['provider'] not in resutl:
                resutl[_d['provider']] = set()
            resutl[_d['provider']].add(_d['first_siteaddress'])
        print(resutl)


    
    def tower_profile(self,data,casename,casetype):
        match_conditions =   {'source_number':{'$in':data}}

        
        # match_conditions['source_number'] = data
        match_conditions['casename'] = casename
        match_conditions['casetype'] = casetype
            
        print(match_conditions)
        # print(len(list(self.collection_indcase.find(match_conditions))))
        pipeline = self.collection_indcase.aggregate([
            {
                "$match":match_conditions
            
            },
            {
                "$addFields": {
                    "isValid": {
                        "$cond": {
                            "if": {
                                "$regexMatch": {
                                    "input": "$destination_number",
                                    "regex": r"^(91\d{10}|\d{10})$"
                                }
                            },
                            "then": "valid",
                            "else": "notValid"
                        }
                    },
                    "dateObj": {
                        "$dateFromString": {
                            "dateString": "$date",
                            "format": "%d-%m-%Y"
                        }
                    }
                }
            },
            {
                "$group": {
                    "_id": "$source_number",
                    "source_number": { "$first": "$source_number" },
                    "min_date": { "$min": "$dateObj" },
                    "max_date": { "$max": "$dateObj" },
                    "no_dates_present": { "$addToSet": "$date" },
                    "no_unique_destination_numbers": { "$addToSet": "$destination_number" },
                    "imei_local": { "$addToSet": "$imei" },
                    "tower_count": { "$addToSet": "$first_siteaddress" },
                    "sector": { "$addToSet": "$first_cgid" },
                    "call_type_count": {
                        "$push": {
                            "$switch": {
                                "branches": [
                                    { "case": { "$in": ["$call_type", ["call_in", "call_out"]] }, "then": "inout" },
                                    { "case": { "$in": ["$call_type", ["sms_out", "sms_in"]] }, "then": "smosmi" }
                                ],
                                "default": "other"
                            }
                        }
                    },
                    "total_calls_count": {
                        "$push": {
                            "id": "$_id",
                            "count": 1
                        }
                    },
                    "total_in_count": {
                        "$sum": { "$cond": [{ "$in": ["$call_type", ["call_in"]] }, 1, 0] }
                    },
                    "total_out_count": {
                        "$sum": { "$cond": [{ "$in": ["$call_type", ["call_out","VOC"]] }, 1, 0] }
                    },
                    "total_smo_count": {
                        "$sum": { "$cond": [{ "$in": ["$call_type", ["sms_out"]] }, 1, 0] }
                    },
                    "total_smt_count": {
                        "$sum": { "$cond": [{ "$in": ["$call_type", ["sms_in"]] }, 1, 0] }
                    },
                    "validUniqueCount": { "$sum": { "$cond": [{ "$eq": ["$isValid", "valid"] }, 1, 0] } },
                    "notValidUniqueCount": { "$sum": { "$cond": [{ "$eq": ["$isValid", "notValid"] }, 1, 0] } }
                }
            },
            {
                "$addFields": {
                    "date_difference": {
                        "$divide": [
                            {
                                "$subtract": [
                                    { "$max": "$max_date" },
                                    { "$min": "$min_date" }
                                ]
                            },
                            86400000
                        ]
                    },
                    "dates_present": { "$size": "$no_dates_present" },
                    "other_number": { "$size": "$no_unique_destination_numbers" },
                }
            },
            {
                "$lookup": {
                    "from": "cdat_suspect",
                    "localField": "source_number",
                    "foreignField": "phone",
                    "as": "suspectData"
                },
                

            },
           
            # {
            #     "$unwind": "$suspectData"
            # },
            {
                "$lookup": {
                    "from": "cdat_cdr",
                    "localField": "source_number",
                    "foreignField": "source_number",
                    "as": "cdrData"
                }
            },
            # {
            #     "$unwind": "$cdrData"
            # },
            {
                "$addFields": {
                    "ratio": {
                        "$cond": [
                            {
                                "$and": [
                                    { "$gt": [{ "$size": { "$filter": { "input": "$call_type_count", "cond": { "$eq": ["$$this", "inout"] } } } }, 0] },
                                    { "$gt": [{ "$size": { "$filter": { "input": "$call_type_count", "cond": { "$eq": ["$$this", "smosmi"] } } } }, 0] }
                                ]
                            },
                            {
                                "$concat": [
                                    { "$toString": { "$size": { "$filter": { "input": "$call_type_count", "cond": { "$eq": ["$$this", "inout"] } } } } },
                                    ":",
                                    { "$toString": { "$size": { "$filter": { "input": "$call_type_count", "cond": { "$eq": ["$$this", "smosmi"] } } } } }
                                ]
                            },
                            "No calls"
                        ]
                    }
                }
            },
            
            {
                "$group": {
                    "_id": "$source_number",
                    "min_date": { "$first": "$min_date" },
                    "max_date": { "$first": "$max_date" },
                    "date_difference": { "$first": "$date_difference" },
                    "dates_present": { "$first": "$dates_present" },
                    "other_number": { "$first": "$other_number" },
                    "imei": { "$first": "$imei_local" },
                    "tower": { "$first": "$tower_count" },
                    "sector": { "$first": "$sector" },
                    "ratio": { "$first": "$ratio" },
                    "nickname": { "$first": "$suspectData.nickname" },
                    "imei_count_cdr": { "$addToSet": "$cdrData.imei" },
                    "total_calls_count": { "$first": "$total_calls_count" },
                    "total_in_count": { "$first": "$total_in_count" },
                    "total_out_count": { "$first": "$total_out_count" },
                    "total_smo_count": { "$first": "$total_smo_count" },
                    "total_smt_count": { "$first": "$total_smt_count" },
                    "validUniqueCount": { "$first": "$validUniqueCount" },
                    "notValidUniqueCount": { "$first": "$notValidUniqueCount" }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source_number": "$_id",
                    "nickname": 1,
                    "min_date": 1,   
                    "max_date": 1,
                    "date_difference": 1,
                    "dates_present": 1,
                    "other_number": 1,
                    "imei": 1,
                    "tower": 1,       
                    "sector": 1,
                    "imei_count_cdr": 1,
                    "total_call_count": { "$size": "$total_calls_count" },
                    "destination_counts": 1,
                    "ratio": 1,
                    'validUniqueCount': 1,
                    'notValidUniqueCount': 1,
                    "ratio_call": {
                        "$concat": [
                            { "$toString": "$total_in_count" },
                            ":",
                            { "$toString": "$total_out_count" }
                        ]
                    },
                    'ratio_sms': {
                        "$concat": [
                            { "$toString": "$total_smt_count" },
                            ":",
                            { "$toString": "$total_smo_count" }
                        ]
                    }
                }
            }
        ])

        info = list(pipeline)
        print(info, "final stage of pipeline--------")
        # for item in info:
        #     print(item)
        return info
    

    def find_sus(self,data,casename,casetype):
        match_conditions =   {'source_number':{'$in':data}}

        
        # match_conditions['source_number'] = data
        match_conditions['casename'] = casename
        match_conditions['casetype'] = casetype
            
        print(match_conditions)
        # print(len(list(self.collection_indcase.find(match_conditions))))
        pipeline = self.collection_indcase.aggregate([
            {
                "$match":match_conditions
            
            },
            {
                "$addFields": {
                    "isValid": {
                        "$cond": {
                            "if": {
                                "$regexMatch": {
                                    "input": "$destination_number",
                                    "regex": r"^(91\d{10}|\d{10})$"
                                }
                            },
                            "then": "valid",
                            "else": "notValid"
                        }
                    },
                    "dateObj": {
                        "$dateFromString": {
                            "dateString": "$date",
                            "format": "%d-%m-%Y"
                        }
                    }
                }
            },
            {
                "$group": {
                    "_id": "$source_number",
                    "call_type_count": {
                        "$push": {
                            "$switch": {
                                "branches": [
                                    { "case": { "$in": ["$call_type", ["call_in", "call_out"]] }, "then": "inout" },
                                    { "case": { "$in": ["$call_type", ["sms_out", "sms_in"]] }, "then": "smosmi" }
                                ],
                                "default": "other"
                            }
                        }
                    },
                }
            },
            
            {
                "$lookup": {
                    "from": "cdat_suspect",
                    "localField": "source_number",
                    "foreignField": "phone",
                    "as": "suspectData"
                },
            },
           
            # {
            #     "$unwind": "$suspectData"
            # },
            {
                "$lookup": {
                    "from": "cdat_cdr",
                    "localField": "source_number",
                    "foreignField": "source_number",
                    "as": "cdrData"
                }
            },
            # {
            #     "$unwind": "$cdrData"
            # },
            
            
            {
                "$group": {
                    "_id": "$source_number",
                    "nickname": { "$first": "$suspectData.nickname" },
                    "imei_count_cdr": { "$addToSet": "$cdrData.imei" }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source_number": "$_id",
                    "nickname": 1,
                    "imei_count_cdr": 1,
                }
            }
        ])

        info = list(pipeline)
        print(info, "final stage of pipeline--------")
        # for item in info:
        #     print(item)
        return info
    
    
    
    def cdr_profile(self,data):
        pipeline = self.cdr_collection.aggregate([
        {
            "$match": {
            "source_number": data,
            "call_type": { '$in': ['call_in', 'call_out', 'sms_in', 'sms_out', 'Voice_out'] },
            
            }
        },
        {
            "$addFields": {
            "isValid": {
                "$cond": {
                'if': {
                    "$regexMatch": {
                    'input': "$destination_number",
                    'regex': r'/^(91\d{10}|\d{10})$/'
                    }
                },
                'then': "valid",
                'else': "notValid"
                }
            },
            "dateObj": {
                "$dateFromString": {
                "dateString": "$date",
                "format": "%Y-%m-%d"
                }
            }
            }
        },
        {
            "$group": {
            "_id": 'null',
            "source_number": { "$first": "$source_number" },
            "min_date": { "$min": "$dateObj" },
            "max_date": { "$max": "$dateObj" },
            "no_dates_present": { "$addToSet": "$date" },
            "no_unique_destination_numbers": { "$addToSet": "$destination_number" },
            "no_unique_imei_count_local": { "$addToSet": "$imei" },
            "no_unique_sector_count": { "$addToSet": "$first_cgid" },
            "call_type_count": {
                "$push": {
                "$switch": {
                    "branches": [
                    { "case": { "$in": ["$call_type", ["call_in", "call_out"]] }, "then": "inout" },
                    { "case": { "$in": ["$call_type", ["sms_in", "sms_out"]] }, "then": "smosmi" }
                    ],
                    "default": "other"
                }
                }
            },
            "total_calls_count": {
                "$push": {
                "id": "$_id",
                "count": 1
                }
            },
            "total_in_count": {
                "$sum": { "$cond": [{ "$in": ["$call_type", ["call_in"]] }, 1, 0] }
            },
            "total_out_count": {
                "$sum": { "$cond": [{ "$in": ["$call_type", ["call_out"]] }, 1, 0] }
            },
            "total_smo_count": {
                "$sum": { "$cond": [{ "$in": ["$call_type", ["sms_in"]] }, 1, 0] }
            },
            "total_smt_count": {
                "$sum": { "$cond": [{ "$in": ["$call_type", ["sms_out"]] }, 1, 0] }
            },
            "validUniqueCount": { "$sum": { "$cond": [{ "$eq": ["$isValid", "valid"] }, 1, 0] } }, 
            "notValidUniqueCount": { "$sum": { "$cond": [{ "$eq": ["$isValid", "notValid"] }, 1, 0] } } 
            }
        },
        {
            "$addFields": {
            "date_difference": {
                "$divide": [
                {
                    "$subtract": [
                    { "$max": "$max_date" },
                    { "$min": "$min_date" }
                    ]
                },
                86400000
                ]
            },
            "dates_present": { "$size": "$no_dates_present" },
            "other_number": { "$size": "$no_unique_destination_numbers" },
            }
        },
        {
            "$lookup": {
            "from": "cdat_suspect",
            "localField": "source_number",
            "foreignField": "phone",
            "as": "suspectData"
            }
        },
        # {
        #     "$unwind": "$suspectData"
        # },
        {
            "$lookup": {
            "from": "cdat_tower",
            "localField": "source_number",
            "foreignField": "source_number",
            "as": "cdrData"
            }
        },
        # {
        #     "$unwind": "$cdrData"
        # },
        {
            "$addFields": {
            "ratio": {
                    "$cond": [
                    {
                        "$and": [
                        { "$gt": [{ "$size": { "$filter": { "input": "$call_type_count", "cond": { "$eq": ["$$this", "inout"] } } } }, 0] },
                        { "$gt": [{ "$size": { "$filter": { "input": "$call_type_count", "cond": { "$eq": ["$$this", "smosmi"] } } } }, 0] }
                        ]
                    },
                    {
                        "$concat": [
                        { "$toString": { "$size": { "$filter": { "input": "$call_type_count", "cond": { "$eq": ["$$this", "inout"] } } } } },
                        ":",
                        { "$toString": { "$size": { "$filter": { "input": "$call_type_count", "cond": { "$eq": ["$$this", "smosmi"] } } } } }
                        ]
                    },
                    "No 'CALL' or 'SMS' data available"
                    ]
                },
                }
            },
        {
            "$group": {
            "_id": "$source_number",
            "min_date": { "$first": "$min_date" },
            "max_date": { "$first": "$max_date" },
            "date_difference": { "$first": "$date_difference" },
            "dates_present": { "$first": "$dates_present" },
            "other_number": { "$first": "$other_number" },
            "imei": { "$first": "$imei" },
            "tower": { "$first": "$tower" },
            "sector": { "$first": "$sector" },
            "ratio": { "$first": "$ratio" },
            "nickname": { "$first": "$suspectData.nickname" },
            "imei_count_cdr": { "$addToSet":"$cdrData.imei"},
            "total_calls_count": { "$first": "$total_calls_count" },
            "total_in_count": { "$first": "$total_in_count" },
            "total_out_count": { "$first": "$total_out_count" },
            "total_smo_count": { "$first": "$total_smo_count" },
            "total_smt_count": { "$first": "$total_smt_count" },
            "validUniqueCount": { "$first": "$validUniqueCount" },
            "notValidUniqueCount": { "$first": "$notValidUniqueCount" } 
            }
        },
        {
            "$project": {
            "_id": 0,
            "source_number": "$_id",
            "nickname": 1,
            "min_date": 1,
            "max_date": 1,
            "date_difference": 1,
            "dates_present": 1,
            "other_number": 1,
            "imei": 1,
            "sector": 1,
            "imei_count_tower": 1,
            "total_call_count": { "$size": "$total_calls_count" },
            "destination_counts": 1,
            "ratio": 1,
            'validUniqueCount':1,
            'notValidUniqueCount':1,
                "ratio_call": {
                        "$concat": [
                        { "$toString": "$total_in_count" },
                        ":",
                        { "$toString": "$total_out_count" }
                        ]},
                    'ratio_sms': {
                        "$concat": [
                        { "$toString": "$total_smt_count" },
                        ":",
                        { "$toString": "$total_smo_count" }
                        ]}
                    }
                }
                ])
        
        pprint(list(pipeline))


    
    
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0
        lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * \
            cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return distance
    
    def common_link(self,value):
        numbers = value['numbers']
        selected_date_str= value['date'] 
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').strftime('%d-%m-%Y')
        result = {}
        result[selected_date] = {}
        for num in numbers:
            cell_data_list = []
            cell_number = self.cdr_collection.find({"source_number": num, "date": selected_date})
            for cell in cell_number:
                cell_id = cell.get('first_cgid')
                print(cell_id)
                cell_records = self.collection_cellidchart.find({'celltowerid': cell_id})
                # print(list(cell_records))
                if cell_records == " ":
                    continue
                else:
                    for cell_record in cell_records:
                        print("entered")
                        cell_data = {
                            'tower_date': cell['date'],
                            'tower_time': cell['time'],
                            'tower_duration':cell['duration'],
                            'cell_id': cell_record['celltowerid'],
                            'tower_latitude': cell_record['lat'],
                            'tower_longitude': cell_record['long'],
                            'azimuth': cell_record['azimuth'],
                            'area_description': cell_record['areadescription']
                        }
                        cell_data_list.append(cell_data)
            
            result[selected_date][num] = cell_data_list
        
        if not selected_date:
            return jsonify({"No dates are selected"})
        if selected_date:
            return jsonify(result[selected_date])

    # def matched_bparty_contact(self):
    #     pipeline = [
    #             {
    #                 '$match': {
    #                     'destination_number': {
    #                         '$regex': '^(91\\d{10}|\\d{10})$'
    #                     }
    #                 }
    #             },
    #             {
    #                 '$group': {
    #                     '_id': '$destination_number'
    #                 }
    #             },
    #             {
    #                 '$lookup': {
    #                     'from': 'ind_cases',
    #                     'let': { 'local_dest_number': '$_id' },
    #                     'pipeline': [
    #                         {
    #                             '$match': {
    #                                 '$expr': {
    #                                     '$or': [
    #                                         { '$eq': ['$destination_number', '$$local_dest_number'] },
    #                                         { '$eq': ['$source_number', '$$local_dest_number'] }
    #                                     ]
    #                                 }
    #                             }
    #                         },
    #                         {
    #                             '$addFields': {
    #                                 'timestamp_in_milliseconds': { '$multiply': ['$timestamp', 1000] }
    #                             }
    #                         },
    #                         {
    #                             '$group': {
    #                                 '_id': {
    #                                     'source_destination': {
    #                                         '$cond': {
    #                                             'if': { '$eq': ['$destination_number', '$$local_dest_number'] },
    #                                             'then': '$destination_number',
    #                                             'else': '$source_number'
    #                                         }
    #                                     }
    #                                 },
    #                                 'first_call': { '$min': { '$toDate': '$timestamp_in_milliseconds' } }, 
    #                                 'last_call': { '$min': { '$toDate': '$timestamp_in_milliseconds' } },                                'doc_count': { '$sum': 1 }
    #                             }
    #                         },
    #                         {
    #                             '$project': {
    #                                 '_id': 0,
    #                                 'number': '$_id.source_destination',
    #                                 'first_call': {
    #                                     '$dateToString': {
    #                                         'format': '%Y-%m-%d %H:%M:%S',
    #                                         'date': '$first_call'
    #                                     }
    #                                 },
    #                                 'last_call': {
    #                                     '$dateToString': {
    #                                         'format': '%Y-%m-%d %H:%M:%S',
    #                                         'date': '$last_call'
    #                                     }
    #                                 },
    #                                 'total_docs': '$doc_count'
    #                             }
    #                         }
    #                     ],
    #                     'as': 'tower_matches'
    #                 }
    #             },
    #             {
    #                 '$match': {
    #                     'tower_matches': { '$ne': [] }
    #                 }
    #             },
    #             {
    #                 '$project': {
    #                     '_id': 0,
    #                     'destination_number': '$_id',
    #                     'tower_matches': 1
    #                 }
    #             }
    #         ]


    #     result = list(self.cdr_collection.aggregate(pipeline))

    #     pprint(result)
    #     return result
        
    def matched_bparty_contact(self):
        pipeline = [
            {
                '$match': {
                    'destination_number': {
                        '$regex': '^(91\\d{10}|\\d{10})$'
                    }
                }
            },
            {
                '$group': {
                    '_id': None,
                    'unique_dest_numbers': { '$addToSet': '$destination_number' },
                    'unique_src_numbers': { '$addToSet': '$source_number' }
                }
            },
            {
                '$project': {
                    'unique_numbers': { '$setUnion': ['$unique_dest_numbers', '$unique_src_numbers'] }
                }
            },
            {
                '$unwind': '$unique_numbers'
            },
            {
                '$lookup': {
                    'from': 'cdat_cdr',
                    'localField': 'unique_numbers',
                    'foreignField': 'destination_number',
                    'as': 'matched_cdr'
                }
            },
            {
                '$match': {
                    'matched_cdr': { '$ne': [] }
                }
            },
            {
                '$lookup': {
                    'from': 'ind_cases',
                    'let': { 'num': '$unique_numbers' },
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$or': [
                                        { '$eq': ['$destination_number', '$$num'] },
                                        { '$eq': ['$source_number', '$$num'] }
                                    ]
                                }
                            }
                        }
                    ],
                    'as': 'ind_cases_matches'
                }
            },
            {
                '$unwind': '$ind_cases_matches'
            },
            {
                '$group': {
                    '_id': '$unique_numbers',
                    'min_date': { '$min': '$ind_cases_matches.timestamp' },
                    'max_date': { '$max': '$ind_cases_matches.timestamp' },
                    'count': { '$sum': 1 }
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'number': '$_id',
                    'min_date': {
                    '$dateToString': {
                        'format': '%Y-%m-%d %H:%M:%S',  
                        'date': { '$toDate': { '$multiply': ['$min_date', 1000] } }
                    }
                    },
                    'max_date': {
                        '$dateToString': {
                            'format': '%Y-%m-%d %H:%M:%S',  
                            'date': { '$toDate': { '$multiply': ['$max_date', 1000] } }
                        }
                    },
                    'count': '$count'
                }
            }
        ]

        result = list(self.collection_indcase.aggregate(pipeline))
        # pprint(result)
        return result








    
    def tower_imei(self,case_name,case_type):
        results = [] 
        
        pipeline = [
            {
            '$match': {
                    'casename': case_name,
                    'casetype': case_type
                }
            },
            {
                '$lookup': {
                    'from': 'cdat_cdr',
                    'let': { 'local_imei': '$imei' },
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$eq': [ '$imei', '$$local_imei' ]
                                }
                            }
                        }
                    ],
                    'as': 'cdr_matches'
                }
            },
            {
                '$match': {
                    'cdr_matches': { '$ne': [] }
                }
            },
            {
                '$addFields': {
                    'timestamp_in_milliseconds': { '$multiply': ['$timestamp', 1000] }
                }
            },
            {
                '$group': {
                    '_id': {
                        'imei': '$imei',
                        'source_number': '$source_number'
                    },
                    'first_call': { '$min': { '$toDate': '$timestamp_in_milliseconds' } },
                    'last_call': { '$max': { '$toDate': '$timestamp_in_milliseconds' } },
                    'doc_count': { '$sum': 1 }
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'imei': '$_id.imei',
                    'tower_source_number': '$_id.source_number',
                    'tower_first_call': {
                        '$dateToString': {
                            'format': '%Y-%m-%d %H:%M:%S',
                            'date': '$first_call'
                        }
                    },
                    'tower_last_call': {
                        '$dateToString': {
                            'format': '%Y-%m-%d %H:%M:%S',
                            'date': '$last_call'
                        }
                    },
                    'tower_total_matches': '$doc_count',
                    'source':'tower_cdr'
                }
            }
        ]
        result = list(self.collection_indcase.aggregate(pipeline))
        # pprint(result)
        result_dict = {}
        for i in result:
            if i['imei'] not in result_dict:
                result_dict[i['imei']] = {'tower':[],'cdr':[],'ipdr':[]}
            result_dict[i['imei']]['tower'].append(i)
                
        # pprint(result_dict)   
        matched_imeis = [entry['imei'] for entry in result]
        # print(matched_imeis)
        
        pipeline2 = [
            {
                '$match':{'imei':{'$in':matched_imeis}}
            },
            {
                '$addFields': {
                    'timestamp_in_milliseconds': { '$multiply': ['$timestamp', 1000] }
                }
            },
            {
                '$group': {
                    '_id': {
                        'imei': '$imei',
                        'source_number': '$source_number'
                    },
                    'first_call': { '$min': { '$toDate': '$timestamp_in_milliseconds' } },
                    'last_call': { '$max': { '$toDate': '$timestamp_in_milliseconds' } },
                    'doc_count': { '$sum': 1 }
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'imei': '$_id.imei',
                    'cdr_source_number': '$_id.source_number',
                    'cdr_first_call': {
                        '$dateToString': {
                            'format': '%Y-%m-%d %H:%M:%S',
                            'date': '$first_call'
                        }
                    },
                    'cdr_last_call': {
                        '$dateToString': {
                            'format': '%Y-%m-%d %H:%M:%S',
                            'date': '$last_call'
                        }
                    },
                    'cdr_total_matches': '$doc_count',
                    'source':'cdr'
                }
            }
        ]
        result2 = list(self.cdr_collection.aggregate(pipeline2))
        for i in result2:
            if i['imei'] not in result_dict:
                result_dict[i['imei']] = {'cdr':[]}
            result_dict[i['imei']]['cdr'].append(i)     
        matched_imeis_str = [int(imei) for imei in matched_imeis]
        pipeline3 = [
            {
                '$match':{'imei':{'$in':matched_imeis_str}}
            },
            {
                '$group': {
                    '_id': {
                        'imei': '$imei',
                        'source_number': '$msisdn'
                    },
                    'first_call': {'$min': {'$toDate': {'$substr': ['$time', 0, 19]}}},
                    'last_call': {'$max': {'$toDate': {'$substr': ['$time', 0, 19]}}},
                    'doc_count': { '$sum': 1 }
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'imei': '$_id.imei',
                    'ipdr_source_number': '$_id.source_number',
                    'ipdr_first_call': {
                        '$dateToString': {
                            'format': '%Y-%m-%d %H:%M:%S',
                            'date': '$first_call'
                        }
                    },
                    'ipdr_last_call': {
                        '$dateToString': {
                            'format': '%Y-%m-%d %H:%M:%S',
                            'date': '$last_call'
                        }
                    },
                    'ipdr_total_matches': '$doc_count',
                    'source':'ipdr'
                }
            }
        ]
        result3 = list(self.collection_ipdr.aggregate(pipeline3))
        for i in result3:
            if i['imei'] not in result_dict:
                result_dict[i['imei']] = {'ipdr':[]}
            result_dict[i['imei']]['ipdr'].append(i)     
        # pprint(result2)
        pprint(result_dict)
        return result_dict

    def imei_find(self,casename,casetype):
        for i in self.collection_ipdr.find():
            imei  = int(i['imei'])
            self.collection_ipdr.update_one({'_id':i['_id']},{'$set':{'imei':imei}})

        
if __name__ == '__main__':
    # Tower_View().case_analysis({'casename':'Andhra','casetype':'towercdr'})
    # Tower_View().cdr_profile("7702003961")
    # Tower_View().othernumber_tracking("7002003961")
    Tower_View().matched_bparty_contact()