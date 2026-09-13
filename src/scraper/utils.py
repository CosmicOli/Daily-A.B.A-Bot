import re
import requests

import scraper.globals as sg


def getHTMLFromLink(postLink):
    requestForPostHTML = requests.get(postLink, headers=sg.headers)
    postHTML = requestForPostHTML.content.decode("utf-8")
    return postHTML


def getPostLinkFromHTML(profileHTML):
    postID = re.search(sg.postMatch, profileHTML)
    if postID:
        postLink = f"https://x.com/EveryDayABA/status/{postID.group(1)}"
    else:
        postLink = None
    return postLink


def getImageLinkFromPostHTML(postHTML):
    imagePartialLink = re.search("src=\"(https://pbs.twimg.com/media/.{15}\\?format=).*?\"", postHTML)
    if (imagePartialLink is None):
        return None
    imageLink = imagePartialLink.group(1) + "jpg&name=4096x4096"
    return imageLink


def getBodyFromPostHTML(postHTML):
    postBody = re.search(f"content=\"({sg.titleMatch}(?s:.)*?)\"", postHTML)
    if (postBody is None):
        return None
    else:
        return postBody.group(1)
