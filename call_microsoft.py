# -*- coding: utf-8 -*-
import requests
from microsoft_apikey import key
from wiki_link_name import wiki_query
from get_category import query_category
import time
import datetime

def microsoft (item, tool_name):
    text = item["text"].encode('utf-8')
    dpaId = item["dpaId"]
    
    url = "https://westus.api.cognitive.microsoft.com/entitylinking/v1.0/link"

    #text= "Donald Trump trifft Barack Obama in Washington. Donald Trump liebt Hunde, während Barack Obama eher ein Pferdemensch ist. Obwohl beide in Amerika geboren wurden, haben sie verschiedene Vorstellungen davon, wie die USA in der Zukunft sich gegenüber Amerika verhalten sollen."
    payload = text
    headers = {
        'ocp-apim-subscription-key': key,
        'content-type': "text/plain",
        'cache-control': "no-cache",
        'postman-token': "ef14b041-2750-73ce-19fb-d36c25868067"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    j=response.json()

    try:
        entities= j["entities"]
        t=time.time()
        annotation = []
        for mention in entities:
            label = mention["name"]
            wiki = mention ["wikipediaId"]
            uri = wiki_query (wiki, "en")
            if uri == "":
                uri = wiki_query (wiki,"de")
            if uri == "":
                uri = "Q0"
            category = query_category(uri)
            insert_dict={}
            for item in mention["matches"]:
                surface = item["text"]
                for item_2 in item["entries"]:
                    start = item_2["offset"]
                    end = start+len(surface)
                    insert_dict= {
                        "start" : start,
                        "end"   : end,
                        "label" : label,
                        "surface" : surface,
                        "uri" : uri,
                        "category_tool" : "",
                        "category" : category,
                        "dpaid" : dpaId,
                        "timestamp" : '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.utcfromtimestamp(t)),
                        "tool" : tool_name
                        }
                    #print(insert_dict)
                    annotation.append(insert_dict)
        output=[True,annotation]
    except KeyError:
        output = [KeyError, response.text]
    
    return output
