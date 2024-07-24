import re
from loguru import logger
from datetime import datetime
import time
from bson.json_util import dumps
from datetime import datetime
import time,re
from pprint import pprint
import pymongo
from MongoClinet import CDAT
mongocdat = CDAT() 


from itertools import combinations

def tower_track(casename,casetype):
    tower_name = ['EOR_FD10_RPTLKH-01_SR', 'Addatheegala', 'Orella_RR2130_2,HTD']#, 'AMBAYATHODE','ARALAM']

    towername = {}
    for site in tower_name:
        towername[site] = set(mongocdat.indcase.distinct('source_number', {'first_siteaddress': site}))
        # print(towername[site])
        towername[site].update((mongocdat.indcase.distinct('destination_number', {'first_siteaddress': site})))

    num = []
    for size in range(2, len(tower_name) + 1):
        combinations_list = list(combinations(tower_name, size))

        for combo in combinations_list:
            # print(combo)
            common_num = {}
            common_num['towername'] = list(combo)
            common_num['numbers'] = list(set.intersection(*[towername[key] for key in combo]))
            if len(common_num['numbers']) != 0:
                num.append(common_num)

    common_num = {}
    sets = [set(values) for values in towername.values()]
    intersection = set.intersection(*sets)
    common_num['towername'] = tower_name
    common_num['numbers'] = list(intersection)
    num.append(common_num)

    pprint(num)
    query = {'data':num,'description':'Numbers are tracked for a given redflag locations','timestamp':datetime.now(),'casename':casename,'casetype':casetype,'redflagtype':'Tower Track'}
    mongocdat.notification.insert_one(query)
    return num

def getdata(flagtype):
    val = mongocdat.redflag.find()
    
    return dumps(val)



def update_redflag(flagtype,flagid, data):
    print(flagtype,flagid,data,"----------")
    data = data.split(",")
    _t = []
    for _d in data:
        tower = {}
        tower['towername'] = _d
        getdata = mongocdat.cellidchart.find_one({'areadescription':_d})
        if getdata is not None: 
            for x in getdata:
                tower['lat'] = x['lat']
                tower['long'] = x['long']
        else:
            tower['lat'] = 0
            tower['long'] = 0

            _t.append(tower)
    print(_t,"=============")
    mongocdat.redflag.insert_one({'flagtype':flagtype,'flagid':flagid,'tower':_t})    


    return "sucess"


def matched_bparty_contact(casename,casetype):
    pipeline = [
            {
                '$match': {
                    'destination_number': {
                        '$regex': '^(91\\d{10}|\\d{10})$'
                    }
                }
            },
            {
                '$match': {
                    '$expr': {
                        '$ne': ['$destination_number', '$source_number']
                    }
                }
            },
            {
                '$group': {
                    '_id': '$destination_number'
                }
            },
            {
                '$lookup': {
                    'from': 'ind_cases',

                    'let': { 'local_dest_number': '$_id' },
                    'pipeline': [
                        {
                            '$match': {
                                'casename' : casename,
                                'casetype' : casetype,
                                '$expr': {
                                    '$or': [
                                        { '$eq': ['$destination_number', '$$local_dest_number'] },
                                        { '$eq': ['$source_number', '$$local_dest_number'] }
                                    ]
                                }
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
                                    'source_destination': {
                                        '$cond': {
                                            'if': { '$eq': ['$destination_number', '$$local_dest_number'] },
                                            'then': '$destination_number',
                                            'else': '$source_number'
                                        }
                                    }
                                },
                                'first_call': { '$min': { '$toDate': '$timestamp_in_milliseconds' } }, 
                                'last_call': { '$min': { '$toDate': '$timestamp_in_milliseconds' } },                                'doc_count': { '$sum': 1 }
                            }
                        },
                        {
                            '$project': {
                                '_id': 0,
                                'number': '$_id.source_destination',
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
                                'total_docs': '$doc_count'
                            }
                        }
                    ],
                    'as': 'tower_matches'
                }
            },
            {
                '$match': {
                    'tower_matches': { '$ne': [] }
                }
            },
            {
                '$unwind': '$tower_matches'
            },
            {
                '$project': {
                    '_id': 0,
                    'destination_number': '$_id',
                    'first_call': '$tower_matches.first_call',
                    'last_call': '$tower_matches.last_call',
                    'total_doc': '$tower_matches.total_docs'
                }
            }
        ]


    result = list(mongocdat.cdrdata.aggregate(pipeline))
    pprint(result)
    for i in result:
        print(i)

    query = {'data':result,'description':'Numbers who are contacted with suspect destinations are found','timestamp':datetime.now(),'casename':casename,'casetype':casetype,'redflagtype':'Bparty track'}
    mongocdat.notification.insert_one(query)

    return result


def getnotify():
    return list(mongocdat.notification.find({},{'_id':0}).sort('timestamp', pymongo.DESCENDING))
    


# tower_track()