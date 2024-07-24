from datetime import datetime
from pymongo import MongoClient
from pprint import pprint
import math
from MongoClinet import CDAT 
mongocdat = CDAT()




# Replace the following with your MongoDB connection details
class Graph_View():
    def __init__(self):
        self.collection_ipdr = mongocdat.ipdr
    
    def convert_size(size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])   
        
    def get_summary(self,data):
        summary = {}        
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
                "vpn": "$privacy_service",
                "msisdn": 1,
                "vpn_ip": "$destination_ip",
                "downlink_vol": 1,
                "uplink_vol": 1,
                "start_time": "$time_st",
                "end_time": "$time_et"
                }
            }
        ]
        query =self.collection_ipdr.aggregate(allvpn_pipeline)
        results = list(query)
        allvpn = []
        for doc in results:
            dwnLink = int(doc['downlink_vol']) if doc['downlink_vol'] != "None" and doc['downlink_vol'] != "" else 0
            upLink = int(doc['uplink_vol']) if doc['uplink_vol'] != "None" and doc['uplink_vol'] != "" else 0
            downlink_vol = self.convert_size(dwnLink)
            uplink_vol = self.convert_size(upLink)
            
            allvpn.append({
                "MSISDN": doc['msisdn'],
                "VPN": doc['vpn'],
                "VPN_IP": doc['vpn_ip'],
                "downlink_vol": downlink_vol,
                "uplink_vol": uplink_vol,
                "start_time": doc['start_time'],
                "end_time": doc['end_time']
            })
        
        
        vpn_pipeline = [
            {
                    "$match": {
                    "is_vpn": 1,
                    "msisdn": data,
                    "destination_ip": { "$ne": None, 
                                    "$ne":"" }
                    }
                },
                {
                    "$group": {
                    "_id": {
                        "vpn": "$privacy_service",
                        "msisdn": "$msisdn",
                        "destination_ip": "$destination_ip"
                    },
                    "count": { "$sum": 1 }
                    }
                },
                {
                    "$group": {
                    "_id": {
                        "vpn_name": "$_id.vpn",
                        "vpn_msisdn": "$_id.msisdn"
                    },
                    "count_of _unique_destination_ips_of_vpn": { "$sum": 1 },
                    "destination_ips_of_vpn": {
                        "$push": {
                        "ip": "$_id.destination_ip",
                        "count": "$count"
                        }
                    },
                    "total_destination_ips_count_of_vpn": { "$sum": "$count" },
                    }
                },
                {
                    "$sort": { "total_destination_ips_count_of_vpn": -1 }
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
        
        
            
        country_pipeline = [
            {
                    "$match": {
                    "country": { "$ne": None},
                    "msisdn": data,
                    "destination_ip": { 
                        "$ne": None, 
                        "$ne":"" 
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
                    "count": { "$sum": 1 }
                    }
                },
                {
                    "$group": {
                    "_id": {
                        "country": "$_id.country",
                        "country_msisdn": "$_id.msisdn"
                    },
                    "count_of_unique_destination_ips_of_country": { "$sum": 1 },
                    "destination_ips_of_country": {
                        "$push": {
                        "ip": "$_id.destination_ip",
                        "count": "$count"
                        }
                    },
                    "total_destination_ips_count_of_country": { "$sum": "$count" },
                    
                    }
                },
                {
                    "$sort": { "total_destination_ips_count_of_country": -1 }
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
                    "company": { "$ne": None},
                    "msisdn": data,
                    "destination_ip": { 
                        "$ne": None, 
                        "$ne":""
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
                    "count": { "$sum": 1 }
                    }
                },
                {
                    "$group": {
                    "_id": {
                        "app": "$_id.company",
                        "app_msisdn": "$_id.msisdn"
                    },
                    "count_of_unique_destination_ips_of_app": { "$sum": 1 },
                    "destination_ips_of_app": {
                        "$push": {
                        "ip": "$_id.destination_ip",
                        "count": "$count"
                        }
                    },
                    "total_destination_ips_count_of_app": { "$sum": "$count" },
                    }
                    },
                    {
                    "$sort": { "total_destination_ips_count_of_app": -1 }
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
                    "min_date": {"$min": "$time_st"},
                    "max_date": {"$max": "$time_et"}
                }
            }
        ]
        query = self.collection_ipdr.aggregate(device_pipeline)
        device_results = list(query)
        
        
        isp_pipeline = [
                {
                '$match': {
                    'msisdn': data,
                    'ip_type': 'isp',
                    'country': 'India'
                }
            },
            {
                '$group': {
                    '_id': '$destination_ip',
                    'vendor': {'$first': '$asn'}
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'ip': '$_id',
                    'vendor': 1
                }
            }
            ]

        query5 = self.collection_ipdr.aggregate(isp_pipeline)
        result5 = list(query5)
        
        isp_india = []
        for doc in result5:
            isp_india.append({
                "ip": doc['ip'],
                "vendor": doc['vendor']
            })

        foreign_isp_pipeline = [
            {
                '$match': {
                    'msisdn': data,
                    'ip_type': 'isp',
                    'country': {'$ne': 'India'}
                }
            },
            {
                '$group': {
                    '_id': '$destination_ip',
                    'vendor': {'$first': '$asn'}
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'ip': '$_id',
                    'vendor': 1
                }
            }
        ]

        query6 = self.collection_ipdr.aggregate(foreign_isp_pipeline)
        result6 = list(query6)
        
        foreign_isp = []
        for doc in result6:
            foreign_isp.append({
                "ip": doc['ip'],
                "vendor": doc['vendor']
            })
        
        
        iptype_pipeline = [
            {
                    "$match": {
                    "ip_type": { "$ne": None},
                    "msisdn": data,
                    "destination_ip": { 
                        "$ne": None, 
                        "$ne":"" 
                    }
                    }
                },
                {
                    "$group": {
                    "_id": {
                        "ip_type": "$ip_type",
                        "msisdn": "$msisdn",
                        "destination_ip": "$destination_ip"
                    },
                    "count": { "$sum": 1 }
                    }
                },
                {
                    "$group": {
                    "_id": {
                        "ip_type": "$_id.ip_type",
                        "iptype_msisdn": "$_id.msisdn"
                    },
                    "count_of_unique_destination_ips_of_iptype": { "$sum": 1 },
                    "destination_ips_of_iptype": {
                        "$push": {
                        "ip": "$_id.destination_ip",
                        "count": "$count"
                        }
                    },
                    "total_destination_ips_count_of_iptype": { "$sum": "$count" },
                    
                    }
                },
                {
                    "$sort": { "total_destination_ips_count_of_iptype": -1 }
                    }
        ]
        
        query4 = self.collection_ipdr.aggregate(iptype_pipeline)
        results4 = list(query4)
        
        iptype = []
        for doc in results4:
            iptype.append({
            "MSISDN_IPTYPE": doc['_id']['iptype_msisdn'], 
            "IPTYPE" : doc['_id']['ip_type'],
            "count_of_unique_destination_ips_of_iptype": doc['count_of_unique_destination_ips_of_iptype'],
            "destination_ips_of_iptype": doc['destination_ips_of_iptype'],
            "total_destination_ips_count_of_iptype": doc['total_destination_ips_count_of_iptype'],
            })
        print(iptype[:1])  
        
        
        
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

            total_unique_country_count = len(set(v['COUNTRY'] for v in country))
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


            summary= {'data':data,
                     'allvpn':allvpn,
                     'isp_india':isp_india,
                     'foreign_isp':foreign_isp,
                     'vpn':vpn,
                     'country':country,
                     'app':app,
                     'iptype':iptype,
                     'device':device_results,
                     'summary_app':summary_app,
                     'summary_country':summary_country,
                     'summary_vpn':summary_vpn, 
                     'summary_iptype':summary_iptype}
            return summary

