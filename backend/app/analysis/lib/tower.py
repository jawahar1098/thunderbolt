from pymongo import MongoClient
import re
from loguru import logger
from datetime import datetime, timedelta
import time
from bson.json_util import dumps
from datetime import datetime
import datetime as datetimeasnow
import time
import re
from math import sin, cos, sqrt, atan2, radians
import pymongo
from pprint import pprint
import openpyxl
from flask import jsonify
import os
from MongoClinet import CDAT, VIGOR, thunderbolt
mongothunder = thunderbolt()
mongocdat = CDAT()
mongovigor = VIGOR()


class Tower_View():
    def __init__(self):
        # self.client = MongoClient('mongodb://localhost:27017')

        self.collection = mongocdat.towercdrdata
        self.cdr_collection = mongocdat.cdrdata
        self.collection_cellidchart = mongocdat.cellidchart
        self.collection_newcell = mongocdat.cellidchart_jio
        self.collection_indcase = mongocdat.indcase
        self.collection_ipdr = mongocdat.ipdr
        # self.mapdata = mongocdat.mapdata4
        self.collection_sdr = mongocdat.sdrdata
        self.collection_suspect = mongocdat.suspect

        # client2 = MongoClient('mongodb://0.0.0.0:27017')
        # db2 = client2['CDAT']
        # self.collection_newcell = db2['cellid_jio']
        pass

    def get_tower_in_polygon(self, coords):
        try:

            print('coordinate:', coords)
            for coord in coords:
                print(coord, "-------------------")
            start_time = time.time()
            polygon_coords = [{'longitude': float(coord['longitude']), 'latitude': float(
                coord['latitude'])} for coord in coords]
            print(polygon_coords)
            coords_time = time.time()
            towers_in_polygon = list(self.collection_newcell.find({
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
            }, {'_id': 0, 'celltowerid': 1, 'tower_key': 1, 'provider': 1, 'lat': 1, 'long': 1, 'azimuth': 1, 'areadescription': 1, 'location': 1}))
            mongo_time = time.time()

            cdr_in_towers = []
            # for tower in towers_in_polygon:
            #     # tower_key = tower['tower_key']
            #     tower_id = tower['celltowerid']

            #     cdr_records = self.cdr_collection.find({'first_cgid': tower_id})
            #     for cdr_record in cdr_records:
            #         cdr_data = {
            #             'tower_location': tower['location'],
            #             'cdr_data': {
            #                 'source_number': cdr_record['source_number'],
            #                 'call_type': cdr_record['call_type'],
            #                 'timestamp': cdr_record['timestamp'],
            #                 'destination_number': cdr_record['destination_number'],
            #                 'first_cgid': cdr_record['first_cgid']
            #             }
            #         }
            #         cdr_in_towers.append(cdr_data)
            loop_time = time.time()
            result = {
                'towers_in_polygon': towers_in_polygon,
                'cdr_in_towers': cdr_in_towers
            }
            result_time = time.time()
            # print(result)
            print(
                f'Function Execution Time: {result_time - start_time} seconds')
            print(
                f'Coordinates Processing Time: {coords_time - start_time} seconds')
            print(f'MongoDB Query Time: {mongo_time - coords_time} seconds')
            print(f'Loop Processing Time: {loop_time - mongo_time} seconds')
            print(f'Result Processing Time: {result_time - loop_time} seconds')
            return result

        except Exception as e:
            print('Error:', e)
            # return jsonify({'error': str(e)})

    def bookmarkdata(self, send_data):
        # data = request.get_json()
        print(send_data, 'send dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        insert_result = self.mapdata.insert_one(send_data)
        print(insert_result)
        return jsonify({"message": "Bookmarks added"})

    def casedata(self, user):
        print(user,"==============")
        getdistinctcase = mongothunder.casedata.find({'username': user},{'_id':0})
        print(getdistinctcase, "-------casename------")
        result = []
        for _r in getdistinctcase:
            result.append(_r)
        logger.info("function starts")
        print(result,"====================")
        return result

    def get_tower(self, coords):
        try:

            print('coordinate:', coords)
            for coord in coords:
                print(coord, "-------------------")
            polygon_coords = [{'longitude': float(coord['longitude']), 'latitude': float(
                coord['latitude'])} for coord in coords]
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
            }, {'_id': 0}))
        except Exception as e:
            pass

        return towers_in_polygon

    def imeisummary(self, casename, casetype, user):
        print("afsdfgkjhadfagsdkjhasgdfjhgkjh")

        pipeline = [
            {
                '$match': {
                    'casename': casename,
                    'casetype': casetype,
                    'user': user
                }
            },
            {
                '$addFields': {
                    'timestamp_in_milliseconds': {'$multiply': ['$timestamp', 1000]}
                }
            },
            {
                '$group': {
                    '_id': {
                        'imei': '$imei',
                        'source_number': '$source_number'
                    },
                    'first_call': {'$min': {'$toDate': '$timestamp_in_milliseconds'}},
                    'last_call': {'$max': {'$toDate': '$timestamp_in_milliseconds'}},
                    'doc_count': {'$sum': 1}
                }
            },
            {
                '$project': {
                    '_id': 0,
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
                '$sort': {
                    'imei': 1
                }
            }
        ]
        result = {}
        result['casesummary'] = list(
            self.collection_indcase.aggregate(pipeline))
        dis_imei = self.collection_indcase.distinct(
            'imei', {'casename': casename, 'casetype': casetype})
        ov_sum = pipeline = [
            {
                '$match': {
                    'imei': {'$in': dis_imei}

                }
            },
            {
                '$addFields': {
                    'timestamp_in_milliseconds': {'$multiply': ['$timestamp', 1000]}
                }
            },
            {
                '$group': {
                    '_id': {
                        'imei': '$imei',
                        'source_number': '$source_number'
                    },
                    'first_call': {'$min': {'$toDate': '$timestamp_in_milliseconds'}},
                    'last_call': {'$max': {'$toDate': '$timestamp_in_milliseconds'}},
                    'doc_count': {'$sum': 1}
                }
            },
            {
                '$project': {
                    '_id': 0,
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
                '$sort': {
                    'imei': 1
                }
            }
        ]

        result['overallsummary'] = list(self.collection.aggregate(ov_sum))
        print(len(result))
        # print(len(result))
        if result:
            print("empty dict")
        return result

    def signlecase(self, casename, casetype, items_per_page, current_page, user):
        skip_doc = int(items_per_page) * (int(current_page))
        end_doc = skip_doc + items_per_page
        print(skip_doc, "=========", end_doc)
        # getdistinctcase = list(self.collection_indcase.find({'casename':casename,'casetype':casetype}))
        result = {}
        # for i in getdistinctcase:
        i = casename
        result['casename'] = casename
        for x in self.collection_indcase.find({'casename': i, 'user': user}).limit(1):
            result['casetype'] = x['casetype']
        result['totalDoc'] = self.collection_indcase.count_documents(
            {'casename': i, 'user': user})
        result['totalFiles'] = len(self.collection_indcase.distinct(
            'file_hash', {'user': user, 'casename': i}))
        for x in self.collection_indcase.find({'casename': i, 'user': user}).sort('as_on_date', pymongo.DESCENDING).limit(1):
            result['updatetime'] = x['as_on_date'].strftime(
                "%d-%m-%Y %H:%M:%S")
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
            _t = self.collection_cellidchart.find_one(
                {'lat': _tow['latitude'], 'long': _tow['longitude']})
            # print(_t)
            if _t is not None:
                towers['cellids'] = _t['celltowerid']
                towers['towername'] = _t['areadescription']

        regex_pattern = '^(?:[6-9]\\d{9}|91[6-9]\\d{10})$'
        ind_num = self.collection_indcase.distinct('source_number', {'casename': casename, 'source_number': {'$regex': regex_pattern}, 'user': user})
        result['distinct_num'] = len(ind_num)
        result['count_pages'] = len(ind_num)
        result['formulaOne'] = [self.tower_profile(ind_num[int(skip_doc):int(end_doc)], casename, casetype, user)]
        # result['formulaOne'] = []
        # for i_num in ind_num[int(skip_doc):int(end_doc)]:
        #     print(i_num)
        #     result['formulaOne'].append(self.tower_profile(i_num,casename,casetype))
        # break

        # print(result)
        return result

    def case_analysis(self, data):
        casename = data['casename']
        casetype = data['casetype']
        getdata = self.collection_indcase.find(
            {'casename': casename, 'casetype': casetype})
        resutl = {}
        for _d in getdata:
            if _d['provider'] not in resutl:
                resutl[_d['provider']] = set()
            resutl[_d['provider']].add(_d['first_siteaddress'])
        print(resutl)

    def tower_profile(self, data, casename, casetype, user):
        print(data, "------num")
        result = {}
        match_conditions = {'source_number': {'$in': data}}

        # match_conditions['source_number'] = data
        match_conditions['casename'] = casename
        match_conditions['casetype'] = casetype
        match_conditions['user'] = user
        pipeline = [
            {
                "$match": match_conditions
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
                    "source_number": {"$first": "$source_number"},
                    "min_date": {"$min": "$dateObj"},
                    "max_date": {"$max": "$dateObj"},
                    "no_dates_present": {"$addToSet": "$date"},
                    "no_unique_destination_numbers": {"$addToSet": "$destination_number"},
                    "imei_local": {"$addToSet": "$imei"},
                    "tower": {"$addToSet": "$sitename"},
                    "sector": {"$addToSet": "$first_cgid"},
                    "state": {"$addToSet": "$state"},
                    "provider": {"$addToSet": "$provider"},
                    "total_calls_count": {"$push": {"id": "$_id", "count": 1}},
                    "total_in_count": {
                        "$sum": {"$cond": [{"$in": ["$incoming", [1]]}, 1, 0]}
                    },
                    "total_out_count": {
                        "$sum": {"$cond": [{"$in": ["$incoming", [0]]}, 1, 0]}
                    },
                    "total_callin_count": {
                        "$sum": {"$cond": [{"$in": ["$call_type", ["call_in"]]}, 1, 0]}
                    },
                    "total_callout_count": {
                        "$sum": {"$cond": [{"$in": ["$call_type", ["call_out"]]}, 1, 0]}
                    },
                    "total_smo_count": {
                        "$sum": {"$cond": [{"$in": ["$call_type", ["sms_out"]]}, 1, 0]}
                    },
                    "total_smi_count": {
                        "$sum": {"$cond": [{"$in": ["$call_type", ["sms_in"]]}, 1, 0]}
                    },
                    "callInCount": {
                        "$sum": {"$cond": [{"$eq": ["$call_type", "call_in"]}, 1, 0]}
                    },
                    "callOutCount": {
                        "$sum": {"$cond": [{"$eq": ["$call_type", "call_out"]}, 1, 0]}
                    },
                    'validUnique': {
                        '$addToSet': {
                            '$ifNull': [
                                {
                                    '$cond': {
                                        'if': {'$eq': ['$isValid', 'valid']},
                                        'then': '$destination_number',
                                        'else': '$$REMOVE'
                                    }
                                },
                                0
                            ]
                        }
                    },
                    'notValidUnique': {
                        '$addToSet': {
                            '$ifNull': [
                                {
                                    '$cond': {
                                        'if': {'$eq': ['$isValid', 'notValid']},
                                        'then': '$destination_number',
                                        'else': '$$REMOVE'
                                    }
                                },
                                0
                            ]
                        }
                    }
                }
            },
            {
                "$addFields": {
                    "date_difference": {
                        "$divide": [
                            {
                                "$subtract": [
                                    {"$max": "$max_date"},
                                    {"$min": "$min_date"}
                                ]
                            },
                            86400000
                        ]
                    },
                    "dates_present": {"$size": "$no_dates_present"},
                    "other_number": {"$size": "$no_unique_destination_numbers"},
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
            {
                "$lookup":{
                    "from":"cdat_sdr",
                    "localField": 'source_number',
                    'foreignField': "source_number",
                    "as": "sdrData"
                }
            },
            # {
            #     "$unwind": "$cdrData"
            # },
            {
                "$group": {
                    "_id": "$source_number",
                    "min_date": {"$first": "$min_date"},
                    "max_date": {"$first": "$max_date"},
                    "date_difference": {"$first": "$date_difference"},
                    "dates_present": {"$first": "$dates_present"},
                    "other_number": {"$first": "$other_number"},
                    "imei": {"$first": "$imei_local"},
                    "tower": {"$first": "$tower"},
                    "sector": {"$first": "$sector"},
                    "state": {"$first": "$state"},
                    "provider": {"$first": "$provider"},
                    "nickname": {"$first": "$suspectData.nickname"},
                    "imei_count_cdr": {"$addToSet": "$cdrData.imei"},
                    "total_calls_count": {"$first": "$total_calls_count"},
                    "total_in_count": {"$first": "$total_in_count"},
                    "total_out_count": {"$first": "$total_out_count"},
                    "total_callin_count": {"$first": "$total_callin_count"},
                    "total_callout_count": {"$first": "$total_callout_count"},
                    "total_smsout_count": {"$first": "$total_smo_count"},
                    "total_smsin_count": {"$first": "$total_smi_count"},
                    "validUniqueCount": {"$first": "$validUnique"},
                    "notValidUniqueCount": {"$first": "$notValidUnique"},
                    "address":{"$first":"$sdrData.permanent_address"},
                    "alternatenumber":{"$first":"$sdrData.alternate_number"},
                    "dateOfActivation":{"$first":"$sdrData.date_of_activation"},
                    "name":{"$first":"$sdrData.fullname"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source_number": "$_id",
                    "nickname": 1,
                    "address":1,
                    "alternatenumber":1,
                    "dateOfActivation":1,
                    "name":1,
                    "min_date": 1,
                    "max_date": 1,
                    "date_difference": 1,
                    "dates_present": 1,
                    "other_number": 1,
                    "imei": 1,
                    "tower": 1,
                    "sector": 1,
                    "state": 1,
                    "provider": 1,
                    "imei_count_cdr": 1,
                    "destination_counts": 1,
                    'validUniqueCount': 1,
                    'notValidUniqueCount': 1,
                    "total_call_count": {"$size": "$total_calls_count"},
                    "total_in_count": 1,
                    "total_out_count": 1,
                    "total_callin_count": 1,
                    "total_callout_count": 1,
                    "total_smsin_count": 1,
                    "total_smsout_count": 1,
                    "ratio": {
                        "$concat": [
                            {"$toString": "$total_in_count"},
                            ":",
                            {"$toString": "$total_out_count"}
                        ]
                    },
                    "ratio_call": {
                        "$concat": [
                            {"$toString": "$total_callin_count"},
                            ":",
                            {"$toString": "$total_callout_count"}
                        ]
                    },
                    'ratio_sms': {
                        "$concat": [
                            {"$toString": "$total_smsin_count"},
                            ":",
                            {"$toString": "$total_smsout_count"}
                        ]
                    }
                }
            }
        ]

        result = list(self.collection_indcase.aggregate(pipeline))
        # print(result,"-------resukgtuf")
        response = []
        for item in result:
            data = item['source_number']
            sms_data = self.only_sms(data, casename, casetype, user)
            incoming = self.only_incoming(data, casename, casetype, user)
            outgoing = self.only_outgoing(data, casename, casetype, user)
            print(sms_data, incoming, outgoing)
            item['only_sms'] = sms_data if sms_data else []

            item['only_incoming'] = incoming if incoming else []

            item['only_outgoing'] = outgoing if outgoing else []

            # print(item,"-----item------")
            response.append(item)
        print(response, "-----------response----------")

        return response

    def only_sms(self, data, casename, casetype, user):
        pipeline = [
            {
                '$match': {
                    'source_number': data,
                    'casename': casename,
                    'casetype': casetype,
                    'user': user,
                    'destination_number': {
                        '$regex': '^(91\\d{10}|\\d{10})$'
                    }
                }
            },
            {
                "$group": {
                    "_id": "$destination_number",
                    "call_types": {"$addToSet": "$call_type"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$match": {
                    "$or": [
                        {"call_types": {"$all": ["sms_in", "sms_out"], "$nin": [
                            "call_in", "call_out"]}},
                        {"call_types": {"$in": ["sms_in", "sms_out"], "$nin": [
                            "call_in", "call_out"]}}
                    ]
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "destination_number": "$_id",
                    "total_record": "$count"
                }
            }
        ]

        sms = list(self.collection_indcase.aggregate(pipeline))
        # print(sms)
        return sms

    def only_incoming(self, data, casename, casetype, user):
        pipeline = [
            {
                '$match': {
                    'source_number': data,
                    'casename': casename,
                    'casetype': casetype,
                    'user': user,
                    'destination_number': {
                        '$regex': '^(91\\d{10}|\\d{10})$'
                    }
                }
            },
            {
                "$group": {
                    "_id": "$destination_number",
                    "call_types": {"$addToSet": "$call_type"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$match": {
                    "call_types": {"$all": ["call_in"], "$nin": ["sms_in", "sms_out", "call_out"]},

                }
            },
            {
                "$project": {
                    "_id": 0,
                    "destination_number": "$_id",
                    "total_record": "$count"
                }
            }
        ]

        incoming = list(self.collection_indcase.aggregate(pipeline))
        # print(incoming)
        return incoming

    def only_outgoing(self, data, casename, casetype, user):
        pipeline = [
            {
                '$match': {
                    'source_number': data,
                    'casename': casename,
                    'casetype': casetype,
                    'user': user,
                    'destination_number': {
                        '$regex': '^(91\\d{10}|\\d{10})$'
                    }
                }
            },
            {
                "$group": {
                    "_id": "$destination_number",
                    "call_types": {"$addToSet": "$call_type"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$match": {
                    "call_types": {"$all": ["call_out"], "$nin": ["sms_in", "sms_out", "call_in"]},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "destination_number": "$_id",
                    "total_record": "$count"
                }
            }
        ]

        outgoing = list(self.collection_indcase.aggregate(pipeline))

        # print(outgoing)
        return outgoing

    def find_sus(self, data, casename, casetype, user):
        match_conditions = {'source_number': {'$in': data}}

        # match_conditions['source_number'] = data
        match_conditions['casename'] = casename
        match_conditions['casetype'] = casetype
        match_conditions['user'] = user

        print(match_conditions)
        # print(len(list(self.collection_indcase.find(match_conditions))))
        pipeline = self.collection_indcase.aggregate([
            {
                "$match": match_conditions

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
                                    {"case": {"$in": ["$call_type", [
                                        "call_in", "call_out"]]}, "then": "inout"},
                                    {"case": {"$in": ["$call_type", [
                                        "sms_out", "sms_in"]]}, "then": "smosmi"}
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
                    "nickname": {"$first": "$suspectData.nickname"},
                    "imei_count_cdr": {"$addToSet": "$cdrData.imei"}
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

    def cdr_profile(self, data):
        pipeline = self.cdr_collection.aggregate([
            {
                "$match": {
                    "source_number": data,
                    "call_type": {'$in': ['call_in', 'call_out', 'sms_in', 'sms_out', 'Voice_out']},

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
                    "source_number": {"$first": "$source_number"},
                    "min_date": {"$min": "$dateObj"},
                    "max_date": {"$max": "$dateObj"},
                    "no_dates_present": {"$addToSet": "$date"},
                    "no_unique_destination_numbers": {"$addToSet": "$destination_number"},
                    "no_unique_imei_count_local": {"$addToSet": "$imei"},
                    "no_unique_sector_count": {"$addToSet": "$first_cgid"},
                    "call_type_count": {
                        "$push": {
                            "$switch": {
                                "branches": [
                                    {"case": {"$in": ["$call_type", [
                                        "call_in", "call_out"]]}, "then": "inout"},
                                    {"case": {"$in": ["$call_type", [
                                        "sms_in", "sms_out"]]}, "then": "smosmi"}
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
                        "$sum": {"$cond": [{"$in": ["$call_type", ["call_in"]]}, 1, 0]}
                    },
                    "total_out_count": {
                        "$sum": {"$cond": [{"$in": ["$call_type", ["call_out"]]}, 1, 0]}
                    },
                    "total_smo_count": {
                        "$sum": {"$cond": [{"$in": ["$call_type", ["sms_in"]]}, 1, 0]}
                    },
                    "total_smt_count": {
                        "$sum": {"$cond": [{"$in": ["$call_type", ["sms_out"]]}, 1, 0]}
                    },
                    "validUniqueCount": {"$sum": {"$cond": [{"$eq": ["$isValid", "valid"]}, 1, 0]}},
                    "notValidUniqueCount": {"$sum": {"$cond": [{"$eq": ["$isValid", "notValid"]}, 1, 0]}}
                }
            },
            {
                "$addFields": {
                    "date_difference": {
                        "$divide": [
                            {
                                "$subtract": [
                                    {"$max": "$max_date"},
                                    {"$min": "$min_date"}
                                ]
                            },
                            86400000
                        ]
                    },
                    "dates_present": {"$size": "$no_dates_present"},
                    "other_number": {"$size": "$no_unique_destination_numbers"},
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
                                    {"$gt": [{"$size": {"$filter": {
                                        "input": "$call_type_count", "cond": {"$eq": ["$$this", "inout"]}}}}, 0]},
                                    {"$gt": [{"$size": {"$filter": {
                                        "input": "$call_type_count", "cond": {"$eq": ["$$this", "smosmi"]}}}}, 0]}
                                ]
                            },
                            {
                                "$concat": [
                                    {"$toString": {"$size": {"$filter": {
                                        "input": "$call_type_count", "cond": {"$eq": ["$$this", "inout"]}}}}},
                                    ":",
                                    {"$toString": {"$size": {"$filter": {
                                        "input": "$call_type_count", "cond": {"$eq": ["$$this", "smosmi"]}}}}}
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
                    "min_date": {"$first": "$min_date"},
                    "max_date": {"$first": "$max_date"},
                    "date_difference": {"$first": "$date_difference"},
                    "dates_present": {"$first": "$dates_present"},
                    "other_number": {"$first": "$other_number"},
                    "imei": {"$first": "$imei"},
                    "tower": {"$first": "$tower"},
                    "sector": {"$first": "$sector"},
                    "ratio": {"$first": "$ratio"},
                    "nickname": {"$first": "$suspectData.nickname"},
                    "imei_count_cdr": {"$addToSet": "$cdrData.imei"},
                    "total_calls_count": {"$first": "$total_calls_count"},
                    "total_in_count": {"$first": "$total_in_count"},
                    "total_out_count": {"$first": "$total_out_count"},
                    "total_smo_count": {"$first": "$total_smo_count"},
                    "total_smt_count": {"$first": "$total_smt_count"},
                    "validUniqueCount": {"$first": "$validUniqueCount"},
                    "notValidUniqueCount": {"$first": "$notValidUniqueCount"}
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
                    "total_call_count": {"$size": "$total_calls_count"},
                    "destination_counts": 1,
                    "ratio": 1,
                    'validUniqueCount': 1,
                    'notValidUniqueCount': 1,
                    "ratio_call": {
                        "$concat": [
                            {"$toString": "$total_in_count"},
                            ":",
                            {"$toString": "$total_out_count"}
                        ]},
                    'ratio_sms': {
                        "$concat": [
                            {"$toString": "$total_smt_count"},
                            ":",
                            {"$toString": "$total_smo_count"}
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

    def common_link(self, value):
        numbers = value['numbers']
        selected_date_str = value['date']
        selected_date = datetime.strptime(
            selected_date_str, '%Y-%m-%d').strftime('%d-%m-%Y')
        result = {}
        result[selected_date] = {}
        for num in numbers:
            cell_data_list = []
            cell_number = self.cdr_collection.find(
                {"source_number": num, "date": selected_date})
            for cell in cell_number:
                cell_id = cell.get('first_cgid')
                print(cell_id)
                cell_records = self.collection_cellidchart.find(
                    {'celltowerid': cell_id})
                # print(list(cell_records))
                if cell_records == " ":
                    continue
                else:
                    for cell_record in cell_records:
                        print("entered")
                        cell_data = {
                            'tower_date': cell['date'],
                            'tower_time': cell['time'],
                            'tower_duration': cell['duration'],
                            'cell_id': cell_record['celltowerid'],
                            'tower_latitude': cell_record['lat'],
                            'tower_longitude': cell_record['long'],
                            'azimuth': cell_record['azimuth'],
                            'area_description': cell_record['areadescription']
                        }
                        cell_data_list.append(cell_data)

            result[selected_date][num] = cell_data_list

        if not selected_date:
            return {"No dates are selected"}
        if selected_date:
            return result[selected_date]
        

    def matched_bparty_contact(self, case_name, case_type, user):
        print(case_name, case_type, user, "-in bparty--")
        pipeline = [
            {
                '$match': {
                    'casename': case_name,
                    'casetype': case_type,
                    'user': user,
                    'destination_number': {
                        '$regex': '^(91\\d{10}|\\d{10})$'
                    }
                }
            },
            {
                '$group': {
                    '_id': None,
                    'unique_dest_numbers': {'$addToSet': '$destination_number'},
                    'unique_src_numbers': {'$addToSet': '$source_number'}
                }
            },
            {
                '$project': {
                    'unique_numbers': {'$setUnion': ['$unique_dest_numbers', '$unique_src_numbers']}
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
                '$lookup': {
                    'from': 'cdat_cdr',
                    'localField': 'unique_numbers',
                    'foreignField': 'source_number',
                    'as': 'matched_cdr_src'
                }
            },
            {
                '$addFields': {
                    'source_true': {
                        '$cond': {
                            'if': { '$in': ['$unique_numbers', '$matched_cdr_src.source_number'] },
                            'then': True,
                            'else': False
                        }
                    }
                }
            },
            {
                '$match': {
                    'matched_cdr': {'$ne': []}
                }
            },
             {
                '$lookup': {
                    'from': 'cdat_suspect',
                    'localField': 'unique_numbers',
                    'foreignField': 'phone',
                    'as': 'matched_suspect'
                }
            },
            {
                '$addFields': {
                    'nickname': {
                        '$cond': {
                            'if': {'$gt': [{'$size': '$matched_suspect'}, 0]},
                            'then': {'$arrayElemAt': ['$matched_suspect.nickname', 0]},
                            'else': ''
                        }
                    }
                }
            },
            {
                '$lookup': {
                    'from': 'ind_cases',
                    'let': {'num': '$unique_numbers'},
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$or': [
                                        {'$eq': ['$destination_number', '$$num']},
                                        {'$eq': ['$source_number', '$$num']}
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
                    'min_date': {'$min': '$ind_cases_matches.timestamp'},
                    'max_date': {'$max': '$ind_cases_matches.timestamp'},
                    'count': {'$sum': 1},
                    'source_true': {'$first': '$source_true'},
                    'nickname':{'$first': '$nickname'}
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'number': '$_id',
                    'min_date': {
                        '$dateToString': {
                            'format': '%Y-%m-%d %H:%M:%S',
                            'date': {'$toDate': {'$multiply': ['$min_date', 1000]}}
                        }
                    },
                    'max_date': {
                        '$dateToString': {
                            'format': '%Y-%m-%d %H:%M:%S',
                            'date': {'$toDate': {'$multiply': ['$max_date', 1000]}}
                        }
                    },
                    'count': '$count',
                    'source_true': '$source_true',
                    'nickname':1
                }
            }
        ]

        result = list(self.collection_indcase.aggregate(pipeline))
        # for item in result:
        #     if item['number'] == '8384064633':
        #         print(item)
        # pprint(result)
        print(len(result))
        return result

    def tower_imei(self, case_name, case_type, user):
        results = []

        print(case_name, case_type, user, "in imei--------")
        pipeline = [
            {
                '$match': {
                    'casename': case_name,
                    'casetype': case_type,
                    'user': user
                }
            },
            {
                '$lookup': {
                    'from': 'cdat_cdr',
                    'let': {'local_imei': '$imei'},
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$eq': ['$imei', '$$local_imei']
                                }
                            }
                        }
                    ],
                    'as': 'cdr_matches'
                }
            },
            {
                '$match': {
                    'cdr_matches': {'$ne': []}
                }
            },
            {
                '$addFields': {
                    'timestamp_in_milliseconds': {'$multiply': ['$timestamp', 1000]}
                }
            },
            {
                '$group': {
                    '_id': {
                        'imei': '$imei',
                        'source_number': '$source_number'
                    },
                    'first_call': {'$min': {'$toDate': '$timestamp_in_milliseconds'}},
                    'last_call': {'$max': {'$toDate': '$timestamp_in_milliseconds'}},
                    'doc_count': {'$sum': 1}
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
                    'source': 'tower_cdr'
                }
            }
        ]
        result = list(self.collection_indcase.aggregate(pipeline))
        pprint(result)
        result_dict = {}
        for i in result:
            if i['imei'] not in result_dict:
                result_dict[i['imei']] = {'tower': [], 'cdr': [], 'ipdr': []}
            result_dict[i['imei']]['tower'].append(i)

        # pprint(result_dict)
        matched_imeis = [entry['imei'] for entry in result]
        # print(matched_imeis)

        pipeline2 = [
            {
                '$match': {'imei': {'$in': matched_imeis}}
            },
            {
                '$addFields': {
                    'timestamp_in_milliseconds': {'$multiply': ['$timestamp', 1000]}
                }
            },
            {
                '$group': {
                    '_id': {
                        'imei': '$imei',
                        'source_number': '$source_number'
                    },
                    'first_call': {'$min': {'$toDate': '$timestamp_in_milliseconds'}},
                    'last_call': {'$max': {'$toDate': '$timestamp_in_milliseconds'}},
                    'doc_count': {'$sum': 1}
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
                    'source': 'cdr'
                }
            }
        ]
        result2 = list(self.cdr_collection.aggregate(pipeline2))
        for i in result2:
            if i['imei'] not in result_dict:
                result_dict[i['imei']] = {'cdr': []}
            result_dict[i['imei']]['cdr'].append(i)
        matched_imeis_str = [imei for imei in matched_imeis]
        pipeline3 = [
            {
                '$match': {'imei': {'$in': matched_imeis_str}}
            },
            {
                '$group': {
                    '_id': {
                        'imei': '$imei',
                        'source_number': '$msisdn'
                    },
                    'first_call': {'$min': {'$toDate': {'$substr': ['$time', 0, 19]}}},
                    'last_call': {'$max': {'$toDate': {'$substr': ['$time', 0, 19]}}},
                    'doc_count': {'$sum': 1}
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
                    'source': 'ipdr'
                }
            }
        ]
        result3 = list(self.collection_ipdr.aggregate(pipeline3))
        for i in result3:
            if i['imei'] not in result_dict:
                result_dict[i['imei']] = {'ipdr': []}
            result_dict[i['imei']]['ipdr'].append(i)
        # pprint(result_dict)
        print(len(result_dict))
        if len(result_dict) > 0:

            return result_dict
        else:
            result_dict = {'message': 'nodata'}
            return result_dict

    def get_tower_analysis(self, value):
        try:
            print("value:", value)
            items_per_page = value['items_per_page']
            total_page = value['page']
            skip_doc = items_per_page * (total_page-1)

            if value['type'] == 'cdr':
                if (len(value) == 4):
                    print("entered")
                    number = value['userNumber']
                    total = self.cdr_collection.count_documents(
                        {"source_number": number})
                    cell_number = self.cdr_collection.find(
                        {"source_number": number})
                    # .sort([("date", pymongo.ASCENDING), ("time", pymongo.ASCENDING)]).skip(skip_doc).limit(items_per_page)
                    result = []
                    for cell in cell_number:
                        cell_id = cell.get('first_cgid')
                        print(cell_id)
                        cell_records = self.collection_cellidchart.find(
                            {'celltowerid': cell_id})
                        for cell_record in cell_records:
                            cell_data = {
                                'tower_date': cell['date'],
                                'tower_time': cell['time'],
                                'tower_latitude': cell_record['lat'],
                                'tower_longitude': cell_record['long'],
                                'azimuth': cell_record['azimuth']
                            }
                            result.append(cell_data)
                    print(len(result), "----cdr tower map count----")
                else:
                    print("---------cdr tower map count with time range--------")
                    number = value['userNumber']
                    from_date_str = value['fromDate']
                    to_date_str = value['toDate']
                    from_date = datetime.strptime(
                        from_date_str, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
                    to_date = datetime.strptime(
                        to_date_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=999)

                    result = []
                    query = {
                        "source_number": number,
                        "$expr": {
                            "$and": [
                                {"$gte": [
                                    {"$dateFromString": {
                                        "dateString": "$date", "format": "%d-%m-%Y"}},
                                    from_date
                                ]},
                                {"$lte": [
                                    {"$dateFromString": {
                                        "dateString": "$date", "format": "%d-%m-%Y"}},
                                    to_date
                                ]}
                            ]
                        }
                    }
                    total = self.cdr_collection.count_documents(query)
                    cell_numbers = self.cdr_collection.find(query)
                    # .sort([("date", pymongo.ASCENDING), ("time", pymongo.ASCENDING)]).skip(skip_doc).limit(items_per_page)

                    for cell in cell_numbers:
                        cell_id = cell.get('first_cgid')
                        print(cell_id)
                        # cell_id = cell.get('cellid')
                        cell_records = list(
                            self.collection_cellidchart.find({'celltowerid': cell_id}))
                        # print(cell_records,"cell records")
                        for cell_record in cell_records:
                            print("inside cellid")
                            cell_data = {
                                'tower_date': cell['date'],
                                'tower_time': cell['time'],
                                'tower_latitude': cell_record['lat'],
                                'tower_longitude': cell_record['long'],
                                'azimuth': cell_record['azimuth']
                            }
                            result.append(cell_data)
            elif value['type'] == 'ipdr':
                print("ipdr selected")

                if len(value) == 4:
                    print("entered into no date")
                    number = value['userNumber']
                    total = self.collection_ipdr.count_documents(
                        {"msisdn": number})
                    print("tttttttttttttttttttttooooooooootal", total)
                    cell_number = self.collection_ipdr.find({"msisdn": number})
                    result = []
                    print(number)
                    for cell in cell_number:
                        cell_id = cell.get('cellid')
                        print(cell_id)
                        cell_records = self.collection_cellidchart.find(
                            {'celltowerid': cell_id})
                        for cell_record in cell_records:
                            # Format the "time" field into date and time parts
                            time_value = cell['time']
                            date_str = time_value.strftime('%Y-%m-%d')
                            time_str = time_value.strftime('%H:%M:%S')

                            cell_data = {
                                'tower_date': date_str,
                                'tower_time': time_str,
                                'tower_latitude': cell_record['lat'],
                                'tower_longitude': cell_record['long'],
                                'azimuth': cell_record['azimuth']
                            }
                            result.append(cell_data)
                    print(result)

                else:
                    print("entered into date")
                    number = value['userNumber']
                    from_date_str = value['fromDate']
                    to_date_str = value['toDate']

                    from_date = datetime.strptime(
                        from_date_str, "%Y-%m-%d").replace(hour=0, minute=0, second=0)
                    to_date = datetime.strptime(
                        to_date_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

                    result = []

                    query = {
                        "msisdn": number,
                        "time": {
                            "$gte": from_date,
                            "$lte": to_date
                        }
                    }

                    total = self.collection_ipdr.count_documents(query)
                    cell_numbers = self.collection_ipdr.find(query)

                    for cell in cell_numbers:
                        cell_id = cell.get('cellid')
                        cell_records = self.collection_cellidchart.find(
                            {'celltowerid': cell_id})
                        for cell_record in cell_records:
                            cell_data = {
                                'tower_date': cell['time'].strftime('%Y-%m-%d'),
                                'tower_time': cell['time'].strftime('%H:%M:%S'),
                                'tower_latitude': cell_record['lat'],
                                'tower_longitude': cell_record['long'],
                                'azimuth': cell_record['azimuth']
                            }
                            result.append(cell_data)
            return ({'cell_ids': result, 'totalpages': total})

        except Exception as e:
            print('Error:', e)

    def create_excel(self, casename, casetype, user):
        print(casename, casetype, "---------------------------")
        regex_pattern = '^(?:[6-9]\\d{9}|91[6-9]\\d{10})$'
        get_data = self.collection_indcase.distinct('source_number', {
                                                    'casename': casename, 'source_number': {'$regex': regex_pattern}, 'user': user})
        data = self.tower_profile(get_data, casename, casetype, user)
        filename = 'formulaOne.xlsx'
        filepath = f'{os.getcwd()}/app/analysis/lib/excel/'
        print(filepath)
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "Sheet1"
        a = 2
        for entry in data:
            pprint(entry)
            worksheet['A1'] = 'source_number'
            worksheet['B1'] = 'provider'
            worksheet['C1'] = 'name'
            worksheet['D1'] = 'address'
            worksheet['E1'] = 'Date of Activation'
            worksheet['F1'] = 'Alternate number'
            worksheet['G1'] = 'nickname'
            worksheet['H1'] = 'min_date'
            worksheet['I1'] = 'max_date'
            worksheet['J1'] = 'date_difference'
            worksheet['K1'] = 'dates_present'
            worksheet['L1'] = 'total_call_count'
            worksheet['M1'] = 'other_number'
            worksheet['N1'] = 'validUniqueCount'
            worksheet['O1'] = 'notValidUniqueCount'
            worksheet['P1'] = 'total callin count'
            worksheet['Q1'] = 'total callout count'
            worksheet['R1'] = 'total smsin count'
            worksheet['S1'] = 'total smsout count'
            worksheet['T1'] = "states"
            worksheet['U1'] = 'tower'
            worksheet['V1'] = 'sector'
            worksheet['W1'] = 'imei'
            worksheet['X1'] = 'only sms'
            worksheet['Y1'] = 'only incoming'
            worksheet['Z1'] = 'only outgoing'
            worksheet['AA1'] = 'imei cdr'

            worksheet[f'A{a}'] = entry['source_number']
            worksheet[f'B{a}'] = ','.join(entry['provider'])
            worksheet[f'C{a}'] = ','.join(entry['name'])
            worksheet[f'D{a}'] = ', '.join(entry['address'])
            worksheet[f'E{a}'] = ','.join(entry['dateOfActivation'])
            worksheet[f'F{a}'] = ','.join(entry['alternatenumber'])
            worksheet[f'G{a}'] = ','.join(entry['nickname'])
            worksheet[f'H{a}'] = datetime.strftime(entry['min_date'], '%d-%m-%Y %H:%M')
            worksheet[f'I{a}'] = datetime.strftime(entry['max_date'], '%d-%m-%Y %H:%M')
            worksheet[f'J{a}'] = entry['date_difference']
            worksheet[f'K{a}'] = entry['dates_present']
            worksheet[f'L{a}'] = entry['total_call_count']
            worksheet[f'M{a}'] = entry['other_number']
            worksheet[f'N{a}'] = ', '.join(map(str, entry['validUniqueCount']))
            worksheet[f'O{a}'] = ', '.join(map(str,entry['notValidUniqueCount']))
            worksheet[f'P{a}'] = entry['total_callin_count']
            worksheet[f'Q{a}'] = entry['total_callout_count']
            worksheet[f'R{a}'] = entry['total_smsin_count']
            worksheet[f'S{a}'] = entry['total_smsout_count']
            worksheet[f'T{a}'] = ', '.join(entry['state'] if entry['state'][0] is not None else "")
            worksheet[f'U{a}'] = ', '.join(entry['tower'])
            worksheet[f'V{a}'] = ', '.join(entry['sector'])
            worksheet[f'W{a}'] = ', '.join(entry['imei'])
            worksheet[f'X{a}'] = len(entry['only_sms'])
            worksheet[f'Y{a}'] = len(entry['only_incoming'])
            worksheet[f'Z{a}'] = len(entry['only_outgoing'])
            worksheet[f'AA{a}'] = ', '.join(
                map(str, entry['imei_count_cdr'][0]))
            a += 1

        workbook.save(f'{filepath}/{filename}')

        return filepath, filename

    def detailed_view(self, casename, casetype, user):
        print(casename, casetype, user, "Datas")
        # client = MongoClient('mongodb://localhost:27017')
        # db = client['CDAT']
        # indcase = db['ind_cases']
        print("sdi pipeline", datetime.now())
        sdi_pipeline = [
            {"$match": {'casename': casename,
                        'casetype': casetype,
                        'user': user,
                        'sitename':{'$ne':""}
                        }
             },
            {"$group": {
                '_id': {
                    'sitename': '$sitename',
                },
                'source_numbers': {'$addToSet': '$source_number'},
                'destination_numbers': {'$addToSet': '$destination_number'},
                'imeis': {'$addToSet': '$imei'}
            }},
            {"$lookup": {
                'from': "cdat_cellidchart",
                'localField': "_id.sitename",
                'foreignField': "areadescription",
                'as': "matched_cellid"
            }
            },
            {"$project": {
                '_id': 0,
                'sitename': '$_id.sitename',
                'lat': {"$first": "$matched_cellid.lat"},
                'long': {"$first": "$matched_cellid.long"},
                'source_numbers': 1,
                'destination_numbers': 1,
                'imeis': 1
            }
            }
        ]
        distinct_sdi = list(mongocdat.indcase.aggregate(sdi_pipeline))
        # pprint(distinct_sdi)
        print("duration pipeline")

        duration_pipeline = [
            {
                "$match": {'casename': casename, 'casetype': casetype, 'user': user, 'duration': 0}
            },
            {
                "$group": {
                    '_id': '$source_number',
                    'count': {'$sum': 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    'source_numbers': '$_id',
                    'count': 1
                }
            }
        ]
        zero_dur_num = list(mongocdat.indcase.aggregate(duration_pipeline))
        # print(zero_dur_num, "Zero Duration Number")
        print("cdr source pipeline")

        cdat_source = [
            {
                "$match": {
                    'casename': casename,
                    'casetype': casetype,
                    'user': user
                }
            },
            {
                "$group": {
                    '_id': '$source_number'
                }
            },
            
            {
                "$lookup": {
                    'from': "cdat_cdr",
                    'let':{'src_number':'$_id'},
                    'pipeline':[{
                        '$match':{
                            '$expr':{
                                '$eq': ['$source_number','$$src_number']
                            }
                        }
                    }],
                    'as': "matched_cdr"
                }
            },
            {
                '$match': {
                    'matched_cdr.0': {'$exists': True}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "source_numbers": {"$addToSet": "$_id"}
                }
            },
            {
                "$project": {
                    '_id': 0,
                    'source_numbers': 1
                }
            }
        ]

        matched_cdat_source = list(mongocdat.indcase.aggregate(cdat_source))
        # print(matched_cdat_source, "matched source number")
        print("cdatimei pipeline")

        cdat_imei = [
            {
                "$match": {
                    'casename': casename,
                    'casetype': casetype,
                    'user': user
                }
            },
            {
                "$group": {
                    '_id': '$imei'
                }
            },
            {
                "$lookup": {
                    'from': "cdat_cdr",
                    'let':{'imei_num':'$_id'},
                    'pipeline':[{
                        '$match':{
                            '$expr':{
                                '$eq': ['$imei','$$imei_num']
                            }
                        }
                    }],
                    'as': "matched_cdr"
                }
            },
            {
                '$match': {
                    'matched_cdr.0': {'$exists': True}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "imeis": {"$addToSet": "$_id"}
                }
            },
            {
                "$project": {
                    '_id': 0,
                    'imeis': 1
                }
            }
        ]

        matched_cdat_imei = list(mongocdat.indcase.aggregate(cdat_imei))
        # print(matched_cdat_imei, "matched cdat imei")
        print("cdatother pipeline")

        cdat_other_in_phone = [
            {
                "$match": {
                    'casename': casename,
                    'casetype': casetype,
                    'user': user
                }
            },
            {
                "$group": {
                    '_id': '$source_number'
                }
            },
            {
                "$lookup": {
                    'from': "cdat_cdr",
                    'let':{'other_num':'$_id'},
                    'pipeline':[{
                        '$match':{
                            '$expr':{
                                '$eq': ['$source_number','$$other_num']
                            }
                        }
                    }],
                    'as': "matched_cdr"
                }
            },
            {
                '$match': {
                    'matched_cdr.0': {'$exists': True}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "source_numbers": {"$addToSet": "$_id"}
                }
            },
            {
                "$project": {
                    '_id': 0,
                    'source_numbers': 1
                }
            }
        ]

        cdat_des_in_phone = list(
            mongocdat.indcase.aggregate(cdat_other_in_phone))
        # print(cdat_des_in_phone, "matched des in phone")
        print("casdat source in des pipeline")

        cdat_source_in_des = [
            {
                "$match": {
                    'casename': casename,
                    'casetype': casetype,
                    'user': user,
                    'destination_number':{'$regex':'^(91\d{10}|\d{10})$'}
                }
            },
            {
                "$group": {
                    '_id': '$destination_number'
                }
            },
            {
                "$lookup": {
                    'from': "cdat_cdr",
                    'let':{'dest_number':'$_id'},
                    'pipeline':[{
                        '$match':{
                            '$expr':{
                                '$eq': ['$source_number','$$dest_number']
                            }
                        }
                    }],
                    'as': "matched_cdr"
                }
            },
            {
                '$match': {
                    'matched_cdr.0': {'$exists': True}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "destination_numbers": {"$addToSet": "$_id"}
                }
            },
            {
                "$project": {
                    '_id': 0,
                    'destination_numbers': 1
                }
            }
        ]

        cdat_src_in_des = list(mongocdat.indcase.aggregate(cdat_source_in_des))
        # print(cdat_src_in_des, "cdat source in des")

        source_num = list(mongocdat.indcase.distinct('source_number', {
                          'casename': casename, 'casetype': casetype, 'user': user}))
        # print(source_num, "source number")
        dest_num = list(mongocdat.indcase.distinct('destination_number', {
                        'casename': casename, 'casetype': casetype, 'user': user}))
        # print(dest_num, "destination number")
        result_num = source_num + dest_num
        # print(result_num, "result number")
        unique_num = list(set(result_num))
        # print(unique_num, "unique number")
        print("vigor pipeline")

        vigor = [
            {
                "$match": {'TXT_TARGET_NUMBER': {"$in": unique_num}}
            },
            {
                '$group': {'_id': '$TXT_TARGET_NUMBER'}
            },
            {
                '$group': {
                    '_id': None,
                    'vigor_source': {"$addToSet": "$_id"}
                }
            },
            {'$project': {"_id": 0, "vigor_source": 1}}

        ]

        vigor_num = list(mongovigor.cri_meta.aggregate(vigor))
        # print(vigor_num, "vigor num")
        print("new number pipeline")

        new_number = [
            {
                '$match': {'casename': casename, 'casetype': casetype, 'user': user}
            },
            {
                '$group': {
                    '_id': {'imei': "$imei", 'source_number': "$source_number"}
                }
            },
            {
                '$lookup': {
                    'from': "cdat_cdr",
                    'localField': "_id.imei",
                    'foreignField': "imei",
                    'as': "matched_docs"
                }
            },
            {
                '$unwind': "$matched_docs"
            },
            {
                '$match': {
                    '$expr': {
                        '$ne': ["$_id.source_number", "$matched_docs.source_number"]
                    }
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'imei': '$_id.imei',
                    'source_number_indcases': "$_id.source_number",
                    'source_number_cdatcdr': "$matched_docs.source_number"
                }
            },
            {
                '$group': {
                    '_id': "$imei",
                    'matched_pairs': {
                        '$addToSet': {
                            'source_number_indcases': "$source_number_indcases",
                            'source_number_cdatcdr': "$source_number_cdatcdr"
                        }
                    }
                }
            }
        ]

        new_cdat_number = list(mongocdat.indcase.aggregate(new_number))
        # print(new_cdat_number)

        response = {}
        if len(distinct_sdi) < 0:
            response['distinct_sdi'] = []
            response['sdi_status'] = 'failure'
        else:
            response['distinct_sdi'] = distinct_sdi,
            response['sdi_status'] = 'success'

        if len(zero_dur_num) < 0:
            response['zero_dur_num'] = [],
            response['z_status'] = 'failure'
        else:
            response['zero_dur_num'] = zero_dur_num,
            response['z_status'] = 'success'
        if len(matched_cdat_source) < 0:
            response['cdat_source'] = [],
            response['cdat_s_status'] = 'failure'
        else:
            response['cdat_source'] = matched_cdat_source,
            response['cdat_s_status'] = 'success'
        if len(matched_cdat_imei) < 0:
            response['cdat_imei'] = [],
            response['cdat_imei_status'] = 'failure'
        else:
            response['cdat_imei'] = matched_cdat_imei,
            response['cdat_imei_status'] = 'success'
        if len(cdat_des_in_phone) < 0:
            response['cdat_des_in_phone'] = [],
            response['cdat_des_status'] = 'failure'
        else:
            response['cdat_des_in_phone'] = cdat_des_in_phone,
            response['cdat_des_status'] = 'success'
        if len(cdat_src_in_des) < 0:
            response['cdat_src_in_des'] = [],
            response['cdat_src_status'] = 'failure'
        else:
            response['cdat_src_in_des'] = cdat_src_in_des,
            response['cdat_src_status'] = 'success'
        if len(vigor_num) < 0:
            response['vigor_num'] = [],
            response['vigor_status'] = 'failure'
        else:
            response['vigor_num'] = vigor_num,
            response['vigor_status'] = 'success'
        if len(new_cdat_number) < 0:
            response['cdatnumber_for_imei'] = [],
            response['cdat_num_imei_status'] = 'failure'
        else:
            response['cdatnumber_for_imei'] = vigor_num,
            response['cdat_num_imei_status'] = 'success'

        return response
    
    
    
    def call_details(self, data, mode, fromdate, todate, items=False, currentpage=False):
        print("inside cdr_daata")
        print(data, mode, items, currentpage, fromdate, todate, "-----in")
        print(mode, "---------------------------mode---------------------------")
        total_pages = 0
        if items == "false":
            skip_doc = False
            items_per_page = False
            current_page = False
        else:
            items_per_page = int(items)
            current_page = int(currentpage)
            skip_doc = int(items_per_page) * (int(currentpage))
        matching_documents = []
        if mode == "source":
            print(mode, "____________________mode__________________")
            print(data, fromdate, todate, items, current_page, "-------data----")
            if fromdate is None and todate is None:
                print(data, skip_doc, items_per_page, "number ----")
                total_pages = self.collection.count_documents(
                    {"source_number": data})
                if items_per_page == False and current_page == False:
                    matching_documents = list(self.collection.find({'source_number': data}).sort(
                        'timestamp', pymongo.DESCENDING))
                else:
                    if current_page > 0:  # Check if current_page is greater than 0
                        skip_doc = (current_page - 1) * items_per_page
                    matching_documents = list(self.collection.find({'source_number': data}).sort(
                        'timestamp', pymongo.DESCENDING).skip(skip_doc).limit(items_per_page))
                # pprint(matching_documents)
                logger.info("query completed for cdr or with date")
            elif fromdate is not None and todate is not None:
                print('date present')
                total_pages = self.collection.count_documents({
                    'source_number': data,
                    'timestamp': {
                        '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                        '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                    }
                })
                if items_per_page == False and current_page == False:
                    matching_documents = self.collection.find({
                        'source_number': data,
                        'timestamp': {
                            '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                            '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                        }
                    }).sort(
                        'timestamp', pymongo.DESCENDING)
                else:
                    if current_page > 0:  # Check if current_page is greater than 0
                        skip_doc = (current_page - 1) * items_per_page
                    print(skip_doc, "#####################")
                    matching_documents = self.collection.find({
                        'source_number': data,
                        'timestamp': {
                            '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                            '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                        }
                    }).sort('timestamp', pymongo.DESCENDING).skip(skip_doc).limit(items_per_page)
                    print("MMMMMMMMMMMM", matching_documents)

        if mode == "destination":
            print(mode, "____________________mode__________________")
            print(data, fromdate, todate, "-------data----")
            if fromdate is None and todate is None:
                print(data, skip_doc, items_per_page, "number ----")
                total_pages = self.collection.count_documents(
                    {"destination_number": data})
                if items_per_page == False and current_page == False:
                    matching_documents = self.collection.find({'destination_number': data}).sort(
                        'timestamp', pymongo.DESCENDING)
                else:
                    if current_page > 0:  # Check if current_page is greater than 0
                        skip_doc = (current_page - 1) * items_per_page
                    matching_documents = self.collection.find({'destination_number': data}).sort(
                        'timestamp', pymongo.DESCENDING).skip(skip_doc).limit(items_per_page)
                logger.info("query completed for cdr or with date")
            elif fromdate is not None and todate is not None:
                print('date present')
                total_pages = self.collection.count_documents({
                    'destination_number': data,
                    'timestamp': {
                        '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                        '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                    }
                })
                if items_per_page == False and current_page == False:
                    matching_documents = self.collection.find({
                        'destination_number': data,
                        'timestamp': {
                            '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                            '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                        }
                    }).sort(
                        'timestamp', pymongo.DESCENDING)
                else:
                    if current_page > 0:  # Check if current_page is greater than 0
                        skip_doc = (current_page - 1) * items_per_page
                    print(skip_doc, "#####################")
                    matching_documents = self.collection.find({
                        'destination_number': data,
                        'timestamp': {
                            '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                            '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                        }
                    }).sort('timestamp', pymongo.DESCENDING).skip(skip_doc).limit(items_per_page)
                    print("MMMMMMMMMMMM", matching_documents)

        if mode == "imei":
            if fromdate is None and todate is None:
                print(data, skip_doc, items_per_page, "number ----")
                total_pages = self.collection.count_documents(
                    {"imei": data})
                if items_per_page == False and current_page == False:
                    matching_documents = self.collection.find({'imei': data}).sort(
                        'timestamp', pymongo.DESCENDING)
                else:
                    if current_page > 0:  # Check if current_page is greater than 0
                        skip_doc = (current_page - 1) * items_per_page
                    matching_documents = self.collection.find({'imei': data}).sort(
                        'timestamp', pymongo.DESCENDING).skip(skip_doc).limit(items_per_page)
                logger.info("query completed for cdr or with date")
            elif fromdate is not None and todate is not None:
                print('date present')
                total_pages = self.collection.count_documents({
                    'imei': data,
                    'timestamp': {
                        '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                        '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                    }
                })
                if items_per_page == False and current_page == False:
                    matching_documents = self.collection.find({
                        'imei': data,
                        'timestamp': {
                            '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                            '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                        }
                    }).sort(
                        'timestamp', pymongo.DESCENDING)
                else:
                    if current_page > 0:  # Check if current_page is greater than 0
                        skip_doc = (current_page - 1) * items_per_page
                    print(skip_doc, "#####################")
                    matching_documents = self.collection.find({
                        'imei': data,
                        'timestamp': {
                            '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                            '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                        }
                    }).sort('timestamp', pymongo.DESCENDING).skip(skip_doc).limit(items_per_page)
                    print("MMMMMMMMMMMM", matching_documents)


        cdr_data = []
        cdrimei_data = []
        dest_data = []
        cdr = None
        logger.info("interation started...")
        # print(matching_documents,"--there--")
        for document in matching_documents:
            destination_number = document['destination_number']
            # calldate = document['timestamp']
            # calltime = document['timestamp']
            call_type = document.get('call_type','')
            duration = document['duration']
            if mode == "source" or mode == "destination":
                imei = document['imei']
            if mode == "imei" or mode == "destination":
                source_number = document['source_number']
            
            cellid = document.get('first_cgid','unknown')
            provider = document.get('provider','unknown')
            roaming = document.get('roaming_circle','unknown')
            calldate = document['date'] #datetimeasnow.datetime.fromtimestamp(document.get('timestamp','').strftime('%Y-%m-%d'))
            calltime = document['time'] #datetimeasnow.datetime.fromtimestamp(document.get('timestamp','').strftime('%H:%M:%S'))

            # Query the other collection for matching cellid
            cellid_match = self.collection_cellidchart.find_one(
                {'celltowerid': cellid})
            if cellid_match is not None:
                provider = cellid_match.get('provider','')
            # print(cellid_match,"cellid_match")
            if cellid_match:
                address = cellid_match['siteaddress']
                lat = cellid_match['lat']
                long = cellid_match['long']
                azimuth = cellid_match['azimuth']
            else:
                address = ""
                lat = 0.0
                long = 0.0
                azimuth = 0
            sdrfinds = self.collection_sdr.find_one(
                {'source_number': destination_number})
            nickname = [nickname.get('nickname', '') for nickname in self.collection_suspect.find(
                {'phone': destination_number}, {'_id': 0}).sort('timestamp', pymongo.ASCENDING).limit(-1)]

            # adresssdr = "Not available"
            if sdrfinds is not None:
                # nickname = sdrfinds.get('nickname')
                adresssdr = sdrfinds.get('local_address')
            else:
                nickname = ""
                adresssdr = ""
            if mode == "source":
                cdr = {
                    'source_number': data,
                    'destination_number': destination_number,
                    'nickname': nickname,
                    'calldate': calldate,
                    'calltime': calltime,
                    'call_type': call_type,
                    'duration': duration,
                    'imei': imei,
                    'cellid': cellid,
                    'provider': provider,
                    'roaming': roaming,
                    'address': address,
                    'latitude': lat,
                    'longitude': long,
                    'azimuth': azimuth,
                    'user_address': adresssdr
                }
                cdr_data.append(cdr)
            if mode == "imei":
                cdr = {
                    'imei': data,
                    'source_number': source_number,
                    'destination_number': destination_number,
                    'nickname': nickname,
                    'calldate': calldate,
                    'calltime': calltime,
                    'call_type': call_type,
                    'duration': duration,
                    'cellid': cellid,
                    'provider': provider,
                    'roaming': roaming,
                    'address': address,
                    'latitude': lat,
                    'longitude': long,
                    'azimuth': azimuth,
                    'user_address': adresssdr
                }
                # print(source_number)
                cdrimei_data.append(cdr)
            if mode == "destination":
                cdr = {
                    'imei': imei,
                    'source_number': source_number,
                    'destination_number': data,
                    'nickname': nickname,
                    'calldate': calldate,
                    'calltime': calltime,
                    'call_type': call_type,
                    'duration': duration,
                    'cellid': cellid,
                    'provider': provider,
                    'roaming': roaming,
                    'address': address,
                    'latitude': lat,
                    'longitude': long,
                    'azimuth': azimuth,
                    'user_address': adresssdr
                }
                # print(source_number)
                dest_data.append(cdr)
       
        logger.info("iteration completed...")
        if mode == "source":
            response = {'data_dict': cdr_data, 'totalpages': total_pages}
            return response
        if mode == "imei":
            response = {'data_dict': cdrimei_data, 'totalpages': total_pages}
            return response
        if mode == "destination":          
            response = {'data_dict': dest_data, 'totalpages': total_pages}
            return response

    def imei_summary(self,data):
       size = len(data)
       print("imei summary")
       data_count = self.collection.find_one({'imei':{'$regex': '^' + data[:size]}}) 
       if data_count is None:
           response = {'status':'empty', 'message':'no data found'}
           print(response)
           return response
       else:
           pipeline = [
               {
                    '$match':{
                        'imei': {'$regex': '^' + data[:size]}  
                    }
                },
               {
                   '$group':{
                       '_id':{'imei':'$imei',
                              'source_number':'$source_number'},
                        "call_in": {
                                "$sum": {
                                    "$cond": [{"$eq": ["$incoming", 1]}, 1, 0]
                                    }
                            },
                        "call_out": {
                                    "$sum": {
                                        "$cond": [{"$eq": ["$incoming", 0]}, 1, 0]
                                    }
                                },
                        "first_call": {"$min": "$date_format"},
                        "last_call": {"$max": "$date_format"},
                        "duration": {"$sum": "$duration"},
                        "total_calls": {"$sum": 1}
                   }
               },
               {
                "$addFields": {
                    "first_call": {
                        "$dateToString": {
                            "format": "%Y-%m-%d %H:%M:%S",
                            "date": "$first_call"
                        }
                    },
                    "last_call": {
                        "$dateToString": {
                            "format": "%Y-%m-%d %H:%M:%S",
                            "date": "$last_call"
                        }
                    }
                }
              },
              {
                '$project': {
                    '_id': 0,
                    'sourcenumber':'$_id.source_number',
                    'imei_number':'$_id.imei',
                    "call_in": 1,
                    "call_out": 1,
                    "total_calls": 1,
                    "duration": 1,
                    "first_call": 1,
                    "last_call": 1
                    }
            }
           ]
           result = list(self.collection.aggregate(pipeline))
           pprint(result)
           response = {'data_dict': result, 'status': 'success',
                        'message': 'data retrived successfully'}

           return response

    def phone_summary(self,data):
       data_count = self.collection.find_one({ 'source_number' : data }) 
       if data_count is None:
           response = {'status':'empty', 'message':'no data found'}
           return response
       else:
           pipeline = [
               {
                   '$match':{
                       'source_number':data
                   }
               },
               {
                   '$group':{
                       '_id':{'imei':'$imei',
                              'source_number':'$source_number'},
                        "call_in": {
                                "$sum": {
                                    "$cond": [{"$eq": ["$incoming", 1]}, 1, 0]
                                    }
                            },
                        "call_out": {
                                    "$sum": {
                                        "$cond": [{"$eq": ["$incoming", 0]}, 1, 0]
                                    }
                                },
                        "first_call": {"$min": "$date_format"},
                        "last_call": {"$max": "$date_format"},
                        "duration": {"$sum": "$duration"},
                        "total_calls": {"$sum": 1}
                   }
               },
               {
                "$addFields": {
                    "first_call": {
                        "$dateToString": {
                            "format": "%Y-%m-%d %H:%M:%S",
                            "date": "$first_call"
                        }
                    },
                    "last_call": {
                        "$dateToString": {
                            "format": "%Y-%m-%d %H:%M:%S",
                            "date": "$last_call"
                        }
                    }
                }
              },
              {
                '$project': {
                    '_id': 0,
                    'sourcenumber':'$_id.source_number',
                    'imei_number':'$_id.imei',
                    "call_in": 1,
                    "call_out": 1,
                    "total_calls": 1,
                    "duration": 1,
                    "first_call": 1,
                    "last_call": 1
                    }
            }
           ]
           result = list(self.collection.aggregate(pipeline))
           response = {'data_dict': result, 'status': 'success',
                        'message': 'data retrived successfully'}

           return response

           





# if __name__ == '__main__':
#     casename = "test"
#     casetype = "towercdr"
#     user = "super@gmail.com"

#     Tower_View().detailed_view(casename,casetype,user)
#     Tower_View().create_excel('testt','towercdr')
#     # Tower_View().cdr_profile("7702003961")
#     # Tower_View().othernumber_tracking("7002003961")
#     Tower_View().tower_imei('mahu','towercdr')
