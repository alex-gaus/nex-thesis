import dataset
db='sqlite:///articles.db'
database = dataset.connect(db)
articles=database["articles"]

articles= list(database.query("select text, dpaId from random_view where batch=1 or batch=2"))

for article in articles:
    dpaId=article["dpaId"]
    dpaId=dpaId.replace("/","v-")
    dpaId=dpaId.replace(":","_")
    text_file = open("articles/%s.txt"%(dpaId), "w")
    text_file.write(article["text"])
    text_file.close()
