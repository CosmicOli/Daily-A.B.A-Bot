import re
import requests

import scraper.globals as sg
import scraper.tracker as st
import scraper.utils as su


def downloadImageFromLink(format, imageLink, title):
    imageFile = open(f"{sg.postsDirectory}{title}.{format}", "wb")

    request = requests.get(imageLink, headers=sg.headers)

    if (request.status_code != 200):
        raise Exception(f"Image request failed with status code {request.status_code}")

    imageFile.write(request.content)
    imageFile.close()


def downloadPostBodyFromHTML(html, title):
    postBody = su.getBodyFromPostHTML(html)
    body = open(f"{sg.postsDirectory}{title}.txt", "w", encoding="utf-8")
    body.write(postBody)
    body.close


def downloadPostBodyFromLink(link, title):
    downloadPostBodyFromHTML(su.getHTMLFromLink(link), title)


def downloadPost(ordinal, postLink):
    postHTML = su.getHTMLFromLink(postLink)
    imageLink = su.getImageLinkFromPostHTML(postHTML)

    if (imageLink is None):
        fileExists = False
        print(f"Day {ordinal} image missing or in incorrect format")
    else:
        # This try except is to catch if an incorrect html code response occurs
        # Depending on which response occurs, it may be worth attempting to download the image again, but I felt this was overkill due to the unlikeliness of this occuring
        # For now, the fact embeds become enabled when the image fails to download is a good enough band aid for this issue
        try:
            downloadImageFromLink("jpg", imageLink, ordinal)
        except Exception as e:
            print(e)
            fileExists = False
        else:
            fileExists = True     

    downloadPostBodyFromHTML(postHTML, ordinal)

    # NOTE: This throws an exception if the post is already tracked
    st.trackPost(ordinal, fileExists, postLink)


# flag is 0 when a post is downloaded, or -1 when a post is already downloaded
def downloadPostIfNotDownloaded(ordinal, postLink):
    flag = -1
    
    if (not st.getPostTrackingEntry(ordinal)):
        flag = 0
        # NOTE: downloadPost throws an exception if the post being downloaded is already tracked
        downloadPost(ordinal, postLink)
        print(f"Post {ordinal} downloaded")
    else:
        print(f"Post {ordinal} already downloaded, skipping")
    return flag


def downloadMostRecentPostFromProfileHTML(profileHTML):
    ordinal = re.search(sg.ordinalMatch, profileHTML).group(1)
    postLink = su.getPostLinkFromHTML(profileHTML)

    if postLink is None:
        raise Exception("Failed to find a post")

    # NOTE: downloadPostIfNotDownloaded throws an exception if the post being downloaded is not already downloaded but is already tracked
    return downloadPostIfNotDownloaded(ordinal, postLink)


def downloadMostRecentPostsFromProfileHTML(profileHTML):
    ordinals = re.findall(sg.ordinalMatch, profileHTML)
    splitProfile = zip(ordinals, re.split(sg.titleMatch, profileHTML))

    counter = 0
    output = []
    for ordinal, html in splitProfile:
        postLink = su.getPostLinkFromHTML(html)

        if postLink is None:
            continue

        # This is handled as downloadPostIfNotDownloaded can throw an exception if the post is not already downloaded but is already tracked
        try:    
            output.append(downloadPostIfNotDownloaded(ordinal, postLink))
        except Exception as e:
            print(f"Exception thrown while downloading post {ordinal}: {e}")
        else:     
            counter += 1

    if (counter == 0):
        raise Exception("Failed to find any posts")
    else:
        return output