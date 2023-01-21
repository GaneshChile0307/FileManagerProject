import hashlib
import os
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder 
from django.views.decorators.csrf import csrf_exempt
import json
from pymongo import MongoClient
import pymongo
from ..Configs.Config import config
from bson.timestamp import Timestamp
import datetime as dt
from ..FileStore import hashPassword

@csrf_exempt
def DeleteFileRequestToAdmin(request):
    # print(request.DELETE)
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        reqId = body['requestId']  

    result={}
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the MongoDB database...')
 
        mongodb_host=params['mongodb_host'].replace("'", "")
        mongodb_port=int(params['mongodb_port'])    
        db_name=params['db_name'].replace("'", "")

        connection = MongoClient(mongodb_host, mongodb_port)
        collection = connection[db_name]['AdminFileRequest']  
        
        collection.delete_one({"reqID":int(reqId)})

        result['status']='success'
        result['msg']='Request Entry Deleted Successfully'
        return HttpResponse(json.dumps(result),content_type="application/json")

    except Exception as ex :

        print(ex)
        error= ex
        result['status']='failed'
        result['msg']=ex

        return HttpResponse(json.dumps(result),content_type="application/json")
