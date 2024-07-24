from datetime import datetime
import pymongo
from MongoClinet import CDAT, thunderbolt,VIGOR
from tqdm import tqdm
mongocdat = CDAT()
mongothunder = thunderbolt()
mongovigor = VIGOR()








def cdrcalls(phn,fromdate):
    print(phn,fromdate, type(phn),type(fromdate))
    # phn = '9437639668'
    # fromdate = '2023-12-18'
    iso_date_str = datetime.strptime(fromdate, '%Y-%m-%d')#.strftime('%d-%m-%Y')
    print(type(iso_date_str), iso_date_str)
    getnum_c = list(mongocdat.cdrdata.find({'source_number':phn,'date_format':{'$gte':iso_date_str}},{'_id':0}))
    getnum_v = list(mongovigor.cri_meta.find({'TXT_TARGET_NUMBER':{'$regex':phn},'DAT_CALL_START':{'$gte':iso_date_str}}))

    print(len(getnum_c))
    data_dict = {'cdr_calls':len(getnum_c),'vigor_calls':len(getnum_v),'unmatched':[],'message':'success'}
    for _gn in tqdm(getnum_c[:100]):
        # print(_gn)
        _vc = mongovigor.cri_meta.find_one({'TXT_TARGET_NUMBER':{'$regex':_gn['source_number']},'DAT_CALL_START':{'$eq':_gn['date_format']}})
        # print(_vc,"==")
        if _vc is None:
            data_dict['unmatched'].append(_gn)
            data_dict['unmatched_count'] = data_dict.get('unmatched_count',0) + 1
    print(data_dict)
    if len(getnum_v) > len(getnum_c):
        print("cdr data not availble for the given period")
        find_calls = mongocdat.cdrdata.find_one({'source_number':phn},sort=[('_id',pymongo.DESCENDING)])
        print(find_calls)
    
    return data_dict
    

