from flask import Flask, request, url_for, redirect, render_template, flash, abort, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import flask_cors
import flask 
from flask_wtf import FlaskForm
from loguru import logger
import functools
from functools import wraps
import jwt
import datetime
import time
import uuid
from MongoClinet import VIGOR, NEXUS
from MongoClinet import thunderbolt as mongoticket


from . import auth_handle
user_management = auth_handle.UserManagement()

from app.auth import auth
cors_allowed_ip = "*"

db = mongoticket().db



# ---------- JWT ---------- #

# JWT token blacklist.
jwt_blacklist = dict()

# JWT authentication decorator function.
def token_required(f):
    """
    Declare and define a decorator to verify the validity of a JWT token, if present, in the request.
    """

    # Wrapper to maintain the original identity of the function over which the decorator is applied.
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # JWT is passed in the request header.
        data = flask.request.headers
        # print(data,"----------flask data----")
        # Attempt JWT validation.
        try:
            if "Authorization" in flask.request.headers:
                token = data["Authorization"].split(' ')[-1]

            # Return 401 if token is not passed.
            if not token or token in jwt_blacklist:
                # Log the request with anonymous user information.
                logger.info(f"Endpoint hit by anonymous user")
            
                # Get the IP address of the client.
                ip_address = flask.request.remote_addr

                # Insert the log document into the MongoDB collection.
                log_document = {
                    "email": "anonymous",
                    "endpoint": flask.request.endpoint,
                    "method": flask.request.method,
                    "timestamp": datetime.datetime.now(),
                    "ip_address": ip_address,
                    "authentication": "failure"
                }
                user_management.users_log.insert_one(log_document)
                return flask.jsonify({"message": "failure on token///"}), 401
            # Decoding the payload to fetch the stored details.
            try:
                print("inside")
                data = jwt.decode(token, 'lihftbasdfcfasd', algorithms = "HS256")
                print(data,"-----data in user check----")
                current_user = user_management.check_user(data["user_id"])
                # expired_tokens = list()

                # # If any blacklisted tokens have expired, remove them from the blacklist.
                # for key, value in jwt_blacklist.items():
                #     if time.time() > value:
                #         expired_tokens.append(key)
                # for expired_token in expired_tokens:
                #     jwt_blacklist.pop(expired_token, None)
                # print(expired_tokens)
                # if expired_tokens:
                #     return flask.jsonify({"message":"session closed"}),401

            # Invalid token shall be denied.
            except Exception as exception:
                print(exception,"-------------------------")
                if exception == "Signature has expired":
                    return flask.jsonify({"message": f"{exception}....."}), 440
                else:
                    return flask.jsonify({"message": f"failure on exception for 00 {exception}"}), 440
            # Log the request with the current user information.
            logger.info(f"Endpoint hit by user {current_user}")
            
            # Get the IP address of the client.
            ip_address = flask.request.remote_addr
            user_agent = flask.request.user_agent.string

            # Insert the log document into the MongoDB collection.
            log_document = {
                "email": current_user["email"],
                "endpoint": flask.request.endpoint,
                "method": flask.request.method,
                "timestamp": datetime.datetime.now(),
                "ip_address": ip_address,
                "user_agent": user_agent
            
            }
            # user_management.users_log.insert_one(log_document)
            # Returns the current logged in users contex to the routes.
            return f(current_user, *args, **kwargs)
        # Invalid token shall be denied.
        except Exception as exception:
            print("here", exception)
            return flask.jsonify({"message": "failure on exception token"}), 401   
            
    return decorated 





# ---------- Session Management ---------- #

