import os
import flask
# from flask import *
from app.auth.routes import token_required
import flask_cors
from flask import Flask, request, jsonify
from app.cdat.lib import main as getcdrdata
from app.cdat.lib import analysis as phDashboard
from app.cdat.lib import graph as getgraphview
from app.cdat.lib import tower_analysis as tower
from app.cdat.lib import dashboard as dashboardcount
from app.cdat.lib import rfi as redflag
from app.cdat import cdr_bp
from app.analysis.lib import tower as towerdata
from app.analysis.lib import sdr_lookup as sdr_lookup
from datetime import datetime
from MongoClinet import Database, CDAT, thunderbolt
import time
from app.cdat.models import *
from app.cdat.lib.dashboard import Cdr_Analysis
mongothunder = thunderbolt()
mongodata = Database()
Sdr_Lookup = sdr_lookup.Sdr_Lookup()
cdat_collection = CDAT()
cdrAnalysis = Cdr_Analysis()

cors_allowed_ip = "*"

# /bookmarkdata , /dashboardcounts

@cdr_bp.route("/profile_num", methods=['POST'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def profilenum(current_user):
    response = ''
    res_toc = ''
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    data = request.form.get('number')
    mode = request.form.get('mode')
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})
    if mode == "profile":
        response = getcdrdata.Cdr_Analysis().cdr_profile(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    
    if mode == "analysis_profile":
        print(data,"--------------")
        response = getcdrdata.Cdr_Analysis().analysis_profile(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    elif mode == "cellIdSearch":
        response = getcdrdata.Cdr_Analysis().cellid_data(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    elif mode == "cdatContacts":
        response = getcdrdata.Cdr_Analysis().cdat_contacts(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    elif mode == "SecondLevel":
        print("Second level")
        response = getcdrdata.Cdr_Analysis().second_level_cdat(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        print(response['time_taken'])

    elif mode == "imeiSearch":
        response = getcdrdata.Cdr_Analysis().phones_used_in_imei(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "towerprofile":
        response = getcdrdata.Cdr_Analysis().tower_profile(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "ipdrprofile":
        response = getcdrdata.Cdr_Analysis().ipdr_profile(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    print(response)
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})
    return jsonify(response)


@cdr_bp.route("/hyperlink", methods=['POST'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def hyperlink(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]

    data = request.form.get('number')
    fromdate = request.form.get('fromdate')
    todate = request.form.get('todate')
    data = request.form.get('number')
    dest = request.form.get('dest_count')
    mode = request.form.get('mode')
    state = request.form.get('state')
    dest_num = request.form.get('dest_num')
    cellid = request.form.get('cellid')
    imei = request.form.get('imei_num', False)
    req_toc = time.time() - tic

    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})

    print(mode, data, dest_num, imei, cellid,
          fromdate, todate, state, "---hyperlink-----")
    response = ''
    res_toc = ''
    if mode == "cdat_count":
        response = getcdrdata.Cdr_Analysis().cdat_contacts(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)
    if mode == "other_states":
        response = getcdrdata.Cdr_Analysis().other_states(data, state)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)
    if mode == "dest_count":
        response = getcdrdata.Cdr_Analysis().dest_count(data, dest)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)
    if mode == "imei":
        imei = imei.split(",")
        response = getcdrdata.Cdr_Analysis().imei_search_info(data, imei)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)
    if mode == "call_in":
        response = getcdrdata.Cdr_Analysis().callin_callout(
            data, mode, imei, dest_num, fromdate, todate, state)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)
    if mode == "call_out":
        response = getcdrdata.Cdr_Analysis().callin_callout(
            data, mode, imei, dest_num, fromdate, todate, state)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)
    if mode == "total_contacts":
        response = getcdrdata.Cdr_Analysis().total_contacts(data, dest_num)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)
    if mode == "total_calls":
        if dest_num == "undefined":
            dest_num = False
        if imei == "undefined" or imei == "" or imei is False:
            imei = False
        if state == "":
            state = False
        print(state, "-in total_calss--")
        response = getcdrdata.Cdr_Analysis().cdr_data(data, mode, fromdate, todate,
                                                      dest_num, imei, state, items=False, currentpage=False)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)

    if mode == "dest_num":
        response = getcdrdata.Cdr_Analysis().contact_info(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)

    if mode == "tower_total_calls" or mode == "tower_day_calls" or mode == "tower_night_calls":
        response = getcdrdata.Cdr_Analysis().location_record(data, cellid, mode)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)

    if mode == "cellidsearch":
        response = getcdrdata.Cdr_Analysis().cellid_data(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)

    if mode == "undefined":
        response = {}
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        response['data_dict'] = 'Not data Matched'

    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


