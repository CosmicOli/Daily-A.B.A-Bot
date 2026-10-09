import sys

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
    print(f"Found {len(sd.downloadMostRecentPostsFromProfileHTML(profileHTML))} posts for backlog.")

    try:
        bu.updateCurrentDayFromProfileHTML(profileHTML)
        print(f"Current Day:{bg.day}")
    except Exception as e:
        print("UNABLE TO INITIALIZE CURRENT DAY: " + str(e))
        sys.exit(-1)

    await bg.tree.sync()

    asyncio.create_task(br.mainLoop())

    print("Ready")

bg.client.run(os.getenv("DISCORD_TOKEN"))
