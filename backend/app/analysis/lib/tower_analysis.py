from pymongo import MongoClient
from loguru import logger
from datetime import datetime
import pymongo
from itertools import combinations
from MongoClinet import CDAT
mongocdat = CDAT()


class Tower_View():
    def __init__(self):
        self.db = mongocdat.db
        self.collection = mongocdat.towercdrdata
        self.collection_cellidchart = mongocdat.cellidchart
        
        # self.client2 = MongoClient('mongodb://10.50.50.230:27017')
        # self.db2 = self.client2['CDAT']
        # self.collection_newcell = self.db2['cellidchart_nov16'] 


    def calls_under_tower(self, key_location=False, sitename_list=False, fromdate=False, todate=False):
        """
        Calls under tower
        """
        logger.info("function starts")
        match_conditions = {
            "$and": []
        }

        if key_location != "undefined":
            key_location = key_location.split(",")
            print(key_location,"keyloc")
            match_conditions["$and"].append({"key_location": {"$in": key_location}})

        if sitename_list != "undefined":
            sitename_list = sitename_list.split(",")
            print(sitename_list,"sitname")
            match_conditions["$and"].append({"sitename": {"$in": sitename_list}})
        else:
            match_conditions["$and"].append({"sitename": {"$exists": True}})

        if fromdate != "undefined" and todate != "undefined":
            match_conditions["$and"].extend([
                {"date": {"$gte": fromdate}},
                {"date": {"$lte": todate}}
            ])
        print(match_conditions)
        # Construct the aggregation pipeline
        pipeline = [
            {
                "$match": match_conditions
            },
            {
                "$addFields": {
                    "calltypeLower": {"$toLower": "$calltype"}
                }
            },
            {
                "$group": {
                    "_id": {
                        "source_number": "$source_number",
                        "destination_number": "$destination_number",
                        "key_location": "$key_location",
                        "sitename": "$sitename",
                        "first_cellid":"$first_cellid",
                        "date":"$date",
                        "time":"$time"

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
                        "first_cellid" : "$_id.first_cellid",
                        "date":"$_id.date",
                        "time":"$_id.time"
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
                                                {"$ne": ["$source_number", None]},
                                                {"$ne": ["$destination_number", None]},
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
                "$unwind": "$matchedPairs"  # Unwind the matchedPairs array
            },
            {
                "$project": {
                    "_id": 0,
                    "phone": "$_id.source_number",
                    "other": "$_id.destination_number",
                    "incoming": 1,
                    "outgoing": 1,
                    "key_location": "$_id.key_location",
                    "sitename": "$_id.sitename",
                    "first_cellid":"$_id.first_cellid",
                    "date":"$_id.date",
                    "time":"$_id.time"



                }
            }
        ]
        logger.info("Aggregation")
        # Execute the aggregation pipeline and retrieve the results
        results = list(self.collection.aggregate(pipeline))
        logger.info("Aggregationends")

        logger.info(f'Calls under tower function ends')
        unique_results = set()
        for result in results:
            unique_results.add(tuple(result.items()))

        if unique_results:
            unique_results_list = [dict(item) for item in unique_results]
            logger.info("RESUKTSSS")
            return unique_results_list
        else:
            print("No matching documents found")

    
   
    def common_numbers_in_different_towers(self,mode, key_locations=None, sitename_list=None, fromdate=None, todate=None):
        """
        Numbers common in different towers
        and 
        Other party common in different towers
        """
        match_conditions = {}
        

        if key_locations != "undefined":
            if not isinstance(key_locations, list):
                key_locations = [key_locations]  
            match_conditions["key_location"] = {"$in": key_locations}

        if sitename_list != "undefined":
            if not isinstance(sitename_list, list):
                sitename_list = [sitename_list] 
            match_conditions["sitename"] = {"$in": sitename_list}

        if fromdate != "undefined" and todate != "undefined":
            match_conditions["date"] = {"$gte": fromdate, "$lte": todate}
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
            common_source_numbers = list(self.collection.aggregate(source_pipeline))
            print(len(common_source_numbers))
            return common_source_numbers 
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
            print(len(common_destination_numbers))
        return  common_destination_numbers 
    




    def common_imei_in_different_towers(self,key_locations=None, sitename_list=None, fromdate=None, todate=None):
        """
        IMEI common in different towers
        """
        match_conditions = {}

        if key_locations != "undefined":
            if not isinstance(key_locations, list):
                key_locations = [key_locations]  # Convert a single key_location to a list
            match_conditions["key_location"] = {"$in": key_locations}

        if sitename_list != "undefined":
            if not isinstance(sitename_list, list):
                sitename_list = [sitename_list]  # Convert a single sitename to a list
            match_conditions["sitename"] = {"$in": sitename_list}

        if fromdate != "undefined" and todate != "undefined":
            match_conditions["date"] = {"$gte": fromdate, "$lte": todate}

        # Create the aggregation pipeline to find common source_numbers and their common towers
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
        print(common_imei_numbers)
        return  common_imei_numbers

    def group_of_numbers(self, phone_numbers, target_key_location, target_sitename):
        '''
        Groups of numbers in different towers
        '''
    
        print(target_sitename,target_key_location,phone_numbers,";;;;;;;;;;;;;;;;;")
        phone_numbers = phone_numbers.split(",") #["6006351760", "6000043627", "6238293752", "6238783726", "6238114280", "6238386498", "6238182894", "6238666519", "6238294621", "6238877292"] 
        #  need to correc for multiple oinputs
        target_key_location = target_key_location.split(",") #["KERALA_ARALAM_0405_JIO_TOWER_CDRS", "GANDAMARDHANA_HILLS_AT_TOWER_CDRS", "  "]
        if target_sitename != "undefined":
            target_sitename = target_sitename.split(",")   # ["Aralam farm", "ANGADIKADAV", "MANNANTHARA", "Peravoor"]
        else:
            print("No matching documents found")   
        
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

                        cellids_dict = [ source_number, cellids]
                        result_dict[sitename]["Phone Numbers and Cellids"].append(cellids_dict)

                result_dict[sitename]["Not Available Phone Numbers"] = unmatched_source_numbers

                print(result_dict)

        # return result_dict
        if result_dict:
            result_dict = list(result_dict.values())
            return result_dict
        else:
            print("No matching documents found")

    def unique_common_groups_in_different_towers(self, sitename_list=None, fromdate=None, todate=None):
        """
        Finding relation of calls between different tower groups.
        """
        match_conditions = {}

        if sitename_list != "undefined":
            sitename_list = sitename_list.split(",")
            match_conditions["sitename"] = {"$in": sitename_list}

        if fromdate != "undefined" and todate != "undefined":
            match_conditions["date"] = {"$gte": fromdate, "$lte": todate}

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
                    "cellids": {
                        "$addToSet": "$first_cellid"
                    },
                    "sitenames": {
                        "$addToSet": "$sitename"
                    }
                }
            },
            {
                "$match": {
                    "cellids.1": {"$exists": True},  
                    "sitenames.1": {"$exists": True} 
                }
            },
            {
                "$group": {
                    "_id": "$sitenames", 
                    "common_groups": {
                        "$push": {
                            "common_group": "$_id",
                            "different_cellids": "$cellids"
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "matched_sitenames": "$_id",
                    "matched_groups": "$common_groups"
                }
            }
        ]

        unique_common_groups = list(self.collection.aggregate(pipeline))
        print(unique_common_groups, "unique_common_groups")
        return unique_common_groups
    


    
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
        
         
    #Internal calling between towers
    def internal_calling(self, sitenames=None, key_location=None):
        """
        Internal calling between towers
        """
        if sitenames is None and key_location is None:
            print("No sitenames or key location specified.")
            return {}

        matched_pairs_dict = {}
        processed_pairs = set()

        if sitenames:
            for sitename1 in sitenames:
                for sitename2 in sitenames:
                    if sitename1 == sitename2:
                        continue

                    pair_key = "_".join(sorted([sitename1, sitename2]))

                    if pair_key in processed_pairs:
                        continue

                    documents_sitename1 = list(self.collection.find({"sitename": sitename1}))
                    documents_sitename2 = list(self.collection.find({"sitename": sitename2}))

                    matched_pairs = set()

                    for doc1 in documents_sitename1:
                        source1 = doc1["source_number"]
                        destination1 = doc1["destination_number"]
                        sitename_1 = doc1["sitename"]

                        for doc2 in documents_sitename2:
                            source2 = doc2["source_number"]
                            destination2 = doc2["destination_number"]
                            sitename_2 = doc2["sitename"]

                            if sitename_1 != sitename_2:
                                if source1 == destination2 and destination1 == source2:
                                    matched_pairs.add((source1, destination1, sitename_1))
                                    matched_pairs.add((source2, destination2, sitename_2))

                    matched_pairs_dict_key = f"{sitename1}_{sitename2}"
                    matched_pairs_dict[matched_pairs_dict_key] = {
                        "MatchedPairs": [{"source": source, "destination": destination, "sitename": sitename_1} for source, destination, sitename_1 in matched_pairs],
                    }

                    processed_pairs.add(pair_key)
        elif key_location:
            key_location_sitenames = list(self.collection.distinct("sitename", {"key_location": key_location}))

            for sitename1 in key_location_sitenames:
                for sitename2 in key_location_sitenames:
                    if sitename1 == sitename2:
                        continue

                    pair_key = "_".join(sorted([sitename1, sitename2]))

                    if pair_key in processed_pairs:
                        continue

                    documents_sitename1 = list(self.collection.find({"sitename": sitename1}))
                    documents_sitename2 = list(self.collection.find({"sitename": sitename2}))

                    matched_pairs = set()

                    for doc1 in documents_sitename1:
                        source1 = doc1["source_number"]
                        destination1 = doc1["destination_number"]
                        sitename_1 = doc1["sitename"]

                        for doc2 in documents_sitename2:
                            source2 = doc2["source_number"]
                            destination2 = doc2["destination_number"]
                            sitename_2 = doc2["sitename"]

                            if sitename_1 != sitename_2:
                                if source1 == destination2 and destination1 == source2:
                                    matched_pairs.add((source1, destination1, sitename_1))
                                    matched_pairs.add((source2, destination2, sitename_2))

                    matched_pairs_dict_key = f"{sitename1}_{sitename2}"
                    matched_pairs_dict[matched_pairs_dict_key] = {
                        "MatchedPairs": [{"source": source, "destination": destination, "sitename": sitename_1} for source, destination, sitename_1 in matched_pairs],
                    }

                    processed_pairs.add(pair_key)

        matched_pairs_dict = {k: v for k, v in matched_pairs_dict.items() if v["MatchedPairs"]}

        if matched_pairs_dict:
            processed_result = {}
            for key, value in matched_pairs_dict.items():
                pair_key = key.replace('_', ' and ').title()
                processed_result[pair_key] = []

                for matched_pair in value["MatchedPairs"]:
                    source = matched_pair["source"]
                    destination = matched_pair["destination"]
                    sitename = matched_pair["sitename"]

                    processed_pair = {
                        f"destination of {sitename}": destination,
                        "sitename": sitename,
                        f"source of {sitename}": source,
                    }

                    processed_result[pair_key].append(processed_pair)

            print(processed_result)
        else:
            print("No matched pairs found.")

        # return matched_pairs_dict
        if matched_pairs_dict:
            return matched_pairs_dict
        else:
            print("No matching documents found")

    
    
    
    #Call details
    def call_details(self, sitename=None):
        """
        Call Details – All calls done from tower with all details such as location address, other party details
        """
        # if sitename is None:
        #     sitename = "Aralam"  
        #     print(sitename, "sitename")

        documents_sitename = list(self.collection.find({"sitename": sitename}))
        print("print  documents_sitename")
        result_dict = {
            "sitename": sitename,
            "call_details": []
        }
        print("print result_dict")
        if not documents_sitename:
            result_dict["message"] = f"No documents found for sitename: {sitename}"
            return result_dict

        for doc in documents_sitename:
            source_number = doc["source_number"]
            destination_number = doc["destination_number"]
            # document_id = doc["_id"]  
            document_id = str(doc["_id"])  # Convert ObjectId to string
            date = doc["date"]
            time = doc["time"]
            call_type = doc["calltype"]
            duration = doc["duration"]
            roaming = doc["roaming"]
            imei = doc["imei"]
            imsi = doc["imsi"]
            first_cellid = doc["first_cellid"]
            last_cellid = doc["last_cellid"]
            
            result_dict["call_details"].append({
                "document_ID" : document_id,
                "source_number" : source_number,
                "destination_number" : destination_number,
                "date" : date,
                "time" : time,
                "call_type" : call_type,
                "duration" : duration,
                "roaming" : roaming,
                "IMEI" : imei,
                "IMSI" : imsi,
                "first_cellID" : first_cellid,
                "last_cellID" : last_cellid
                
            })
        # print(result_dict)

        # return result_dict
        if result_dict:
            return result_dict
        else:
            print("No matching documents found")
        
    
        
    
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
    def summary(self, source_number=None):
        """
        Summary – Summary of all calls done from tower
        """
        incoming_call_types = ['A2P_SMSIN', 'P2P_SMSIN', 'VDO-IN', 'Voice_IN', 'a_in', 'a_in_vw', 'a_in_wv', 'v_in', 'v_in_vw', 'v_in_wv']
        outgoing_call_types = ['P2AOUT', 'P2POUT', 'VDO-OUT', 'Voice_OUT', 'a_out', 'a_out_vw', 'a_out_wv', 'v_out', 'v_out_vw']

        query = {"calltype": {"$in": incoming_call_types + outgoing_call_types}}
        
        
            
        cursor = self.collection.find({'source_number':source_number})

        call_data_by_source_destination = {}
        first_call_for_destination = {}
        last_call_for_destination = {}

        for document in cursor:
            if "source_number" not in document:
                continue

            source_number = document["source_number"]
            destination_number = document["destination_number"]
            call_type = document["calltype"]
            
            call_date = document.get("date", "")
            call_time = document.get("time", "")
            
            duration = int(document.get("duration", 0))

            key = (source_number, destination_number)

            if key not in call_data_by_source_destination:
                call_data_by_source_destination[key] = {
                    "incoming_count": 0,
                    "outgoing_count": 0,
                    "total_duration": 0
                }

            if call_type in incoming_call_types:
                call_data_by_source_destination[key]["incoming_count"] += 1
                call_data_by_source_destination[key]["total_duration"] += duration
            elif call_type in outgoing_call_types:
                call_data_by_source_destination[key]["outgoing_count"] += 1
                call_data_by_source_destination[key]["total_duration"] += duration

            if key not in first_call_for_destination:
                first_call_for_destination[key] = {
                    "timestamp": f"{call_date} {call_time}",
                    "document": document
                }
            elif f"{call_date} {call_time}" < first_call_for_destination[key]["timestamp"]:
                first_call_for_destination[key] = {
                    "timestamp": f"{call_date} {call_time}",
                    "document": document
                }
            
            if key not in last_call_for_destination:
                last_call_for_destination[key] = {
                    "timestamp": f"{call_date} {call_time}",
                    "document": document
                }
            elif f"{call_date} {call_time}" > last_call_for_destination[key]["timestamp"]:
                last_call_for_destination[key] = {
                    "timestamp": f"{call_date} {call_time}",
                    "document": document
                }

        results = {}

        for (source_number, destination_number), counts in call_data_by_source_destination.items():
            result_key = f"{source_number}-{destination_number}"
            results[result_key] = {
                "Source Number": source_number,
                "Destination Number": destination_number,
                "Incoming Call Count": counts['incoming_count'],
                "Outgoing Call Count": counts['outgoing_count'],
                "Total Calls Count": counts['incoming_count'] + counts['outgoing_count'],
                "Total Duration": counts['total_duration'],
                "First Call Timestamp": first_call_for_destination[(source_number, destination_number)]["timestamp"],
                "Last Call Timestamp": last_call_for_destination[(source_number, destination_number)]["timestamp"]
            }

        # if source_number:
        #     print(f"Details for Source Number: {source_number}\n")
        #     print(results)
        # else:
        #     print("General Results:")
        #     print(results)
        if source_number:
            if results:
                print(results)
                res = list(results.values())
                return res
            else:
                print(f"No matching documents found for Source Number: {source_number}")
                return "no data"
        else:
            if results:
                print("General Results:")
                # print(results)
                return results
            else:
                print("No matching documents found")
                
                
                
    #under_tower_calls            
    def under_tower_calls(self, sitenames):
        """
        Under Tower Calls – Such calls where both numbers were present at tower location     
        """
        try:
            matching_pairs_dict = {}

            for sitename in sitenames:
                documents = self.collection.find({"sitename": sitename})
                matching_pairs = {}

                for doc in documents:
                    source_number = doc["source_number"]
                    destination_number = doc["destination_number"]
                    call_type = doc["calltype"]
                    first_cell_id = doc["first_cellid"]
                    call_date = doc["date"]
                    call_time = doc["time"]

                    reversed_pair = (destination_number, source_number)
                    query = {
                        "source_number": reversed_pair[0],
                        "destination_number": reversed_pair[1],
                        "sitename": sitename,
                        "date": call_date, 
                        "time": call_time,  
                    }
                    reversed_doc = self.collection.find_one(query)

                    if reversed_doc:
                        pair_key = tuple(sorted([source_number, destination_number]))
                        if pair_key in matching_pairs:
                            matching_pairs[pair_key].append({
                                "source": source_number,
                                "destination": destination_number,
                                "call_type": call_type,
                                "first_cell_id": first_cell_id,
                                "date": call_date,
                                "time": call_time
                            })
                        else:
                            matching_pairs[pair_key] = [{
                                "source": source_number,
                                "destination": destination_number,
                                "call_type": call_type,
                                "first_cell_id": first_cell_id,
                                "date": call_date,
                                "time": call_time
                            }]

                for pair_key, pairs_list in matching_pairs.items():
                    matching_pairs[pair_key] = sorted(pairs_list, key=lambda x: (x["date"], x["time"]))

                matching_pairs_dict[sitename] = matching_pairs

            results = matching_pairs_dict
            if results:
                print("General Results:")
                print(results)
                return results
            else:
                print("No matching documents found")
                return None

        except Exception as e:
            print(f"Error processing data: {str(e)}")

    
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

            towers_in_circle = list(self.collection_cellidchart.find({
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
                    tower_dict[area]['cellid'] = [cell_id['celltowerid'] for cell_id in self.collection_cellidchart.find({'areadescription':area})] #tower.get('celltowerid')
                    tower_dict[area]['state'] = [cell_id['state'] for cell_id in self.collection_cellidchart.find({'areadescription':area}).sort("lastupdate",pymongo.DESCENDING).limit(1)]
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
            towername[site] = set(mongo.collection_tower.distinct('source_number', {'sitename': site}))

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

        print(num)
        return num

        
        
  
  
        
        
        
    def common_numbers_in_towers(self,mode, inputdata=None, sitename_list=None, fromdate=None, todate=None):
        """
        Numbers common in different towers
        and 
        Other party common in different towers
        """
        print(inputdata,"common lookup",mode)

        inputdata =  [{'towername': 'Addatheegala', 'cellid': ['29-21572', '29-21571']}, {'towername': 'VALAYAMKODE', 'cellid': ['29-56471', '29-56473']}, {'towername': 'VEERPADU', 'cellid': ['29-48271', '29-48272']}]
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
        sitename_list = ['VEERPADU']
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
