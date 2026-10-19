import re
import requests

import scraper.globals as sg
import scraper.tracker as st
import scraper.utils as su


def downloadImageFromLink(format, imageLink, title):
    imageFile = open(f"{sg.postsDirectory}{title}.{format}", "wb")

    request = requests.get(imageLink, headers=sg.headers)

    # I know technically any code beginning with 2 is 'successful' but I expect a code of 200 and am gonna stick with that for now
    if (request.status_code != 200):
        raise Exception(f"Image request failed with status code '{request.status_code}'")

    imageFile.write(request.content)
    imageFile.close()


def downloadPostBodyFromHTML(html, title):
    postBody = su.getBodyFromPostHTML(html)
    if (not postBody is None):
        body = open(f"{sg.postsDirectory}{title}.txt", "w", encoding="utf-8")
        body.write(postBody)
        body.close
    else:
        raise Exception("No post body found in HTML")


def downloadPostBodyFromLink(link, title):
    # NOTE: This raises an exception if no post body is found
    downloadPostBodyFromHTML(su.getHTMLFromLink(link), title)


def downloadPost(ordinal, postLink):
    # NOTE: This raises an exception if the postLink is invalid
    postHTML = su.getHTMLFromLink(postLink)
    imageLink = su.getImageLinkFromPostHTML(postHTML)

    if (imageLink is None):
        fileExists = False
        print(f"WARNING: Day '{ordinal}' image missing or in incorrect format")
    else:
        # This try except is to catch if an incorrect http code response occurs
        # Depending on which response occurs, it may be worth attempting to download the image again, but I felt this was overkill due to the unlikeliness of this occuring
        # For now, the fact embeds become enabled when the image fails to download is a good enough band aid for this issue
        try:
            downloadImageFromLink("jpg", imageLink, ordinal)
        except Exception as e:
            print(f"WARNING: Day '{ordinal}' image download failed:{e}")
            fileExists = False
        else:
            fileExists = True

    # The programmed behaviour when no text file is found is to make the message content just the link, so this only needs to be a warning and not an error
    try:
        downloadPostBodyFromHTML(postHTML, ordinal)
    except Exception as e:
        print(f"WARNING: Day '{ordinal}' body download failed:{e}")

    # NOTE: This raises an exception if the post is already tracked
    st.trackPost(ordinal, fileExists, postLink)


# flag is 0 when a post is downloaded, or -1 when a post is already tracked
def downloadPostIfNotTracked(ordinal, postLink):
    flag = -1
    
    if (not st.getPostTrackingEntry(ordinal)):
        flag = 0
        # NOTE: downloadPost raises an exception if the post being downloaded is already tracked, or if the postLink is invalid
        # Okay I am a silly billy; I already accounted for the first of those exceptions with the if statement, but I guess I'll keep the note due to the latter half
        downloadPost(ordinal, postLink)
        print(f"Post {ordinal} downloaded")
    else:
        print(f"Post {ordinal} already tracked, skipping")
    return flag


def downloadMostRecentPostFromProfileHTML(profileHTML):
    ordinal = su.getFirstOrdinalFromText(profileHTML)
    if (ordinal == None):
        raise Exception("No ordinal found in profileHTML")    

    postLink = su.getPostLinkFromProfileHTML(profileHTML)

    if postLink is None:
        raise Exception("No post link found in profileHTML")

    # NOTE: downloadPostIfNotTracked raises an exception if the postLink is invalid
    # That being said, it should never be possible for a fqdn not to be returned from su.getPostLinkFromHTML(profileHTML), unless it returns None
    return downloadPostIfNotTracked(ordinal, postLink)


def downloadMostRecentPostsFromProfileHTML(profileHTML):
    ordinals = su.getOrdinalsFromText(profileHTML)
    splitProfile = zip(ordinals, re.split(sg.titleMatch, profileHTML))

    output = []
    for ordinal, html in splitProfile:
        postLink = su.getPostLinkFromProfileHTML(html)

        if postLink is None:
            continue

        # This is handled as downloadPostIfNotDownloaded can raise an exception if the postLink is invalid
        try:    
            output.append(downloadPostIfNotTracked(ordinal, postLink))
        except Exception as e:
            print(f"Exception raised while downloading post {ordinal}: {e}")

    return output