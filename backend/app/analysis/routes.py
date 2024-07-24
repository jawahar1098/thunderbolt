import os
import flask
from flask import *
from app.analysis.lib import tower_analysis as tower
from app.analysis.lib import tower as towerdata
from app.analysis.lib import rfi as redflag
from app.analysis import analysis_bp
from app.analysis.lib import maindashborad
import time
import flask_cors
from app.auth.routes import token_required
from datetime import datetime
from MongoClinet import thunderbolt

mongothunder = thunderbolt()


cors_allowed_ip = "*"


# ------------------------------------Tower Analysis-----------------------------------#
@analysis_bp.route("/tower_analysis", methods=['POST'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def tower_analysis(current_user):
    # print("WECLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    key_location = flask.request.form.get("key_location")
    sitename = flask.request.form.get("sitename")
    fromdate = flask.request.form.get("fromdate")
    todate = flask.request.form.get("todate")
    mode = flask.request.form.get("mode")
    numbers = flask.request.form.get("numbers")
    lat = flask.request.form.get('lat')
    long = flask.request.form.get('long')
    radius = flask.request.form.get('radius')
    # phone_numbers = flask.request.form.get("phone_numbers")
    print(fromdate, todate, "-------------------------------------")

    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/tower_analysis'})
   
    response = []
    if mode == "same_site":
        response = tower.Tower_View().within_tower(
            key_location, sitename, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "common_source" or mode == "common_destination":
        response = tower.Tower_View().common_numbers_in_different_towers(
            mode, key_location, sitename, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "common_imei":
        response = tower.Tower_View().common_imei_in_different_towers(
            key_location, sitename, fromdate, todate)
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
            numbers, key_location, sitename)  # , fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "internal_calling":
        response = tower.Tower_View().internal_calling(sitename, key_location)
        # print(response,"RESSSSSSSSSSSSSSSSSSSSSSSSSS")
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "unique_tower_counts":
        response = tower.Tower_View().tower_details()
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "call_details":
        response = tower.Tower_View().call_details(sitename)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "day_wise_analysis":
        response = tower.Tower_View().day_wise_analysis(sitename, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "summary":
        response = tower.Tower_View().summary(numbers)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "under_tower_calls":
        response = tower.Tower_View().calls_under_tower(
            key_location, sitename, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "different_tower":
        response = tower.Tower_View().different_towers(
            sitename, key_location, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "location_time":
        response = tower.Tower_View().location_time(
            sitename, key_location, fromdate, todate)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "tower_group_creation":
        response = tower.Tower_View().tower_groups_location_time(lat, long, radius)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "summary":
        response = tower.Tower_View().summary(numbers)
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


@analysis_bp.route("/tower_analysis_2", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def tower_analysis_two(current_user):
    print("WECLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    inputdata = flask.request.get_json('value')
    print(inputdata, "------------------------------------------")
    mode = inputdata['mode']
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/tower_analysis_2'})
   
    response = []
    if mode == "common_source" or mode == "common_destination" or mode == "common_imei":
        response = tower.Tower_View().common_numbers_in_towers(
            mode, inputdata['value'])
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    # if mode == "common_imei":
    #     response = tower.Tower_View().common_imei_in_different_towers(key_location,sitename,fromdate,todate)
    if mode == "overview":
        response == tower.Tower_View().overview(inputdata['value'])
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    if mode == "formulaone":
        print(inputdata['value'])
        response = tower.Tower_View().aggregate_tower_data(inputdata['value'])
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})
    
    return jsonify(response)


@analysis_bp.route("/tower", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def towersummary(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    print("in tower func")
    coord = flask.request.get_json('coordinates')
    print(coord)
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/tower','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/tower'})
   
    res = towerdata.Tower_View().get_tower_in_polygon(coord)
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    res['time_taken'] = time_taken
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(res)



@analysis_bp.route("/getcasedata", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def getcase(current_user):
    print(request.method, "----------ffffffffffffffffffffffff--------------")
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
   
    if request.method == "GET":
        response = towerdata.Tower_View().casedata()
        res_toc = time.time() - tic
        time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
        response['time_taken'] = time_taken
    

    if request.method == "POST":
        casename = flask.request.get_json('casename')
        casetype = flask.request.get_json('casetype')
        itemsper_page = flask.request.get_json('itemsper_page')
        pagenumber = flask.request.get_json('pagenumber')
        mode = flask.request.get_json('mode')
        print(casename, mode['mode'])
        mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':mode,'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/getcasedata'})
        if mode['mode'] == "singlecase":
            response = towerdata.Tower_View().signlecase(
                casename['casename'], casetype['casetype'], itemsper_page['itemsper_page'], pagenumber['pagenumber'])
            res_toc = time.time() - tic
            time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
            response['time_taken'] = time_taken
        if mode['mode'] == "imeisummary":
            response = towerdata.Tower_View().tower_imei(
                casename['casename'], casetype['casetype'])
            res_toc = time.time() - tic
            time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
            response['time_taken'] = time_taken
        if mode['mode'] == "bparty":
            response = towerdata.Tower_View().matched_bparty_contact(
                casename['casename'], casetype['casetype'])
            res_toc = time.time() - tic
            time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
            response['time_taken'] = time_taken
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


# @analysis_bp.route("/getvalue", methods=['POST', 'GET'])
# def numberValue():
#     number = flask.request.get_json('number')
#     towerval = getcdrdata.Cdr_Analysis().tower_profile(number['number'])
#     # towerval = towerdata.Tower_View().tower_profile(number['number'])
#     print(towerval,"================")
#     if len(towerval) == 0:
#         val = "Nodata"
#     else:
#         val = towerval[0]
#     return jsonify({'towerpro':val})

@analysis_bp.route('/get_common_link', methods=['POST'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def get_common_and_grouped_data(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/get_common_link','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/get_common_link'})

    numbers = flask.request.get_json('numbers')
    selected_date = flask.request.get_json('date')
    response = towerdata.Tower_View().common_link(
        numbers['numbers'], selected_date['date'])
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})
        
    return jsonify(response)


@analysis_bp.route('/redflagidentifier', methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def getredflag(current_user):
    username = flask.request.get_json('username')
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/redflagidentifier','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/redflagidentifier'})
   
    response = redflag.tower_track()
    
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


@analysis_bp.route('/updateredflag', methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def redflagupdate(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/updateredflag','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/updateredflag'})
   
    flagtype = flask.request.get_json('flagtype')
    flagid = flask.request.get_json('flagid')
    value = flask.request.get_json('value')
    print(flagid, flagtype, value, "-------")
    response = redflag.update_redflag(
        flagtype['flagtype'], flagid['flagid'], value['value'])
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


@analysis_bp.route('/getredflags', methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def getredglagdata(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/getredflags','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':'/getredflags'})
   
    flagtype = flask.request.get_json('flagtype')
    response = redflag.getdata(flagtype['flagtype'])
    print(getdata)
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


@analysis_bp.route("/getnotifications", methods=['POST', "GET"])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def getnotifications(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':"/getnotifications",'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':"/getnotifications"})
   
    response = redflag.getnotify()
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)


@analysis_bp.route("/formulaOneexport", methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def formulaexport(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':"/formulaOneexport",'starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':"/formulaOneexport"})
   
    print(':iuuuuuuuuuuuuuuasid;f')
    csname = flask.request.get_json('csname')
    cstype = flask.request.get_json('cstype')
    user = flask.request.get_json('user')
    print(csname['casename'], cstype)

    filepath, filename = towerdata.Tower_View().create_excel(
        csname['casename'], cstype['casetype'], user['user'])
    res_toc = time.time() - tic
    
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':''}})

    return send_from_directory(filepath, filename)

@analysis_bp.route('/map_data', methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def map_data(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
   
    print('inside')
    tic = time.time()
    print(tic)
    # print(request.get_json('data'),"============")
    data = request.get_json('data')
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/map_data','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})
    print(data)
    # print(data['user'])
    req_toc = time.time() - tic
    response = maindashborad.map_numbers(data['user'])
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})
    
    return jsonify(response)


@analysis_bp.route('/add_numbers', methods=['POST', 'GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def add_numbers(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
   
    print("inside the addnumbers")
    tic = time.time()
    print(tic)
    # print(request.get_json('data'),"============")
    data = request.get_json('data')
    print(data)
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/add_numbers','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})
    req_toc = time.time() - tic
    response = maindashborad.add_intresred_numbers(data['user'], data['numbers'].split(","))
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})
    
    return jsonify(response)

@analysis_bp.route('/addlbs', methods=['POST','GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def addlbs(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
   
    print("inside the addnumbers")
    data = request.get_json('data')
    print(data)
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/addlbs','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})
    response = maindashborad.add_lbs( data['numbers'].split(","),data['user'],)
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)
    
@analysis_bp.route('/lbstrack', methods = ['POST','GET'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def lbstrack(current_user):
    tic = time.time()
    fuuid = datetime.now().strftime("%d%m%Y%H%M%S%f%z")[:19]
    req_toc = time.time() - tic
   
    data = request.get_json('data')
    mongothunder.userlogs.insert_one({'username':current_user.get('email','unknown'),'mode':'/lbstrack','starttime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'fuuid':fuuid,'source':data})
    response = maindashborad.lbs_loc(data['user'])
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    mongothunder.userlogs.update_one({'fuuid':fuuid},{'$set':{'Quering_time':res_toc,'endtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'message':response.get('message','')}})

    return jsonify(response)
