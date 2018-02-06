import requests
from txt_werk_apikey import txt_werk
from joblib import Memory
import os
import os.path
import time
import datetime

cachedir = "./temp"
if not os.path.exists(cachedir) :
   os.mkdir(cachedir)
memory = Memory(cachedir=cachedir, verbose=0)

# @memory.cache
def txtwerk (item, tool_name):
    text = item["text"].encode('utf-8')
    dpaId = item["dpaId"]
    #except ImportError :
    #raise RuntimeError("Credentials must be supplied as dict in txt_werk_apikey.py. See example_txt_werk_apikey.py or use this as a template: txt_werk=dict(apikey='apikey')")
    TXT_WERK_URL = "https://api.neofonie.de/rest/txt/analyzer"
    key = str(txt_werk['apikey'])
    headers={'X-Api-Key' : key}

    r = requests.post(TXT_WERK_URL, data={'text': text, 'services' : 'entities'}, headers=headers)
    response = r.json()
    try:
        if response["language"] != "de":
            output=[False,response]
        elif response["language"] == "de":
            try:
                t=time.time()
                annotation=[]
                for entity in response["entities"]:
                    if entity["uri"] != None:
                        uri=entity["uri"].replace("https://www.wikidata.org/wiki/","")
                    else:
                        uri= "Q0"
                    if entity["type"][:3] == "ORG":
                        category= "ORG"
                    elif entity["type"][:3] == "PER":
                        category = "PER"
                    elif entity["type"][:3] == "PLA":
                        category = "LOC"
                    else:
                        category = "OTH"
                    insert_dict={
                        "start" : entity["start"],
                        "end" : entity["end"],
                        "label" : entity["label"],
                        "surface" : entity["surface"],
                        "uri" : uri,
                        "category_tool" : entity["type"],
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

    return output