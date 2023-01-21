import hashlib
import os
from django.http import HttpResponse
import  pandas
from django.core.serializers.json import DjangoJSONEncoder 
from django.views.decorators.csrf import csrf_exempt
import json
from pymongo import MongoClient
import pymongo
from ..Configs.Config import config
from bson.timestamp import Timestamp
from datetime import datetime
from ..FileStore import hashPassword

@csrf_exempt
def register_user(request):

    prevUserID=None
    currentUserId=None
    result={}
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body['name']   
        password = body['password']
        email = body['username']

    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the MongoDB database...')
 
        mongodb_host=params['mongodb_host'].replace("'", "")
        mongodb_port=int(params['mongodb_port'])    
        db_name=params['db_name'].replace("'", "")

        connection = MongoClient(mongodb_host, mongodb_port)
        collection = connection[db_name]['UserDetails']  


        user = collection.find_one({"userEmail": email})
        if user:
            result['msg']='username and mail id already present  ! please make another one or try again!'
            return HttpResponse(json.dumps(result),content_type="application/json")
        else:
            
            LastUserData=collection.find().sort("userID", -1).limit(1)
            for val in LastUserData:
                prevUserID=val['userID']
            currentUserId= prevUserID + 1

            timeStamp=datetime.now()

            role=0
            salt = hashPassword.salt
            hashPassWord = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            
            collection.insert_one({"userName":username,
                                    "userEmail":email,
                                    "passWord":hashPassWord,
                                     "userID":currentUserId,
                                     "timeStamp":timeStamp,
                                     "role":role})

            result['status']='success'
            result['msg']='User Registered Successfully'
            return HttpResponse(json.dumps(result),content_type="application/json")

    except Exception as ex :

        print(ex)
        error= ex
        result['status']='failed'
        result['msg']=ex

        return HttpResponse(json.dumps(result),content_type="application/json")

               