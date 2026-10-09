from dotenv import load_dotenv
load_dotenv()

import os
os.environ["POSTS_DIRECTORY"] = f"{os.getenv("POSTS_DIRECTORY")[:-1]}_Test/"

# I clicked random for a while and decided this was what I settled on (xkcd 729)
# I am hard coding it instead of leaving putting it in the .env as I want the test script to be able to run without any user setup
# I hope this is allowed as per the internet archive's rules on web scraping; I couldn't find anything to suggest it isn't but yaknow, my bad if it isn't
os.environ["REFERENCE_IMAGE_LINK"] = "https://imgs.xkcd.com/comics/laser_pointer.png"

import sys
sys.path.insert(1, './src/')

import tracking as t
import utils as u

u.init()

import src_bot.utils
import src_scraper.download

u.remove()

print(f"Passed {t.passed} tests out of {t.attempted} attempted")