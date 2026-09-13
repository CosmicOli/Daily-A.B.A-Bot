import os
import shutil

import bot.globals as bg
import scraper.globals as sg


def init():
    try:
        os.mkdir(sg.postsDirectory)
        #print("Posts directory created")
    except FileExistsError:
        #print("Posts directory already exists")
        pass

    open(sg.postTrackerFile, "a").close()


def remove():
    bg.day = 0
    shutil.rmtree(sg.postsDirectory, ignore_errors=True)


def reset():
    remove()
    init()