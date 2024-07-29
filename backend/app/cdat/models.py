
from datetime import datetime
from flask_mongoengine import MongoEngine
from mongoengine import *
from mongoengine import Document, StringField, connect
from bson import ObjectId


from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField
from datetime import datetime

# db = MongoEngine()
connect('NexusData',host='mongodb://mymongo:27017/')
# connect('NexusData',host='mongodb://mongo-cdat:27017/')




class User(Document, ):
    email = StringField(nullable=False)
    name = StringField()
    password = StringField()
    role = StringField(default="user")
    meta = {'db_alias': 'default'}

class Case(Document,  ):
    name = StringField()
    alias = StringField()
    createdate = DateTimeField(default=datetime.utcnow())
    user_id = ReferenceField(User)
    ownerName = ListField()
    meta = {'db_alias': 'default'}

class Corpus(Document,  ):
    hash_md5 = StringField()
    case_id = ReferenceField(Case)
    filename = StringField()
    field_value = StringField()
    processed = StringField()
    filesize = DecimalField()
    # uploadOn = DateTimeField()
    field_value = StringField()
    datetime = DateTimeField(default=datetime.utcnow())
    type_f = StringField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    user_id = ReferenceField(User)
    voip_count = StringField()
    provider = StringField()
    meta = {'db_alias': 'default'}
    
class Call_Stats(Document,  ):
  
    field_value = StringField()
    type_f = StringField()
    file_count = IntField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    meta = {'db_alias': 'default'}


    

class VoipCalls(Document,  ):
    user_id = ReferenceField(User)
    case_id = ReferenceField(Case)
    count = IntField()
    destination_ip = StringField()
    uploaded_status = StringField()
    # dest_type = StringField()
    # destination_port = StringField()
    destination_port = ListField()
    upload_time = DateTimeField()
    time = DateTimeField()
    end_time = DateTimeField()
    msisdn = StringField()
    ownerName = StringField()
    source_ip = StringField()
    # source_port = StringField()
    source_port = ListField()
    # cellid = StringField()
    cellid = ListField()
    vendor = StringField()
    celllocation =StringField()
    # matchedcall = ListField()
    matchedcall = StringField()
    latitude = StringField()
    longitude = StringField()
    ipinfo = StringField()
    filehash = StringField()
    home_circle = StringField()
    provider = StringField()
    status = IntField()
    visual=IntField()
    meta = {'db_alias': 'default'}


class ProbVoipCalls(Document,):
    user_id = ReferenceField(User)
    case_id = ReferenceField(Case)
    count = IntField()
    destination_ip = StringField()
    uploaded_status = StringField()
    # dest_type = StringField()
    destination_port = StringField()
    # destination_port = ListField()
    upload_time = DateTimeField()
    time = DateTimeField()
    end_time = DateTimeField()
    msisdn = StringField()
    ownerName = StringField()
    source_ip = StringField()
    source_port = StringField()
    # source_port = ListField()
    cellid = StringField()
    # cellid = ListField()
    vendor = StringField()
    celllocation =StringField()
    # matchedcall = ListField()
    matchedcall = StringField()
    latitude = StringField()
    longitude = StringField()
    ipinfo = StringField()
    filehash = StringField()
    home_circle = StringField()
    provider = StringField()
    status = IntField()
    visual=IntField()
    meta = {'db_alias': 'default'}



class MatchedCalls(Document,  ):
    user_id = ReferenceField(User)
    case_id = ReferenceField(Case)
    caller1 = StringField()
    ownerName = StringField()
    # upload_time = DateTimeField()
    caller2 = StringField()
    calltime = DateTimeField()
    addtime = DateTimeField()
    source_ip = StringField()
    destination_ip = StringField()
    filehash = ListField(StringField())
    remarks = StringField()
    meta = {'db_alias': 'default'}

class RawData(Document,  ):
    user_id = ReferenceField(User)
    case_id = ReferenceField(User)
    cellid = StringField()
    msisdn = StringField()
    source_ip = StringField()
    source_port = StringField()
    public_ip = StringField()
    public_port = StringField()
    destination_ip = StringField()
    destination_port = StringField()
    dpi = StringField()
    ppi = StringField()
    time = DateTimeField()
    filehash = StringField()
    imei = StringField()
    imsi = StringField()
    downlink_vol = StringField()
    uplink_vol = StringField()
    roaming = StringField()
    ipv6 = StringField()
    provider = StringField()
    vpn = StringField()
    company = StringField()
    asn = StringField()
    domain = StringField()
    meta = {'db_alias': 'user-db-alias'}


