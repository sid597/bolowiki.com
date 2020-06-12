from models import *
from flask import current_app as app
from wikipedia import WikipediaParser
import json
from tts import GoogleTextToSpeech
from pymysql import escape_string as thwart

def getUserDataFirst(currentUserUsername):
    return User.query.filter_by(username=currentUserUsername).first()


def getWikipediaArticleDataFirst(articleNameToSearchWith):
    return WikipediaArticles.query.filter_by(articleName=articleNameToSearchWith).first()


def getAllWikiLinksDataFirst(linksNameToSearchWith=''):
    return AllWikiLinks.query.filter_by(wikiLink=linksNameToSearchWith).first()


def getUserDataAll(currentUserUsername):
    return User.query.filter_by(username=currentUserUsername).first()


def getWikipediaArticleDataAll(articleNameTosearchWith):
    return WikipediaArticles.query.filter_by(articleName=articleNameTosearchWith).first()


def getAllWikiLinksDataAll(linksNameTosearchWith=''):
    AllWikiLinks.query.filter_by(wikiLink=linksNameTosearchWith).first()


def createNewWikipediaArticle(articleNameTosaveWith, articleDictToSave):
    newWikiArticle = WikipediaArticles(articleName=articleNameTosaveWith, articleDict=articleDictToSave)
    db.session.add(newWikiArticle)
    db.session.commit()


def createNewAllWikiLink(articleNameTosaveWith, articleLocationToSaveWhere, textToSave):
    newWikiLinkWithFragment = AllWikiLinks(wikiLink=articleNameTosaveWith, location=articleLocationToSaveWhere,
                                           text=textToSave)
    db.session.add(newWikiLinkWithFragment)
    db.session.commit()


def createNewUser(username,password,email):
    newUser = User(username=username,password=password,email=email)
    db.session.add(newUser)
    db.session.commit()



class methodsForTTS():
    """Methods used for text-to-speech
    """

    def __init__(self, username, path, fragment):
        self.currentUserUsername = username
        self.wikipediaArticlePath = path
        self.wikipediaArticleFragment = fragment
        self.nameToSaveWith = str('_'.join(path.split('/')) + '#' + fragment)
        self.nameWithoutFragment = str('_'.join(path.split('/')))

    def addToUsersWikiLinks(self):
        try:
            user = getUserDataFirst(self.currentUserUsername)
            userWikiLinks = user.wikiLinks
            app.logger.info(self.nameToSaveWith not in userWikiLinks)
            if (self.nameToSaveWith not in userWikiLinks) or (userWikiLinks is None):
                user.wikiLinks += ' ' + self.nameToSaveWith
                db.session.commit()
                app.logger.info("username is %s : links are %s" % (self.currentUserUsername, user.wikiLinks))

            else:
                app.logger.info('something went wrong')

        except Exception as e:
            app.logger.info("error in addToUsersWikiLinks : %s" % e)
            return str(e)

    def getWikipediaArticleFragment(self):
        try:
            article = getWikipediaArticleDataFirst(self.nameWithoutFragment)
            app.logger.info("article is : %s" % article)

            if article is not None:
                articleDict = json.loads(article.articleDict)
                # pprint(articleDict)
                articleFragment = articleDict[self.wikipediaArticleFragment]
                return ''.join(articleFragment)
            wikiUrl = 'https://en.wikipedia.org' + self.wikipediaArticlePath
            app.logger.info("wikipedia url is : %s" % wikiUrl)
            parsedArticle = WikipediaParser(wikiUrl)
            parsedArticle.instantiate()
            app.logger.info("wikipedia parsedArticle  is : %s" % parsedArticle)
            articleDict = parsedArticle.wikiDict
            jsonifiedArticle = json.dumps(articleDict)
            createNewWikipediaArticle(self.nameWithoutFragment, jsonifiedArticle)
            app.logger.info("Commit successful")
            app.logger.info("Checking if article got commited :  %s" %
                            (getWikipediaArticleDataFirst(self.nameWithoutFragment)).articleDict)
            articleFragment = articleDict[self.wikipediaArticleFragment]
            return ''.join(articleFragment)
        except Exception as e:
            app.logger.info("error in get wiki : %s" % e)
            return str(e)

    def textToSpeech(self, convertThisArticleToSpeech):
        try:
            wikilinkData = getAllWikiLinksDataFirst(self.nameToSaveWith)
            if wikilinkData is None:
                app.logger.info("articleLocation is none for combined path : %s" % self.nameToSaveWith)
                mediaLocation = GoogleTextToSpeech(convertThisArticleToSpeech, self.nameToSaveWith)
                createNewAllWikiLink(self.nameToSaveWith, mediaLocation, convertThisArticleToSpeech)
                return mediaLocation
            media = getAllWikiLinksDataFirst(self.nameToSaveWith)
            return media.location
        except Exception as e:
            app.logger.info("error in get wiki : %s" % e)
            return str(e)


#################
#  Test TTS     #
#################

""" If we parse the url then we get following result:

https://en.wikipedia.org/wiki/Anarchy#Etymology
ParseResult(scheme='https', netloc='en.wikipedia.org', path='/wiki/Anarchy',
                        params='', query='', fragment='Etymology')
                        
https://en.wikipedia.org/wiki/Unincorporated_area
https://en.wikipedia.org/wiki/Moore,_Indiana
                       
How to check if test passed ?
check the article on wiki or in print console and the audio file created
in $ (os.cpwd())/static/tts/                        
"""


def testTTS():
    path = '/wiki/Unincorporated_area'
    fragment = ''
    user = 'qwer'
    newtts = methodsForTTS(user, path, fragment)
    print(newtts.nameToSaveWith)
    art = newtts.getWikipediaArticleFragment()
    print(art)
    newtts.textToSpeech(art)
    newtts.addToUsersWikiLinks()

