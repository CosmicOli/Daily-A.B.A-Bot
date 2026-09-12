import asyncio
import os
import re
import requests
import discord
from discord import app_commands
from dotenv import load_dotenv
from collections import OrderedDict

load_dotenv()

# GLOBALS FOR DISCORD BOT
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
boundChannelsFile = "BoundChannels.txt"
postTrackerFile = "PostTracker.csv"

open(boundChannelsFile, "a").close()
open(postTrackerFile, "a").close()

# GLOBALS FOR TWITTER SCRAPING
headers = {"User-Agent": os.getenv("USER_AGENT")}
profileLink = "https://x.com/EveryDayABA"
titleMatch = "Day \\d+ of A\\.B\\.A posting\\."
ordinalMatch = "Day (\\d+) of A\\.B\\.A posting\\."
postMatch = "data-href=\"/EveryDayABA/status/(\\d+)\""

def getHTMLFromLink(postLink):
    requestForPostHTML = requests.get(postLink, headers=headers)
    postHTML = requestForPostHTML.content.decode("utf-8")
    return postHTML

def getPostLinkFromHTML(profileHTML):
    postID = re.search(postMatch, profileHTML)
    if postID:
        postLink = f"https://x.com/EveryDayABA/status/{postID.group(1)}"
    else:
        postLink = None
    return postLink

def getImageLinkFromPostHTML(postHTML):
    imagePartialLink = re.search("src=\"(https://pbs.twimg.com/media/.{15}\\?format=).*?\"", postHTML)
    if (imagePartialLink is None):
        return None
    imageLink = imagePartialLink.group(1) + "jpg&name=4096x4096"
    return imageLink

def getBodyFromPostHTML(postHTML):
    postBody = re.search(f"content=\"({titleMatch}(?s:.)*?)\"", postHTML)
    if (postBody is None):
        return None
    else:
        return postBody.group(1)

def downloadImageFromLink(format, imageLink, title):
    imageFile = open(f"Posts/{title}.{format}", "wb")

    request = requests.get(imageLink, headers=headers)

    if (request.status_code != 200):
        return -1

    imageFile.write(request.content)
    imageFile.close()
    return 0


def trackPost(ordinal, imageExists, link):
    flag = -1
    file = open(postTrackerFile, "r+")
    lines = file.readlines()
    if (not any(re.search(ordinal,x) for x in lines)):
        flag = 0
        file.write(f"{ordinal}, {imageExists}, {link}\n")

    file.close()
    return flag


def downloadPost(ordinal, postLink):
    postHTML = getHTMLFromLink(postLink)
    imageLink = getImageLinkFromPostHTML(postHTML)

    if (downloadImageFromLink("jpg", imageLink, ordinal) == -1 or imageLink is None):
        fileExists = False
        print(f"Day {ordinal} image missing or in incorrect format")
    else:
        fileExists = True

    postBody = getBodyFromPostHTML(postHTML)
    body = open(f"Posts/{ordinal}.txt", "w")
    body.write(postBody)
    body.close

    trackPost(ordinal, fileExists, imageLink)


def downloadMostRecentPost():
    profileHTML = getHTMLFromLink(profileLink)
    ordinal = re.search(ordinalMatch, profileHTML).group(1)
    postLink = getPostLinkFromHTML(profileHTML)

    if postLink is None:
        return -1

    downloadPost(ordinal, postLink)

    return ordinal


def downloadMostRecentPosts():
    profileHTML = getHTMLFromLink(profileLink)
    ordinals = re.findall(ordinalMatch, profileHTML)
    splitProfile = zip(ordinals, re.split(titleMatch, profileHTML))

    for ordinal, html in splitProfile:
        postLink = getPostLinkFromHTML(html)

        if postLink is None:
            continue

        downloadPost(ordinal, postLink)

    return list(OrderedDict.fromkeys(ordinals)) # Only want the list of unique ordinals, not all matches for the ordinals appearing in the html


async def mainLoop():

    while True:
        #currentOrdinal = downloadMostRecentPost()
        #if ()
        await asyncio.sleep(1800) # 30 minutes timer

async def bindBotToChannel(channelID):
    flag = -1
    file = open(boundChannelsFile, "r+")
    if (not any(re.search(channelID,x) for x in file.readlines())):
        file.write(channelID + "\n")
        flag = 0
    file.close()
    return flag

@tree.command(description='Binds the bot to the current channel.', guild=discord.Object(id=1105583914044641370))
async def bind(interaction):
    flag = await bindBotToChannel(str(interaction.channel.id))
    if (flag == 0):
        await interaction.response.send_message(f"Bound to channel: {interaction.channel.name} (ID: {interaction.channel.id})")
    else:
        await interaction.response.send_message(f"Already bound to channel: {interaction.channel.name} (ID: {interaction.channel.id})")

@tree.command(description='Sends the most recent post.', guild=discord.Object(id=1105583914044641370))
async def today(interaction):
    await interaction.response.send_message(file=discord.File())

    
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print(f"Downloaded {len(downloadMostRecentPosts())} posts.")
    await tree.sync(guild=discord.Object(id=1105583914044641370))
    asyncio.create_task(mainLoop())
    print("Ready")

client.run(os.getenv("DISCORD_TOKEN"))
