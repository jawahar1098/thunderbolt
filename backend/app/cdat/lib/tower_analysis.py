from pymongo import MongoClient
from loguru import logger
from datetime import datetime,timedelta
import pymongo
from itertools import combinations
# from cdr.mongocli import Mongo_Connect
# mongo = Mongo_Connect
from pprint import pprint
from flask import jsonify, request
import time
from MongoClinet import CDAT
mongocdat = CDAT()
import json

class Tower_View():
    def __init__(self):
        self.collection = mongocdat.towercdrdata
        self.collection_cdr = mongocdat.cdrdata
        self.collection_ipdr = mongocdat.ipdr
        self.collection_sdr = mongocdat.sdrdata
        self.collection_suspect = mongocdat.suspect
        self.collection_cellidchart = mongocdat.cellidchart
        self.collection_newcell = mongocdat.cellidchart_jio
        self.mapdata = mongocdat.mapdata
        # self.client2 = MongoClient('mongodb://10.50.50.230:27017')
        

    def calls_under_tower(self, inputdata=False, fromdate=False, todate=False):
        """
        Calls under tower
        """
        time1 = {'title':'function starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time()}

        cellid_list = [cellid for tower in inputdata for cellid in tower.get('cellid', [])]
        sitename_list = [item.get('towername', '') for item in inputdata]
        print(inputdata,fromdate,todate,"call under tower")
        logger.info("function starts")
        match_conditions = {
            "$and": []
        }
        if len(sitename_list) > 0:
            print(sitename_list,"sitname")
            match_conditions["$and"].append({"sitename": {"$in": sitename_list}})
        # else:
        #     match_conditions["$and"].append({"sitename": {"$exists": True}})

        if len(cellid_list) > 0:
            print(cellid_list,"sitename")
            match_conditions["$and"].append({"first_cgid": {"$in": cellid_list}})

        if fromdate != None and todate != None:
            print(fromdate,type(fromdate))
            from_date = datetime.strptime(fromdate, "%Y-%m-%dT%H:%M:%S")#.replace(hour=0, minute=0, second=0, microsecond=0)
            to_date = datetime.strptime(todate, "%Y-%m-%dT%H:%M:%S")#.replace(hour=23, minute=59, second=59, microsecond=999)
            match_conditions["$expr"] = {
                    "$and": [
                        {"$gte": [{"$dateFromString": {"dateString": {"$concat": ["$date", "T", "$time"]}, "format": "%d-%m-%YT%H:%M:%S"}}, from_date]},
                        {"$lte": [{"$dateFromString": {"dateString": {"$concat": ["$date", "T", "$time"]}, "format": "%d-%m-%YT%H:%M:%S"}}, to_date]}
                    ]
                }
        print(match_conditions)
        # Construct the aggregation pipeline
        pipeline = [
            {
                "$match": match_conditions
            },
            {
                "$addFields": {
                    "calltypeLower": {"$toLower": "$call_type"}
                }
            },
            {
                "$group": {
                    "_id": {
                        "source_number": "$source_number",
                        "destination_number": "$destination_number",
                        "sitename": "$sitename",
                        "first_cgid":"$first_cgid",
                        "date":"$date",
                        "time":"$time",
                        "date_format":"$date_format"

                    },
                    "incoming": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$regexMatch": {
                                        "input": "$calltypeLower",
                                        "regex": "in",
                                    }
                                },
                                1,
                                0
                            ]
                        }
                    },
                    "outgoing": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$regexMatch": {
                                        "input": "$calltypeLower",
                                        "regex": "out",
                                    }
                                },
                                1,
                                0
                            ]
                        }
                    }
                }
            },
            {
                "$lookup": {
                    "from": "cdat_tower",
                    "let": {
                        "source_number": "$_id.source_number",
                        "destination_number": "$_id.destination_number",
                        "sitename": "$_id.sitename",
                        "first_cgid" : "$_id.first_cgid",
                        "date":"$_id.date",
                        "time":"$_id.time",
                        "date_format":"$_id.date_format",
                        "sitename_list": sitename_list 
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                        "$or": [
                                                {
                                                    "$and": [
                                                        {"$eq": ["$source_number", "$$destination_number"]},
                                                        {"$eq": ["$destination_number", "$$source_number"]},
                                                        {"$in": ["$sitename", "$$sitename_list"]},
                                                        {"$ne": ["$sitename", "$$sitename"]},
                                                        {"$eq": ["$date", "$$date"]},
                                                        {"$ne": ["$source_number", None]},
                                                        {"$ne": ["$destination_number", None]},
                                                        {
                                                            "$or": [
                                                                {
                                                                    "$and": [
                                                                        { "$eq": [{ "$minute": { "$toDate": "$date_format" } }, { "$add": [{ "$minute": { "$toDate": "$$date_format" } }, 1] }] },
                                                                        { "$eq": [{ "$hour": { "$toDate": "$date_format" } }, { "$hour": { "$toDate": "$$date_format" } }] }
                                                                    ]
                                                                },
                                                                {
                                                                    "$and": [
                                                                        { "$eq": [{ "$minute": { "$toDate": "$$date_format" } }, { "$add": [{ "$minute": { "$toDate": "$date_format" } }, 1] }] },
                                                                        { "$eq": [{ "$hour": { "$toDate": "$$date_format" } }, { "$hour": { "$toDate": "$date_format" } }] }
                                                                    ]
                                                                },
                                                                {
                                                                    "$eq": [
                                                                        { "$minute": { "$toDate": "$date_format" } },
                                                                        { "$minute": { "$toDate": "$$date_format" } }
                                                                    ]
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }      
                                            ],     
                                         }
                                    }
                        }
                    ],
                    "as": "matchedPairs"
                }
            },
            {
                "$unwind": "$matchedPairs"  # Unwind the matchedPairs array
            },
            {
                "$project": {
                    "_id": 0,
                    "phone": "$_id.source_number",
                    "other": "$_id.destination_number",
                    "incoming": 1,
                    "outgoing": 1,
                    "sitename": "$_id.sitename",
                    "first_cellid":"$_id.first_cgid",
                    "date":"$_id.date",
                    "time":"$_id.time",
                    "date_format":"$_id.date_format"

                }
            }
        ]
        logger.info("Aggregation")
        # Execute the aggregation pipeline and retrieve the results
        time2 = {'title':'Aggregation for callunder','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time()}
        results = list(self.collection.aggregate(pipeline))
        time3 = {'title':'Aggregation ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'iteration time':time.time() - time2['timestamp']}

        logger.info("Aggregationends")

        logger.info('Calls under tower function ends')
        unique_results = set()
        for result in results:
            unique_results.add(tuple(result.items()))

        if unique_results:
            unique_results_list = [dict(item) for item in unique_results]
            sorted_results = sorted(unique_results_list, key=lambda x: (x['date'],x['time']))

            # pprint(unique_results_list)
            time4 = {'title':'function ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'iteration time':time.time() - time1['timestamp']}

            response = {'unique_results_list':sorted_results,'status':'success','times':[time1,time2,time3,time4]}
            logger.info("RESUKTSSS")
            return response
        else:
            response = {'unique_results_list':[],'status':'failure','times':['nodata']}
            return response

    def bookmarkdata(self,send_data):
        # data = request.get_json()
        print(send_data,'send dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        insert_result = self.mapdata.insert_one(send_data)
        print(insert_result)
        return jsonify({"message": "Bookmarks added"})

    
   # fixed input from geo query 
    def common_numbers_in_different_towers(self,mode, inputdata=None, fromdate=None, todate=None):
        print(inputdata,"---inside query-----")
        time1 = {'title':'Function starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time()}

        # sitename_list = ['AMBAYATHODE','ANGADIKADAV','Matlapad']
        cellid_list = [cellid for tower in inputdata for cellid in tower.get('cellid', [])]
        sitename_list = [item.get('towername', '') for item in inputdata]
        # cellid_list = ['40586201A9E10']
        # cellid_list = ['4058620129C23']
        print(cellid_list)
        print(sitename_list)
        """
        Numbers common in different towers
        and 
        Other party common in different towers
        """
        match_conditions = {}

        if len(sitename_list) > 0:
            match_conditions["sitename"] = {"$in": sitename_list}
        if len(cellid_list) > 0:
            match_conditions["first_cgid"] = {"$in": cellid_list}

        if fromdate != None and todate != None:
            from_date = datetime.strptime(fromdate, "%Y-%m-%dT%H:%M:%S")#.replace(hour=0, minute=0, second=0, microsecond=0)
            to_date = datetime.strptime(todate, "%Y-%m-%dT%H:%M:%S")#.replace(hour=23, minute=59, second=59, microsecond=999)
            match_conditions["$expr"] = {
                    "$and": [
                        {"$gte": [{"$dateFromString": {"dateString": {"$concat": ["$date", "T", "$time"]}, "format": "%d-%m-%YT%H:%M:%S"}}, from_date]},
                        {"$lte": [{"$dateFromString": {"dateString": {"$concat": ["$date", "T", "$time"]}, "format": "%d-%m-%YT%H:%M:%S"}}, to_date]}
                    ]
                }
        print(match_conditions)
        if mode == "common_source":
            print("In common numbers")
            source_pipeline = [
                {
                    "$match": match_conditions
                },
                {
                    "$group": {
                        "_id": "$source_number",
                        "common_towers": {
                            "$addToSet": "$sitename"
                        }
                    }
                },
                {
                    "$match": {
                        "common_towers.1": {"$exists": True}  
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "source_number": "$_id",
                        "common_towers": "$common_towers"
                    }
                },
                {
                    "$group": {
                        "_id": "$common_towers",
                        "common_numbers": {
                            "$addToSet": "$source_number"
                        }
                    }
                }
            ]
            time2 = {'title':'Aggreagtion for common numbers starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time()}
            common_source_numbers = list(self.collection.aggregate(source_pipeline))
            time3 = {'title':'Aggregation ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'iteration time':time.time() - time2['timestamp']}
            time4 = {'title':'Function ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'iteration time':time.time() - time1['timestamp']}

            print(common_source_numbers,"----source------")
            if len(common_source_numbers) > 0:
                response = {"common_source_numbers":common_source_numbers,'status':'success', 'times':[time1,time2,time3,time4]}
            else:
                response = {"common_source_numbers":common_source_numbers,'status':'failure','times':['nodata']}

            return response 
        if mode == "common_destination": 
            print("In dest numbers")
  
            destination_pipeline = [
            {
                "$match": match_conditions
            },
            {
                "$group": {
                    "_id": "$destination_number",
                    "common_towers": {
                        "$addToSet": "$sitename"
                    }
                }
            },
            {
                "$match": {
                    "common_towers.1": {"$exists": True}  
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "destination_number": "$_id",
                    "common_towers": "$common_towers"
                }
            },
            {
                "$group": {
                    "_id": "$common_towers",
                    "common_numbers": {
                        "$addToSet": "$destination_number"
                    }
                }
            }
            ]

            
            common_destination_numbers = list(self.collection.aggregate(destination_pipeline))
            if len(common_destination_numbers) > 0:
                response = {"common_destination_numbers":common_destination_numbers,'status':'success'}
            else:
                response = {"common_destination_numbers":[],'status':'failure'}

            return  response 
        if mode == "common_imei":
            imei_pipeline = [
            {
                "$match": match_conditions
            },
            {
                "$group": {
                    "_id": "$imei",
                    "common_towers": {
                        "$addToSet": "$sitename"
                    }
                }
            },
            {
                "$match": {
                    "common_towers.1": {"$exists": True}  # Filters for source_numbers with more than one common tower
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "imei": "$_id",
                    "common_towers": "$common_towers"
                }
            },
            {
                "$group": {
                    "_id": "$common_towers",
                    "common_numbers": {
                        "$addToSet": "$imei"
                    }
                }
            }
        ]
        common_imei_numbers = list(self.collection.aggregate(imei_pipeline))
        if len(common_imei_numbers) > 0:
            response = {"common_imei_numbers":common_imei_numbers,'status':'success'}
        else:
            response = {"common_imei_numbers":[],'status':'failure'}

        return response
    

    # [{'towername': 'Prayar North, Kollam', 'cellid': []}, {'towername': 'Krishnapuram 3, Kollam', 'cellid': []}, {'towername': 'VALIYAKULANGARA', 'cellid': []}, {'towername': 'PRAYAR', 'cellid': []}, {'towername': 'Oachira, Kollam', 'cellid': []}, {'towername': 'Ochira Railway Station, Kollam', 'cellid': []}]


    #need to fix frontend
    def group_of_numbers(self, phone_numbers, fromdate, todate, inputdata=None):
        '''
        Groups of numbers in different towers
        '''

        cellid_list = [cellid for tower in inputdata for cellid in tower.get('cellid', [])]
        sitename_list = [item.get('towername', '') for item in inputdata]

        print(sitename_list,cellid_list,phone_numbers,";;;;;;;;;;;;;;;;;")
        phone_numbers = phone_numbers.split(",") #["6006351760", "6000043627", "6238293752", "6238783726", "6238114280", "6238386498", "6238182894", "6238666519", "6238294621", "6238877292"] 
        #  need to correc for multiple oinputs
              # ["Aralam farm", "ANGADIKADAV", "MANNANTHARA", "Peravoor"]
        match_conditions = {}

        if len(sitename_list) > 0:
            match_conditions["sitename"] = {"$in": sitename_list}

        if len(cellid_list) > 0:
            match_conditions["first_cgid"] = {"$in": cellid_list}
        if phone_numbers:
            match_conditions["source_number"] = {"$in": phone_numbers}

        if fromdate != None and todate != None:
            print(fromdate,type(fromdate))
            
            from_date = datetime.strptime(fromdate, "%Y-%m-%dT%H:%M:%S")#.replace(hour=0, minute=0, second=0, microsecond=0)
            to_date = datetime.strptime(todate, "%Y-%m-%dT%H:%M:%S")#.replace(hour=23, minute=59, second=59, microsecond=999)
            match_conditions["$expr"] = {
                    "$and": [
                        {"$gte": [{"$dateFromString": {"dateString": {"$concat": ["$date", "T", "$time"]}, "format": "%d-%m-%YT%H:%M:%S"}}, from_date]},
                        {"$lte": [{"$dateFromString": {"dateString": {"$concat": ["$date", "T", "$time"]}, "format": "%d-%m-%YT%H:%M:%S"}}, to_date]}
                    ]
                }
        print(match_conditions)
        
        result_dict = {}
        for sitename in sitename_list:
            source_and_cellid_data = self.collection.aggregate([
                {
                    "$match": {
                        **match_conditions,
                        "sitename": sitename,
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "sitename": "$sitename",
                            "source_number": "$source_number"
                        },
                        "unique_cellids": {"$addToSet": "$first_cgid"}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "sitename": "$_id.sitename",
                        "source_number": "$_id.source_number",
                        "unique_cellids": 1
                    }
                }
            ])

            info = list(source_and_cellid_data)

            if info:
                available_source_numbers = [entry["source_number"] for entry in info]

                unmatched_source_numbers = [number for number in phone_numbers if number not in available_source_numbers]


                for entry in info:
                    source_number = entry["source_number"]
                    cellids = entry["unique_cellids"]

                    if source_number in phone_numbers:
                        if sitename not in result_dict:
                            result_dict[sitename] = {
                                "Available_Phone_Numbers": [],
                                "Not_Available_Phone_Numbers": [],
                                "Cellids": [],
                                "sitename": sitename
                            }

                        result_dict[sitename]["Available_Phone_Numbers"].append(source_number)

                        result_dict[sitename]["Cellids"].append(cellids)

                result_dict[sitename]["Not_Available_Phone_Numbers"] = unmatched_source_numbers

                print(result_dict)

        # return result_dict
        if result_dict:
            result_dict = list(result_dict.values())
            response = {'result_dict':result_dict,'status':'success','message':'data received successfully'}
            return response
        else:
            print("No matching documents found")
            response = {'result_dict':[{'Available_Phone_Numbers':['-'],'Cellids':['-'],'Not_Available_Phone_Numbers':phone_numbers,"sitename": sitename}],'status':'failure','message':'no data found'}
            return response

    def unique_common_groups_in_different_towers(self, inputdata=None, fromdate=None, todate=None):
        """
        Finding relation of calls between different tower groups.
        """
        print('unique_common_groups_in_different_towers')
        match_conditions = {'destination_number': {
                                 '$regex': '^(91\\d{10}|\\d{10})$'
                           }}

        sitename_list = []
        cellid_list = []

        cellid_list = [cellid for tower in inputdata for cellid in tower.get('cellid', [])]
        sitename_list = [item.get('towername', '') for item in inputdata]

        if sitename_list != None:
            match_conditions["sitename"] = {"$in": sitename_list}
        if len(cellid_list) > 0:
            match_conditions["first_cgid"] = {"$in": cellid_list}

        if fromdate != None and todate != None:
            # match_conditions["date"] = {"$gte": fromdate, "$lte": todate}
            from_date = datetime.strptime(fromdate, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
            to_date = datetime.strptime(todate, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=999)
            match_conditions["$expr"] = {
                "$and": [
                    {"$gte": [{"$dateFromString": {"dateString": "$date", "format": "%d-%m-%Y"}}, from_date]},
                    {"$lte": [{"$dateFromString": {"dateString": "$date", "format": "%d-%m-%Y"}}, to_date]}
                ]
            }
        print(match_conditions)
       
        pipeline = [
            {
            "$match": match_conditions
            },
            {
                "$group": {
                    "_id": {
                        "source_number": "$source_number",
                        "destination_number": "$destination_number",
                        "imei": "$imei",
                    },
                    "sitenames_and_cellids": {
                        "$addToSet": {
                            "sitename": "$sitename",
                            "cellids": "$first_cgid"
                        }
                    }
                }
            },
            {
                "$match": {
                    "sitenames_and_cellids.1": {"$exists": True}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "same_convo": "$_id",
                    "common_sitenames": "$sitenames_and_cellids"
                }
            }
        ]
        unique_common_groups = list(self.collection.aggregate(pipeline))
        pprint(unique_common_groups)
        
        if len(unique_common_groups) > 0:
            response = {'unique_common_groups':unique_common_groups,'status':'success'}
        else:
            response = {'unique_common_groups':[],'status':'failure'}
            
        return response
    

    #available and Not available
    def numbers_groups_different_towers(self, phone_numbers, target_key_location, target_sitename):
        # phone_numbers = ["6006351760", "6000043627", "6238293752", "6238783726", "6238114280", "6238386498", "6238182894", "6238666519", "6238294621", "6238877292"]  
        # target_key_location = ["KERALA_ARALAM_0405_JIO_TOWER_CDRS", "GANDAMARDHANA_HILLS_AT_TOWER_CDRS", "YELLAVARAM_KONTA_AP_TRACK_JIO_TOWER_CDRS"]
        # target_sitename = ["Aralam farm", "ANGADIKADAV", "MANNANTHARA", "Peravoor"]

        """
        Groups of numbers in different towers
        """
        result_dict = {}
        print(target_sitename)
        for sitename in target_sitename:
            source_and_cellid_data = self.collection.aggregate([
                {
                    "$match": {
                        "key_location": {"$in": target_key_location},
                        "sitename": sitename,
                        "source_number": {"$in": phone_numbers}
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "key_location": "$key_location",
                            "sitename": "$sitename",
                            "source_number": "$source_number"
                        },
                        "unique_cellids": {"$addToSet": "$first_cellid"}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "key_location": "$_id.key_location",
                        "sitename": "$_id.sitename",
                        "source_number": "$_id.source_number",
                        "unique_cellids": 1
                    }
                }
            ])

            info = list(source_and_cellid_data)

            if info:
                available_source_numbers = [entry["source_number"] for entry in info]

                unmatched_source_numbers = [number for number in phone_numbers if number not in available_source_numbers]


                for entry in info:
                    source_number = entry["source_number"]
                    cellids = entry["unique_cellids"]
                    key_location = entry["key_location"]

                    if source_number in phone_numbers:
                        if sitename not in result_dict:
                            result_dict[sitename] = {
                                "key location": key_location,
                                "Available Phone Numbers": [],
                                "Not Available Phone Numbers": [],
                                "Phone Numbers and Cellids": [],
                                "sitename": sitename
                            }

                        result_dict[sitename]["Available Phone Numbers"].append(source_number)

                        cellids_dict = {"source number": source_number, "cellids": cellids}
                        result_dict[sitename]["Phone Numbers and Cellids"].append(cellids_dict)

                result_dict[sitename]["Not Available Phone Numbers"] = unmatched_source_numbers

                print(result_dict)

        # return result_dict
        if result_dict:
            return result_dict
        else:
            print("No matching documents found")


    #TOTAL UNIQUE TOWERDATA
    def unique_tower_counts(self):
        distinct_key_locations = self.collection.distinct("key_location")
        unique_source_counts_by_location = {}
        for location in distinct_key_locations:
            query = {"key_location": location}
            unique_source_numbers = self.collection.distinct("source_number", query)
            unique_source_counts_by_location[location] = len(unique_source_numbers)
    
         #TOWERDATA IMEI count
        distinct_key_locations = self.collection.distinct("key_location")
        unique_imei_counts_by_location = {}
        for location in distinct_key_locations:
            query = {"key_location": location}
            unique_imei_numbers = self.collection.distinct("imei", query)
            unique_imei_counts_by_location[location] = len(unique_imei_numbers)
    
        #State-wise Source Number
        distinct_key_locations = self.collection.distinct("key_location")
        unique_state_wise_count = {}
        for state in distinct_key_locations:
            query = {"key_location": location}
            state_wise_count = self.collection.count_documents(query)
            unique_state_wise_count[state] = state_wise_count


        #Cellid count
        distinct_key_locations = self.collection.distinct("key_location")
        unique_state_wise_sitenames = {}
        for key_location in distinct_key_locations:
            distinct_sitenames = self.collection.distinct("sitename", {"key_location": key_location})
            sitename_counts = {}
            for sitename in distinct_sitenames:
                first_cellid_count = self.collection.count_documents({"key_location": key_location, "sitename": sitename})
                sitename_counts[sitename] = first_cellid_count
            unique_state_wise_sitenames[key_location] = sitename_counts

                
        result = {
        "total_unique_source_count_towerdata": unique_source_counts_by_location,
        "total_unique_imei_count_towerdata": unique_imei_counts_by_location,
        "total_state-wise_count_towerdata": unique_state_wise_count,
        "total_state-wise_cellid_towerdata": unique_state_wise_sitenames
            
        }
        # for key,value in result.items():
        #     print(f"{key} : {value}")   
        # return result  
        if result:
            for key, value in result.items():
                print(f"{key} : {value}")
            return result
        else:
            print("No matching documents found") 
        
         
    def internal_calling(self, inputdata=None,fromdate=None,todate=None):
        """
        internal calling
        """
        print("internal calling function enterss==========")
        time1 = {'title':'Function starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time()}

        cellid_list = [cellid for tower in inputdata for cellid in tower.get('cellid', [])]
        sitename_list = [item.get('towername', '') for item in inputdata]

        logger.info("function starts")
        match_conditions = {
            "$and": [{'destination_number': {
                                '$regex': '^(91\\d{10}|\\d{10})$'
                            }}]
        }
        if len(sitename_list) > 0:
            print(sitename_list,"sitname")
            match_conditions["$and"].append({"sitename": {"$in": sitename_list}})
        if len(cellid_list) > 0:
            # print(sitename_list,"sitname")
            match_conditions["$and"].append({"first_cgid": {"$in": cellid_list}})

        if fromdate != None and todate != None:
            print(fromdate,todate,"-----------date range-------")
            from_date = datetime.strptime(fromdate, "%Y-%m-%dT%H:%M:%S")#.replace(hour=0, minute=0, second=0, microsecond=0)
            to_date = datetime.strptime(todate, "%Y-%m-%dT%H:%M:%S")#.replace(hour=23, minute=59, second=59, microsecond=999)
            
            match_conditions["$expr"] = {
                    "$and": [
                        {"$gte": [{"$dateFromString": {"dateString": {"$concat": ["$date", "T", "$time"]}, "format": "%d-%m-%YT%H:%M:%S"}}, from_date]},
                        {"$lte": [{"$dateFromString": {"dateString": {"$concat": ["$date", "T", "$time"]}, "format": "%d-%m-%YT%H:%M:%S"}}, to_date]}
                    ]
                }
        # print(match_conditions)
        # Construct the aggregation pipeline
        print(match_conditions,"----------match conditions")
        pipeline = [
            {
                "$match": match_conditions
            },
            {
                "$addFields": {
                    "calltypeLower": {"$toLower": "$call_type"}
                }
            },
            {
                "$group": {
                    "_id": {
                        "source_number": "$source_number",
                        "destination_number": "$destination_number",
                        "sitename": "$sitename",
                        "first_cgid":"$first_cgid",
                        "date":"$date",
                        "time":"$time",
                        "date_format":"$date_format"

                    },
                    "incoming": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$regexMatch": {
                                        "input": "$calltypeLower",
                                        "regex": "in",
                                    }
                                },
                                1,
                                0
                            ]
                        }
                    },
                    "outgoing": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$regexMatch": {
                                        "input": "$calltypeLower",
                                        "regex": "out",
                                    }
                                },
                                1,
                                0
                            ]
                        }
                    }
                }
            },
            {
                "$lookup": {
                    "from": "cdat_tower",
                    "let": {
                        "source_number": "$_id.source_number",
                        "destination_number": "$_id.destination_number",
                        "sitename": "$_id.sitename",
                        "first_cgid" : "$_id.first_cgid",
                        "date":"$_id.date",
                        "time":"$_id.time",
                        "date_format":"$_id.date_format"
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$or": [
                                        {
                                            "$and": [
                                                {"$eq": ["$source_number", "$$destination_number"]},
                                                {"$eq": ["$destination_number", "$$source_number"]},
                                                {"$eq": ["$sitename", "$$sitename"]},
                                                {"$eq": ["$date", "$$date"]},
                                                {"$ne": ["$source_number", None]},
                                                {"$ne": ["$destination_number", None]},
                                                {
                                                    "$or": [
                                                        {
                                                            "$and": [
                                                                { "$eq": [{ "$minute": { "$toDate": "$date_format" } }, { "$add": [{ "$minute": { "$toDate": "$$date_format" } }, 1] }] },
                                                                { "$eq": [{ "$hour": { "$toDate": "$date_format" } }, { "$hour": { "$toDate": "$$date_format" } }] }
                                                            ]
                                                        },
                                                        # {
                                                        #     "$and": [
                                                        #         { "$eq": [{ "$minute": { "$toDate": "$$date_format" } }, { "$add": [{ "$minute": { "$toDate": "$date_format" } }, 1] }] },
                                                        #         { "$eq": [{ "$hour": { "$toDate": "$$date_format" } }, { "$hour": { "$toDate": "$date_format" } }] }
                                                        #     ]
                                                        # },
                                                        {
                                                            "$eq": [
                                                                { "$minute": { "$toDate": "$date_format" } },
                                                                { "$minute": { "$toDate": "$$date_format" } }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    "as": "matchedPairs"
                }
            },
            {
                "$unwind": "$matchedPairs"  
            },
            # {
            #     "$sort":{
            #             'sitename':1,
            #             'date_format':1
            #             }
            # },
            {
                "$sort": {
                    "_id.sitename": 1,
                    "_id.date_format": 1
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "phone": "$_id.source_number",
                    "other": "$_id.destination_number",
                    "incoming": 1,
                    "outgoing": 1,
                    "sitename": "$_id.sitename",
                    "first_cellid":"$_id.first_cgid",
                    "date":"$_id.date",
                    "time":"$_id.time",
                    "date_format":"$_id.date_format"
                }
            }
            
        ]
        logger.info("Aggregation")
        # Execute the aggregation pipeline and retrieve the results
        time2 = {'title':'Mongo query internal call starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time()}
        results = list(self.collection.aggregate(pipeline))
        time3 = {'title':'Aggregation ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'iteration time':time.time() - time2['timestamp']}

        print(results)
        logger.info("Aggregation ends")
        logger.info('internal calling function ends')
        unique_results_list = []
        unique_results = set()
        for result in results:
            unique_results.add(tuple(result.items()))
        time4 = {'title':'function ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'iteration time':time.time() - time1['timestamp']}
        if unique_results:
            unique_results_list = [dict(item) for item in unique_results]
            # pprint(unique_results_list)
            sorted_results = sorted(unique_results_list, key=lambda x: (x['date'],x['time'],x['sitename']))

            logger.info("RESUKTSSS")
            response = {'unique_results_list':sorted_results,'status':'success','times':[time1,time2,time3,time4]}
            return response
        else:
            response = {'unique_results_list':[],'status':'failure', 'times':['no data']}
            return response
    
    # Call details
    def call_details(self, inputdata,fromdate,todate):
        print("inside call detials ")
        """
        Call Details – All calls done from tower with all details such as location address, other party details
        """
        time1 = {'title':'function starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time() }

        cellid_list = [cellid for tower in inputdata for cellid in tower.get('cellid', [])]
        sitename_list = [item.get('towername', '') for item in inputdata]
        print(inputdata,"call under tower")
        logger.info("function starts")
        match_conditions = {
            "$and": []
        }
        if len(sitename_list) > 0:
            print(sitename_list,"sitname")
            match_conditions["$and"].append({"sitename": {"$in": sitename_list}})
        
        if len(cellid_list) > 0:
            print(cellid_list,"sitename")
            match_conditions["$and"].append({"first_cgid": {"$in": cellid_list}})

        if fromdate != None and todate != None:
            print(fromdate,type(fromdate))
            
            from_date = datetime.strptime(fromdate, "%Y-%m-%dT%H:%M:%S")#.replace(hour=0, minute=0, second=0, microsecond=0)
            to_date = datetime.strptime(todate, "%Y-%m-%dT%H:%M:%S")#.replace(hour=23, minute=59, second=59, microsecond=999)
            match_conditions["$expr"] = {
                    "$and": [
                        {"$gte": [{"$dateFromString": {"dateString": {"$concat": ["$date", "T", "$time"]}, "format": "%d-%m-%YT%H:%M:%S"}}, from_date]},
                        {"$lte": [{"$dateFromString": {"dateString": {"$concat": ["$date", "T", "$time"]}, "format": "%d-%m-%YT%H:%M:%S"}}, to_date]}
                    ]
                }
        
        pipeline = [
            {
                "$match": match_conditions
            },
            {
                '$project':{
                    '_id':0,
                    'source_number':"$source_number",
                    'destination_number':"$destination_number",
                    'date':"$date",
                    'time':"$time",
                    'call_type':"$call_type",
                    'duration':"$duration",
                    'roaming':"$roaming_circle",
                    'imei':"$imei",
                    'imsi':"$imsi",
                    'first_cgid':"$first_cgid",
                    'last_cgid':"$last_cgid"
                }
            }
        ]
        time2 = {'title':'Aggregation starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time()}

        calldetails_data = list(mongocdat.towercdrdata.aggregate(pipeline))
        
        time3 = {'title':'Aggregation ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'iteration time':time.time() - time2['timestamp']}
        time4 = {'title':'function ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'iteration time':time.time() - time1['timestamp']}

        if len(calldetails_data) < 0:
            result_dict = {'call_details':[],'status':'failure','times':['nodata']}
            return result_dict
        else:
            result_dict = {'call_details' : calldetails_data , 'status':'success' , 'times':[time1,time2,time3,time4]}
            return result_dict
        
    
        
    #Day wise analysis
    def day_wise_analysis(self, sitenames, start_date, end_date):
        # sitenames = ["ARALAM", "ADAKKATHODE (BSNL)", "MANNANTHARA", "KELAKAM", "Peravoor"]  
        # start_date = "01-02-2023"
        # end_date = "07-02-2023"
        """
        Day wise analysis of towers
        """

        start_datetime = datetime.strptime(start_date, "%d-%m-%Y")
        end_datetime = datetime.strptime(end_date, "%d-%m-%Y")

        matched_pairs = set()

        for i in range(len(sitenames)):
            for j in range(i + 1, len(sitenames)):
                sitename1 = sitenames[i]
                sitename2 = sitenames[j]

                documents_sitename1 = list(self.collection.find({"sitename": sitename1, "date": {"$gte": start_date, "$lte": end_date}}))
                documents_sitename2 = list(self.collection.find({"sitename": sitename2, "date": {"$gte": start_date, "$lte": end_date}}))

                for doc1 in documents_sitename1:
                    source1 = doc1["source_number"]
                    destination1 = doc1["destination_number"]
                    sitename_1 = doc1["sitename"]
                    date_1 = datetime.strptime(doc1["date"], "%d-%m-%Y")

                    for doc2 in documents_sitename2:
                        source2 = doc2["source_number"]
                        destination2 = doc2["destination_number"]
                        sitename_2 = doc2["sitename"]
                        date_2 = datetime.strptime(doc2["date"], "%d-%m-%Y")

                        if sitename_1 != sitename_2 and start_datetime <= date_1 <= end_datetime and start_datetime <= date_2 <= end_datetime:
                            if (source1 == destination2 and destination1 == source2) and (doc1 != doc2):
                                matched_pairs.add((source1, destination1, sitename_1))
                                matched_pairs.add((source2, destination2, sitename_2))

        matched_pairs_dict = {
            "MatchedPairs": [{"Source": source, "Destination": destination, "Sitename": sitename} for source, destination, sitename in matched_pairs]
        }
        print(matched_pairs_dict)
        # return matched_pairs_dict
        if matched_pairs_dict:
            return matched_pairs_dict
        else:
            print("No matching documents found")

    #Summary
    def summary(self, inputdata, fromdate, todate):

        """
        Summary – Summary of all calls done from tower
        """
      
        logger.info("profleinfo retriving")
        # getprofile = self.contact_info(data)
        getdata = []
        cellid_list = [cellid for tower in inputdata for cellid in tower.get('cellid', [])]
        sitename_list = [item.get('towername', '') for item in inputdata]
        print(inputdata,"call under tower")
        logger.info("function starts")
        match_conditions = {
            "$and": []
        }
        if len(sitename_list) > 0:
            print(sitename_list,"sitname")
            match_conditions["$and"].append({"sitename": {"$in": sitename_list}})
        
        if len(cellid_list) > 0:
            print(cellid_list,"sitename")
            match_conditions["$and"].append({"first_cgid": {"$in": cellid_list}})

        if fromdate != None and todate != None:
            print(fromdate,type(fromdate))
            
            from_date = datetime.strptime(fromdate, "%Y-%m-%dT%H:%M:%S")#.replace(hour=0, minute=0, second=0, microsecond=0)
            to_date = datetime.strptime(todate, "%Y-%m-%dT%H:%M:%S")#.replace(hour=23, minute=59, second=59, microsecond=999)
            match_conditions["$expr"] = {
                    "$and": [
                        {"$gte": [{"$dateFromString": {"dateString": {"$concat": ["$date", "T", "$time"]}, "format": "%d-%m-%YT%H:%M:%S"}}, from_date]},
                        {"$lte": [{"$dateFromString": {"dateString": {"$concat": ["$date", "T", "$time"]}, "format": "%d-%m-%YT%H:%M:%S"}}, to_date]}
                    ]
                }
        print(match_conditions)
        pipeline = [
            {
                "$match": match_conditions
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
                    "duration":{"$sum":"$duration"},
                    "total_calls":{"$sum": 1}
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
                    "address": {"$ifNull": ["$sdrData.local_address", "no address found"]},
                    "call_in": 1,
                    "call_out": 1,
                    "total_calls":1,
                    "duration":1,
                    "first_call": 1,
                    "last_call": 1
                }
            }
        ]
        
        getdata = list(mongocdat.towercdrdata.aggregate(pipeline))

        
        logger.info("mongo retriving")
        


        if len(getdata) < 0:
            response = {'result': [],'status':'failure','message':'no data found'}
        else:
            response = {'result': getdata,'status':'success','message':'data retrived successfully'}

        return response
            

    def number_summary(self, number):
        print(number,"-number---")

        """
        Summary – Summary of all calls done from tower
        """
      
        logger.info("profleinfo retriving")
        # getprofile = self.contact_info(data)
        
        
        
        pipeline = [
            {
                "$match": {'source_number' : number}
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
                    "duration":{"$sum":"$duration"},
                    "total_calls":{"$sum": 1}
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
                    "address": {"$ifNull": ["$sdrData.local_address", "no address found"]},
                    "call_in": 1,
                    "call_out": 1,
                    "total_calls":1,
                    "duration":1,
                    "first_call": 1,
                    "last_call": 1
                }
            }
        ]
        
        result = list(mongocdat.towercdrdata.aggregate(pipeline))

        
        logger.info("mongo retriving")
        


        if len(result) < 0:
            response = {'result': [],'status':'failure','message':'no data found'}
        else:
            response = {'result': result,'status':'success','message':'data retrived successfully'}

        return response
    
                     
    #Calculate_area_description
    def tower_groups_location_time(self, lat, long, radius_km):
        """
        Create tower groups on location or time basis for analysis
        """
        print(lat)
        print(long)
        print(radius_km)
        try:
            matching_area_descriptions = []

            radius_meters = int(radius_km) * 1000

            towers_in_circle = list(self.collection_newcell.find({
                'location': {
                    '$near': {
                        '$geometry': {
                            'type': "Point",
                            'coordinates': [float(long), float(lat)]
                        },
                        '$maxDistance': radius_meters
                    }
                }
            }, {"_id": 0}))
            print(len(towers_in_circle),"==========")
            tower_dict = {}

            for tower in towers_in_circle:

                area = tower.get('areadescription')
                # print(area)
                if area not in tower_dict:
                    tower_dict[area] = {}
                    tower_dict[area]['towername'] = area
                    tower_dict[area]['cellid'] = [cell_id['celltowerid'] for cell_id in self.collection_newcell.find({'areadescription':area})] #tower.get('celltowerid')
                    tower_dict[area]['state'] = [cell_id['state'] for cell_id in self.collection_newcell.find({'areadescription':area}).sort("lastupdate",pymongo.DESCENDING).limit(1)]
                    tower_dict[area]['provider'] = tower.get('operator')
            # print(tower_dict)
            tower_data = list(tower_dict.values())
            if len(tower_data) > 0:
                # print(tower_data)
                return tower_data
            else:
                return ["No matching area descriptions found"]

        except Exception as e:
            print(e)
            return [f"Error processing data: {str(e)}"]
        
    
    def tower_track():
        tower_name = ['EOR_FD10_RPTLKH-01_SR', 'Aalachi', 'ARYAPARAMB', 'AMBAYATHODE','ARALAM']

        towername = {}
        for site in tower_name:
            towername[site] = set(mongocdat.towercdrdata.distinct('source_number', {'sitename': site}))

        num = []
        for size in range(2, len(tower_name) + 1):
            combinations_list = list(combinations(tower_name, size))

            for combo in combinations_list:
                # print(combo)
                common_num = {}
                common_num['towername'] = list(combo)
                common_num['numbers'] = list(set.intersection(*[towername[key] for key in combo]))
                num.append(common_num)

        common_num = {}
        sets = [set(values) for values in towername.values()]
        intersection = set.intersection(*sets)
        common_num['towername'] = tower_name
        common_num['numbers'] = list(intersection)
        num.append(common_num)

        # print(num)
        return num

              
    def common_numbers_in_towers(self,mode, inputdata=None, sitename_list=None, fromdate=None, todate=None):
        """
        Numbers common in different towers
        and 
        Other party common in different towers
        """
        print(inputdata,"common lookup",mode)

        # inputdata =  [{'towername': 'Addatheegala', 'cellid': ['29-21572', '29-21571']}, {'towername': 'VALAYAMKODE', 'cellid': ['29-56471', '29-56473']}, {'towername': 'VEERPADU', 'cellid': ['29-48271', '29-48272']}]
        if mode == "common_source":  
            in_val = "source_number"
        if mode == "common_destination":  
            in_val = "destination_number"
        if mode == "common_imei":  
            in_val = "imei"
        towername = {}
        for site in inputdata:
            towername[site['towername']] = set(self.collection.distinct(in_val,{'sitename':site['towername']}))
        # print(towername)
        keys = list(towername.keys())
        num = []
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                common_num = {}
                print(len(towername[keys[i]]),"------",keys[j])
                set_a = set(towername[keys[i]])
                set_b = set(towername[keys[j]])
                union = set_a.intersection(set_b)
                common_num['towername'] = f"{keys[i]}_{keys[j]}"
                common_num['numbers'] = list(union)
                num.append(common_num)
              
               
        
        sets = [set(values) for values in towername.values()]
        intersection = set.intersection(*sets)
        common_num = {}
        common_num['towername'] = "All Towers"
        common_num['numbers'] = list(intersection)
        num.append(common_num)
        common_num = {}

        return num
    

    def aggregate_tower_data(self, inputdata):
        print("aggregate_inside",inputdata)
        match_conditions = {"calltype": { '$in': ['Voice_IN', 'Voice_OUT', 'SMO', 'SMT'] }}
        # sitename_list = ['VEERPADU']
        sitename_list = []
        firstcellid = []
        for in_val in inputdata:
            sitename_list.append(in_val['towername'])
            # firstcellid.append(in_val['cellid'])

        if len(sitename_list) > 0:
            match_conditions['sitename'] = {"$in": sitename_list}
         
        # if len(firstcellid) > 0:
        #     match_conditions['first_cellid'] = {"in": firstcellid}

        print(match_conditions,"----------------------------------------")
        pipeline = self.collection.aggregate([
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
                    "no_unique_imei_count_local": { "$addToSet": "$imei" },
                    "no_unique_tower_count": { "$addToSet": "$sitename" },
                    "no_unique_sector_count": { "$addToSet": "$first_cellid" },
                    "call_type_count": {
                        "$push": {
                            "$switch": {
                                "branches": [
                                    { "case": { "$in": ["$calltype", ["Voice_IN", "Voice_OUT"]] }, "then": "inout" },
                                    { "case": { "$in": ["$calltype", ["SMO", "SMT"]] }, "then": "smosmi" }
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
                        "$sum": { "$cond": [{ "$in": ["$calltype", ["Voice_IN"]] }, 1, 0] }
                    },
                    "total_out_count": {
                        "$sum": { "$cond": [{ "$in": ["$calltype", ["Voice_OUT"]] }, 1, 0] }
                    },
                    "total_smo_count": {
                        "$sum": { "$cond": [{ "$in": ["$calltype", ["SMO"]] }, 1, 0] }
                    },
                    "total_smt_count": {
                        "$sum": { "$cond": [{ "$in": ["$calltype", ["SMT"]] }, 1, 0] }
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
                    "imei": { "$size": "$no_unique_imei_count_local" },
                    "tower": { "$size": "$no_unique_tower_count" },
                    "sector": { "$size": "$no_unique_sector_count" },
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
                            "No 'CALL' or 'SMS' data available"
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
                    "imei": { "$first": "$imei" },
                    "tower": { "$first": "$tower" },
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

#-----------------common analysis---------------#

    def roaming_details(self,number,fromdate=None, todate=None):
        """Groups documents by state for a given number within an optional date range
        and returns the document count for each state along with source_number."""
        numbers = number.split(",")
        
        native = list(self.collection_sdr.find({'source_number':{"$in":numbers}},{'_id':0,'source_number':1,'state':1,'date_of_activation':1}))
        print(native)
        
        match_conditions = {}
        
        if fromdate and todate:
            from_date = datetime.strptime(fromdate, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
            to_date = datetime.strptime(todate, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=999)
            match_conditions = {
                "$expr": {
                        "$and": [
                            {"$gte": [{"$dateFromString": {"dateString": "$date", "format": "%d-%m-%Y"}}, from_date]},
                            {"$lte": [{"$dateFromString": {"dateString": "$date", "format": "%d-%m-%Y"}}, to_date]}
                        ]
                }
            }

        pipeline_cdr = [
            {"$match": {**match_conditions,
                        "source_number":{"$in":numbers},
                        "state":{"$ne": ["",None]}}},  
            {"$group": {
                "_id": {"state": "$state", "source_number": "$source_number"},
                "count": {"$sum": 1}  
            }},
            {"$project": {
                "_id": 0,
                "state": "$_id.state",
                "source_number": "$_id.source_number",
                "count": 1,
                "from":"cdr"
            }}
        ]

        pipeline_tower = [
            {"$match": {**match_conditions,
                        "source_number":{"$in":numbers},
                        "state":{"$ne": ["",None]}}},  
            {"$group": {
                "_id": {"state": "$state", "source_number": "$source_number"},
                "count": {"$sum": 1}  
            }},
            {"$project": {
                "_id": 0,
                "state": "$_id.state",
                "source_number": "$_id.source_number",
                "count": 1,
                "from":"tower"
            }}
        ]
        
        
        pipeline_ipdr = [
            {
                "$match":{ **match_conditions,
                          "msisdn":{"$in":numbers}} 
            },
            {
                "$lookup": {
                    "from": "cdat_cellid",
                    "localField": "cell_id",
                    "foreignField": "celltowerid",
                    "as": "tower_data"
                }
            },
            {
                "$unwind": "$tower_data"
            },
            {
                "$group": {
                    "_id": {
                        "msisdn": "$msisdn",
                        "state": "$tower_data.state"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source_number": "$_id.msisdn",
                    "state": "$_id.state",
                    "count": 1,
                    "from":"ipdr"
                }
            }
        ]

        result3 = list(self.collection_ipdr.aggregate(pipeline_ipdr))
        pprint(result3)
        result1 = list(self.collection_cdr.aggregate(pipeline_cdr))
        result2 = list(self.collection.aggregate(pipeline_tower))
        print(result2,"-------")
        result = result1 + result2 + result3
        roaming_circle = []
        print(result)
        for item in result:
            roaming_circle.append({
                'source_number':item['source_number'],
                'state':item.get('state',''),
                'count':item['count'],
                'from':item['from']
            })
        print(native,"----native")
        response = {'data_dict':roaming_circle if roaming_circle else 'No Data',
                    'native_dict':native if native else 'No Data'}
        # pprint(result)
        return response

    def roaming_analysis_details(self,number,fromdate=None, todate=None):
        """Groups documents by state for a given number within an optional date range
        and returns the document count for each state along with source_number."""
        numbers = number.split(",")
        
        native = list(self.collection_sdr.find({'source_number':{"$in":numbers}},{'_id':0,'source_number':1,'state':1,'date_of_activation':1}))
        print(native)
        
        match_conditions = {}
        
        if fromdate and todate:
            match_conditions = {
                "timestamp": {
                    "$gte": datetime.strptime(fromdate, "%Y-%m-%dT%H:%M").timestamp(),
                    "$lte": datetime.strptime(todate, "%Y-%m-%dT%H:%M").timestamp()
                }
            }

        pipeline_cdr = [
            {"$match": {**match_conditions,
                        "source_number":{"$in":numbers},
                        "state":{"$ne": ["",None]}}},  
            {"$group": {
                "_id": {"state": "$state", "source_number": "$source_number"},
                "count": {"$sum": 1}  
            }},
            {"$project": {
                "_id": 0,
                "state": "$_id.state",
                "source_number": "$_id.source_number",
                "count": 1,
                "from":"cdr"
            }}
        ]

        pipeline_tower = [
            {"$match": {**match_conditions,
                        "source_number":{"$in":numbers},
                        "state":{"$ne": ["",None]}}},  
            {"$group": {
                "_id": {"state": "$state", "source_number": "$source_number"},
                "count": {"$sum": 1}  
            }},
            {"$project": {
                "_id": 0,
                "state": "$_id.state",
                "source_number": "$_id.source_number",
                "count": 1,
                "from":"tower"
            }}
        ]
        
        
        pipeline_ipdr = [
            {
                "$match":{ **match_conditions,
                          "msisdn":{"$in":numbers}} 
            },
            {
                "$lookup": {
                    "from": "cdat_cellid",
                    "localField": "cell_id",
                    "foreignField": "celltowerid",
                    "as": "tower_data"
                }
            },
            {
                "$unwind": "$tower_data"
            },
            {
                "$group": {
                    "_id": {
                        "msisdn": "$msisdn",
                        "state": "$tower_data.state"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source_number": "$_id.msisdn",
                    "state": "$_id.state",
                    "count": 1,
                    "from":"ipdr"
                }
            }
        ]

        result3 = list(self.collection_ipdr.aggregate(pipeline_ipdr))
        pprint(result3)
        result1 = list(self.collection_cdr.aggregate(pipeline_cdr))
        result2 = list(self.collection.aggregate(pipeline_tower))
        print(result2,"-------")
        result = result1 + result2 + result3
        roaming_circle = []
        print(result)
        for item in result:
            roaming_circle.append({
                'source_number':item['source_number'],
                'state':item.get('state',''),
                'count':item['count'],
                'from':item['from']
            })
        print(native,"----native")
        response = {'data_dict':roaming_circle if roaming_circle else 'No Data',
                    'native_dict':native if native else 'No Data'}
        pprint(result)
        return response
    
    
    
    
    def active_and_inactive_period(self,number):
        number = number.split(",")
        pipeline = [
            {
                "$match": {"source_number":{"$in": number}}
            },
            {
                "$group": {
                    "_id": {
                        "source_number": "$source_number",
                        "sitename": "$sitename"
                    },
                    "dates": {"$addToSet": "$date"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source_number": "$_id.source_number",
                    "sitename": "$_id.sitename",
                    "dates": "$dates"
                }
            },
            {
                "$unwind": "$dates"
            },
            {
                "$group": {
                    "_id": {
                        "source_number": "$source_number",
                        "sitename": "$sitename"
                    },
                    "startdate": {"$min": {"$dateFromString": {"dateString": "$dates", "format": "%d-%m-%Y"}}},
                    "enddate": {"$max": {"$dateFromString": {"dateString": "$dates", "format": "%d-%m-%Y"}}},
                    "allDates": {"$addToSet": "$dates"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source_number": "$_id.source_number",
                    "sitename": "$_id.sitename",
                    "startdate": {"$dateToString": {"format": "%Y-%m-%d", "date": "$startdate"}},
                    "enddate": {"$dateToString": {"format": "%Y-%m-%d", "date": "$enddate"}},
                    "allDates": 1,
                    "from":"towerdata"
                }
            }
        ]
        result1 = list(self.collection.aggregate(pipeline))
        pipeline2 = [
            {
                "$match": {"source_number":{"$in": number}}
            },
            {
                "$group": {
                    "_id": {
                        "source_number": "$source_number",
                        "sitename": "$sitename"
                    },
                    "dates": {"$addToSet": "$date"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source_number": "$_id.source_number",
                    "sitename": "$_id.sitename",
                    "dates": "$dates"
                }
            },
            {
                "$unwind": "$dates"
            },
            {
                "$group": {
                    "_id": {
                        "source_number": "$source_number",
                        "sitename": "$sitename"
                    },
                    "startdate": {"$min": {"$dateFromString": {"dateString": "$dates", "format": "%d-%m-%Y"}}},
                    "enddate": {"$max": {"$dateFromString": {"dateString": "$dates", "format": "%d-%m-%Y"}}},
                    "allDates": {"$addToSet": "$dates"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source_number": "$_id.source_number",
                    "sitename": "$_id.sitename",
                    "startdate": {"$dateToString": {"format": "%Y-%m-%d", "date": "$startdate"}},
                    "enddate": {"$dateToString": {"format": "%Y-%m-%d", "date": "$enddate"}},
                    "allDates": 1,
                    "from":"cdrdata"
                }
            }
        ]
        
        pipeline_ipdr = [
            {
                "$lookup": {
                    "from": "cdat_cellid",
                    "localField": "cell_id",
                    "foreignField": "celltowerid",
                    "as": "tower_data"
                }
            },
            {
                "$unwind": "$tower_data"
            },
            {
                "$group": {
                    "_id": {
                        "sitename": "$tower_data.areadescription",
                        "msisdn": "$msisdn"
                    },
                    "allDates": {"$addToSet": "$date"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "sitename": "$_id.sitename",
                    "msisdn": "$_id.msisdn",
                    "allDates": 1,
                    "from":"ipdrdata",
                    "startdate": {
                        "$min": {
                            "$dateFromString": {
                                "dateString": {
                                    "$arrayElemAt": ["$allDates", 0]  
                                },
                                "format": "%Y-%m-%d"  
                            }
                        }
                    },
                    "enddate": {
                        "$max": {
                            "$dateFromString": {
                                "dateString": {
                                    "$arrayElemAt": ["$allDates", -1] 
                                },
                                "format": "%Y-%m-%d" 
                            }
                        }
                    }
                }
            }
        ]

        
        result3 = list(self.collection_ipdr.aggregate(pipeline_ipdr))
        print(result3)
        
        result2 = list(self.collection_cdr.aggregate(pipeline2))
        print(result2,"----")
        result = result1 + result2
        pprint(result)
        period_list = []
        for item in result:
            source_number = item['source_number'] 
            sitename = item.get('sitename')
            start_date = item['startdate']
            end_date = item['enddate']
            active_dates = item['allDates']
            source = item['from']
            
            # Convert date strings to datetime objects for comparison
            start_date_m = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_m = datetime.strptime(end_date, "%Y-%m-%d")

            # Convert active_dates to datetime objects
            active_dates_f = [datetime.strptime(date, "%d-%m-%Y") for date in active_dates]

            # Generate a list of all dates between start_date and end_date
            all_dates_range = [start_date_m + timedelta(days=x) for x in range((end_date_m - start_date_m).days + 1)]
            all_dates = [date.strftime("%d-%m-%Y") for date in all_dates_range]

            # Find inactive dates (dates not present in active_dates)
            inactive_dates = [date for date in all_dates if date not in [dt.strftime("%d-%m-%Y") for dt in active_dates_f]]
            
            cdr = {
                'source_number':source_number,
                'sitename':sitename,
                'start_date':start_date,
                'end_date':end_date,
                'source':source,
                'active_dates':len(active_dates),
                'inactive_dates':len(inactive_dates)
            }
            period_list.append(cdr)
            
        response = {'data_dict':period_list if period_list else 'No Data'}   
        pprint(period_list)
        return response
     

    # need to add in frontend
    def is_newentry(self, number, sitename, fromdate, todate):
        # sitename = sitename.split(",")
        # Convert fromdate and todate strings to datetime objects with the 'd-m-y' format
        from_date = datetime.strptime(fromdate, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
        to_date = datetime.strptime(todate, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=999)
        earliest_date_cdr = None 
        earliest_date_ipdr = None 
        
        pipeline_tower = [
        {
            "$match": {
                "sitename": sitename,
                "source_number": number,
                "$expr": {
                    "$and": [
                        {"$gte": [
                            {"$dateFromString": {"dateString": "$date", "format": "%d-%m-%Y"}},
                            from_date
                        ]},
                        {"$lte": [
                            {"$dateFromString": {"dateString": "$date", "format": "%d-%m-%Y"}},
                            to_date
                        ]}
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$sitename",
                "count_within_range": {"$sum": 1},
                "earliest_date": {"$min": {"$dateFromString": {"dateString": "$date", "format": "%d-%m-%Y"}}}
            }
        }
        ]
                
        pipeline_cdr = [
            {
                "$match": {
                    "source_number": number
                }
            },
            {
                "$group": {
                    "_id": {
                        "source_number": number
                    },
                    "unique_first_cgid": {
                        "$push": "$first_cgid"
                    }
                }
            },
            {
                "$lookup": {
                    "from": "cdat_cellid",
                    "localField": "unique_first_cgid",
                    "foreignField": "celltowerid",
                    "as": "matched_docs"
                }
            },
            {
                "$unwind": "$matched_docs"
            },
            {
                "$match": {
                    "matched_docs.areadescription": sitename
                }
            },
            {
                "$group": {
                    "_id": "$matched_docs.celltowerid",
                    "unique_cgid": {
                        "$push": "$matched_docs.celltowerid"
                    }
                }
            },
            {
                "$project": {
                    "unique_cgid": 1
                }
            },
            {
                "$unwind": "$unique_cgid"
            },
            {
                "$lookup": {
                    "from": "cdr",
                    "localField": "unique_cgid",
                    "foreignField": "first_cgid",
                    "as": "matched_cgid_docs"
                }
            },
            {
                "$unwind": "$matched_cgid_docs"
            },
            {
                "$group": {
                    "_id": None,
                    "earliest_date_cdr": {
                        "$min": {
                            "$dateFromString": {"dateString": "$matched_cgid_docs.date", "format": "%d-%m-%Y"}
                        }
                    }
                }
            }
        ]
        
        pipeline_ipdr = [
            {
                "$match": {
                    "msisdn": number
                }
            },
            {
                "$group": {
                    "_id": {
                        "msisdn": number
                    },
                    "unique_cell_id": {
                        "$push": "$cell_id"
                    }
                }
            },
            {
                "$lookup": {
                    "from": "cdat_cellid",
                    "localField": "unique_cell_id",
                    "foreignField": "celltowerid",
                    "as": "matched_docs"
                }
            },
            {
                "$unwind": "$matched_docs"
            },
            {
                "$match": {
                    "matched_docs.areadescription":  sitename
                }
            },
            {
                "$group": {
                    "_id": "$matched_docs.celltowerid",
                    "unique_cellid": {
                        "$push": "$matched_docs.celltowerid"
                    }
                }
            },
            {
                "$project": {
                    "unique_cellid": 1
                }
            },
            {
                "$unwind": "$unique_cellid"
            },
            {
                "$lookup": {
                    "from": "ipdr",
                    "localField": "unique_cellid",
                    "foreignField": "cell_id",
                    "as": "matched_cellid_docs"
                }
            },
            {
                "$unwind": "$matched_cellid_docs"
            },
            {
                "$group": {
                    "_id": None,
                    "earliest_date_ipdr": {
                        "$min": "$matched_cellid_docs.time"             
                        }
                    }
                }

        ]
        result_ipdr = list(self.collection_ipdr.aggregate(pipeline_ipdr))
        if result_ipdr:
            earliest_date_ipdr = min(entry.get("earliest_date_ipdr") for entry in result_ipdr if "earliest_date_ipdr" in entry)
            print(earliest_date_ipdr,"-ipdr---")
        result_cdr = list(self.collection_cdr.aggregate(pipeline_cdr))
        if result_cdr:
            earliest_date_cdr = min(entry.get("earliest_date_cdr") for entry in result_cdr if "earliest_date_cdr" in entry)
        
        result_tower = list(self.collection.aggregate(pipeline_tower))
        if result_tower:
            tower_start_dates = [entry.get('earliest_date') for entry in result_tower if entry['count_within_range'] > 0]
            if tower_start_dates:
                start_date_tower = min(tower_start_dates)
                result = [{'tower':'','cdr':'','ipdr':''}]
                if start_date_tower is not None or earliest_date_cdr is not None or earliest_date_ipdr is not None:
                    if start_date_tower and start_date_tower < from_date:
                        tower = (f"User with number {number} is an old existing user from {start_date_tower} found in tower data")
                    if earliest_date_cdr is not None:
                        if earliest_date_cdr < from_date:
                            cdr = (f"User with number {number} is an old existing user from {earliest_date_cdr} found in CDR data")
                    if earliest_date_ipdr is not None:
                        if earliest_date_ipdr < from_date:
                            ipdr = (f"User with number {number} is an old existing user from {earliest_date_ipdr} found in IPDR data") 
                        result.append({'tower':tower,'cdr':cdr,'ipdr':ipdr})
                        return result  
                    else:
                        new = (f"User with number {number} is a new user for this {sitename}")
                        return new
                else:
                    error = ("Invalid start date for the given date range")
                    return error
            else:
                error = (f"User with number {number} is not present within the given date range")
                return error
            
    def tower_profile(self,inputdata,fromdate,todate):
        time1 = {'title':'function starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time()}

        cellid_list = [cellid for tower in inputdata for cellid in tower.get('cellid', [])]
        sitename_list = [item.get('towername', '') for item in inputdata]
        print(inputdata,"call under tower")
        logger.info("function starts")
        match_conditions = {
            "$and": []
        }
        if len(sitename_list) > 0:
            print(sitename_list,"sitname")
            match_conditions["$and"].append({"sitename": {"$in": sitename_list}})
        
        if len(cellid_list) > 0:
            print(cellid_list,"sitename")
            match_conditions["$and"].append({"first_cgid": {"$in": cellid_list}})

        if fromdate != None and todate != None:
            print(fromdate,type(fromdate))
           
            print(fromdate,todate)
            from_date = datetime.strptime(fromdate, "%Y-%m-%dT%H:%M:%S")#.replace(hour=0, minute=0, second=0, microsecond=0)
            to_date = datetime.strptime(todate, "%Y-%m-%dT%H:%M:%S")#.replace(hour=23, minute=59, second=59, microsecond=999)
            
            match_conditions["$expr"] = {
                    "$and": [
                        {"$gte": [{"$dateFromString": {"dateString": {"$concat": ["$date", "T", "$time"]}, "format": "%d-%m-%YT%H:%M:%S"}}, from_date]},
                        {"$lte": [{"$dateFromString": {"dateString": {"$concat": ["$date", "T", "$time"]}, "format": "%d-%m-%YT%H:%M:%S"}}, to_date]}
                    ]
                }
        result = {}
        print(match_conditions,"(((((((((((((#############)))))))))))))")
        # match_conditions = {'source_number':{'$in':data}}

        # match_conditions['source_number'] = data
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
                    "provider":{"$addToSet": "$provider"},
                    "total_calls_count": {"$push": {"id": "$_id","count": 1}},
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
                        "$sum": { "$cond": [{ "$eq": ["$call_type", "call_in"] }, 1, 0] }
                    },
                    "callOutCount": {
                        "$sum": { "$cond": [{ "$eq": ["$call_type", "call_out"] }, 1, 0] }
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
                    "from": "cdat_sdr",
                    "localField": "source_number",
                    "foreignField": "source_number",
                    "as": "sdrData"
                },
            },
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
                    "fullname": {"$first": "$sdrData.fullname"},
                    "date_of_activation": {"$first": "$sdrData.date_of_activation"},
                    "local_address": {"$first": "$sdrData.local_address"},
                    "alternate_number": {"$first": "$sdrData.alternate_number"},
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
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source_number": "$_id",
                    "nickname": 1,
                    "fullname": 1,
                    "date_of_activation": 1,
                    "local_address": 1,
                    "alternate_number": 1,
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
                    "total_in_count":1,
                    "total_out_count":1,
                    "total_callin_count":1,
                    "total_callout_count":1,
                    "total_smsin_count":1,
                    "total_smsout_count":1,
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
        time2 = {'title':'Aggregation for tower profile starts','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'timestamp':time.time()}
        result = list(self.collection.aggregate(pipeline))
        time3 = {'title':'Aggregation ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'query time':time.time() - time2['timestamp']}

        # print(result,"-------resukgtuf")
        response = []
        for item in result:
            data = item['source_number']
            sms_data = self.only_sms(data)
            incoming = self.only_incoming(data)
            outgoing = self.only_outgoing(data)
            # print(sms_data,incoming,outgoing)
            item['only_sms'] = sms_data if sms_data else []
            
            item['only_incoming'] = incoming if incoming else []

            item['only_outgoing'] = outgoing if outgoing else []

            # print(item,"-----item------")
            response.append(item)
        # print(response,"-----------response----------")
        time4 = {'title':'function ends','time':datetime.now().strftime('%d-%m-%Y %H:%M:%S'), 'iteration time':time.time() - time1['timestamp']}
        if len(response) < 0:
            data = {'response':[],'status':'failure','message':'no data found','times':['no data']}
        else:
            data = {'response':response,'status':'success','message':'data retrived successfully','times':[time1,time2,time3,time4]}
            
        return data


    def only_sms(self,data):
        pipeline = [
                    {
                        '$match': {
                            'source_number': data,
                            'destination_number': {
                                '$regex': '^(91\\d{10}|\\d{10})$'
                            }
                        }
                    },
                    {
                        "$group": {
                            "_id": "$destination_number",
                            "call_types": { "$addToSet": "$call_type" },
                            "count": { "$sum": 1 }  
                        }
                    },
                    {
                        "$match": {
                            "$or": [
                                { "call_types": { "$all": ["sms_in", "sms_out"], "$nin": ["call_in", "call_out"] } },
                                { "call_types": { "$in": ["sms_in", "sms_out"], "$nin": ["call_in", "call_out"] } }
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
    
        sms = list(self.collection.aggregate(pipeline))
        # print(sms)
        return sms


    def only_incoming(self,data):
        pipeline = [
                    {
                        '$match': {
                            'source_number': data,
                            'destination_number': {
                                '$regex': '^(91\\d{10}|\\d{10})$'
                            }
                        }
                    },
                    {
                        "$group": {
                            "_id": "$destination_number",
                            "call_types": { "$addToSet": "$call_type" },
                            "count": { "$sum": 1 }  
                        }
                    },
                    {
                        "$match": {
                                "call_types": { "$all": ["call_in"], "$nin": ["sms_in", "sms_out","call_out"] },
                            
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

        incoming = list(self.collection.aggregate(pipeline))
        # print(incoming)
        return incoming

    def only_outgoing(self,data):
        pipeline = [
                    {
                        '$match': {
                            'source_number': data,
                            'destination_number': {
                                '$regex': '^(91\\d{10}|\\d{10})$'
                            }
                        }
                    },
                    {
                        "$group": {
                            "_id": "$destination_number",
                            "call_types": { "$addToSet": "$call_type" },
                            "count": { "$sum": 1 }  
                        }
                    },
                    {
                        "$match": {
                                "call_types": { "$all": ["call_out"], "$nin": ["sms_in", "sms_out","call_in"] },
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

        outgoing = list(self.collection.aggregate(pipeline))

        # print(outgoing)
        return outgoing