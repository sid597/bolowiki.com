from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    settings = db.Column(db.Text(32500))
    tracking = db.Column(db.Text(32500))
    rank = db.Column(db.String(3))
    wikiLinks = db.Column(db.Text(32500), default='')


class WikipediaArticles(db.Model):
    __tablename__ = 'wikipediaArticles'
    id = db.Column(db.Integer, primary_key=True)
    articleName = db.Column(db.String(200))
    articleDict = db.Column(db.JSON)


class AllWikiLinks(db.Model):
    __tablename__ = "AllWikiLinks"
    id = db.Column(db.Integer, primary_key=True)
    wikiLink = db.Column(db.String(200))
    location = db.Column(db.String(500))
    text = db.Column(db.Text(50000))
