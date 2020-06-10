from MySQLdb import escape_string as thwart
from dbconnect import connection
from urllib.parse import urlparse


class queryDb():
    c, conn = connection()

    def __init__(self, username, c, wikiArticleFullLink=""):
        self.username = username
        self.wikiArticleFullLink = wikiArticleFullLink
        self.c = c

    def getUserData(self):
        c.execute("SELECT * FROM users WHERE username = (%s)",
                  (thwart(self.username),))

    def getUserId(self):
        c.execute("SELECT id  FROM users WHERE username = (%s)",
                  (thwart(self.username),))

    def createNewUser(self,username, password, email,):
        c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                  (thwart(self.username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))

    def getUserWikilinks(self):
        userId = self.getUserId()
        userLinks = c.execute("SELECT wikiLinks FROM userWikiLinks WHERE userId=(%s)",
                              (thwart(userId),))
        return userLinks

    def checkLinkInGlobalWikiList(self):
        isItThere = c.execute("SELECT id FROM wikiList WHERE article=(%s) ",
                              (thwart(self.wikiArticleFullLink),))
        if isItThere is None:
            return False
        return isItThere

    def getWikiLocation(self):
        location = c.execute("SELECT location FROM wikiList WHERE article=(%s)",
                             (thwart(self.wikiArticleFullLink),))
        if location is None:
            return False
        return location

    def saveToGlobalWikiList(self):
        parsedUrl = urlparse(self.wikiArticleFullLink)
        locationToSaveInto = parsedUrl.path
        wikipediaPageLink = parsedUrl.scheme+'://'+parsedUrl.netloc + parsedUrl.path
        try:
            c.execute("INSERT INTO wikiList (location, article) VALUES (%s, %s) ",
                      (thwart(locationToSaveInto), thwart(wikipediaPageLink),))
        except Exception as e:
            return str(e)

    def updateUsersWikiList(self):
        return
