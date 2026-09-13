import discord

import tracking as t
import utils as u

import bot.globals as bg
import bot.utils as bu
import scraper.globals as sg
import scraper.tracker as st

testGroupName = "utils"

def reset():
    u.reset()

    global testOrdinal
    global testBody
    global testBodyFile
    global testLink
    global content
    global image

    testOrdinal = "test"
    testBody = "body"
    testBodyFile = None
    testLink = "link"
    content = ""
    image = None
    


# Test 1: for updateCurrentDay; checks if current day updates
# Expects: the day to change from -1
# NOTE: Cannot test against a known 'correct' day, so this only checks for a change in day
reset()
t.attemptTest(testGroupName, 1)

bg.day = -1
bu.updateCurrentDay()
if (bg.day != -1):
    t.passTest(testGroupName, 1, f"day={bg.day}")
else:
    t.failTest(testGroupName, 1, f"day={bg.day}")


# NOTE: There are 4 relevant binary variables for generateMessageContentAndImage: entry, entry[1] (whether an image is expected), content, image
# This means on paper there are 16 tests to do, however I am reducing all tests where "entry" does not exist into one as if an exception is thrown (as is tested for) then no code associated with these other variables can ever run
# Hence, there are 8 tests + 1 test for no entry, totalling 9; the last test for generateMessageContentAndImage should hence be test 10

# NOTE 2: I have split generateMessageContent and generateMessageImage up, and as they are independant I *could* rewrite the tests to remove 2 test cases... but I cannot be bothered right now
# The following tests still correctly test the entire functionality, just excessively so

# Test 2: for generateMessageContentAndImage; checks if exception thrown when no entry found
# Expects: an exception to be raised
reset()
t.attemptTest(testGroupName, 2)

try:
    content, image = bu.generateMessageContentAndImage(testOrdinal)
except:
    t.passTest(testGroupName, 2, "Exception thrown")
else:
    t.failTest(testGroupName, 2, "Exception should have been raised")


# Test 3: for generateMessageContentAndImage; checks when entry, no files for body or image, entry has marked it expects no image
# Expects: content=f"\n{testLink}" and image=None
reset()
t.attemptTest(testGroupName, 3)

st.trackPost(testOrdinal, False, testLink)
content, image = bu.generateMessageContentAndImage(testOrdinal)

if (content == f"\n{testLink}" and image == None):
    t.passTest(testGroupName, 3, f"\ncontent='{content}'\nimage='{image}'")
else:
    t.failTest(testGroupName, 3, f"\ncontent='{content}'\nimage='{image}'")


# Test 4: for generateMessageContentAndImage; checks when entry, no files for body or image, entry has marked it expects an image
# Expects: content=f"\n{testLink}" and image=None
# NOTE: There should be a warning printed with this test
reset()
t.attemptTest(testGroupName, 4)

st.trackPost(testOrdinal, False, testLink)
content, image = bu.generateMessageContentAndImage(testOrdinal)

if (content == f"\n{testLink}" and image == None):
    t.passTest(testGroupName, 4, f"\ncontent='{content}'\nimage='{image}'")
else:
    t.failTest(testGroupName, 4, f"\ncontent='{content}'\nimage='{image}'")


# Test 5: for generateMessageContentAndImage; entry and file for body exists, no file for image exists, entry has marked it expects no image
# Expects: content=f"{testBody}\n{testLink}" and image=None
reset()
t.attemptTest(testGroupName, 5)

testBodyFile = open(f"{sg.postsDirectory}{testOrdinal}.txt", "w")
testBodyFile.write(testBody)
testBodyFile.close()

st.trackPost(testOrdinal, False, testLink)
content, image = bu.generateMessageContentAndImage(testOrdinal)

if (content == f"{testBody}\n{testLink}" and image == None):
    t.passTest(testGroupName, 5, f"\ncontent='{content}'\nimage='{image}'")
else:
    t.failTest(testGroupName, 5, f"\ncontent='{content}'\nimage='{image}'")


