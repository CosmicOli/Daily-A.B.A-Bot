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
    imageLink = imagePartialLink.group(1) + "jpg&name=4096x4096"
    return imageLink

def downloadImageFromLink(format, imageLink, title):
    imageFile = open(f"Posts/{title}.{format}", "wb")
    imageFile.write(requests.get(imageLink, headers=headers).content)
    imageFile.close()


def downloadMostRecentPost():
    profileHTML = getHTMLFromLink(profileLink)
    ordinal = re.search(ordinalMatch, profileHTML).group(1)
    postLink = getPostLinkFromHTML(profileHTML)

    if postLink is None:
        print("No post found, defaulting to embed.")
        return
    
    postHTML = getHTMLFromLink(postLink)
    imageLink = getImageLinkFromPostHTML(postHTML)
    downloadImageFromLink("jpg", imageLink, ordinal)


def downloadMostRecentPosts():
    profileHTML = getHTMLFromLink(profileLink)
    ordinals = re.findall(ordinalMatch, profileHTML)
    splitProfile = zip(ordinals, re.split(titleMatch, profileHTML))

    for ordinal, html in splitProfile:
        postLink = getPostLinkFromHTML(html)

        if postLink is None:
            continue

        postHTML = getHTMLFromLink(postLink)
        imageLink = getImageLinkFromPostHTML(postHTML)
        downloadImageFromLink("jpg", imageLink, ordinal)

async def bindBotToChannel(channelID):
    flag = -1
    file = open("BoundChannels.txt", "r+")
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
    #downloadMostRecentPosts()
    #print(f"Downloaded {len(os.listdir('Posts'))} posts.")
    await tree.sync(guild=discord.Object(id=1105583914044641370))
    print("Ready")

client.run(os.getenv("DISCORD_TOKEN"))
