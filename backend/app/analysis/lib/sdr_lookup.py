from pymongo import MongoClient
import pymongo
from datetime import datetime, time, timedelta
import math
from pprint import pprint
from loguru import logger
import re
import datetime as datetimeasnow
import tqdm
from MongoClinet import CDAT
mongocdat = CDAT()

logger.add("file_log.log",
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")


class Sdr_Lookup():
    def __init__(self):
        # self.client = MongoClient('mongodb://localhost:27017')
        self.collection_sdr = mongocdat.sdrdata
        self.collection_cellidchart = mongocdat.cellidchart
        self.collection_cdr = mongocdat.cdrdata
        self.collection_ipdr = mongocdat.ipdr
        # self.collection_sdr.create_index([("fullname",pymongo.TEXT)])
        # self.collection_sdr.create_index([("local_address",pymongo.ASCENDING)])

    def remove_duplicate_dicts(self, data_list, key):
        seen = set()
        result = []
        for d in data_list:
            d_key = d[key]
            if d_key not in seen:
                seen.add(d_key)
                result.append(d)
        return result

    # Number of sim cards purchased/registered against a particular name.
    def name_search(self, name):
        """_summary_ : this function will search the name in sdr collection with exact and similar match.
                       Also remove the same duplicate doc coming in exact and similar finding only return the unique doc using the remove_duplicate_dicts function.

        Args:
            name (_type_): name in string 

        Returns:
            _type_: response will contain header will be the key of unique_matched_entities and data_dict will be the values of unique_matched_entities.
        """
        print(name)
        matched_entities = []
        doc = list(self.collection_sdr.find({'fullname': name}, {'_id': 1, 'fullname': 1, 'source_number': 1,
                   'date_of_activation': 1, 'alternate_number': 1, 'local_address': 1, 'permanent_address': 1, 'state': 1}))
        for item in doc:
            matched_entities.append({'unique_id': str(item['_id']),
                                     'name': item['fullname'],
                                     'source_number': item['source_number'],
                                     'alternate_number': item['alternate_number'],
                                     'date_of_activation': item['date_of_activation'],
                                     'local_address': item['local_address'],
                                     'permanent_address': item['permanent_address'],
                                     'state': item['state'],
                                     'match': 'exact_match'})

        print("first query done")
        doc = self.collection_sdr.find({'fullname': {'$regex': name, '$options': 'i'}}, {'_id': 1, 'fullname': 1, 'source_number': 1,
                                       'date_of_activation': 1, 'alternate_number': 1, 'local_address': 1, 'permanent_address': 1, 'state': 1})
        print("second query done")
    
        for item in doc:
            print("09999")
            matched_entities.append({'unique_id': str(item['_id']),
                                     'name': item['fullname'],
                                     'source_number': item['source_number'],
                                     'alternate_number': item['alternate_number'],
                                     'date_of_activation': item['date_of_activation'],
                                     'local_address': item['local_address'],
                                     'permanent_address': item['permanent_address'],
                                     'state': item['state'],
                                     'match': 'partical_match'})
            
        unique_matched_entities = self.remove_duplicate_dicts(
            matched_entities, 'unique_id')
        pprint(list(unique_matched_entities))
        headers = [k for k in unique_matched_entities[0].keys(
        )] if unique_matched_entities else 'No Data'
        response = {'headers': headers,
                    'data_dict': unique_matched_entities if unique_matched_entities else 'Not Data matched'}
        pprint(response['data_dict'])
        return response

    # Search for phone numbers that share the same SDR with phone numbers of SDB.
    # Alternative phone numbers of all the same SDR numbers.

    def number_search(self, number, fromdate=None, todate=None):
        print(number, fromdate, todate)
        """_summary_ : for given list of number, if number match it will return 
        {'_id':1,'fullname':1,'source_number':1,'date_of_activation':1,'alternate_number':1,'local_address':1,'permanent_address':1,'state':1}
        

        Args:
            number (_type_): number in string type

        Returns:
            _type_: response will contain header will be the key of matched_entities and data_dict will be the values of matched_entities.
        """
        pipeline = []
        # match_conditions = []
        match_conditions = {
            "$and": []
        }
        if number:
            number_list = number.split(",")
            match_conditions["$and"].append(
                {"source_number": {"$in": number_list}})

        if fromdate and todate:
            try:
                from_date = datetime.strptime(
                    fromdate, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
                to_date = datetime.strptime(
                    todate, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=999)
                # print(from_date,to_date)
                match_conditions["$and"].append({
                    "$expr": {
                        "$and": [
                            {"$gte": [{"$dateFromString": {
                                "dateString": "$date_of_activation", "format": "%d-%m-%Y"}}, from_date]},
                            {"$lte": [{"$dateFromString": {
                                "dateString": "$date_of_activation", "format": "%d-%m-%Y"}}, to_date]}
                        ]
                    }
                })
                # print(match_conditions)
            except ValueError:
                return "Invalid date format. Please use 'Y-m-d'."

        # Match documents based on provided conditions
        if match_conditions["$and"]:
            pipeline.append({"$match": match_conditions})

        # Add projection stage to reshape documents if needed
        pipeline.append(
            {
                "$project": {
                    '_id': 1, 'fullname': 1, 'source_number': 1,
                    'date_of_activation': 1, 'alternate_number': 1,
                    'local_address': 1, 'permanent_address': 1, 'state': 1, 'operator': 1
                }
            })
        result = list(self.collection_sdr.aggregate(pipeline))
        # doc = list(self.collection_sdr.find({'source_number':{"$in":number}},{'_id':1,'fullname':1,'source_number':1,'date_of_activation':1,'alternate_number':1,'local_address':1,'permanent_address':1,'state':1}))
        matched_entities = []
        
        for item in result:
            print(item)
            matched_entities.append({'unique_id': str(item['_id']),
                                     'name': item['fullname'],
                                     'source_number': item['source_number'],
                                     'alternate_number': item['alternate_number'],
                                     'date_of_activation': item['date_of_activation'],
                                     'local_address': item['local_address'],
                                     'permanent_address': item['permanent_address'],
                                     'provider': item['operator'],
                                     'state': item['state']})
        headers = [k for k in matched_entities[0].keys(
        )] if matched_entities else 'No Data'
        response = {'headers': headers,
                    'data_dict': matched_entities if matched_entities else 'Not Data matched'}
        # pprint(response['data_dict'])
        return response

    # Address based (House no, Village)- Phones with same address as the target phone number – complete address search with maximum match.
    def address_search(self, partial_address):
        print(type(partial_address),partial_address, "-------------")
        """_summary_ : for given partial_address ,find the all the possible matched address and it will return 
        {'_id':1,'fullname':1,'source_number':1,'date_of_activation':1,'alternate_number':1,'local_address':1,'permanent_address':1,'state':1}
        

        Args:
            partial_address (string): partial_address in string type

        Returns:
            _type_: response will contain header will be the key of matched_entities and data_dict will be the values of matched_entities.
        """
        matched_entities = []
        doc = list(self.collection_sdr.find({"local_address": {"$regex": partial_address, "$options": "i"}}, {
                   '_id': 1, 'fullname': 1, 'source_number': 1, 'date_of_activation': 1, 'alternate_number': 1, 'local_address': 1, 'permanent_address': 1, 'state': 1}))
        for item in doc:
            matched_entities.append({'unique_id': str(item['_id']),
                                     'name': item['fullname'],
                                     'source_number': item['source_number'],
                                     'alternate_number': item['alternate_number'],
                                     'date_of_activation': item['date_of_activation'],
                                     'local_address': item['local_address'],
                                     'permanent_address': item['permanent_address'],
                                     'state': item['state']})
        headers = [k for k in matched_entities[0].keys(
        )] if matched_entities else 'No Data'
        response = {'headers': headers,
                    'data_dict': matched_entities if matched_entities else 'Not Data matched'}
        pprint(response['data_dict'])
        return response

    # POA/DOA of the target number – Phone numbers in database with same date of activation and POA.
    def date_target(self, numbers):
        # date with poa number
        print(numbers, "------")
        # merchant_code
        """_summary_ : Phone numbers in database with same date of activation and POA

        Args:
            numbers (string): list of numbers input

        Returns:
            _type_: response will contain header will be the key of matched_entities and data_dict will be the values of matched_entities.
        """
        # poa_no
        numbers = numbers.split(",")
        dates = self.collection_sdr.distinct(
            'date_of_activation', {"source_number": {"$in": numbers}})
        poa_number = self.collection_sdr.distinct(
            'poa_no', {"source_number": {"$in": numbers}})
        print(dates)
        print(poa_number)
        matched_entities = []
        doc = list(self.collection_sdr.find({"date_of_activation": {"$in": dates},
                                             "poa_no": {"$in": poa_number}},
                                            {'_id': 1, 'fullname': 1, 'source_number': 1, 'date_of_activation': 1, 'poa_no': 1, 'alternate_number': 1, 'local_address': 1, 'permanent_address': 1, 'state': 1}))
        # pprint(doc)
        for item in doc:
            matched_entities.append({'unique_id': str(item['_id']),
                                     'name': item['fullname'],
                                     'source_number': item['source_number'],
                                     'alternate_number': item['alternate_number'],
                                     'date_of_activation': item['date_of_activation'],
                                     'mercant_phone': item['poa_no'],
                                     'local_address': item['local_address'],
                                     'permanent_address': item['permanent_address'],
                                     'state': item['state']})
        pprint(matched_entities)
        headers = [k for k in matched_entities[0].keys(
        )] if matched_entities else 'No Data'
        response = {'headers': headers,
                    'data_dict': matched_entities if matched_entities else 'Not Data matched'}
        # pprint(response['data_dict'])
        return response

    def sm_poa(self, data, fromdate=False, todate=False):
        """
        description : same date recharge 

        """
        print(data, "data_dict")
        data = data.split(",")
        print(data, "Datas")
        getdata = []
        if fromdate is None and todate is None:
            print("inside none")
            query = {'msisdn': {"$in": data}}
        else:
            print("inside not none")
            query = {'msisdn': {"$in": data},
                     'sim_activation_timestamp': {
                '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()}
            }

        getdata.extend(mongocdat.poadata.find(query))
        if len(getdata) == 0:
            response = {'data_dict': [], 'status': 'empty',
                        'message': 'no data found'}
            return response
        else:
            matched_entities = []
            distinct_dates = mongocdat.poadata.distinct(
                'sim_activation_date', {'msisdn': {"$in": data}})
            print(distinct_dates, "-date")
            poa_list = mongocdat.poadata.distinct(
                'pos_code', {'msisdn': {"$in": data}})
            print(poa_list, "-rh list")
            if fromdate is not None and todate is not None:
                matched_documents = list(mongocdat.poadata.find({'pos_code': {"$in": poa_list},
                                                                 'sim_activation_date': {'$in': distinct_dates},
                                                                 'sim_activation_timestamp': {
                    '$gte': datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                    '$lte': datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                }
                }))
            else:
                matched_documents = list(mongocdat.poadata.find(
                    {'pos_code': {"$in": poa_list}, 'sim_activation_date': {'$in': distinct_dates}}))
                print(matched_documents, "--Data")
                for item in matched_documents:
                    matched_entities.append({'unique_id': str(item['_id']),
                                            'name': item['name_of_subscriber'],
                                             'msisdn': item['msisdn'],
                                             'alternate_number': item['alternate_phone_no'],
                                             'sim_activation_date': item['sim_activation_date'],
                                             'local_address': item['subscriber_address'],
                                             'provider': item['provider'],
                                             'state': item['circle_name']})
            pprint(matched_entities)
            headers = [k for k in matched_entities[0].keys(
            )] if matched_entities else 'No Data'
            response = {'headers': headers, 'data_dict': matched_entities,
                        'status': 'success', 'message': 'data retrived successfully'}
            return response

    def alternate_number(self, number, fromdate=None, todate=None):
        print(number, fromdate, todate)
        """_summary_ : for given list of number, if number match it will return 
        {'_id':1,'fullname':1,'source_number':1,'date_of_activation':1,'alternate_number':1,'local_address':1,'permanent_address':1,'state':1}
        

        Args:
            number (_type_): number in string type

        Returns:
            _type_: response will contain header will be the key of matched_entities and data_dict will be the values of matched_entities.
        """
        pipeline = []
        # match_conditions = []
        match_conditions = {
            "$and": []
        }
        if number:
            number_list = number.split(",")
            match_conditions["$and"].append(
                {"alternate_number": {"$in": number_list}})

        if fromdate and todate:
            try:
                from_date = datetime.strptime(
                    fromdate, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
                to_date = datetime.strptime(
                    todate, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=999)
                # print(from_date,to_date)
                match_conditions["$and"].append({
                    "$expr": {
                        "$and": [
                            {"$gte": [{"$dateFromString": {
                                "dateString": "$date_of_activation", "format": "%d-%m-%Y"}}, from_date]},
                            {"$lte": [{"$dateFromString": {
                                "dateString": "$date_of_activation", "format": "%d-%m-%Y"}}, to_date]}
                        ]
                    }
                })
                # print(match_conditions)
            except ValueError:
                return "Invalid date format. Please use 'Y-m-d'."

        # Match documents based on provided conditions
        if match_conditions["$and"]:
            pipeline.append({"$match": match_conditions})

        # Add projection stage to reshape documents if needed
        pipeline.append(
            {
                "$project": {
                    '_id': 1, 'fullname': 1, 'source_number': 1,
                    'date_of_activation': 1, 'alternate_number': 1,
                    'local_address': 1, 'permanent_address': 1, 'state': 1
                }
            })
        result = list(self.collection_sdr.aggregate(pipeline))
        # doc = list(self.collection_sdr.find({'source_number':{"$in":number}},{'_id':1,'fullname':1,'source_number':1,'date_of_activation':1,'alternate_number':1,'local_address':1,'permanent_address':1,'state':1}))
        matched_entities = []
        for item in result:
            matched_entities.append({'unique_id': str(item['_id']),
                                     'name': item['fullname'],
                                     'source_number': item['source_number'],
                                     'alternate_number': item['alternate_number'],
                                     'date_of_activation': item['date_of_activation'],
                                     'local_address': item['local_address'],
                                     'permanent_address': item['permanent_address'],
                                     'operator': item.get('operator'),
                                     'state': item['state']})
        headers = [k for k in matched_entities[0].keys(
        )] if matched_entities else 'No Data'
        response = {'headers': headers,
                    'data_dict': matched_entities if matched_entities else 'Not Data matched'}
        pprint(response['data_dict'])
        return response


# if __name__ == "__main__":
#     name = "Ramesh"
#     address = "Fort Street"
#     number = "8000004458,8000004662"
#     # fromdate = "2016-06-21"
#     # todate = "2016-06-22"
#     Sdr_Lookup().number_search(number,fromdate=None,todate=None)
