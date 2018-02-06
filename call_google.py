# This function calls the Google NER-api


import requests
import json
import time
import datetime
from joblib import Memory
import os
import os.path
from wiki_link_name import wiki_query
from get_category import query_category
import dataset

cachedir = "./temp"
if not os.path.exists(cachedir) :
   os.mkdir(cachedir)
memory = Memory(cachedir=cachedir, verbose=0)
db='sqlite:///articles.db'
database = dataset.connect(db)
annotation = database["annotation_user"]
#@memory.cache
def google (item,tool_name):

    #text="Trump sprach an diesem Montag vor dem Bundesverfassungsgericht in Karlsruhe über den Aktienkurs von Apple."
    text = item["text"].encode('utf-8')
    dpaId = item["dpaId"]
    text0=list(database.query("select text from random_view where dpaId = :dpaId", dpaId=dpaId))[0]["text"]
    #dpaId = "Test"
    url = "https://language.googleapis.com/v1beta2/documents:analyzeEntities"

    querystring = {"key":"AIzaSyBcTrjGvS3gxthY2Iq70Xt-LfXsr3Hd4U8"}

    payload = "{\n  \"encodingType\": \"UTF8\",\n  \"document\": {\n    \"type\": \"PLAIN_TEXT\",\n    \"language\": \"de\",\n    \"content\": \"%s'\"\n  }\n}"%(text)


    response = requests.request("POST", url, data=payload, params=querystring)
    j=response.json()
    import IPython
    #IPython.embed()
    t=time.time()
    try:
        if j["language"] != "de":
            output=[False,j]
        elif j["language"] == "de":
            try:
                entities=j["entities"]
                annotation=[]
                for entity in entities:
                    text1=text0
                    start=0
                    end=0
                    for mention in entity["mentions"]:
                        if mention["type"]=="PROPER":
                            label=entity["name"]
                            category_tool =entity["type"]
                            #start=mention["text"]["beginOffset"]
                            surface=mention["text"]["content"]
                            end_o=end
                            if text1.find(surface) != -1:
                                start=text1.find(surface)+end
                                end=start+len(surface)
                                text1=text1[end-end_o:]
                                end=start+len(surface)

                            else:
                                start=-1
                                end=-1

                            try:
                                lang=entity["metadata"]["wikipedia_url"][8:10]
                                wiki=entity["metadata"]["wikipedia_url"][30:].replace("_"," ")
                                uri=wiki_query(wiki, lang)
                                if uri == "":
                                    if category_tool[:3] == "PER" or "ORG" or "LOC":
                                        category = category_tool[:3]
                                    else:
                                        category = "OTH"
                                    uri="Q0"
                                else:
                                    category = query_category(uri)
                            except KeyError:
                                if category_tool[:3] == "UNK":
                                    category = "OTH"
                                    uri="Q0"
                                else:
                                    if category_tool[:3] == "PER" or "ORG" or "LOC":
                                        category = category_tool[:3]
                                    else:
                                        category = "OTH"
                                    uri="Q0"
                            insert_dict={
                                "start" : start,
                                "end" : end,
                                "label" : label,
                                "surface" : surface,
                                "uri" : uri,
                                "category_tool" : category_tool,
                                "category" : category,
                                "dpaid" : dpaId,
                                "timestamp" : '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.utcfromtimestamp(t)),
                                "tool" : tool_name
                            }
                            import IPython
                            #IPython.embed()
                            annotation.append(insert_dict)
                output=[True,annotation]
            except KeyError:
                output= [KeyError,j]
    except KeyError:
        output= [KeyError,j]

    return(output)
            
        
