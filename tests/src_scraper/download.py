import os

import tracking as t
import globals as g
import utils as u

import bot.globals as bg
import bot.utils as bu
import scraper.download as sd
import scraper.globals as sg
import scraper.tracker as st

testGroupName = "download"

def reset():
    u.reset()

    global testOrdinal
    global referenceOrdinal
    global testPostLink
    global testImageLink
    global testImageFormat # NOTE: This is to be used when code expects you to be able to change the file format; I will magic number "jpg" where there is no control at that scope

    testOrdinal = "test"
    referenceOrdinal = "REFERENCE"
    testPostLink = "link"
    testImageLink = "link"
    testImageFormat = "jpg"


# As sd.downloadPost can throw an exception, in most cases the test should fail if an exception is thrown
# This function factors out handling the exception in every test where relevant
def downloadPost(ordinal, postLink):
    try:
        sd.downloadPost(ordinal, postLink)
    except Exception as e:
        t.failCurrentTest(f"Exception text={e}")



# Test 1: for downloadImageFromLink; checks if an invalid http code causes an exception
# Expects: an exception to be raised with the string "Image request failed with status code '404'"
reset()
t.attemptTest(testGroupName, 1)

# Just gonna hope that google don't change this link to respond with a non 404 http code
testImageLink = "https://www.google.com/test"

try:
    sd.downloadImageFromLink(testImageFormat, testImageLink, testOrdinal)
except Exception as e:
    if (str(e) == "Image request failed with status code '404'"):
        t.passCurrentTest(f"Exception text={e}")
    else:
        t.failCurrentTest(f"Exception text={e}")


# Test 2: for downloadImageFromLink; checks if a valid image link downloads the correct image
# Expects: the same image as the reference image to be downloaded
# NOTE: the expectation is that twitter images are all .jpg, however this part of code is written to account for all file formats
reset()
t.attemptTest(testGroupName, 2)

testImageLink = g.referenceImageLink
testImageFormat = "png"

u.downloadReferenceImageFromLink(testImageFormat, testImageLink, referenceOrdinal)
try:
    sd.downloadImageFromLink(testImageFormat, testImageLink, testOrdinal)
except Exception as e:
    t.failCurrentTest(f"Exception text={e}")
else:
    referenceImage = open(f"{sg.postsDirectory}{referenceOrdinal}.{testImageFormat}", "rb").read()
    image = open(f"{sg.postsDirectory}{testOrdinal}.{testImageFormat}", "rb").read()
    if (image == referenceImage):
        t.passCurrentTest(f"Image downloaded matched reference image")
    else:
        t.failCurrentTest(f"Image downloaded incorrectly")



# Test 3: for downloadPostBodyFromHTML; checks if the correct body is saved to the correct file upon given a valid post HTML
# Expects: the test body to be saved to the correct file
reset()
t.attemptTest(testGroupName, 3)

sd.downloadPostBodyFromHTML(g.testPostHTML, testOrdinal)
try:
    file = open(f"{sg.postsDirectory}{testOrdinal}.txt", "r", encoding="utf-8")
except Exception as e:
    t.failCurrentTest(f"Exception raised while attempting to read the supposedly created file\nException text={e}")
else:
    body = file.read()
    file.close()
    if (body == g.testPostBody):
        t.passCurrentTest(f"Post body saved to file correctly")
    else:
        t.failCurrentTest(f"Downloaded text={body}")



# not going to test individually whether body no image and image no body work, as it requires making a custom webpage
# not going to test for the case where the image link returns an invalid http code, as it requires making a custom webpage

# Test 4: for downloadPost; checks if an exception is raised when the post link is invalid
# Expects: an exception to be raised
# NOTE: I am not testing for a particular exception or test here as the exception should be raised by requests.get, and while there should be a consistent exception thrown by requests.get the point of the test is that we don't care which one it is
reset()
t.attemptTest(testGroupName, 4)

try:
    sd.downloadPost(testOrdinal, "")
except Exception as e:
    t.passCurrentTest(f"Exception text={e}")
else:
    t.failCurrentTest(f"No exception raised when expected")


# Test 5: for downloadPost; checks if a valid link (a link that produces html with http code 200) that doesn't produce twitter post html produces the right entry information
# Expects: the entry to be f"{testOrdinal},False,{testPostLink}" and for no image or text files to be created
# NOTE: Some warnings are expected to be printed during this test
reset()
t.attemptTest(testGroupName, 5)

# Look if google is down we have bigger problems than whether my code passes these tests
testPostLink = "https://google.com/"
downloadPost(testOrdinal, testPostLink)

if (os.path.isfile(f"{sg.postsDirectory}{testOrdinal}.jpg")):
    t.failCurrentTest(f"Image downloaded unexpectedly")
elif (os.path.isfile(f"{sg.postsDirectory}{testOrdinal}.txt")):
    t.failCurrentTest(f"Post body downloaded unexpectedly")
else:
    postTrackingEntry = st.getPostTrackingEntry(testOrdinal)
    if (postTrackingEntry == None):
        t.failCurrentTest(f"No post tracking entry made")
    elif (f"{postTrackingEntry[0]},{postTrackingEntry[1]},{postTrackingEntry[2]}" == f"{testOrdinal},False,{testPostLink}"):
        t.passCurrentTest(f"Entry={postTrackingEntry[0]},{postTrackingEntry[1]},{postTrackingEntry[2]}")



# Test 6: for downloadPost; 
# Expects:
reset()
t.attemptTest(testGroupName, 6)


# Test 7: for downloadPost; 
# Expects:
reset()
t.attemptTest(testGroupName, 7)


reset()