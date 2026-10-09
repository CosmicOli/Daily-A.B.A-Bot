import discord

import tracking as t
import utils as u

import bot.globals as bg
import bot.utils as bu
import scraper.globals as sg
import scraper.tracker as st
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

# Test 1: for downloadImageFromLink, 
# Expects: 
reset()
t.attemptTest(testGroupName, 1)