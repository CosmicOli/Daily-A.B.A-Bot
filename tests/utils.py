import os
import shutil

import requests

import bot.globals as bg
import scraper.globals as sg


# To avoid the test script requiring manual setup or git tracked reference files, I am using this function that is as of implementation identical to the one in the main script
# Based on manual testing I would say this works (at least for now), so I deem it 'good enough' to be used to pull a reference image for testing purposes
def downloadReferenceImageFromLink(format: str, imageLink: str, title: str):
    imageFile = open(f"{sg.postsDirectory}{title}.{format}", "wb")

    request = requests.get(imageLink, headers=sg.headers)

    # I know technically any code beginning with 2 is 'successful' but I expect a code of 200 and am gonna stick with that for now
    if (request.status_code != 200):
        raise Exception(f"Image request failed with status code '{request.status_code}'")

    imageFile.write(request.content)
    imageFile.close()


def init():
    try:
        os.mkdir(sg.postsDirectory)
        #print("Posts directory created")
    except FileExistsError:
        #print("Posts directory already exists")
        pass

    open(sg.postTrackerFile, "a").close()


def remove():
    shutil.rmtree(sg.postsDirectory, ignore_errors=True)


def reset():
    remove()
    init()