# Python packages
import json

# Exxternal packages
from urllib.parse import unquote
from flask import current_app as app

# Local packages
from bolowikiApp.wikipedia_text_to_speech.textToSpeech import GoogleTextToSpeech
from bolowikiApp.parse_wikipedia_article import WikipediaParser
from bolowikiApp.models import db, User, WikipediaArticles, AllWikiLinks


def getUserDataFirst(currentUserUsername):
    return User.query.filter_by(username=currentUserUsername).first()


def getUserRemainingLimit(currentUserUsername):
    return User.query.filter_by(username=currentUserUsername).first().remainingLimit


def getUserDataAll(currentUserUsername):
    return User.query.filter_by(username=currentUserUsername).first()


def getWikipediaArticleDataFirst(articleNameToSearchWith):
    return WikipediaArticles.query.filter_by(articleName=articleNameToSearchWith).first()


def getAllWikiLinksDataFirst(linksNameToSearchWith=''):
    return AllWikiLinks.query.filter_by(wikiLink=linksNameToSearchWith).first()


def getWikipediaArticleDataAll(articleNameTosearchWith):
    return WikipediaArticles.query.filter_by(articleName=articleNameTosearchWith).first()


def getAllWikiLinksDataAll(linksNameTosearchWith=''):
    return AllWikiLinks.query.filter_by(wikiLink=linksNameTosearchWith).first()


def setUserRemainingLimit(currentUserUsername, lengthOfTextToConvert):
    user = getUserDataFirst(currentUserUsername)
    user.remainingLimit = user.remainingLimit - lengthOfTextToConvert
    db.session.commit()


def createNewWikipediaArticle(articleNameTosaveWith, articleDictToSave):
    newWikiArticle = WikipediaArticles(
        articleName=articleNameTosaveWith,
        articleDict=articleDictToSave
    )
    db.session.add(newWikiArticle)
    db.session.commit()


def createNewAllWikiLink(articleNameTosaveWith, articleLocationToSaveWhere, textToSave):
    newWikiLinkWithFragment = AllWikiLinks(
        wikiLink=articleNameTosaveWith,
        location=articleLocationToSaveWhere,
        text=textToSave
    )
    db.session.add(newWikiLinkWithFragment)
    db.session.commit()


def createNewUser(username, email, password):
    app.logger.info("username,email,password are : %s, %s, %s" %
                    (username, email, password))
    newUser = User(username=username, password=password, email=email)
    db.session.add(newUser)
    db.session.commit()



