from models import *

from wikipedia import WikipediaParser
from flask import Flask,jsonify
import json
app = Flask(__name__)
def main():
    parsedArticle = WikipediaParser("https://en.wikipedia.org/wiki/Anarchy")
    parsedArticle.instantiate()

    print(len(json.dumps(parsedArticle.wikiDict)))

    # print([ki for ki in parsedArticle.wikiDict])

if __name__ == '__main__':
    with app.app_context():
        main()