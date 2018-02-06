# -*- coding: utf-8 -*-
"""

@author: martin virtel
"""

import re
import csv
import requests
import sys
import logging
import urllib
import collections
import pprint
import os
import tempfile
# import datapipeline


logging.basicConfig(level=logging.DEBUG,stream=sys.stderr)
logging.getLogger("requests").setLevel(logging.DEBUG)
logger=logging.getLogger(__name__)


try :
    from credentials import dpa as auth
except ImportError :
    raise RuntimeError("Credentials must be supplied as dict in credentials.py. See example_credentials.py or use this as a template: dpa=dict(login='user',password='secret')")

prefix = "https://nstr.neofonie.de/solr-dev/news/select?q="


def sequentialize(mapping) :
    """
    yields mapping as key/value pairs. If value is any iterable other than a string or a mapping, yield a key/element pair for every element of the value
    a: 1, b: [1,2], c: range(10,20,5)  => (a,1) (b,1) (b,2) (c,10) (c,15)
    """
    for(k,v) in mapping.items() :
        if isinstance(v,collections.Iterable) and not (isinstance(v,collections.Mapping)
                 or isinstance(v,str) ) :
            for e in v :
                yield (k,e)
        else :
            yield (k,v)



def query(q,**kwargs) :
    if kwargs :
        q="{0}&{1}".format(q,urllib.parse.urlencode(tuple(sequentialize(kwargs))))
    url="{0}{1}".format(prefix,q)
    response = requests.get(url,auth=(auth["login"],auth["password"]))
    logger.debug("Query: {}".format(urllib.parse.unquote(url)))
    if not response.ok :
        raise RuntimeError("get_json: {url}\n{response.status_code} : {response.reason}\n{response.text}".format(**locals()))
    return response.json()


def show(result) :
    import pprint
    with tempfile.NamedTemporaryFile("w",encoding="utf-8") as f: 
        f.write(pprint.pformat(result))
        f.flush()
        os.system("less %s" % f.name)





if __name__=='__main__' :
    import copy
    from pprint import pprint
    test_deduplicate()
    doc=dict(response=dict(docs=[dict(title="a",body="b"),dict(title="a",body="c")]))
    pprint(doc)
    pprint(deduplicate(copy.deepcopy(doc),attr="title"))


