from datetime import datetime,date, timedelta
from pymongo import MongoClient
import calendar
from pprint import pprint
from MongoClinet import CDAT
mongocdat = CDAT()



# Replace the following with your MongoDB connection details
class Graph_View():
    def __init__(self):
        self.collection_ipdr = mongocdat.ipdr
        self.collection_cdr = mongocdat.cdrdata


    def get_data(self, msisdn, fromdate=None, todate=None):
        print(msisdn)
        pipeline = []  # Initialize the pipeline list here

        if fromdate is None and todate is None:
            current_date = datetime.now()
            first_day_of_month = current_date.replace(day=1)
            last_day_of_month = current_date.replace(day=1, month=current_date.month + 1) - timedelta(days=1)           
            print(first_day_of_month, last_day_of_month)
            fromdate_def = first_day_of_month  # Format as date only
            todate_def = last_day_of_month   # Format as date only

            pipeline.append({
                '$match': {
                    'msisdn': msisdn,
                    'time': {
                        '$gte': fromdate_def,
                        '$lte': todate_def + timedelta(days=1) - timedelta(seconds=1)
                    }
                }
            })

            pipeline.append({
                '$project': {
                    'destination_ip': 1,
                    'time': 1,
                }
            })

        if fromdate and todate:
            fromdate_def = datetime.strptime(fromdate, "%Y-%m-%d")
            todate_def = datetime.strptime(todate, "%Y-%m-%d")

            pipeline.append({
                '$match': {
                    'msisdn': msisdn,
                    'time': {
                        '$gte': fromdate_def,
                        '$lte': todate_def + timedelta(days=1) - timedelta(seconds=1)
                    }
                }
            })

            # Group by destination_ip and month
            pipeline.append({
                '$group': {
                    '_id': {
                        'destination_ip': '$destination_ip',
                    },
                    'count': {'$sum': 1},
                }
            })
        else:
            # No date filter, group by destination_ip only
            pipeline.append({
                '$group': {
                    '_id': {
                        'destination_ip': '$destination_ip',
                    },
                    'count': {'$sum': 1},
                }
            })

            pipeline.append({
                '$project': {
                    '_id': 0,
                    'destination_ip': '$_id.destination_ip',
                    'count': 1,
                }
            })

        # print(pipeline, "------------pipeline-------------")
        data = list(self.collection_ipdr.aggregate(pipeline))
        return data


    def get_data_usage(self, msisdn, fromdate=None, todate=None):
        print("+++++++++++++++++++++++++++++")
        pipeline = []
        print(msisdn,fromdate,todate)
        # MongoDB aggregation pipeline to get data usage with uplink_vol and downlink_vol
        if fromdate is None and todate is None:
            current_date = datetime.now()
            first_day_of_month = current_date.replace(day=1)
            last_day_of_month = current_date.replace(day=1, month=current_date.month + 1) - timedelta(days=1)           
            print(first_day_of_month, last_day_of_month)
            fromdate_def = first_day_of_month  # Format as date only
            todate_def = last_day_of_month
            pipeline = [
                {
                    '$match': {
                        'msisdn': msisdn,
                        'time': {
                        '$gte': fromdate_def,
                        '$lte': todate_def + timedelta(days=1) - timedelta(seconds=1)
                    }
                    }
                }
            ]

        if fromdate is not None and todate is not None:
            fromdate_def = datetime.strptime(fromdate, "%Y-%m-%d")
            todate_def = datetime.strptime(todate, "%Y-%m-%d")

            pipeline.append({
                '$match': {
                    'msisdn': msisdn,
                    'time': {
                        '$gte': fromdate_def,
                        '$lte': todate_def + timedelta(days=1) - timedelta(seconds=1)
                    }
                }
            })

        pipeline.extend([
            {
                '$group': {
                    '_id': {
                        'destination_ip': '$destination_ip',
                        'date': { '$dateToString': { 'format': '%Y-%m-%d', 'date': '$time' } }
                    },
                    'uplink_usage': { '$sum': { '$toInt': '$uplink_vol' } },
                    'downlink_usage': { '$sum': { '$toInt': '$downlink_vol' } },
                    'count': { '$sum': 1 },
                    'start_time': { '$min': '$time' },
                    'end_time': { '$max': '$time_et' }
                }
            },
            {
                '$group': {
                    '_id': '$_id.destination_ip',
                    'usage_data': {
                        '$push': {
                            'date': '$_id.date',
                            'uplink_usage': '$uplink_usage',
                            'downlink_usage': '$downlink_usage',
                            'count': '$count',
                        }
                    }
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'destination_ip': '$_id',
                    'usage_data': 1
                }
            }
        ])

        # Execute the aggregation pipeline
        print(pipeline)
        data_usage = list(self.collection_ipdr.aggregate(pipeline))
        print(data_usage)
        return data_usage



    def get_cellid_filter(self, msisdn, fromdate=None, todate=None):
        pipeline = []

        if fromdate is None and todate is None:
            current_date = datetime.now()
            first_day_of_month = current_date.replace(day=1)
            last_day_of_month = current_date.replace(day=1, month=current_date.month + 1) - timedelta(days=1)
            print(first_day_of_month, last_day_of_month)
            fromdate_def = first_day_of_month
            todate_def = last_day_of_month
            pipeline.append({
                '$match': {
                    'msisdn': msisdn,
                    'time': {
                        '$gte': fromdate_def,
                        '$lte': todate_def + timedelta(days=1) - timedelta(seconds=1)
                    }
                }
            })
            pipeline.append({
                '$project': {
                    'cell_id': 1,
                }
            })

        if fromdate is not None and todate is not None:
            fromdate_def = datetime.strptime(fromdate, "%Y-%m-%d")
            todate_def = datetime.strptime(todate, "%Y-%m-%d")
            pipeline.append({
                '$match': {
                    'msisdn': msisdn,
                    'time': {
                        '$gte': fromdate_def,
                        '$lte': todate_def + timedelta(days=1) - timedelta(seconds=1)
                    }
                }
            })
            pipeline.append({
                '$project': {
                    'cell_id': 1,
                }
            })

        pipeline.append({
            '$group': {
                '_id': {
                    'cell_id': '$cell_id',
                },
                'count': {'$sum': 1},
            }
        })

        pipeline.append({
            '$project': {
                '_id': 0,
                'cell_id': '$_id.cell_id',
                'count': 1,
            }
        })

        data = list(self.collection_ipdr.aggregate(pipeline))
        return data
    
        
    def get_imei_filter(self, msisdn, fromdate=None, todate=None):
        pipeline = []

        if fromdate is None and todate is None:
            current_date = datetime.now()
            first_day_of_month = current_date.replace(day=1)
            last_day_of_month = current_date.replace(day=1, month=current_date.month + 1) - timedelta(days=1)
            print(first_day_of_month, last_day_of_month)
            fromdate_def = first_day_of_month
            todate_def = last_day_of_month
            pipeline.append({
                '$match': {
                    'msisdn': msisdn,
                    'time': {
                        '$gte': fromdate_def,
                        '$lte': todate_def + timedelta(days=1) - timedelta(seconds=1)
                    }
                }
            })
            pipeline.append({
                '$project': {
                    'imei': 1,
                }
            })

        if fromdate is not None and todate is not None:
            fromdate_def = datetime.strptime(fromdate, "%Y-%m-%d")
            todate_def = datetime.strptime(todate, "%Y-%m-%d")
            pipeline.append({
                '$match': {
                    'msisdn': msisdn,
                    'time': {
                        '$gte': fromdate_def,
                        '$lte': todate_def + timedelta(days=1) - timedelta(seconds=1)
                    }
                }
            })
            pipeline.append({
                '$project': {
                    'imei': 1,
                }
            })

        pipeline.append({
            '$group': {
                '_id': {
                    'imei': '$imei',
                },
                'count': {'$sum': 1},
            }
        })

        pipeline.append({
            '$project': {
                '_id': 0,
                'imei': '$_id.imei',
                'count': 1,
            }
        })

        data = list(self.collection_ipdr.aggregate(pipeline))
        return data
    
    def get_daywise_usage(self, msisdn, fromdate=None, todate=None):
        # MongoDB aggregation pipeline to get day-wise data usage with uplink_vol and downlink_vol
        pipeline = []
        if fromdate is None and todate is None:
            current_date = datetime.now()
            first_day_of_month = current_date.replace(day=1)
            last_day_of_month = current_date.replace(day=1, month=current_date.month + 1) - timedelta(days=1)           
            print(first_day_of_month, last_day_of_month)
            fromdate_def = first_day_of_month  # Format as date only
            todate_def = last_day_of_month
            
            pipeline = [
                {
                    '$match': {
                        'msisdn': msisdn,
                        'time': {
                            '$gte': fromdate_def,
                            '$lte': todate_def + timedelta(days=1) - timedelta(seconds=1)
                        },
                        '$expr': {
                            '$and': [
                                {'$gte': [{'$hour': '$time'}, 6]},
                                {'$lt': [{'$hour': '$time'}, 18]}
                            ]
                        }
                    }
                }
            ]

       
        if fromdate is not None and todate is not None:
            fromdate_def = datetime.strptime(fromdate, "%Y-%m-%d")
            todate_def = datetime.strptime(todate, "%Y-%m-%d")
            
            pipeline = [
                {
                    '$match': {
                        'msisdn': msisdn,
                        'time': {
                            '$gte': fromdate_def,
                            '$lte': todate_def + timedelta(days=1) - timedelta(seconds=1)
                        },
                        '$expr': {
                            '$and': [
                                {'$gte': [{'$hour': '$time'}, 6]},
                                {'$lt': [{'$hour': '$time'}, 18]}
                            ]
                        }
                    }
                }
            ]


        pipeline.extend([
            {
                '$group': {
                    '_id': {
                        'destination_ip': '$destination_ip',
                        'date': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$time'}}
                    },
                    'uplink_usage': {'$sum': {'$toInt': '$uplink_vol'}},
                    'downlink_usage': {'$sum': {'$toInt': '$downlink_vol'}},
                    'count': {'$sum': 1},
                    'day_count': {'$sum': 1},
                    'night_count': {'$sum': 0},
                    'start_time': {'$min': '$time'},
                    'end_time': {'$max': '$time_et'}
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'destination_ip': '$_id.destination_ip',
                    'date': '$_id.date',
                    'uplink_usage': 1,
                    'downlink_usage': 1,
                    'total_usage': {'$add': ['$uplink_usage', '$downlink_usage']},
                    'day_count': 1,
                    'night_count': 1,
                    'duration': {'$subtract': ['$end_time', '$start_time']}
                }
            }
        ])

        # Execute the aggregation pipeline
        daywise_data_usage = list(self.collection_ipdr.aggregate(pipeline))
        return daywise_data_usage

    def get_company(self, msisdn, fromdate=None, todate=None):
        print(msisdn,fromdate,todate,"-----")
        pipeline = []  # Initialize the pipeline list here

        if fromdate is None and todate is None:
            current_date = datetime.now()
            first_day_of_month = current_date.replace(day=1)
            last_day_of_month = current_date.replace(day=1, month=current_date.month + 1) - timedelta(days=1)           
            print(first_day_of_month, last_day_of_month)
            fromdate_def = first_day_of_month  # Format as date only
            todate_def = last_day_of_month   # Format as date only

            pipeline.append({
                '$match': {
                    'msisdn': msisdn,
                    'time': {
                        '$gte': fromdate_def,
                        '$lte': todate_def + timedelta(days=1) - timedelta(seconds=1)
                    }
                }
            })

            pipeline.append({
                '$project': {
                    'company': 1,
                    'time': 1,
                }
            })

        if fromdate and todate:
            fromdate_def = datetime.strptime(fromdate, "%Y-%m-%d")
            todate_def = datetime.strptime(todate, "%Y-%m-%d")

            pipeline.append({
                '$match': {
                    'msisdn': msisdn,
                    'time': {
                        '$gte': fromdate_def,
                        '$lte': todate_def + timedelta(days=1) - timedelta(seconds=1)
                    }
                }
            })

            # Group by company and month
            pipeline.append({
                '$group': {
                    '_id': {
                        'company': '$company',
                    },
                    'count': {'$sum': 1},
                }
            })
        else:
            # No date filter, group by company only
            pipeline.append({
                '$group': {
                    '_id': {
                        'company': '$company',
                    },
                    'count': {'$sum': 1},
                }
            })

            pipeline.append({
                '$project': {
                    '_id': 0,
                    'company': '$_id.company',
                    'count': 1,
                }
            })

        # print(pipeline, "------------pipeline-------------")
        data = list(self.collection_ipdr.aggregate(pipeline))
        # pprint(data)
        return data

    def get_nightwise_usage(self,msisdn,fromdate=None,todate=None):
        # print(msisdn,month,year,"night")
        # MongoDB aggregation pipeline to get day-wise data usage with uplink_vol and downlink_vol
        pipeline = []
        if fromdate is None and todate is None:
            current_date = datetime.now()
            first_day_of_month = current_date.replace(day=1)
            last_day_of_month = current_date.replace(day=1, month=current_date.month + 1) - timedelta(days=1)           
            print(first_day_of_month, last_day_of_month)
            fromdate_def = first_day_of_month  # Format as date only
            todate_def = last_day_of_month
            pipeline = [
            {
                '$match': {
                    'msisdn': msisdn,
                    'time': {
                                '$gte': fromdate_def,
                                '$lte': todate_def + timedelta(days=1) - timedelta(seconds=1)
                            },
                    '$expr': {
                        '$or': [
                            # Night hours from 6 PM to 11:59:59 PM
                            {'$and': [{'$gte': [{'$hour': '$time'}, 18]}, {'$lte': [{'$hour': '$time'}, 23]}]},
                            # Night hours from 12 AM to 6 AM
                            {'$and': [{'$gte': [{'$hour': '$time'}, 0]}, {'$lt': [{'$hour': '$time'}, 6]}]}
                        ]
                    }
                }
            }
            ]
        if fromdate is not None and todate is not None:
            fromdate_def = datetime.strptime(fromdate, "%Y-%m-%d")
            todate_def = datetime.strptime(todate, "%Y-%m-%d")
            pipeline = [
            {
                '$match': {
                    'msisdn': msisdn,
                    'time': {
                                '$gte': fromdate_def,
                                '$lte': todate_def + timedelta(days=1) - timedelta(seconds=1)
                            },
                    '$expr': {
                        '$or': [
                            # Night hours from 6 PM to 11:59:59 PM
                            {'$and': [{'$gte': [{'$hour': '$time'}, 18]}, {'$lte': [{'$hour': '$time'}, 23]}]},
                            # Night hours from 12 AM to 6 AM
                            {'$and': [{'$gte': [{'$hour': '$time'}, 0]}, {'$lt': [{'$hour': '$time'}, 6]}]}
                        ]
                    }
                }
            }
            ]
            
        pipeline.extend([
            {
                '$group': {
                    '_id': {
                        'destination_ip': '$destination_ip',
                        'date': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$time'}}
                    },
                    'uplink_usage': {'$sum': {'$toInt': '$uplink_vol'}},
                    'downlink_usage': {'$sum': {'$toInt': '$downlink_vol'}},
                    'count': {'$sum': 1},
                    'day_count': {'$sum': 0},
                    'night_count': {'$sum': 1},
                    'start_time': {'$min': '$time'},
                    'end_time': {'$max': '$time_et'}
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'destination_ip': '$_id.destination_ip',
                    'date': '$_id.date',
                    'uplink_usage': 1,
                    'downlink_usage': 1,
                    'total_usage': {'$add': ['$uplink_usage', '$downlink_usage']},
                    'day_count': 1,
                    'night_count': 1,
                    'duration': {'$subtract': ['$end_time', '$start_time']}
                }
            }
        ])
        # Execute the aggregation pipeline
        nightwise_data_usage = list(self.collection_ipdr.aggregate(pipeline))
        return nightwise_data_usage
    
    
    
    def top_10_towerid(self, data,mode,fromdate=None, todate=None):
        pipeline = []
        if fromdate is not None and todate is not None:
            print("###########")
            fromdate_def = int(datetime.strptime(fromdate,"%Y-%m-%d").timestamp())
            todate_def = int(datetime.strptime(todate,"%Y-%m-%d").timestamp())

        if fromdate is None and todate is None:
            print("--------")
            current_date = datetime.now()
            first_day_of_month = current_date.replace(day=1)
            last_day_of_month = current_date
            fromdate_def = int(datetime.strptime(first_day_of_month, "%Y-%m-%d").timestamp())
            todate_def = int(datetime.strptime(last_day_of_month,"%Y-%m-%d").timestamp())
            pipeline = [
                {
                    '$match': {
                        'source_number': data,  
                        'timestamp':{'$gte':fromdate_def,'$lte':todate_def}
                    }
                },
                {
                    '$addFields': {
                        'datetime': {
                            '$toDate': '$timestamp'
                        }
                    }
                },
                {
                    '$project': {
                        'first_cgid': 1,
                    }
                }
            ]
            if mode == "daytop10cellid":
                pipeline[0]['$match']['$expr'] = {
                    '$and': [
                        {'$gte': [{'$hour': '$datetime'}, 6]},
                        {'$lt': [{'$hour': '$datetime'}, 18]}
                    ]
                }
            elif mode == "night_top10cellid":
                pipeline[0]['$match']['$expr'] = {
                    '$or': [
                        # Night hours from 6 PM to 11:59:59 PM
                        {'$and': [{'$gte': [{'$hour': '$datetime'}, 18]}, {'$lte': [{'$hour': '$datetime'}, 23]}]},
                        # Night hours from 12 AM to 6 AM
                        {'$and': [{'$gte': [{'$hour': '$datetime'}, 0]}, {'$lt': [{'$hour': '$datetime'}, 6]}]}
                    ]
                }
            pipeline.append({
                '$project': {
                    '_id': 0,
                    'cell_id': '$_id.first_cgid',
                    'count': 1
                }
            })
            pipeline.append({
                '$sort': {'count': -1} 
            })

            pipeline.append({
                '$limit': 10  
            })

            data = list(self.collection_cdr.aggregate(pipeline))
            return data



