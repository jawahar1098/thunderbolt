import pymongo
import datetime
import calendar
from datetime import datetime, time
import math
from loguru import logger
from MongoClinet import CDAT as mongocdat
from MongoClinet import CDAT
# 
mongocdat = CDAT()


logger.add("file_log.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

class Cdr_Analysis:
    def __init__(self):
        self.collection_cdrdata =  mongocdat.cdrdata
        self.collection_cellid = mongocdat.cellidchart
        self.collection_towerid = mongocdat.towercdrdata
        self.collection_sdrdata = mongocdat.sdrdata
        self.collection_ipdrvoip = mongocdat.ipdr
        self.collection_rhdata = mongocdat.rhdata
        self.collection_poadata = mongocdat.poadata
        self.collection_gprs = mongocdat.gprs
               
    def totalCalls(self, data):
        total_calls = self.collection_cdrdata.count_documents({"source_number":data, 'call_type': {'$in': ['call_in', 'call_out']}})
        print(total_calls)
        fromdate, todate = "2023-02-11" , "2023-03-01"
        get_data = self.collection_cdrdata.find({'source_number':data,'call_type': {'$in': ['call_in', 'call_out']},'timestamp': {
                '$gte': datetime.strptime(fromdate, "%Y-%m-%d").timestamp() * 1000,  
                '$lte': datetime.strptime(todate, "%Y-%m-%d").timestamp() * 1000  
            }})
        data_dict_day = {}
        data_dict_night = {}
        start_time = time(6, 0, 0)  
        end_time = time(18, 0, 0)
        start_time_night = time(18, 1, 0)
        end_time_night = time(5,59,0)
        print(start_time_night, end_time_night,"------------")
        for value in get_data:
            current_date = datetime.fromtimestamp(value['timestamp']/1000)
            given_time = current_date.time()
            day_name = calendar.day_name[current_date.weekday()]
            if day_name.lower().strip() == "monday" and start_time <= given_time <= end_time:
                data_dict_day['monday'] = data_dict_day.get('monday', 0) + 1

            if day_name.lower().strip() == "monday" and  (given_time >= start_time_night or given_time <= end_time_night):
                data_dict_night['monday'] = data_dict_night.get('monday', 0) + 1

            if day_name.lower().strip() == "tuesday" and start_time <= given_time <= end_time:
                data_dict_day['tuesday'] = data_dict_day.get('tuesday', 0) + 1

            if day_name.lower().strip() == "tuesday" and (given_time >= start_time_night or given_time <= end_time_night):
                data_dict_night['tuesday'] = data_dict_night.get('tuesday', 0) + 1

            if day_name.lower().strip() == "wednesday" and start_time <= given_time <= end_time:
                data_dict_day['wednesday'] = data_dict_day.get('wednesday', 0) + 1

            if day_name.lower().strip() == "wednesday" and  (given_time >= start_time_night or given_time <= end_time_night):
                data_dict_night['wednesday'] = data_dict_night.get('wednesday', 0) + 1

            if day_name.lower().strip() == "thursday" and start_time <= given_time <= end_time:
                data_dict_day['thursday'] = data_dict_day.get('thursday', 0) + 1

            if day_name.lower().strip() == "thursday" and  (given_time >= start_time_night or given_time <= end_time_night) :
                data_dict_night['thursday'] = data_dict_night.get('thursday', 0) + 1

            if day_name.lower().strip() == "friday" and start_time <= given_time <= end_time:
                data_dict_day['friday'] = data_dict_day.get('friday', 0) + 1

            if day_name.lower().strip() == "friday" and  (given_time >= start_time_night or given_time <= end_time_night) :
                data_dict_night['friday'] = data_dict_night.get('friday', 0) + 1

            if day_name.lower().strip() == "saturday" and start_time <= given_time <= end_time:
                data_dict_day['saturday'] = data_dict_day.get('saturday', 0) + 1

            if day_name.lower().strip() == "saturday" and (given_time >= start_time_night or given_time <= end_time_night) :
                data_dict_night['saturday'] = data_dict_night.get('saturday', 0) + 1

            if day_name.lower().strip() == "sunday" and start_time <= given_time <= end_time:
                data_dict_day['sunday'] = data_dict_day.get('sunday', 0) + 1

            if day_name.lower().strip() == "sunday" and (given_time >= start_time_night or given_time <= end_time_night) :
                data_dict_night['sunday'] = data_dict_night.get('sunday', 0) + 1

        

        print(data_dict_night, data_dict_day)
        return None
    

    def total_incomingcalls(self, data):
        total_calls = self.collection_cdrdata.count_documents({"source_number":data, 'call_type': {'$in': ['call_in']}})
        print(total_calls)
        fromdate, todate = "2023-02-11" , "2023-03-01"
        get_data = self.collection_cdrdata.find({'source_number':data,'call_type': {'$in': ['call_in']},'timestamp': {
                '$gte': datetime.strptime(fromdate, "%Y-%m-%d").timestamp() * 1000,  
                '$lte': datetime.strptime(todate, "%Y-%m-%d").timestamp() * 1000  
            }})
        data_dict_day = {}
        data_dict_night = {}
        start_time = time(6, 0, 0)  
        end_time = time(18, 0, 0)
        start_time_night = time(18, 1, 0)
        end_time_night = time(5,59,0)
        print(start_time_night, end_time_night,"------------")
        for value in get_data:
            current_date = datetime.fromtimestamp(value['timestamp']/1000)
            given_time = current_date.time()
            day_name = calendar.day_name[current_date.weekday()]
            if day_name.lower().strip() == "monday" and start_time <= given_time <= end_time:
                data_dict_day['monday'] = data_dict_day.get('monday', 0) + 1

            if day_name.lower().strip() == "monday" and  (given_time >= start_time_night or given_time <= end_time_night):
                data_dict_night['monday'] = data_dict_night.get('monday', 0) + 1

            if day_name.lower().strip() == "tuesday" and start_time <= given_time <= end_time:
                data_dict_day['tuesday'] = data_dict_day.get('tuesday', 0) + 1

            if day_name.lower().strip() == "tuesday" and (given_time >= start_time_night or given_time <= end_time_night):
                data_dict_night['tuesday'] = data_dict_night.get('tuesday', 0) + 1

            if day_name.lower().strip() == "wednesday" and start_time <= given_time <= end_time:
                data_dict_day['wednesday'] = data_dict_day.get('wednesday', 0) + 1

            if day_name.lower().strip() == "wednesday" and  (given_time >= start_time_night or given_time <= end_time_night):
                data_dict_night['wednesday'] = data_dict_night.get('wednesday', 0) + 1

            if day_name.lower().strip() == "thursday" and start_time <= given_time <= end_time:
                data_dict_day['thursday'] = data_dict_day.get('thursday', 0) + 1

            if day_name.lower().strip() == "thursday" and  (given_time >= start_time_night or given_time <= end_time_night) :
                data_dict_night['thursday'] = data_dict_night.get('thursday', 0) + 1

            if day_name.lower().strip() == "friday" and start_time <= given_time <= end_time:
                data_dict_day['friday'] = data_dict_day.get('friday', 0) + 1

            if day_name.lower().strip() == "friday" and  (given_time >= start_time_night or given_time <= end_time_night) :
                data_dict_night['friday'] = data_dict_night.get('friday', 0) + 1

            if day_name.lower().strip() == "saturday" and start_time <= given_time <= end_time:
                data_dict_day['saturday'] = data_dict_day.get('saturday', 0) + 1

            if day_name.lower().strip() == "saturday" and (given_time >= start_time_night or given_time <= end_time_night) :
                data_dict_night['saturday'] = data_dict_night.get('saturday', 0) + 1

            if day_name.lower().strip() == "sunday" and start_time <= given_time <= end_time:
                data_dict_day['sunday'] = data_dict_day.get('sunday', 0) + 1

            if day_name.lower().strip() == "sunday" and (given_time >= start_time_night or given_time <= end_time_night) :
                data_dict_night['sunday'] = data_dict_night.get('sunday', 0) + 1

        

        print(data_dict_night, data_dict_day)
        return None
    

    def total_outgoingcalls(self, data):
        total_calls = self.collection_cdrdata.count_documents({"source_number":data, 'call_type': {'$in': ['call_out']}})
        print(total_calls)
        fromdate, todate = "2023-02-11" , "2023-03-01"
        get_data = self.collection_cdrdata.find({'source_number':data,'call_type': {'$in': ['call_out']},'timestamp': {
                '$gte': datetime.strptime(fromdate, "%Y-%m-%d").timestamp() * 1000,  
                '$lte': datetime.strptime(todate, "%Y-%m-%d").timestamp() * 1000  
            }})
        data_dict_day = {}
        data_dict_night = {}
        start_time = time(6, 0, 0)  
        end_time = time(18, 0, 0)
        start_time_night = time(18, 1, 0)
        end_time_night = time(5,59,0)
        print(start_time_night, end_time_night,"------------")
        for value in get_data:
            current_date = datetime.fromtimestamp(value['timestamp']/1000)
            given_time = current_date.time()
            day_name = calendar.day_name[current_date.weekday()]
            if day_name.lower().strip() == "monday" and start_time <= given_time <= end_time:
                data_dict_day['monday'] = data_dict_day.get('monday', 0) + 1

            if day_name.lower().strip() == "monday" and  (given_time >= start_time_night or given_time <= end_time_night):
                data_dict_night['monday'] = data_dict_night.get('monday', 0) + 1

            if day_name.lower().strip() == "tuesday" and start_time <= given_time <= end_time:
                data_dict_day['tuesday'] = data_dict_day.get('tuesday', 0) + 1

            if day_name.lower().strip() == "tuesday" and (given_time >= start_time_night or given_time <= end_time_night):
                data_dict_night['tuesday'] = data_dict_night.get('tuesday', 0) + 1

            if day_name.lower().strip() == "wednesday" and start_time <= given_time <= end_time:
                data_dict_day['wednesday'] = data_dict_day.get('wednesday', 0) + 1

            if day_name.lower().strip() == "wednesday" and  (given_time >= start_time_night or given_time <= end_time_night):
                data_dict_night['wednesday'] = data_dict_night.get('wednesday', 0) + 1

            if day_name.lower().strip() == "thursday" and start_time <= given_time <= end_time:
                data_dict_day['thursday'] = data_dict_day.get('thursday', 0) + 1

            if day_name.lower().strip() == "thursday" and  (given_time >= start_time_night or given_time <= end_time_night) :
                data_dict_night['thursday'] = data_dict_night.get('thursday', 0) + 1

            if day_name.lower().strip() == "friday" and start_time <= given_time <= end_time:
                data_dict_day['friday'] = data_dict_day.get('friday', 0) + 1

            if day_name.lower().strip() == "friday" and  (given_time >= start_time_night or given_time <= end_time_night) :
                data_dict_night['friday'] = data_dict_night.get('friday', 0) + 1

            if day_name.lower().strip() == "saturday" and start_time <= given_time <= end_time:
                data_dict_day['saturday'] = data_dict_day.get('saturday', 0) + 1

            if day_name.lower().strip() == "saturday" and (given_time >= start_time_night or given_time <= end_time_night) :
                data_dict_night['saturday'] = data_dict_night.get('saturday', 0) + 1

            if day_name.lower().strip() == "sunday" and start_time <= given_time <= end_time:
                data_dict_day['sunday'] = data_dict_day.get('sunday', 0) + 1

            if day_name.lower().strip() == "sunday" and (given_time >= start_time_night or given_time <= end_time_night) :
                data_dict_night['sunday'] = data_dict_night.get('sunday', 0) + 1

        

        print(data_dict_night, data_dict_day)
        return None
    

    def call_stat(self, data ):
        total_calls = self.collection_cdrdata.count_documents({'source_number':data, 'call_type':{'$in':['call_in','call_out']}})
        incoming_calls = self.collection_cdrdata.count_documents({'source_number':data, 'call_type':'call_in'})
        outgoing_calls = self.collection_cdrdata.count_documents({'source_number':data, 'call_type':'call_out'})
        response = {"total_calls":total_calls, 'incoming_calls':incoming_calls, 'outgoing_calls':outgoing_calls}
        return response
    
    def calls_with_destination(self, data, calltype):
        all_contacts = self.collection_cdrdata.find({'source_number':data,'call_type': calltype})#.limit(30)
        destinationNunber = {}
        for contacts in all_contacts:
            dest_contact = contacts['destination_number']
            if  dest_contact not in destinationNunber:
                
                destinationNunber[dest_contact] = {}
                destinationNunber[dest_contact] = self.collection_cdrdata.count_documents({"source_number":data, 'destination_number':dest_contact, 'call_type': calltype})
                query = [{'$match': {'source_number': data,'destination_number': dest_contact,'call_type': calltype  }},
                            {'$group': {'_id': None,  'duration': {'$sum': '$duration'}}}]
                total_call_duration = self.collection_cdrdata.aggregate(query)
                # for duration in total_call_duration:
                #     destinationNunber[dest_contact]['duration'] = str(duration['duration'])
                # print(destinationNunber)      
            
        return destinationNunber
    
    def calls_with_daywise(self,data, fromdate = False, todate = False):
        
        

        get_data = self.collection_cdrdata.find({'source_number':data,'call_type': 'call_in','timestamp': {
                '$gte': datetime.strptime(fromdate, "%Y-%m-%d").timestamp() * 1000,  
                '$lte': datetime.strptime(todate, "%Y-%m-%d").timestamp() * 1000  
            }})
        data_dict_day = {}
        start_time = time(6, 0, 0)  
        end_time = time(18, 0, 0)
        daywise_count = {}
        for induvidial_data in get_data:
            dest_num = induvidial_data['destination_number']
            day = induvidial_data['date']
            indiv_data = self.collection_cdrdata.find({'source_number':data,'destination_number':dest_num,'call_type': 'call_in'})
            if day not in daywise_count:
                daywise_count[day] = {}
                

        for value in get_data:
            current_date = datetime.fromtimestamp(value['timestamp']/1000)
            given_time = current_date.time()
            day_name = calendar.day_name[current_date.weekday()]
            if day_name.lower().strip() == "monday" and start_time <= given_time <= end_time:
                data_dict_day['monday'] = data_dict_day.get('monday', 0) + 1
    

    

# if __name__ == "__main__":
#     Cdr_Analysis().calls_with_destination()