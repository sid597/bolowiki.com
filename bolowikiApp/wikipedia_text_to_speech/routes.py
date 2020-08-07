# External packages
from flask import request, session, jsonify, Blueprint
from urllib.parse import urlparse
from flask import current_app as app

# Local packages
from ..dbOperations import methodsForTTS, setUserRemainingLimit
from .textToSpeech import GoogleTextToSpeech
from ..utils import remainingCharacterLimitNotZero, login_required

textToSpeech_bp = Blueprint('textToSpeech_bp', __name__, url_prefix='/text_to_speech')


@textToSpeech_bp.route('/wikipedia/', methods=['GET', 'POST'])
def getWiki():
    """ Receive a request to convert the clicked link to audio
        check if link is present in AllWikiLinks
            yes :
                return from there
            no  :
                get the parsed page from wikipedia class
                save that to allwikilinks list with the wikilink being path and text being the dict
                call convertospeech with necessary fragment
                get the location where this is saved
        Link in users wikilinks ?
        no : then add
        else: take user to that location

        https://en.wikipedia.org/wiki/Anarchy#Etymology
        ParseResult(scheme='https', netloc='en.wikipedia.org', path='/wiki/Anarchy',
                    params='', query='', fragment='Etymology')
    """
    try:
        acceptedWikipediaUrls = {'en.wikipedia.org', 'hi.wikipedia.org'}
        getLanguageSpecificUrl = {
            'en': 'https://en.wikipedia.org',
            'hi': 'https://hi.wikipedia.org'
        }
        app.logger.info("Inside getWiki")
        app.logger.info("request received is %s" % request)
        app.logger.info("request form received is %s" % request.form)

        wikiLinkToBeParsed = str(request.form['wikipediaLink']).strip()
        articleLanguage = str(request.form['articleLanguage'])
        app.logger.info( "wikiLink to be parsed is : %s, artice language is %s, and its type is %s" % (
        wikiLinkToBeParsed, articleLanguage, type(wikiLinkToBeParsed)))
        parsedUrl = urlparse(wikiLinkToBeParsed)
        app.logger.info("parsedUrl is : %s" % str(parsedUrl))
        if parsedUrl.netloc not in acceptedWikipediaUrls or parsedUrl.scheme != 'https':

            msg = "Pass a valid wikipedia url, for e.g :  https://en.wikipedia.org/wiki/Anarchy"
            return jsonify({
                'txt': msg, 'mediaLocation':
                    '', "success": False,
            })

        wikipediaNetLoc = getLanguageSpecificUrl[articleLanguage]
        path = parsedUrl.path
        fragment = parsedUrl.fragment

        if 'logged_in' in session:
            username = session['username']
            newTTS = methodsForTTS(
                username,
                path,
                articleLanguage,
                wikipediaNetLoc,
                fragment
            )
            mediaLocation, articleFragment, articleContentsList, articleFragmentLength, articalTotalLength = newTTS.orchestrator
            # TODO : Uncomment the following line
            # setUserRemainingLimit(username, articleFragmentLength)

            return jsonify({
                'mediaLocation': mediaLocation + '.mp3',
                'txt': articleFragment,
                "success": True,
                'articleContents': articleContentsList,
                'articleFragmentLength': articleFragmentLength,
                'articalTotalLength': articalTotalLength,
            })

        username = 'UserNotLoggedIn'
        fragment = ''
        newTTS = methodsForTTS(
            username,
            path,
            articleLanguage,
            wikipediaNetLoc,
            fragment
        )
        mediaLocation, articleFragment, articleContentsList, articleFragmentLength, articalTotalLength = newTTS.orchestrator
        return jsonify({
            'mediaLocation': mediaLocation + '.mp3',
            'txt': articleFragment,
            "success": True,
            'articleContents': '',
            'articleFragmentLength': articleFragmentLength,
            'articalTotalLength': articalTotalLength
        })
    except Exception as e:
        app.logger.info("error in get wiki route : %s" % e)
        return str(e)