# ------------------------------------------------- CDR graph ---------------------------------------------------------------
    def top_10_location(self,data,mode,fromdate=None,todate=None):
        print(data,mode,"---------top_10_location------------")
        current_date = datetime.now()
        first_day_of_month = current_date.replace(day=1)
        last_day_of_month = current_date
        fromdate_def = first_day_of_month.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")
        todate_def = last_day_of_month.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")
        # f = "2019-06-03"
        # t = "2020-12-21"
        # print(data,t,f)
        if fromdate is not None and todate is not None:
            fromdate_def = int(datetime.strptime(fromdate,"%Y-%m-%d").timestamp())
            todate_def = int(datetime.strptime(todate,"%Y-%m-%d").timestamp())

        # if fromdate is None and todate is None:
        #     print("came")
        #     fromdate_def = int(datetime.strptime(first_day_of_month, "%Y-%m-%d").timestamp())
        #     todate_def = int(datetime.strptime(last_day_of_month,"%Y-%m-%d").timestamp())
        if fromdate is None and todate is None:
            fromdate_def = int(first_day_of_month.timestamp())
            todate_def = int(last_day_of_month.timestamp())   
        if mode == "all_data":
            pipeline = [
            {
                 "$match": {
                    "source_number": data,
                }
            },
            {
                "$group": {
                    "_id": {
                        "state": "$state",
                        "date": "$date"
                    }
                }
            },
            {
                "$group": {
                    "_id": "$_id.state",
                    "unique_dates": { "$addToSet": "$_id.date" },
                    "count": { "$sum": 1 }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "state": "$_id",
                    "count": 1
                }
            }]
        elif mode is None:
            pipeline = [
                {
                    "$match": {
                        "source_number": data,
                        "timestamp": {
                            "$gte": fromdate_def,
                            "$lte": todate_def
                        }
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "state": "$state",
                            "date": "$date"
                        }
                    }
                },
                {
                    "$group": {
                        "_id": "$_id.state",
                        "unique_dates": { "$addToSet": "$_id.date" },
                        "count": { "$sum": 1 }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "state": "$_id",
                        "count": 1
                    }
                }]
            

            # Execute the aggregation
        result = list(self.collection_cdr.aggregate(pipeline))
        return result    
    
    def cdr_data(self, number,fromdate=None,todate=None): 
        print(number,fromdate,todate,"=================number=========================")
        
        if fromdate is not None and todate is not None:
            fromdate_def = int(datetime.strptime(fromdate,"%Y-%m-%d").timestamp())
            todate_def = int(datetime.strptime(todate,"%Y-%m-%d").timestamp())

        # if fromdate is None and todate is None:
        #     fromdate_def = int(datetime.strptime(first_day_of_month, "%Y-%m-%d").timestamp())
        #     todate_def = int(datetime.strptime(last_day_of_month,"%Y-%m-%d").timestamp())
        if fromdate is None and todate is None:
            current_date = datetime.now()
            first_day_of_month = current_date.replace(day=1)
            print(type(first_day_of_month))
            last_day_of_month = current_date
            fromdate_def = int(first_day_of_month.timestamp())
            todate_def = int(last_day_of_month.timestamp())

              
        pipeline = [
            {
                '$match': {
                    'source_number': number,
                    'call_type': {'$in': ['call_in', 'call_out']},
                     'timestamp': {
                            "$gte": fromdate_def,
                            "$lte": todate_def
                        },
                }
            },
            {
                '$group': {
                    '_id': '$destination_number',
                    'call_in_count': {
                        '$sum': {
                            '$cond': [{'$eq': ['$call_type', 'call_in']}, 1, 0]
                        }
                    },
                    'call_out_count': {
                        '$sum': {
                            '$cond': [{'$eq': ['$call_type', 'call_out']}, 1, 0]
                        }
                    }
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'destination_number': '$_id',
                    'call_in_count': 1,
                    'call_out_count': 1
                }
            }
        ]
        # Execute the aggregation pipeline
        cdrcallcount = list(self.collection_cdr.aggregate(pipeline))
        # print(cdrcallcount,"***********************")
        return cdrcallcount






# if __name__ == '__main__':
#     msisdn = "7702003961"
#     fromdate='2023-02-01'
#     todate='2023-03-01'
#     # fromdate = None
#     # todate = None
#     mode="daytop10cellid"
#     # mode = None
#     # Graph_View().top_10_location(data,False,fromdate,todate)
#     # Graph_View().top_10_towerid(data,mode,fromdate,todate)
#     # Graph_View().top_10_location(data,mode,fromdate,todate)
#     Graph_View().top_10_towerid(msisdn,fromdate,todate)
#     # app.run(debug=True)