@cdr_bp.route("/imei_search", methods=['POST'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def imei_search(current_user):
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    tic = time.time()
    data = request.form.get('number')
    mode = request.form.get('mode')
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})
    response = ''
    res_toc = ''
    if mode == "IMEIUsedInPHONE":
        response = getcdrdata.Cdr_Analysis().imei_used_in_phone(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "PhoneUsedinIMEI":
        response = getcdrdata.Cdr_Analysis().phones_used_in_imei(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "IMEISearchInfo":
        data = data.split(",")
        response = getcdrdata.Cdr_Analysis().imei_search_info(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


@cdr_bp.route("/imsi_details", methods=['POST'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def imsi_details(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]

    data = request.form.get('number')
    mode = request.form.get('mode')
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})
    response = ''
    res_toc = ''
    if mode == "IMSI":
        response = getcdrdata.Cdr_Analysis().imsi_search_info(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "IMSIPhone":
        response = getcdrdata.Cdr_Analysis().imsi_used_in_phone(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})
    
    return jsonify(response)


@cdr_bp.route("/summary_of_mobile", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def summaryNew(current_user):
    """
    Payload: Mobile Number

    Description:
    This function generates the data for phone,nickname,callin,callout,duration,firstcall,lastcall,address
    based on given mobile number

    return:
    phone,nickname,callin,callout,duration,firstcall,lastcall,address

    """
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    data = flask.request.form.get("number")
    mode = flask.request.form.get("mode")
    fromdate = flask.request.form.get('fromdate')
    todate = flask.request.form.get('todate')
    items = flask.request.form.get('items_per_page')
    currentpage = flask.request.form.get('page')
    print(data, mode, fromdate, todate)
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})

    if mode == "summary_total":
        response = getcdrdata.Cdr_Analysis().get_total_summary(data, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)
    if mode == "summaryBetweenDates":
        response = getcdrdata.Cdr_Analysis().getsummary_between_dates(
            data, mode, fromdate, todate, items, currentpage)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['times'].append(time_taken)
        with open('summary.log', '+a') as file:
            for i in response['times']:
                file.writelines(f"{i}\n")
        response['time_taken'] = time_taken
        # return jsonify(response)

    # response = getcdrdata.Cdr_Analysis().getsummary(
    #     data, mode, fromdate, todate, items, currentpage)
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})
    
    return jsonify(response)


@cdr_bp.route("/summary_for_state", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def summaryStateWise(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    data = request.form.get('number')
    fromDate = request.form.get('fromdate')
    endDate = request.form.get('todate')
    state = request.form.get('state')
    mode = request.form.get('mode')
    print(mode, state)
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})
    
    if state is not None:
        state = state
    else:
        state = False
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})

    if mode == "SummaryWithoutState" or mode == "SummaryStateWise" or mode == "SummaryWithState":
        res_toc = time.time() - tic
        response = getcdrdata.Cdr_Analysis().summary_for_state(
            data, state, mode, fromDate, endDate)
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})
    return jsonify(response)


@cdr_bp.route("/location", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def location(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]

    data = flask.request.form.get("number")
    from_date = flask.request.form.get("from_date")
    to_date = flask.request.form.get("to_date")
    mode = flask.request.form.get("mode")
    items = flask.request.form.get('items_per_page')
    currentpage = flask.request.form.get('page')
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})

    if mode == "TotalLocation":
        response = getcdrdata.Cdr_Analysis().total_location(
            data, items, currentpage, from_date, to_date)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)

    if mode == "DayNightMapping":
        response = getcdrdata.Cdr_Analysis().day_night_mapping(data, from_date, to_date)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)

    if mode == "Top10DayLocWithDate":
        response = getcdrdata.Cdr_Analysis().day_mapping_with_date(data, from_date, to_date)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)

    if mode == "Top10NightLocWithDate":
        response = getcdrdata.Cdr_Analysis().night_mapping_with_date(data, from_date, to_date)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


