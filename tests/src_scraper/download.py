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
    global testPostHTML
    global testProfileHTML
    global testImageLink
    global testImageFormat # NOTE: This is to be used when code expects you to be able to change the file format; I will magic number "jpg" where there is no control at that scope
    global flag

    testOrdinal = "test"
    referenceOrdinal = "REFERENCE"
    testPostLink = "link"
    testPostHTML = g.testPostHTML
    testProfileHTML = g.testProfileHTML
    testImageLink = "link"
    testImageFormat = "jpg"
    flag = None

    sg.postLinkPrefix = "https://x.com/EveryDayABA/status/"
    sg.postIDMatch = "data-href=\"/EveryDayABA/status/(\\d+)\""



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

testPostHTML = ""

try:
    sd.downloadPostBodyFromHTML(testPostHTML, testOrdinal)
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

sd.downloadPostBodyFromHTML(testPostHTML, testOrdinal)
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

# An exception raised when the post link is invalid should take priority over an exception raised due to the post already being tracked
# This ensures both errors would occur, and in this situation that the priority is correct
st.trackPost(testOrdinal, False, testPostLink)

try:
    sd.downloadPost(testOrdinal, testPostLink)
except Exception as e:
    # A different exception can be raised that is unrelated, which has to be accounted for
    # I am relying on this function only having these two types of exception be possible for this test to work, but I personally think that is okay as that is effectively in the spec for this function
    if (str(e) == f"Post already tracked for ordinal '{testOrdinal}'"):
        t.failCurrentTest(f"Incorrect exception priority: Exception text={e}")
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


# Test 7: for downloadPost; checks if an exception is raised when attempting to download a post that has already been tracked
# Expects: an exception to be raised with the string f"Post already tracked for ordinal '{testOrdinal}'"
# NOTE: Some warnings are expected to be printed during this test; they are however unrelated to what is being tested for
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



# Test 8: for downloadPostIfNotTracked; checks if an exception is raised when the post link is invalid
# Expects: an exception to be raised
# NOTE: I am not testing for a particular exception or test here as the exception should be raised by requests.get, and while there should be a consistent exception thrown by requests.get the point of the test is that we don't care which one it is
reset()
t.attemptTest(testGroupName, 8)

try:
    sd.downloadPostIfNotTracked(testOrdinal, testPostLink)
except Exception as e:
    t.passCurrentTest(f"Exception text={e}")
else:
    t.failCurrentTest(f"No exception raised when expected")


# Test 9: for downloadPostIfNotTracked; checks if the correct flag is raised when attempting to download an untracked post
# Expects: a return value of 0
# NOTE: Some warnings are expected to be printed during this test; they are however unrelated to what is being tested for
reset()
t.attemptTest(testGroupName, 9)

testPostLink = "https://google.com/"

flag = sd.downloadPostIfNotTracked(testOrdinal, testPostLink)
if (flag == 0):
    t.passCurrentTest(f"Post correctly downloaded when not already tracked: flag={flag}")
else:
    t.failCurrentTest(f"Post failed to download despite being untracked: flag={flag}")


# Test 10: for downloadPostIfNotTracked; checks if the correct flag is raised when attempting to download a tracked post
# Expects: a return value of -1
reset()
t.attemptTest(testGroupName, 10)

st.trackPost(testOrdinal, True, testPostLink)

testPostLink = "https://google.com/"

flag = sd.downloadPostIfNotTracked(testOrdinal, testPostLink)
if (flag == -1):
    t.passCurrentTest(f"Post correctly failed to download due to being tracked: flag={flag}")
else:
    t.failCurrentTest(f"Post incorrectly downloaded when already tracked: flag={flag}")


# This is used for tests where downloadMostRecentPostFromProfileHTML is expected to throw exceptions
def testForSpecificException_downloadMostRecentPostFromProfileHTML(exceptionText):
    try:
        sd.downloadMostRecentPostFromProfileHTML(testProfileHTML)
    except Exception as e:
        if (str(e) == exceptionText):
            t.passCurrentTest(f"Exception text={e}")
        else:
            t.failCurrentTest(f"Incorrect exception: Exception text={e}")
    else:
        t.failCurrentTest(f"No exception raised when expected")


# Test 11: for downloadMostRecentPostFromProfileHTML; checks if an exception is raised when no ordinal is found (and a no link exception is raised)
# Expects: an exception to be raised with the string "No ordinal found in profileHTML"
# NOTE: this exception should be raised first, before either the exception for no link or invalid link; no link and invalid link are mutually exclusive, so a test for each case is required
reset()
t.attemptTest(testGroupName, 11)

testProfileHTML = ""
testForSpecificException_downloadMostRecentPostFromProfileHTML("No ordinal found in profileHTML")


# Test 12: for downloadMostRecentPostFromProfileHTML; checks if an exception is raised when no ordinal is found (and an invalid link exception is raised)
# Expects: an exception to be raised with the string "No ordinal found in profileHTML"
# NOTE: this exception should be raised first, before either the exception for no link or invalid link; no link and invalid link are mutually exclusive, so a test for each case is required
reset()
t.attemptTest(testGroupName, 12)

sg.postLinkPrefix = "" # This makes the link invalid

testProfileHTML = "data-href=\"/EveryDayABA/status/1\""
testForSpecificException_downloadMostRecentPostFromProfileHTML("No ordinal found in profileHTML")


# Test 13: for downloadMostRecentPostFromProfileHTML; checks if an exception is raised when no post link is found (and an ordinal is found)
# Expects: an exception to be raised with the string "No post link found in profileHTML"
reset()
t.attemptTest(testGroupName, 13)

testProfileHTML = "Day 1 of A.B.A posting."
testForSpecificException_downloadMostRecentPostFromProfileHTML("No post link found in profileHTML")


