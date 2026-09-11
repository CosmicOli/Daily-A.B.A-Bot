import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {"User-Agent": os.getenv("USER_AGENT")}

url = "https://x.com/EveryDayABA"
requestForProfileHTML = requests.get(url, headers=headers)
profileHTML = requestForProfileHTML.content.decode("utf-8") #open("aba.html", "wb").write(requestForProfileHTML.content)

titleMatch = "Day \\d+ of A\\.B\\.A posting\\."
ordinalMatch = "Day (\\d+) of A\\.B\\.A posting\\."

ordinals = re.findall(ordinalMatch, profileHTML)

splitProfile = zip(ordinals, re.split(titleMatch, profileHTML))

postMatch = "data-href=\"/EveryDayABA/status/(\\d+)\""

for ordinal, html in splitProfile:
    postID = re.search(postMatch, html)
    if postID:
        postLink = f"https://x.com/EveryDayABA/status/{postID.group(1)}"
        requestForPostHTML = requests.get(postLink, headers=headers)
        postHTML = requestForPostHTML.content

        # The scraped site allows the image ID to be found, but then a format and size that seems to be standard is appended to the end of the link to get the image
        imagePartialLink = re.search("src=\"(https://pbs.twimg.com/media/.{15}\\?format=).*?\"", postHTML.decode("utf-8"))
        imageLink = imagePartialLink.group(1) + "jpg&name=4096x4096"

        imageFile = open(f"Posts/{ordinal}.jpg", "wb")
        imageFile.write(requests.get(imageLink, headers=headers).content)
        imageFile.close()