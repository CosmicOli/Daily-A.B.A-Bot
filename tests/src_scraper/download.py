import os

import tracking as t
import globals as g
import utils as u

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
else:
    t.failCurrentTest("No exception raised when expected")


# Test 2: for downloadImageFromLink; checks if a valid image link downloads the correct image
# Expects: the same image as the reference image to be downloaded
# NOTE: the expectation is that twitter images are all .jpg, however this part of code is written to account for all file formats
# NOTE: a non twitter source has been chosen as twitter has harsh rate limiting, and I want to avoid tests failing due to server side issues
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



# Test 3: for downloadPostBodyFromHTML; checks if an exception is raised if no post body is found in the HTML
# Expects: an exception to be raised with the string "No post body found in HTML"
reset()
t.attemptTest(testGroupName, 3)

try:
    sd.downloadPostBodyFromHTML("", testOrdinal)
except Exception as e:
    if (str(e) == "No post body found in HTML"):
        t.passCurrentTest(f"Exception text={e}")
    else:
        t.failCurrentTest(f"Exception text={e}")
else:
    t.failCurrentTest("No exception raised when expected")


# Test 4: for downloadPostBodyFromHTML; checks if the correct body is saved to the correct file upon given a valid post HTML
# Expects: the test body to be saved to the correct file
reset()
t.attemptTest(testGroupName, 4)

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



# NOTE: Twitter has harsh rate limiting, so links to twitter will not be used when testing downloadPost; this however leads to some unfortunate holes in the tests
# The most obvious hole is that these tests do not verify that the correct things happen when the correct link is provided
# This is not great, but on paper a failure in this function should be easy to spot manually as post bodies or images will consistently be missing
# Plus, on paper the only functionality not tested here is specific case handling of other fully tested functions, so an error should be 'self contained' to this function
# Broadly however, I would not be able to do a full test without custom webpages regardless
# E.g. I cannot test for when a post body exists but no image, or vice versa
# E.g. I cannot test the case where an invalid http code exception occurs when downloading the image

# NOTE: I am not testing for different states of the PostTracker.csv file here with the exception of the 'obvious' cases of the post having already been tracked or not
# This is because io to this file is tested to follow a standard that should have no conceptual issues, and frankly hence I do not want to have to account for cases that don't follow this standard
# And yaknow, if I am wrong about the lack of notable conceptual issues then I guess I will cross that bridge when I get to it

# Test 5: for downloadPost; checks if an exception is raised when the post link is invalid
# Expects: an exception to be raised
# NOTE: I am not testing for a particular exception or test here as the exception should be raised by requests.get, and while there should be a consistent exception thrown by requests.get the point of the test is that we don't care which one it is
reset()
t.attemptTest(testGroupName, 5)

try:
    sd.downloadPost(testOrdinal, "")
except Exception as e:
    # A different exception can be raised that is unrelated, which has to be accounted for
    # I am relying on this function only having these two types of exception be possible for this test to work, but I personally think that is okay as that is effectively in the spec for this function
    if (str(e) == f"Post already tracked for ordinal '{testOrdinal}'"):
        t.failCurrentTest(f"Exception text={e}")
    else:
        t.passCurrentTest(f"Exception text={e}")
else:
    t.failCurrentTest(f"No exception raised when expected")


# Test 6: for downloadPost; checks if a valid link (a link that produces html with http code 200) that doesn't produce twitter post html produces the right entry information
# Expects: the entry to be f"{testOrdinal},False,{testPostLink}" and for no image or text files to be created
# NOTE: Some warnings are expected to be printed during this test; to test for these warning I am testing whether the files that they warn are not created indeed are not
reset()
t.attemptTest(testGroupName, 6)

# Look if google is down we have bigger problems than whether my code passes these tests
testPostLink = "https://google.com/"
try:
    sd.downloadPost(testOrdinal, testPostLink)
except Exception as e:
    t.failCurrentTest(f"Exception text={e}")

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


# Test 7: for downloadPost; 
# Expects:
reset()
t.attemptTest(testGroupName, 7)

st.trackPost(testOrdinal, True, testPostLink)

testPostLink = "https://google.com/"

try:
    sd.downloadPost(testOrdinal, testPostLink)
except Exception as e:
    if (str(e) == f"Post already tracked for ordinal '{testOrdinal}'"):
        t.passCurrentTest(f"Exception text={e}")
    else:
        t.failCurrentTest(f"Exception text={e}")


# Test 8: for downloadPost; 
# Expects:
reset()
t.attemptTest(testGroupName, 8)


reset()