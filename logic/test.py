from models import *

from wikipedia import WikipediaParser
from flask import Flask,jsonify
import json
from dbOperations import *
from pprint import pprint
from __init__ import *

def main():
    # parsedArticle = WikipediaParser("https://en.wikipedia.org/wiki/Anarchy")
    # parsedArticle.instantiate()
    #
    # print(len(json.dumps(parsedArticle.wikiDict)))

    # print([ki for ki in parsedArticle.wikiDict])
    wik = getWikipediaArticleDataFirst("_wiki_Wikipedia")
    pprint(json.loads(wik.articleDict))
if __name__ == '__main__':
    with app.app_context():
        main()