# Test 14: for downloadMostRecentPostFromProfileHTML; checks if an exception is raised when an invalid post link is found (and an ordinal is found)
# Expects: an exception to be raised
# NOTE: I am not testing for a particular exception or test here as the exception should be raised by requests.get, and while there should be a consistent exception thrown by requests.get the point of the test is that we don't care which one it is
reset()
t.attemptTest(testGroupName, 14)

sg.postLinkPrefix = "" # This makes the link invalid

testProfileHTML = "data-href=\"/EveryDayABA/status/1\" Day 1 of A.B.A posting."
try:
    sd.downloadMostRecentPostFromProfileHTML(testProfileHTML)
except Exception as e:
    if (str(e) == "No post link found in profileHTML" or str(e) == "No ordinal found in profileHTML"):
        t.failCurrentTest(f"Incorrect exception: Exception text={e}")
    else:
        t.passCurrentTest(f"Exception text={e}")
else:
    t.failCurrentTest(f"No exception raised when expected")


# Test 15: for downloadMostRecentPostFromProfileHTML; checks if the correct flag is raised when attempting to download an untracked post
# Expects: a return value of 0
# NOTE: This is not comprehensive proof of correct downloading, as I am assuming that this function relies on downloadPost and so the proof lies in the tests for that function instead
reset()
t.attemptTest(testGroupName, 15)

testOrdinal = 1
testProfileHTML = f"test Day {testOrdinal} of A.B.A posting."
sg.postLinkPrefix = "https://google.com/"
sg.postIDMatch = "(test)" # I have to assume that a grouping exists in the regex, as I don't see a way of making a test postIDMatch have an arbitrary amount of groupings and the code to not care

try:
    flag = sd.downloadMostRecentPostFromProfileHTML(testProfileHTML)
except Exception as e:
    t.failCurrentTest(f"Exception text={e}")
else:
    if (flag == 0):
        t.passCurrentTest(f"Post correctly downloaded when not already tracked: flag={flag}")
    else:
        t.failCurrentTest(f"Post failed to download despite being untracked: flag={flag}")


# Test 16: for downloadMostRecentPostFromProfileHTML; checks if the correct flag is raised when attempting to download a tracked post
# Expects: a return value of -1
reset()
t.attemptTest(testGroupName, 16)

testOrdinal = 1
testProfileHTML = f"test Day {testOrdinal} of A.B.A posting."
sg.postLinkPrefix = "https://google.com/"
sg.postIDMatch = "(test)" # I have to assume that a grouping exists in the regex, as I don't see a way of making a test postIDMatch have an arbitrary amount of groupings and the code to not care

st.trackPost(testOrdinal, True, testPostLink)

try:
    flag = sd.downloadMostRecentPostFromProfileHTML(testProfileHTML)
except Exception as e:
    t.failCurrentTest(f"Exception text={e}")
else:
    if (flag == -1):
        t.passCurrentTest(f"Post correctly failed to download due to being tracked: flag={flag}")
    else:
        t.failCurrentTest(f"Post incorrectly downloaded when already tracked: flag={flag}")



# Test 17: for downloadMostRecentPostsFromProfileHTML; checks that the output contains nothing when no backlog is found
# Expects: len(output) == 0
reset()
t.attemptTest(testGroupName, 17)

testProfileHTML = ""

output = sd.downloadMostRecentPostsFromProfileHTML(testProfileHTML)

if (len(output) == 0):
    t.passCurrentTest("Correctly downloaded 0 posts when 0 posts were present")
else:
    t.failCurrentTest(f"Output={output}")


# Test 18: for downloadMostRecentPostsFromProfileHTML; checks if all posts found are downloaded when they are not already tracked
# Expects: output to be [0,0,0]
reset()
t.attemptTest(testGroupName, 18)

testOrdinal = 1
testProfileHTML = f"test Day {testOrdinal} of A.B.A posting. test Day {testOrdinal + 1} of A.B.A posting. test Day {testOrdinal + 2} of A.B.A posting."
sg.postLinkPrefix = "https://google.com/"
sg.postIDMatch = "(test)" # I have to assume that a grouping exists in the regex, as I don't see a way of making a test postIDMatch have an arbitrary amount of groupings and the code to not care

output = sd.downloadMostRecentPostsFromProfileHTML(testProfileHTML)

if (all(map(lambda x: x == 0, output))):
    t.passCurrentTest(f"Downloaded: {output.count(0)} posts\noutput={output}")
else:
    t.failCurrentTest(f"Downloaded: {output.count(0)} posts\noutput={output}")

reset()


# Test 19: for downloadMostRecentPostsFromProfileHTML; checks if all posts found are downloaded when some are already tracked
# Expects: output to be [-1,0,-1]
reset()
t.attemptTest(testGroupName, 19)

testOrdinal = 1
testProfileHTML = f"test Day {testOrdinal} of A.B.A posting. test Day {testOrdinal + 1} of A.B.A posting. test Day {testOrdinal + 2} of A.B.A posting."
sg.postLinkPrefix = "https://google.com/"
sg.postIDMatch = "(test)" # I have to assume that a grouping exists in the regex, as I don't see a way of making a test postIDMatch have an arbitrary amount of groupings and the code to not care

st.trackPost(testOrdinal, True, testPostLink)
st.trackPost(testOrdinal + 2, True, testPostLink)

output = sd.downloadMostRecentPostsFromProfileHTML(testProfileHTML)

if (output[0] == -1 and output[1] == 0 and output[2] == -1):
    t.passCurrentTest(f"Downloaded: {output.count(0)} posts\noutput={output}")
else:
    t.failCurrentTest(f"Downloaded: {output.count(0)} posts\noutput={output}")


reset()