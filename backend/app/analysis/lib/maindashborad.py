from MongoClinet import CDAT, thunderbolt, VIGOR
import pymongo
import math
from pprint import pprint
from datetime import datetime
mongocdat = CDAT()
mongothunder = thunderbolt()
mongovigor = VIGOR()




def add_intresred_numbers(user,numbers):
    try:
        print(numbers)
        missing_numbers = mongothunder.number_anaysis.distinct('source_number', {'user':user})
        print(missing_numbers,"----missing_number----")
        # Insert missing numbers into the collection
        data_list = []
        for number in numbers:
            print(number)
            if number not in missing_numbers:
                print("new number")
                data = find_currentlocation(user,number)
                mongothunder.number_anaysis.insert_one(data)
                del data['_id']
                data_list.append(data)


        response = {'data_dict': data_list, 'status':'success', 'message':'numbers added successfully'}

        return response
    except Exception as e:
        response = {'data_dict': '', 'status':'failure', 'message':e}
        return response


def map_numbers(user):
    try:
        get_numbers = list(mongothunder.number_anaysis.find({'user':user},{'_id':0}))
        
        response = {'data_dict': get_numbers, 'status':'success', 'message':'numbers added successfully'}
        # print(response)
        return response
    except Exception as e:
        response = {'data_dict': '', 'status':'failure', 'message':str(e)}
        # print(response)
        return response
    

def find_currentlocation(user,number):
    print("inside find_currentlocation")
    list_loc = []
    cdr_data = mongocdat.cdrdata.find_one({'source_number':number},{'first_cgid':1,'date_format':1,'_id':0},sort=[('date_format', pymongo.DESCENDING)])
    if cdr_data is not None:
        cdr_data['source'] = 'cdr'
        cdr_data['date'] = cdr_data['date_format'].strftime('%Y-%m-%d %H:%M:%S')
        list_loc.append(cdr_data)
    tower_cdr = mongocdat.towercdrdata.find_one({'source_number':number},{'first_cgid':1,'date_format':1,'_id':0}, sort =[('date_format', pymongo.DESCENDING)])
    if tower_cdr is not None:
        tower_cdr['source'] = 'towercdr'
        tower_cdr['date'] = tower_cdr['date_format'].strftime('%Y-%m-%d %H:%M:%S')
        list_loc.append(tower_cdr)
    ipdr = mongocdat.ipdrdata.find_one({'msisdn':number},{'cell_id':1,'time':1,'_id':0}, sort =[('time', pymongo.DESCENDING)])
    if ipdr is not None:
        ipdr['source'] = 'ipdr'
        ipdr['first_cgid'] = ipdr['cell_id']
        ipdr['date'] = ipdr['time'].strftime('%Y-%m-%d %H:%M:%S')
        list_loc.append(ipdr)
    vigor = mongovigor.cri_meta.find_one({'TXT_TARGET_NUMBER':number},{'TXT_CELL_ID_A':1,'DAT_CALL_START':1,'_id':0}, sort =[('DAT_CALL_START', pymongo.DESCENDING)])
    if vigor is not None:
        vigor['source'] = 'lsb'
        vigor['first_cgid'] = vigor['TXT_CELL_ID_A']
        vigor['date'] = vigor['DAT_CALL_START'].strftime('%Y-%m-%d %H:%M:%S')
        list_loc.append(vigor)
    unique_data = []
    seen_first_cgid = set()

    for item in list_loc:
        if 'first_cgid' in item and item['first_cgid'] not in seen_first_cgid:
            unique_data.append(item)
            seen_first_cgid.add(item['first_cgid'])

    # Sort by 'date_format' in descending order
    sorted_data = sorted(unique_data, key=lambda x: x.get('date'), reverse=True)
    print(sorted_data,"----sorted data------")
    loc_dict = {'lat':'','long':'','areadescription':'','state':'','provider':'', 'status':"no_cellid_match", 'source_number':number, 'user':user}
    if len(sorted_data) > 0:
        print(sorted_data[0]['first_cgid'])
        get_lat_long = mongocdat.cellidchart.find_one({'celltowerid':sorted_data[0]['first_cgid']},sort=[('lastupdate', pymongo.DESCENDING)])
        print(type(get_lat_long),
        "========================================================================================")
        print(get_lat_long,"-----cellid data-----------------")
        if get_lat_long is not None:
            print("insied ")
            loc_dict['lat'] = get_lat_long['lat']
            loc_dict['long'] = get_lat_long['long']
            loc_dict['areadescription'] = get_lat_long['areadescription']
            loc_dict['state'] = get_lat_long['state']
            loc_dict['provider'] = get_lat_long['provider']
            loc_dict['date'] = sorted_data[0]['date']
            loc_dict['from'] = sorted_data[0]['source']
            loc_dict['source_number'] = number
            loc_dict['user'] = user
            loc_dict['status'] = "success"
        print(loc_dict,"--loc dict--")    
        return loc_dict   

        
    else:
        loc_dict = {'source_number':number, 'user':user, 'status':'no_data'}

        
        return loc_dict


