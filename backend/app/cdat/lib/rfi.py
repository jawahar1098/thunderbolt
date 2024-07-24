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
from MongoClinet import Database
mongodata = Database()

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


def matched_bparty_contact(casename,casetype,user):
    print(casename,casetype)
    print(type(casename),type(casetype))
    filehashes = mongodata.filemanage.distinct('file_hash',{'redflag_check':'yes'})
    print(filehashes)
    pipeline = [
            {
                '$match': {
                    'destination_number': {
                        '$regex': '^(91\\d{10}|\\d{10})$'
                    },
                    'file_hash':{"$in":filehashes},
                    'casename':casename,
                    'casetype':casetype,
                    'user':user
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

    result = list(mongocdat.indcase.aggregate(pipeline))
    
    print(result,"------bparty result-------")
    if len(result)>0:
        query = {'read':'0','data':result,'description':'Numbers who are contacted with suspect destinations are found','timestamp':datetime.now(),'casename':casename,'casetype':casetype,'redflagtype':'Bparty track','user':user}
        mongocdat.notification.insert_one(query)

    # pprint(result)
    return result

def matched_bparty_contact(casename, casetype, user):
        print(casename, casetype, user, "-in bparty--")
        filehashes = mongodata.filemanage.distinct('file_hash',{'redflag_check':'yes'})

        pipeline = [
            {
                '$match': {
                    'casename': casename,
                    'casetype': casetype,
                    'user': user,
                    'file_hash':{'$in':filehashes},
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

        result = list(mongocdat.indcase.aggregate(pipeline))
        
        print(len(result))
        if len(result)>0:
            query = {'read':'0','data':result,'description':'Numbers who are contacted with suspect destinations are found','timestamp':datetime.now(),'casename':casename,'casetype':casetype,'redflagtype':'Bparty track','user':user}
            mongocdat.notification.insert_one(query)
        return result


def getnotify():
    return list(mongocdat.notification.find({},{'_id':0}).sort('timestamp', pymongo.DESCENDING))
    


# tower_track()