#!/usr/bin/env python
# -*- coding: UTF-8 -*-import urllib.parse
# This function uses the wikidata sparql query to define the category (Per, Org, Loc, Oth) of an entity

import urllib.request
import requests
import xml
import dataset

from joblib import Memory
import os


cachedir = "./temp"
if not os.path.exists(cachedir) :
   os.mkdir(cachedir)


memory = Memory(cachedir=cachedir, verbose=0)

@memory.cache
def query_category (uri):
    session=requests.session()
    # uri="Q1408652"
    # uri="Q8488" """BCN 92"""
    # uri = "Q19020" """OSCAR"""
    # uri = "Q101712" """Person"""
    #uri = "Q12418" """Mona Lisa"""
    if uri != None:
    # and category_start== None:
        url_person= "".join(("https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=ASK%20%7B%20wd%3A",uri,"%20wdt%3AP31%2Fwdt%3AP279*%20wd%3AQ5%2C%20wd%3AQ215627%20%7D"))
        response_person = session.get(url_person)
        text_person=response_person.text
        y_person=text_person.find("true")
        if y_person > -1:
            #print("Person")
            x=2
        # Organisation:
        url_organisation= "".join(("https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=ASK%20%7B%20wd%3A",uri,"%20wdt%3AP31%2Fwdt%3AP279*%20wd%3AQ43229%7D"))
        response_organisation = session.get(url_organisation)
        text_organisation=response_organisation.text
        y_organisation=text_organisation.find("true")
        if y_organisation > -1:
            #print("Organisation")
            x=2

        # Location:
        # Parameter: Q1496967: territorial entity , Q618123: geographical object, Q82794: geographic region Q2221906: geographical point
        location_query=dict(query="""
            ASK { wd:%(uri)s wdt:P31/wdt:P279* wd:Q1496967, wd:Q618123, wd:Q82794 }
            """%locals())
        response_location=session.get("https://query.wikidata.org/bigdata/namespace/wdq/sparql",params=location_query)
        text_location=response_location.text
        y_location=text_location.find("true")
        if y_location > -1:
            #print("Location")
            x=2

        if y_person > -1:
            category="PER"
        elif y_location > -1:
            category="LOC"
        elif y_organisation > -1:
            category="ORG"
        else:
            category="OTH"
        #print("Category is: ",category)
    return (category)
        


