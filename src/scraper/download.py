import re
import requests

import scraper.globals as sg
import scraper.tracker as st
import scraper.utils as su


def downloadImageFromLink(format, imageLink, title):
    imageFile = open(f"Posts/{title}.{format}", "wb")

    request = requests.get(imageLink, headers=sg.headers)

    if (request.status_code != 200):
        return -1

    imageFile.write(request.content)
    imageFile.close()
    return 0

def downloadPostBodyFromHTML(html, title):
    postBody = su.getBodyFromPostHTML(html)
    body = open(f"Posts/{title}.txt", "w")
    body.write(postBody)
    body.close

def downloadPostBodyFromLink(link, title):
    downloadPostBodyFromHTML(su.getHTMLFromLink(link), title)

def downloadPost(ordinal, postLink):
    postHTML = su.getHTMLFromLink(postLink)
    imageLink = su.getImageLinkFromPostHTML(postHTML)

    if (downloadImageFromLink("jpg", imageLink, ordinal) == -1 or imageLink is None):
        fileExists = False
        print(f"Day {ordinal} image missing or in incorrect format")
    else:
        fileExists = True

    downloadPostBodyFromHTML(postHTML, ordinal)

    st.trackPost(ordinal, fileExists, postLink)


def downloadPostIfNotDownloaded(ordinal, postLink):
    flag = -1
    
    if (not st.getPostTrackingEntry(ordinal)):
        flag = 0
        downloadPost(ordinal, postLink)
        print(f"Post {ordinal} downloaded")
    else:
        print(f"Post {ordinal} already downloaded, skipping")
    return flag


def downloadMostRecentPost():
    profileHTML = su.getHTMLFromLink(sg.profileLink)
    ordinal = re.search(sg.ordinalMatch, profileHTML).group(1)
    postLink = su.getPostLinkFromHTML(profileHTML)

    if postLink is None:
        return -1

    return downloadPostIfNotDownloaded(ordinal, postLink)


def downloadMostRecentPosts():
    profileHTML = su.getHTMLFromLink(sg.profileLink)
    ordinals = re.findall(sg.ordinalMatch, profileHTML)
    splitProfile = zip(ordinals, re.split(sg.titleMatch, profileHTML))

    counter = 0
    output = []
    for ordinal, html in splitProfile:
        postLink = su.getPostLinkFromHTML(html)

        if postLink is None:
            continue

        counter += 1
        output.append(downloadPostIfNotDownloaded(ordinal, postLink))

    if (counter == 0):
        return -1
    else:
        return output