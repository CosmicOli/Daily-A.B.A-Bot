from dotenv import load_dotenv
load_dotenv()

import os
os.environ["POSTS_DIRECTORY"] = f"{os.getenv("POSTS_DIRECTORY")[:-1]}_Test/"

import sys
sys.path.insert(1, './src/')

import tracking as t
import utils as u

u.init()

import src_bot.utils

u.remove()

print(f"Passed {t.passed} tests out of {t.attempted} attempted")