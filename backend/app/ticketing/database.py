

from mongoengine import *
import logging
import pymongo
import time
from flask_login import UserMixin
from datetime import datetime


DB1_NAME = 'THUNDERBOLT'
DB1_ALIAS = 'default_2'


connect(DB1_NAME, host='mongodb://mymongo:27017', alias=DB1_ALIAS)
# connect(DB1_NAME, host='mongodb://localhost:27017', alias=DB1_ALIAS)



class SafeDocumentMixin:

    def save_safe(self, *args, **kwargs):
        for attempt in range(5):
            try:
                return self.save(*args, **kwargs)
            except pymongo.errors.AutoReconnect as e:
                wait_t = 0.5 * pow(2, attempt) # exponential back off
                logging.warning("PyMongo auto-reconnecting... %s. Waiting %.1f seconds.", str(e), wait_t)
                time.sleep(wait_t)

    @classmethod
    def objects_safe(cls, *args, **kwargs):
        for attempt in range(5):
            try:
                return cls.objects(*args, **kwargs)
            except pymongo.errors.AutoReconnect as e:
                wait_t = 0.5 * pow(2, attempt) # exponential back off
                print('PyMongo auto-reconnecting')
                logging.warning("PyMongo auto-reconnecting... %s. Waiting %.1f seconds.", str(e), wait_t)
                time.sleep(wait_t)

class Users(Document, UserMixin, SafeDocumentMixin):
    meta = {'db_alias': DB1_ALIAS,}

    email = EmailField(nullable=False)
    name = StringField()
    email = StringField()
    password1 = StringField()
    password2 = StringField()
    mobilenumber = StringField()
    designation = StringField()
    officername = StringField()
    team =  StringField()
    modules =  StringField()
    token_expiry = DateTimeField()
    token = StringField()
    role = StringField()
    Application = StringField()
    superior = StringField(default="Top Superior")
    status = StringField(default="Active")
    availability = StringField(default="Active")
    Application = ListField()
    user_id = StringField()
    logged = StringField()

class Tickets(Document,UserMixin,SafeDocumentMixin):
    meta = {'db_alias': DB1_ALIAS,}
 
    # _id = ObjectIdField()
    useremail = StringField()
    superior = StringField()
    date = StringField()
    officername = StringField()
    type =  StringField()
    role = StringField()
    designation =StringField()
    others = StringField()
    requestcategory =  StringField()
    requesttype =  StringField()
    requesttypes =  ListField()
    subtypes = StringField()
    team =  StringField()
    modules = StringField()
    relation =   StringField()
    nickname =   StringField()
    suspect =   StringField()
    name =   StringField()
    location =   StringField()
    source =  StringField()
    reason =  StringField()
    refno =  StringField()
    refdate = StringField()
    date1 = StringField()
    date2 = StringField()
    time = StringField()
    totimepicker = StringField()
    remarks =  StringField()
    token = StringField()
    result =ListField()
    pending = StringField()
    approval = StringField()
    Comments = StringField()
    Signature = ImageField()
    assign_Officer = StringField()
    edit = StringField(default="No")
    newnumber = ListField()
    priority = StringField()
    status =  StringField()
    status_count = StringField(default="0")
    raise_time = StringField()
    Analyst_Approval = StringField()
    Send_to_INS = StringField()
    SP_Approval = StringField()
    DSP_Approval = StringField()
    Send_to_SP = StringField()
    SP_Reject = StringField()
    DSP_Reject = StringField()
    INS_Reject = StringField()
    INSPR_Approval = StringField()
    Send_to_DSP = StringField ()
    proforma_data = ListField()

    
class HandleTickets(Document,UserMixin,SafeDocumentMixin):
    meta = {'db_alias': DB1_ALIAS,}

    msisdn = StringField()
    FetchedNickName = StringField()


class Comments(Document,UserMixin,SafeDocumentMixin):
    meta = {'db_alias': DB1_ALIAS,}

    msisdn = IntField()
    remarks = StringField()

class ActionLog(Document,UserMixin,SafeDocumentMixin):
    meta = {'db_alias': DB1_ALIAS,}

    email = EmailField()
    deletedata = StringField()
    updatedata = StringField()
    
class SignDoc(Document,UserMixin,SafeDocumentMixin):
    meta = {'db_alias': DB1_ALIAS,}

    annexureSign = ImageField()












