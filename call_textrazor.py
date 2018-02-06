# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from textrazor import TextRazorAnalysisException
import textrazor as textrazor_function
from textrazor_apikey import api_key
import time
import datetime
from requests import HTTPError
from get_category import query_category

def textrazor(item, tool_name):
    text = item["text"] #.encode('utf-8')
    dpaId = item["dpaId"]
    
    textrazor_function.api_key=api_key
    #text=text.encode('UTF-8')  
    client = textrazor_function.TextRazor(extractors=["entities","words"])
    #response = client.analyze_url("http://www.bbc.co.uk/news/uk-politics-18640916")
    try:
        response = client.analyze(text)

        if response.ok != True:
            output=[False,response.message]
        else:
            if response.language != "ger":
                output=[False,response]
            else:
                entities_list=[]
                if len(response.entities())==0:
                    output=[True,entities_list]
                else:
                    t=time.time()
                    annotation=[]   
                    for entity in response.entities():
                        label = entity.id
                        if entity.wikidata_id == None:
                            uri="QO"
                            category = "OTH"
                        else:
                            uri=entity.wikidata_id
                            category = query_category(uri)
                        surface = entity.matched_text
                        position = entity.matched_positions
                        start=entity.starting_position
                        end=entity.ending_position
                        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.utcfromtimestamp(t))
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
    except TextRazorAnalysisException:
            output=[False,"http error"]
    return(output)