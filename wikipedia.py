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
        self.acceptedTags = ['p', 'ul', 'h2', 'h3', 'dl', 'ol']
        self.h2Orh3 = ['h2', 'h3']
        self.ctr = 0
        self.wikiDict = {}

    def getWikiSections(self):
        self.wikiSections = self.soup.find(id="toc").find_all('li')
        return self.wikiSections

    def getSectionTitles(self):
        
        for section in self.wikiSections:
            self.wikiSectionTitles.append(section.find_all('span')[1].string)
        return self.wikiSectionTitles

    def getAllContentTags(self):

        for i in self.body:
            tag = i.name
            # print(tag)
            if tag in self.acceptedTags:
                self.wikiParas.append(i)
            # l.append(i.name)
        return self.wikiParas

    def getIntroParas(self):
        ctr = 0
        for i in self.wikiParas[self.ctr:]:
            tag = i.name
            if tag != 'p':
                return ''.join(self.wikiIntro)
            else:
                self.wikiIntro.append(self.htmlToPlain(i))
                self.ctr += 1
        return ''.join(self.wikiIntro)
        
    def parseParas(self):
        l = []
        for i in self.wikiParas[self.ctr:]:
            tag = i.name
            # print(tag)
            if tag in self.h2Orh3:
                return l
            else:
                l.append(self.htmlToPlain(i))
                self.ctr += 1

    def htmlToPlain(self, p):
        """p is paragraph in html it can have other tags init as well I have to 
            get string content from them.

            Approach 1:
                Go to each tag in p and get string for that tag
        """
        l = []
        paraContent = p.contents
        for i in paraContent:
            tag = i.name
            if tag == 'li':
                listContents = i.contents
                for cont in listContents:
                    if cont.string != None:
                        l.append(cont.string)
            elif tag == 'dd':
                dlItems = i.contents
                for ddCon in dlItems:
                    if ddCon.string != None:
                        l.append(ddCon.string)
            elif i.string is None or tag == 'sup':
                pass
            else:
                l.append(str(i.string))
        return ''.join(l)

    def getTitlesContent(self):
        ptr = self.ctr
        currentTitle = []

        while ptr != len(self.wikiParas):
            tag = self.wikiParas[ptr].name
            currentTag = self.wikiParas[ptr]
            if tag in self.h2Orh3:
                currentTitle = ''.join(
                    [i.string if i.string != None else '' for i in currentTag.contents])
                # print (currentTitle)
                self.ctr += 1
                ptr = self.ctr
            else:
                l = self.parseParas()
                if l != None:
                    self.wikiDict[currentTitle] = ''.join(l)
                ptr = self.ctr
        return self.wikiDict

    def getAll(self):
        self.getWikiSections()
        self.getSectionTitles()
        self.getAllContentTags()
        self.getIntroParas()
        self.getTitlesContent()


dragon = Wikipedia('https://en.wikipedia.org/wiki/Anarchy')
dragon.getAll()
# print(dragon.wikiDict['English Civil War (1642–1651)'])
chars = 0
print(dragon.getIntroParas())
for ki in dragon.wikiDict:
    print('-------------------------------------------------')
    print(ki)
    print('\n')
    

    val = dragon.wikiDict[ki]
    chars += len(val)
    print(val)

print('-------------------------------------------------')

pprint(dragon.wikiSectionTitles)
print (chars)
# print(dragon.wikiIntro)
# d = dragon.getIntroParas()
# print(''.join(d))

# dl = dragon.htmlToPlain(d)

# s = ''
# for i in dl :
#     print(i)
#     s+=i
# print (s)
# print(dl)

# print()
