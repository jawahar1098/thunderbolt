# Imports.
import datetime
import os
import pymongo
import uuid
import werkzeug.security
from MongoClinet import thunderbolt
mongocli = thunderbolt()

class UserManagement:
    """
    Perform user related functions to serve the API.
    """

    def __init__(self):

        # MongoDB initialisation.
        
        
        # Attach the required collections to the class.
        self.users = mongocli.users
        

    def user_count(self):
        """
        Get the number of registered users.

        :return int: number of registered users.
        """

        # If "users" collection is non existent, no users exist.
        if "users" not in mongocli.list_collectons:
            return 0

        # Otherwise return a count of documents(users) in the collection.
        return self.users.count_documents({})


    def get_users(self):
        """
        Get information of all registered users.

        :return list: list of registered users.
        """

        # Track the list of registered users.
        registered_users = list()

        # Iterate over all users.
        for registered_user in self.users.find({"username": {"$exists": True}}, {"_id": False, "password": False}):
            
            # Convert the timestamp to a string for user-friendly display on the dashboard.
            registered_user["created_at"] = datetime.datetime.fromtimestamp(registered_user["created_at"]).strftime("%d %B %Y, %H:%M:%S")
            
            # Add this user to the store.
            registered_users.append(registered_user)

        # Find the collection in the config where the configured roles exist.
        # roles = self.config_collection.find_one({"roles": {"$exists": True}})["roles"]
        roles = []
        return {"users": registered_users, "roles": roles}


    def register_user(self, user_data):
        print(user_data ,"userdata")
        """
        Register a new user.

        :param user_data dict: receive information about a user for the registration.
        """

        # Store the hashed password in the database.
        user_data["password"] = werkzeug.security.generate_password_hash(user_data["password"], method = "sha256")
        
        # Generate a random UUID for the new user.
        user_data["user_id"] = str(uuid.uuid1())

        # The user is active by default.
        user_data["status"] = True

        # Current user's creation time.
        user_data["created_at"] = datetime.datetime.now().timestamp()

        # Initialise user bookmarks with empty fields.
        user_data["bookmarks"] = []

        


        # Check if a user exists witth the same username.
        user_check = self.users.find_one({"email": user_data["email"]})
    
        # If a user does not exist, accept the registeration request adn return the user ID.
        if not user_check:
            print()
            self.users.insert_one(user_data)
            return user_data["user_id"]
        
        # Otherwise return None.
        else:
            return None


    def check_user(self, user_id):
        """
        Check if a user is registered.

        :param user_id str: User ID that belongs to a user.
        :return string: username corresponding to the user ID.
        """

        # Return the information corresponding to the specified user ID.
        return self.users.find_one({
            "user_id": user_id
            }, {
                "user_id": user_id,
                "email": True,
                # "role": True
            }
        )


    def login_user(self, login_data):
        """
        Validate a login attempt matching the username and password.

        :param user_id str: User ID that belongs to a user.
        """
        # print(mongocli.list_collectons)
        print(login_data,"pppp",login_data["email"])
        # Fetch the user corresponding to the passed username.
        result = mongocli.users.find_one({
            "email": login_data["email"]
            # ,"logged": "0"
            })
        print(result)
        # If a user matching the user ID is found, check the password.
        if result:
            # If the username and password match, return the role and the user ID.
            # if (result["email"] == login_data["email"]):
            #     return { "user_id": str(uuid)}

            # Otherwise return None.

            alll = []
            collection = self.users
            all_user = collection.find({'team':"CAT", 'role':"Analyst"})
            for all in all_user:
                    alll.append({"officername":all["officername"]})
            print(result,"========================")
            if result['password1'] == login_data['password'] and result["status"] == "Active":
                userDetails = {
                    "designation": result['designation'],
                    "officername": result['officername'],
                    'password':result['password1'],
                    "email": result["email"],
                    "team": result["team"],
                    "modules": result["modules"],
                    "superior": result["superior"],
                    "role":result["role"],
                    'user_id' :  result['user_id'],
                    "ALL" : alll,
                    'user_id': result['user_id'],
                    'Model' : result['Application']
                }
                return { "user_id": result['user_id'],'userdata':userDetails}
            else:
                return None
        # Otherwise return None.
        return None


    def update_user(self, update_data):
        """
        Update the data of a user.

        :param update_data dict: get the updation data.
        """

        result = None
        user_id = update_data.get("user_id", None)
        action = update_data.get("action", None)

        # Proceed with if an action is specified with a user ID.
        if user_id and action:

            # Create a filter with the user ID.
            filter_string = {"user_id": update_data["user_id"]}

            # Toggle the active state of the user.
            if action == "activate":

                status = update_data.get("state", None)

                if status is not None:
                    
                    result = self.users_collection.update_one(
                        filter_string,
                        update = {
                            "$set": {
                                "status": status
                            }
                        },
                        upsert = False
                    )

            # Delete the user.
            elif action == "delete":

                user_details = self.check_user(user_id)

                if user_details["role"] == "Super Administrator":
                    return result


                result = self.users_collection.delete_one(filter_string)

            # Update bookmark for user.
            elif action == "bookmark":

                status = update_data.get("state", None)
                file_id = update_data.get("file_id", None)

                if status is not None and file_id is not None:

                    if status:

                        result = self.users_collection.update_one(
                            filter_string,
                            update = {
                                "$push": {
                                    "bookmarks": file_id
                                }
                            },
                            upsert = True
                        )
                    
                    else:

                        result = self.users_collection.update_one(
                            filter_string,
                            update = {
                                "$pull": {
                                    "bookmarks": file_id
                                }
                            },
                            upsert = False
                        )

            return result


    def get_bookmarks(self, user_id):
        """
        Get the bookmarks for a particular user.

        :param user_id str: user ID of the user whose bookmarks are to be fetched.
        :return list: list of file IDs that have been bookmarked by the user.
        """

        bookmarks = self.users_collection.find_one({"user_id": user_id}, {"bookmarks": True, "_id": False})

        return bookmarks
    

    