class methodsForTTS():
    """Methods used for text-to-speech
    """

    def __init__(self, username, path, articleLanguage, wikipediaNetLoc, fragment=''):
        self.currentUserUsername = username
        self.wikipediaArticlePath = path
        self.wikipediaArticleFragment = ' '.join(unquote(fragment).split('_'))
        self.nameToSaveWith = unquote(
            '_'.join(path.split('/')) + '#' + self.wikipediaArticleFragment)
        self.nameWithoutFragment = str('_'.join(path.split('/')))
        self.filename = unquote(
            '_'.join(path.split('/')) + '__' + self.wikipediaArticleFragment)
        self.articleFragment = None
        self.articleContentsList = None
        self.articleTotalCharacterCount = 0
        self.articleFragmentLength = 0
        self.articleLanguage = articleLanguage
        self.wikipediaNetLoc = wikipediaNetLoc

    @property
    def orchestrator(self):
        app.logger.info("Inside orchestrator")
        app.logger.info("self.currentUserUsername is %s " %
                        self.currentUserUsername)
        app.logger.info("self.wikipediaArticlePath is %s " %
                        self.wikipediaArticlePath)
        app.logger.info("self.wikipediaArticleFragment is %s " %
                        self.wikipediaArticleFragment)
        app.logger.info("self.nameToSaveWith is %s " % self.nameToSaveWith)
        app.logger.info("self.filename is %s " % self.filename)

        currentUser = getUserDataFirst(self.currentUserUsername)
        userWikiLinks = currentUser.wikiLinks
        isArticleThere = getAllWikiLinksDataFirst(self.nameToSaveWith)
        self.getWikipediaArticleFragment()
        if self.nameToSaveWith in userWikiLinks:
            # TODO somehow tell the user to move to that location
            app.logger.info("Article data %s" %(isArticleThere.location, self.articleFragment, articleContentsList))
            return isArticleThere.location, self.articleFragment, self.articleContentsList, self.articleFragmentLength, self.articleTotalCharacterCount

        self.addToUsersWikiLinks()
        if isArticleThere is None:
            app.logger.info("Article is none ")

            app.logger.info("Article to convert is : %s " %
                            self.articleFragment)
            return self.textToSpeech(
                self.articleFragment), self.articleFragment, self.articleContentsList, self.articleFragmentLength, self.articleTotalCharacterCount
        app.logger.info("Article is there and its location is : %s" %
                        isArticleThere.location)
        return isArticleThere.location, self.articleFragment, self.articleContentsList, self.articleFragmentLength, self.articleTotalCharacterCount

    def addToUsersWikiLinks(self):
        try:
            app.logger.info("Inside addToUsersWikiLinks")
            user = getUserDataFirst(self.currentUserUsername)
            userWikiLinks = user.wikiLinks
            app.logger.info("Is name to save with in user wiki links %s" %
                            self.nameToSaveWith not in userWikiLinks)
            if (self.nameToSaveWith not in userWikiLinks) or (userWikiLinks is None):
                user.wikiLinks += ' ' + self.nameToSaveWith
                db.session.commit()
                app.logger.info("username is %s : links are %s" %
                                (self.currentUserUsername, user.wikiLinks))

            else:
                app.logger.info(
                    "link is already there in user's wiki link BUT HOW CAN THIS BE ? ")

        except Exception as e:
            app.logger.error("error in addToUsersWikiLinks : %s" % e)
            return str(e)

    def getWikipediaArticleFragment(self):
        try:
            app.logger.info("Inside getWikipediaArticleFragment")
            article = getWikipediaArticleDataFirst(self.nameWithoutFragment)
            app.logger.info("article is : %s" % article)
            if article is not None:
                articleDict = json.loads(article.articleDict)
                # pprint(articleDict)
                self.articleFragment = ''.join(
                    articleDict[self.wikipediaArticleFragment][0])
                app.logger.info("Got article fragment ")
                app.logger.info("article fragment is %s" %
                                self.articleFragment)
                self.articleFragmentLength = len(self.articleFragment)
                app.logger.debug("articleFragmentLength is %s" %
                                 self.articleFragmentLength)

                self.articleContentsList = [i for i in articleDict]

            wikiUrl = self.wikipediaNetLoc + self.wikipediaArticlePath
            app.logger.info("wikipedia url is : %s" % wikiUrl)
            parsedArticle = WikipediaParser(wikiUrl)
            articleDict, articleTotalCharacterCount = parsedArticle.instantiate()
            app.logger.debug("articleTotalCharacterCount is %s" %
                             articleTotalCharacterCount)
            self.articleTotalCharacterCount = articleTotalCharacterCount
            app.logger.info("wikipedia parsedArticle  is : %s" % parsedArticle)
            # articleDict = parsedArticle.wikiDict
            jsonifiedArticle = json.dumps(articleDict)
            createNewWikipediaArticle(
                self.nameWithoutFragment, jsonifiedArticle)
            app.logger.info("Commit successful")
            app.logger.info("Checking if article got commited :  %s" % (
                getWikipediaArticleDataFirst(self.nameWithoutFragment)).articleDict)
            self.articleFragment = ''.join(
                articleDict[self.wikipediaArticleFragment][0])
            self.articleContentsList = [[contentName, articleDict[contentName][1]] for contentName in articleDict]
            self.articleFragmentLength = len(self.articleFragment)
            app.logger.debug("articleFragmentLength is %s" %
                             self.articleFragmentLength)

        except Exception as e:
            app.logger.error("error in get wiki : %s" % e)
            return str(e)

    def textToSpeech(self, convertThisArticleToSpeech):
        try:
            app.logger.info("Inside textToSpeech")
            wikilinkData = getAllWikiLinksDataFirst(self.nameToSaveWith)
            if wikilinkData is None:
                app.logger.info(
                    "articleLocation is for combined path : %s" % self.filename)
                mediaLocation = GoogleTextToSpeech(
                    textToConvert=convertThisArticleToSpeech,
                    nameToSaveWith=self.filename,
                    translateLanguage=self.articleLanguage,
                    voiceGender='MALE',
                    convertType='wiki'
                )
                createNewAllWikiLink(
                    self.nameToSaveWith,
                    mediaLocation,
                    convertThisArticleToSpeech
                )
                return mediaLocation
            media = getAllWikiLinksDataFirst(self.nameToSaveWith)
            return media.location
        except Exception as e:
            app.logger.error("error in get wiki : %s" % e)
            return str(e)
