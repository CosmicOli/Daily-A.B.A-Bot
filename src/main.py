from dotenv import load_dotenv
load_dotenv()

import asyncio
import os

import bot.globals as bg
import bot.response as br
import bot.utils as bu
import scraper.download as sd
import scraper.globals as sg
import scraper.utils as su

import bot.commands


try:
    os.mkdir(sg.postsDirectory)
    print("Posts directory created")
except FileExistsError:
    print("Posts directory already exists")

open(sg.postTrackerFile, "a").close()


@bg.client.event
async def on_ready():
    print(f"Logged in as {bg.client.user}")

    profileHTML = su.getHTMLFromLink(sg.profileLink)
    # This try except is legacy, coming from when an exception was raised when no posts were found
    # I've realised that is a bit silly to throw an exception over, as there could just be no backlog posts
    # I am keeping the try except even though I don't think there are any exceptions that can be raised just in case I am wrong 
    try:
        print(f"Found {len(sd.downloadMostRecentPostsFromProfileHTML(profileHTML))} posts for backlog.")
    except Exception as e:
        print(f"WARNING: EXCEPTION OCCURED WHILE DOWNLOADING POST BACKLOG: {e}")

    try:
        bu.updateCurrentDayFromProfileHTML(profileHTML)
        print(f"Current Day:{bg.day}")
    except Exception as e:
        print(f"WARNING: EXCEPTION OCCURED WHILE INITIALIZING CURRENT DAY: {e}")

    await bg.tree.sync()

    asyncio.create_task(br.mainLoop())

    print("Ready")

bg.client.run(os.getenv("DISCORD_TOKEN"))