@cdr_bp.route("/call_details", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def call_details(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]

    data = flask.request.form.get("number")
    dest_num = flask.request.form.get("dest_num")
    mode = flask.request.form.get("mode")
    sd = flask.request.form.get("fromdate")
    ed = flask.request.form.get("todate")
    items = flask.request.form.get('items_per_page')
    currentpage = flask.request.form.get('page')
    print(data, mode, items, currentpage, "call_details")
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})

    if mode == "CommonContacts":
        response = getcdrdata.Cdr_Analysis().common_contacts(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)
    if mode == "common_contacts":
        response = getcdrdata.Cdr_Analysis().common_contact_hyperlink(dest_num, data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)
    if mode == "handset":
        response = getcdrdata.Cdr_Analysis().common_handset(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)
    

    if mode == "cdrdetails" or mode == "cdrIMEI":
        print(data, mode, items, currentpage, "cdr_details")
        response = getcdrdata.Cdr_Analysis().cdr_data(
            data, mode, sd, ed, False, False, False, items, currentpage)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)
    
    if mode == "CdrBetweenDates":
        print(data, mode, sd, ed, "cdr_details")
        response = getcdrdata.Cdr_Analysis().CdrBetweenDates(
            data, mode, sd, ed, currentpage)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        return jsonify(response)
    

    if mode == "multipleNumber":
        response = getcdrdata.Cdr_Analysis().multi_cdr_data(
            data, sd, ed, items, currentpage)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)

    if mode == "CdrBtwmultipleNumber" or mode == "loopcalls":
        response = getcdrdata.Cdr_Analysis().cdr_btw_multilevel(data, mode, sd, ed)
        res_toc = time.time() - tic
        
        # return jsonify(response)

    if mode == "silentPeriod":
        print("---manin--")
        print(data, sd, ed)
        response = getcdrdata.Cdr_Analysis().silent_period(data, sd, ed)
        print(response)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)

    if mode == "ipdrdetails":
        response = getcdrdata.Cdr_Analysis().ipdr_details(
            data, sd, ed, items, currentpage)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)

    if mode == "gprsdetails":
        response = getcdrdata.Cdr_Analysis().gprs_details(data, items, currentpage)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)

    if mode == "summary_ipdr":
        response = getcdrdata.Cdr_Analysis().summary_ipdr(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)

    elif mode == "IpdrGprsCdr":
        response = getcdrdata.Cdr_Analysis().ipdr_gprs_cdr(data, sd, ed)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})
    return jsonify(response)