@auth.route("/loginapi", methods = ["POST", "OPTIONS"])
@flask_cors.cross_origin(origin = cors_allowed_ip, supports_credentials = True)
def login():
    """
    Handle login functionality at "/login" endpoint.

    :param origin list: list of allowed IP addresses as per CORS policy.
    :param supports_credentials bool: to match the "include_credentials" header.
    """

    # Dereference the credentials in the request body.
    admin_email = 'super@gmail.com'
    admin_password = '123'

    data = flask.request.json
    print(data)
    email = data.get("email", None)
    password = data.get("password1", None)
    
    print(email, password,"==")
    
    # Check if the provided credentials match the administrator credentials
    if email == admin_email and password == admin_password:
        userDetails = {
            "name": "Super",
            "email": email,
            "password1": password,
            "password2": "123",
            "mobilenumber": "9637645941",
            "designation": "Administrator",
            "officername": "Super Admin",
            "question": "What's the name of the first school you attended?",
            "answer": "123",
            "status": "Active",
            "Model" : '',
            "userid": "5e3423wsgfwq3452345",#str(uuid.uuid1())
            # "logged": "0",
        }

        

        token = jwt.encode({
                    "user_id": userDetails["userid"],
                    # "role": login_success_user_info["role"],
                    # "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes = 60)
                },
                "lihftbasdfcfasd",
                "HS256"
            )
        print(token,    {"message": "success", "access_token": token,'userdata':userDetails})
        # return flask.make_response(flask.jsonify({"message": "success", "access_token": token,'userdata':userDetails})), 200
        return flask.make_response(flask.jsonify({"message": "success", 'userdata':userDetails})), 200
            # If both username and password have been provided, proceed further.
    if email and password:

        # Check the number of registered users.
        # registered_users_count = user_management.user_count()

        
        print(email, password)
        login_success_user_info = user_management.login_user({
                "email": email,
                "password": password,
            })
        # print(login_success_user_info, "---===========================")
        # If the credentials were correct.
        if login_success_user_info:

            token = jwt.encode({
                    "user_id": login_success_user_info["user_id"],
                    # "role": login_success_user_info["role"],
                    # "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes = 60)
                },
                "lihftbasdfcfasd",
                "HS256"
            )

            # inserting new field
            # collection = db['users']
            # collection.update_one({'email': email}, {'$set': {'logged': '1'}})

            # print(token)
            # return flask.make_response(flask.jsonify({"message": "success", "access_token": token,'userdata':login_success_user_info['userdata']})), 200
            return flask.make_response(flask.jsonify({"message": "success","access_token":token,'userdata':login_success_user_info['userdata']})), 200
        
        else:
            print("no users")

            return flask.make_response(flask.jsonify({"message": "no_cred"}))
    
    else:
        print('unauthorized')
        return flask.make_response(flask.jsonify({"message": "failure"})), 400
    

@auth.route("/user", methods = ["GET", "OPTIONS"])
@flask_cors.cross_origin(origin = cors_allowed_ip, supports_credentials = True)
@token_required
def user(current_user):
    """
    Verif
     the validity of the token for a logged-in user. Serves as an extra check at every page of the app.
    """
    print("-------",current_user)
    email = current_user['email']
    # This will execute only if the token was valid, since token validation is present at this endpoint. Hence, simply return a success response.
    return flask.make_response(flask.jsonify({"message": "success", "email": email, "user_id": current_user["user_id"], "authorized": True})), 200


# -------------------------------------------------------------------------------------------------------------------------------------------
# @auth.route('/updateuser', methods=['GET','POST'])
# @flask_cors.cross_origin(origin = cors_allowed_ip, supports_credentials = True)
# @token_required
# def update_user():
#     data = request.json
#     id = data.get('id')
#     # print(id)

#     # Retrieve the user with the provided email from the database
#     user =  Users.objects_safe(id = id).first()
#     # print(user)
#     if user:
#         # Update the user fields with the edited data
#         user.name = data.get('name')
#         user.email = data.get('email')
#         user.mobilenumber = data.get('mobilenumber')
#         user.password1 = data.get('password1')
#         user.password2 = data.get('password2')
#         user.designation = data.get('designation')
#         user.officername = data.get('officername')
#         user.team = data.get('team')
#         user.modules = data.get('modules')
#         user.status = data.get('status')
#         user.superior = data.get('superior')
#         user.role = data.get('role')
#         # Save the changes to the database
#         user.save()

