from MongoClinet import CDAT,Database
from bson import ObjectId
from datetime import datetime , timedelta
import uuid
from pprint import pprint
import math


import pymongo
mongocdat = CDAT()
mongodata = Database()






class RFI():
    def __init__(self, result,user):
        self.id = result
        self.user = user
        print("insied class", self.user)

        self.data()
        

    def data(self):
        print("data---------------")
        self.filedata = mongodata.filemanage.find_one({'_id':ObjectId(self.id)},{'_id':0,'source_number':1,'from_date':1,'to_date':1,'filetype':1})
        print(self.filedata,"----------")
        self.source_number = self.filedata['source_number']
        self.st = self.filedata['from_date']
        self.et = self.filedata['to_date']
        self.ft = self.filedata['filetype']
        self.more_device()
        self.shared_device()
        self.zero_activity_day()
        if self.ft == "cdr":
            self.cdat_contact()
            self.only_incoming()
            self.only_outgoing()
        if self.ft == "ipdr":
            self.vpn_usage()
            self.foreign_isp()

    def convert_size(cls, size_bytes):
        # print(size_bytes, "inside convert")
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def more_device(self):
        print("inside more device")
        result = []
        if self.ft == "cdr" or  self.ft == "towercdr":
            number = "source_number"
        if self.ft == "ipdr":
            number = "msisdn"
        pipeline = [
            {
                '$match': {
                    number : self.source_number,
                    'date_format': {'$gte': self.st, '$lte': self.et},
                    'imei': {'$ne': '0'}
                }
            },
            {
                '$group': {
                    '_id': '$imei',
                    "count": {"$sum": 1}
                }
            },
            {
                "$match": {
                    "count": {"$gte": 2}
                }
            },
            {
                "$group": {
                    "_id": 0,
                    "imei": {"$addToSet":"$_id"},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "imei": "$imei",
                    "total_device":{"$size":"$imei"}
                }
            },

        ]

        # print(pipeline)
        if self.ft == "cdr":
            result = list(mongocdat.cdrdata.aggregate(pipeline))
        if self.ft == "towercdr":
            result = list(mongocdat.towercdrdata.aggregate(pipeline))
        if self.ft == "ipdr":
            result = list(mongocdat.ipdrdata.aggregate(pipeline))
        # print(result,"----------imei----------")
        if len(result) > 0:
            unique_id = uuid.uuid4().__str__()
            print(unique_id)
            print(str(unique_id),"-----------------------unique id---------------")
            response = {'rfid':str(unique_id),'seen':'0','result':result, 'status':'success', 'message':'more device found'}
            mongocdat.notification.insert_one({'rfid':str(unique_id),'seen':'0','redflagtype':"device",'data':result,'number':self.source_number,'user':self.user, 'casename':'','filetype':self.ft,'description':'Number which are available n more than two devices','timestamp':datetime.now()})
        else:
            response = {'result':[],'status':'failure', 'message':'no anomaly device found'}

        return response
    
    # not for single number it will check all data in db
    def shared_device(self):
        imei = []
        if self.ft == "cdr":
            number = "$source_number"
            imei = mongocdat.cdrdata.distinct('imei',{'source_number':self.source_number})
        if self.ft == "towercdr":
            number = "$source_number"
            imei = mongocdat.towercdrdata.distinct('imei',{'source_number':self.source_number})
        if self.ft == "ipdr":
            number = "$msisdn"
            imei = mongocdat.ipdrdata.distinct('imei',{'msisdn':self.source_number})
        print(imei,"----------------distinct---------")
        pipeline = [
            {
                '$match':{
                    'imei':{ '$in' : imei,'$nin':['null', None, ''] },
                    'msisdn':{'$regex' : '^(91\\d{10}|\\d{10})$'}
                }
            },
            {
                "$group": {
                    "_id": "$imei",
                    "source_numbers": {"$addToSet": number},
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
                }
            }
        ]
        if self.ft == "cdr":
            print("cdr")
            result = list(mongocdat.cdrdata.aggregate(pipeline))
        if self.ft == "towercdr":
            result = list(mongocdat.towercdrdata.aggregate(pipeline))
        if self.ft == "ipdr":
            result = list(mongocdat.ipdrdata.aggregate(pipeline))
        print(result,"----------imei----------")
        if len(result) > 0:
            unique_id = uuid.uuid4().__str__()
            response = {'rfid':str(unique_id),'seen':'0','result':result, 'status':'success', 'message':'more number found '}
            mongocdat.notification.insert_one({'rfid':str(unique_id),'seen':'0','redflagtype':"shared_device",'data':result,'number':self.source_number,'user':self.user, 'casename':'','filetype':self.ft,'description':"Imei's which are available more than two numbers",'timestamp':datetime.now()})
        else:
            response = {'result':[],'status':'failure', 'message':'no number found'}

        return response

    # def cdat_contact(self):
    #     print("inside cdat")
    #     pipeline = [
    #             {
    #                 '$match': {
    #                     'source_number': self.source_number,
    #                     'date_format': {'$gte': self.st, '$lte': self.et},
    #                     'destination_number': {'$regex': '^(91\\d{10}|\\d{10})$'}
    #                 }
    #             },
    #             {
    #                 '$group': {
    #                     '_id':{'destination_number': '$destination_number',
    #                            'source_number':'$source_number'
    #                            },
    #                     "cdr_field": {"$push": "$$ROOT"}
                        
    #                 },
    #             },
    #             {
    #                 '$lookup': {
    #                     'from': 'cdat_cdr',
    #                     'localField': '_id.destination_number',
    #                     'foreignField': 'source_number',
    #                     'as': 'matched_cdr'
    #                 }
    #             },
    #             {
    #                 '$match': {
    #                     'matched_cdr': {'$ne': []}  
    #                 }
    #             },
    #             {
    #                 '$unwind': '$matched_cdr'
    #             },
    #             {
    #                 '$group': {
    #                     '_id':{
    #                             'bparty':'$_id.destination_number',
    #                             'source_number':'$_id.source_number'
    #                            },
    #                     "call_in": {
    #                                 "$sum": {
    #                                     "$cond": [{"$eq": ["$matched_cdr.incoming", 1]}, 1, 0]
    #                                     }
    #                                 },
    #                     "call_out": {
    #                                 "$sum": {
    #                                     "$cond": [{"$eq": ["$matched_cdr.incoming", 0]}, 1, 0]
    #                                 }
    #                             },
    #                     "first_call": {"$min": "$matched_cdr.date_format"},
    #                     "last_call": {"$max": "$matched_cdr.date_format"},
    #                     "duration": {"$sum": "$matched_cdr.duration"},
    #                     "total_calls": {"$sum": 1}
    #                     }
    #             },
    #             {
    #                 "$addFields": {
    #                     "first_call": {
    #                         "$dateToString": {
    #                             "format": "%Y-%m-%d %H:%M:%S",
    #                             "date": "$first_call"
    #                         }
    #                     },
    #                     "last_call": {
    #                         "$dateToString": {
    #                             "format": "%Y-%m-%d %H:%M:%S",
    #                             "date": "$last_call"
    #                         }
    #                     }
    #                 }
    #             },
    #             {
    #                 '$project': {
    #                     '_id': 0,
    #                     'destination_number':'$_id.bparty',
    #                     "call_in": 1,
    #                     "call_out": 1,
    #                     "total_calls": 1,
    #                     "duration": 1,
    #                     "first_call": 1,
    #                     "last_call": 1
    #                     }
    #             }
    #         ]
        
    #     result = list(mongocdat.cdrdata.aggregate(pipeline))
    #     print(result,"-------bparty----")
    #     if len(result) > 0:
    #         unique_id = uuid.uuid4().__str__()
    #         print(unique_id)
    #         print(str(unique_id),"-------------------in second0000000000---------")
    #         response = {'rfid':str(unique_id),'seen':'0','result':result,'status':'success', 'message':'bparty found in db'}
    #         mongocdat.notification.insert_one({'rfid':str(unique_id),'seen':'0','redflagtype':"bparty",'data':result,'number':self.source_number,'user':self.user, 'casename':'','filetype':self.ft,'description':'Bparty Number which are available in suspect','timestamp':datetime.now()})

    #     else:
    #         response = {'result':[],'status':'failure', 'message':'no bparty found in db'}


    #     return response

    def cdat_contact(self):
        print("inside cdat")
        pipeline = [
                {
                    '$match': {
                        'source_number': self.source_number,
                        'date_format': {'$gte': self.st, '$lte': self.et},
                        'destination_number': {'$regex': '^(91\\d{10}|\\d{10})$'}
                    }
                },
                {
                    '$group': {
                        '_id':'$destination_number'
                                                      
                    }
                },
                {
                    '$lookup': {
                        'from': 'cdat_cdr',
                        'localField': '_id',
                        'foreignField': 'source_number',
                        'as': 'matched_cdr'
                    }
                },
                {
                    '$match': {
                        'matched_cdr': {'$ne': []}  
                    }
                },
                {
                    '$group': {
                        '_id': 0,
                        'matched_destination_numbers': {'$addToSet': '$_id'},
                    }
                }
            ]
        data = list(mongocdat.cdrdata.aggregate(pipeline))
        bparty = data[0]['matched_destination_numbers']
        matched_bparty = [
            {
                '$match':{'source_number':self.source_number,
                          'destination_number':{'$in':bparty}
                          }
            },
            {
                '$group': {
                    '_id':{
                            'bparty':'$destination_number',
                            'source_number':'$source_number'
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
                '$project': {
                    '_id': 0,
                    'destination_number':'$_id.bparty',
                    "call_in": 1,
                    "call_out": 1,
                    "total_calls": 1,
                    "duration": 1,
                    "first_call": 1,
                    "last_call": 1
                    }
            }
        ]
        result = list(mongocdat.cdrdata.aggregate(matched_bparty))


        if len(result) > 0:
            unique_id = uuid.uuid4().__str__()
            print(unique_id)
            print(str(unique_id),"-------------------in second0000000000---------")
            response = {'rfid':str(unique_id),'seen':'0','result':result,'status':'success', 'message':'bparty found in db'}
            mongocdat.notification.insert_one({'rfid':str(unique_id),'seen':'0','redflagtype':"bparty",'data':result,'number':self.source_number,'user':self.user, 'casename':'','filetype':self.ft,'description':'Bparty Number which are available in suspect','timestamp':datetime.now()})

        else:
            response = {'result':[],'status':'failure', 'message':'no bparty found in db'}


        return response


    def only_incoming(self):
        if self.ft == "cdr":
            print("cdr")
            type = mongocdat.cdrdata.distinct('call_type')

        if self.ft == "towercdr":
            type = mongocdat.towercdrdata.distinct('call_type')
        if len(type) == 1 and "call_in" in type:
            pipeline = [
                            {
                                '$match': {
                                    'source_number': self.source_number,
                                    'destination_number': {
                                        '$regex': '^(91\\d{10}|\\d{10})$'
                                    },
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


            if self.ft == "cdr":
                print("cdr")
                result = list(mongocdat.cdrdata.aggregate(pipeline))
            if self.ft == "towercdr":
                result = list(mongocdat.towercdrdata.aggregate(pipeline))
            if len(result) > 0:
                unique_id = uuid.uuid4().__str__()
                response = {'result':result,'status':'success', 'message':'only incoming call'}
                mongocdat.notification.insert_one({'rfid':str(unique_id),'seen':'0','redflagtype':"incoming",'data':result,'number':self.source_number,'user':self.user, 'casename':'','filetype':self.ft,'description':'Number which is only used to attend incoming call','timestamp':datetime.now()})
        else:
            response = {'result':[],'status':'failure', 'message':'no data found'}
        return response
    
    def only_outgoing(self):
        if self.ft == "cdr":
            print("cdr")
            type = mongocdat.cdrdata.distinct('call_type')

        if self.ft == "towercdr":
            type = mongocdat.towercdrdata.distinct('call_type')
        if len(type) == 1 and "call_out" in type:
            pipeline = [
                            {
                                '$match': {
                                    'source_number': self.source_number,
                                    'destination_number': {
                                        '$regex': '^(91\\d{10}|\\d{10})$'
                                    },
                                    
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
            if self.ft == "cdr":
                print("cdr")
                result = list(mongocdat.cdrdata.aggregate(pipeline))
            if self.ft == "towercdr":
                result = list(mongocdat.towercdrdata.aggregate(pipeline))
            if len(result) > 0:
                response = {'result':result,'status':'success', 'message':'only outgoing call'}
                unique_id = uuid.uuid4().__str__()
                mongocdat.notification.insert_one({'rfid':str(unique_id),'seen':'0','redflagtype':"outgoing",'data':result,'number':self.source_number,'user':self.user, 'casename':'','filetype':self.ft,'description':'Number which is only used to call other person','timestamp':datetime.now()})
        else:
            response = {'result':[],'status':'failure', 'message':'no data found'}
        return response

    def only_sms(self):
        if self.ft == "cdr":
            print("cdr")
            type = mongocdat.cdrdata.distinct('call_type')

        if self.ft == "towercdr":
            type = mongocdat.towercdrdata.distinct('call_type')
        if (len(type) == 2 or len(type) == 1) and ("sms_in" in type or "sms_out" in type) and ('call_in' not in type and 'call_out' not in type):
                pipeline = [
                                {
                                    '$match': {
                                        'source_number': self.source_number,
                                        'destination_number': {
                                            '$regex': '^(91\\d{10}|\\d{10})$'
                                        }
                                    }
                                },
                                {
                                    "$group": {
                                        "_id": "$destination_number",
                                        "count": { "$sum": 1 }  
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
                if self.ft == "cdr":
                    print("cdr")
                    result = list(mongocdat.cdrdata.aggregate(pipeline))
                if self.ft == "towercdr":
                    result = list(mongocdat.towercdrdata.aggregate(pipeline))
                if len(result) > 0:
                    response = {'result':result,'status':'success', 'message':'only sms'}
                    unique_id = uuid.uuid4().__str__()
                    mongocdat.notification.insert_one({'rfid':str(unique_id),'seen':'0','redflagtype':"only_sms",'data':result,'number':self.source_number,'user':self.user, 'casename':'','filetype':self.ft,'description':'Number which is only used to sms not for call','timestamp':datetime.now()})
        else:
            response = {'result':[],'status':'failure', 'message':'no data found'}
        return response
        
    def vpn_usage(self):
        pipeline = [
            {
                "$match":{
                    "msisdn":self.source_number,
                    # 'time': {'$gte': self.st, '$lte': self.et},
                    "is_vpn":1
                }
            },
            {
                '$group':{
                    '_id':{
                        'vpn':'$service',
                        'destination_ip':'$destination_ip'
                    },
                    'downlink_vol': {'$sum':{'$toInt': '$downlink_vol'}},
                    'uplink_vol': {'$sum': {'$toInt': '$uplink_vol'}},
                    'count':{"$sum":1}
                }
            },
            {
                '$group':{
                    '_id':0,
                    '_id':{
                            'vpn':'$_id.vpn'
                          },
                    'downlink_vol': {'$sum': '$downlink_vol'},
                    'uplink_vol': {'$sum': '$uplink_vol'},
                    "count_of_unique_destination_ips_of_vpn": {"$sum": 1},
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
            },
            {
                '$project': {
                    '_id':0,
                    '_id':'$_id.vpn',
                    'downlink_vol':1,
                    'uplink_vol':1,
                    'count_of_unique_destination_ips_of_vpn':1,
                    'total_destination_ips_count_of_vpn':1
                }
            }
            ]
        result = list(mongocdat.ipdrdata.aggregate(pipeline))
        print('vpn')
        vpn_result = []
        for doc in result:
            dwnLink = int(
                doc['downlink_vol']) if doc['downlink_vol'] != "None" and doc['downlink_vol'] != "" else 0
            upLink = int(
                doc['uplink_vol']) if doc['uplink_vol'] != "None" and doc['uplink_vol'] != "" else 0
            downlink_vol = self.convert_size(dwnLink)
            uplink_vol = self.convert_size(upLink)
            vpn_result.append(
                {'vpn':doc['_id'],
                 'downlink_vol':downlink_vol,
                 'uplink_vol':uplink_vol,
                 'count_of_unique_destination_ips_of_vpn':doc['count_of_unique_destination_ips_of_vpn'],
                 'total_destination_ips_count_of_vpn':doc['total_destination_ips_count_of_vpn']}
            )
            

        # pprint(result)
        if len(result) > 0:
            response = {'result':vpn_result,'status':'success', 'message':'found vpn usage'}
            unique_id = uuid.uuid4().__str__()
            mongocdat.notification.insert_one({'rfid':str(unique_id),'seen':'0','redflagtype':"vpn",'data':vpn_result,'number':self.source_number,'user':self.user, 'casename':'','filetype':self.ft,'description':'vpn ip detected from this number ipdr record','timestamp':datetime.now()})

        else:
            response = {'result':[],'status':'failure', 'message':'no vpn usage'}
        return response

      
    def foreign_isp(self):
        pipeline = [
            {
                '$match':{
                    'msisdn': self.source_number,
                    #'time': {'$gte': self.st, '$lte': self.et},
                    'com_type': 'isp',
                    'country': {'$ne': 'India'}
                }
            },
            {
                '$group':{
                    '_id':{
                        'country':'$country',
                        'destination_ip':'$destination_ip',
                        'vendor':'$asn'
                    },
                    'downlink_vol':{'$sum':{'$toInt': '$downlink_vol'}},
                    'uplink_vol': {'$sum': {'$toInt': '$uplink_vol'}},
                    'count':{'$sum':1}

                    
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'ip': '$_id.destination_ip',
                    'vendor': '$_id.vendor',
                    'country': '$_id.country',
                    'downlink_vol': 1,
                    'uplink_vol': 1,
                    'count':1
                }
            } 
        ]
        result = list(mongocdat.ipdrdata.aggregate(pipeline))
        print("-----foreign isp --------------")
        # pprint(result)
        isp_result = []
        for doc in result:
            dwnLink = int(
                doc['downlink_vol']) if doc['downlink_vol'] != "None" and doc['downlink_vol'] != "" else 0
            upLink = int(
                doc['uplink_vol']) if doc['uplink_vol'] != "None" and doc['uplink_vol'] != "" else 0
            downlink_vol = self.convert_size(dwnLink)
            uplink_vol = self.convert_size(upLink)
            isp_result.append({
                'ip':doc['ip'],
                'vendor':doc['vendor'],
                'country':doc['country'],
                'count':1,
                'downlink_vol':downlink_vol,
                'uplink_vol':uplink_vol
            })

        if len(isp_result) > 0:
            response = {'result':isp_result,'status':'success', 'message':'found vpn usage'}
            unique_id = uuid.uuid4().__str__()
            mongocdat.notification.insert_one({'rfid': str(unique_id) ,'redflagtype':"foreign_isp",'data':isp_result,'number':self.source_number,'user':self.user,'seen':'0', 'casename':'','filetype':self.ft,'description':'foreign ip detected from this number ipdr record','timestamp':datetime.now()})
        else:
            response = {'result':[],'status':'failure', 'message':'no found foreign isp usage'}
        return response


    def zero_activity_day(self):
        if self.ft == "cdr" or  self.ft == "towercdr":
            number = "source_number"
        if self.ft == "ipdr":
            number = "msisdn"
        pipeline = [
            {
                "$match": {number:self.source_number,
                           'date_format': {'$gte': self.st, '$lte': self.et},}
            },
            {
                "$group": {
                    "_id": {
                        "source_number": "$source_number",
                    },
                    "dates": {"$addToSet": "$date"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "source_number": "$_id.source_number",
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
                    "startdate": {"$dateToString": {"format": "%Y-%m-%d", "date": "$startdate"}},
                    "enddate": {"$dateToString": {"format": "%Y-%m-%d", "date": "$enddate"}},
                    "allDates": 1,
                }
            }
        ]
        if self.ft == "cdr":
            result = list(mongocdat.cdrdata.aggregate(pipeline))
        if self.ft == "towercdr":
            result = list(mongocdat.towercdrdata.aggregate(pipeline))
        if self.ft == "ipdr":
            result = list(mongocdat.ipdrdata.aggregate(pipeline))
        period_list = []
        for item in result:
            source_number = item['source_number'] 
            start_date = item['startdate']
            end_date = item['enddate']
            active_dates = item['allDates']
            
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
            if len(inactive_dates) > 0:
                cdr = {
                    'source_number':source_number,
                    'start_date':start_date,
                    'end_date':end_date,
                    'inactive_dates':inactive_dates
                }
                period_list.append(cdr)
            if len(result) > 0:
                unique_id = uuid.uuid4().__str__()
                response = {'rfid': str(unique_id),'seen':'0','result':period_list, 'status':'success', 'message':'more device found'}
                mongocdat.notification.insert_one({'rfid':str(unique_id),'seen':'0','redflagtype':"silent_days",'data':period_list,'number':self.source_number,'user':self.user, 'casename':'','filetype':self.ft,'description':'These days are may be switch off or not reachable.','timestamp':datetime.now()})
            else:
                response = {'result':[],'status':'failure', 'message':'no anomaly device found'}

            return response


def getnotify(user):
    sort_keys = [('timestamp', pymongo.DESCENDING), ('seen', pymongo.ASCENDING)]
    return list(mongocdat.notification.find({'user':user},{'_id':0}).sort(sort_keys))
    
def updateseenrfi(rfid,user):
    print("-----------------inside updateseenrfi---------------")
    print(rfid,user)

    mongocdat.notification.update_one({"rfid":rfid,'user':user},{"$set":{'seen':"1"}})
    print("-------------after--------------")
    return getnotify(user)