@cdr_bp.route("/search", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def search(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]

    lat = flask.request.form.get("lat")
    long = flask.request.form.get("long")
    data = flask.request.form.get("number")
    mode = flask.request.form.get("mode")
    nickname = flask.request.form.get('nickname')
    address = flask.request.form.get('address')
    state = flask.request.form.get('state')
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})

    if mode == "LatLongCdrData":
        response = getcdrdata.Cdr_Analysis().lat_long_cdr_data(lat, long)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)

    if mode == "CellidData":
        response = getcdrdata.Cdr_Analysis().cellid_data(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)

    if mode == "SingleAddress" or mode == "BulkAddress":
        response = getcdrdata.Cdr_Analysis().single_address(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)

    if mode == "RhData":
        response = getcdrdata.Cdr_Analysis().rh_details(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)

    if mode == "POAData":
        response = getcdrdata.Cdr_Analysis().poa_search(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        # return jsonify(response)
    if mode == "NicknameSearch" or mode == "MixedSearch":
        response = getcdrdata.Cdr_Analysis().nickname_search(
            data, mode, nickname, address, state)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    # if mode == "MixedSearch":
    #     response = getcdrdata.Cdr_Analysis().nickname_search(data,mode,nickname,address)
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


@cdr_bp.route("/phone_dashboard", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def phone_dashboard(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    data = flask.request.form.get('number')
    mode = flask.request.form.get('mode')
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})

    if mode == "phone_dashboard":
        response = phDashboard.Cdr_Analysis().call_stat(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "incoming_data":
        response = phDashboard.Cdr_Analysis().calls_with_destination(data, 'call_in')
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "outgoing_data":
        response = phDashboard.Cdr_Analysis().calls_with_destination(data, 'call_out')
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


@cdr_bp.route("/graph_view", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def graph_view(current_user):
    print("-------------")
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    data = request.json
    print(data, "dataaaaaaaa")
    num = data.get("number")
    fromdate = data.get("fromdate")
    todate = data.get("todate")
    print(num, fromdate, todate)
    mode = data.get("mode")
    submode = data.get('submode')
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})

    if mode == "IPCount":
        response = getgraphview.Graph_View().get_data(num, fromdate, todate)
        res_toc = time.time() - tic
        
    if mode == "getcompany":
        response = getgraphview.Graph_View().get_company(num, fromdate, todate)
        res_toc = time.time() - tic
        
    if mode == "ImeiCount":
        response = getgraphview.Graph_View().get_imei_filter(num, fromdate, todate)
        res_toc = time.time() - tic
        
    if mode == "CellidCount":
        response = getgraphview.Graph_View().get_cellid_filter(num, fromdate, todate)
        res_toc = time.time() - tic
        
    if mode == "DataUsage":
        response = getgraphview.Graph_View().get_data_usage(num, fromdate, todate)
        res_toc = time.time() - tic
        
    if mode == "DaywiseDataUsage":
        response = getgraphview.Graph_View().get_daywise_usage(num, fromdate, todate)
        res_toc = time.time() - tic
        
    if mode == "NightwiseDataUsage":
        response = getgraphview.Graph_View().get_nightwise_usage(num, fromdate, todate)
        res_toc = time.time() - tic
        
    if mode == "CdrCount":
        response = getgraphview.Graph_View().cdr_data(num, fromdate, todate)
        res_toc = time.time() - tic
        
    if mode == 'toptenlocation':
        response = getgraphview.Graph_View().top_10_location(
            data, submode, fromdate, todate)
        res_toc = time.time() - tic
        
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})
    return jsonify(response)


