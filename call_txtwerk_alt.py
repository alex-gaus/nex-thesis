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

@memory.cache
def txtwerk_alt (text):
    #except ImportError :
    #raise RuntimeError("Credentials must be supplied as dict in txt_werk_apikey.py. See example_txt_werk_apikey.py or use this as a template: txt_werk=dict(apikey='apikey')")
    TXT_WERK_URL = "https://api.neofonie.de/rest/txt/analyzer"
    key = str(txt_werk['apikey'])
    headers={'X-Api-Key' : key}
    r = requests.post(TXT_WERK_URL, data={'text': text, 'services' : 'entities-ml,measures'}, headers=headers)
    response = r.json()
    try:
        if response["language"] != "de":
            output=[False,response]
        elif response["language"] == "de":
            try:
                for entity in response["entities"]:
                    t=time.time()
                    entity["timestamp"]='{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.utcfromtimestamp(t))
                    if entity["uri"] !=None:
                        entity["uri"]=entity["uri"].replace("https://www.wikidata.org/wiki/","")
                    extra={"txtwerk_alt":{"category":entity['type']}}
                    entity["extra"] = str(extra)
                    del(entity["type"])
                output=[True,response["entities"]]
            
            except KeyError:
                output= [KeyError,response]
    except KeyError:
            output= [KeyError,response]

    return output