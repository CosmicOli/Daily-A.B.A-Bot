import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

# GLOBALS
headers = {"User-Agent": os.getenv("USER_AGENT")}
profileLink = "https://x.com/EveryDayABA"
titleMatch = "Day \\d+ of A\\.B\\.A posting\\."
ordinalMatch = "Day (\\d+) of A\\.B\\.A posting\\."
postMatch = "data-href=\"/EveryDayABA/status/(\\d+)\""

def getHTMLFromLink(postLink):
    requestForPostHTML = requests.get(postLink, headers=headers)
    postHTML = requestForPostHTML.content.decode("utf-8")
    return postHTML

def getPostLinkFromHTML(profileHTML):
    postID = re.search(postMatch, profileHTML)
    if postID:
        postLink = f"https://x.com/EveryDayABA/status/{postID.group(1)}"
    else:
        postLink = None
    return postLink

def getImageLinkFromPostHTML(postHTML):
    imagePartialLink = re.search("src=\"(https://pbs.twimg.com/media/.{15}\\?format=).*?\"", postHTML)
    imageLink = imagePartialLink.group(1) + "jpg&name=4096x4096"
    return imageLink

def downloadImageFromLink(format, imageLink, title):
    imageFile = open(f"Posts/{title}.{format}", "wb")
    imageFile.write(requests.get(imageLink, headers=headers).content)
    imageFile.close()


def downloadMostRecentPost():
    profileHTML = getHTMLFromLink(profileLink)
    ordinal = re.search(ordinalMatch, profileHTML).group(1)
    postLink = getPostLinkFromHTML(profileHTML)

    if postLink is None:
        print("No post found.")
        return
    
    postHTML = getHTMLFromLink(postLink)
    imageLink = getImageLinkFromPostHTML(postHTML)
    downloadImageFromLink("jpg", imageLink, ordinal)


def downloadMostRecentPosts():
    profileHTML = getHTMLFromLink(profileLink)
    ordinals = re.findall(ordinalMatch, profileHTML)
    splitProfile = zip(ordinals, re.split(titleMatch, profileHTML))

    for ordinal, html in splitProfile:
        postLink = getPostLinkFromHTML(html)

        if postLink is None:
            continue

        postHTML = getHTMLFromLink(postLink)
        imageLink = getImageLinkFromPostHTML(postHTML)
        downloadImageFromLink("jpg", imageLink, ordinal)


downloadMostRecentPosts()