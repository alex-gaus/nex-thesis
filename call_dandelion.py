# This function calls the dandelion NER-api

from dandelion_apikey import token
import json
from dandelion import DataTXT
from wiki_link_import import wiki_query
from get_category import query_category
import time
import datetime


def dandelion(item,tool_name):
    
    text = item["text"].encode('utf-8')
    dpaId = item["dpaId"]
    
    datatxt = DataTXT(app_id=token, app_key=token)
    response = datatxt.nex(
        text,
        include_categories=True,
        include_types=True,
        include_image=True,
        include_lod=True,
        include_alternate_labels=True,
        include_abstract=True)
    try:
        if response["lang"] != "de":
            output=[False,response]
        elif response["lang"] == "de":
            try:
                annotation=[]
                t=time.time()
                for entity in response.annotations:
                    wiki= str(entity["id"])
                    uri = wiki_query(wiki)
                    category = query_category(uri)
                    surface = entity["spot"]
                    start = entity["start"]
                    end = entity["end"]
                    label = entity["title"]
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
                # import IPython
                # IPython.embed()
            except KeyError:
                output= [KeyError,response]
    except KeyError:
        output= [KeyError,response]

    return output
