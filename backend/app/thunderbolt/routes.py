from app.thunderbolt import thunder_bp
from flask import request,jsonify
from app.thunderbolt.lib.maindashboard import *
import time






@thunder_bp.route('/add_numbers', methods=['POST', 'GET'])
def add_numbers():
    print("inside the addnumbers")
    tic = time.time()
    print(tic)
    # print(request.get_json('data'),"============")
    data = request.get_json('data')
    req_toc = time.time() - tic
    response = add_intresred_numbers(data['user'],data['numbers'].split(","))
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    return jsonify(response)


@thunder_bp.route('/map_data',methods=['POST','GET'])
def map_data():
    print('inside')
    tic = time.time()
    print(tic)
    # print(request.get_json('data'),"============")
    data = request.get_json('data')
    print(data)
    # print(data['user'])
    req_toc = time.time() - tic
    response = map_numbers(data['user'])
    res_toc = time.time() - tic
    time_taken = {"received_at": tic, "first": req_toc, "res": res_toc}
    response['time_taken'] = time_taken
    return jsonify(response)


@thunder_bp.route('/getnotificaions', methods = ['POST','GET'])
def getnotificaions():
    notification_count = mongocdat.notification.count_documents({'read':'0'})
    response = {'notificationcount':notification_count,'status':'sucess'}
    return response