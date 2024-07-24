
from pymongo import MongoClient
from pprint import pprint
from collections import defaultdict
from MongoClinet import CDAT
mongocdat = CDAT()
collection_towerid = mongocdat.towercdrdata
collection_cdr = mongocdat.cdrdata
collection_ipdr  = mongocdat.ipdrdata


# client = MongoClient('mongodb://localhost:27017')
# mongocdat = client['CDAT']
# collection_towerid = mongocdat['cdat_tower']
# collection_cdr = mongocdat['cdat_cdr']
# collection_towerid = mongocdat.towercdrdata
# collection_cdr = mongocdat.cdrdata

def tower_profile(data):
        result = {}
        pipeline = [
            {
                "$match": {'source_number':data}
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

        result = list(collection_towerid.aggregate(pipeline))

        sms_data = only_sms(data)
        incoming = only_incoming(data)
        outgoing = only_outgoing(data)
        
        result.append(sms_data) if sms_data else [{'only_sms':"no data"}]
        
        result.append(incoming) if incoming else [{'only_incoming':"no data"}]

        result.append(outgoing) if outgoing else [{'only_incoming':"no data"}]

        
        pprint(result)


        
        return result


def only_sms(data):
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
    

    result = list(collection_towerid.aggregate(pipeline))
    sms = {'only_sms':result}
    # print(sms)
    return sms


def only_incoming(data):
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

    result = list(collection_towerid.aggregate(pipeline))
    incoming = {'only_incoming':result}
    # print(incoming)
    return incoming

def only_outgoing(data):
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

    result = list(collection_towerid.aggregate(pipeline))
    outgoing = {'only_outgoing':result}

    # print(outgoing)
    return outgoing

def cdr_profile(data):
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
                                {"case": {"$eq": ["$incoming", 1]}, "then": 1},
                                {"case": {"$eq": ["$incoming", 0]}, "then": 0}
                            ],
                            "default": 0
                        }
                    }
                },
                "outgoing_calls": {
                    "$sum": {
                        "$switch": {
                            "branches": [
                                {"case": {"$eq": ["$incoming", 0]}, "then": 1},
                                {"case": {"$eq": ["$incoming", 1]}, "then": 0}
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

    result = list(collection_cdr.aggregate(pipeline))
    count_cdat = cdat_count(data)
    cdat = count_cdat[0]['destination_numbers']
    result.append({'cdat_count':cdat})
    pprint(result)
    return result



def cdat_count(number):
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
                                    {"$eq": ["$source_number", "$$destination_number"]}
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

    result = list(collection_cdr.aggregate(pipeline))
    print(result)
    return result

def cdat_contact(data):
    count_cdat = cdat_count(data)
    cdat = count_cdat[0]['destination_numbers']
    print(cdat,"----cdat---")
    pipeline = [
        {
            "$match": {
                'source_number': data,
                'destination_number':{"$in":cdat}
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
                "duration":{"$sum":"$duration"},
                "total_call":{"$sum": 1}
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
                "inc_officer": {"$ifNull": ["$suspectData.inc_officer", "Unknown"]},
                "address": {"$ifNull": ["$sdrData.local_address", "no address found"]},
                "call_in": 1,
                "call_out": 1,
                "total_call":1,
                "duration":1,
                "first_call": 1,
                "last_call": 1
            }
        }
    ]


    result = list(collection_cdr.aggregate(pipeline))
    pprint(result)




def state_track(data):
    data = data.split(",")
    cdr_pipeline = [
        {"$match": {"source_number": {"$in": data},"state":{"$ne":''}}},
        {"$sort": {"date_format": -1}},
        {"$group": {
            "_id": {"source_number": "$source_number", "state": "$state"},
            "doc": {"$first": "$$ROOT"}
        }},
        {"$sort": {"_id.source_number": 1, "doc.date_format": -1}},
        {"$group": {
            "_id": "$_id.source_number",
            "states_and_dates": {
                "$push": {
                    "state": "$_id.state",
                    "date": {"$dateToString": {"format": "%Y-%m-%d %H:%M:%S", "date": "$doc.date_format"}} }
            }
        }},
        {
            "$addFields": {
                "states_and_dates": {
                    "$map": {
                        "input": "$states_and_dates",
                        "in": {
                            "state": "$$this.state",
                            "date": "$$this.date",
                            "data": "cdr"
                        }
                    }
                }
            }
        },
        {"$project": {
            "source_number": "$_id",
            "last_two_states_and_dates": {
                "$slice": ["$states_and_dates", 2]
            }
        }}
    ]

    tower_pipeline = [
        {"$match": {"source_number": {"$in": data},"state":{"$ne":''}}},
        {"$sort": {"date_format": -1}},
        {"$group": {
            "_id": {"source_number": "$source_number", "state": "$state"},
            "doc": {"$first": "$$ROOT"}
        }},
        {"$sort": {"_id.source_number": 1, "doc.date_format": -1}},
        {"$group": {
            "_id": "$_id.source_number",
            "states_and_dates": {
                "$push": {
                    "state": "$_id.state",
                    "date": {"$dateToString": {"format": "%Y-%m-%d %H:%M:%S", "date": "$doc.date_format"}} }
            }
        }},
        {
            "$addFields": {
                "states_and_dates": {
                    "$map": {
                        "input": "$states_and_dates",
                        "in": {
                            "state": "$$this.state",
                            "date": "$$this.date",
                            "data": "tower"
                        }
                    }
                }
            }
        },
        {"$project": {
            "source_number": "$_id",
            "last_two_states_and_dates": {
                "$slice": ["$states_and_dates", 2]
            }
        }}
    ]

    ipdr_pipeline = [
        {"$match": {"msisdn": {"$in": data},"state":{"$ne":''}}},
        {"$sort": {"date_format": -1}},
        {"$group": {
            "_id": {"source_number": "$msisdn", "state": "$state"},
            "doc": {"$first": "$$ROOT"}
        }},
        {"$sort": {"_id.source_number": 1, "doc.date_format": -1}},
        {"$group": {
            "_id": "$_id.source_number",
            "states_and_dates": {
                "$push": {
                    "state": "$_id.state",
                    "date": {"$dateToString": {"format": "%Y-%m-%d %H:%M:%S", "date": "$doc.date_format"}} }
            }
        }},
        {
            "$addFields": {
                "states_and_dates": {
                    "$map": {
                        "input": "$states_and_dates",
                        "in": {
                            "state": "$$this.state",
                            "date": "$$this.date",
                            "data": "ipdr"
                        }
                    }
                }
            }
        },
        {"$project": {
            "source_number": "$_id",
            "last_two_states_and_dates": {
                "$slice": ["$states_and_dates", 2]
            }
        }}
    ]

    cdr = list(collection_cdr.aggregate(cdr_pipeline))   
    tower = list(collection_cdr.aggregate(tower_pipeline))   
    ipdr = list(collection_ipdr.aggregate(ipdr_pipeline))   

    result = cdr + tower + ipdr
    final_result = {}
    for item in result:
        if item['source_number'] not in final_result:
            final_result[item['source_number']] = []

        final_result[item['source_number']].extend([
            {
                'state': item['last_two_states_and_dates'][0]['state'],
                'date': item['last_two_states_and_dates'][0]['date'],
                'from': item['last_two_states_and_dates'][0]['data']
            },
            {
                'state': item['last_two_states_and_dates'][1]['state'],
                'date': item['last_two_states_and_dates'][1]['date'],
                'from': item['last_two_states_and_dates'][1]['data']
            }
        ])

    # pprint(final_result)
    result_dict = {}

    for phone_number, records in final_result.items():
        unique_states = set(record['state'] for record in records)
        sorted_records = sorted(records, key=lambda x: x['date'], reverse=True)
        print(f"Phone Number: {phone_number}")
        result_dict[phone_number] = {}
        for state in unique_states:
            state_records = [record for record in sorted_records if record['state'] == state]
            if state_records:  
                first_record = state_records[0]  
                result_dict[phone_number][state] = first_record

    pprint(result_dict)

    return result_dict


         

    # pprint(result)


# def new_data(user,numbers):
#     # numbers = numbers.split(",")
#     cdr_pipeline = [
#         {"$match": {"source_number": {"$in": numbers},"state":{"$ne":''}}},
#         {"$sort": {"date_format": -1}},
#         {"$group": {
#             "_id": {"source_number": "$source_number", "state": "$state"},
#             "doc": {"$first": "$$ROOT"}
#         }},
#         {"$sort": {"_id.source_number": 1, "doc.date_format": -1}},
#         {"$group": {
#             "_id": "$_id.source_number",
#             "states_and_dates": {
#                 "$push": {
#                     "state": "$_id.state",
#                     "date": {"$dateToString": {"format": "%Y-%m-%d %H:%M:%S", "date": "$doc.date_format"}} },
#                     # "cellid":"$doc.first_cgid"
#             }
#         }},
#         {
#             "$addFields": {
#                 "states_and_dates": {
#                     "$map": {
#                         "input": "$states_and_dates",
#                         "in": {
#                             "state": "$$this.state",
#                             "date": "$$this.date",
#                             # "cellid": "$$this.cellid",
#                             "data": "cdr"
#                         }
#                     }
#                 }
#             }
#         },
#         {"$project": {
#             "source_number": "$_id",
#             "last_two_states_and_dates": {
#                 "$slice": ["$states_and_dates", 2]
#             }
#         }}
#     ]
    

#     tower_pipeline = [
#         {"$match": {"source_number": {"$in": numbers},"state":{"$ne":''}}},
#         {"$sort": {"date_format": -1}},
#         {"$group": {
#             "_id": {"source_number": "$source_number", "state": "$state"},
#             "doc": {"$first": "$$ROOT"}
#         }},
#         {"$sort": {"_id.source_number": 1, "doc.date_format": -1}},
#         {"$group": {
#             "_id": "$_id.source_number",
#             "states_and_dates": {
#                 "$push": {
#                     "state": "$_id.state",
#                     "date": {"$dateToString": {"format": "%Y-%m-%d %H:%M:%S", "date": "$doc.date_format"}} },
#                     # "cellid":"$doc.first_cgid"
#             }
#         }},
#         {
#             "$addFields": {
#                 "states_and_dates": {
#                     "$map": {
#                         "input": "$states_and_dates",
#                         "in": {
#                             "state": "$$this.state",
#                             "date": "$$this.date",
#                             # "cellid": "$$this.cellid",
#                             "data": "tower"
#                         }
#                     }
#                 }
#             }
#         },
#         {"$project": {
#             "source_number": "$_id",
#             "last_two_states_and_dates": {
#                 "$slice": ["$states_and_dates", 2]
#             }
#         }}
#     ]

#     # ipdr_pipeline = [
#     #     {"$match": {"msisdn": {"$in": numbers},"state":{"$ne":''}}},
#     #     {"$sort": {"time": -1}},
#     #     {"$group": {
#     #         "_id": {"source_number": "$msisdn", "state": "$state"},
#     #         "doc": {"$first": "$$ROOT"}
#     #     }},
#     #     {"$sort": {"_id.source_number": 1, "doc.time": -1}},
#     #     {"$group": {
#     #         "_id": "$_id.source_number",
#     #         "states_and_dates": {
#     #             "$push": {
#     #                 "state": "$_id.state",
#     #                 "date": {"$dateToString": {"format": "%Y-%m-%d %H:%M:%S", "date": "$doc.time"}} },
#     #                 "cellid":"$doc.cellid",
#     #         }
#     #     }},
#     #     {
#     #         "$addFields": {
#     #             "states_and_dates": {
#     #                 "$map": {
#     #                     "input": "$states_and_dates",
#     #                     "in": {
#     #                         "state": "$$this.state",
#     #                         "date": "$$this.date",
#     #                         "cellid":"$$this.cellid",
#     #                         "data": "ipdr"
#     #                     }
#     #                 }
#     #             }
#     #         }
#     #     },
#     #     {"$project": {
#     #         "source_number": "$_id",
#     #         "last_two_states_and_dates": {
#     #             "$slice": ["$states_and_dates", 2]
#     #         }
#     #     }}
#     # ]

#     cdr = list(mongocdat.cdrdata.aggregate(cdr_pipeline))   
#     tower = list(mongocdat.towercdrdata.aggregate(tower_pipeline))   
#     # ipdr = list(mongocdat.ipdrdata.aggregate(ipdr_pipeline))   

#     result = cdr + tower #+ ipdr
#     pprint(result)
#     final_result = {}
#     for item in result:
#         if item['source_number'] not in final_result:
#             final_result[item['source_number']] = []

#         for state_info in item['last_two_states_and_dates']:
#             final_result[item['source_number']].append({
#                 'state': state_info.get('state', ''),
#                 'date': state_info.get('date', ''),
#                 'from': state_info.get('data', ''),
#                 'cellid': state_info.get('cellid', ''),
#             })

#     # pprint(final_result)
#     result_dict = {}

#     for phone_number, records in final_result.items():
#         unique_states = set(record['state'] for record in records)
#         sorted_records = sorted(records, key=lambda x: x['date'], reverse=True)[:2]
#         print(f"Phone Number: {phone_number}")
#         result_dict[phone_number] = {}
#         for state in unique_states:
#             state_records = [record for record in sorted_records if record['state'] == state]
#             if state_records:  
#                 first_record = state_records[0]  
#                 result_dict[phone_number][state] = first_record

#     pprint(result_dict)

#     return result_dict

   


if __name__ == "__main__":
    # data = "9059093788"
    data = "9354048282"

    # tower_profile(data)
    cdat_contact(data)


# db.cdr.aggregate([
#   {
#     $match: {
#       source_number: "your_source_number"
#     }
#   },
#   {
#     $group: {
#       _id: null,
#       start_date: { $min: { $dateFromString: { dateString: "$date", format: "%d-%m-%Y" } } },
#       end_date: { $max: { $dateFromString: { dateString: "$date", format: "%d-%m-%Y" } } },
#       dates: { $addToSet: { $dateFromString: { dateString: "$date", format: "%d-%m-%Y" } } },
#       incoming_calls: {
#         $sum: {
#           $switch: {
#             branches: [
#               { case: { $eq: ["$incoming", 1] }, then: 1 },
#               { case: { $eq: ["$incoming", 0] }, then: 0 }
#             ],
#             default: 0
#           }
#         }
#       },
#       outgoing_calls: {
#         $sum: {
#           $switch: {
#             branches: [
#               { case: { $eq: ["$incoming", 0] }, then: 1 },
#               { case: { $eq: ["$incoming", 1] }, then: 0 }
#             ],
#             default: 0
#           }
#         }
#       },
#       total_duration: { $sum: "$duration" },
#       unique_destination_numbers: { $addToSet: "$destination_number" },
#       documents: { $push: "$$ROOT" }
#     }
#   },
#   {
#     $addFields: {
#       one_to_one_call: {
#         $eq: [{ $size: "$unique_destination_numbers" }, 1]
#       },
#       only_sms: {
#         $size: {
#           $filter: {
#             input: "$documents",
#             as: "doc",
#             cond: { $eq: ["$$doc.duration", 0] }
#           }
#         }
#       },
#       no_transaction_calls: {
#         $eq: [{ $sum: "$documents.duration" }, 0]
#       },
#       total_present_dates: { $size: "$dates" }
#     }
#   },
#   {
#     $project: {
#       _id: 0,
#       source_number: "your_source_number",
#       start_date: { $dateToString: { format: "%d-%m-%Y", date: "$start_date" } },
#       end_date: { $dateToString: { format: "%d-%m-%Y", date: "$end_date" } },
#       total_present_dates: 1,
#       silent_days_count: { $subtract: [{ $size: "$dates" }, "$total_present_dates"] },
#       incoming_calls: 1,
#       outgoing_calls: 1,
#       total_duration: 1,
#       unique_destination_number_count: { $size: "$unique_destination_numbers" },
#       only_sms: 1,
#       no_transaction_calls: 1,
#       one_to_one_call: 1
#     }
#   }
# ])
    












# def new_data_old(user,numbers):
#     cdr_pipeline = [
#         {"$match": {"source_number": {"$in": numbers},"state":{"$ne":''}}},
#         {"$sort": {"date_format": -1}},
#         {"$group": {
#             "_id": {"source_number": "$source_number", "state": "$state"},
#             "doc": {"$first": "$$ROOT"}
#         }},
#         {"$sort": {"_id.source_number": 1, "doc.date_format": -1}},
#         {"$group": {
#             "_id": "$_id.source_number",
#             "states_and_dates": {
#                 "$push": {
#                     "state": "$_id.state",
#                     "cellid": "$doc.first_cgid",
#                     "sitename": "$doc.sitename",
#                     "date": {"$dateToString": {"format": "%Y-%m-%d %H:%M:%S", "date": "$doc.date_format"}} }
#             }
#         }},
#         {
#             "$addFields": {
#                 "states_and_dates": {
#                     "$map": {
#                         "input": "$states_and_dates",
#                         "in": {
#                             "state": "$$this.state",
#                             "date": "$$this.date",
#                             "cellid":"$$this.cellid",
#                             "areadescription":"$$this.sitename",
#                             "data": "cdr"
#                         }
#                     }
#                 }
#             }
#         },
#         {"$project": {
#             "source_number": "$_id",
#             "final_two": {
#                 "$slice": ["$states_and_dates", 2]
#             }
#         }}
#     ]
#     cdr = list(mongocdat.cdrdata.aggregate(cdr_pipeline))
#     final_result = {}
#     for item in cdr:
#         if item['source_number'] not in final_result:
#             final_result[item['source_number']] = []
#         final_result[item['source_number']].extend([
#             {
#                 'user': user,
#                 'source_number':item['source_number'],
#                 'state': item['final_two'][0]['state'],
#                 'date': item['final_two'][0]['date'],
#                 'cellid': item['final_two'][0]['cellid'],
#                 'areadescription':item['final_two'][0]['areadescription'],
#                 'data': item['final_two'][0]['data'],
#                 'lat': mongocdat.cellidchart.find_one({'celltowerid':item['final_two'][0]['cellid']},{'_id':0,'lat':1}).get('lat',''),
#                 'long': mongocdat.cellidchart.find_one({'celltowerid':item['final_two'][0]['cellid']},{'_id':0,'long':1}).get('long','')
#             },
#             {
#                 'user': user,
#                 'source_number':item['source_number'],
#                 'state': item['final_two'][0]['state'],
#                 'date': item['final_two'][0]['date'],
#                 'cellid': item['final_two'][0]['cellid'],
#                 'areadescription':item['final_two'][0]['areadescription'],
#                 'data': item['final_two'][0]['data'],
#                 'lat': mongocdat.cellidchart.find_one({'celltowerid':item['final_two'][0]['cellid']},{'_id':0,'lat':1}).get('lat',''),
#                 'long': mongocdat.cellidchart.find_one({'celltowerid':item['final_two'][0]['cellid']},{'_id':0,'long':1}).get('long','')
#             }
#         ])