import asyncio
import os
import re
import requests
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

# GLOBALS FOR DISCORD BOT
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
day = 0
channels = []

# GLOBALS FOR TWITTER SCRAPING
headers = {"User-Agent": os.getenv("USER_AGENT")}
profileLink = "https://x.com/EveryDayABA"
titleMatch = "Day \\d+ of A\\.B\\.A posting\\."
ordinalMatch = "Day (\\d+) of A\\.B\\.A posting\\."
postMatch = "data-href=\"/EveryDayABA/status/(\\d+)\""
postTrackerFile = "PostTracker.csv"
open(postTrackerFile, "a").close()

try:
    os.mkdir("Posts")
    print("Posts directory created")
except FileExistsError:
    print("Posts directory already exists")



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
    file = open(postTrackerFile, "a+")
    file.write(f"{ordinal},{imageExists},{link}\n")
    file.close()


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

    trackPost(ordinal, fileExists, postLink)


def getPostTrackingEntry(ordinal):
    file = open(postTrackerFile, "r")
    lines = file.readlines()
    file.close()

    matchingEntries = [x for x in lines if x.split(",")[0] == ordinal]

    if (len(matchingEntries) == 0):
        return False
    
    entry = matchingEntries[0].split(",")

    return entry


def downloadPostIfNotDownloaded(ordinal, postLink):
    flag = -1
    
    if (not getPostTrackingEntry(ordinal)):
        flag = 0
        downloadPost(ordinal, postLink)
        print(f"Post {ordinal} downloaded")
    else:
        print(f"Post {ordinal} already downloaded, skipping")
    return flag
    

def downloadMostRecentPost():
    profileHTML = getHTMLFromLink(profileLink)
    ordinal = re.search(ordinalMatch, profileHTML).group(1)
    postLink = getPostLinkFromHTML(profileHTML)

    if postLink is None:
        return -1

    return downloadPostIfNotDownloaded(ordinal, postLink)


def downloadMostRecentPosts():
    profileHTML = getHTMLFromLink(profileLink)
    ordinals = re.findall(ordinalMatch, profileHTML)
    splitProfile = zip(ordinals, re.split(titleMatch, profileHTML))

    counter = 0
    output = []
    for ordinal, html in splitProfile:
        postLink = getPostLinkFromHTML(html)

        if postLink is None:
            continue

        counter += 1
        output.append(downloadPostIfNotDownloaded(ordinal, postLink))

    if (counter == 0):
        return -1
    else:
        return output


def updateCurrentDay():
    profileHTML = getHTMLFromLink(profileLink)
    global day 
    day = re.search(ordinalMatch, profileHTML).group(1)


def generateMessageContent(ordinal):
    entry = getPostTrackingEntry(ordinal)
    if (not entry):
        return -1

    if (entry[1]):
        image = discord.File(f"Posts/{ordinal}.jpg")
    else:
        image = None

    bodyFile = open(f"Posts/{ordinal}.txt")
    body = bodyFile.read()
    bodyFile.close()

    return (body + "\n" + entry[2]), image


async def sendMessageToChannel(channel, content, image):
    removeEmbed = True
    if (image is None):
        removeEmbed = False

    message = await channel.send(content=content, file=image)
    await message.edit(suppress=removeEmbed)


async def sendPostToChannels(ordinal):
    content, image = generateMessageContent(ordinal)

    for channel in channels:
        await sendMessageToChannel(channel, content, image)
    return 0


async def mainLoop():
    while True:
        await asyncio.sleep(1800) # 30 minutes timer
        flag = downloadMostRecentPost()

        if (flag == 0):
            updateCurrentDay()

            await sendPostToChannels(day)


async def respondWithPost(interaction: discord.Interaction, content: str, image: discord.File):
    removeEmbed = True
    if (image is None):
        removeEmbed = False
    
    await interaction.response.send_message(content=content, file=image, suppress_embeds = removeEmbed)


async def bindBotToChannel(channel: discord.channel):
    if (not channel in channels):
        channels.append(channel)
        return 0
    else:
        return 1
    

@tree.command(description='Binds the bot to the current channel or thread.')
async def bind(interaction: discord.Interaction):
    flag = await bindBotToChannel(interaction.channel)
    if (flag == 0):
        await interaction.response.send_message(f"Bound to channel #{interaction.channel.name} (ID: {interaction.channel.id}) in server {interaction.guild.name} (ID: {interaction.guild.id})")
    else:
        await interaction.response.send_message(f"Already bound to channel #{interaction.channel.name} (ID: {interaction.channel.id}) in server {interaction.guild.name} (ID: {interaction.guild.id})")


@tree.command(name="today", description="Sends the most recent post.")
async def today(interaction: discord.Interaction):
    content, image = generateMessageContent(day)
    await respondWithPost(interaction, content, image)


@tree.command(name="day", description="Sends a specified post, if it is cached by the bot")
async def day(interaction: discord.Interaction, day: str):
    entry = getPostTrackingEntry(day)
    if (not entry):
        await interaction.response.send_message(f"This bot instance has not cached day \"{day}\".")
        return
    
    content, image = generateMessageContent(day)
    await respondWithPost(interaction, content, image)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print(f"Found {len(downloadMostRecentPosts())} posts for backlog.")
    updateCurrentDay()
    print(f"Current Day:{day}")
    await tree.sync()
    asyncio.create_task(mainLoop())
    print("Ready")

client.run(os.getenv("DISCORD_TOKEN"))
