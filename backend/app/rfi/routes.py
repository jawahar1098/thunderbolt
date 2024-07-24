from app.rfi import rfi_bp
from flask import request,jsonify
from app.rfi.lib.rfi import getnotify,updateseenrfi
from MongoClinet import CDAT
from app.auth.routes import token_required
import flask_cors

cors_allowed_ip = "*"

mongocdat = CDAT()




@rfi_bp.route('/notificationscount', methods = ['POST'])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def getnotificaions(current_user):
    print("get notifications ========================",current_user)
    username = request.form.get('user')
    print(username,"==========++++++++++++++++++++++++++++++===========================++++++++++++++++++++++++++======")
    notification_count = mongocdat.notification.count_documents({'seen':'0','user':username})
    response = {'notificationcount':notification_count,'status':'sucess'}
    return response




@rfi_bp.route("/getnotifications", methods=['POST', "GET"])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def getnotifications(current_user):
    user = request.form.get('user')
    data = getnotify(user)
    return jsonify(data)



@rfi_bp.route("/updateseen", methods=['POST', "GET"])
@flask_cors.cross_origin(origin=cors_allowed_ip, supports_credentials=True)
@token_required
def updateseen(current_user):
    print(request.form)
    rfid = request.form.get('rfid')
    user = request.form.get('user')
    data = updateseenrfi(rfid,user)
    print('resfsgfsdgaergesg')
    return jsonify(data)