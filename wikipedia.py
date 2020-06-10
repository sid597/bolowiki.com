"""
A minimal reproduction of wikipedia article html which I parse in this module.
To check out the minimal reproductions go to wiki.html

Note : This module does parse contents of table, images. Also note that wikipedia 
        represents scientific formulas as images (if they are coded so ) for eg.
        if one wants to write sqrt(2) they might use LaTex or Mathjax and wikipedia 
        converts that to images. Therefore this module might not be useful if you want to 
        search for these type of articles.
        
        Superscripts are parsed out because they won't make sense in audio


"""
import bs4 as bs
import urllib.request
from pprint import pprint
from collections import deque


class WikipediaParser():

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

    def getContentTitles(self):
        """Get different sections Titles in the wikipedia article 
            For e.g article is Anarchy(https://en.wikipedia.org/wiki/Anarchy)

            So its section Titles are :
            1	Etymology
            2	Political philosophy
                2.1	Description
                2.2	Immanuel Kant
            3	Anthropology
            4	Examples of state-collapse anarchy
                4.1	English Civil War (1642–1651)
                4.2	French Revolution (1789–1799)
                4.3	Jamaica (1720)
                4.4	Russian Civil War (1917–1922)
                4.5	Spain (1936)
                4.6	Albania (1997)
                4.7	Somalia (1991–2006)
            5	Lists of ungoverned communities
                5.1	Ungoverned communities
                5.2	Anarchist communities
            6	See also
            7	References
            8	External links


            Approach : Every wikipedia article has a contents pane and in html is id is 'toc'
                        So I grab that id's contents and all these contents are <li> tags with <span> which
                        contains the text for content no and its name. So I take the name and put them in a wikiSectionTitles List.


        Returns:
            list: A list containing all the article content titles 
        """
        self.wikiSections = self.soup.find(id="toc").find_all('li')
        return self.wikiSections
        for section in self.wikiSections:
            self.wikiSectionTitles.append(section.find_all('span')[1].string)
        return self.wikiSectionTitles

    def getAllContentTags(self):
        """From the Wikipedia article html parse out all the necessary data related to 
           content for e.g paragraphs, list, headings. Tables are not included because 
           I can't think of a good way to convert the tables data in audio format which will
           make sense to listner.

           Approach: Go through all the tags in wikipedia article body and if the tag is 
                     is in acceptesTags list then add them to wikiParas List.

        Returns:
            list: A list of all the content which make up the wikipedia article.
        """

        for i in self.body:
            tag = i.name
            # print(tag)
            if tag in self.acceptedTags:
                self.wikiParas.append(i)
            # l.append(i.name)
        return self.wikiParas

    def getIntroParas(self):
        """Get the introduction paragraphs for the wikipedia article

           Approach : So I extracted all the wikipedia articles html contents in a list called wikiParas.
                      I extract all the contents(using in beautifulSoup context) from the wikiParas which have <p> tags
                      and if I encounter some content withtag not equal to p Ireturn. This ensures that I only get the 
                      intorduction paragraphs for the wikipedia article

        Returns:
            list: A list containing the introduction paragraphs
        """

        ctr = 0
        for i in self.wikiParas[self.ctr:]:
            tag = i.name
            if tag != 'p':
                return ''.join(self.wikiIntro)
            else:
                self.wikiIntro.append(self.htmlToPlain(i))
                self.ctr += 1
        self.wikiDict['Intro'] = ''.join(self.wikiIntro)
        return ''.join(self.wikiIntro)

    def parseParas(self):
        """Parse the paragraph(i.e content presented in <p> </p> tags)
           A paragraph can have multiple tags init for eg. Tags for :
           links, italics, list etc. 

        """
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
        """Get all the strings(in beautifulSoup context) from paragraph.
           The paragraph can have other tags init as well I have to 
            get string content from them.
            The type of tags that can be there are :
            - li
            - dd
            - sup 

            Approach : Go to each tag in p and get string for that tag
        """
        l = []
        paraContent = p.contents
        for i in paraContent:
            tag = i.name
            if tag == 'li' or tag == 'dd':
                listContents = i.contents
                for cont in listContents:
                    if cont.string != None:
                        l.append(cont.string)

            elif i.string is None or tag == 'sup':
                pass
            else:
                l.append(str(i.string))
        return ''.join(l)

    def getTitlesContent(self):
        """Get the contents for each title in wikipedia article

        Returns:
            dict: A dictionary which has title as key and their content as value for the corresponding
                  wikipedia article.
        """
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
                    self.wikiDict[currentTitle] = (
                        "%s. \n" % currentTitle + ''.join(l))
                ptr = self.ctr
        return self.wikiDict

    def instantiate(self):
        self.getContentTitles()
        self.getAllContentTags()
        self.getIntroParas()
        self.getTitlesContent()
