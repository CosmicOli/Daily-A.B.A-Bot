from html import unescape
import re
import requests

import scraper.globals as sg

def getHTMLFromLink(link):
    requestForPostHTML = requests.get(link, headers=sg.headers)
    postHTML = requestForPostHTML.content.decode("utf-8")
    return postHTML


def getPostLinkFromHTML(profileHTML):
    postID = re.search(sg.postIDMatch, profileHTML)
    if postID:
        postLink = f"{sg.postLinkPrefix}{postID.group(1)}"
    else:
        postLink = None
    return postLink


def getImageLinkFromPostHTML(postHTML):
    imagePartialLink = re.search(sg.imagePartialLinkMatch, postHTML)
    if (imagePartialLink is None):
        return None
    imageLink = imagePartialLink.group(1) + "jpg&name=4096x4096"
    return imageLink


def getBodyFromPostHTML(postHTML):
    postBody = re.search(sg.postBodyMatch, postHTML)
    if (postBody is None):
        return None
    else:
        # I have changed how regex works now to account for the account reposting its own posts; I am not hence certain that html unescape is necessary anymore, but nevertheless I might as well keep it
        formattedBody = unescape(postBody.group(1)).replace("\\n", "\n")

        if (re.search(sg.extraLinkMatch, formattedBody) is None):
            return formattedBody
        else:
            return formattedBody[:-24]
