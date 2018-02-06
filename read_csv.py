# -*- coding: utf-8 -*-
import csv
import os
import dataset
from get_category import query_category
db='sqlite:///articles.db'
database = dataset.connect(db)
annotation = database["annotation_user"]

# db='sqlite:///annotations.db'
# annotations = dataset.connect(db)
# annotation = annotations["annotations"]


documents = os.listdir("output/annotation-user")
for document in documents:
    if document != ".DS_Store":
        print(document)
        dpaId=document[:-4].replace("_",":")
        dpaId=dpaId.replace("v-","/")
        text0=list(database.query("select text from random_view where dpaId = :dpaId", dpaId=dpaId))[0]["text"]
        users = os.listdir("output/annotation-user/%s"%document)
        for user in users:
            if user != ".DS_Store":
                print(user)
                username=user[:-4]
                with open('output/annotation-user/%s/%s'%(document,user), 'r') as csvfile:
                    entities = csv.reader(csvfile, delimiter='\t', quotechar='|')
                    marker=0
                    text=text0
                    start=0
                    end=0
                    for token in entities:
                        try:
                            #print(token[2])
                            if token[3] != "_":
                                import IPython
                                #IPython.embed()
                                # position=token[1].split("-")
                                # start=position[0]
                                # end=position[1]
                                surface=token[2]
                                end_o=end
                                start=text.find(surface)+end
                                end=start+len(surface)
                                text=text[end-end_o:]
                                information=token[3].split(":")
                                label=information[0]
                                #cateogry=information[1]
                                uri=information[1]
                                category = query_category(uri)
                                category_user = information[2]
                                status=category_user.find("[")
                                category_user=category_user.split("[")[0]
                                uri=uri.split("[")[0]
                                print(status)
                                if status != -1 and marker != 0:
                                    entity["end"]=end
                                    old_surface=entity["surface"]
                                    new_surface=" ".join([old_surface,surface])
                                    entity["surface"]=new_surface
                                    print("&&&&&&")
                                else:
                                    entity={
                                        "start":start,
                                        "end":end,
                                        "surface":surface,
                                        "label":label,
                                        "category":category,
                                        "category_user":category_user,
                                        "uri":uri,
                                        "user":username,
                                        "dpaid":dpaId
                                    }
                                #print ("JETZT ",token[1],token[2],token[3])
                                marker=marker+1
                                print(entity)
                                #annotation.insert(entity)
                                import IPython
                                #IPython.embed()
                                annotation.upsert(entity,["start","dpaid", "user"])
                            else:
                                marker=0
                        except IndexError:
                            #print("no entity")
                            x=0

# documents = os.listdir("annotation")
# for document in documents:
#     if document != ".DS_Store":
#         users = os.listdir("annotation/%s"%document)
#         for user in users:
#             print(user)

#             tree = ET.parse('annotation/%s/%s'%(document,user))
#             root = tree.getroot()

#             text = root.findall("*/{http://www.dspin.de/data/textcorpus}text")[0].text
#             tokens = root.findall("*/{http://www.dspin.de/data/textcorpus}tokens")[0]
#             token_dict={}
#             for token in tokens:
#                 token_dict.update({token.attrib["ID"]:token.text})
#             sentences = root.findall("*/{http://www.dspin.de/data/textcorpus}sentences")[0]
#             try:
#                 namedEntities = root.findall("*/{http://www.dspin.de/data/textcorpus}namedEntities")[0]
#                 entities={}
#                 start=0
#                 end=0
#                 for entity in namedEntities:
#                     try:
#                         class_=entity.attrib["class"]
#                     except KeyError:
#                         class_=None
#                     if entity.attrib["tokenIDs"].find(" ") == -1:
#                         token= token_dict[entity.attrib["tokenIDs"]]
#                         id_=entity.attrib["tokenIDs"]
#                     else: 
#                         ids=entity.attrib["tokenIDs"].split(" ")
#                         c=1
#                         token=""
#                         for id_ in ids:
#                             token="%s %s"%(token,token_dict[id_])
#                         token=token[1:]
#                     end_o=end
#                     start=text.find(token)+end
#                     end=start+len(token)
#                     text=text[end-end_o:]    
#                     entities.update({id_: {"text": token, "class":class_, "start": start, "end": end}})
#                 print(entities)
#             except IndexError:
#                 print("Document has no Annotations")