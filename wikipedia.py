"""
Wikipedia html parsing

#&.firstHeading
#bodyContent/ .mw-body-content
    .mw-parser-output
    <p> tags : with tags <b>, <a>, <sup>
    #&.toc
        - ul
    

other tags: table, div, 
"""
import bs4 as bs
import urllib.request
from pprint import pprint
from collections import deque
# sauce = urllib.request.urlopen(
#     'https://en.wikipedia.org/wiki/Dragon_2').read()
# soup = bs.BeautifulSoup(sauce, 'lxml')


# print(soup.find(id="firstHeading").string)
# print(soup.find(id="bodyContent" ).string)
# print (soup.find_all('div',class_="mw-parser-output"))






class Wikipedia():

    def __init__(self, linkToWiki):

        self.wikiLink = urllib.request.urlopen(linkToWiki).read()
        self.soup = bs.BeautifulSoup(self.wikiLink, 'lxml')
        self.title = self.soup.find(id="firstHeading").string
        self.body = self.soup.find('div', class_="mw-parser-output").children
        self.wikiSections = None
        self.wikiSectionTitles = []
        self.wikiParas = []
        self.wikiIntro = []
        self.ctr = 0

    def getWikiSections(self):
        self.wikiSections = self.soup.find(id="toc").find_all('li')
        return self.wikiSections

    def getSectionTitles(self):
        self.getWikiSections()
        for section in self.wikiSections:
            self.wikiSectionTitles.append(section.find_all('span')[1].string)
        return self.wikiSectionTitles

    
    def getAllContentTags(self):
        for i in self.body:
            tag = str(i)[:5]
            if (('<p>' in tag or '<ul>' in tag ) or ('<h2>' in tag or '<h3>' in tag)):
                self.wikiParas.append(i)
            # l.append(i.name)
        return self.wikiParas

    def getIntoParas(self):
        ctr = 0
        for i in self.wikiParas[self.ctr:]:
            tag = str(i)[:5]
            if '<h2>' in tag or '<h3>' in tag:
                return self.wikiIntro
            else:
                self.wikiIntro.append(self.htmlToPlain(i))
                self.ctr += 1
                
    def parseParas(self):
        l = []
        for i in self.wikiParas[self.ctr:]:
            tag = str(i)[:5]
            if '<h2>' in tag or '<h3>' in tag:
                return l
            else:
                l.append(i)
                self.ctr += 1
        
    def getTitlesContent(self):
        ptr = self.ctr
        
        while ptr != len(self.wikiParas):
            tag = str(self.wikiParas[ptr])[:5]
            currentTag = self.wikiParas[ptr]
            if '<h2>' in tag:
                currentTitle = currentTag.span.string
                print (currentTitle)
                self.ctr += 1
                ptr = self.ctr
                
            elif '<h3>' in tag:
                currentTitle = currentTag.span.string
                print (currentTitle)
                self.ctr += 1
                ptr = self.ctr
            else:
                l = self.parseParas()
                print(l)
                ptr = self.ctr
        # return

    
    def getAll(self):
        self.getWikiSections()
        self.getSectionTitles()
        self.getAllContentTags()
        self.getIntoParas()


    def htmlToPlain(self,p):
        """p is paragraph in html it can have other tags init as well I have to 
            get string content from them.
                
            Approach 1:
                Go to each tag in p and get string for that tag
        """
        l = []
        paraContent = p.contents
        for i in paraContent:
            tag= str(i)[:5]
            if i.string is None or  '<sup' in tag :
                pass
            else:
                
                l.append(str(i.string))
        
        return ''.join(l)

dragon = Wikipedia('https://en.wikipedia.org/wiki/Anarchy')
dragon.getAll()

# print(dragon.wikiIntro)
d = dragon.getIntoParas()
print(''.join(d))

# dl = dragon.htmlToPlain(d)

# s = ''
# for i in dl :
#     print(i)
#     s+=i 
# print (s)
# print(dl)

# print(dragon.getTitlesContent())