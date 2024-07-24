import tqdm
import pymongo
import time
from datetime import datetime, timedelta
import math
from pprint import pprint
from loguru import logger
import re
from collections import defaultdict
import datetime as datetimeasnow
from pymongo import MongoClient
from MongoClinet import CDAT
mongocdat = CDAT()


logger.add("file_log.log",
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")


class Cdr_Analysis:
    def __init__(self):

        self.roaming_circle = ""
        self.collection_cdrdata = mongocdat.cdrdata
        self.collection_cellid = mongocdat.cellidchart
        self.collection_towerid = mongocdat.towercdrdata
        self.collection_sdrdata = mongocdat.sdrdata
        self.collection_ipdr = mongocdat.ipdrdata
        self.collection_voip = mongocdat.voip
        self.collection_matchedcall = mongocdat.matchedcall
        self.collection_poadata = mongocdat.poadata
        self.collection_gprs = mongocdat.gprs
        self.collection_suspect = mongocdat.suspect
        self.collection_phonearea = mongocdat.phonearea

        self.collection_cdrdata.create_index("source_number")
        self.collection_cdrdata.create_index("destination_number")
        self.collection_cdrdata.create_index("call_type")
        self.collection_cdrdata.create_index("imei")
        self.collection_cdrdata.create_index("imsi")
        self.collection_cdrdata.create_index("state")
        self.collection_cdrdata.create_index("duration")
        self.collection_cdrdata.create_index("first_cgid")
        self.collection_cdrdata.create_index("roaming_circle")
        self.collection_cdrdata.create_index(
            [("timestamp", pymongo.DESCENDING)])
        self.collection_cellid.create_index("celltowerid")
        self.collection_cellid.create_index("siteaddress")
        self.collection_cellid.create_index("lat")
        self.collection_cellid.create_index("long")
        self.collection_cellid.create_index("azimuth")
        self.collection_sdrdata.create_index("source_number")
        self.collection_sdrdata.create_index("nickname")
        self.collection_sdrdata.create_index("local_address")
        self.collection_gprs.create_index("Mobile No")

        self.imei_count = 0
        self.cdatcounts = 0
        self.roamingcount = 0
        self.cdatcontactnumber = ""
        self.imei = ''
        self.callin_count = 0
        self.callout_count = 0
        self.unique_numbers = set()
        self.unique_number_cdat = set()
        self.num_list = []

    def othernumber_tracking(self, number):
        number_pattern = re.compile(r'^\d{10}$|^91(\d{10})$')
        query = {'source_number': number,
                 'destination_number': {'$regex': number_pattern}}
        numbers = self.collection_cdrdata.distinct('destination_number', query)
        result = []
        for destination_number in numbers:
            cell_data = {
                'destination_number': destination_number,
            }
            result.append(cell_data)

        data = {'destination_numbers': result}
        print(data)
        return data

    def count_imei(self, checkvalue):
        if self.imei != checkvalue:
            self.imei_count.append(checkvalue)
            self.imei = checkvalue
        return None

    def cdat_count(self, data):
        print("IN COUNT")
        number_pattern = re.compile(r'^\d{10}$|^91(\d{10})$')
        matching_destination_documents = self.collection_cdrdata.find({'destination_number':  {
                                                                      '$regex': number_pattern}, 'source_number': data})  # , 'call_type': {'$in': ['call_in', 'call_out']}})
        for dest_num in matching_destination_documents:
            dest_number_1 = dest_num['destination_number']
            if dest_number_1 not in self.num_list:
                # ,{'$or':{'source_number':number, 'destination_number':data}})
                get_data = self.collection_cdrdata.find_one(
                    {'source_number': dest_number_1})
                if get_data is not None:
                    self.cdatcounts += 1
                    self.unique_numbers.add(dest_number_1)
                # else:
                #     get_suspect_data = self.collection_suspect.find_one(
                #         {'phone': dest_number_1})
                #     if get_suspect_data is not None:
                #         self.unique_numbers.add(dest_number_1)
                self.num_list.append(dest_number_1)

        dest_number = self.collection_cdrdata.distinct(
            'source_number', {'destination_number': data})
        for one_num in dest_number:
            self.unique_numbers.add(one_num)

        print(self.unique_numbers, "-----------------")
        cdat_num = []
        for _i in self.unique_numbers:
            cdat_num.append(_i)
        return cdat_num

    def roaming_count(self, roaming):
        if self.roaming_circle != roaming:
            self.roamingcount += 1
            self.roaming_circle = roaming

        return self.roamingcount

    def dest_contact(self, data):
        number_pattern = re.compile(r'^\d{10}$|^91(\d{10})$')
        query = {'source_number': data,
                 'destination_number': {'$regex': number_pattern}}
        unique_states = set()
        get_dest = self.collection_cdrdata.distinct(
            'destination_number', query)
        # print(get_dest)
        for dest in get_dest:
            get_home = self.collection_sdrdata.distinct(
                'state_key', {'source_number': dest})
            if len(get_home) == 0:
                get_home = self.collection_phonearea.distinct(
                    'state', {'phoneprefix': dest[:5]})
                # print(get_home,"------get home")
            unique_states.update(get_home)

        # unique_state_count = len(unique_states)
        dest_count = get_dest
        get_home = self.collection_cdrdata.distinct(
            'destination_number', {'source_number': data})

        dest_all_num = []
        phoneprefix = self.collection_phonearea.distinct('phoneprefix')

        for num in get_home:
            # print(num,len(num))
            if len(num) > 5 and num[:5] not in phoneprefix:
                dest_all_num.append(num)

        return unique_states, dest_count, dest_all_num

    def other_states(self, data, states):
        print(data, states, "________________________")
        get_state = states.split(",")
        pipeline = [
            {'$match': {'source_number': data}},
            {'$group': {'_id': '$destination_number', 'count': {'$sum': 1}}}
        ]

        result = self.collection_cdrdata.aggregate(pipeline)
        print(result, "result")
        state_counts = {}
        # Dictionary to store matching unique destination_numbers for each state
        state_destinations = {}

        for entry in result:
            print(entry)
            destination_number = entry['_id']
            match_query = {'source_number': data,
                           'state_key': {'$in': get_state}}
            matched_states = self.collection_sdrdata.distinct(
                'state_key', match_query)
            if not matched_states:
                # If state_key does not match, check the phone collection
                phone_match_query = {
                    'phone': destination_number, 'state': {'$in': get_state}}
                matched_states = self.collection_phonearea.distinct(
                    'state', phone_match_query)
            if matched_states:
                for state in matched_states:
                    state_counts[state] = state_counts.get(
                        state, 0) + entry['count']
                    state_destinations.setdefault(
                        state, set()).add(destination_number)

        data_dict = []
        for state, dest_numbers in state_destinations.items():
            # Count unique destination numbers
            dest_count_list = list(dest_numbers)
            # print(dest_count_list)
            data_dict.append({'state': state, 'dest_count': dest_count_list})

        headers = ['state', 'dest_count']
        response = {'headers': headers, 'data_dict': data_dict}
        print(response, "response")
        return response

    def dest_count(self, data, dest):
        print(data, dest, "inside")
        dest = dest.split(",")
        cdr_data = []
        for destination_number in dest:
            query = {
                'source_number': data,
                'destination_number': destination_number
            }
            result = self.collection_cdrdata.find(query)
            result = self.collection_cdrdata.find(query)
            logger.info("interation started...")
            for document in result:
                destination_number = document['destination_number']
                call_type = document['call_type']
                call_type = document['call_type']
                duration = document['duration']
                cellid = document['first_cgid']
                provider = document['provider']
                roaming = document['roaming_circle']
                calldate = datetime.fromtimestamp(
                    document['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                cellid_match = self.collection_cellid.find_one(
                    {'celltowerid': cellid})
                if cellid_match:
                    address = cellid_match.get('siteaddress')
                    lat = cellid_match.get('lat')
                    long = cellid_match.get('long')
                    azimuth = cellid_match.get('azimuth')
                else:
                    address = ""
                    lat = 0.0
                    long = 0.0
                    azimuth = 0
                sdrfinds = self.collection_sdrdata.find_one(
                    {'source_number': destination_number})
                nickname = [nickname.get('nickname', 'not available') for nickname in self.collection_suspect.find(
                    {'phone': document['destination_number']}, {'_id': 0}).sort('timestamp', pymongo.ASCENDING).limit(-1)]
                if sdrfinds is not None:
                    adresssdr = sdrfinds.get('local_address', '')
                cdr = {
                    'source_number': data,
                    'destination_number': destination_number,
                    'nickname': nickname,
                    'calldate': calldate,
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
                cdr_data.append(cdr)
        headers = [k for k in cdr_data[0].keys()] if cdr_data else []
        response = {'headers': headers, 'data_dict': cdr_data}
        return response

    def contact_info(self, data):  # 6372621003
        home_circle, total_contacts, isd_contacts = self.dest_contact(data)
        home_circle = list(home_circle)
        # print(home_circle)
        output = {}
        outputlist = []
        # , 'call_type': {'$in': ['call_in', 'call_out']}})
        get_data = self.collection_cdrdata.find({'source_number': data})
        get_data_count = self.collection_cdrdata.count_documents(
            {'source_number': data})
        get_sdr_data = self.collection_sdrdata.find_one(
            {'source_number': data})
        sdr_address = [address_phone['areadescription']
                       for address_phone in self.collection_phonearea.find({'phoneprefix': data[:5]})]
        sdr_nickname = "Not Available"
        sdr_fullname = "Not Available"
        if get_sdr_data is not None:
            sdr_address = get_sdr_data['local_address']
            sdr_fullname = get_sdr_data['fullname']

        if get_data_count == 0:

            headers = ['source_number', 'total_calls', 'cdat_count', 'duration', 'roaming_circle', 'imei',
                       'call_start_date', 'call_end_date', 'address', 'last_updated', 'nickname', 'provider']
            response = {'headers': headers, 'data_dict': "Not data Matched"}
            return response
        else:
            print(get_data_count, "-------count--------")
            imei_value = []
            logger.info(" loop starts")
            for value in get_data:
                # dest.append(value['destination_number'])
                if value['source_number'] == data:
                    output['number'] = data
                    if value['imei'] not in imei_value:
                        imei_value.append(value['imei'])
                    output['other_states'] = home_circle

                    output['imei'] = imei_value
                if value['destination_number'] == data:
                    output['number'] = data
                output['provider'] = value['provider']
                output['address'] = f'Name: {sdr_fullname}, {sdr_address}'
                output['total_contacts'] = total_contacts
            logger.info("Loop ends")

            output['nickname'] = [nickname.get('nickname', '') for nickname in self.collection_suspect.find(
                {'phone': data}, {'_id': 0}).sort('timestamp', pymongo.ASCENDING).limit(-1)]
            # list(self.unique_numbers)
            output['cdat_count'] = list(self.cdat_count(data))
            output['total_contacts'] = list(set(total_contacts))
            output['module'] = [module['module_name'] for module in self.collection_suspect.find(
                {'phone': data}).sort('timestamp', pymongo.DESCENDING).limit(1)]
            output['org'] = [org['organization'] for org in self.collection_suspect.find(
                {'phone': data}).sort('timestamp', pymongo.DESCENDING).limit(1)]
            output['cat'] = [cat['category'] for cat in self.collection_suspect.find(
                {'phone': data}).sort('timestamp', pymongo.DESCENDING).limit(1)]
            output['io_name'] = [io_name['inc_officer'] for io_name in self.collection_suspect.find(
                {'phone': data}).sort('timestamp', pymongo.DESCENDING).limit(1)]
            output['isd_count'] = isd_contacts
            logger.info("timestamp starts")
            output['last_updated'] = [last_update['as_on_date'] for last_update in self.collection_cdrdata.find(
                {'source_number': data}).sort('timestamp', pymongo.DESCENDING).limit(1)]
            output['call_start_date'] = [datetime.fromtimestamp(st_date['timestamp']).strftime(
                '%Y-%m-%d %H:%M:%S') for st_date in self.collection_cdrdata.find({'source_number': data}).sort('timestamp', pymongo.ASCENDING).limit(1)]
            output['call_end_date'] = [datetime.fromtimestamp(en_dt['timestamp']).strftime(
                '%Y-%m-%d %H:%M:%S') for en_dt in self.collection_cdrdata.find({'source_number': data}).sort('timestamp', pymongo.DESCENDING).limit(1)]
            logger.info("timestamp ends")

            outputlist.append(output)
            headers = ['number', 'total_contacts', 'cdat_count', 'other_states', 'imei', 'call_start_date',
                       'call_end_date', 'nickname', 'cat', 'module', 'org', 'last_updated', 'address', 'provider', 'io_name', 'caf']
            response = {'headers': headers, 'data_dict': outputlist}
            # print(response)
            return response

    def cdr_profile(self, data):
        ft = time.time()
        time1 = {'title':'Functions starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time()}
        pipeline = [
            {
                "$match": {
                    "source_number": data,
                    'destination_number': {
                        '$regex': '^(91\\d{10}|\\d{10})$'
                    }
                }
            },
            {
                "$group": {
                    "_id": '$source_number',
                    "start_date": {"$min": {"$dateFromString": {"dateString": "$date", "format": "%d-%m-%Y"}}},
                    "last_updated_date": {"$max": "$as_on_date"},
                    "end_date": {"$max": {"$dateFromString": {"dateString": "$date", "format": "%d-%m-%Y"}}},
                    "dates": {"$addToSet": {"$dateFromString": {"dateString": "$date", "format": "%d-%m-%Y"}}},
                    "incoming_calls": {
                        "$sum": {
                            "$switch": {
                                "branches": [
                                    {"case": {
                                        "$eq": ["$incoming", 1]}, "then": 1},
                                    {"case": {
                                        "$eq": ["$incoming", 0]}, "then": 0}
                                ],
                                "default": 0
                            }
                        }
                    },
                    "outgoing_calls": {
                        "$sum": {
                            "$switch": {
                                "branches": [
                                    {"case": {
                                        "$eq": ["$incoming", 0]}, "then": 1},
                                    {"case": {
                                        "$eq": ["$incoming", 1]}, "then": 0}
                                ],
                                "default": 0
                            }
                        }
                    },
                    "total_duration": {"$sum": "$duration"},
                    "unique_destination_numbers": {"$addToSet": "$destination_number"},
                    "roaming_state": {"$addToSet": "$state"},
                    "total_imei": {"$addToSet": "$imei"},
                    "total_provider": {"$addToSet": "$provider"},
                    "documents": {"$push": "$$ROOT"}
                }
            },
            {
                "$addFields": {
                    "one_to_one_call": {
                        "$eq": [{"$size": "$unique_destination_numbers"}, 1]
                    },
                    "only_sms": {
                        "$size": {
                            "$filter": {
                                "input": "$documents",
                                "as": "doc",
                                "cond": {"$eq": ["$$doc.duration", 0]}
                            }
                        }
                    },
                    "no_transaction_calls": {
                        "$eq": [{"$sum": "$documents.duration"}, 0]
                    },
                    "total_present_dates": {"$size": "$dates"}
                }
            },
            {
                "$lookup": {
                    "from": "cdat_suspect",
                    "let": {"source_number": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {"$eq": ["$phone", "$$source_number"]}
                            }
                        }
                    ],
                    "as": "suspectData"
                }
            },
            {
                "$unwind": {
                    "path": "$suspectData",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$lookup": {
                    "from": "cdat_sdr",
                    "let": {"source_number": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {"$eq": ["$source_number", "$$source_number"]}
                            }
                        }
                    ],
                    "as": "sdrData"
                }
            },
            {
                "$unwind": {
                    "path": "$sdrData",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source_number": data,
                    "nickname": {"$ifNull": ["$suspectData.nickname", "Unknown"]},
                    "local_address": {"$ifNull": ["$sdrData.local_address", "no address found"]},
                    "permanent_address": {"$ifNull": ["$sdrData.permanent_address", "no address found"]},
                    "start_date": {"$dateToString": {"format": "%d-%m-%Y", "date": "$start_date"}},
                    "end_date": {"$dateToString": {"format": "%d-%m-%Y", "date": "$end_date"}},
                    "total_present_dates": 1,
                    # "silent_days_count": {"$subtract": [{"$size": "$dates"}, "$total_present_dates"]},
                    "silent_days_count": {
                        "$subtract": [
                            {"$divide": [{"$subtract": ["$end_date", "$start_date"]}, 86400000]}, 
                            "$total_present_dates"
                        ]
                    },
                    "incoming_calls": 1,
                    "outgoing_calls": 1,
                    "total_duration": 1,
                    "unique_destination_number_count": "$unique_destination_numbers",
                    "roaming_state": "$roaming_state",
                    "total_imei": "$total_imei",
                    "total_provider": "$total_provider",
                    "only_sms": 1,
                    "no_transaction_calls": 1,
                    "one_to_one_call": 1,
                    "last_updated_date": {"$dateToString": {"format": "%d-%m-%Y %H:%M:%S", "date": "$last_updated_date"}},
                }
            }

        ]

        # Execute the aggregation pipeline
        time2 = {'title':'Profile Aggrgation starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'),'timestamp':time.time()}
        result = list(self.collection_cdrdata.aggregate(pipeline))
        time3 = {'title':'Profile Aggregation ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'),'querytime':time.time() - time2['timestamp']}
        time4 = {'title':"cdat_count_check starts",'time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'),'timestamp':time.time()}
        count_cdat = self.cdat_count(data)
        time5 = {'title':"cdat_count_check ends",'time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'),'querytime':time.time() -time4['timestamp']}

        print(count_cdat,"-=====--------")
        cdat = count_cdat#[0]['destination_numbers'] if len(count_cdat) > 0 else []
        first_dict = result[0] if result else {}
        first_dict['cdat_count'] = cdat if len(cdat) > 0 else []
        # result.append({'cdat_count':cdat})
        # pprint(result)
        time6 = {'title':'function ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'),'timestamp':time.time() - ft}
        if len(result) > 0:
            response = {'data_dict': result, 'status': 'success',
                        'message': 'data retrived successfully','times':[time1,time2,time3,time4,time5,time6]}
        else:
            response = {'data_dict': 'No data Matched',
                        'status': 'failure', 'message': ' no data found','times':[]}
        return response

    def single_number_profile(self, data, fromdate=None, todate=None):

        if fromdate is not None and todate is not None:
            match_stage = {
                "$match":  {
                    'source_number': data,
                    'timestamp': {
                        '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                        '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()},
                    '$or': [{'destination_number': {'$regex': '^[0-9]{0,10}$'}},
                            {'$and': [{'destination_number': {
                                '$regex': '^[0-9]{10}$'}}, {'duration': {'$gt': 0}}]},
                            {'destination_number': {'$exists': False}}
                            ]
                }
            }
        else:
            match_stage = {
                "$match": {
                    "source_number": data,
                    'destination_number': {
                        '$regex': '^(91\\d{10}|\\d{10})$'
                    }
                }
            }

        pipeline = [
            match_stage,
            {
                "$group": {
                    "_id": '$source_number',
                    "start_date": {"$min": {"$dateFromString": {"dateString": "$date", "format": "%d-%m-%Y"}}},
                    "last_updated_date": {"$max": "$as_on_date"},
                    "end_date": {"$max": {"$dateFromString": {"dateString": "$date", "format": "%d-%m-%Y"}}},
                    "dates": {"$addToSet": {"$dateFromString": {"dateString": "$date", "format": "%d-%m-%Y"}}},
                    "incoming_calls": {
                        "$sum": {
                            "$switch": {
                                "branches": [
                                    {"case": {
                                        "$eq": ["$incoming", 1]}, "then": 1},
                                    {"case": {
                                        "$eq": ["$incoming", 0]}, "then": 0}
                                ],
                                "default": 0
                            }
                        }
                    },
                    "outgoing_calls": {
                        "$sum": {
                            "$switch": {
                                "branches": [
                                    {"case": {
                                        "$eq": ["$incoming", 0]}, "then": 1},
                                    {"case": {
                                        "$eq": ["$incoming", 1]}, "then": 0}
                                ],
                                "default": 0
                            }
                        }
                    },
                    "total_duration": {"$sum": "$duration"},
                    "unique_destination_numbers": {"$addToSet": "$destination_number"},
                    "roaming_state": {"$addToSet": "$state"},
                    "total_imei": {"$addToSet": "$imei"},
                    "total_provider": {"$addToSet": "$provider"},
                    "documents": {"$push": "$$ROOT"}
                }
            },
            {
                "$addFields": {
                    "one_to_one_call": {
                        "$eq": [{"$size": "$unique_destination_numbers"}, 1]
                    },
                    "only_sms": {
                        "$size": {
                            "$filter": {
                                "input": "$documents",
                                "as": "doc",
                                "cond": {"$eq": ["$$doc.duration", 0]}
                            }
                        }
                    },
                    "no_transaction_calls": {
                        "$eq": [{"$sum": "$documents.duration"}, 0]
                    },
                    "total_present_dates": {"$size": "$dates"}
                }
            },
            {
                "$lookup": {
                    "from": "cdat_suspect",
                    "let": {"source_number": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {"$eq": ["$phone", "$$source_number"]}
                            }
                        }
                    ],
                    "as": "suspectData"
                }
            },
            {
                "$unwind": {
                    "path": "$suspectData",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$lookup": {
                    "from": "cdat_sdr",
                    "let": {"source_number": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {"$eq": ["$source_number", "$$source_number"]}
                            }
                        }
                    ],
                    "as": "sdrData"
                }
            },
            {
                "$unwind": {
                    "path": "$sdrData",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source_number": data,
                    "nickname": {"$ifNull": ["$suspectData.nickname", "Unknown"]},
                    "local_address": {"$ifNull": ["$sdrData.local_address", "no address found"]},
                    "permanent_address": {"$ifNull": ["$sdrData.permanent_address", "no address found"]},
                    "start_date": {"$dateToString": {"format": "%d-%m-%Y", "date": "$start_date"}},
                    "end_date": {"$dateToString": {"format": "%d-%m-%Y", "date": "$end_date"}},
                    "total_present_dates": 1,
                    "silent_days_count": {"$subtract": [{"$size": "$dates"}, "$total_present_dates"]},
                    "incoming_calls": 1,
                    "outgoing_calls": 1,
                    "total_duration": 1,
                    "unique_destination_number_count": "$unique_destination_numbers",
                    "roaming_state": "$roaming_state",
                    "total_imei": "$total_imei",
                    "total_provider": "$total_provider",
                    "only_sms": 1,
                    "no_transaction_calls": 1,
                    "one_to_one_call": 1,
                    "last_updated_date": {"$dateToString": {"format": "%d-%m-%Y %H:%M:%S", "date": "$last_updated_date"}},
                }
            }

        ]

        # Execute the aggregation pipeline
        result = list(self.collection_cdrdata.aggregate(pipeline))
        count_cdat = self.cdat_count(data)
        cdat = count_cdat#[0]['destination_numbers'] if count_cdat else []
        first_dict = result[0] if result else {}
        first_dict['cdat_count'] = cdat if len(cdat) > 0 else []
        # result.append({'cdat_count':cdat})
        pprint(result)
        if len(result) > 0:
            response = {'data_dict': result, 'status': 'success',
                        'message': 'data retrived successfully'}
        else:
            response = {'data_dict': 'No data Matched',
                        'status': 'failure', 'message': ' no data found'}
        return response

    def analysis_profile(self, data, fromdate=None, todate=None):
        print("multiple", data, fromdate, todate)
        phone_numbers = data.split(',')
        result_list = []
        for num in phone_numbers:
            if fromdate is not None and todate is not None:
                match_stage = {
                    "$match":  {
                        'source_number': num,
                        'timestamp': {
                            '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                            '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()},
                        '$or': [{'destination_number': {'$regex': '^[0-9]{0,10}$'}},
                                {'$and': [{'destination_number': {
                                    '$regex': '^[0-9]{10}$'}}, {'duration': {'$gt': 0}}]},
                                {'destination_number': {'$exists': False}}
                                ]
                    }
                }
            else:
                match_stage = {
                    "$match": {
                        "source_number": num,
                        'destination_number': {
                            '$regex': '^(91\\d{10}|\\d{10})$'
                        }
                    }
                }

            pipeline = [
                match_stage,
                {
                    "$group": {
                        "_id": '$source_number',
                        "start_date": {"$min": {"$dateFromString": {"dateString": "$date", "format": "%d-%m-%Y"}}},
                        "last_updated_date": {"$max": "$as_on_date"},
                        "end_date": {"$max": {"$dateFromString": {"dateString": "$date", "format": "%d-%m-%Y"}}},
                        "dates": {"$addToSet": {"$dateFromString": {"dateString": "$date", "format": "%d-%m-%Y"}}},
                        "incoming_calls": {
                            "$sum": {
                                "$switch": {
                                    "branches": [
                                        {"case": {
                                            "$eq": ["$incoming", 1]}, "then": 1},
                                        {"case": {
                                            "$eq": ["$incoming", 0]}, "then": 0}
                                    ],
                                    "default": 0
                                }
                            }
                        },
                        "outgoing_calls": {
                            "$sum": {
                                "$switch": {
                                    "branches": [
                                        {"case": {
                                            "$eq": ["$incoming", 0]}, "then": 1},
                                        {"case": {
                                            "$eq": ["$incoming", 1]}, "then": 0}
                                    ],
                                    "default": 0
                                }
                            }
                        },
                        "total_duration": {"$sum": "$duration"},
                        "unique_destination_numbers": {"$addToSet": "$destination_number"},
                        "roaming_state": {"$addToSet": "$state"},
                        "total_imei": {"$addToSet": "$imei"},
                        "total_provider": {"$addToSet": "$provider"},
                        "documents": {"$push": "$$ROOT"}
                    }
                },
                {
                    "$addFields": {
                        "one_to_one_call": {
                            "$eq": [{"$size": "$unique_destination_numbers"}, 1]
                        },
                        "only_sms": {
                            "$size": {
                                "$filter": {
                                    "input": "$documents",
                                    "as": "doc",
                                    "cond": {"$eq": ["$$doc.duration", 0]}
                                }
                            }
                        },
                        "no_transaction_calls": {
                            "$eq": [{"$sum": "$documents.duration"}, 0]
                        },
                        "total_present_dates": {"$size": "$dates"}
                    }
                },
                {
                    "$lookup": {
                        "from": "cdat_suspect",
                        "let": {"source_number": "$_id"},
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {"$eq": ["$phone", "$$source_number"]}
                                }
                            }
                        ],
                        "as": "suspectData"
                    }
                },
                {
                    "$unwind": {
                        "path": "$suspectData",
                        "preserveNullAndEmptyArrays": True
                    }
                },
                {
                    "$lookup": {
                        "from": "cdat_sdr",
                        "let": {"source_number": "$_id"},
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {"$eq": ["$source_number", "$$source_number"]}
                                }
                            }
                        ],
                        "as": "sdrData"
                    }
                },
                {
                    "$unwind": {
                        "path": "$sdrData",
                        "preserveNullAndEmptyArrays": True
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "source_number": num,
                        "nickname": {"$ifNull": ["$suspectData.nickname", "Unknown"]},
                        "local_address": {"$ifNull": ["$sdrData.local_address", "no address found"]},
                        "permanent_address": {"$ifNull": ["$sdrData.permanent_address", "no address found"]},
                        "start_date": {"$dateToString": {"format": "%d-%m-%Y", "date": "$start_date"}},
                        "end_date": {"$dateToString": {"format": "%d-%m-%Y", "date": "$end_date"}},
                        "total_present_dates": 1,
                        "silent_days_count": {"$subtract": [{"$size": "$dates"}, "$total_present_dates"]},
                        "incoming_calls": 1,
                        "outgoing_calls": 1,
                        "total_duration": 1,
                        "unique_destination_number_count": "$unique_destination_numbers",
                        "roaming_state": "$roaming_state",
                        "total_imei": "$total_imei",
                        "total_provider": "$total_provider",
                        "only_sms": 1,
                        "no_transaction_calls": 1,
                        "one_to_one_call": 1,
                        "last_updated_date": {"$dateToString": {"format": "%d-%m-%Y %H:%M:%S", "date": "$last_updated_date"}},
                    }
                }

            ]

            # Execute the aggregation pipeline
            result = list(self.collection_cdrdata.aggregate(pipeline))
            count_cdat = self.cdat_count(phone_numbers)
            pprint(count_cdat,"==================")
            cdat = count_cdat#[0]['destination_numbers'] if count_cdat else []
            first_dict = result[0] if result else {}
            first_dict['cdat_count'] = cdat if len(cdat)>0 else []
            result_list.append(result)
        # result.append({'cdat_count':cdat})
        # pprint(result)
        if len(result) > 0:
            response = {'data_dict': result_list, 'status': 'success',
                        'message': 'data retrived successfully'}
        else:
            response = {'data_dict': 'No data Matched',
                        'status': 'failure', 'message': ' no data found'}
        return response

    def cdat_count_old(self, number):
        pipeline = [
            {
                "$match": {
                    "source_number": number,
                    'destination_number': {
                        '$regex': '^(91\\d{10}|\\d{10})$'
                    }
                }
            },
            {
                "$group": {
                    "_id": "$destination_number",
                    "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "destination_number": "$_id",
                    "count": 1
                }
            },
            {
                "$lookup": {
                    "from": "cdat_cdr",
                    "let": {"destination_number": "$destination_number"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$and": [
                                        {"$ne": ["$source_number", number]},
                                        {"$eq": ["$source_number",
                                                 "$$destination_number"]}
                                    ]
                                }
                            }
                        }
                    ],
                    "as": "matched_documents"
                }
            },
            {"$unwind": "$matched_documents"},
            {
                "$group": {
                    "_id": "$destination_number",
                    "count": {"$first": "$count"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "destination_number": "$_id"
                }
            },
            {
                "$group": {
                    "_id": 0,
                    "destination_numbers": {"$push": "$destination_number"}
                }
            }
        ]

        result = list(self.collection_cdrdata.aggregate(pipeline))
        print(result)
        return result

    def convert_size(cls, size_bytes):
        # print(size_bytes, "inside convert")
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def ipdr_profile(self, data):

        summary = {}
        if self.collection_ipdr.count_documents({'msisdn': data}) == 0:
            response = {'summary': 'no data',
                        'status': 'empty', 'message': "no data found"}
            return response

        allvpn_pipeline = [
            {
                "$match": {
                    "msisdn": data,
                    "is_vpn": 1
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "vpn": "$vpn",
                    "msisdn": 1,
                    "vpn_ip": "$destination_ip",
                    "downlink_vol": 1,
                    "uplink_vol": 1,
                    "start_time": "$time",
                    "end_time": "$time_et"
                }
            }
        ]
        query = self.collection_ipdr.aggregate(allvpn_pipeline)
        results = list(query)
        allvpn = []
        for doc in results:
            dwnLink = int(
                doc['downlink_vol']) if doc['downlink_vol'] != "None" and doc['downlink_vol'] != "" else 0
            upLink = int(
                doc['uplink_vol']) if doc['uplink_vol'] != "None" and doc['uplink_vol'] != "" else 0
            downlink_vol = self.convert_size(dwnLink)
            uplink_vol = self.convert_size(upLink)
            start_time = doc['start_time']
            end_time = doc['end_time']
            duration = end_time - start_time
            allvpn.append({
                "MSISDN": doc['msisdn'],
                "VPN": doc['vpn'],
                "VPN_IP": doc['vpn_ip'],
                "downlink_vol": downlink_vol,
                "uplink_vol": uplink_vol,
                "start_time": doc['start_time'],
                "end_time": doc['end_time'],
                "duration": str(duration)
            })

        vpn_pipeline = [
            {
                "$match": {
                    "is_vpn": 1,
                    "msisdn": data,
                    "destination_ip": {"$ne": None,
                                       "$ne": ""}
                }
            },
            {
                "$group": {
                    "_id": {
                        "vpn": "$vpn",
                        "msisdn": "$msisdn",
                        "destination_ip": "$destination_ip"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$group": {
                    "_id": {
                        "vpn_name": "$_id.vpn",
                        "vpn_msisdn": "$_id.msisdn"
                    },
                    "count_of _unique_destination_ips_of_vpn": {"$sum": 1},
                    "destination_ips_of_vpn": {
                        "$push": {
                            "ip": "$_id.destination_ip",
                            "count": "$count"
                        }
                    },
                    "total_destination_ips_count_of_vpn": {"$sum": "$count"},
                }
            },
            {
                "$sort": {"total_destination_ips_count_of_vpn": -1}
            }
        ]
        query = self.collection_ipdr.aggregate(vpn_pipeline)
        results = list(query)
        vpn = []
        for doc in results:
            vpn.append({
                "MSISDN_VPN": doc['_id']['vpn_msisdn'],
                "VPN": doc['_id']['vpn_name'],
                "count_of _unique_destination_ips_of_vpn": doc['count_of _unique_destination_ips_of_vpn'],
                "destination_ips_of_vpn": doc['destination_ips_of_vpn'],
                "total_destination_ips_count_of_vpn": doc['total_destination_ips_count_of_vpn'],
            })
        # print(vpn[:5])

        country_pipeline = [
            {
                "$match": {
                    "country": {"$ne": None},
                    "msisdn": data,
                    "destination_ip": {
                        "$ne": None,
                        "$ne": ""
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "country": "$country",
                        "msisdn": "$msisdn",
                        "destination_ip": "$destination_ip"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$group": {
                    "_id": {
                        "country": "$_id.country",
                        "country_msisdn": "$_id.msisdn"
                    },
                    "count_of_unique_destination_ips_of_country": {"$sum": 1},
                    "destination_ips_of_country": {
                        "$push": {
                            "ip": "$_id.destination_ip",
                            "count": "$count"
                        }
                    },
                    "total_destination_ips_count_of_country": {"$sum": "$count"},

                }
            },
            {
                "$sort": {"total_destination_ips_count_of_country": -1}
            }
        ]
        query2 = self.collection_ipdr.aggregate(country_pipeline)
        results2 = list(query2)
        country = []
        for doc in results2:
            country.append({
                "MSISDN_COUNTRY": doc['_id']['country_msisdn'],
                "COUNTRY": doc['_id']['country'],
                "count_of_unique_destination_ips_of_country": doc['count_of_unique_destination_ips_of_country'],
                "destination_ips_of_country": doc['destination_ips_of_country'],
                "total_destination_ips_count_of_country": doc['total_destination_ips_count_of_country'],
            })
        app_pipeline = [
            {
                "$match": {
                    "company": {"$ne": None},
                    "msisdn": data,
                    "destination_ip": {
                        "$ne": None,
                        "$ne": ""
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "company": "$company",
                        "msisdn": "$msisdn",
                        "destination_ip": "$destination_ip"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$group": {
                    "_id": {
                        "app": "$_id.company",
                        "app_msisdn": "$_id.msisdn"
                    },
                    "count_of_unique_destination_ips_of_app": {"$sum": 1},
                    "destination_ips_of_app": {
                        "$push": {
                            "ip": "$_id.destination_ip",
                            "count": "$count"
                        }
                    },
                    "total_destination_ips_count_of_app": {"$sum": "$count"},
                }
            },
            {
                "$sort": {"total_destination_ips_count_of_app": -1}
            }
        ]
        query3 = self.collection_ipdr.aggregate(app_pipeline)
        results3 = list(query3)

        app = []
        for doc in results3:
            app.append({
                "MSISDN_APP": doc['_id']['app_msisdn'],
                "APP": doc['_id']['app'],
                "count_of_unique_destination_ips_of_app": doc['count_of_unique_destination_ips_of_app'],
                "destination_ips_of_app": doc['destination_ips_of_app'],
                "total_destination_ips_count_of_app": doc['total_destination_ips_count_of_app'],
            })
        device_pipeline = [
            {
                "$match": {
                    "msisdn": data
                }
            },
            {
                "$group": {
                    "_id": "$imei",
                    "count": {"$sum": 1},
                    "min_date": {"$min": "$time"},
                    "max_date": {"$max": "$end_time"}
                }
            }
        ]
        query = self.collection_ipdr.aggregate(device_pipeline)
        device_results = list(query)

        isp_pipeline = [
            {
                '$match': {
                    'msisdn': data,
                    'com_type': 'isp',
                    'country': 'India'
                }
            },
            {
                '$group': {
                    '_id': '$destination_ip',
                    'vendor': {'$first': '$asn'},
                    'downlink_vol': {'$first': '$downlink_vol'},
                    'uplink_vol': {'$first': '$uplink_vol'},
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'ip': '$_id',
                    'vendor': 1,
                    'downlink_vol': 1,
                    'uplink_vol': 1
                }
            }
        ]

        query5 = self.collection_ipdr.aggregate(isp_pipeline)
        result5 = list(query5)

        isp_india = []
        for doc in result5:
            # print(doc,"indian isp doc")
            try:
                if 'downlink_vol' in doc and 'uplink_vol' in doc:
                    dwnLink = int(
                        doc['downlink_vol']) if doc['downlink_vol'] != "None" and doc['downlink_vol'] != "" else 0
                    upLink = int(
                        doc['uplink_vol']) if doc['uplink_vol'] != "None" and doc['uplink_vol'] != "" else 0
                    total_usage = upLink + dwnLink
                    usage = self.convert_size(total_usage)

                    isp_india.append({
                        "ip": doc['ip'],
                        "vendor": doc['vendor'],
                        "usage": usage
                    })
            except Exception as e:
                print(f" error in isp query :{e}")

        foreign_isp_pipeline = [
            {
                '$match': {
                    'msisdn': data,
                    'com_type': 'isp',
                    'country': {'$ne': 'India'}
                }
            },
            {
                '$group': {
                    '_id': '$destination_ip',
                    'vendor': {'$first': '$asn'},
                    'country': {'$first': '$country'},
                    'downlink_vol': {'$first': '$downlink_vol'},
                    'uplink_vol': {'$first': '$uplink_vol'}
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'ip': '$_id',
                    'vendor': 1,
                    'country': 1,
                    'downlink_vol': 1,
                    'uplink_vol': 1,
                }
            }
        ]

        query6 = self.collection_ipdr.aggregate(foreign_isp_pipeline)
        result6 = list(query6)

        foreign_isp = []
        for doc in result6:
            dwnLink = int(
                doc['downlink_vol']) if doc['downlink_vol'] != "None" and doc['downlink_vol'] != "" else 0
            upLink = int(
                doc['uplink_vol']) if doc['uplink_vol'] != "None" and doc['uplink_vol'] != "" else 0
            total_usage = upLink + dwnLink
            usage = self.convert_size(total_usage)
            foreign_isp.append({
                "ip": doc['ip'],
                "vendor": doc['vendor'],
                "country": doc['country'],
                "usage": usage
            })

        iptype_pipeline = [
            {
                "$match": {
                    "com_type": {"$ne": None},
                    "msisdn": data,
                    "destination_ip": {
                        "$ne": None,
                        "$ne": ""
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "ip_type": "$com_type",
                        "msisdn": "$msisdn",
                        "destination_ip": "$destination_ip"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$group": {
                    "_id": {
                        "ip_type": "$_id.ip_type",
                        "iptype_msisdn": "$_id.msisdn"
                    },
                    "count_of_unique_destination_ips_of_iptype": {"$sum": 1},
                    "destination_ips_of_iptype": {
                        "$push": {
                            "ip": "$_id.destination_ip",
                            "count": "$count"
                        }
                    },
                    "total_destination_ips_count_of_iptype": {"$sum": "$count"},

                }
            },
            {
                "$sort": {"total_destination_ips_count_of_iptype": -1}
            }
        ]

        query4 = self.collection_ipdr.aggregate(iptype_pipeline)
        results4 = list(query4)

        iptype = []
        for doc in results4:
            iptype.append({
                "MSISDN_IPTYPE": doc['_id']['iptype_msisdn'],
                "IPTYPE": doc['_id']['ip_type'],
                "count_of_unique_destination_ips_of_iptype": doc['count_of_unique_destination_ips_of_iptype'],
                "destination_ips_of_iptype": doc['destination_ips_of_iptype'],
                "total_destination_ips_count_of_iptype": doc['total_destination_ips_count_of_iptype'],
            })

        voip_pipeline = [
            {
                "$match": {
                    "msisdn": data,
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "msisdn": 1,
                    "source_ip": "$source_ip",
                    "destination_ip": "$destination_ip",
                    "time": "$time",
                    "end_time": "$end_time",
                    # "same_handshake": "$matched_handshake",
                    "vendor": "$vendor",
                    # "app": "$app",
                    "cellid": "$cellid",
                    "roaming": "$home_circle",
                    # "ip_type": "$ip_type",
                    "ipinfo": "$ipinfo"
                }},
            {
                "$sort": {
                    # "same_handshake": 1,
                    "time": 1
                }
            }
        ]

        query7 = self.collection_voip.aggregate(voip_pipeline)
        results7 = list(query7)
        voip = []
        for doc in results7:
            start_time = doc['time']
            end_time = doc['end_time']
            duration = end_time - start_time
            voip.append({
                "source_ip": doc['source_ip'],
                "destination_ip": doc['destination_ip'],
                "msisdn": doc['msisdn'],
                "start_time": doc['time'],
                "end_time": doc['end_time'],
                # "same_handshake": doc['same_handshake'],
                "vendor": doc['vendor'],
                "app": doc.get('app', ''),
                "cellid": doc['cellid'],
                "roaming": doc['roaming'],
                # "ip_type": doc['ip_type'],
                "ipinfo": doc['ipinfo'],
                "duration": str(duration)
            })

        matchedcall_pipeline = [{
            '$match': {
                "caller1": data
            }},
            {"$project": {
                '_id': 0,
                'caller1': 1,
                'caller2': '$caller2',
                'calltime': '$calltime',
                'destination_ip': '$destination_ip',
                'source_ip': '$source_ip'
            }}
        ]
        query8 = list(self.collection_matchedcall.aggregate(
            matchedcall_pipeline))
        matchedcall = []
        for doc in query8:
            matchedcall.append({
                "caller1": doc['caller1'],
                "caller2": doc['caller2'],
                "calltime": doc['calltime'],
                "destination_ip": doc['destination_ip'],
                "source_ip": doc['source_ip']
            })

        if data is not None:
            if vpn:
                highest_count_vpn = vpn[0]
                lowest_count_vpn = vpn[-1]
                highest_count_vpn_ip = highest_count_vpn['destination_ips_of_vpn'][0]['ip']
                lowest_count_vpn_ip = lowest_count_vpn['destination_ips_of_vpn'][0]['ip']
            else:
                highest_count_vpn = None
                lowest_count_vpn = None
                highest_count_vpn_ip = None
                lowest_count_vpn_ip = None
            total_unique_vpn_count = len(set(v['VPN'] for v in vpn))

            summary_vpn = {
                'data': data,
                'highest_count_vpn': highest_count_vpn,
                'highest_count_vpn_ip': highest_count_vpn_ip,
                'lowest_count_vpn': lowest_count_vpn,
                'lowest_count_vpn_ip': lowest_count_vpn_ip,
                'total_unique_vpn_count': total_unique_vpn_count
            }
            if app:
                highest_count_app = app[0]
                lowest_count_app = app[-1]
                highest_count_app_ip = highest_count_app['destination_ips_of_app'][0]['ip']
                lowest_count_app_ip = lowest_count_app['destination_ips_of_app'][0]['ip']
            else:
                highest_count_app = None
                lowest_count_app = None
                highest_count_app_ip = None
                lowest_count_app_ip = None
            total_unique_app_count = len(set(v['APP'] for v in app))

            summary_app = {
                'data': data,
                'highest_count_app': highest_count_app,
                'highest_count_app_ip': highest_count_app_ip,
                'lowest_count_app': lowest_count_app,
                'lowest_count_app_ip': lowest_count_app_ip,
                'total_unique_app_count': total_unique_app_count
            }
            if country:
                highest_count_country = country[0]
                lowest_count_country = country[-1]
                highest_count_country_ip = highest_count_country['destination_ips_of_country'][0]['ip']
                lowest_count_country_ip = lowest_count_country['destination_ips_of_country'][0]['ip']
            else:
                highest_count_country = None
                lowest_count_country = None
                highest_count_country_ip = None
                lowest_count_country_ip = None

            total_unique_country_count = len(
                set(v['COUNTRY'] for v in country))
            summary_country = {
                'data': data,
                'highest_count_country': highest_count_country,
                'highest_count_country_ip': highest_count_country_ip,
                'lowest_count_country': lowest_count_country,
                'lowest_count_country_ip': lowest_count_country_ip,
                'total_unique_country_count': total_unique_country_count
            }

            if iptype:
                highest_count_iptype = iptype[0]
                lowest_count_iptype = iptype[-1]
                highest_count_iptype_ip = highest_count_iptype['destination_ips_of_iptype'][0]['ip']
                lowest_count_iptype_ip = lowest_count_iptype['destination_ips_of_iptype'][0]['ip']
            else:
                highest_count_iptype = None
                lowest_count_iptype = None
                highest_count_iptype_ip = None
                lowest_count_iptype_ip = None
            total_unique_iptype_count = len(set(v['IPTYPE'] for v in iptype))
            summary_iptype = {
                'data': data,
                'highest_count_iptype': highest_count_iptype,
                'highest_count_iptype_ip': highest_count_iptype_ip,
                'lowest_count_iptype': lowest_count_iptype,
                'lowest_count_iptype_ip': lowest_count_iptype_ip,
                'total_unique_iptype_count': total_unique_iptype_count
            }

            summary = {'data': data,
                       'allvpn': allvpn,
                       'isp_india': isp_india,
                       'foreign_isp': foreign_isp,
                       'vpn': vpn,
                       'country': country,
                       'app': app,
                       'iptype': iptype,
                       'voip': voip,
                       'matchedcall': matchedcall,
                       'device': device_results,
                       'summary_app': summary_app,
                       'summary_country': summary_country,
                       'summary_vpn': summary_vpn,
                       'summary_iptype': summary_iptype,
                       'status': 'success',
                       'message': 'data retrived successfully'}

            return summary

    def tower_profile(self, data):
        match_conditions = {}

        match_conditions['source_number'] = data

        print(match_conditions)
        # print((list(self.collection_towerid.find(match_conditions))))
        pipeline = self.collection_towerid.aggregate([
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
                    "tower_count": {"$addToSet": "$sitename"},
                    "sector": {"$addToSet": "$first_cgid"},
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
                        "$sum": {"$cond": [{"$in": ["$call_type", ["call_out", "VOC"]]}, 1, 0]}
                    },
                    "total_smo_count": {
                        "$sum": {"$cond": [{"$in": ["$call_type", ["sms_out"]]}, 1, 0]}
                    },
                    "total_smt_count": {
                        "$sum": {"$cond": [{"$in": ["$call_type", ["sms_in"]]}, 1, 0]}
                    },
                    "validUnique": {
                        "$addToSet": {
                            "$cond": {
                                "if": {"$eq": ["$isValid", "valid"]},
                                "then": "$destination_number",
                                "else": "$$REMOVE"
                            }
                        }
                    },
                    "notValidUnique": {
                        "$addToSet": {
                            "$cond": {
                                "if": {"$eq": ["$isValid", "notValid"]},
                                "then": "$destination_number",
                                "else": "$$REMOVE"
                            }
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
                            "No calls"
                        ]
                    }
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
                    "imei": {"$first": "$imei_local"},
                    "tower": {"$first": "$tower_count"},
                    "sector": {"$first": "$sector"},
                    "ratio": {"$first": "$ratio"},
                    "nickname": {"$first": "$suspectData.nickname"},
                    "imei_count_cdr": {"$addToSet": "$cdrData.imei"},
                    "total_calls_count": {"$first": "$total_calls_count"},
                    "total_in_count": {"$first": "$total_in_count"},
                    "total_out_count": {"$first": "$total_out_count"},
                    "total_smo_count": {"$first": "$total_smo_count"},
                    "total_smt_count": {"$first": "$total_smt_count"},
                    "validUniqueCount": {"$first": "$validUnique"},
                    "notValidUniqueCount": {"$first": "$notValidUnique"}
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
                        ]
                    },
                    'ratio_sms': {
                        "$concat": [
                            {"$toString": "$total_smt_count"},
                            ":",
                            {"$toString": "$total_smo_count"}
                        ]
                    }
                }
            }
        ])

        info = list(pipeline)
        if len(info) > 0:
            response = {'data_dict': info, 'status': 'success',
                        'message': 'data retrived successfully'}
        else:
            response = {'data_dict': 'No data Matched',
                        'status': 'failure', 'message': 'no data found'}
        return response

    def cellid_info(self, data):
        output = {}
        outputlist = []
        get_data = self.db['cdrdata'].find({'first_cgid': data})
        callduration = 0
        callcount = 0
        for value in get_data:
            print(value)
            callcount = callcount+1
            callduration += value['duration']
            output['provider'] = value['provider']
            output['total_calls'] = callcount
            output['roaming_circle'] = self.roaming_count(
                value['roaming_circle'])
            output['imei'] = self.count_imei([value['imei']])
            output['total_call_duration'] = callduration
            output['Address'] = ""
            output['last_updated'] = ""
            output['nickname'] = ""
            output['cdat_count'] = self.cdat_count(value['destination_number'])
        outputlist.append(output)
        response = {'headers': [
            k for k in output.keys()], 'data_dict': outputlist}
        print(response)
        return response

    def call_in(self, calltype):

        if calltype == 'call_in':
            self.callin_count += 1
        if calltype == 'call_out':
            self.callout_count += 1
        return self.callin_count, self.callout_count

    def getsummary(self, data, mode, fromdate=False, todate=False, item=False, currentpage=False):
        time1 = datetime.now()
        print(data, type(currentpage), type(item), "first")
        # items_per_page = int(item)
        # current_page = int(currentpage)
        # skip_doc = int(items_per_page) *(int(current_page) - 1)
        # total_pages = self.collection_cdrdata.count_documents({'source_number': data})
        logger.info("profleinfo retriving")

        getprofile = self.contact_info(data)
        time2 = datetime.now()
        getdata = []
        query = {'source_number': data,
                 '$or': [{'destination_number': {'$regex': '^[0-9]{0,10}$'}},
                         {'$and': [{'destination_number': {
                             '$regex': '^[0-9]{10}$'}}, {'duration': {'$gt': 0}}]},
                         {'destination_number': {'$exists': False}}
                         ]
                 }
        # {'source_number': data}) #,'call_type':{'$in':['call_in','call_out']}})#.sort('timestamp',pymongo.ASCENDING).skip(skip_doc).limit(items_per_page)
        getdata.extend(self.collection_cdrdata.find(query))
        time3 = datetime.now()
        print(len(getdata))
        if len(getdata) == 0:
            response = {'header2': ['source_number', 'destination_number', 'nickname', 'call_in', 'call_out', 'total_calls', 'duration', 'first_call',
                                    'last_call', 'address'], 'data2': 'No Data', 'headers': '', 'data_dict': '', 'status': 'empty', 'message': 'no data found'}
            return response

        outputdict = {}
        logger.info("mongo retriving")
        time4 = datetime.now()
        for dest in getdata:
            # logger.info("Data rendering started")
            indiv_dest_number = []
            other_number = dest['destination_number'] if dest['source_number'] == data else dest['source_number']
            if other_number not in outputdict and (other_number.isdigit()):
                if not (len(other_number) < 10 and (int(dest['duration']) == 0)):
                    outputdict[other_number] = {'source_number': data, 'call_type': '', 'destination_number': other_number,
                                                'first_call': '', 'last_call': '', 'nickname': '', 'call_in': 0, 'call_out': 0, 'total_calls': 0, 'duration': 0}

                    if mode == "summary_new":

                        # ,'call_type':{'$in':['call_in','call_out']} })#.sort('timestamp',pymongo.ASCENDING).skip(skip_doc).limit(items_per_page)
                        indiv_dest_number = (self.collection_cdrdata.find(
                            {'source_number': data, 'destination_number': other_number}))

                    callduration = 0
                    callin_count = 0
                    callout_count = 0
                    first_call = None
                    last_call = None
                    for value in indiv_dest_number:

                        callduration += value['duration']
                        if value["incoming"] == 1:
                            callin_count += 1
                        elif value["incoming"] == 0:  # == 'call_out':
                            callout_count += 1

                        if first_call is None or value['timestamp'] < first_call:
                            first_call = value['timestamp']
                        if last_call is None or value['timestamp'] > last_call:
                            last_call = value['timestamp']

                        # outputdict[other_number]['address'] = value['first_cgid_address']

                    if isinstance(first_call, int):
                        first_call = datetime.fromtimestamp(
                            first_call).strftime('%Y-%m-%d %H:%M:%S')
                    if isinstance(last_call, int):
                        last_call = datetime.fromtimestamp(
                            last_call).strftime('%Y-%m-%d %H:%M:%S')

                    sdr_match = self.collection_sdrdata.find_one(
                        {'source_number': value['destination_number']})
                    nickname = [nickname.get('nickname', '') for nickname in self.collection_suspect.find(
                        {'phone': value['destination_number']}, {'_id': 0}).sort('timestamp', pymongo.ASCENDING).limit(-1)]
                    full_name = sdr_match.get('fullname') if sdr_match else ''
                    user_address = sdr_match.get(
                        'local_address') if sdr_match else ''
                    outputdict[other_number]['nickname'] = nickname
                    outputdict[other_number]['address'] = f'{full_name} {user_address}'
                    outputdict[other_number]['first_call'] = first_call
                    outputdict[other_number]['last_call'] = last_call
                    outputdict[other_number]['total_calls'] = callin_count + \
                        callout_count
                    outputdict[other_number]['duration'] = callduration
                    outputdict[other_number]['call_in'] = callin_count
                    outputdict[other_number]['call_out'] = callout_count

            # print(outputdict)
        time5 = datetime.now()
            # outputdict[other_number]['address'] = value['first_cgid_address']

        outputlist = list(outputdict.values())
        if mode == "total_calls":
            response = {'headers': [
                k for k in outputlist[0].keys()], 'data_dict': outputlist, 'status': 'success', 'message': 'data retrived successfully'}
        else:
            response = {'header2': ['source_number', 'destination_number', 'nickname', 'call_in', 'call_out', 'total_calls', 'duration', 'first_call',
                                    'last_call', 'address'], 'data2': outputlist, 'headers': getprofile['headers'], 'data_dict': getprofile['data_dict'], 'status': 'success', 'message': 'data retrived successfully'}
        return response

    def getsummary_between_dates(self, data, mode, fromdate=None, todate=None, item=False, currentpage=False):
        time1 = {'title':'function starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time() }
        print(data, type(currentpage), type(item), "first")
        # items_per_page = int(item)
        # current_page = int(currentpage)
        # skip_doc = int(items_per_page) *(int(current_page) - 1)
        # total_pages = self.collection_cdrdata.count_documents({'source_number': data})
        logger.info("profleinfo retriving")
        time2 = {'title':'Aggregation for cda profile starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time()}
        getprofile = self.cdr_profile(data)
        time3 = {'title':'Aggregation ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'querytime':time.time() - time2['timestamp']}

        getdata = []
        if fromdate is None and todate is None:
            query = {'source_number': data,
                     '$or': [{'destination_number': {'$regex': '^[0-9]{0,10}$'}},
                             {'$and': [{'destination_number': {
                                 '$regex': '^[0-9]{10}$'}}, {'duration': {'$gt': 0}}]},
                             {'destination_number': {'$exists': False}}
                             ]
                     }
        if fromdate is not None and todate is not None:
            query = {'source_number': data, 'timestamp': {
                '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()},
                '$or': [{'destination_number': {'$regex': '^[0-9]{0,10}$'}},
                        {'$and': [{'destination_number': {
                            '$regex': '^[0-9]{10}$'}}, {'duration': {'$gt': 0}}]},
                        {'destination_number': {'$exists': False}}
                        ]
            }

        # {'source_number': data}) #,'call_type':{'$in':['call_in','call_out']}})#.sort('timestamp',pymongo.ASCENDING).skip(skip_doc).limit(items_per_page)
        time4 = {'title':'Aggregation for contacts starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time()}
        getdata.extend(self.collection_cdrdata.find(query))
        time5 = {'title':'Aggregation ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'querytime':time.time() - time4['timestamp']}
        print(len(getdata))

        if len(getdata) == 0:
            response = {'header2': ['source_number', 'destination_number', 'nickname', 'call_in', 'call_out', 'total_calls', 'duration', 'first_call',
                                    'last_call', 'address'], 'data_dict': 'Not data Matched', 'status': 'empty', 'message': 'no data found','times':['nodata']}  # ,'totalpages':total_pages}
            return response

        outputdict = {}
        logger.info("mongo retriving")
        time6 = {'title':'Python iteration ends 3 mongo queries included','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time()}
        for dest in getdata:
            # logger.info("Data rendering started")
            indiv_dest_number = []
            other_number = dest['destination_number'] if dest['source_number'] == data else dest['source_number']
            if other_number not in outputdict and (other_number.isdigit()):
                if not (len(other_number) < 10 and (int(dest['duration']) == 0)):
                    # print(data, fromdate, todate, other_number, "inside")
                    if fromdate is None and todate is None:
                        indiv_dest_number_count = self.collection_cdrdata.count_documents(
                            {'source_number': data, 'destination_number': other_number})
                    if fromdate is not None and todate is not None:
                        indiv_dest_number_count = self.collection_cdrdata.count_documents({'source_number': data, 'destination_number': other_number, 'timestamp': {
                            '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                            '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                        }})
                        # print(indiv_dest_number_count)

                    if indiv_dest_number_count != 0:
                        outputdict[other_number] = {'source_number': data, 'call_type': '',
                                                    'destination_number': other_number, 'first_call': '', 'last_call': '', 'nickname': ''}
                        if fromdate is None and todate is None:
                            indiv_dest_number = self.collection_cdrdata.find(
                                {'source_number': data, 'destination_number': other_number})
                        if fromdate is not None and todate is not None:
                            indiv_dest_number = self.collection_cdrdata.find({'source_number': data, 'destination_number': other_number, 'timestamp': {
                                '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                                '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                            }})
                        # print(indiv_dest_number)
                        callduration = 0
                        callin_count = 0
                        callout_count = 0
                        first_call = None
                        last_call = None
                        for value in indiv_dest_number:

                            callduration += value['duration']
                            if value["incoming"] == 1:
                                callin_count += 1
                            elif value["incoming"] == 0:  # == 'call_out':
                                callout_count += 1

                            if first_call is None or value['timestamp'] < first_call:
                                first_call = value['timestamp']
                            if last_call is None or value['timestamp'] > last_call:
                                last_call = value['timestamp']

                            # outputdict[other_number]['address'] = value['first_cgid_address']

                        if isinstance(first_call, int):
                            first_call = datetime.fromtimestamp(
                                first_call).strftime('%Y-%m-%d %H:%M:%S')
                        if isinstance(last_call, int):
                            last_call = datetime.fromtimestamp(
                                last_call).strftime('%Y-%m-%d %H:%M:%S')

                        sdr_match = self.collection_sdrdata.find_one(
                            {'source_number': value['destination_number']})
                        nickname = [nickname.get('nickname', '') for nickname in self.collection_suspect.find(
                            {'phone': value['destination_number']}, {'_id': 0}).sort('timestamp', pymongo.ASCENDING).limit(-1)]
                        full_name = sdr_match.get(
                            'fullname') if sdr_match else ''
                        user_address = sdr_match.get(
                            'local_address') if sdr_match else ''
                        outputdict[other_number]['nickname'] = nickname
                        outputdict[other_number]['address'] = f'{full_name} {user_address}'
                        outputdict[other_number]['first_call'] = first_call
                        outputdict[other_number]['last_call'] = last_call
                        outputdict[other_number]['total_calls'] = callin_count + callout_count
                        outputdict[other_number]['duration'] = callduration
                        outputdict[other_number]['call_in'] = callin_count
                        outputdict[other_number]['call_out'] = callout_count

            # print(outputdict)

            # outputdict[other_number]['address'] = value['first_cgid_address']
            outputlist = (list(outputdict.values()))
        time7 = {'title':'python iteration ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'iteration time':time.time() - time6['timestamp']}
        time8 = {'title':'Function ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'processing time':time.time() - time1['timestamp']}

        if mode == "total_calls":
            response = {'headers': [
                k for k in outputlist[0].keys()], 'data_dict': outputlist,'times':[time1,time2,time3,time4,time5,time6,time7,time8]}
        else:
            response = {'data_dict':getprofile,'header2': ['source_number', 'destination_number', 'nickname', 'call_in', 'call_out', 'total_calls', 'duration', 'first_call',
                        'last_call', 'address'], 'data2': outputlist, 'status': 'success', 'message': 'data retrived successfully','times':[time1,time2,time3,time4,time5,time6,time7,time8]}  # , 'headers': getprofile['headers'], 'data_dict': getprofile['data_dict']}  # ,'totalpages':total_pages}
        return response

    def get_total_summary(self, data, fromdate, todate):
        logger.info("profleinfo retriving for total summaray")
        getprofile = self.cdr_profile(data)
        query = {}
        if fromdate is None and todate is None:
            query = {
                '$or': [{'destination_number': data},
                        {'$and': [{'destination_number': data},
                                  {'duration': {'$gt': 0}}]},
                        {'destination_number': {'$exists': False}}
                        ]
            }
        if fromdate is not None and todate is not None:
            query = {'timestamp': {
                '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()},
                '$or': [{'destination_number': data},
                        {'$and': [{'destination_number': data},
                                  {'duration': {'$gt': 0}}]},
                        {'destination_number': {'$exists': False}}
                        ]
            }

        unique_source_numbers = self.collection_cdrdata.distinct(
            'source_number', query)
        # print((unique_source_numbers),"--------------------------")
        outputlist = []
        outputdict = {}
        logger.info("mongo retriving")
        for source_number in unique_source_numbers:
            print(source_number)
            if fromdate is None and todate is None:
                query = {'source_number': source_number,
                         '$or': [{'destination_number': data},
                                 {'$and': [{'destination_number': data},
                                           {'duration': {'$gt': 0}}]},
                                 {'destination_number': {'$exists': False}}
                                 ]
                         }
            if fromdate is not None and todate is not None:
                query = {'source_number': source_number, 'timestamp': {
                    '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                    '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()},
                    '$or': [{'destination_number': data},
                            {'$and': [{'destination_number': data},
                                      {'duration': {'$gt': 0}}]},
                            {'destination_number': {'$exists': False}}
                            ]
                }

            # {'source_number': source_number, 'destination_number': data, 'call_type': {'$in': ['call_in', 'call_out']}})
            getdata = list(self.collection_cdrdata.find(query))
            if len(getdata) == 0:
                response = {'data2': 'Not data Matched'}
                return response
            logger.info("mongo retriving")
            callin_count = 0
            callout_count = 0
            callduration = 0
            first_call = None
            last_call = None
            other_number = None
            nickname = None
            user_address = None
            for dest in getdata:
                # print(dest['source_number'],"----------------")
                if dest['source_number'] not in outputdict:
                    outputdict[dest['source_number']] = {}

                other_number = dest['source_number']
                sdr_match = self.collection_sdrdata.find_one(
                    {'source_number': dest['source_number']})
                nickname = sdr_match.get('nickname') if sdr_match else ''
                user_address = sdr_match.get(
                    'local_address') if sdr_match else ''
                # other_number = data
                if "in" in dest["call_type"].lower():
                    callin_count += 1
                elif "out" in dest["call_type"].lower():  # == 'call_out':
                    callout_count += 1

                timestamp = dest['timestamp']
                if first_call is None or timestamp < first_call:
                    first_call = timestamp
                if last_call is None or timestamp > last_call:
                    last_call = timestamp

                # You need to adjust this based on your data structure
                callduration += dest.get('duration', 0)

            if first_call is not None:
                first_call = datetime.fromtimestamp(
                    first_call).strftime('%Y-%m-%d %H:%M:%S')

            if last_call is not None:
                last_call = datetime.fromtimestamp(
                    last_call).strftime('%Y-%m-%d %H:%M:%S')

            outputdict[dest['source_number']] = {
                'source_number': data,
                'destination_number': other_number,
                'nickname': nickname,
                'address': user_address,
                'total_calls': callin_count + callout_count,
                'duration': callduration,
                'first_call': first_call,
                'last_call': last_call,
                'call_in': callin_count,
                'call_out': callout_count,
            }
            print(outputdict)

        outputlist = list(outputdict.values())

        response = {
            'header2': ['source_number', 'destination_number', 'nickname', 'call_in', 'call_out', 'total_calls', 'duration', 'first_call', 'last_call', 'address'],
            'data2': outputlist if outputlist else 'Not data Matched', 'status': 'success', 'message': 'data retrived successfully', 'data_dict': getprofile['data_dict']
        }

        return response

    def total_contacts(self, data, dest_num):
        print(data, dest_num, "=====total_calls====")
        getdata = dest_num.split(",")
        outputdict = {}
        for dest in getdata:
            # logger.info("Data rendering started")
            other_number = dest
            indiv_dest_number = []
            if other_number not in outputdict:
                outputdict[other_number] = {}
                print(data, other_number)
                # ,'call_type':{'$in':['call_in','call_out']} })#.sort('timestamp',pymongo.ASCENDING).skip(skip_doc).limit(items_per_page)

                indiv_dest_number = (self.collection_cdrdata.find(
                    {'source_number': data, 'destination_number': str(other_number)}))

                callduration = 0
                callin_count = 0
                callout_count = 0
                first_call = None
                last_call = None
                loop_count_second = 0
                for value in indiv_dest_number:

                    callduration += value['duration']
                    if value["incoming"] == 1:
                        callin_count += 1
                    elif value["incoming"] == 0:  # == 'call_out':
                        callout_count += 1

                    if first_call is None or value['timestamp'] < first_call:
                        first_call = value['timestamp']
                    if last_call is None or value['timestamp'] > last_call:
                        last_call = value['timestamp']

                    # outputdict[other_number]['address'] = value['first_cgid_address']
                    loop_count_second += 1
                if isinstance(first_call, int):
                    first_call = datetime.fromtimestamp(
                        first_call).strftime('%Y-%m-%d %H:%M:%S')
                if isinstance(last_call, int):
                    last_call = datetime.fromtimestamp(
                        last_call).strftime('%Y-%m-%d %H:%M:%S')
                sdr_match = self.collection_sdrdata.find_one(
                    {'source_number': dest})
                full_name = sdr_match.get(
                    'fullname') if sdr_match else 'Not Available'
                user_address = sdr_match.get('local_address') if sdr_match else [
                    address_phone['areadescription'] for address_phone in self.collection_phonearea.find({'phoneprefix': dest[:5]})]
                outputdict[other_number]['address'] = f'Name: {full_name}, Address: {user_address}'
                outputdict[other_number]['source_number'] = data
                outputdict[other_number]['destination_number'] = dest
                outputdict[other_number]['first_call'] = first_call
                outputdict[other_number]['last_call'] = last_call
                outputdict[other_number]['total_calls'] = callin_count + \
                    callout_count
                outputdict[other_number]['duration'] = callduration
                outputdict[other_number]['call_in'] = callin_count
                outputdict[other_number]['call_out'] = callout_count
                outputdict[other_number]['nickname'] = [nickname.get('nickname', '') for nickname in self.collection_suspect.find(
                    {'phone': value['destination_number']}, {'_id': 0}).sort('timestamp', pymongo.ASCENDING).limit(-1)]

            # outputdict[other_number]['address'] = value['first_cgid_address']

        outputlist = list(outputdict.values())

        print(outputlist)

        response = {'headers': ['source_number', 'destination_number', 'nickname', 'call_in', 'call_out',
                                'total_calls', 'duration', 'first_call', 'last_call', 'address'], 'data_dict': outputlist}
        return response

    def imei_used_in_phone(self, data):
        logger.info("started")
        if self.collection_cdrdata.count_documents({'source_number': data}) == 0:
            response = {'headers': 'No Data', 'data_dict': 'Not data Matched',
                        'status': 'empty', 'message': "no data found"}
            return response
        cdr_fetch = self.collection_cdrdata.distinct(
            'imei', {'source_number': data})
        total_pages = self.collection_cdrdata.count_documents(
            {'source_number': data})

        output_dict = {}

        overall_imei = []
        for imei in cdr_fetch:
            matching_documents = self.collection_cdrdata.find(
                {'imei': imei, 'source_number': data})
            # Initialize variables to store the information
            call_in_count = 0
            call_out_count = 0
            total_count = 0
            duration = 0
            nickname = None
            first_call = None
            last_call = None
            source_number = None
            address = None
            source_numbers = []

            # Extract the data for each matching document
            logger.info(f"for loop starts -- {imei}")
            for document in matching_documents:
                source_number = document['source_number']
                call_type = document['incoming']
                timestamp = document['timestamp']

                if call_type == 1:  # 'call_in':
                    call_in_count += 1
                elif call_type == 0:  # 'call_out':
                    call_out_count += 1

                total_count = call_in_count + call_out_count
                duration += document['duration']

                if first_call is None or timestamp < first_call:
                    first_call = timestamp
                if last_call is None or timestamp > last_call:
                    last_call = timestamp

                if source_number not in source_numbers:
                    source_numbers.append(source_number)
            logger.info("for loop ends")
            # Convert timestamps to readable date format
            if first_call:
                first_call = datetime.fromtimestamp(
                    first_call).strftime('%Y-%m-%d %H:%M:%S')
            if last_call:
                last_call = datetime.fromtimestamp(
                    last_call).strftime('%Y-%m-%d %H:%M:%S')

            nickname = [nickname.get('nickname', 'not available') for nickname in self.collection_suspect.find(
                {'phone': source_number}, {'_id': 0}).sort('timestamp', pymongo.ASCENDING).limit(-1)]
            address = [sdr_add.get('local_address', '') for sdr_add in self.collection_sdrdata.find(
                {"source_number": source_number}).sort('timestamp', pymongo.DESCENDING).limit(-1)]
            cdr_contacts = {
                "imei": imei,
                "nickname": nickname,
                "source_number": source_number,
                "call_in": call_in_count,
                "call_out": call_out_count,
                "total_calls": total_count,
                "dur": duration,
                "first_call": first_call,
                "last_call": last_call,
                "address": address
            }
            overall_imei.append(cdr_contacts)

        response = {'headers': list(
            overall_imei[0].keys()), 'data_dict': overall_imei}
        logger.info("ended")
        return response

    def imsi_used_in_phone(self, data):
        logger.info(f"Function starts for {data}")
        # Find documents matching the source_number
        if self.collection_cdrdata.count_documents({'source_number': data}) == 0:
            response = {'headers': 'No Data',
                        'status': 'failure', 'message': 'no data found'}
            return response
        else:

            matching_documents = self.collection_cdrdata.find(
                {'source_number': data})

            # Initialize variables to store the information
            call_in_count = 0
            call_out_count = 0
            total_count = 0
            duration = 0
            first_call = None
            last_call = None
            imsi = None

            # Extract the data for each matching document
            for document in matching_documents:
                sdr_match = self.collection_sdrdata.find_one(
                    {"source_number": data})
                address = sdr_match['local_address'] if sdr_match else ''
                call_type = document['incoming']
                timestamp = document['timestamp']
                document_imsi = document['imsi']

                if call_type == 1:  # 'call_in':
                    call_in_count += 1
                elif call_type == 0:  # 'call_out':
                    call_out_count += 1

                total_count = call_in_count+call_out_count
                duration += document['duration']

                if first_call is None or timestamp < first_call:
                    first_call = timestamp
                if last_call is None or timestamp > last_call:
                    last_call = timestamp

            nickname = [nickname.get('nickname', 'not available') for nickname in self.collection_suspect.find(
                {'phone': data}, {'_id': 0}).sort('timestamp', pymongo.ASCENDING).limit(-1)]

            # Convert timestamps to readable date format
            if first_call:
                first_call = datetime.fromtimestamp(
                    first_call).strftime('%Y-%m-%d %H:%M:%S')
            if last_call:
                last_call = datetime.fromtimestamp(
                    last_call).strftime('%Y-%m-%d %H:%M:%S')

            cdr_contacts = {
                "source_number": data,
                "nickname": nickname,
                "imsi": document_imsi,
                "call_in": call_in_count,
                "call_out": call_out_count,
                "total_calls": total_count,
                "dur": duration,
                "first_call": first_call,
                "last_call": last_call,
                "address": address
            }

            response = {'headers': [k for k in cdr_contacts.keys()], 'data_dict': [
                cdr_contacts], 'status': 'success', 'message': 'data retrived successfully'}
            logger.info(f"Function ends")
            return response

    def imsi_search_info(self, data):
        logger.info("function starts")
        # Find documents matching the source_number
        if self.collection_cdrdata.count_documents({'imsi': data}) == 0:
            response = {'headers': 'No Data',
                        'status': 'failure', 'message': 'no data found'}
            return response
        else:

            matching_documents = self.collection_cdrdata.find(
                {'imsi': data})

            # Initialize variables to store the information
            call_in_count = 0
            call_out_count = 0
            total_count = 0
            duration = 0
            nickname = None
            address = None
            first_call = None
            last_call = None
            source_number = None
            source_numbers = []

            # Extract the data for each matching document
            for document in matching_documents:
                source_number = document['source_number']
                call_type = document['incoming']
                timestamp = document['timestamp']
                sdr_match = self.collection_sdrdata.find_one(
                    {"source_number": source_number})
                address = sdr_match['local_address'] if sdr_match else ''

                if call_type == 1:
                    call_in_count += 1
                elif call_type == 0:
                    call_out_count += 1

                total_count = call_in_count+call_out_count
                duration += document['duration']

                if first_call is None or timestamp < first_call:
                    first_call = timestamp
                if last_call is None or timestamp > last_call:
                    last_call = timestamp

                if source_number not in source_numbers:
                    source_numbers.append(source_number)

            nickname = [nickname.get('nickname', 'not available') for nickname in self.collection_suspect.find(
                {'phone': data}, {'_id': 0}).sort('timestamp', pymongo.ASCENDING).limit(-1)]
            # Convert timestamps to readable date format
            if first_call:
                first_call = datetime.fromtimestamp(
                    first_call).strftime('%Y-%m-%d %H:%M:%S')
            if last_call:
                last_call = datetime.fromtimestamp(
                    last_call).strftime('%Y-%m-%d %H:%M:%S')

            cdr_contacts = {
                "imsi": data,
                "nickname": nickname,
                "source_number": source_number,
                "call_in": call_in_count,
                "call_out": call_out_count,
                "total_calls": total_count,
                "dur": duration,
                "first_call": first_call,
                "last_call": last_call,
                "address": address
            }

            response = {'headers': [k for k in cdr_contacts.keys()], 'data_dict': [
                cdr_contacts], 'status': 'success', 'message': 'data retrived successfully'}
            logger.info("function starts")

            return response

    def phones_used_in_imei(self, data):
        if self.collection_cdrdata.count_documents({'imei': data}) == 0:
            response = {'data_dict': 'Not data matched',
                        'status': 'empty', 'message': 'no data found'}
            return response
        else:
            logger.info("Search starts")
            matching_documents = self.collection_cdrdata.find(
                {'imei': data})
            # first_call = None
            # last_call = None
            outputdict = {}

            for document in matching_documents:
                source_number = document['source_number']

                if source_number not in outputdict:
                    outputdict[source_number] = {
                        'sourcenumber': document['source_number'],
                        'call_in': 0,
                        'call_out': 0,
                        'duration': 0,
                        'total_calls': 0,
                        'imei_number': document['imei'],
                        'first_call': None,  # Initialize with None
                        'last_call': None,   # Initialize with None
                    }

                if document['incoming'] == 1:
                    outputdict[source_number]['call_in'] += 1
                elif document['incoming'] == 0:
                    outputdict[source_number]['call_out'] += 1

                outputdict[source_number]['duration'] += document['duration']
                outputdict[source_number]['total_calls'] += 1
            ad_nk = list(outputdict.keys())
            for val in ad_nk:
                address = [sdr_add.get('local_address', '') for sdr_add in self.collection_sdrdata.find(
                    {"source_number": val}).sort('timestamp', pymongo.DESCENDING).limit(-1)]
                if len(address) == 0:
                    address = [address_phone['areadescription']
                               for address_phone in self.collection_phonearea.find({'phoneprefix': val[:5]})]
                outputdict[val]['address'] = address
                outputdict[val]['nickname'] = [nickname.get('nickname', 'not available') for nickname in self.collection_suspect.find({
                    'phone': val}, {'_id': 0}).sort('timestamp', pymongo.ASCENDING).limit(-1)]
                first_call_data = self.collection_cdrdata.find_one({'source_number': val, 'imei':
                                                                    data}, {'timestamp': 1}, sort=[('timestamp', pymongo.ASCENDING)])
                if first_call_data:
                    first_call_timestamp = first_call_data['timestamp']
                    outputdict[val]['first_call'] = datetime.fromtimestamp(
                        first_call_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                last_call_data = self.collection_cdrdata.find_one({'source_number': val, 'imei':
                                                                   data}, {'timestamp': 1}, sort=[('timestamp', pymongo.DESCENDING)])
                if last_call_data:
                    last_call_timestamp = last_call_data['timestamp']
                    outputdict[val]['last_call'] = datetime.fromtimestamp(
                        last_call_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            cdr_contacts = list(outputdict.values())
            response = {'data_dict': cdr_contacts, 'status': 'success',
                        'message': 'data retrived successfully'}
            logger.info("Search ends")

            return response

    def imei_search_info(self, data, imeinumbers):
        print("In imei searcj", data)
        overall_imei = []
        for imei in imeinumbers:
            matching_documents = self.collection_cdrdata.find(
                {'imei': imei, 'source_number': data})

            # Initialize variables to store the information
            call_in_count = 0
            call_out_count = 0
            total_count = 0
            duration = 0
            nickname = None
            first_call = None
            last_call = None
            source_number = None
            address = None
            source_numbers = []

            # Extract the data for each matching document
            for document in matching_documents:
                source_number = document['source_number']
                call_type = document['incoming']
                timestamp = document['timestamp']

                if call_type == 1:
                    call_in_count += 1
                elif call_type == 0:
                    call_out_count += 1

                # += 1 if call_type in ['call_in', 'call_out'] else 0
                total_count = call_in_count + call_out_count
                duration += document['duration']

                if first_call is None or timestamp < first_call:
                    first_call = timestamp
                if last_call is None or timestamp > last_call:
                    last_call = timestamp

                if source_number not in source_numbers:
                    source_numbers.append(source_number)

            nickname = [nickname.get('nickname', 'not available') for nickname in self.collection_suspect.find(
                {'phone': data}, {'_id': 0}).sort('timestamp', pymongo.ASCENDING).limit(-1)]
            address = [sdr_add.get('local_address', '') for sdr_add in self.collection_sdrdata.find(
                {"source_number": data}).sort('timestamp', pymongo.DESCENDING).limit(-1)]
            if len(address) == 0:
                # print("IN IF CONDIOT")
                address = [address_phone['areadescription']
                           for address_phone in self.collection_phonearea.find({'phoneprefix': data[:5]})]
            # Convert timestamps to readable date format
            if first_call:
                first_call = datetime.fromtimestamp(
                    first_call).strftime('%Y-%m-%d %H:%M:%S')
            if last_call:
                last_call = datetime.fromtimestamp(
                    last_call).strftime('%Y-%m-%d %H:%M:%S')

            cdr_contacts = {
                "imei": imei,
                "nickname": nickname,
                "source_number": source_number,
                "call_in": call_in_count,
                "call_out": call_out_count,
                "total_calls": total_count,
                "dur": duration,
                "first_call": first_call,
                "last_call": last_call,
                "address": address
            }
            overall_imei.append(cdr_contacts)

        response = {'headers': list(
            overall_imei[0].keys()), 'data_dict': overall_imei, 'status': 'success', 'message': 'data retrived successfully'}
        return response

    def total_location(self, data, item, currentpage, fromdate, todate):
        print("In total locations", fromdate, todate)
        # Find documents matching the source_number
        if fromdate is None and todate is None:
            count_documents = self.collection_cdrdata.count_documents(
                {'source_number': data})
        if fromdate is not None and todate is not None:
            count_documents = self.collection_cdrdata.count_documents({
                'source_number': data,
                # 'incoming': {'$in': [0,1]},
                'timestamp': {
                    '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                    '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                }
            })

        if count_documents == 0:
            response = {'headers': 'No Data', 'data_dict': '',
                        'status': 'empty', 'message': 'no data found'}
            return response
        else:
            print("In else-----")
            items_per_page = int(item)
            current_page = int(currentpage)
            skip_doc = int(items_per_page) * (int(current_page) - 1)
            total_pages = count_documents
            # .sort('timestamp', pymongo.DESCENDING).skip(skip_doc).limit(items_per_page)
            if fromdate is None and todate is None:
                matching_documents = self.collection_cdrdata.find(
                    {'source_number': data})
            if fromdate is not None and todate is not None:
                matching_documents = self.collection_cdrdata.find({
                    'source_number': data,
                    # 'inconing': {'$in': [0,1]},
                    'timestamp': {
                        '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                        '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                    }
                })

            # Initialize a dictionary to store the tower data
            tower_data = {}
            sdr_match = self.collection_sdrdata.find_one(
                {"source_number": data})
            suspect_match = self.collection_suspect.find_one({"phone": data})
            nickname = suspect_match.get(
                'nickname', '') if suspect_match else ''
            user_address = sdr_match.get(
                'local_address', '') if sdr_match else ''

            # Extract the data for each matching document
            for document in matching_documents:
                tower_id = document['first_cgid']
                call_type = document['call_type']
                timestamp = document['timestamp']

                if call_type in ['call_in', 'call_out']:
                    if tower_id not in tower_data:
                        tower_data[tower_id] = {
                            'total_calls': 0,
                            'first_call': timestamp,
                            'last_call': timestamp,
                        }
                    else:
                        if timestamp < tower_data[tower_id]['first_call']:
                            tower_data[tower_id]['first_call'] = timestamp
                        if timestamp > tower_data[tower_id]['last_call']:
                            tower_data[tower_id]['last_call'] = timestamp
                    tower_data[tower_id]['total_calls'] += 1

            # Sort the tower data by call count in descending order
            sorted_tower_data = sorted(
                tower_data.items(), key=lambda x: x[1]['total_calls'], reverse=True)

            # Prepare the data for the top 10 towers
            total_location = []
            for tower_id, datas in sorted_tower_data:
                matched_tower = self.collection_cellid.find_one(
                    {'celltowerid': tower_id}, {'siteaddress': 1, 'lat': 1, 'long': 1})
                siteaddress = matched_tower.get(
                    'siteaddress', '') if matched_tower else 'Adress not Found'
                latitude = matched_tower.get('lat') if matched_tower else ''
                longitude = matched_tower.get('long') if matched_tower else ''

                tower = {
                    'source_number': data,
                    'nickname': nickname,
                    'tower_id': tower_id,
                    'latitude': latitude,
                    'longitude': longitude,
                    'total_calls': datas['total_calls'],
                    'first_call': datetime.fromtimestamp(datas['first_call']).strftime('%Y-%m-%d %H:%M:%S'),
                    'last_call': datetime.fromtimestamp(datas['last_call']).strftime('%Y-%m-%d %H:%M:%S'),
                    'site_address': siteaddress,
                    'user_address': user_address
                }
                total_location.append(tower)

            response = {
                'headers': ['source_number', 'nickname', 'Tower ID', 'total_calls', 'first_call', 'last_call', 'site_address', 'user_address'],
                'data_dict': total_location,
                'totalpages': total_pages,
                'status': 'success',
                'message': 'data retrived successfully'
            }
            return response

    def day_night_mapping(self, data, fromdate, todate):
        print(fromdate, todate, "------------date range ------------")
        top_10_day_towers = None
        top_10_night_towers = None
        if fromdate is None and todate is None:
            if self.collection_cdrdata.count_documents({'source_number': data}) == 0:
                response = {
                    'headers': "No Data",
                    'day_data':  top_10_day_towers,
                    'night_data': top_10_night_towers,
                    'status': 'empty',
                    'message': 'no data found'
                }
                return response
        if fromdate is not None and todate is not None:
            if self.collection_cdrdata.count_documents({'source_number': data, 'timestamp': {
                '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
            }}) == 0:
                response = {
                    'headers': "No Data",
                    'day_data':  top_10_day_towers,
                    'night_data': top_10_night_towers,
                    'status': 'empty',
                    'message': 'no data found'
                }
                return response

        # .sort('timestamp', pymongo.DESCENDING).skip(skip_doc).limit(items_per_page)
        if fromdate is None and todate is None:
            matching_documents = self.collection_cdrdata.find(
                {'source_number': data})
        if fromdate is not None and todate is not None:
            matching_documents = self.collection_cdrdata.find(
                {'source_number': data, 'timestamp': {
                    '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                    '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()}})

        # Initialize dictionaries to store the tower data for day and night
        day_tower_data = {}
        night_tower_data = {}
        sdr_match = self.collection_sdrdata.find_one({"source_number": data})
        suspect_match = self.collection_suspect.find_one({"phone": data})
        nickname = suspect_match.get('nickname', '') if suspect_match else ''
        user_address = sdr_match.get('local_address', '') if sdr_match else ''

        # Extract the data for each matching document
        for document in matching_documents:
            tower_id = document['first_cgid']
            timestamp = document['timestamp']
            call_type = document['call_type']

            # Convert the timestamp to a datetime object
            datetime_obj = datetime.fromtimestamp(timestamp)

            # Check if the time is within the day mapping range (6 AM to 6 PM)
            if 6 <= datetime_obj.hour < 18:
                mapping_dict = day_tower_data
            else:
                mapping_dict = night_tower_data

            if call_type in ['call_in', 'call_out']:
                if tower_id not in mapping_dict:
                    mapping_dict[tower_id] = {
                        'total_calls': 0,
                        'first_call': timestamp,
                        'last_call': timestamp,
                    }
                else:
                    if timestamp < mapping_dict[tower_id]['first_call']:
                        mapping_dict[tower_id]['first_call'] = timestamp
                    if timestamp > mapping_dict[tower_id]['last_call']:
                        mapping_dict[tower_id]['last_call'] = timestamp

            if tower_id in mapping_dict:
                mapping_dict[tower_id]['total_calls'] += 1
            else:
                pass

        # Sort the tower data for day and night by call count in descending order
        sorted_day_tower_data = sorted(day_tower_data.items(
        ), key=lambda x: x[1]['total_calls'], reverse=True)
        sorted_night_tower_data = sorted(
            night_tower_data.items(), key=lambda x: x[1]['total_calls'], reverse=True)

        # Prepare the data for the top 10 towers for day and night
        top_10_day_towers = []
        top_10_night_towers = []

        for tower_id, datas in sorted_day_tower_data[:10]:
            matched_tower = self.collection_cellid.find_one(
                {'celltowerid': tower_id}, {'siteaddress': 1})
            siteaddress = matched_tower.get(
                'siteaddress', '') if matched_tower else 'Adress not Found'

            tower = {
                'source_number': data,
                'nickname': nickname,
                'tower_id': tower_id,
                'first_call': datetime.fromtimestamp(datas['first_call']).strftime('%Y-%m-%d %H:%M:%S'),
                'last_call': datetime.fromtimestamp(datas['last_call']).strftime('%Y-%m-%d %H:%M:%S'),
                'total_calls': datas['total_calls'],
                'site_address': siteaddress,
                'user_address': user_address
            }
            top_10_day_towers.append(tower)

        for tower_id, datas in sorted_night_tower_data[:10]:
            matched_tower = self.collection_cellid.find_one(
                {'celltowerid': tower_id}, {'siteaddress': 1})
            siteaddress = matched_tower.get(
                'siteaddress', '') if matched_tower else 'Adress not Found'

            tower = {
                'source_number': data,
                'nickname': nickname,
                'tower_id': tower_id,
                'total_calls': datas['total_calls'],
                'first_call': datetime.fromtimestamp(datas['first_call']).strftime('%Y-%m-%d %H:%M:%S'),
                'last_call': datetime.fromtimestamp(datas['last_call']).strftime('%Y-%m-%d %H:%M:%S'),
                'site_address': siteaddress,
                'user_address': user_address
            }
            top_10_night_towers.append(tower)

        response = {
            'headers': ['source_number', 'nickname', 'tower_id', 'total_calls', 'first_call', 'last_call', 'site_address', 'user_address'],
            'day_data':  top_10_day_towers,
            'night_data': top_10_night_towers,
            'status': 'success',
            'message': 'data retrived successfully'
        }
        return response

    def day_mapping_with_date(self, data, fromdate, todate):
        print(data, fromdate, todate, "--------------------------")
        # Find documents matching the source_number and within the date range
        if fromdate is None and todate is None:
            count_documents = self.collection_cdrdata.count_documents(
                {'source_number': data})
        if fromdate is not None and todate is not None:
            print(fromdate, todate, "-inside---")
            count_documents = self.collection_cdrdata.count_documents({
                'source_number': data,
                # 'incoming': {'$in': [0,1]},
                'timestamp': {
                    '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                    '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                }
            })

        if count_documents == 0:
            response = {'headers': "No Data", 'data_dict': "",
                        'status': 'failure', 'message': 'no data found'}
            return response
        else:
            print("----------------------")
            if fromdate is None and todate is None:
                matching_documents = self.collection_cdrdata.find(
                    {'source_number': data})
            if fromdate is not None and todate is not None:
                matching_documents = self.collection_cdrdata.find({
                    'source_number': data,
                    # 'inconing': {'$in': [0,1]},
                    'timestamp': {
                        '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                        '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                    }
                })
        # Initialize a dictionary to store the tower data for day
            day_tower_data = {}
            sdr_match = self.collection_sdrdata.find_one(
                {"source_number": data})
            suspect_match = self.collection_suspect.find_one({"phone": data})
            nickname = suspect_match.get(
                'nickname', '') if suspect_match else ''
            user_address = sdr_match.get(
                'local_address', '') if sdr_match else ''

            # Extract the data for each matching document
            for document in matching_documents:
                tower_id = document['first_cgid']
                timestamp = document['timestamp']
                call_type = document['call_type']

                if tower_id not in day_tower_data:
                    day_tower_data[tower_id] = {
                        'total_calls': 0,
                        'first_call': timestamp,
                        'last_call': timestamp,
                    }
                else:
                    if timestamp < day_tower_data[tower_id]['first_call']:
                        day_tower_data[tower_id]['first_call'] = timestamp
                    if timestamp > day_tower_data[tower_id]['last_call']:
                        day_tower_data[tower_id]['last_call'] = timestamp

                datetime_obj = datetime.fromtimestamp(timestamp / 1000)

                # Check if the time is within the day mapping range (6 AM to 6 PM)
                if 6 <= datetime_obj.hour < 18:
                    # Increment the call count based on call_type
                    if call_type in ['call_in', 'call_out']:
                        day_tower_data[tower_id]['total_calls'] += 1

            # Sort the tower data for day by call count in descending order
            sorted_day_tower_data = sorted(day_tower_data.items(
            ), key=lambda x: x[1]['total_calls'], reverse=True)

            # Prepare the data for the top 10 towers for day
            top_10_day_towers = []
            # print(sorted_day_tower_data)
            for tower_id, datas in sorted_day_tower_data[:10]:
                matched_tower = self.collection_cellid.find_one(
                    {'celltowerid': tower_id}, {'siteaddress': 1})
                siteaddress = matched_tower.get(
                    'siteaddress', '') if matched_tower else 'Adress not Found'
                tower = {
                    'nickname': nickname,
                    'source_number': data,
                    'tower_id': tower_id,
                    'first_call': datetime.fromtimestamp(datas['first_call']).strftime('%Y-%m-%d %H:%M:%S'),
                    'last_call': datetime.fromtimestamp(datas['last_call']).strftime('%Y-%m-%d %H:%M:%S'),
                    'total_calls': datas['total_calls'],
                    'user_address': user_address,
                    'site_address': siteaddress

                }
                top_10_day_towers.append(tower)

        response = {
            'headers': ['source_number', 'nickname', 'tower_id', 'total_calls', 'first_call', 'last_call', 'siteaddress', 'user_address'],
            'data_dict': top_10_day_towers,
            'status': 'success',
            'message': 'data retrived successfully'
        }
        return response

    def night_mapping_with_date(self, data, fromdate, todate):
        # Find documents matching the source_number and within the date range
        if fromdate == "" and todate == "":
            count_documents = self.collection_cdrdata.count_documents(
                {'source_number': data})
        elif fromdate != "" and todate != "":
            count_documents = self.collection_cdrdata.count_documents({
                'source_number': data,
                'incoming': {'$in': [0, 1]},
                'timestamp': {
                    '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                    '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                }
            })

        if count_documents == 0:
            response = {'headers': "No Data", 'data_dict': "",
                        'status': 'failure', 'message': 'no data found'}
            return response
        else:
            print("----------------------")
            if fromdate == "" and todate == "":
                matching_documents = self.collection_cdrdata.find(
                    {'source_number': data})
            elif fromdate != "" and todate != "":
                matching_documents = self.collection_cdrdata.find({
                    'source_number': data,
                    'incoming': {'$in': [0, 1]},
                    'timestamp': {
                        '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                        '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                    }
                })
        # Initialize a dictionary to store the tower data for day
            night_tower_data = {}
            sdr_match = self.collection_sdrdata.find_one(
                {"source_number": data})
            suspect_match = self.collection_suspect.find_one({"phone": data})

            nickname = suspect_match['nickname'] if suspect_match else ''
            user_address = sdr_match['local_address'] if sdr_match else ''

            # Extract the data for each matching document
            for document in matching_documents:
                tower_id = document['first_cgid']
                timestamp = document['timestamp']
                call_type = document['call_type']

                if tower_id not in night_tower_data:
                    night_tower_data[tower_id] = {
                        'total_calls': 0,
                        'first_call': timestamp,
                        'last_call': timestamp,
                    }
                else:
                    if timestamp < night_tower_data[tower_id]['first_call']:
                        night_tower_data[tower_id]['first_call'] = timestamp
                    if timestamp > night_tower_data[tower_id]['last_call']:
                        night_tower_data[tower_id]['last_call'] = timestamp

                datetime_obj = datetime.fromtimestamp(timestamp / 1000)

                # Check if the time is within the day mapping range (6 AM to 6 PM)
                if datetime_obj.hour >= 18 or datetime_obj.hour < 6:
                    # Increment the call count based on call_type
                    if call_type in ['call_in', 'call_out']:
                        if tower_id not in night_tower_data:
                            night_tower_data[tower_id] = {
                                'total_calls': 0,
                            }
                        night_tower_data[tower_id]['total_calls'] += 1

            # Sort the tower data for day by call count in descending order
            sorted_day_tower_data = sorted(night_tower_data.items(
            ), key=lambda x: x[1]['total_calls'], reverse=True)

            # Prepare the data for the top 10 towers for day
            top_10_night_towers = []

            for tower_id, datas in sorted_day_tower_data[:10]:
                matched_tower = self.collection_cellid.find_one(
                    {'celltowerid': tower_id}, {'siteaddress': 1})
                siteaddress = matched_tower.get(
                    'siteaddress', '') if matched_tower else 'Adress not Found'

                tower = {
                    'source_number': data,
                    'tower_id': tower_id,
                    'total_calls': datas['total_calls'],
                    'first_call': datetime.fromtimestamp(datas['first_call']).strftime('%Y-%m-%d %H:%M:%S'),
                    'last_call': datetime.fromtimestamp(datas['last_call']).strftime('%Y-%m-%d %H:%M:%S'),
                    'user_address': user_address,
                    'site_address': siteaddress,
                    'nickname': nickname
                }
                top_10_night_towers.append(tower)

            response = {
                'headers': ['source_number', 'nickname', 'tower_id', 'total_calls', 'first_call', 'last_call', 'site_address', 'user_address'],
                'data_dict': top_10_night_towers,
                'status': 'success',
                'message': 'data retrived successfully'
            }
            return response

    def summary_for_state(self, data, state, mode, fromdate, todate):
        matching_documents_list = []
        if mode == "SummaryWithState" or mode == "SummaryWithoutState" or mode == "SummaryStateWise":
            print(data, state, "with state")
            if fromdate is None and todate is None:
                matching_documents_list = list(self.collection_cdrdata.find({
                    'source_number': data,
                }))
            if fromdate is not None and todate is not None:
                matching_documents_list = list(self.collection_cdrdata.find({
                    'source_number': data,
                    'timestamp': {
                        '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                        '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                    }
                }))
            print(data, state, fromdate, todate, "--for all-")
        # elif mode == "SummaryWithoutState":
        #     print(data, state, "without state")
        #     matching_documents = self.collection_cdrdata.find({
        #         'source_number': data
        #     })
        #     matching_documents_list = list(matching_documents)
        # elif mode == "SummaryStateWise":
        #     print(data, "statewise")
        #     matching_documents = self.collection_cdrdata.find({
        #         'source_number': data,
        #     })
        #     matching_documents_list = list(matching_documents)

            # Initialize a nested dictionary to store the data for each destination number and state
            destination_data = {}

            # Extract the data for each destination number
            for document in matching_documents_list:
                destination_number = document['destination_number']
                call_type = document['incoming']
                duration = document['duration']
                timestamp = document['timestamp']
                # Get the first_cgid field from cdrcall

                tower_state = document.get('state', '')

                if mode == "SummaryWithState" and state and state != tower_state:
                    # Skip this record if mode is "SummaryWithState" and state is provided but doesn't match the tower_state
                    continue
                elif mode == "SummaryWithoutState" and state and state == tower_state:
                    # Skip this record if mode is "SummaryWithoutState" and state is provided and matches the tower_state
                    continue

                # Combine destination number and state as the key for the nested dictionary
                destination_state_key = (destination_number, tower_state)

                if destination_state_key not in destination_data:
                    destination_data[destination_state_key] = {
                        'source_number': data,
                        'call_in': 0,
                        'call_out': 0,
                        'total_count': 0,
                        'total_duration': 0,
                        'first_call': timestamp,
                        'last_call': timestamp,
                        'address': '',  # Added 'address' key to destination_data
                        'nickname': ''  # Added 'nickname' key to destination_data
                    }

                if call_type == 1:
                    destination_data[destination_state_key]['call_in'] += 1
                elif call_type == 0:
                    destination_data[destination_state_key]['call_out'] += 1
                destination_data[destination_state_key]['total_count'] += 1
                destination_data[destination_state_key]['total_duration'] += duration

                if timestamp < destination_data[destination_state_key]['first_call']:
                    destination_data[destination_state_key]['first_call'] = timestamp
                if timestamp > destination_data[destination_state_key]['last_call']:
                    destination_data[destination_state_key]['last_call'] = timestamp

            # Prepare the data for each destination number and state
            cdr_contacts_data = []
            for (destination_number, tower_state), dest_data in destination_data.items():
                # Use 'destination_number' as the 'MSISDN' parameter
                sdrdata_entry = self.collection_sdrdata.find_one(
                    {'source_number': destination_number})
                if sdrdata_entry:
                    dest_data['address'] = f'Name: {sdrdata_entry.get("fullname", "")}, Address:{sdrdata_entry.get("local_address", "")}'
                dest_data['nickname'] = [nickname.get('nickname', 'not available') for nickname in self.collection_suspect.find(
                    {'phone': destination_number}, {'_id': 0}).sort('timestamp', pymongo.ASCENDING).limit(-1)]

                first_call = None
                last_call = None

                if isinstance(dest_data['first_call'], int):
                    first_call = datetimeasnow.datetime.fromtimestamp(
                        dest_data['first_call'])
                    # first_call = datetime.fromtimestamp(dest_data['first_call'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

                if isinstance(dest_data['last_call'], int):
                    last_call = datetimeasnow.datetime.fromtimestamp(
                        dest_data['last_call'])
                    # last_call = datetime.fromtimestamp(dest_data['last_call'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

                cdr_contacts = {
                    "source_number": dest_data['source_number'],
                    "nickname": dest_data['nickname'],
                    "destination_number": destination_number,
                    "state": tower_state,
                    "call_in": dest_data['call_in'],
                    "call_out": dest_data['call_out'],
                    "total_calls": dest_data['total_count'],
                    "duration": dest_data['total_duration'],
                    "first_call": first_call,
                    "last_call": last_call,
                    "address": dest_data['address'],
                }
                cdr_contacts_data.append(cdr_contacts)
            # data_dict = list(cdr_contacts_data.values()) if cdr_contacts_data else "Not data Matched"
            data_dict = cdr_contacts_data if cdr_contacts_data else "Not data Matched"
            # print(data_dict,"data  dict")
            response = {'headers': ['source_number', 'nickname', 'destination_number', 'state', 'call_in',
                                    'call_out', 'duration', 'first_call', 'last_call', 'address'], 'data_dict': data_dict, 'status': 'success', 'message': 'data retrived successfully'}
            return response
        else:
            # Handle invalid mode value here if needed
            response = {'headers': [], 'data_dict': [],
                        'status': 'failure', 'message': 'no data found'}
            return response

    def tower_data(self, data):
        matching_documents = self.collection_towerid.find(
            {'source_number': data})
        tower_data = []
        for document in matching_documents:
            destination_number = document['destination_number']
            calldate = document['date']
            calltime = document['time']
            call_type = document['call_type']
            duration = document['duration']
            imei = document['imei']
            imsi = document['imsi']
            cellid = document['first_cgid']
            roaming = document['roaming_circle']
            # lat = document['lat']
            # long = document['long']

            tower = {
                'source_number': data,
                'nickname': 'not available',
                'destination_number': destination_number,
                'calldate': calldate,
                'calltime': calltime,
                'Call_type': call_type,
                'duration': duration,
                'imei': imei,
                'imsi': imsi,
                'cellid': cellid,
                'roaming': roaming,
                # 'latitude': lat,
                # 'longitude': long,
            }
            tower_data.append(tower)

        headers = [k for k in tower_data[0].keys()] if tower_data else []
        response = {'headers': headers, 'data_dict': tower_data}
        return response

    # --------------------- call_details --------------------------- #
    def cdr_data(self, data, mode, fromdate, todate, dest_num, imei_num, state, items=False, currentpage=False):
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
        if mode == "cdrdetails" or mode == "CdrBetweenDates":
            print(mode, "____________________mode__________________")
            print(data, fromdate, todate, "-------data----")
            if fromdate == "" and todate == "":
                print(data, skip_doc, items_per_page, "number ----")
                total_pages = self.collection_cdrdata.count_documents(
                    {"source_number": data})
                if items_per_page == False and current_page == False:
                    matching_documents = self.collection_cdrdata.find({'source_number': data}).sort(
                        'timestamp', pymongo.DESCENDING)
                else:
                    if current_page > 0:  # Check if current_page is greater than 0
                        skip_doc = (current_page - 1) * items_per_page
                    matching_documents = self.collection_cdrdata.find({'source_number': data}).sort(
                        'timestamp', pymongo.DESCENDING).skip(skip_doc).limit(items_per_page)
                logger.info("query completed for cdr or with date")
            elif fromdate != "" and todate != "":
                print('date present')
                total_pages = self.collection_cdrdata.count_documents({
                    'source_number': data,
                    'timestamp': {
                        '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                        '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                    }
                })
                if items_per_page == False and current_page == False:
                    matching_documents = self.collection_cdrdata.find({
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
                    matching_documents = self.collection_cdrdata.find({
                        'source_number': data,
                        'timestamp': {
                            '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                            '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                        }
                    }).sort('timestamp', pymongo.DESCENDING).skip(skip_doc).limit(items_per_page)
                    print("MMMMMMMMMMMM", matching_documents)

        if mode == "total_calls":
            logger.info(
                f"-----------total calls-----------,{data, dest_num,imei_num}")
            total_pages = self.collection_cdrdata.count_documents(
                {"source_number": data})
            if fromdate and todate:
                print(fromdate, todate)
                matching_documents = list(self.collection_cdrdata.find({'source_number': data, 'destination_number': dest_num,
                                                                        'timestamp': {
                                                                            '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                                                                            '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                                                                        }}).sort(
                    'timestamp', pymongo.DESCENDING))
            if state:
                print(state, "--inside stae")
                if fromdate and todate:
                    print(fromdate, todate)
                    matching_documents = list(self.collection_cdrdata.find({'source_number': data, 'state': state, 'destination_number': dest_num,
                                                                            'timestamp': {
                                                                                '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                                                                                '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                                                                            }}).sort(
                        'timestamp', pymongo.DESCENDING))
                else:
                    print("if state without daterange")
                    matching_documents = list(self.collection_cdrdata.find({'source_number': data, 'destination_number': dest_num, 'state': state,
                                                                            }).sort(
                        'timestamp', pymongo.DESCENDING))

            else:
                print("first---------------")
                matching_documents = list(self.collection_cdrdata.find({'source_number': data, 'destination_number': dest_num}).sort(
                    'timestamp', pymongo.DESCENDING))

            logger.info("query completed")
        if mode == "total_calls" and imei_num is not False:
            logger.info(
                f"-----------total calls-----------,{data, dest_num,imei_num}")
            total_pages = self.collection_cdrdata.count_documents(
                {"source_number": data})
            matching_documents = list(self.collection_cdrdata.find({'source_number': data, 'destination_number': dest_num}).sort(
                'timestamp', pymongo.DESCENDING))  # .skip(skip_doc).limit(items_per_page))
            logger.info("query completed")
        if mode == "total_calls" and dest_num is False:
            logger.info(
                f"-----------total calls-----------,{data, dest_num,imei_num}")
            total_pages = self.collection_cdrdata.count_documents(
                {"source_number": data})
            matching_documents = list(self.collection_cdrdata.find({'source_number': data, 'imei': imei_num}).sort(
                'timestamp', pymongo.DESCENDING))  # .skip(skip_doc).limit(items_per_page))
            logger.info("query completed")

        if mode == "cdrIMEI":
            print(data, "inside imei")
            if fromdate is None and todate is None:
                matching_documents = self.collection_cdrdata.find({'imei': data}).sort(
                    'timestamp', pymongo.DESCENDING)
            elif fromdate is not None and todate is not None:
                print('date present')
                total_pages = self.collection_cdrdata.count_documents({
                    'imei': data,
                    'timestamp': {
                        '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                        '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                    }
                })
                matching_documents = self.collection_cdrdata.find({
                    'imei': data,
                    'timestamp': {
                        '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                        '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                    }
                })

        cdr_data = []
        cdrimei_data = []
        cdr = None
        logger.info("interation started...")
        # print(matching_documents,"--there--")
        for document in matching_documents:
            destination_number = document['destination_number']
            # calldate = document['timestamp']
            # calltime = document['timestamp']
            call_type = document['call_type']
            duration = document['duration']
            if mode == "cdrdetails" or "hlink_number" or "total_contacts":
                imei = document['imei']
            if mode == "cdrIMEI":
                source_number = document['source_number']
            cellid = document['first_cgid']
            provider = document['provider']
            roaming = document['roaming_circle']
            calldate = datetimeasnow.datetime.fromtimestamp(
                document['timestamp']).strftime('%Y-%m-%d')
            calltime = datetimeasnow.datetime.fromtimestamp(
                document['timestamp']).strftime('%H:%M:%S')

            # Query the other collection for matching cellid
            cellid_match = self.collection_cellid.find_one(
                {'celltowerid': cellid})
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
            sdrfinds = self.collection_sdrdata.find_one(
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
            if mode == "cdrdetails" or mode == "total_contacts" or mode == "CdrBetweenDates" or mode == "total_calls":
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
            if mode == "cdrIMEI":
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
        # print(cdrimei_data, "cdr")
        # print(cdr_data,cdr)
        logger.info("iteration completed...")
        if mode == "cdrdetails" or mode == "total_calls" or mode == "CdrBetweenDates":
            headers = [k for k in cdr_data[0].keys()] if cdr_data else []
            response = {'headers': headers,
                        'data_dict': cdr_data, 'totalpages': total_pages}
            return response
        if mode == "cdrIMEI":
            headers = [k for k in cdrimei_data[0].keys()
                       ] if cdrimei_data else []
            response = {'headers': headers, 'data_dict': cdrimei_data}
            return response

    def cdr_data_with_time(self, data, fromdate, todate):
        print(data, fromdate, todate, "?????????????????????????????????")

        matching_documents = self.collection_cdrdata.find({
            'source_number': data,
            'timestamp': {
                '$gte': datetime.strptime(fromdate, "%Y-%m-%d").timestamp(),
                '$lte': datetime.strptime(todate, "%Y-%m-%d").timestamp()
            }
        })

        # print(matching_documents)

        cdr_data = []

        for document in matching_documents:
            print(document)
            sdr_match = self.collection_sdrdata.find_one(
                {'source_number': document['destination_number']})
            suspect_data = self.collection_suspect.find_one(
                {'phone': document['destination_number']})
            nickname = suspect_data.get('nickname') if suspect_data else ''
            address = sdr_match.get('local_address') if sdr_match else ''
            destination_number = document['destination_number']
            calldate = datetime.fromtimestamp(
                document['timestamp']).strftime('%d-%m-%Y')
            calltime = datetime.fromtimestamp(
                document['timestamp']).strftime('%H:%M:%S')
            call_type = document['call_type']
            duration = document['duration']
            imei = document['imei']
            cellid = document['first_cgid']
            provider = document['provider']
            roaming = document['roaming_circle']

            # Query the other collection for matching cellid
            cellid_match = self.collection_cellid.find_one(
                {'celltowerid': cellid})
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
                'azimuth': azimuth
            }

            cdr_data.append(cdr)

        headers = [k for k in cdr_data[0].keys()] if cdr_data else []
        response = {'headers': headers, 'data_dict': cdr_data}
        return response

    def common_contacts(self, source_numbers_list, from_date=None, to_date=None):
        print(source_numbers_list, "entered into func")
        source_numbers_list = source_numbers_list.split(",")
        if from_date is not None and to_date is not None:
            match_stage = {
                "$match": {
                    "source_number": {"$in": source_numbers_list},
                    'timestamp': {
                        '$gte': datetime.strptime(from_date, "%Y-%m-%dT%H:%M").timestamp(),
                        '$lte': datetime.strptime(to_date, "%Y-%m-%dT%H:%M").timestamp()},
                    '$or': [{'destination_number': {'$regex': '^[0-9]{0,10}$'}},
                            {'$and': [{'destination_number': {
                                '$regex': '^[0-9]{10}$'}}, {'duration': {'$gt': 0}}]},
                            {'destination_number': {'$exists': False}}
                            ]
                }
            }
        else:
            match_stage = {
                "$match": {
                    "source_number": {"$in": source_numbers_list},
                    'destination_number': {
                        '$regex': '^(91\\d{10}|\\d{10})$'
                    }
                }
            }
        pipeline = [
            # {
            #     "$match": {
            #         "source_number": {"$in": source_numbers_list},
            #         'destination_number': {
            #                         '$regex': '^(91\\d{10}|\\d{10})$'
            #                     }
            #     }
            # },
            match_stage,
            {
                "$group": {
                    "_id": "$destination_number",
                    "source_numbers": {"$addToSet": "$source_number"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$match": {
                    "source_numbers.1": {"$exists": True}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "destination_number": "$_id",
                    "source_numbers": 1,
                    "count": 1
                }
            }
        ]

        result = list(self.collection_cdrdata.aggregate(pipeline))
        print(result)
        print(len(result))
        if len(result) > 0:
            response = {'result': result, 'status': 'success',
                        'message': 'data retrived successfully'}
        else:
            response = {'result': [], 'status': 'empty',
                        'message': 'no data found'}

        return response

    def common_contact_hyperlink(self, destination, source):
        source_list = source.split(", ")
        print(source_list)
        print("--common hyper---")
        query = {
            'source_number': 1,
            'destination_number': 1,
            'timestamp': 1,
            'date': 1,
            'time': 1,
            'call_type': 1,
            'imei': 1,
            'duration': 1,
            'first_cgid': 1,
            'provider': 1,
            'roaming_circle': 1
        }
        result = list(self.collection_cdrdata.find(
            {'destination_number': destination, 'source_number': {'$in': source_list}}, query))
        print(len(result))
        cdr_data = []
        for document in result:
            suspectdata_match = self.collection_suspect.find_one(
                {'phone': document['destination_number']})
            sdrdata_match = self.collection_sdrdata.find_one(
                {'source_number': document['destination_number']})
            nickname = suspectdata_match['nickname'] if suspectdata_match else ''
            user_address = sdrdata_match['local_address'] if sdrdata_match else ''
            cellid_match = self.collection_cellid.find_one(
                {'celltowerid': document['first_cgid']})
            address = cellid_match['siteaddress'] if cellid_match else ''
            lat = cellid_match['lat'] if cellid_match else 0.0
            long = cellid_match['long'] if cellid_match else 0.0
            azimuth = cellid_match['azimuth'] if cellid_match else 0
            date = datetime.fromtimestamp(
                document['timestamp']).strftime('%d-%m-%Y')
            time_of_call = datetime.fromtimestamp(
                document['timestamp']).strftime('%H:%M:%S')
            cdr_data.append({
                'source_number': document['source_number'],
                'nickname': nickname,
                'destination_number': document['destination_number'],
                'calldate': date,
                'calltime': time_of_call,
                'call_type': document['call_type'],
                'duration': document['duration'],
                'imei': document['imei'],
                'cellid': document['first_cgid'],
                'provider': document['provider'],
                'roaming': document['roaming_circle'],
                'address': address,
                'latitude': lat,
                'longitude': long,
                'azimuth': azimuth,
                'user_address': user_address
            })
        headers = [k for k in cdr_data[0].keys()] if cdr_data else []
        if cdr_data:
            response = {'headers': headers, 'data_dict': cdr_data,
                        'status': 'success', 'message': 'data retrived successfully'}
        else:
            response = {'headers': headers, 'data_dict': 'Not Data matched',
                        'status': 'failure', 'message': 'no data found'}
        return response

    def common_handset(self, source_numbers_list, from_date=None, to_date=None):
        print("entered into handset", source_numbers_list, from_date, to_date)
        source_numbers_list = source_numbers_list.split(",")
        if from_date is not None and to_date is not None:
            print("entered into none")
            match_stage = {
                "$match": {
                    "source_number": {"$in": source_numbers_list},
                    'timestamp': {
                        '$gte': datetime.strptime(from_date, "%Y-%m-%dT%H:%M").timestamp(),
                        '$lte': datetime.strptime(to_date, "%Y-%m-%dT%H:%M").timestamp()},
                    '$or': [{'destination_number': {'$regex': '^[0-9]{0,10}$'}},
                            {'$and': [{'destination_number': {
                                '$regex': '^[0-9]{10}$'}}, {'duration': {'$gt': 0}}]},
                            {'destination_number': {'$exists': False}}
                            ]
                }
            }
        else:
            print("entered into not none")
            match_stage = {
                "$match": {
                    "source_number": {"$in": source_numbers_list},
                    'destination_number': {
                        '$regex': '^(91\\d{10}|\\d{10})$'
                    }
                }
            }
        cdr_pipeline = [
            # {
            #     "$match": {
            #         "source_number": {"$in": source_numbers_list},
            #         'destination_number': {
            #                     '$regex': '^(91\\d{10}|\\d{10})$'
            #                 }
            #     }
            # },
            match_stage,
            {
                "$group": {
                    "_id": "$imei",
                    "source_numbers": {"$addToSet": "$source_number"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$match": {
                    "source_numbers.1": {"$exists": True}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "imei": "$_id",
                    "source_numbers": 1,
                    "count": 1,
                    "from": "cdr"
                }
            }
        ]
        tower_pipeline = [
            {
                "$match": {
                    "source_number": {"$in": source_numbers_list},
                    'destination_number': {
                        '$regex': '^(91\\d{10}|\\d{10})$'
                    }
                }
            },
            {
                "$group": {
                    "_id": "$imei",
                    "source_numbers": {"$addToSet": "$source_number"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$match": {
                    "source_numbers.1": {"$exists": True}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "imei": "$_id",
                    "source_numbers": 1,
                    "count": 1,
                    "from": "tower-cdr"
                }
            }
        ]
        ipdr_pipeline = [
            {
                "$match": {
                    "msisdn": {"$in": source_numbers_list},
                    'destination_number': {
                        '$regex': '^(91\\d{10}|\\d{10})$'
                    }
                }
            },
            {
                "$group": {
                    "_id": "$imei",
                    "source_numbers": {"$addToSet": "$msisdn"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$match": {
                    "source_numbers.1": {"$exists": True}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "imei": "$_id",
                    "source_numbers": 1,
                    "count": 1,
                    "from": "ipdr"
                }
            }
        ]

        cdr_result = list(self.collection_cdrdata.aggregate(cdr_pipeline))
        tower_result = list(self.collection_cdrdata.aggregate(tower_pipeline))
        ipdr_result = list(self.collection_cdrdata.aggregate(ipdr_pipeline))
        result = cdr_result + ipdr_result + tower_result
        if len(result) > 0:
            response = {'result': result, 'status': 'success',
                        'message': 'data retrived successfully'}
        else:
            response = {'result': 'no data',
                        'status': 'empty', 'message': 'no data found'}

        return response

    def location_record(self, number, cellid, mode):
        query = {
            'source_number': 1,
            'destination_number': 1,
            'timestamp': 1,
            'date': 1,
            'time': 1,
            'call_type': 1,
            'imei': 1,
            'duration': 1,
            'first_cgid': 1,
            'provider': 1,
            'roaming_circle': 1
        }
        result = []
        if mode == "tower_day_calls":
            print("--common hyper---", number, cellid)
            start_time = datetime.strptime('06:00:00', '%H:%M:%S').time()
            end_time = datetime.strptime('18:00:00', '%H:%M:%S').time()

            # Set the time strings for the time range
            from_time_str = start_time.strftime('%H:%M:%S')
            to_time_str = end_time.strftime('%H:%M:%S')

            result = list(self.collection_cdrdata.find({'source_number': number, 'first_cgid': cellid, 'call_type': {
                          '$in': ['call_in', 'call_out']}, 'time': {'$gte': from_time_str, '$lte': to_time_str}}, query))
        if mode == "tower_night_calls":
            print(number, mode, cellid)
            start_time_1 = datetime.strptime('18:00:00', '%H:%M:%S').time()
            start_time_2 = datetime.strptime('23:59:59', '%H:%M:%S').time()
            from_time_str = start_time_1.strftime('%H:%M:%S')
            to_time_str = start_time_2.strftime('%H:%M:%S')
            # Query for the time range from 18:00:00 to 23:59:59
            night_hours_query_1 = {
                '$and': [
                    {'time': {'$gte': from_time_str}},
                    {'time': {'$lte': to_time_str}}
                ]
            }
            start_time_3 = datetime.strptime('00:00:00', '%H:%M:%S').time()
            start_time_4 = datetime.strptime('23:59:59', '%H:%M:%S').time()
            from_time_str_2 = start_time_3.strftime('%H:%M:%S')
            to_time_st_r_2 = start_time_4.strftime('%H:%M:%S')
            # Query for the time range from 00:00:00 to 06:00:00
            night_hours_query_2 = {
                '$and': [
                    {'time': {'$gte': from_time_str_2}},
                    {'time': {'$lte': to_time_st_r_2}}
                ]
            }

            result = list(self.collection_cdrdata.find({'source_number': number, 'first_cgid': cellid, 'call_type': {
                          '$in': ['call_in', 'call_out']}, '$or': [night_hours_query_1, night_hours_query_2]}, query))
            print(result, "---")

        if mode == "tower_total_calls":
            result = list(self.collection_cdrdata.find(
                {'source_number': number, 'first_cgid': cellid, 'call_type': {'$in': ['call_in', 'call_out']}}, query))

        cdr_data = []
        for document in result:
            suspectdata_match = self.collection_suspect.find_one(
                {'phone': document['destination_number']})
            sdrdata_match = self.collection_sdrdata.find_one(
                {'source_number': document['destination_number']})
            nickname = suspectdata_match['nickname'] if suspectdata_match else ''
            user_address = sdrdata_match['local_address'] if sdrdata_match else ''
            cellid_match = self.collection_cellid.find_one(
                {'celltowerid': document['first_cgid']})
            address = cellid_match['siteaddress'] if cellid_match else ''
            lat = cellid_match['lat'] if cellid_match else 0.0
            long = cellid_match['long'] if cellid_match else 0.0
            azimuth = cellid_match['azimuth'] if cellid_match else 0
            date = datetime.fromtimestamp(
                document['timestamp']).strftime('%d-%m-%Y')
            time_of_call = datetime.fromtimestamp(
                document['timestamp']).strftime('%H:%M:%S')
            cdr_data.append({
                'source_number': document['source_number'],
                'nickname': nickname,
                'destination_number': document['destination_number'],
                'calldate': date,
                'calltime': time_of_call,
                'call_type': document['call_type'],
                'duration': document['duration'],
                'imei': document['imei'],
                'cellid': document['first_cgid'],
                'provider': document['provider'],
                'roaming': document['roaming_circle'],
                'address': address,
                'latitude': lat,
                'longitude': long,
                'azimuth': azimuth,
                'user_address': user_address
            })
        # pprint(cdr_data)
        headers = [k for k in cdr_data[0].keys()] if cdr_data else []
        # headers = cdr_data[0].keys() if cdr_data else 'no data'
        response = {'headers': headers,
                    'data_dict': cdr_data if cdr_data else 'Not Data matched'}
        # print(response,"-----------------------")
        return response


# --------------------------------common link------------------------------#


    def get_common_link_using_area(self, source_numbers, fromdate=False, todate=False):
        print(source_numbers, fromdate, todate, "-------------")
        source_numbers = source_numbers.split(",")
        pipeline = [
            {
                "$match": {
                    "source_number": {"$in": source_numbers}
                }
            },
            {
                "$group": {
                    "_id": "$date",
                    "count": {"$sum": 1}
                }
            },
            {
                "$match": {
                    "count": {"$gte": len(source_numbers)}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "date": "$_id"
                }
            }
        ]
        common_dates = list(self.collection_cdrdata.aggregate(pipeline))

        print(common_dates)
        date_strings = [date_entry['date'] for date_entry in common_dates]

        date_dict = defaultdict(lambda: defaultdict(lambda: {
                                'source_numbers': set(), 'first_cgids': set(), 'state': set(), 'time': set()}))

        query = {
            '_id': 0,
            'source_number': 1,
            'date': 1,
            'time': 1,
            'first_cgid': 1
        }
        if fromdate != "undefined" and todate != "undefined":
            print("inside date filter")
            fromdate_def = int(datetime.strptime(
                fromdate, "%Y-%m-%d").timestamp())
            todate_def = int(datetime.strptime(todate, "%Y-%m-%d").timestamp())
            print(fromdate_def, todate_def)
            result = self.collection_cdrdata.find(
                {
                    'source_number': {'$in': source_numbers},
                    'date': {'$in': date_strings},
                    'timestamp': {
                        '$gte': fromdate_def,
                        '$lte': todate_def
                    }
                },
                projection=query
            ).sort([
                ('timestamp', 1),
                ('first_cgid', 1)
            ])
        else:
            print("inside common")
            result = self.collection_cdrdata.find(
                {
                    'source_number': {'$in': source_numbers},
                    'date': {'$in': date_strings}
                },
                projection=query
            ).sort([
                ('timestamp', 1),
                ('first_cgid', 1)
            ])

        date_dict = {}

        for item in result:
            date = item['date']
            time = item['time']
            source_number = item['source_number']
            first_cgid = item['first_cgid']

            result_cellid = self.collection_cellid.find_one(
                {'celltowerid': first_cgid})

            if result_cellid is not None:
                area = result_cellid.get('areadescription')
                state = result_cellid.get('state')

                if date not in date_dict:
                    date_dict[date] = {}

                if area not in date_dict[date]:
                    date_dict[date][area] = {
                        'state': state,
                        'source_numbers': {},
                        'cellid_data': {}
                    }

                if source_number not in date_dict[date][area]['source_numbers']:
                    date_dict[date][area]['source_numbers'][source_number] = {
                        'cellid_data': {}
                    }

                if first_cgid not in date_dict[date][area]['source_numbers'][source_number]['cellid_data']:
                    date_dict[date][area]['source_numbers'][source_number]['cellid_data'][first_cgid] = {
                        'time': []  # Assuming you only need time for each cellid
                    }

                date_dict[date][area]['source_numbers'][source_number]['cellid_data'][first_cgid]['time'].append(
                    time)
        meeting_list = []

        for date, area_set in date_dict.items():
            for area, data in area_set.items():
                state = data['state']
                source_numbers_dict = data['source_numbers']

                # Check if there's more than one unique source_number in the same date and area
                if len(source_numbers_dict) > 1:
                    source_numbers_list = []
                    for source_number, cellid_data in source_numbers_dict.items():
                        cellid_list = []
                        for cellid, cellid_data in cellid_data['cellid_data'].items():
                            cellid_list.append({
                                'cellid': cellid,
                                'time': cellid_data['time']
                            })

                        source_number_entry = {
                            'source_number': source_number,
                            'cellid_data': cellid_list
                        }
                        source_numbers_list.append(source_number_entry)

                    meeting_list.append({
                        'date': date,
                        'state': state,
                        'location': area,
                        'entry': source_numbers_list

                    })

        pprint(meeting_list)
        response = {'data_dict': meeting_list}
        return response
# --------------------------------------------------------------------------------#

    def calculate_missing_dates(self, start_timestamp, end_timestamp, data_timestamps):
        t = datetime.now()
        logger.info(f"start timing for caluclate missing dates {t}")
        start_date = datetime.fromtimestamp(start_timestamp)
        end_date = datetime.fromtimestamp(end_timestamp)
        all_dates = set()
        current_date = start_date
        while current_date <= end_date:
            all_dates.add(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
        data_dates = [datetime.fromtimestamp(timestamp).strftime(
            '%Y-%m-%d') for timestamp in data_timestamps]
        data_dates_set = set(data_dates)
        missing_dates = sorted(list(all_dates - data_dates_set))
        t2 = datetime.now()
        logger.info(f"end timing for caluclate missing dates {t2}")
        return missing_dates

    def silent_period(self, number, fromdate=None, todate=None):
        logger.info("In silent period", number, fromdate, todate)
        if fromdate is None and todate is None:
            if self.collection_cdrdata.count_documents({"source_number": number}) == 0:
                response = {'headers': "No data",
                            'data_dict': "No Data Available",
                            'status': 'failure',
                            'message': 'no data found'}
                return response
        else:
            if self.collection_cdrdata.count_documents({"source_number": number, 'timestamp': {
                '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                    '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()}}) == 0:
                response = {'headers': "No data",
                            'data_dict': "No Data Available",
                            'status': 'failure',
                            'message': 'no data found'}
                return response

        if fromdate is None and todate is None:
            number_pattern = re.compile(r'^\d{10}$|^91(\d{10})$')
            query = {'source_number': number,
                     'destination_number': {'$regex': number_pattern}}
            get_documents = self.collection_cdrdata.find(
                query, {'_id': 0, 'destination_number': 1})

        if fromdate is not None and todate is not None:
            print("---silent date range ---")
            number_pattern = re.compile(r'^\d{10}$|^91(\d{10})$')
            query = {'source_number': number,
                     'destination_number': {'$regex': number_pattern}, 'timestamp': {
                         '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                         '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()}}
            get_documents = self.collection_cdrdata.find(
                query, {'_id': 0, 'destination_number': 1})

        outputdict = {}
        outputlist = []

        for dest in get_documents:
            dest = dest['destination_number']
            if fromdate is None and todate is None:
                induvidual_data = self.collection_cdrdata.find(
                    {'source_number': number, 'destination_number': dest}).sort('timestamp', pymongo.ASCENDING)
            if fromdate is not None and todate is not None:
                induvidual_data = self.collection_cdrdata.find(
                    {'source_number': number, 'destination_number': dest, 'timestamp': {
                        '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                        '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()}}).sort('timestamp', pymongo.ASCENDING)

            other_number = dest
            if other_number not in outputdict:
                outputdict[other_number] = {'source_number': number, 'destination_number': other_number, 'nickname': '',
                                            'call_start_date': '', 'call_end_date': '', 'in': 0, 'out': 0, 'calls': 0, 'dur': 0, 'address': '', 'silent_period': 0}

            callduration = 0
            callin_count = 0
            callout_count = 0
            timestamps = []
            for value in induvidual_data:
                callduration += value['duration']
                if value["incoming"] == 1:
                    callin_count += 1
                elif value["incoming"] == 0:
                    callout_count += 1
                if value['timestamp'] not in timestamps:
                    timestamps.append(value['timestamp'])

            missing_dates = self.calculate_missing_dates(
                timestamps[0], timestamps[-1], timestamps)
            outputdict[other_number]['in'] = callin_count
            outputdict[other_number]['out'] = callout_count
            outputdict[other_number]['calls'] = callin_count + \
                callout_count
            outputdict[other_number]['dur'] = callduration
            outputdict[other_number]['call_start_date'] = datetime.fromtimestamp(
                timestamps[0]).strftime('%d-%m-%Y %H:%M:%S')
            outputdict[other_number]['call_end_date'] = datetime.fromtimestamp(
                timestamps[-1]).strftime('%d-%m-%Y %H:%M:%S')
            # outputdict[other_number]['missing_dates'] = missing_dates
            outputdict[other_number]['silent_period'] = len(missing_dates)

        outputlist = list(outputdict.values())
        response = {'data_dict': outputlist, 'status': 'success',
                    'message': 'data retrived successfully'}
        logger.info("function ends")
        return response

    # ------------------------------------------------------------------

    def lat_long_cdr_data(self, lat, long):
        if self.collection_cellid.count_documents({'lat': lat, 'long': long}) == 0:
            response = {'headers': 'No Data',
                        'status': 'empty', 'message': 'no data found'}
            return response
        matching_documents = self.collection_cellid.find({
            'lat': lat,
            'long': long
        })

        matching_documents_list = list(matching_documents)

        cdr_data = []
        for document in matching_documents_list:
            celltowerid = document.get('celltowerid', "")
            if not celltowerid:
                continue  # Skip documents without a valid 'celltowerid'

            # Query cdrdata collection with the celltowerid
            cdr_matches = self.collection_cdrdata.find(
                {"first_cgid": celltowerid})
            for cdr_match in cdr_matches:
                source_number = cdr_match['source_number']
                destination_number = cdr_match['destination_number']
                call_type = cdr_match['call_type']
                duration = cdr_match['duration']
                provider = cdr_match['provider']
                roaming = cdr_match['roaming_circle']
                timestamp = cdr_match['timestamp']
                sdr_match = self.collection_sdrdata.find_one(
                    {"source_number": source_number})
                nickname = sdr_match['nickname'] if sdr_match else ''
                address = sdr_match['local_address'] if sdr_match else ''
                call_timestamp = datetime.fromtimestamp(
                    timestamp).strftime('%Y-%m-%d %H:%M:%S')

                end_timestamp = timestamp + duration
                last_call_timestamp = datetime.fromtimestamp(
                    end_timestamp).strftime('%Y-%m-%d %H:%M:%S')

                cdr = {
                    'source_number': source_number,
                    'nickname': nickname,
                    'Destination_number': destination_number,
                    'Call_type': call_type,
                    'Duration': duration,
                    'Start_Time': call_timestamp,
                    'End_Time': last_call_timestamp,
                    'Provider': provider,
                    'Roaming': roaming,
                    'lat': lat,
                    'long': long,
                    'address': address
                }

                cdr_data.append(cdr)

            headers = list(cdr_data[0].keys())
            response = {'headers': headers,
                        'data_dict': cdr_data if cdr_data else "not Data Matched", 'status': 'success', 'message': 'data retrived successfully'}
            return response

    def cellid_data(self, data):
        print(data, "data")
        data = data.split(",")
        if self.collection_cellid.count_documents({'celltowerid': {'$in': data}}) == 0:
            response = {'headers': 'No Data', 'data_dict': 'Not data Matched',
                        'status': 'empty', 'message': "no data found"}
            return response
        else:

            matched_documents = self.collection_cellid.find(
                {'celltowerid': {'$in': data}})
            matched_documents_list = list(matched_documents)
            print(matched_documents_list)
            cellid_data = []

            for document in matched_documents_list:
                print(document)
                cellid = document.get('celltowerid')
                bts_id = document.get('bts_id')
                areadescription = document.get('areadescription')
                siteaddress = document.get('siteaddress')
                lat = document.get('lat')
                long = document.get('long')
                azimuth = document.get('azimuth')
                operator = document.get('operator')
                state = document.get('state')
                otype = document.get('otype')
                lastupdate = document.get('lastupdate')
                lastupdate_time = datetime.fromtimestamp(
                    lastupdate).strftime('%Y-%m-%d %H:%M:%S')
                cellid_list = {
                    'celltowerid': cellid,
                    'bts_id': bts_id,
                    'areadescription': areadescription,
                    'siteaddress': siteaddress,
                    'lat': lat,
                    'long': long,
                    'azimuth': azimuth,
                    'operator': operator,
                    'state': state,
                    'otype': otype,
                    'lastupdate': lastupdate_time
                }
                cellid_data.append(cellid_list)

            headers = list(cellid_data[0].keys()) if cellid_data else []

            response = {'headers': headers, 'data_dict': cellid_data,
                        'status': 'success', 'message': 'data retrived successfully'}

            return response

    def cdat_contacts(self, data):
        time1 = {'title':'Functions starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time()}
        time2 = {'title':'Mongo Query for cdat_count starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time()}
        count_cdat = self.cdat_count(data)
        print(count_cdat,"===================dfasdfasdfasd===============")
        time3 = {'title':'Query ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time() - time2['timestamp']}
        cdat = count_cdat#[0]['destination_numbers'] if len(count_cdat) >0 else []
        pipeline = [
            {
                "$match": {
                    'source_number': data,
                    'destination_number': {"$in": cdat}
                }
            },
            {
                "$group": {
                    "_id": {
                        'destination_number': "$destination_number",
                        'source_number': "$source_number"
                    },
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
                "$lookup": {
                    "from": "cdat_suspect",
                    "let": {"destination_number": "$_id.destination_number"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {"$eq": ["$phone", "$$destination_number"]}
                            }
                        }
                    ],
                    "as": "suspectData"
                }
            },
            {
                "$unwind": {
                    "path": "$suspectData",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$lookup": {
                    "from": "cdat_sdr",
                    "let": {"destination_number": "$_id.destination_number"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {"$eq": ["$source_number", "$$destination_number"]}
                            }
                        }
                    ],
                    "as": "sdrData"
                }
            },
            {
                "$unwind": {
                    "path": "$sdrData",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source_number": "$_id.source_number",
                    "destination_number": "$_id.destination_number",
                    "nickname": {"$ifNull": ["$suspectData.nickname", "Unknown"]},
                    "cat": {"$ifNull": ["$suspectData.category", "Unknown"]},
                    "io_name": {"$ifNull": ["$suspectData.inc_officer", "Unknown"]},
                    "address": {"$ifNull": ["$sdrData.local_address", "no address found"]},
                    "call_in": 1,
                    "call_out": 1,
                    "total_calls": 1,
                    "duration": 1,
                    "first_call": 1,
                    "last_call": 1
                }
            }
        ]
        time4 = {'title':'Mongo aggrgation for cdat_contacts starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time()}
        result = list(self.collection_cdrdata.aggregate(pipeline))
        time5 = {'title':'Mongo aggrgation for cdat_contacts ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time() - time4['timestamp']}

        time6 = {'title':'function ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time() - time1['timestamp']}
        if result:
            
            response = {'headers': ['source_number', 'destination_number', 'nickname', 'cat', 'call_in', 'call_out', 'total_calls', 'duration', 'first_call', 'last_call', 'address', 'io_name'],
                        'data_dict': result, 'status': 'success', 'message': 'data retrived successfully','times':[time1,time2,time3,time4,time5,time6]}
        else:
            response = {'data_dict': 'Not data Matched',
                        'status': 'failure', 'message': 'no data found','times':[time1,time2,time3,time4,time5,time6]}
        return response

    def second_level_cdat(self, data):
        # Find all unique source numbers in the collection
        unique_source_numbers = self.collection_cdrdata.distinct(
            'source_number')

        # Initialize an empty dictionary to store the consolidated data
        overall_all = {}
        for source_number in unique_source_numbers:
            matching_destination_documents = self.collection_cdrdata.find(
                {'destination_number': source_number, 'source_number': data})
            matching_destination_documents_list = list(
                matching_destination_documents)

            for source in matching_destination_documents_list:
                second_source = source['destination_number']
                for unique_source_number in unique_source_numbers:
                    second_level = self.collection_cdrdata.find(
                        {'source_number': second_source, 'destination_number': unique_source_number})
                    result_dict = {}
                    for item in second_level:
                        source_number = item['source_number']
                        destination_number = item['destination_number']

                        # Check if the destination_number already exists in the result_dict
                        if destination_number in result_dict:
                            # If it exists, update the existing data
                            result = result_dict[destination_number]
                            result['call_in'] += 1 if item['incoming'] == 1 else 0
                            result['call_out'] += 1 if item['incoming'] == 0 else 0
                            result['Duration'] += item['duration']
                            # result['nickname'] = nickname
                            # result['address'] = address

                            if item['timestamp'] < result['first_call_timestamp']:
                                result['first_call_timestamp'] = item['timestamp']

                            if item['timestamp'] > result['last_call_timestamp']:
                                result['last_call_timestamp'] = item['timestamp']
                        else:
                            # If it doesn't exist, create a new entry in the result_dict
                            result_dict[destination_number] = {
                                'source_number': source_number,
                                'destination_number': destination_number,
                                # 'nickname': nickname,
                                'call_in': 1 if item['incoming'] == 1 else 0,
                                'call_out': 1 if item['incoming'] == 0 else 0,
                                'Duration': item['duration'],
                                'first_call_timestamp': item['timestamp'],
                                'last_call_timestamp': item['timestamp'],
                                # 'address': address
                            }

                    for destination_number, result in result_dict.items():
                        # Convert the first_call_timestamp and last_call_timestamp to datetime and format them
                        result['first_call'] = datetime.fromtimestamp(
                            result['first_call_timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                        result['last_call'] = datetime.fromtimestamp(
                            result['last_call_timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                        sdr_match = self.collection_suspect.find_one(
                            {'phone': destination_number})
                        nickname = sdr_match['nickname'] if sdr_match else ''
                        address = sdr_match['address'] if sdr_match else ''
                        result['nickname'] = nickname
                        result['address'] = address
                        overall_all[destination_number] = result
        if overall_all:
            data_dict = list(overall_all.values()
                             )
            response = {'headers': ['source_number', 'destination_number', 'nickname', 'call_in', 'call_out', 'Duration', 'First call', 'Last call', 'address'],
                        'data_dict': data_dict, 'status': 'success', 'message': 'data retrived successfully'}
        else:
            response = {'headers': 'no data',
                        'data_dict': 'Not data Matched', 'status': 'failure', 'message': 'no data found'}
        return response

    def single_address(self, data):
        logger.info(f"Adress search for {data}")
        single_num = data.split(",")
        output_list = []
        out_dict = {}
        for num in single_num:
            sdr_num = self.collection_sdrdata.find_one(
                {'source_number': str(num)})
            if num not in out_dict and sdr_num is not None:
                out_dict[num] = {
                    'source_number': sdr_num.get('source_number', ''),
                    'name': sdr_num.get('fullname', ''),
                    # 'first_call': [datetime.fromtimestamp(f_c['timestamp']).strftime('%Y-%m-%d %H:%M:%S') for f_c in self.collection_cdrdata.find({'source_number': num}).sort('timestamp', pymongo.ASCENDING).limit(1)],
                    # 'last_call': [datetime.fromtimestamp(l_c['timestamp']).strftime('%Y-%m-%d %H:%M:%S') for l_c in self.collection_cdrdata.find({'source_number': num}).sort('timestamp', pymongo.DESCENDING).limit(1)],
                    'nickname': [nk['nickname'] for nk in self.collection_suspect.find({'phone': str(num)}).sort('timestamp', pymongo.DESCENDING).limit(1)],
                    'module_name': [mn['module_name'] for mn in self.collection_suspect.find({'phone': str(num)}).sort('timestamp', pymongo.DESCENDING).limit(1)],
                    'last_updated': [l_u['as_on_date'] for l_u in self.collection_suspect.find({'phone': str(num)}).sort('timestamp', pymongo.DESCENDING).limit(1)],
                    'local_address': sdr_num.get('local_address', ''),
                    'permanent_address': sdr_num.get('permanent_address', '')

                }
                output_list.append(out_dict[num])

        headers = [k for k in output_list[0].keys(
        )] if output_list else "No Data"
        response = {'headers': headers, 'data_dict': output_list,
                    'status': 'success', 'message': 'data retrived successfully'}
        print(response)
        logger.info(f"Ends")

        return response

    def cdr_btw_multilevel(self, data, mode, fromdate, todate, items=False, currentpage=False):
        print(data)
        data_list = data.split(",")

        multi_cdr = []  # Create an empty list to store all the data
        print(mode, data, items, currentpage,fromdate, "-----in totals calls,cdr")
        items_per_page = int(items)
        current_page = int(currentpage)
        skip_doc = int(items_per_page) * (int(current_page) - 1)
        total_count = 0
        src_num = data_list
        if fromdate is None:
            for source_number in data_list:
                for destination_number in data_list:
                    if source_number != destination_number:
                        total_count += self.collection_cdrdata.count_documents(
                            {'source_number': source_number, 'destination_number': destination_number})
        if fromdate is not None:
            for source_number in data_list:
                for destination_number in data_list:
                    if source_number != destination_number:
                        total_count += self.collection_cdrdata.count_documents(
                            {'source_number': source_number, 'destination_number': destination_number, 'timestamp': {
                                '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                                '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                            }})
        
        if mode == "CdrBtwmultipleNumber" or mode == "loopcalls":
            print(mode)
            # Loop through each source_number in data_list
            for source_number in data_list:
                # Loop through each destination_number (except the current source_number)
                for destination_number in data_list:
                    if source_number != destination_number:
                        if fromdate is None:
                            matching_documents = self.collection_cdrdata.find(
                                {'source_number': source_number, 'destination_number': destination_number}).sort('timestamp', 1)
                        if fromdate is not None:
                            matching_documents = self.collection_cdrdata.find(
                                {'source_number': source_number, 'destination_number': destination_number, 'timestamp': {
                                    '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                                    '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                                }}).sort('timestamp', 1)

                        sdr_match = self.collection_sdrdata.find_one(
                            {'source_number': destination_number})
                        suspect_nickname = self.collection_suspect.find_one(
                            {'phone': destination_number})
                        nickname = suspect_nickname.get(
                            'nickname') if suspect_nickname else ''
                        user_address = sdr_match.get(
                            'local_address') if sdr_match else ''
                        # Create a list to store the documents for the current combination
                        number_documents = []

                        for document in matching_documents:
                            print(document)
                            timestamp = document['timestamp']
                            calldate = datetimeasnow.datetime.fromtimestamp(
                                timestamp).strftime('%Y-%m-%d')
                            calltime = datetimeasnow.datetime.fromtimestamp(
                                timestamp).strftime('%H:%M:%S')
                            call_type = document['call_type']
                            duration = document['duration']
                            imei = document['imei']
                            cellid = document['first_cgid']
                            provider = document['provider']
                            roaming = document['roaming_circle']

                            if mode == "loopcalls":
                                fromdate_obj = datetime.strptime(
                                    fromdate, '%Y-%m-%d')
                                todate_obj = datetime.strptime(
                                    todate, '%Y-%m-%d')
                                # doc_date_obj = datetime.fromtimestamp(timestamp / 1000)
                                doc_date_obj = datetime.fromtimestamp(
                                    timestamp)

                                if doc_date_obj < fromdate_obj or doc_date_obj > todate_obj:
                                    continue

                            # Query the other collection for matching cellid
                            cellid_match = self.collection_cellid.find_one(
                                {'celltowerid': cellid})
                            # print(cellid_match, "cellid_match")
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

                            cdr = {
                                'source_number': source_number,
                                'nickname': nickname,
                                'destination_number': destination_number,
                                'calldate': calldate,
                                'calltime': calltime,
                                'call_type': call_type,
                                'duration': duration,
                                'imei': imei,
                                'cellId': cellid,
                                'provider': provider,
                                'roaming': roaming,
                                'address': address,
                                'latitude': lat,
                                'longitude': long,
                                'azimuth': azimuth,
                                'user_address': user_address
                            }
                            # Append the cdr dictionary for each matching document
                            number_documents.append(cdr)

                        # Append the documents for the current combination to the multi_cdr list
                        multi_cdr.extend(number_documents)
                        # print(multi_cdr, "-----------")
        if mode == "loopcalls":
            multi_cdr.sort(key=lambda x: x['calldate'] + ' ' + x['calltime'])
        print(len(multi_cdr), "---")
        if len(multi_cdr) > 0:
            response = {
                'headers': ['source_number', 'nickname', 'destination_number', 'calldate', 'calltime', 'call_type', 'duration', 'imei', 'cellId',
                            'Provider', 'Roaming', 'Address', 'Latitude', 'Longitude', 'azimuth', 'user_address'],
                'data_dict': multi_cdr, 'totalpages': total_count, 'status': 'success', 'message': 'data retrived successfully'
            }
            return response
        else:
            response = {'header': "no Data", 'data_dict': 'Not Data Matched',
                        'status': 'failure', 'message': 'no data found'}
            return response
            # print(response)

    def multi_cdr_data(self, data, fromdate=None, todate=None, items=False, currentpage=False):
        print(data, items, currentpage, fromdate,
              todate, "-----in totals calls,cdr")
        print(data, "data")
        data_list = data.split(",")
        multi_cdr = []  # Create an empty list to store all the data
        if items == "false":
            skip_doc = False
            items_per_page = False
        else:
            items_per_page = int(items)
            current_page = int(currentpage)
            skip_doc = int(items_per_page) * int(current_page)
        total_count = 0
        if fromdate is None:
            for number in data_list:
                total_count += self.collection_cdrdata.count_documents(
                    {'source_number': number})
        if fromdate is not None:
            for number in data_list:
                total_count += self.collection_cdrdata.count_documents(
                    {'source_number': number,
                     'timestamp': {
                         '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                         '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                     }
                     })

        for number in data_list:
            if fromdate is None:
                matching_documents = self.collection_cdrdata.find(
                    {'source_number': number}).sort('timestamp', 1)
            if fromdate is not None:
                matching_documents = self.collection_cdrdata.find(
                    {'source_number': number, 'timestamp': {
                        '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                        '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                    }}).sort('timestamp', 1)
            # print(list(matching_documents))
            sdr_match = self.collection_sdrdata.find_one(
                {"source_number": number})
            suspect_nickname_list = list(self.collection_suspect.find(
                {'phone': number}).sort('timestamp', pymongo.DESCENDING).limit(1))
            # suspect_nickname_list = list(suspect_nickname_cursor)
            suspect_nickname = suspect_nickname_list[0] if suspect_nickname_list else None
            nickname = suspect_nickname.get(
                'nickname') if suspect_nickname else ''

            user_address = sdr_match.get('local_address') if sdr_match else ''
            # print(matching_documents, "multi")

            # Create a list to store the documents for the current number
            number_documents = []

            for document in matching_documents:
                destination_number = document['destination_number']
                calldate = datetime.fromtimestamp(
                    document['timestamp']).strftime('%d-%m-%Y %H:%M:%S')
                call_type = document['call_type']
                duration = document['duration']
                imei = document['imei']
                cellid = document['first_cgid']
                provider = document['provider']
                roaming = document['roaming_circle']

                # Query the other collection for matching cellid
                cellid_match = self.collection_cellid.find_one(
                    {'celltowerid': cellid})
                # print(cellid_match, "cellid_match")
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

                cdr = {
                    'source_number': number,
                    'nickname': nickname,
                    'destination_number': destination_number,
                    'calldate': calldate,
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
                    'user_address': user_address
                }
                # Append the cdr dictionary for each matching document
                number_documents.append(cdr)

            # Append the documents for the current number to the multi_cdr list
            multi_cdr.extend(number_documents)
            multi_cdr_sorted = sorted(multi_cdr, key=lambda x: (x['calldate']))
            pprint(multi_cdr_sorted)
        if multi_cdr_sorted:
            response = {
                'headers': ['source_number', 'nickname', 'destination_number', 'calldate', 'call_type', 'duration', 'imei', 'cellid',
                            'provider', 'roaming', 'address', 'latitude', 'longitude', 'azimuth', 'user_address'],
                'data_dict': multi_cdr_sorted,
                'status': 'success',
                'message': 'data retrived successfully'
            }
        else:
            response = {'data_dict': 'No data Matched',
                        'status': 'failure', 'message': 'no data found'}

        return response

    def callin_callout(self, data, mode, imei, other_number=False, fromdate=False, todate=False, state=False):
        print(data, mode, imei, other_number,
              other_number, fromdate, todate, state)
        mode = 1 if mode == "call_in" else 0
        print(mode, "---")
        matching_documents = []
        if other_number == "undefined":

            print(("in asdfasdfsdf"))
            matching_documents = self.collection_cdrdata.find(
                {'source_number': data, 'incoming': mode, 'imei': imei})
        if fromdate and todate:
            matching_documents = list(self.collection_cdrdata.find(
                {'source_number': data, 'destination_number': other_number, 'incoming': mode,
                 'timestamp': {
                     '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                     '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                 }}))
            print(matching_documents)
        if state:
            if fromdate and todate:
                matching_documents = list(self.collection_cdrdata.find(
                    {'source_number': data, 'destination_number': other_number, 'state': state, 'incoming': mode,
                     'timestamp': {
                         '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                         '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                     }}))
                print(matching_documents)
            else:
                matching_documents = self.collection_cdrdata.find(
                    {'source_number': data, 'destination_number': other_number, 'state': state, 'incoming': mode, })

        else:
            matching_documents = self.collection_cdrdata.find(
                {'source_number': data, 'destination_number': other_number, 'incoming': mode, })
            # matching_documents_list = list(matching_documents)
            # print(matching_documents,"cdr match doc")
        cdr_data = []
        cdr = None
        for document in matching_documents:
            destination_number = document['destination_number']
            calldate = datetime.fromtimestamp(
                document['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            # calltime = document['time']
            call_type = document['call_type']
            duration = document['duration']
            imei = document['imei']
            cellid = document['first_cgid']
            provider = document['provider']
            roaming = document['roaming_circle']
            nickname = [nickname.get('nickname', '') for nickname in self.collection_suspect.find(
                {'phone': destination_number}).sort('timestamp', pymongo.ASCENDING).limit(-1)]
            user_address = [user_address.get('permanent_address', '') for user_address in self.collection_sdrdata.find(
                {'source_number': destination_number}).sort('timestamp', pymongo.ASCENDING).limit(-1)]

            # Query the other collection for matching cellid
            cellid_match = self.collection_cellid.find_one(
                {'celltowerid': cellid})
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
            cdr = {
                'source_number': data,
                'nickname': nickname,
                'destination_number': destination_number,
                'calldate': calldate,
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
                'user_address': user_address
            }
            cdr_data.append(cdr)

            # print(cdrimei_data,"cdr")

        headers = [k for k in cdr_data[0].keys()] if cdr_data else "No Data"
        response = {'headers': headers, 'data_dict': cdr_data}
        # print(response,"---------------")

        return response

    def ipdr_details(self, data, fromdate, todate, items, currentpage):
        print(fromdate, todate, currentpage,
              "----------------ijcdiudhhdhubchsdbhcbdshb----------------------------")
        total_pages = 0
        if items == "false":
            skip_doc = False
            items_per_page = False
            current_page = False
        else:
            items_per_page = int(items)
            current_page = int(currentpage)
            skip_doc = int(items_per_page) * (int(current_page))

        matching_documents = []
        if fromdate == "" and todate == "":
            total_pages = self.collection_ipdr.count_documents(
                {'msisdn': data})
            if items_per_page == False and current_page == False:
                matched_documents = self.collection_ipdr.find(
                    {'msisdn': data}).sort('timestamp', pymongo.DESCENDING)
            else:
                if current_page > 0:
                    skip_doc = (current_page - 1) * items_per_page
                    print(
                        skip_doc, "---------------------skip_doc,current_page''''''''")
                matched_documents = self.collection_ipdr.find({'msisdn': data}).sort(
                    'timestamp', pymongo.DESCENDING).skip(skip_doc).limit(items_per_page)
            # print(len(matched_documents),"-outside time")
        elif fromdate != "" and todate != "":
            total_pages = self.collection_ipdr.count_documents(
                {
                    'msisdn': data,
                    'time': {
                        '$gte': datetime.combine(fromdate_obj, datetime.min.time()),
                        '$lte': datetime.combine(todate_obj, datetime.max.time())
                    }
                })
            # Convert string dates to datetime objects
            fromdate_obj = datetime.strptime(fromdate, "%Y-%m-%dT%H:%M")
            todate_obj = datetime.strptime(todate, "%Y-%m-%dT%H:%M")
            if items_per_page == False and current_page == False:
                # Use the time field for filtering, considering only the date part
                matched_documents = list(self.collection_ipdr.find({
                    'msisdn': data,
                    'time': {
                        '$gte': datetime.combine(fromdate_obj, datetime.min.time()),
                        '$lte': datetime.combine(todate_obj, datetime.max.time())
                    }
                }))
            else:
                matched_documents = list(self.collection_ipdr.find({
                    'msisdn': data,
                    'time': {
                        '$gte': datetime.combine(fromdate_obj, datetime.min.time()),
                        '$lte': datetime.combine(todate_obj, datetime.max.time())
                    }
                }).sort('timestamp', pymongo.DESCENDING).skip(skip_doc).limit(items_per_page))

            # print(len(matched_documents),"-inside time")

        ipdr_list = []
        for document in matched_documents:
            destination_ip = document['destination_ip']
            destination_port = document['destination_port']
            source_ip = document['source_ip']
            source_port = document['source_port']
            cellid = document['cell_id']
            # celllocation = document['celllocation']
            vendor = document['provider']
            start_time = document['time']
            end_time = document['time_et']
            duration = end_time - start_time
            # ipinfo = document['ipinfo']
            home_circle = document['roaming']
            provider = document['provider']
            company = document['company']
            domain = document['domain']
            vpn = document['is_vpn']
            ip_type = document['com_type']
            dwnLink = int(
                document['downlink_vol']) if document['downlink_vol'] != "None" and document['downlink_vol'] != "" else 0
            upLink = int(
                document['uplink_vol']) if document['uplink_vol'] != "None" and document['uplink_vol'] != "" else 0
            total_usage = upLink + dwnLink
            usage = self.convert_size(total_usage)
            # if document['downlink_vol'] != "None" and document['uplink_vol'] != "None":
            #     datausage = int(document['downlink_vol']) + int(document['uplink_vol'])
            ipdr = {
                'msisdn': data,
                'source_ip': source_ip,
                'source_port': source_port,
                'destination_ip': destination_ip,
                'destination_port': destination_port,
                'cgid': cellid,
                # 'celllocation': celllocation,
                'start_time': start_time,
                'end_time': end_time,
                'duration': str(duration),
                # 'ipinfo': ipinfo,
                'company': company,
                'domain': domain,
                'vpn': vpn,
                'datausage': usage,
                'ip_type': ip_type,
                'home_circle': home_circle,
                'provider': provider
            }
            ipdr_list.append(ipdr)
        headers = [k for k in ipdr_list[0].keys()] if ipdr_list else "No Data"
        response = {'headers': headers, 'data_dict': ipdr_list, 'totalpages': total_pages,
                    'status': 'success', 'message': 'data retrived successfully'}
        return response

    def rh_details(self, data):
        if mongocdat.rhdata.find({'msisdn': {"$in": data}}) == 0:
            response = {'headers': 'No Data'}
            return response
        else:
            matched_documents = mongocdat.rhdata.find(
                {'MSISDN': data})
            rh_list = []
            for document in matched_documents:
                amount = document['Recharge Amount']
                mor = document['Mode of Recharge']
                dealerid = document['Dealer ID']
                dealername = document['Dealer Name']
                dealeradd = document['Dealer Address']
                dealercontact = document['Dealer Contact']
                date = document['Date']
                time_of_doc = document['Time']
                transac_detail = document['Transaction Details']
                circle = document['Circle']

                rh = {
                    'Phone': data,
                    'Recharge Amount': amount,
                    'Mode of Recharge': mor,
                    'Dealer ID': dealerid,
                    'Dealer Name': dealername,
                    'Dealer Address': dealeradd,
                    'Dealer Contact': dealercontact,
                    'Date': date,
                    'Time': time_of_doc,
                    'Transaction Details': transac_detail,
                    'Circle': circle
                }
                rh_list.append(rh)
            headers = [k for k in rh_list[0].keys()] if rh_list else "No Data"
            response = {'headers': headers, 'data_dict': rh_list}
            return response

    def sm_rh(self, data, fromdate=False, todate=False):
        """
        description : same date recharge 

        """
        print(data, "data_dict")
        data = data.split(",")
        print(data, "Datas")
        getdata = []
        if fromdate is None and todate is None:
            query = {'msisdn': {"$in": data}}
        else:
            query = {'msisdn': {"$in": data},
                     'timestamp': {
                '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()}
            }

        getdata.extend(mongocdat.rhdata.find(query))
        if len(getdata) == 0:
            response = {'data_dict': [], 'status': 'empty',
                        'message': 'no data found'}
            return response
        else:
            distinct_dates = mongocdat.rhdata.distinct(
                'date', {'msisdn': {"$in": data}})
            rh_list = mongocdat.rhdata.distinct(
                'retailer_msisdn', {'msisdn': {"$in": data}})
            if fromdate is not None and todate is not None:
                matched_documents = mongocdat.rhdata.find({'retailer_msisdn': {"$in": rh_list},
                                                           'date': {'$in': distinct_dates},
                                                           'timestamp': {
                    '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                    '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                }
                })
            else:
                matched_documents = mongocdat.rhdata.find({'retailer_msisdn': {"$in": rh_list},
                                                           'date': {'$in': distinct_dates}
                                                           })

            rh_list = []
            for document in matched_documents:
                msisdn = document['msisdn']
                amount = document['recharge_amount']
                mode = document['recharge_type']
                dealername = document['dealer_name']
                dealeradd = document['dealer_address']
                dealercontact = document['retailer_msisdn']
                date = document['date_format']
                transac_detail = document['transcation_details']
                circle = document['subscriber_circle']
                provider = document['provider']
                rh = {
                    'Phone': msisdn,
                    'recharge_amount': amount,
                    'mode_of_recharge': mode,
                    'dealername': dealername,
                    'dealer_address': dealeradd,
                    'dealer_contact': dealercontact,
                    'date': date,
                    'transaction_details': transac_detail,
                    'circle': circle,
                    'provider': provider
                }
                rh_list.append(rh)
            pprint(rh_list)
            response = {'status': 'success', 'data_dict': rh_list}
            return response

    def poa_search(self, data):
        if self.collection_poadata.count_documents({'TELEPHONE_NUMBER': int(data)}) == 0:
            response = {'headers': 'No Data'}
            return response
        else:
            matched_documents = self.collection_poadata.find(
                {'TELEPHONE_NUMBER': int(data)})
            poa_list = []

            for document in matched_documents:
                caf_no = document['CAF_SERIAL_NO']
                user = document['NAME_OF_SUBSCRIBER']
                loc_address = f"{document['LOC_ADDR_HOUSENO_FLATNO']} {document['LOC_ADDR_STREET_ADDR_NAME']}, {document['LOC_ADDR_CITY']}, {document['LOC_ADDR_STATE_UT']} {document['LOC_ADDR_POSTL_CODE']}"
                imsi = document['IMSI']
                circel_name = document['CIRCLE_NAME']
                sim_active_date = document['SIM_ACTIVATION_DATE']
                sim_active_time = document['SIM_ACTIVATION_TIME']
                agent_name = document['POS_AGENT_NAME']
                agent_address = f"{document['POS_HOUSENO_FLATNO']} {document['POS_STREET_ADDR_NAME']} {document['POS_LOCALITY']} {document['POS_CITY']} {document['POS_STATE_UT']} {document['POS_POSTL_CODE']}"

                poa = {
                    'PHONE': data,
                    'SUBSCRIBER': user,
                    'CAF_SERIAL_NO': caf_no,
                    'Loc_Address': loc_address,
                    'imsi': imsi,
                    'circel_name': circel_name,
                    'sim_active_date': sim_active_date,
                    'sim_active_time': sim_active_time,
                    'agent_name': agent_name,
                    'agent_address': agent_address
                }
                poa_list.append(poa)
            headers = [k for k in poa_list[0].keys()] if poa_list else []
            response = {'headers': headers, 'data_dict': poa_list}
            return response

    def gprs_details(self, data, items, currentpage):
        items_per_page = int(items)
        current_page = int(currentpage)
        skip_doc = int(items_per_page) * (int(current_page) - 1)
        total_pages = self.collection_gprs.count_documents({'msisdn': data})
        # .sort('start_timestamp', pymongo.ASCENDING).skip(skip_doc).limit(items_per_page)
        matched_documents = self.collection_gprs.find({'msisdn': data})

        gprs_list = []
        for document in matched_documents:
            ip_address = document['destination_ip']
            cell1 = document['cell_id']
            imei = document['imei']
            imsi = document['imsi']
            downlink_vol = document['downlink']
            uplink_vol = document['uplink']
            # total_vol = document['total_vol']
            start_time = document['time']
            end_time = document['time_et']
            # type_of_recharge = document['Pre/Post']
            roaming = document['roaming']
            # network = document['2G/3G']
            # roaming_net = document['Roaming Network Indicator']
            # home_circle = document['Home_Circle']

            gprs = {
                'source_number': data,
                'ip_address': ip_address,
                'cgid': cell1,
                'imei': imei,
                'imsi': imsi,
                'downlink_vol': downlink_vol,
                'uplink_vol': uplink_vol,
                # 'total_vol': total_vol,
                'start_time': start_time,
                'end_time': end_time,
                # 'type': type_of_recharge,
                'roaming': roaming,
                # 'Network': network,
                # 'Roaming_Network': roaming_net,
                # 'Home_circle': home_circle
            }
            gprs_list.append(gprs)

        headers = [k for k in gprs_list[0].keys()] if gprs_list else "No Data"
        response = {'headers': headers,
                    'data_dict': gprs_list, 'totalpages': total_pages, 'status': 'success', 'message': 'data retrived successfully'}
        print(response)
        return response

    def ipdr_gprs_cdr(self, data, fromdate=None, todate=None):
        print("----------------------")
        print(data, fromdate, todate, "-----uyfuyf--")
        if fromdate is None:
            print("inside")
            cdr_documents = self.collection_cdrdata.find(
                {'source_number': data})
            ipdr_documents = self.collection_ipdr.find({'msisdn': data})
            gprs_documents = self.collection_gprs.find({'msisdn': data})
        if fromdate is not None:
            print("inside date range")
            fromdate_obj = datetime.strptime(fromdate, "%Y-%m-%dT%H:%M")
            todate_obj = datetime.strptime(todate, "%Y-%m-%dT%H:%M")
            cdr_documents = self.collection_cdrdata.find({'source_number': data, 'timestamp': {
                '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
            }})
            ipdr_documents = self.collection_ipdr.find({'msisdn': data, 'time': {
                '$gte': datetime.combine(fromdate_obj, datetime.min.time()),
                '$lte': datetime.combine(todate_obj, datetime.max.time())
            }})
            gprs_documents = self.collection_gprs.find({'msisdn': data, 'time': {
                '$gte': datetime.combine(fromdate_obj, datetime.min.time()),
                '$lte': datetime.combine(todate_obj, datetime.max.time())
            }})

        cdr_data = []
        ipdr_data = []
        gprs_data = []
        cdr = None
        for document in cdr_documents:
            # print("--```````````````````````````````````---")
            destination_number = document['destination_number']
            calldate = datetime.fromtimestamp(
                document['timestamp']).strftime("%d/%m/%Y %H:%M:%S")
            call_type = document['call_type']
            duration = document['duration']
            imei = document['imei']
            cellid = document['first_cgid']
            provider = document['provider']
            roaming = document['roaming_circle']
            # Query the other collection for matching cellid
            cellid_match = self.collection_cellid.find_one(
                {'celltowerid': cellid})
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
            sdrfinds = self.collection_sdrdata.find_one(
                {'source_number': destination_number})
            # nickname = "Not available"
            # adresssdr = "Not available"
            if sdrfinds is not None:
                nickname = sdrfinds.get('nickname')
                adresssdr = sdrfinds.get('local_address')
            else:
                nickname = ""
                adresssdr = ""
            cdr = {
                'source_number': data,
                'nickname': nickname,
                'destination_number': destination_number,
                'calldate': calldate,
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
        for document in ipdr_documents:
            destination_ip = document['destination_ip']
            destination_port = document['destination_port']
            source_ip = document['source_ip']
            source_port = document['source_port']
            cellid = document['cell_id']
            # celllocation = document['celllocation']
            # vendor = document['provider']
            start_time = document['time']
            end_time = document['time_et']
            # ipinfo = document['ipinfo']
            home_circle = document['state']
            provider = document['provider']

            ipdr = {
                'msisdn': data,
                'destination_ip': destination_ip,
                'destination_port': destination_port,
                'source_ip': source_ip,
                'source_port': source_port,
                'cgid': cellid,
                # 'celllocation': celllocation,
                # 'vendor': vendor,
                'start_time': start_time,
                'end_time': end_time,
                # 'ipinfo': ipinfo,
                'home_roaming_circle': home_circle,
                'provider': provider
            }
            ipdr_data.append(ipdr)
        for document in gprs_documents:
            print(document, "-----333--------")
            ip_address = document['source_ip']
            cell1 = document['cgid']
            imei = document['imei']
            imsi = document['imsi']
            downlink_vol = document['downlink_vol']
            uplink_vol = document['uplink_vol']
            total_vol = document['total_vol']
            start_time = document['start_time']
            end_time = document['end_time']
            # type_of_recharge = document['Pre/Post']
            roaming = document['roaming_circle']
            # network = document['2G/3G']
            roaming_net = document['roaming_circle']
            home_circle = document['home_circle']

            gprs = {
                'msisdn': data,
                'source_ip': ip_address,
                'cgid': cell1,
                'imei': imei,
                'imsi': imsi,
                'downlink_vol': downlink_vol,
                'uplink_vol': uplink_vol,
                'total_vol': total_vol,
                'start_time': start_time,
                'end_time': end_time,
                # 'type': type_of_recharge,
                'roaming_circle': roaming,
                # 'Network': network,
                'provider': roaming_net,
                'home_circle': home_circle
            }
            gprs_data.append(gprs)
        cdr_headers = [
            k for k in cdr_data[0].keys()] if cdr_data else "No Data"
        ipdr_headers = [
            k for k in ipdr_data[0].keys()] if ipdr_data else "No Data"
        gprs_headers = [
            k for k in gprs_data[0].keys()] if gprs_data else "No Data"

        # Handle missing headers or empty datasets
        if not cdr_headers:
            cdr_headers = ['source_number', 'nickname', 'destination_number', 'calldate', 'call_type', 'duration',
                           'imei', 'cellid', 'provider', 'roaming', 'address', 'latitude', 'longitude', 'azimuth', 'user_address']
        if not ipdr_headers:
            ipdr_headers = ['msisdn', 'destination_ip', 'destination_port', 'source_ip',
                            'source_port', 'cgid', 'provider', 'start_time', 'end_time', 'home_circle']
        if not gprs_headers:
            gprs_headers = ['msisdn', 'source_ip', 'cgid', 'imei', 'imsi', 'downlink_vol', 'uplink_vol',
                            'total_vol', 'start_time', 'end_time', 'roaming_circle', 'provider', 'home_circle']

        response = {
            'cdr_headers': cdr_headers,
            'ipdr_headers': ipdr_headers,
            'gprs_headers': gprs_headers,
            'cdr_data': cdr_data[:10],
            'ipdr_data': ipdr_data[:10],
            'gprs_data': gprs_data[:10]
        }
        # print(response)
        return response

    def nickname_search(self, data, mode, nickname=False, address=False, state=False):

        # Convert the data to lowercase to perform case-insensitive matching
        data_lower = data.lower()
        regex_pattern = f".*{re.escape(data_lower)}.*"
        # Create a regular expression to match data with any characters before and after
        print(regex_pattern)
        if mode == "NicknameSearch":
            matched_documents = self.collection_suspect.find(
                {'nickname': {'$exists': True, '$regex': regex_pattern, '$options': 'i'}})
        print(state, "stateeeeeeeeeeeeeeeeeeeeeeeeee")
        if mode == "MixedSearch":
            regex_nickname = f".*{re.escape(nickname.lower())}.*"
            regex_address = f".*{re.escape(address.lower())}.*"
            regex_state = f".*{re.escape(state.lower())}.*"
            print(regex_state, state)

            query = {
                '$or': [
                    {'phone': {'$regex': regex_pattern, '$options': 'i'}},
                    {'nickname': {'$exists': True,
                                  '$regex': regex_nickname, '$options': 'i'}},
                    {'address   ': {'$exists': True,
                                    '$regex': regex_address, '$options': 'i'}},
                    {'permanent_address': {'$exists': True,
                                           '$regex': regex_address, '$options': 'i'}},
                    {'state': {'$exists': True, '$regex': regex_state, '$options': 'i'}}
                ]
            }

            matched_documents = self.collection_suspect.find(query)
        nickname_list = []
        for document in matched_documents:
            msisdn = document['phone']
            nickname = document.get('nickname', "")
            name = document.get("first_name", "")
            provider = document.get('poa_name', '')
            circle = document.get("operator", "")
            local_address = document.get("local_address", "")
            permanent_address = document.get('permanent_address', '')
            # mnp = document['MNP']
            activation_date = document.get('date_of_activation')

            nickname = {
                'msisdn': msisdn,
                'nickname': nickname,
                'name': name,
                'provider': provider,
                'circle': circle,
                'local_address': local_address,
                'permanent_address': permanent_address,
                # 'mnp' : mnp,
                'activation_date': activation_date
            }
            nickname_list.append(nickname)

        headers = [k for k in nickname_list[0].keys(
        )] if nickname_list else "No Data"
        response = {'headers': headers, 'data_dict': nickname_list}
        return response

    def summary_ipdr(self, data, fromdate=None, todate=None):
        print(data, fromdate, todate, "entered into func")
        if fromdate is not None and todate is not None:
            fromdate_obj = datetime.strptime(fromdate, "%Y-%m-%dT%H:%M")
            todate_obj = datetime.strptime(todate, "%Y-%m-%dT%H:%M")
        summary = {}
        if self.collection_ipdr.count_documents({'msisdn': data}) == 0:
            response = {'summary': 'no data',
                        'status': 'empty', 'message': "no data found"}
            return response

        if fromdate is not None and todate is not None:
            print("entered into not none")
            allvpn_stage = {
                "$match": {
                    "msisdn": data,
                    "is_vpn": 1,
                    'time': {
                        '$gte': datetime.combine(fromdate_obj, datetime.min.time()),
                        '$lte': datetime.combine(todate_obj, datetime.max.time())
                    }
                }

            }
        else:
            print("entered into none")
            allvpn_stage = {
                "$match": {
                    "msisdn": data,
                    "is_vpn": 1
                }

            }

        allvpn_pipeline = [
            allvpn_stage,
            {
                "$project": {
                    "_id": 0,
                    "vpn": "$vpn",
                    "msisdn": 1,
                    "vpn_ip": "$destination_ip",
                    "downlink_vol": 1,
                    "uplink_vol": 1,
                    "start_time": "$time",
                    "end_time": "$time_et"
                }
            }
        ]
        query = self.collection_ipdr.aggregate(allvpn_pipeline)
        results = list(query)
        allvpn = []
        for doc in results:
            dwnLink = int(
                doc['downlink_vol']) if doc['downlink_vol'] != "None" and doc['downlink_vol'] != "" else 0
            upLink = int(
                doc['uplink_vol']) if doc['uplink_vol'] != "None" and doc['uplink_vol'] != "" else 0
            downlink_vol = self.convert_size(dwnLink)
            uplink_vol = self.convert_size(upLink)
            start_time = doc['start_time']
            end_time = doc['end_time']
            duration = end_time - start_time
            allvpn.append({
                "MSISDN": doc['msisdn'],
                "VPN": doc['vpn'],
                "VPN_IP": doc['vpn_ip'],
                "downlink_vol": downlink_vol,
                "uplink_vol": uplink_vol,
                "start_time": doc['start_time'],
                "end_time": doc['end_time'],
                "duration": str(duration)
            })

        if fromdate is not None and todate is not None:
            print("entered into vpn Not None")
            vpn_stage = {
                "$match": {
                    "is_vpn": 1,
                    "msisdn": data,
                    "destination_ip": {"$ne": None,
                                       "$ne": ""},
                    'time': {
                        '$gte': datetime.combine(fromdate_obj, datetime.min.time()),
                        '$lte': datetime.combine(todate_obj, datetime.max.time())
                    }
                }

            }
        else:
            print("entered into vpn None")
            vpn_stage = {
                "$match": {
                    "is_vpn": 1,
                    "msisdn": data,
                    "destination_ip": {"$ne": None,
                                       "$ne": ""}
                }

            }

        vpn_pipeline = [
            # {
            #     "$match": {
            #         "is_vpn": 1,
            #         "msisdn": data,
            #         "destination_ip": {"$ne": None,
            #                            "$ne": ""}
            #     }
            # },
            vpn_stage,
            {
                "$group": {
                    "_id": {
                        "vpn": "$vpn",
                        "msisdn": "$msisdn",
                        "destination_ip": "$destination_ip"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$group": {
                    "_id": {
                        "vpn_name": "$_id.vpn",
                        "vpn_msisdn": "$_id.msisdn"
                    },
                    "count_of _unique_destination_ips_of_vpn": {"$sum": 1},
                    "destination_ips_of_vpn": {
                        "$push": {
                            "ip": "$_id.destination_ip",
                            "count": "$count"
                        }
                    },
                    "total_destination_ips_count_of_vpn": {"$sum": "$count"},
                }
            },
            {
                "$sort": {"total_destination_ips_count_of_vpn": -1}
            }
        ]
        query = self.collection_ipdr.aggregate(vpn_pipeline)
        results = list(query)
        vpn = []
        for doc in results:
            vpn.append({
                "MSISDN_VPN": doc['_id']['vpn_msisdn'],
                "VPN": doc['_id']['vpn_name'],
                "count_of _unique_destination_ips_of_vpn": doc['count_of _unique_destination_ips_of_vpn'],
                "destination_ips_of_vpn": doc['destination_ips_of_vpn'],
                "total_destination_ips_count_of_vpn": doc['total_destination_ips_count_of_vpn'],
            })
        print(vpn[:5])

        if fromdate is not None and todate is not None:
            print("entered into country not none")
            country_stage = {
                "$match": {
                    "country": {"$ne": None},
                    "msisdn": data,
                    "destination_ip": {
                        "$ne": None,
                        "$ne": ""
                    },
                    'time': {
                        '$gte': datetime.combine(fromdate_obj, datetime.min.time()),
                        '$lte': datetime.combine(todate_obj, datetime.max.time())
                    }
                }
            }
        else:
            print("entered into country none")
            country_stage = {
                "$match": {
                    "country": {"$ne": None},
                    "msisdn": data,
                    "destination_ip": {
                        "$ne": None,
                        "$ne": ""
                    }
                }
            }

        country_pipeline = [
            # {
            #     "$match": {
            #         "country": {"$ne": None},
            #         "msisdn": data,
            #         "destination_ip": {
            #             "$ne": None,
            #             "$ne": ""
            #         }
            #     }
            # },
            country_stage,
            {
                "$group": {
                    "_id": {
                        "country": "$country",
                        "msisdn": "$msisdn",
                        "destination_ip": "$destination_ip"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$group": {
                    "_id": {
                        "country": "$_id.country",
                        "country_msisdn": "$_id.msisdn"
                    },
                    "count_of_unique_destination_ips_of_country": {"$sum": 1},
                    "destination_ips_of_country": {
                        "$push": {
                            "ip": "$_id.destination_ip",
                            "count": "$count"
                        }
                    },
                    "total_destination_ips_count_of_country": {"$sum": "$count"},

                }
            },
            {
                "$sort": {"total_destination_ips_count_of_country": -1}
            }
        ]
        query2 = self.collection_ipdr.aggregate(country_pipeline)
        results2 = list(query2)
        country = []
        for doc in results2:
            country.append({
                "MSISDN_COUNTRY": doc['_id']['country_msisdn'],
                "COUNTRY": doc['_id']['country'],
                "count_of_unique_destination_ips_of_country": doc['count_of_unique_destination_ips_of_country'],
                "destination_ips_of_country": doc['destination_ips_of_country'],
                "total_destination_ips_count_of_country": doc['total_destination_ips_count_of_country'],
            })

        if fromdate is not None and todate is not None:
            print("entered into app not none")
            app_stage = {
                "$match": {
                    "company": {"$ne": None},
                    "msisdn": data,
                    "destination_ip": {
                        "$ne": None,
                        "$ne": ""
                    },
                    'time': {
                        '$gte': datetime.combine(fromdate_obj, datetime.min.time()),
                        '$lte': datetime.combine(todate_obj, datetime.max.time())
                    }
                }
            }
        else:
            print("entered into app none")
            app_stage = {
                "$match": {
                    "company": {"$ne": None},
                    "msisdn": data,
                    "destination_ip": {
                        "$ne": None,
                        "$ne": ""
                    }
                }
            }

        app_pipeline = [
            # {
            #     "$match": {
            #         "company": {"$ne": None},
            #         "msisdn": data,
            #         "destination_ip": {
            #             "$ne": None,
            #             "$ne": ""
            #         }
            #     }
            # },
            app_stage,
            {
                "$group": {
                    "_id": {
                        "company": "$company",
                        "msisdn": "$msisdn",
                        "destination_ip": "$destination_ip"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$group": {
                    "_id": {
                        "app": "$_id.company",
                        "app_msisdn": "$_id.msisdn"
                    },
                    "count_of_unique_destination_ips_of_app": {"$sum": 1},
                    "destination_ips_of_app": {
                        "$push": {
                            "ip": "$_id.destination_ip",
                            "count": "$count"
                        }
                    },
                    "total_destination_ips_count_of_app": {"$sum": "$count"},
                }
            },
            {
                "$sort": {"total_destination_ips_count_of_app": -1}
            }
        ]
        query3 = self.collection_ipdr.aggregate(app_pipeline)
        results3 = list(query3)

        app = []
        for doc in results3:
            app.append({
                "MSISDN_APP": doc['_id']['app_msisdn'],
                "APP": doc['_id']['app'],
                "count_of_unique_destination_ips_of_app": doc['count_of_unique_destination_ips_of_app'],
                "destination_ips_of_app": doc['destination_ips_of_app'],
                "total_destination_ips_count_of_app": doc['total_destination_ips_count_of_app'],
            })

        if fromdate is not None and todate is not None:
            device_stage = {
                "$match": {
                    "msisdn": data,
                    "destination_ip": {"$ne": ""},
                    'time': {
                        '$gte': datetime.combine(fromdate_obj, datetime.min.time()),
                        '$lte': datetime.combine(todate_obj, datetime.max.time())
                    }
                }
            }
        else:
            device_stage = {
                "$match": {
                    "msisdn": data,
                    "destination_ip": {"$ne": ""}

                }
            }

        device_pipeline = [
            # {
            #     "$match": {
            #         "msisdn": data,
            #         "destination_ip":{"$ne": ""}
            #     }
            # },
            device_stage,
            {
                "$group": {
                    "_id": "$imei",
                    "count": {"$sum": 1},
                    "min_date": {"$min": "$time"},
                    "max_date": {"$max": "$time_et"}
                }
            }
        ]
        query = self.collection_ipdr.aggregate(device_pipeline)
        device_results = list(query)

        if fromdate is not None and todate is not None:
            isp_stage = {
                '$match': {
                    'msisdn': data,
                    'com_type': 'isp',
                    'country': 'India',
                    'time': {
                        '$gte': datetime.combine(fromdate_obj, datetime.min.time()),
                        '$lte': datetime.combine(todate_obj, datetime.max.time())
                    }
                }
            }
        else:
            isp_stage = {
                '$match': {
                    'msisdn': data,
                    'com_type': 'isp',
                    'country': 'India'
                }
            }

        isp_pipeline = [
            # {
            #     '$match': {
            #         'msisdn': data,
            #         'com_type': 'isp',
            #         'country': 'India'
            #     }
            # },
            isp_stage,
            {
                '$group': {
                    '_id': '$destination_ip',
                    'vendor': {'$first': '$asn'},
                    'downlink_vol': {'$first': '$downlink_vol'},
                    'uplink_vol': {'$first': '$uplink_vol'},
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'ip': '$_id',
                    'vendor': 1,
                    'downlink_vol': 1,
                    'uplink_vol': 1
                }
            }
        ]

        query5 = self.collection_ipdr.aggregate(isp_pipeline)
        result5 = list(query5)

        isp_india = []
        for doc in result5:
            print(doc, "indian isp doc")
            try:
                if 'downlink_vol' in doc and 'uplink_vol' in doc:
                    dwnLink = int(
                        doc['downlink_vol']) if doc['downlink_vol'] != "None" and doc['downlink_vol'] != "" else 0
                    upLink = int(
                        doc['uplink_vol']) if doc['uplink_vol'] != "None" and doc['uplink_vol'] != "" else 0
                    total_usage = upLink + dwnLink
                    usage = self.convert_size(total_usage)

                    isp_india.append({
                        "ip": doc['ip'],
                        "vendor": doc['vendor'],
                        "usage": usage
                    })
            except Exception as e:
                print(f" error in isp query :{e}")

        if fromdate is not None and todate is not None:
            foreign_stage = {
                '$match': {
                    'msisdn': data,
                    'com_type': 'isp',
                    'country': {'$ne': 'India'},
                    'time': {
                        '$gte': datetime.combine(fromdate_obj, datetime.min.time()),
                        '$lte': datetime.combine(todate_obj, datetime.max.time())
                    }
                }
            }
        else:
            foreign_stage = {
                '$match': {
                    'msisdn': data,
                    'com_type': 'isp',
                    'country': {'$ne': 'India'}
                }
            }

        foreign_isp_pipeline = [
            # {
            #     '$match': {
            #         'msisdn': data,
            #         'com_type': 'isp',
            #         'country': {'$ne': 'India'}
            #     }
            # },
            foreign_stage,
            {
                '$group': {
                    '_id': '$destination_ip',
                    'vendor': {'$first': '$asn'},
                    'country': {'$first': '$country'},
                    'downlink_vol': {'$first': '$downlink_vol'},
                    'uplink_vol': {'$first': '$uplink_vol'}
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'ip': '$_id',
                    'vendor': 1,
                    'country': 1,
                    'downlink_vol': 1,
                    'uplink_vol': 1,
                }
            }
        ]

        query6 = self.collection_ipdr.aggregate(foreign_isp_pipeline)
        result6 = list(query6)

        foreign_isp = []
        for doc in result6:
            dwnLink = int(
                doc['downlink_vol']) if doc['downlink_vol'] != "None" and doc['downlink_vol'] != "" else 0
            upLink = int(
                doc['uplink_vol']) if doc['uplink_vol'] != "None" and doc['uplink_vol'] != "" else 0
            total_usage = upLink + dwnLink
            usage = self.convert_size(total_usage)
            foreign_isp.append({
                "ip": doc['ip'],
                "vendor": doc['vendor'],
                "country": doc['country'],
                "usage": usage
            })

        if fromdate is not None and todate is not None:
            iptype_stage = {
                "$match": {
                    "com_type": {"$ne": None},
                    "msisdn": data,
                    "destination_ip": {
                        "$ne": None,
                        "$ne": ""
                    },
                    'time': {
                        '$gte': datetime.combine(fromdate_obj, datetime.min.time()),
                        '$lte': datetime.combine(todate_obj, datetime.max.time())
                    }
                }
            }
        else:
            iptype_stage = {
                "$match": {
                    "com_type": {"$ne": None},
                    "msisdn": data,
                    "destination_ip": {
                        "$ne": None,
                        "$ne": ""
                    }
                }
            }

        iptype_pipeline = [
            # {
            #     "$match": {
            #         "com_type": {"$ne": None},
            #         "msisdn": data,
            #         "destination_ip": {
            #             "$ne": None,
            #             "$ne": ""
            #         }
            #     }
            # },
            iptype_stage,
            {
                "$group": {
                    "_id": {
                        "com_type": "$com_type",
                        "msisdn": "$msisdn",
                        "destination_ip": "$destination_ip"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$group": {
                    "_id": {
                        "com_type": "$_id.com_type",
                        "iptype_msisdn": "$_id.msisdn"
                    },
                    "count_of_unique_destination_ips_of_iptype": {"$sum": 1},
                    "destination_ips_of_iptype": {
                        "$push": {
                            "ip": "$_id.destination_ip",
                            "count": "$count"
                        }
                    },
                    "total_destination_ips_count_of_iptype": {"$sum": "$count"},

                }
            },
            {
                "$sort": {"total_destination_ips_count_of_iptype": -1}
            }
        ]

        query4 = self.collection_ipdr.aggregate(iptype_pipeline)
        results4 = list(query4)

        iptype = []
        for doc in results4:
            iptype.append({
                "MSISDN_IPTYPE": doc['_id']['iptype_msisdn'],
                "IPTYPE": doc['_id']['com_type'],
                "count_of_unique_destination_ips_of_iptype": doc['count_of_unique_destination_ips_of_iptype'],
                "destination_ips_of_iptype": doc['destination_ips_of_iptype'],
                "total_destination_ips_count_of_iptype": doc['total_destination_ips_count_of_iptype'],
            })

        if fromdate is not None and todate is not None:
            voip_stage = {
                "$match": {
                    "msisdn": data,
                    'time': {
                        '$gte': datetime.combine(fromdate_obj, datetime.min.time()),
                        '$lte': datetime.combine(todate_obj, datetime.max.time())
                    }
                }
            }
        else:
            voip_stage = {
                "$match": {
                    "msisdn": data,
                }
            }

        voip_pipeline = [
            {
                "$match": {
                    "msisdn": data,
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "msisdn": 1,
                    "source_ip": "$source_ip",
                    "destination_ip": "$destination_ip",
                    "time": "$time",
                    "end_time": "$end_time",
                    # "same_handshake": "$matched_handshake",
                    "vendor": "$vendor",
                    "app": "$app",
                    "cellid": "$cellid",
                    "roaming": "$home_circle",
                    "com_type": "$com_type",
                    "ipinfo": "$ipinfo"
                }},
            {
                "$sort": {
                    # "same_handshake": 1,
                    "time": 1
                }
            }
        ]

        query7 = self.collection_voip.aggregate(voip_pipeline)
        results7 = list(query7)
        voip = []
        for doc in results7:
            start_time = doc['time']
            end_time = doc['end_time']
            duration = end_time - start_time
            voip.append({
                "source_ip": doc['source_ip'],
                "destination_ip": doc['destination_ip'],
                "msisdn": doc['msisdn'],
                "start_time": doc['time'],
                "end_time": doc['end_time'],
                # "same_handshake": doc['same_handshake'],
                "vendor": doc['vendor'],
                "app": doc.get('app', ''),
                "cellid": doc['cellid'],
                "roaming": doc['roaming'],
                # "com_type": doc['com_type'],
                "ipinfo": doc['ipinfo'],
                "duration": str(duration)
            })

        if fromdate is not None and todate is not None:
            matchedcall_stage = {
                '$match': {
                    "caller1": data,
                    'time': {
                        '$gte': datetime.combine(fromdate_obj, datetime.min.time()),
                        '$lte': datetime.combine(todate_obj, datetime.max.time())
                    }
                }}
        else:
            matchedcall_stage = {
                '$match': {
                    "caller1": data
                }}

        matchedcall_pipeline = [
            # {
            # '$match': {
            #     "caller1": data
            # }},
            matchedcall_stage,
            {"$project": {
                '_id': 0,
                'caller1': 1,
                'caller2': '$caller2',
                'calltime': '$calltime',
                'destination_ip': '$destination_ip',
                'source_ip': '$source_ip'
            }}
        ]
        query8 = list(self.collection_matchedcall.aggregate(
            matchedcall_pipeline))
        matchedcall = []
        for doc in query8:
            matchedcall.append({
                "caller1": doc['caller1'],
                "caller2": doc['caller2'],
                "calltime": doc['calltime'],
                "destination_ip": doc['destination_ip'],
                "source_ip": doc['source_ip']
            })

        if data is not None:
            if vpn:
                highest_count_vpn = vpn[0]
                lowest_count_vpn = vpn[-1]
                highest_count_vpn_ip = highest_count_vpn['destination_ips_of_vpn'][0]['ip']
                lowest_count_vpn_ip = lowest_count_vpn['destination_ips_of_vpn'][0]['ip']
            else:
                highest_count_vpn = None
                lowest_count_vpn = None
                highest_count_vpn_ip = None
                lowest_count_vpn_ip = None
            total_unique_vpn_count = len(set(v['VPN'] for v in vpn))

            summary_vpn = {
                'data': data,
                'highest_count_vpn': highest_count_vpn,
                'highest_count_vpn_ip': highest_count_vpn_ip,
                'lowest_count_vpn': lowest_count_vpn,
                'lowest_count_vpn_ip': lowest_count_vpn_ip,
                'total_unique_vpn_count': total_unique_vpn_count
            }
            if app:
                highest_count_app = app[0]
                lowest_count_app = app[-1]
                highest_count_app_ip = highest_count_app['destination_ips_of_app'][0]['ip']
                lowest_count_app_ip = lowest_count_app['destination_ips_of_app'][0]['ip']
            else:
                highest_count_app = None
                lowest_count_app = None
                highest_count_app_ip = None
                lowest_count_app_ip = None
            total_unique_app_count = len(set(v['APP'] for v in app))

            summary_app = {
                'data': data,
                'highest_count_app': highest_count_app,
                'highest_count_app_ip': highest_count_app_ip,
                'lowest_count_app': lowest_count_app,
                'lowest_count_app_ip': lowest_count_app_ip,
                'total_unique_app_count': total_unique_app_count
            }
            if country:
                highest_count_country = country[0]
                lowest_count_country = country[-1]
                highest_count_country_ip = highest_count_country['destination_ips_of_country'][0]['ip']
                lowest_count_country_ip = lowest_count_country['destination_ips_of_country'][0]['ip']
            else:
                highest_count_country = None
                lowest_count_country = None
                highest_count_country_ip = None
                lowest_count_country_ip = None

            total_unique_country_count = len(
                set(v['COUNTRY'] for v in country))
            summary_country = {
                'data': data,
                'highest_count_country': highest_count_country,
                'highest_count_country_ip': highest_count_country_ip,
                'lowest_count_country': lowest_count_country,
                'lowest_count_country_ip': lowest_count_country_ip,
                'total_unique_country_count': total_unique_country_count
            }

            if iptype:
                highest_count_iptype = iptype[0]
                lowest_count_iptype = iptype[-1]
                highest_count_iptype_ip = highest_count_iptype['destination_ips_of_iptype'][0]['ip']
                lowest_count_iptype_ip = lowest_count_iptype['destination_ips_of_iptype'][0]['ip']
            else:
                highest_count_iptype = None
                lowest_count_iptype = None
                highest_count_iptype_ip = None
                lowest_count_iptype_ip = None
            total_unique_iptype_count = len(set(v['IPTYPE'] for v in iptype))
            summary_iptype = {
                'data': data,
                'highest_count_iptype': highest_count_iptype,
                'highest_count_iptype_ip': highest_count_iptype_ip,
                'lowest_count_iptype': lowest_count_iptype,
                'lowest_count_iptype_ip': lowest_count_iptype_ip,
                'total_unique_iptype_count': total_unique_iptype_count
            }

            summary = {'data': data,
                       'allvpn': allvpn,
                       'isp_india': isp_india,
                       'foreign_isp': foreign_isp,
                       'vpn': vpn,
                       'country': country,
                       'app': app,
                       'iptype': iptype,
                       'voip': voip,
                       'matchedcall': matchedcall,
                       'device': device_results,
                       'summary_app': summary_app,
                       'summary_country': summary_country,
                       'summary_vpn': summary_vpn,
                       'summary_iptype': summary_iptype,
                       'status': 'success',
                       'message': 'data retrived successfully'
                       }
            return summary
