import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://x.com/EveryDayABA"
requestForProfileHTML = requests.get(url, headers={"User-Agent":os.getenv("USER_AGENT")})
profileHTML = requestForProfileHTML.content.decode("utf-8") #open("aba.html", "wb").write(requestForProfileHTML.content)

titleMatch = "Day \\d+ of A\\.B\\.A posting\\."
ordinalMatch = "Day (\\d+) of A\\.B\\.A posting\\."

ordinals = re.findall(ordinalMatch, profileHTML)

splitProfile = zip(ordinals, re.split(titleMatch, profileHTML))

#print(list(splitProfile))  

#print(len(list(splitProfile)))

postMatch = "data-href=\"/EveryDayABA/status/(\\d+)\""

for ordinal, html in splitProfile:
    #print(ordinal)
    #print(html)

    postID = re.search(postMatch, html)
    if postID:
        print(f"Day {ordinal}: https://x.com/EveryDayABA/status/{postID.group(1)}")

#currentPost = re.findall(match, profileHTML)

#open("aba.txt", "w").write("\n".join(currentPost))