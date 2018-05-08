import json
import os
import boto3
import hashlib
import random
from datetime import datetime
from chalice import Chalice, Response, BadRequestError
from chalice import NotFoundError

app = Chalice(app_name='itsshort')
app.debug = True

DDB = boto3.client('dynamodb')

@app.route('/')
def index():
    return {'status': 'itsshort is live'}

@app.route('/shorten', methods=['POST'])
def shorten():
    url = app.current_request.json_body.get('url','')
    timestamp = datetime.now().replace(microsecond=0).isoformat()
    urlid = hashlib.md5(url).hexdigest()[:6]
    if not url:
        raise BadRequestError("Missing URL")
    DDB.put_item(
        TableName=os.environ['APP_TABLE_NAME'],
        Item={'urlid':{'S': urlid},
              'timestamp':{'S': timestamp},
              'url':{'S':url}})
    return {'shortened': urlid}

@app.route('/{identifier}', methods=['GET'])
def retrieve(identifier):
    try:
        record = DDB.get_item(Key={'urlid': {'S': identifier}},
        TableName=os.environ['APP_TABLE_NAME'])
        
    except Exception as e:
        raise NotFoundError(identifier)
    
    # Response Data
    urlid = hashlib.md5(identifier).hexdigest()[:10]
    headers = app.current_request.to_dict()
    context = app.current_request.context
    sourceip = context['identity']['sourceIp']
    useragent = headers['headers']['user-agent']
    timestamp = datetime.now().replace(microsecond=0).isoformat()

    DDB.put_item(
        TableName=os.environ['APP_TABLE_NAME'],
        Item={'urlid':{'S': urlid},
              'identifier':{'S': identifier},
              'sourceip':{'S': sourceip},
              'useragent':{'S': useragent},
              'timestamp':{'S':timestamp}})

    return Response(status_code=301,
                   headers={'Location': record['Item']['url']['S']}, body='')