# Test 6: for generateMessageContentAndImage; entry and file for body exists, no file for image exists, entry has marked it expects an image
# Expects: content=f"{testBody}\n{testLink}" and image=None
# NOTE: There should be a warning printed with this test
reset()
t.attemptTest(testGroupName, 6)

testBodyFile = open(f"{sg.postsDirectory}{testOrdinal}.txt", "w")
testBodyFile.write(testBody)
testBodyFile.close()

st.trackPost(testOrdinal, True, testLink)
content, image = bu.generateMessageContentAndImage(testOrdinal)

if (content == f"{testBody}\n{testLink}" and image == None):
    t.passTest(testGroupName, 6, f"\ncontent='{content}'\nimage='{image}'")
else:
    t.failTest(testGroupName, 6, f"\ncontent='{content}'\nimage='{image}'")


# Test 7: for generateMessageContentAndImage; entry and file for image exists, no file for body exists, entry has marked it expects no image
# Expects: content=f"\n{testLink}" and image=None
reset()
t.attemptTest(testGroupName, 7)

open(f"{sg.postsDirectory}{testOrdinal}.jpg", "w").close()

st.trackPost(testOrdinal, False, testLink)
content, image = bu.generateMessageContentAndImage(testOrdinal)

if (content == f"\n{testLink}" and image == None):
    t.passTest(testGroupName, 7, f"\ncontent='{content}'\nimage='{image}'")
else:
    t.failTest(testGroupName, 7, f"\ncontent='{content}'\nimage='{image}'")


# Test 8: for generateMessageContentAndImage; entry and file for image exists, no file for body exists, entry has marked it expects an image
# Expects: content=f"\n{testLink}" and image to be a discord.File object
reset()
t.attemptTest(testGroupName, 8)

open(f"{sg.postsDirectory}{testOrdinal}.jpg", "w").close()

st.trackPost(testOrdinal, True, testLink)
content, image = bu.generateMessageContentAndImage(testOrdinal)

if (content == f"\n{testLink}" and isinstance(image,discord.File)):
    t.passTest(testGroupName, 8, f"\ncontent='{content}'\nimage='{image}'")
else:
    t.failTest(testGroupName, 8, f"\ncontent='{content}'\nimage='{image}'")


# Test 9: for generateMessageContentAndImage; entry file and image exist, entry has marked it expects no image
# Expects: content=f"{testBody}\n{testLink}" and image=None
reset()
t.attemptTest(testGroupName, 9)

testBodyFile = open(f"{sg.postsDirectory}{testOrdinal}.txt", "w")
testBodyFile.write(testBody)
testBodyFile.close()

open(f"{sg.postsDirectory}{testOrdinal}.jpg", "w").close()

st.trackPost(testOrdinal, False, testLink)
content, image = bu.generateMessageContentAndImage(testOrdinal)

if (content == f"{testBody}\n{testLink}" and image == None):
    t.passTest(testGroupName, 9, f"\ncontent='{content}'\nimage='{image}'")
else:
    t.failTest(testGroupName, 9, f"\ncontent='{content}'\nimage='{image}'")


# Test 10: for generateMessageContentAndImage; entry file and image exist, entry has marked it expects no image
# Expects: content=f"{testBody}\n{testLink}" and image to be a discord.File object
reset()
t.attemptTest(testGroupName, 10)

testBodyFile = open(f"{sg.postsDirectory}{testOrdinal}.txt", "w")
testBodyFile.write(testBody)
testBodyFile.close()

open(f"{sg.postsDirectory}{testOrdinal}.jpg", "w").close()

st.trackPost(testOrdinal, True, testLink)
content, image = bu.generateMessageContentAndImage(testOrdinal)

if (content == f"{testBody}\n{testLink}" and isinstance(image,discord.File)):
    t.passTest(testGroupName, 10, f"\ncontent='{content}'\nimage='{image}'")
else:
    t.failTest(testGroupName, 10, f"\ncontent='{content}'\nimage='{image}'")


# I believe as image will equal a test file, it blocks the test file from being deleted without calling a reset
reset()