import re

import tracking as t
import utils as u

import scraper.globals as sg
import scraper.tracker as st

testGroupName = "tracker"

def reset():
    u.reset()

    global testOrdinal
    global testPostLink
    global output
    global file
    global postTrackerFileContents

    testOrdinal = "test"
    testPostLink = "link"
    output = None
    file = None
    postTrackerFileContents = None

    sg.postLinkPrefix = "https://x.com/EveryDayABA/status/"
    sg.postIDMatch = "data-href=\"/EveryDayABA/status/(\\d+)\""


# NOTE: I am not adding tests for what happens in erronious or comprehensive data situations, e.g. only one comma in an entry, lots of different files already in the tracker, etc
# This is because both of these functions should adhere to a standard that avoids incorrect data being written in or read, and that standard is being tested to
# The one case I do check for erronious data is when it is expected; that is in particular when an entry with the same ordinal already exists when attempting to add one, or trying to read an entry that doesn't exist


# Test 1: for getPostTrackingEntry; checks that when attempting to retrieve an entry that doesn't exist, None is returned
# Expects: the return value to be None
reset()
t.attemptTest(testGroupName, 1)

# While uneccessary and not comprehensive, I am adding this as a sanity check to make sure that the existence of a non-colliding entry doesn't break anything
st.trackPost(testOrdinal + testOrdinal, True, testPostLink)

output = st.getPostTrackingEntry(testOrdinal)
if (output == None):
    t.passCurrentTest(f"output={output}")
else:
    t.failCurrentTest(f"output={output}")


# Test 2: for getPostTrackingEntry; checks that when attempting to retrieve an entry that does exist, the whole entry is returned
# Expects: the return value to be [testOrdinal, "True", testPostLink]
reset()
t.attemptTest(testGroupName, 2)

st.trackPost(testOrdinal, True, testPostLink)

output = st.getPostTrackingEntry(testOrdinal)
if (output == [testOrdinal, "True", testPostLink]):
    t.passCurrentTest(f"output={output}")
else:
    t.failCurrentTest(f"output={output}")



# Test 3: for trackpost; checks that when attempting to track a post that does not exist, the post is tracked
# Expects: f"{testOrdinal},True,{testPostLink}\n" to be added to the tracker file
reset()
t.attemptTest(testGroupName, 3)

# While uneccessary and not comprehensive, I am adding this as a sanity check to make sure that the existence of a non-colliding entry doesn't break anything
st.trackPost(testOrdinal + testOrdinal, True, testPostLink)

st.trackPost(testOrdinal, True, testPostLink)

file = open(sg.postTrackerFile, "r")
postTrackerFileContents = file.read()
file.close()

if (re.search(f"{testOrdinal},True,{testPostLink}\n", postTrackerFileContents)):
    t.passCurrentTest(f"postTrackerFileContents={postTrackerFileContents}")
else:
    t.failCurrentTest(f"postTrackerFileContents={postTrackerFileContents}")


# Test 4: for trackpost; checks that when attempting to track a post that does exist, the post is not tracked
# Expects: an exception to be raised with the string f"Post already tracked for ordinal '{testOrdinal}'"
reset()
t.attemptTest(testGroupName, 4)

st.trackPost(testOrdinal, False, testPostLink)
testPostLink = "different"
try:
    st.trackPost(testOrdinal, True, testPostLink)
except Exception as e:
    if (str(e) == f"Post already tracked for ordinal '{testOrdinal}'"):
        t.passCurrentTest(f"Exception text={e}")
    else:
        t.failCurrentTest(f"Exception text={e}")
else:
    t.failCurrentTest("No exception raised when expected")