#         return jsonify({'message': 'User details updated successfully'})
#     else:
#         return jsonify({'message': 'User not found'})
    
    
@auth.route("/register", methods = ["GET", "OPTIONS", "POST"])
@flask_cors.cross_origin(origin = cors_allowed_ip, supports_credentials = True)
# @token_required
def  register():
        print('in register python')
        if request.method == "POST":
            password1 = request.json.get("password1"),
            password2 = request.json.get("password2"),
            user_found = user_management.users.find_one({'name':request.json.get("name")})
            email_found = user_management.users.find_one({'email':request.json.get("email")}) #Users.objects_safe(email = request.json.get("email"))
            superior = request.json.get("superior")
            selected_apps = request.json.get("Model")
            apps_string = selected_apps # ', '.join(selected_apps) if selected_apps else None
            if superior == "":
                super1 = "Top Superior"
            else:
                super1 = request.json.get("superior")
            
            # modules = request.json.get("modules")
            # if modules == "":
            #     module = "---"
            # else:
            #     module = request.json.get("superior")
            

            if user_found:
                # message = 'There already is a user by that name'
                return jsonify({'message': 'There already is a user by that name'})
            if email_found:
                # message = 'This email already exists in database'
                return jsonify({'message': 'This email already exists in database'})
            if password1 != password2:
                # message = 'Passwords should match!'
                return jsonify({'message': 'Passwords should match!'})
            else:
                # hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
                user_management.users.insert_one({
                                    "name": request.json.get("name"),
                                    "email": request.json.get("email"),
                                    "password1": request.json.get("password1"),
                                    "password2": request.json.get("password2"),
                                    "mobilenumber": request.json.get("mobilenumber"),
                                    "designation": request.json.get("designation"),
                                    "officername": request.json.get("officername"),
                                    "team": request.json.get("team"),
                                    "modules": request.json.get("modules"),
                                    "role": request.json.get("role"),
                                    "superior": super1,
                                    'status':"Active",
                                    "Application":apps_string,
                                    "user_id": str(uuid.uuid1()) ,
                                    "logged":"0"              
               
                })

                # user_management.users.save()
                # registration = request.get_json()   
                designation_mapping = {
                    'IG': 'SuperAdmin',
                    'DIG': 'SuperAdmin',
                    'SP': 'Admin',
                    'DSP': 'Admin',
                    'INSPR': 'Admin',
                    'SI': 'User',
                    'ASI': 'User',
                    'HC': 'User',
                    'PC': 'User'
                }
                mapped_designation = designation_mapping.get(request.json.get("designation"))
                print(apps_string,"================appp string")
                if "VIGOR" in apps_string:
                    current_time = datetime.datetime.now()
                    new_user = {
                    'name' : request.json.get("name"),
                    'email' : request.json.get("email"),
                    'designation' : mapped_designation,
                    'adminname' : request.json.get("officername"),
                    'username' : request.form.get('username'),
                    'assigned_phone_no' : request.json.get("mobilenumber"),
                    'status' : 'Active',
                    'password' :request.json.get("password1"),
                    'created_at': current_time,
                    "user_id": str(uuid.uuid1())               

                    }
                    VIGOR().db['ACCOUNTS'].insert_one(new_user)
                if "NEXUS" in apps_string:
                    current_time = datetime.datetime.now()
                    new_user = {
                    'name' : request.json.get("name"),
                    'email' : request.json.get("email"),
                    'designation' : mapped_designation,
                    'adminname' : request.json.get("officername"),
                    'username' : request.form.get('username'),
                    'assigned_phone_no' : request.json.get("mobilenumber"),
                    'status' : 'Active',
                    'password' :request.json.get("password1"),
                    'created_at': current_time,
                    "user_id": str(uuid.uuid1()) 
                    }
                    NEXUS().db['accounts'].insert_one(new_user)
                    
                # print(registration)
                # Collection1.insert_one(registration)
        return jsonify({'message': 'Registration successful'})

@auth.route('/logout_api', methods=['GET','POST'])
@flask_cors.cross_origin(origin = cors_allowed_ip, supports_credentials = True)
@token_required
def logout_api(current_user):
    logout_user()
    return jsonify({'message':'logout'})


#-------------------- end ----------------#



