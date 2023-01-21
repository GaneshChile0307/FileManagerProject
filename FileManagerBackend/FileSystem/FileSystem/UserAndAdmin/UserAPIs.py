from django.http import HttpResponse
import  pandas
from django.core.serializers.json import DjangoJSONEncoder 
from django.views.decorators.csrf import csrf_exempt
import json
from pymongo import MongoClient
from ..Configs.Config import config
import hashlib
import os
from ..FileStore import hashPassword
from bson import json_util
from datetime import datetime

@csrf_exempt
def login_user(request):
    result={}
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body['username']   
        password = body['password']

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

        # user = collection.find_one({},{"userName": username})
        # print(user)
        salt = hashPassword.salt
        correctPassword =  hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)

        userDetails = collection.find_one({"userEmail": username, "passWord": correctPassword})
        if userDetails:
            userDetails =json_util.dumps(userDetails)
            userDetails=json.loads(userDetails)
            userDetails.pop('passWord')
            
            if userDetails:
                result['status']='success'
                result['msg']='logged In'
                result['userdetails']=userDetails
                return HttpResponse(json.dumps(result),content_type="application/json")
            else:
                result['status']='failed'
                result['msg']='access denied'
                return HttpResponse(json.dumps(result),content_type="application/json")
        else:
            result['status']='failed'
            result['msg']='Please type username or password correctly  or please register to login!'
            return HttpResponse(json.dumps(result),content_type="application/json")


    except Exception as ex :

        print(ex)
        error= ex
        result['status']='failed'
        result['msg']=ex

        return HttpResponse(json.dumps(result),content_type="application/json")


def getUserByUserId(request):
   
    result={}
    userId = request.GET.get('userid')
    
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

        userDetails = collection.find_one({"userID": int(userId)})
        userDetails.pop('passWord')
        userRegDate=userDetails['timeStamp']  
        uDate=userRegDate.strftime("%d-%m-%Y")
        userDetails['timeStamp']=uDate

        userDetails =json_util.dumps(userDetails)
        
        if userDetails:
            result['status']='success'  
            result['userDetails']=json.loads(userDetails) 
            return HttpResponse(json.dumps(result),content_type="application/json")
        else:
            result['status']='failed'
            result['msg']='access denied'
            return HttpResponse(json.dumps(result),content_type="application/json")

    except Exception as ex :

        print(ex)
        result['status']='failed'
        result['msg']=ex

        return HttpResponse(json.dumps(result),content_type="application/json")



def getUserFileDataByUserId(request):
    
    result={}
    userId = request.GET.get('userid')

    try:
        # read connection parametsers
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the MongoDB database...')
 
        mongodb_host=params['mongodb_host'].replace("'", "")
        mongodb_port=int(params['mongodb_port'])    
        db_name=params['db_name'].replace("'", "")

        connection = MongoClient(mongodb_host, mongodb_port)
        collection = connection[db_name]['FileUpload']  

        fileDetails = collection.find({"userID": int(userId)})   

        reqData=[]
        for fq in fileDetails:
            fq.pop('file_content')
            fcd=fq['filecreationDate']
            fud=fq['fileUpdationDate']

            creatDate=fcd.strftime("%d-%m-%Y")
            updateDate=fud.strftime("%d-%m-%Y")

            fq['filecreationDate']=creatDate
            fq['fileUpdationDate']=updateDate

            reqData.append(fq)
            
        reqData =json_util.dumps(reqData)
        reqData=json.loads(reqData)
        df = pandas.DataFrame.from_records(reqData)
        js_data = df.to_json(orient = 'records')
        json_data =json.loads(js_data)
        
        if fileDetails:
            result['status']='success'  
            result['userDetails']=json_data
            return HttpResponse(json.dumps(result),content_type="application/json")
        else:
            result['status']='failed'
            result['msg']='access denied'
            return HttpResponse(json.dumps(result),content_type="application/json")

    except Exception as ex :

        print(ex)
        result['status']='failed'
        result['msg']=ex

        return HttpResponse(json.dumps(result),content_type="application/json")


def getAllUserFileData(request):
    
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
        collection = connection[db_name]['FileUpload']  

        fileDetails = collection.find({})

        reqData=[]
        for fq in fileDetails:
            fq.pop('file_content')

            fcd=fq['filecreationDate']
            fud=fq['fileUpdationDate']

            creatDate=fcd.strftime("%d-%m-%Y")
            updateDate=fud.strftime("%d-%m-%Y")

            fq['filecreationDate']=creatDate
            fq['fileUpdationDate']=updateDate
            reqData.append(fq)  
            
        reqData =json_util.dumps(reqData)
        reqData=json.loads(reqData)
        df = pandas.DataFrame.from_records(reqData)
        js_data = df.to_json(orient = 'records')
        json_data =json.loads(js_data)
        
        if fileDetails:
            result['status']='success'  
            result['userDetails']=json_data 
            return HttpResponse(json.dumps(result),content_type="application/json")
        else:
            result['status']='failed'
            result['msg']='access denied'
            return HttpResponse(json.dumps(result),content_type="application/json")

    except Exception as ex :

        print(ex)
        result['status']='failed'
        result['msg']=ex

        return HttpResponse(json.dumps(result),content_type="application/json")




@csrf_exempt
def DeleteFileRequestFromUser(request):
    
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        fileId = body['fileId']  

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
        collection = connection[db_name]['FileUpload']  
        
        collection.delete_one({"fileId":int(fileId)})

        result['status']='success'
        result['msg']='Request Entry Deleted Successfully'
        return HttpResponse(json.dumps(result),content_type="application/json")

    except Exception as ex :

        print(ex)
        error= ex
        result['status']='failed'
        result['msg']=ex

        return HttpResponse(json.dumps(result),content_type="application/json")