@cdr_bp.route("/analysis", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def analysis(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]

    number = flask.request.form.get("number")
    fromdate = flask.request.form.get("fromdate")
    todate = flask.request.form.get("todate")
    name = flask.request.form.get("name")
    address = flask.request.form.get("address")
    mode = flask.request.form.get("mode")
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':analysis})

    print(number, "Number")
    if mode == "TowerData":
        response = getcdrdata.Cdr_Analysis().tower_data(number)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        return jsonify(response)

    if mode == "name_search":
        response = Sdr_Lookup.name_search(name)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "number_search":
        response = Sdr_Lookup.number_search(number, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "address_search":
        response = Sdr_Lookup.address_search(address)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "date_target":
        response = Sdr_Lookup.date_target(number)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "meeting_point":
        print("inside meeting point")
        response = getcdrdata.Cdr_Analysis().get_common_link_using_area(
            number, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "recharge_history":
        print("inside the recharge route")
        response = getcdrdata.Cdr_Analysis().sm_rh(number, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response["time_taken"] = time_taken

    if mode == "sm_poa":
        print("inside the sm_poa route")
        response = Sdr_Lookup.sm_poa(number, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response["time_taken"] = time_taken

    if mode == "alternate_number":
        print("inside the alternate route")
        response = Sdr_Lookup.alternate_number(number, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response["time_taken"] = time_taken

    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


@cdr_bp.route("/dashboard_data", methods=['GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def dashboardData(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]

    try:
        response = dashboardcount.Cdr_Analysis().unique_counts()
        res_toc = time.time() - tic
        mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/dashboard_data','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/dashboard_data'})

        time_taken = {"received_at": tic, "res": res_toc}
        response_data = {
            "status": "success",
            "data": response,
            "time_taken": time_taken,
            "message": "Data retrieved successfully"
        }

    except Exception as e:
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "res": res_toc}
        response_data = {
            "status": "error",
            "data": None,
            "time_taken": time_taken,
            "message": str(e)
        }
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response_data)


@cdr_bp.route("/tower_dashboard", methods=["GET", "POST"])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def tower_dashboard(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    mode = flask.request.get_json("mode")
    req_toc = time.time() - tic
    print("-----------mode-----routes---", mode)
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/tower_dashboard'})

    if mode == mode:
        response = dashboardcount.Cdr_Analysis().dashboard_map(mode)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response_data = {
            "status": "success",
            "data": response,
            "time_taken": time_taken,
            "message": "Data retrieved successfully"
        }
        print(response_data, "+++++++++++++++++++++++++++++++++++++++++++++")
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})
    
    return jsonify(response_data)


@cdr_bp.route("/pie-chart", methods=['GET', "POST"])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def pie_charts(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/pie-chart','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/pie-chart'})
    response = dashboardcount.Cdr_Analysis().pieChart()
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "res": res_toc}
    response['time_taken'] = time_taken
    result = {
        "data": response,
    }
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(result)


@cdr_bp.route("/counts", methods=["GET", "POST"])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def counts(current_user):
    print("Inside")
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/pie-chart','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/counts'})
    response = dashboardcount.Cdr_Analysis().pieChart()
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "res": res_toc}
    response['time_taken'] = time_taken
    
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})
    
    return jsonify(response)


# ------------------------------------Tower Analysis-----------------------------------#
@cdr_bp.route("/tower_analysis", methods=['POST'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def tower_analysis(current_user):
    # print("WECLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/pie-chart','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/tower_analysis'})

    key_location = flask.request.form.get("key_location")
    sitename = flask.request.form.get("sitename")
    fromdate = flask.request.form.get("fromdate")
    todate = flask.request.form.get("todate")
    mode = flask.request.form.get("mode")
    numbers = flask.request.form.get("numbers")
    lat = flask.request.form.get('lat')
    long = flask.request.form.get('long')
    radius = flask.request.form.get('radius')
    req_toc = time.time() - tic

    response = ''

    if mode == "common_source" or mode == "common_destination":
        response = tower.Tower_View().common_numbers_in_different_towers(
            mode, key_location, sitename, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "relational_call":
        response = tower.Tower_View().unique_common_groups_in_different_towers(
            key_location, sitename, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "group_of_numbers":
        response = tower.Tower_View().group_of_numbers(
            numbers, key_location, fromdate, todate, sitename)  # , fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "internal_calling":
        response = tower.Tower_View().internal_calling(sitename, key_location)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "call_details":
        response = tower.Tower_View().call_details(numbers, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "day_wise_analysis":
        response = tower.Tower_View().day_wise_analysis(sitename, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "numbersummary":
        response = tower.Tower_View().number_summary(numbers)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "under_tower_calls":
        response = tower.Tower_View().calls_under_tower(
            key_location, sitename, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "tower_group_creation":
        response = tower.Tower_View().tower_groups_location_time(lat, long, radius)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response_data = {
            'time_taken': time_taken,
            'response': response
        }
        # return response_data

    # if mode == "summary":
    #     response = tower.Tower_View().summary(numbers)
    #     res_toc = time.time() - tic
    #     time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    #     response['time_taken'] = time_taken

    if mode == "roaming_details":
        response = tower.Tower_View().roaming_details(numbers, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "active_inactive_period":
        response = tower.Tower_View().active_and_inactive_period(numbers)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


@cdr_bp.route("/tower_analysis_2", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def tower_analysis_two(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]

    print("WECLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
    inputdata = flask.request.get_json('value')
    mode = inputdata['mode']
    fromdate = inputdata.get('fromdate')
    todate = inputdata.get('todate')

    print(mode,fromdate,todate,"===")
    numbers = inputdata.get('numbers')
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'tower_analysis_2'})

    response = {}
    # if mode == "common_source" or  mode == "common_destination" or mode == "common_imei":
    #     response = tower.Tower_View().common_numbers_in_towers(mode,inputdata['value'])
    if mode == "common_source" or mode == "common_destination" or mode == "common_imei":
        response = tower.Tower_View().common_numbers_in_different_towers(
            mode, inputdata['value'], fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "overview":
        response == tower.Tower_View().overview(inputdata['value'])
    # if mode == "formulaone":
    #     response = tower.Tower_View().aggregate_tower_data(inputdata['value'])
    #     res_toc = time.time() - tic
    #     time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    #     response['time_taken'] = time_taken
    if mode == "sameconvo":
        response = tower.Tower_View().unique_common_groups_in_different_towers(
            inputdata['value'], fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "internalcalling":
        response = tower.Tower_View().internal_calling(
            inputdata['value'], fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "callsundertower":
        response = tower.Tower_View().calls_under_tower(
            inputdata['value'], fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "call_detials":
        print("call detials")
        response = tower.Tower_View().call_details(inputdata['value'],fromdate,todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "summary":
        response = tower.Tower_View().summary(inputdata['value'] , fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "groupofnumbers":
        print(numbers, inputdata['value'], "------------")
        response = tower.Tower_View().group_of_numbers(numbers, fromdate, todate, inputdata['value'])
        print(response,"---------")
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken

    if mode == "formulaone":
        response = tower.Tower_View().tower_profile(inputdata['value'],fromdate,todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken


    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


@cdr_bp.route("/tower", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def towersummary(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/tower','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/tower'})

    print("in tower func")
    coord = flask.request.get_json('coordinates')
    req_toc = time.time() - tic
    response = towerdata.Tower_View().get_tower_in_polygon(coord)
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})
    
    return jsonify(response)



@cdr_bp.route("/getcasedata", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def getcase(current_user):
    print(request.method, "gwt")
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]

    req_toc = time.time() - tic

    casename = flask.request.get_json('casename')
    casetype = flask.request.get_json('casetype')
    user = flask.request.get_json('user')
    itemsper_page = flask.request.get_json('itemsper_page')
    pagenumber = flask.request.get_json('pagenumber')
    mode = flask.request.get_json('mode')
    print(casename,mode['mode'],user['user'])
    getdata = ''
    res_toc = ''
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/getcasedata'})

    if mode['mode'] == "getcases":
        getdata = towerdata.Tower_View().casedata(user['user'])
        print(getdata,'datat')
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        # getdata['time_taken'] = time_taken

    if mode['mode'] == "detailed_view":
        getdata = towerdata.Tower_View().detailed_view(
            casename['casename'], casetype['casetype'], user['user'])
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}


    if mode['mode'] == "singlecase":
        getdata = towerdata.Tower_View().signlecase(
            casename['casename'], casetype['casetype'], itemsper_page['itemsper_page'], pagenumber['pagenumber'], user['user'])
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}

    if mode['mode'] == "imeisummary":
        getdata = towerdata.Tower_View().tower_imei(
            casename['casename'], casetype['casetype'], user['user'])
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}

    if mode['mode'] == "bparty":
        case_name = casename['casename']
        case_type = casetype['casetype']
        getdata = towerdata.Tower_View().matched_bparty_contact(
            case_name, case_type, user['user'])
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':getdata.get('message','')}})
    return jsonify(getdata)


@cdr_bp.route("/getvalue", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def numberValue(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/getvalue','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/getvalue'})
    number = flask.request.get_json('number')
    towerval = getcdrdata.Cdr_Analysis().tower_profile(number['number'])
    # towerval = towerdata.Tower_View().tower_profile(number['number'])
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    towerval['time_taken'] = time_taken

    print(towerval, "================")
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':towerval.get('message','')}})

    return jsonify(towerval)


@cdr_bp.route("/cell_tower", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def towermap(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    print("in tower map function")
    data = flask.request.get_json()
    print(data)
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':"/cell_tower",'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})

    response = towerdata.Tower_View().get_tower_analysis(data)
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


@cdr_bp.route('/get_common_link', methods=['POST'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def get_common_and_grouped_data(current_user):
    value = request.json
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    # numbers = value['numbers']
    # selected_date = value.get('date', '')
    # print(numbers,selected_date,"------first------")
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/get_common_link','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/get_common_link'})
    response = towerdata.Tower_View().common_link(value)
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})
        
    return jsonify(response)


@cdr_bp.route('/redflagidentifier', methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def getredflag(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/redflagidentifier','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/redflagidentifier'})
    
    username = flask.request.get_json('username')
    response = redflag.tower_track()
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})
    
    return jsonify(response)


@cdr_bp.route('/updateredflag', methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def redflagupdate(current_user):
    flagtype = flask.request.get_json('flagtype')
    flagid = flask.request.get_json('flagid')
    value = flask.request.get_json('value')
    print(flagid, flagtype, value, "-------")
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/updateredflag','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/updateredflag'})
    response = redflag.update_redflag(
        flagtype['flagtype'], flagid['flagid'], value['value'])
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


@cdr_bp.route('/getredflags', methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def getredglagdata(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/getredflags','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/getredflags'})

    flagtype = flask.request.get_json('flagtype')
    response = redflag.getdata(flagtype['flagtype'])

    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken

    print(response)
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})
    
    return jsonify(response)


@cdr_bp.route("/getnotifications", methods=['POST', "GET"])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def getnotifications(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
    # in here data is return of a function
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':"/getnotifications",'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':"/getnotifications"})
    response = redflag.getnotify()
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


@cdr_bp.route("/bookmarkdata", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def bookmarkdata(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})
    
    data = flask.request.get_json()
    response = towerdata.Tower_View().bookmarkdata(data)
    print(response)
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify({'status': 'SUCESSFULL','time_taken':time_taken})
    # return jsonify('SUCESSFULL')

@cdr_bp.route('/dashboardcounts', methods = ['GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def cdrcounts(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/dashboardcounts','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/dashboardcounts'})
   
    count_result = dashboardcount.Cdr_Analysis().cdrcounts()
    print(type(count_result),"?????")
    res_toc = time.time() - tic
    # time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    # response['time_taken'] = time_taken
    mongothunder.userlogs.update_one({'username':current_user.get('email','unknown'),'fuuid':fuuid,},{'$set':{'endtime':res_toc}})
    return count_result

@cdr_bp.route('/dashboardCount',methods=["POST","GET"])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def dashboardCount(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/dashboardCount','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/dashboardCount'})

    start_time = time.time()
    aggStart = time.time() - start_time
    # print(list(VoipCalls.objects()))
    voip_count = list(VoipCalls.objects().aggregate([{"$count":"VoipCount"}]).__dict__['_CommandCursor__data'])
    VoipCount = voip_count[0]["VoipCount"] if voip_count else 0
    matched_count = list(MatchedCalls.objects().aggregate([{"$count":"MatchedCount"}]).__dict__['_CommandCursor__data'])
    MatchedCount = matched_count[0]["MatchedCount"] if matched_count else 0
    raw_data_count = list(RawData.objects().aggregate([{"$match":{"$and":[{"vpn":{"$exists":True}},{"vpn":{"$ne":""}}]}},{"$count":"TotalCount"}]).__dict__['_CommandCursor__data'])
    RawdataCount = raw_data_count[0]["TotalCount"] if raw_data_count else 0
    aggEnd = time.time() - aggStart

    voipAppsdetails = list(VoipCalls.objects().aggregate([{"$group":{"_id":{"vendor":"$vendor"},"count":{"$sum":1}}}]).__dict__["_CommandCursor__data"])
    Totalapps = [obj["_id"]["vendor"] for obj in voipAppsdetails]
    Totalapp_count = [obj["count"] for obj in voipAppsdetails]

    TotalTime = time.localtime(aggEnd-start_time).tm_sec
    print(Totalapps,Totalapp_count,VoipCount,MatchedCount,RawdataCount)
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response = {"AggStart":time.localtime(start_time).tm_sec,"AggEnd":time.localtime(aggEnd).tm_sec,"VoipCount":VoipCount,"MatchedCount":MatchedCount,"VPNCount":RawdataCount,"Apps":Totalapps,"AppVoipCount":Totalapp_count,"TotalTime":TotalTime,'time_taken' : time_taken}
    mongothunder.userlogs.update_one({'username':current_user.get('email','unknown'),'fuuid':fuuid,},{'$set':{'endtime':res_toc}})

    return jsonify(response)

@cdr_bp.route('/daylocation', methods = ['GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def day_mapping(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/daylocation','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/daylocation'})
   
    matching_documents = cdat_collection.cdrdata.find()

    day_tower_data = {}
    night_tower_data = {}
    data = ''
    
    sdr_match = cdat_collection.sdrdata.find_one({"source_number":data})
    nickname = sdr_match.get('nickname', '') if sdr_match else ''

    user_address = sdr_match['local_address'] if sdr_match else ''
    # Extract the data for each matching document
    for document in matching_documents:
        tower_id = document['first_cgid']
        # address = document['first_cgid_address']
        # latitude = document['lat']
        # longitude = document['long']
        timestamp = document['timestamp']
        call_type = document['incoming']

        # Convert the timestamp to a datetime object
        datetime_obj = datetime.fromtimestamp(timestamp / 1000)

        # Check if the time is within the day mapping range (6 AM to 6 PM)
        if 6 <= datetime_obj.hour < 18:
            if call_type in [1,0]:
                if tower_id not in day_tower_data:
                    day_tower_data[tower_id] = {
                        'total_calls': 0,
                        # 'latitude': latitude,
                        # 'longitude': longitude,
                        # 'address': address,
                    }
                day_tower_data[tower_id]['total_calls'] += 1
                
        datetime_obj = datetime.fromtimestamp(timestamp)

        if datetime_obj.hour >= 18 or datetime_obj.hour < 6:
            if call_type in [1,0]:
                if tower_id not in night_tower_data:
                    night_tower_data[tower_id] = {
                        'total_calls': 0,
                        # 'latitude': latitude,
                        # 'longitude': longitude,
                        # 'address': address,
                    }
                night_tower_data[tower_id]['total_calls'] += 1      
        
        
    
        
    # Sort the tower data for day by call count in descending order
    sorted_day_tower_data = sorted(day_tower_data.items(), key=lambda x: x[1]['total_calls'], reverse=True)
    sorted_night_tower_data = sorted(night_tower_data.items(), key=lambda x: x[1]['total_calls'], reverse=True)

    # Prepare the data for the top 10 towers for day
    top_10_day_towers = []
    night_towers = []
    
    for tower_id, datas in sorted_day_tower_data:
        tower = {
            'nickname':nickname,
            'user_address': user_address,
            'source_number': data,
            'tower_id': tower_id,
            # 'address': datas['address'],
            'total_calls': datas['total_calls'],
            # 'latitude': datas['latitude'],
            # 'longitude': datas['longitude']
        }
        top_10_day_towers.append(tower)

    for tower_id, datas in sorted_night_tower_data:
        tower = {
            'Phone': data,
            'nickname':nickname,
            'user_address': user_address,
            'source_number': data,
            'tower_id': tower_id,
            # 'address': datas['address'],
            'total_calls': datas['total_calls'],
            # 'latitude': datas['latitude'],
            # 'longitude': datas['longitude']
        }
        night_towers.append(tower)
       


    total_day_count = len(top_10_day_towers)
    total_night_count = len(night_towers)

    response = {
 
        'daycount' : total_day_count,
        'nightcount':total_night_count,
    }

    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken

    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return response




@cdr_bp.route("/tower_lookup", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def tower_lookup(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]

    data = flask.request.form.get("number")
    mode = flask.request.form.get("mode")
    sd = flask.request.form.get("fromdate")
    ed = flask.request.form.get("todate")
    items = flask.request.form.get('items_per_page')
    currentpage = flask.request.form.get('page')
    req_toc = time.time() - tic
    print(data, mode, items, currentpage, "data")
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})

    if mode == "source" or mode == "destination" or mode == "imei":
        print(data, mode, items, currentpage, "cdr_details")
        response = towerdata.Tower_View().call_details(
            data, mode, sd, ed, items, currentpage)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
        return jsonify(response)
    
    if mode == "imeisummary":
        response = towerdata.Tower_View().imei_summary(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    
        return jsonify(response)
    if mode == "phonesummary":
        response = towerdata.Tower_View().phone_summary(data)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)
