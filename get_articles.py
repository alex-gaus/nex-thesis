#! /usr/bin/env python
# This function uses an internal api of the german news agency to download newswire texts

from neofonie import show, query
import json
import os.path
import string
import datetime
from datetime import date
import errno
import click
import dataset
db='sqlite:///articles.db'
database = dataset.connect(db)
articles=database["articles"]


@click.command()
@click.option('--day1', default=str(date(2017, 3, 1)),prompt="Start Day (Format:YYYY-MM-DD), default:", help='Startposition')
@click.option('--day2', default=str(date(2017, 3, 1)),prompt="End Day (Format:YYYY-MM-DD), default:", help='Endposition')
@click.option('--rows_batch', default=1000,prompt="Batches for Server Requests, default:", help='default=1000')
#day1= str(date(2017, 2, 14))
#day2= str(date(2017, 4, 12))
#rows_batch=1000
 
def neofonie_query(day1,day2,rows_batch):

    

    daytext1=str("createdAt:[")
    daytext2=str("T00:00:00.001Z TO ")
    daytext3=str("T23:59:59.999Z]")
    dayframe="".join([daytext1,day1,daytext2,day2,daytext3])
    

    counter=1
    start_position=0

    numFound="noch nicht bekannt"


    

    while numFound=="noch nicht bekannt" or start_position <= numFound:
        result=(query('*:*',
                    wt="json",
                    fq=[
                        "sourceId:dpa",
                        dayframe,
                        "-dpaRessort:rs",
                        "-dpaTitle:Tagesvorschau",
                        "-dpaTitle:Abendvorschau",
                        "-dpaTitle:Morgenvorschau",
                        "-dpaTitle:Terminvorschau",
                        "-dpaTitle:DAX",
                        "-dpaTitle:Ausgewählte Investmentfond",
                        "-dpaTitle:*Ausgewählte Auslandsaktien*",
                        "-dpaTitle:EuroStoxx",
                        "-dpaTitle:MDAX",
                        "-dpaTitle:TecDAX",
                        "-dpaTitle:Devisenkurse am",
                        "-dpaId:*dpa-afx*",
                        # "-text:-----------------------",
                        "-text:berichtet dpa heute wie folgt",
                        "-dpaTitle:DGAP-News"
                    ],
                    fl="createdAt,dpaTitle,dpaId,dpaRessort,dpaServices,text,dpaKeywords,dpaService,dpaservices,dpaservice",
                        # "dpaServices",
                        # "createdAt",
                        # "dpaId",
                    sort= "createdAt asc",   
                    start=start_position,
                    rows=rows_batch
                    )
                )
        print("\ndownloaded  batch\n")
        numFound=int(result["response"]["numFound"])
        amount_batches=numFound//rows_batch
        last_batch=numFound%rows_batch
        amount_batches=numFound//rows_batch
        last_batch=numFound%rows_batch
        print("\n Amount of articles:",numFound,"\n")
        docs=result["response"]["docs"]
    #For Loop
        for doc in docs :
            #print("Schleife fuer Datei {0} fuer Titel {dpaTitle}".format(filename,**d)) # d["dpaTitle"]
        

        # ##DPA ID as filename
        #     string_begin_temp =(doc["dpaId"])
        #     string_begin_temp = string_begin_temp.replace(":","_")
        #     string_begin=string_begin_temp.replace('/', 'v-')
        # #Writing the file               
        #     string_end=".json"
        #     filename="".join([string_begin,string_end])
        #     foldername=(doc["createdAt"])
        #     foldername=foldername[0:10]
        #     # filename="/Users/alex/python_project/outputs/DPA-Meldungen/{string_begin}.json".format(**locals())
        #     # #
        #     # verzeichnisname aus createdAt
        #     # os.makedirectory ???
        #     #
        #     # try / except 
        #     #
        #     file_path = "".join(["/Users/alex/python_project/outputs/DPA-Meldungen/",foldername,"/"])
        #     try: 
        #         os.makedirs(file_path)
        #     except OSError:
        #         if not os.path.isdir(file_path):
        #             raise  

        #     with open(file_path+filename, 'w') as f:    
        #         json.dump(doc,f)
        #         f.close()
        #         print("\nSaved:", filename,"\n","Article Number",counter)

            print (doc)
            insert_dic={
                "dpaId":doc["dpaId"],
                "text":doc["text"],
                "createdAt":doc["createdAt"],
                "dpaTitle":doc["dpaTitle"],
                "dpaRessort":doc["dpaRessort"]
                #"dpaServices":doc["dpaServices"]
            }
            articles.insert(insert_dic)
            counter=counter+1
        #Moving the file
        #old_position="".join(["/Users/alex/python_project/",filename])
        #new_position="".join(["/Users/alex/python_project/outputs/DPA-Meldungen/",filename])
        #os.rename(old_position, new_position)
        #print("\nMoved file",filename)  
        
        if start_position <= amount_batches*rows_batch:
            start_position=start_position+rows_batch
        else:
            start_position=start_position+rows_batch
            rows_batch=last_batch
        

    print("\n\n**FINISHED**")
    print (doc)

if __name__=="__main__":
        neofonie_query()