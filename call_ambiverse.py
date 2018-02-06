import requests
import json
from ambiverse_apikey import client_id, client_secret
from ambiverse_token import get_token
from joblib import Memory
import os
import logging
import sys
import time
import datetime
from get_category import query_category
logging.basicConfig(level=logging.INFO,stream=sys.stdout)

cachedir = "./temp"
if not os.path.exists(cachedir) :
   os.mkdir(cachedir)
memory = Memory(cachedir=cachedir, verbose=0)

@memory.cache
def ambiverse(item,tool_name):
    text = item["text"]#.encode('utf-8')
    dpaId = item["dpaId"]
    ambiverse_token=get_token(client_id, client_secret)
    ambiverse_request_url = "https://api.ambiverse.com/v1/entitylinking/analyze"
    text_string=json.dumps({"text" : text })
    payload= text_string
    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'authorization': ambiverse_token
    }
    response = requests.request("POST", ambiverse_request_url, data=payload, headers=headers)
    response= response.json()
    try:
        response_matches =  response["matches"]

        entity_list= []
        try:
            if response["language"] != "de":
                output=[False,response]
            elif response["language"] == "de":
                # import IPython
                # IPython.embed()
                try:
                    t=time.time()
                    annotation=[]
                    for entity in response["matches"]:
                        surface = entity["text"]
                        start = entity["charOffset"]
                        end =int(entity["charOffset"])+int(entity["charLength"])
                        label = ""
                        t=time.time()
                        entity["timestamp"]='{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.utcfromtimestamp(t))
                        try:
                            uri=entity["entity"]["id"]
                            uri=uri.replace("http://www.wikidata.org/entity/","")
                            entity["uri"] = uri
                            category = query_category(uri)
                        except KeyError:
                            uri ="Q0"
                            category = "OTH"

                        insert_dict={
                            "start" : start,
                            "end" : end,
                            "label" : label,
                            "surface" : surface,
                            "uri" : uri,
                            "category_tool" : "",
                            "category" : category,
                            "dpaid" : dpaId,
                            "timestamp" : '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.utcfromtimestamp(t)),
                            "tool" : tool_name
                            }
                        annotation.append(insert_dict)
                    output=[True,annotation]
                
                except KeyError:
                    output= [KeyError,response]
        except KeyError:
            output= [KeyError,response]
    except KeyError:
        output= [KeyError,response]
    return output
