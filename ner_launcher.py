
from call_function import call_fuction
from call_txtwerk import txtwerk
from call_google import google
from call_dandelion import dandelion
from call_ambiverse import ambiverse
from call_textrazor import textrazor
from call_microsoft import microsoft
# from call_txtwerk_alt import txtwerk_alt
# from call_ambiverse import ambiverse
# from call_dandelion import dandelion
# from call_textrazor import textrazor
# from call_aylien import aylien
# from call_semantria import semantria
# from write_output_db import write_output_db
import logging
import sys
import dataset
logging.basicConfig(level=logging.INFO,stream=sys.stdout)




### Parameters
### Here are the parameters to run "ner_launcher.py"
### dpa-articles are in the db "articles.db"
### The next lines of code create a list.
### Every item in the list has the dpa_id and the text (title and text combined) of the dpa article

db='sqlite:///articles.db'
database = dataset.connect(db)
dpa_list=list(database.query("select dpaId, text from random_view where batch = 2"))
logging.info("Got list with %d articles"%len(dpa_list))



### In the list "ner_tools" all the NER-Tools are listed as functions.
### There will be a request for every tool in the list.
### As funtions:
ner_tools= [ 
    google
    # txtwerk
    # txtwerk_alt
    # dandelion
    # ambiverse
    # textrazor
    # microsoft
    # aylien
    # semantria
]

### This list makes strings from the functions
ner_names=[]
for x in ner_tools:
    ner_names.append(x.__name__)

logging.info("\n***Starting*** \nwith Ner-Tools %s\n"%(ner_names))


### This functions calls the NER-APIs with the texts from "dpa_list".
### For every text from the list there is an API-request for every NER-Tool.
### After the request is done, the the ouput will be written in the database (write_output_db)


for item in dpa_list:
    #item["text"]="Dieser Text enthält keine Entis"
    #item["text"] = "Sanan Suomi  etymologiasta ei  ole täyttä varmuutta. Se on ilmeisesti ollut alun perin Suomenlahden ympäristöä ja sittemmin lähinnä Varsinais-Suomea koskeva nimitys ja laajentunut vasta myöhemmin tarkoittamaan koko maata."
    output=call_fuction(item,ner_tools)

logging.info("\n***END***\nner_launcher done for %s documents with %s tools"%(len(dpa_list),(len(ner_tools))))
