import globals as g
import tracking as t
import utils as u

import scraper.utils as su

testGroupName = "utils"

def reset():
    u.reset()

    global testPostLink
    global output1
    global output2
    global file
    global body
    global postLink
    global imageLink
    global testProfileHTML
    global testPostHTML
    global ordinal
    global ordinals

    testPostLink = "link"
    output1 = None
    output2 = None
    file = None
    body = ""
    postLink = ""
    imageLink = ""
    testProfileHTML = g.testProfileHTML
    testPostHTML = g.testPostHTML
    ordinal = ""
    ordinals = [""]

    

# Test 1: for getHTMLFromLink; checks if getting HTML from the same website known to always have the same html consistently twice produces the same HTML
# Expects: output1 == output2
# NOTE: There is no website I can use that I can reliably guarantee produces the same HTML now as in the future, so instead I am checking that it gets the same information from the same source twice in a row
reset()
t.attemptTest(testGroupName, 1)

testPostLink = "https://hasthelargehadroncolliderdestroyedtheworldyet.com/"

output1 = su.getHTMLFromLink(testPostLink)
output2 = su.getHTMLFromLink(testPostLink)
if (output1 == output2):
    #t.passCurrentTest(f"output1={output1}\noutput2={output2}")
    t.passCurrentTest(f"Outputs matched") # To avoid lots of html spam in the test log, I will use this instead on pass
else:
    t.failCurrentTest(f"output1={output1}\noutput2={output2}")


# Test 2: for getHTMLFromLink; checks if getting HTML from two different websites produces different html
# Expects: not output1 == output2
reset()
t.attemptTest(testGroupName, 2)

testPostLink = "https://google.com/"

output1 = su.getHTMLFromLink(testPostLink)

testPostLink = "https://hasthelargehadroncolliderdestroyedtheworldyet.com/"

output2 = su.getHTMLFromLink(testPostLink)
if (not output1 == output2):
    #t.passCurrentTest(f"output1={output1}\noutput2={output2}")
    t.passCurrentTest(f"Outputs correctly did not match") # To avoid lots of html spam in the test log, I will use this instead on pass
else:
    t.failCurrentTest(f"output1={output1}\noutput2={output2}")



# Test 3: for getPostLinkFromProfileHTML; checks if the function returns None when the post link is not there
# Expects: return value of None
reset()
t.attemptTest(testGroupName, 3)

testProfileHTML = ""

postLink = su.getPostLinkFromProfileHTML(testProfileHTML)

if (postLink == None):
    t.passCurrentTest(f"postLink={postLink}")
else:
    t.failCurrentTest(f"postLink={postLink}")


# Test 4: for getPostLinkFromProfileHTML; checks if the function returns g.testPostLink when the post link is present
# Expects: return value of g.testPostLink
reset()
t.attemptTest(testGroupName, 4)

postLink = su.getPostLinkFromProfileHTML(testProfileHTML)

if (postLink == g.testPostLink):
    t.passCurrentTest(f"postLink={postLink}")
else:
    t.failCurrentTest(f"postLink={postLink}")



# Test 5: for getImageLinkFromPostHTML; checks if the function returns None when the image link is not there
# Expects: return value of None
reset()
t.attemptTest(testGroupName, 5)

testPostHTML = ""

imageLink = su.getImageLinkFromPostHTML(testPostHTML)

if (imageLink == None):
    t.passCurrentTest(f"imageLink={imageLink}")
else:
    t.failCurrentTest(f"imageLink={imageLink}")


# Test 6: for getImageLinkFromPostHTML; checks if the function returns g.testImageLink when the image link is present
# Expects: return value of g.testImageLink
reset()
t.attemptTest(testGroupName, 6)

imageLink = su.getImageLinkFromPostHTML(testPostHTML)

if (imageLink == g.testImageLink):
    t.passCurrentTest(f"imageLink={imageLink}")
else:
    t.failCurrentTest(f"imageLink={imageLink}")



# Test 7: for getBodyFromPostHTML; checks if the function returns None when the post body is not there
# Expects: return value of None
reset()
t.attemptTest(testGroupName, 7)

testPostHTML = ""

body = su.getBodyFromPostHTML(testPostHTML)

if (body == None):
    t.passCurrentTest(f"body={body}")
else:
    t.failCurrentTest(f"body={body}")


# Test 8: for getBodyFromPostHTML; checks if the function returns g.testPostBody when the post body is present
# Expects: return value of g.testPostBody
reset()
t.attemptTest(testGroupName, 8)

# In 'real' code it is reasonable to expect only the first step to occur
# That being said, I have added the next two instances of the function to guarantee that when no link is present and when the link is present the body is succesfully returned, as if g.testPostHTML changes it is important both parts of the test occur
# I am hence somewhat tailoring this to the function itself (or, I guess the regex pattern), which while not ideal is necessary for proper testing
# Congratulations this regex and the side effects, you are hence by proxy promoted to being part of the spec :confetti:
body = su.getBodyFromPostHTML(testPostHTML)
body = su.getBodyFromPostHTML("text:\"" + body + "\"")
body = su.getBodyFromPostHTML("text:\"" + body + " https://t.co/test1test2" + "\"")

if (body == g.testPostBody):
    t.passCurrentTest(f"body={body}")
else:
    t.failCurrentTest(f"body={body}")



# Test 9: for getFirstOrdinalFromText; checks if the function returns None when no ordinal is found
# Expects: return value of None
reset()
t.attemptTest(testGroupName, 9)

testProfileHTML = ""

ordinal = su.getFirstOrdinalFromText(testProfileHTML)

if (ordinal == None):
    t.passCurrentTest(f"ordinal={ordinal}")
else:
    t.failCurrentTest(f"ordinal={ordinal}")


# Test 10: for getFirstOrdinalFromText; checks if the function returns g.testOrdinal when the input is g.testProfileHTML
# Expects: return value of g.testOrdinal
reset()
t.attemptTest(testGroupName, 10)

ordinal = su.getFirstOrdinalFromText(testProfileHTML)

if (ordinal == g.testOrdinal):
    t.passCurrentTest(f"ordinal={ordinal}")
else:
    t.failCurrentTest(f"ordinal={ordinal}")


# Test 11: for getOrdinalsFromText; checks if the function returns [] when no ordinal is found
# Expects: return value of []
reset()
t.attemptTest(testGroupName, 11)

testProfileHTML = ""

ordinals = su.getOrdinalsFromText(testProfileHTML)

if (ordinals == []):
    t.passCurrentTest(f"ordinals={ordinals}")
else:
    t.failCurrentTest(f"ordinals={ordinals}")


# Test 12: for getOrdinalsFromText; checks if the function returns a list of ordinals corresponding to the ordinals in the text
# Expects: return value of ["1","3","2"]
reset()
t.attemptTest(testGroupName, 12)

testProfileHTML = "Day 1 of A.B.A posting. Day 3 of A.B.A posting. Day 2 of A.B.A posting."

ordinals = su.getOrdinalsFromText(testProfileHTML)

if (ordinals == ["1","3","2"]):
    t.passCurrentTest(f"ordinals={ordinals}")
else:
    t.failCurrentTest(f"ordinals={ordinals}")