def state_change_detection(user):
    print(user)
    get_numbers = mongothunder.number_anaysis.distinct('source_number',{'user':user})

    if get_numbers:
        result = cdr_state_finding(get_numbers)

    pass


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth specified in decimal degrees.
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return round(r * c)


def cdr_state_finding(user):
    numbers = mongothunder.number_anaysis.find({'user':user,"status":'success'},{'source_number':1,'state':1,'date':1})

    # if numbers:
    for number in numbers:
        # numbers = numbers.split(",")
        print(number,"newdaa numbers")
        date = datetime.strptime(number['date'], "%Y-%m-%dT%H:%M")
        cdr_pipeline = [
            {"$match": {"source_number": number, 
                        'date_format':{ '$gte': datetime.combine(date, datetime.min.time())},
                        "state":{"$ne":''}}},
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
                        "cellid":"$doc.first_cgid",
                        "provider":"$doc.provider",
                        "date": {"$dateToString": {"format": "%Y-%m-%d %H:%M:%S", "date": "$doc.date_format"}}
                        },
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
                                "cellid": "$$this.cellid",
                                "provider":"$$this.provider",
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
            }},
            {"$unwind": "$last_two_states_and_dates"},
            {"$lookup": {
                "from": "cdat_cellidchart",
                "localField": "last_two_states_and_dates.cellid",
                "foreignField": "celltowerid",
                "as": "tower_info"
            }},
            {"$unwind": "$tower_info"},
            {"$addFields": {
                "last_two_states_and_dates.lat": "$tower_info.lat",
                "last_two_states_and_dates.long": "$tower_info.long",
                "last_two_states_and_dates.sitename": "$tower_info.areadescription"
            }},
            {"$group": {
                "_id": "$source_number",
                "last_two_states_and_dates": {"$push": "$last_two_states_and_dates"}
            }}
        ]
        

        tower_pipeline = [
            {"$match": {"source_number": number,
                        'date_format':{ '$gte': datetime.combine(date, datetime.min.time())},
                        "state":{"$ne":''}}},
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
                        "cellid":"$doc.first_cgid",
                        "provider":"$doc.provider",
                        "date": {"$dateToString": {"format": "%Y-%m-%d %H:%M:%S", "date": "$doc.date_format"}} },
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
                                "cellid": "$$this.cellid",
                                "provider":"$$this.provider",
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
            }},
            {"$unwind": "$last_two_states_and_dates"},
            {"$lookup": {
                "from": "cdat_cellidchart",
                "localField": "last_two_states_and_dates.cellid",
                "foreignField": "celltowerid",
                "as": "tower_info"
            }},
            {"$unwind": "$tower_info"},
            {"$addFields": {
                "last_two_states_and_dates.lat": "$tower_info.lat",
                "last_two_states_and_dates.long": "$tower_info.long",
                "last_two_states_and_dates.sitename": "$tower_info.areadescription"
            }},
            {"$group": {
                "_id": "$source_number",
                "last_two_states_and_dates": {"$push": "$last_two_states_and_dates"}
            }}
        ]

        ipdr_pipeline = [
            {"$match": {"msisdn": number,
                        'date_format':{ '$gte': datetime.combine(date, datetime.min.time())},
                        "state":{"$ne":''}}},
            {"$sort": {"time": -1}},
            {"$group": {
                "_id": {"source_number": "$msisdn", "state": "$state"},
                "doc": {"$first": "$$ROOT"}
            }},
            {"$sort": {"_id.source_number": 1, "doc.time": -1}},
            {"$group": {
                "_id": "$_id.source_number",
                "states_and_dates": {
                    "$push": {
                        "state": "$_id.state",
                        "cellid":"$doc.cellid",
                        "provider":"$doc.provider",
                        "date": {"$dateToString": {"format": "%Y-%m-%d %H:%M:%S", "date": "$doc.time"}} },
                }
            }},
            {"$lookup": {
                "from": "cdat_cellidchart", 
                "localField": "last_two_states_and_dates.cellid",
                "foreignField": "celltowerid",
                "as": "tower_info"
            }},
            {
                "$addFields": {
                    "states_and_dates": {
                        "$map": {
                            "input": "$states_and_dates",
                            "in": {
                                "state": "$$this.state",
                                "date": "$$this.date",
                                "cellid":"$$this.cellid",
                                "provider":"$$this.provider",
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
            }},
            {"$unwind": "$last_two_states_and_dates"},
            {"$lookup": {
                "from": "cdat_cellid",
                "localField": "last_two_states_and_dates.cellid",
                "foreignField": "celltowerid",
                "as": "tower_info"
            }},
            {"$unwind": "$tower_info"},
            {"$addFields": {
                "last_two_states_and_dates.lat": "$tower_info.lat",
                "last_two_states_and_dates.long": "$tower_info.long",
                "last_two_states_and_dates.sitename": "$tower_info.areadescription"
            }},
            {"$group": {
                "_id": "$source_number",
                "last_two_states_and_dates": {"$push": "$last_two_states_and_dates"}
            }}
        ]

        cdr = list(mongocdat.cdrdata.aggregate(cdr_pipeline))   
        tower = list(mongocdat.towercdrdata.aggregate(tower_pipeline))   
        ipdr = list(mongocdat.ipdrdata.aggregate(ipdr_pipeline))   
        # print(cdr,"===========aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        result = cdr + tower + ipdr
        final_result = {}
        for item in result:
            if item['_id'] not in final_result:
                final_result[item['_id']] = []

            for state_info in item['last_two_states_and_dates']:
                final_result[item['_id']].append({
                    'state': state_info.get('state', ''),
                    'date': state_info.get('date', ''),
                    'from': state_info.get('data', ''),
                    'cellid': state_info.get('cellid', ''),
                    'lat':state_info.get('lat',''),
                    'long':state_info.get('long',''),
                    'sitename':state_info.get('sitename',''),
                    'provider':state_info.get('provider','')
                })


        result_dict = {}

        for phone_number, records in final_result.items():
            unique_states = set(record['state'] for record in records)
            sorted_records = sorted(records, key=lambda x: x['date'], reverse=True)
            # print(f"Phone Number: {phone_number}")
            result_dict[phone_number] = {}
            
            state_counter = 0
            
            for state in sorted(unique_states, key=lambda x: max(record['date'] for record in sorted_records if record['state'] == x), reverse=True):
                state_records = [record for record in sorted_records if record['state'] == state]
                
                if state_records and state_counter < 2:  
                    first_record = state_records[0]  
                    result_dict[phone_number][state] = first_record
                    state_counter += 1
            if len(result_dict[phone_number]) == 2:
                lat1 = result_dict[phone_number][list(result_dict[phone_number].keys())[0]]['lat']
                lon1 = result_dict[phone_number][list(result_dict[phone_number].keys())[0]]['long']
                lat2 = result_dict[phone_number][list(result_dict[phone_number].keys())[1]]['lat']
                lon2 = result_dict[phone_number][list(result_dict[phone_number].keys())[1]]['long']
                distance = haversine(float(lat1), float(lon1), float(lat2), float(lon2))

                result_dict[phone_number]['distance'] = distance
                mongothunder.number_anaysis.update_one({'source_number':phone_number},{"$set": {'lat': result_dict[phone_number][list(result_dict[phone_number].keys())[0]]['lat'],
                                                                                                'pre_lat':result_dict[phone_number][list(result_dict[phone_number].keys())[1]]['lat'],
                                                                                                'long':result_dict[phone_number][list(result_dict[phone_number].keys())[0]]['long'],
                                                                                                'pre_long':result_dict[phone_number][list(result_dict[phone_number].keys())[1]]['long'],
                                                                                                'state':result_dict[phone_number][list(result_dict[phone_number].keys())[0]]['state'],
                                                                                                'pre_state':result_dict[phone_number][list(result_dict[phone_number].keys())[1]]['state'],
                                                                                                'cellid':result_dict[phone_number][list(result_dict[phone_number].keys())[0]]['cellid'],
                                                                                                'pre_cellid':result_dict[phone_number][list(result_dict[phone_number].keys())[1]]['cellid'],
                                                                                                'date':result_dict[phone_number][list(result_dict[phone_number].keys())[0]]['date'],
                                                                                                'pre_date':result_dict[phone_number][list(result_dict[phone_number].keys())[1]]['date'],
                                                                                                'from':result_dict[phone_number][list(result_dict[phone_number].keys())[0]]['from'],
                                                                                                'pre_from':result_dict[phone_number][list(result_dict[phone_number].keys())[1]]['from'],
                                                                                                'provider':result_dict[phone_number][list(result_dict[phone_number].keys())[0]]['provider'],
                                                                                                'pre_provider':result_dict[phone_number][list(result_dict[phone_number].keys())[1]]['provider'],
                                                                                                'distance': distance}})
            elif len(result_dict[phone_number]) == 1:
                mongothunder.number_anaysis.update_one({'source_number':phone_number},{"$set": {'lat': result_dict[phone_number][list(result_dict[phone_number].keys())[0]]['lat'],
                                                                                                'long':result_dict[phone_number][list(result_dict[phone_number].keys())[0]]['long'],
                                                                                                'state':result_dict[phone_number][list(result_dict[phone_number].keys())[0]]['state'],
                                                                                                'cellid':result_dict[phone_number][list(result_dict[phone_number].keys())[0]]['cellid'],
                                                                                                'date':result_dict[phone_number][list(result_dict[phone_number].keys())[0]]['date'],
                                                                                                'from':result_dict[phone_number][list(result_dict[phone_number].keys())[0]]['from'],
                                                                                                'provider':result_dict[phone_number][list(result_dict[phone_number].keys())[0]]['provider'],
                                                                                                }})
                


            print('update_one')   
        return result_dict





def add_lbs(number,user):
    for num in number:
        print(num,"-----------------")
        check_exists = mongothunder.lbstrack.find_one({'source_number':num})
        print(check_exists)
        if check_exists is None:
            data_dict = {'source_number':num,'lat':'','pre_lat':'','long':'','pre_long':'',}
            projection = {'TXT_TARGET_NUMBER':1, 'TXT_IMSI':1, 'TXT_IMEI':1, 'TXT_LATITUDE':1, 'TXT_LONGITUDE':1,'DAT_EVENT_TIME':1}
            latest_doc = mongovigor.lbs.find_one({'TXT_TARGET_NUMBER':num},projection,sort = [('_id', pymongo.DESCENDING)])
            print(latest_doc)
            if latest_doc is not None:
                data_dict['lat'] = latest_doc['TXT_LATITUDE'] 
                data_dict['long'] = latest_doc['TXT_LONGITUDE']
                data_dict['event_time'] = latest_doc['DAT_EVENT_TIME']
                data_dict['username'] = user
                mongothunder.lbstrack.insert_one(data_dict)
            else:
                mongothunder.lbstrack.insert_one(data_dict)
            
    response = {'status':'success', 'message':'numbers added successfully'}

    return response
        
def lbs_loc(user):
    getdata = mongothunder.lbstrack.find()
    res = []
    projection = {'TXT_TARGET_NUMBER':1, 'TXT_IMSI':1, 'TXT_IMEI':1, 'TXT_LATITUDE':1, 'TXT_LONGITUDE':1,'DAT_EVENT_TIME':1}
    for _g in getdata:
        
        latest_doc = mongovigor.lbs.find_one({'TXT_TARGET_NUMBER':_g['source_number']},projection,sort = [('_id', pymongo.DESCENDING)])
        if latest_doc is not None:
            _g['pre_lat'] = _g['lat']
            _g['pre_long'] = _g['long']
            _g['lat'] = latest_doc['TXT_LATITUDE']
            _g['long'] = latest_doc['TXT_LONGITUDE']
            _g['event_time'] = latest_doc['DAT_EVENT_TIME']
            del _g['_id']
            mongothunder.lbstrack.update_one({'source_number':_g['source_number']},{'$set':_g})
            if _g['username'] == user:
                res.append(_g)
            
    response = {'data_dict': res, 'status':'success', 'message':'fetched'}

    return response
            
            