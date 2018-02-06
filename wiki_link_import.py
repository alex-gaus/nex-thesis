import urllib.parse
import urllib.request
import requests
import requests_cache
from joblib import Memory
import os


cachedir = "./temp"
if not os.path.exists(cachedir) :
   os.mkdir(cachedir)


memory = Memory(cachedir=cachedir, verbose=0)

#requests_cache.install_cache()

session=requests.session()


x=0
@memory.cache
def wiki_query(wiki):
    """ return wikidata link for wikipedia id

    >>> type(wiki_query(100))==str
    True
    
    >>> wiki_query(999)
    'https://www.wikidata.org/wiki/Q688510'
   

    >>> wiki_query(400)
    Traceback (most recent call last):
    ...
    KeyError: 'pageprops'
    """
    
    pageid =str(wiki)
    api_url= "https://de.wikipedia.org/w/api.php?action=query&format=json&prop=pageprops&pageids="
    #pageid="736"
    url="".join([api_url,pageid])

        


    # Alex orig.
    # f = urllib.request.urlopen(url)
    # response=(f.read().decode('utf-8'))
    # print(response)
    # response= response.split(":")
    # ohne session response = requests.get(url).json()
    response = session.get(url).json()
 
    
    # wikidata_id = response[-1]
    # wikidata_id = wikidata_id.replace("'", "")
    # wikidata_id = wikidata_id.replace('"', "")
    # wikidata_id = wikidata_id.replace('}', "")
    # print("WIKIDATA ID: ",wikidata_id)
    #
    # if 'pageprops' in response['query']['pages'][pageid]
    #
    #
    try :
        wikidata_id=response['query']['pages'][pageid]['pageprops']['wikibase_item']
       
        
    except KeyError :
        wikidata_id="Q0"
    
    # wikidata_base="https://www.wikidata.org/wiki/"
    # wikidata_url= "".join([wikidata_base,wikidata_id])
    
    
    # w  = open("temp.txt", "w")
    # w.write(wikidata_url) 
    # wikipedia_base= "https://de.wikipedia.org/wiki?curid="
    # wikipedia_url= "".join ([wikipedia_base,pageid])
    # print('URL WIKIDATA: ', wikidata_url)
    # print ('URL WIKIPEDIA: ', wikipedia_url)
    #print(wikidata_url)
    return wikidata_id 

if __name__=="__main__" :
    import doctest
    doctest.testmod(verbose=True)
    # assert wiki_query(100) == "https://www.wikidata.org/wiki/Q19577"
    # assert wiki_query(999) == "https://www.wikidata.org/wiki/Q688510"
    # assert wiki_query(101) == "https://www.wikidata.org/wiki/Q19577"
    # assert wiki_query(400) == "https://www.wikidata.org/wiki/Q19577"