class TempRawData(Document,  ):
    user_id = ReferenceField(User)
    case_id = ReferenceField(Case)
    cellid = StringField()
    msisdn = StringField()
    source_ip = StringField()
    source_port = StringField()
    public_ip = StringField()
    public_port = StringField()
    destination_ip = StringField()
    destination_port = StringField()
    dpi = StringField()
    ppi = StringField()
    time = DateTimeField()
    filehash = StringField()
    imei = StringField()
    imsi = StringField()
    downlink_vol = StringField()
    uplink_vol = StringField()
    roaming = StringField()
    ipv6 = StringField()
    provider = StringField()
    meta = {'db_alias': 'user-db-alias'}


class Callers(Document,  ):
    msisdn = StringField()
    ownerName = StringField()
    # upload_time = DateTimeField()
    user_id = ReferenceField(User)
    case_id = ReferenceField(Case)
    filehash = ReferenceField(Corpus)
    name = StringField()
    notes = StringField()
    visual = StringField()
    meta = {'db_alias': 'default'}



class GtrData(Document,  ):
    user_id = ReferenceField(User)
    case_id = ReferenceField(Case)
    msisdn = StringField()
    source_ip = StringField()
    upload_time = DateTimeField()
    source_port = StringField()
    public_ip = StringField()
    public_port = StringField()
    destination_ip = StringField()
    destination_port = StringField()
    dpi = StringField()
    ppi = StringField()
    time = DateTimeField()
    filehash = StringField()
    meta = {'db_alias': 'default'}

class GrData(Document,  ):
    user_id = ReferenceField(User)
    case_id = ReferenceField(User)
    msisdn = StringField()
    source_ip = StringField()
    source_port = StringField()
    public_ip = StringField()
    public_port = StringField()
    destination_ip = StringField()
    destination_port = StringField()
    dpi = StringField()
    ppi = StringField()
    time = DateTimeField()
    filehash = StringField()
    meta = {'db_alias': 'default'}
class RawData(Document,  ):
    user_id = ReferenceField(User)
    case_id = ReferenceField(User)
    cellid = StringField()
    msisdn = StringField()
    ownerName = StringField()
    source_ip = StringField()
    source_port = StringField()
    public_ip = StringField()
    public_port = StringField()
    destination_ip = StringField()
    destination_port = StringField()
    dpi = StringField()
    ppi = StringField()
    time = DateTimeField()
    filehash = StringField()
    imei = StringField()
    imsi = StringField()
    downlink_vol = StringField()
    uplink_vol = StringField()
    roaming = StringField()
    ipv6 = StringField()
    provider = StringField()
    vpn = StringField()
    company = StringField()
    asn = StringField()
    domain = StringField()
    meta = {'db_alias': 'default'}


class TempRawData(Document,  ):
    user_id = ReferenceField(User)
    case_id = ReferenceField(Case)
    cellid = StringField()
    msisdn = StringField()
    source_ip = StringField()
    source_port = StringField()
    public_ip = StringField()
    public_port = StringField()
    destination_ip = StringField()
    destination_port = StringField()
    dpi = StringField()
    ppi = StringField()
    time = DateTimeField()
    filehash = StringField()
    imei = StringField()
    imsi = StringField()
    downlink_vol = StringField()
    uplink_vol = StringField()
    roaming = StringField()
    ipv6 = StringField()
    provider = StringField()
    meta = {'db_alias': 'default'}


class Callers(Document,  ):
    msisdn = StringField()
    ownerName = StringField()
    user_id = ReferenceField(User)
    case_id = ReferenceField(Case)
    filehash = ReferenceField(Corpus)
    name = StringField()
    notes = StringField()
    visual = StringField()
    meta = {'db_alias': 'default'}



class GtrData(Document,  ):
    user_id = ReferenceField(User)
    case_id = ReferenceField(Case)
    msisdn = StringField()
    source_ip = StringField()
    source_port = StringField()
    public_ip = StringField()
    public_port = StringField()
    destination_ip = StringField()
    destination_port = StringField()
    dpi = StringField()
    ppi = StringField()
    time = DateTimeField()
    filehash = StringField()
    meta = {'db_alias': 'default'}

class GrData(Document,  ):
    user_id = ReferenceField(User)
    case_id = ReferenceField(User)
    msisdn = StringField()
    source_ip = StringField()
    source_port = StringField()
    public_ip = StringField()
    public_port = StringField()
    destination_ip = StringField()
    destination_port = StringField()
    dpi = StringField()
    ppi = StringField()
    time = DateTimeField()
    filehash = StringField()
    meta = {'db_alias': 'default'}

