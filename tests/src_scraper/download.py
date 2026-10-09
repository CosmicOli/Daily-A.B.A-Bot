import os

import tracking as t
import utils as u

import bot.globals as bg
import bot.utils as bu
import scraper.download as sd
import scraper.globals as sg
import scraper.utils as su

testGroupName = "download"

def reset():
    u.reset()

    global testOrdinal
    global testBody
    global testBodyFile
    global testLink
    global content
    global image
    global profileHTML

    testOrdinal = "test"
    testBody = "body"
    testBodyFile = None
    testLink = "link"
    content = ""
    image = None
    profileHTML = su.getHTMLFromLink(sg.profileLink)

# Test 1: for downloadImageFromLink; checks if an invalid http code causes an exception
# Expects: an exception to be raised with the string "Image request failed with status code '404'"
reset()
t.attemptTest(testGroupName, 1)

# Just gonna hope that google don't change this link to respond with a non 404 http code
try:
    sd.downloadImageFromLink("jpg", "https://www.google.com/test", testOrdinal)
except Exception as e:
    if (str(e) == "Image request failed with status code '404'"):
        t.passCurrentTest(testGroupName, f"Exception text={e}")
    else:
        t.failCurrentTest(testGroupName, f"Exception text={e}")


# Test 2: for downloadImageFromLink; checks if a valid image link downloads the correct image
# Expects: the same image as the reference image to be downloaded
reset()
t.attemptTest(testGroupName, 2)

u.downloadReferenceImageFromLink("png", os.getenv("REFERENCE_IMAGE_LINK"), "REFERENCE_IMAGE")
try:
    sd.downloadImageFromLink("png", os.getenv("REFERENCE_IMAGE_LINK"), testOrdinal)
except Exception as e:
    t.failCurrentTest(testGroupName, f"Exception text={e}")
else:
    referenceImage = open(f"{sg.postsDirectory}REFERENCE_IMAGE.png", "rb").read()
    image = open(f"{sg.postsDirectory}{testOrdinal}.png", "rb").read()
    if (image == referenceImage):
        t.passCurrentTest(testGroupName, f"Image downloaded successfully")
    else:
        t.failCurrentTest(testGroupName, f"Image downloaded incorrectly")




reset()