from dotenv import load_dotenv
load_dotenv()

import asyncio
import os

import bot.globals as bg
import bot.response as br
import bot.utils as bu
import scraper.download as sd
import scraper.globals as sg

import bot.commands


try:
    os.mkdir("Posts")
    print("Posts directory created")
except FileExistsError:
    print("Posts directory already exists")

open(sg.postTrackerFile, "a").close()


@bg.client.event
async def on_ready():
    print(f"Logged in as {bg.client.user}")
    print(f"Found {len(sd.downloadMostRecentPosts())} posts for backlog.")
    bu.updateCurrentDay()
    print(f"Current Day:{bg.day}")
    await bg.tree.sync()
    asyncio.create_task(br.mainLoop())
    print("Ready")

bg.client.run(os.getenv("DISCORD_TOKEN"))