class GmCalls(Document,  ):
    user_id = ReferenceField(User)
    case_id = ListField(ReferenceField(Case))
    caller1 = StringField()
    # upload_time = DateTimeField()
    caller2 = StringField()
    calltime = DateTimeField()
    addtime = DateTimeField()
    source_ip = StringField()
    destination_ip = StringField()
    filehash = ListField(StringField())
    meta = {'db_alias': 'default'}
class GmCalls(Document,  ):
    user_id = ReferenceField(User)
    case_id = ListField(ReferenceField(Case))
    caller1 = StringField()
    caller2 = StringField()
    calltime = DateTimeField()
    addtime = DateTimeField()
    source_ip = StringField()
    destination_ip = StringField()
    filehash = ListField(StringField())
    meta = {'db_alias': 'default'}



class IpInfo(Document,  ):
    companyname_text  =  StringField()
    carriername_text  =  StringField() 
    longitude_text  =  StringField()
    abuseemail_text  =  StringField()
    country_flag_text  =  StringField()
    privacyhosting_text  =  StringField()
    privacytor_text  =  StringField()
    country_text  =  StringField()
    abusephone_text  =  StringField()
    continentcode_text  =  StringField()
    bogon_text  =  StringField()
    asnroute_text  =  StringField()
    privacyrelay_text  =  StringField()
    hostname_text  =  StringField()
    abusename_text  =  StringField()
    carriermnc_text  =  StringField()
    privacyservice_text  =  StringField()
    abuseaddress_text  =  StringField()
    domainstotal_text  =  StringField()
    carriermcc_text  =  StringField()
    country_name_text  =  StringField()
    latitude_text  =  StringField()
    abusenetwork_text  =  StringField()
    isEU_text  =  StringField()
    privacyvpn_text  =  StringField()
    abusecountry_text  =  StringField()
    asndomain_text  =  StringField()
    country_flagemoji_text  =  StringField()
    timezone_text  =  StringField()
    country_flagunicode_text  =  StringField()
    loc_text  =  StringField()
    asntype_text  =  StringField()
    ip_text  =  StringField()
    asnname_text  =  StringField()
    asnasn_text  =  StringField()
    privacyproxy_text  =  StringField()
    city_text  =  StringField()
    country_currencysymbol_text  =  StringField()
    domainsip_text  =  StringField()
    postal_text  =  StringField()
    continent_text  =  StringField()
    country_currencycode_text  =  StringField()
    domainsdomains_text  =  StringField()
    country_currency_text  =  StringField()
    companydomain_text  =  StringField()
    continentname_text  =  StringField()
    region_text  =  StringField()
    companytype_text  =  StringField()
    anycast_text  =  StringField()
    meta = {'db_alias': 'default'}


# Pcap DataBase Schema Added on February 09th 2023

class PcapCorpus(Document,  ):
    hash_md5 = StringField()
    case_id = ReferenceField(Case)
    filename = StringField()
    processed = StringField()
    filesize = DecimalField()
    datetime = DateTimeField(default=datetime.utcnow())
    type_f = StringField()
    # start_time = DateTimeField()
    # end_time = DateTimeField()
    user_id = ReferenceField(User)
    voip_count = StringField()
    meta = {'db_alias': 'default'}

class PcapVoipCalls(Document,  ):
    user_id = ReferenceField(User)
    case_id = ReferenceField(Case)
    count = IntField()
    destination_ip = StringField()
    destination_port = StringField()
    time = DateTimeField()
    # end_time = DateTimeField()
    # msisdn = StringField()
    source_ip = StringField()
    source_port = StringField()
    # cellid = StringField()
    vendor = StringField()
    # celllocation =StringField()
    # latitude = StringField()
    # longitude = StringField()
    ipinfo = StringField()
    filehash = StringField()
    # home_circle = StringField()
    # status = IntField()
    # visual=IntField()
    meta = {'db_alias': 'default'}

class PcapRawData(Document,  ):
    user_id = ReferenceField(User)
    case_id = ReferenceField(User)
    # msisdn = StringField()
    source_ip = StringField()
    source_port = StringField()
    # public_ip = StringField()
    # public_port = StringField()
    destination_ip = StringField()
    destination_port = StringField()
    dpi = StringField()
    ppi = StringField()
    time = DateTimeField()
    filehash = StringField()
    meta = {'db_alias': 'default'}


class PcapTempRawData(Document,  ):
    user_id = ReferenceField(User)
    case_id = ReferenceField(Case)
    # msisdn = StringField()
    source_ip = StringField()
    source_port = StringField()
    # public_ip = StringField()
    # public_port = StringField()
    destination_ip = StringField()
    destination_port = StringField()
    dpi = StringField()
    ppi = StringField()
    time = DateTimeField()
    filehash = StringField()
    meta = {'db_alias': 'default'}