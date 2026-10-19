# Daily-A.B.A-Bot
A simple discord bot for posting the daily A.B.A post from https://x.com/EveryDayABA
  
Uses the python library [requests](https://pypi.org/project/requests/) to web-scrape the most recent daily post  
  
This was not made in association with @EveryDayABA  

# Setup
This setup assumes knowledge of how to run python scripts, write .env files, and install python libraries  
  
A .env file needs to be created in the root directory of this repository, with three environment variables:  
- USER_AGENT: The user-agent http header for your bot instance, used for web-scraping  
- DISCORD_TOKEN: The discord bot token for your bot instance, used to connect the running code to a particular discord bot  
- POSTS_DIRECTORY: A specified directory for your downloaded posts and tracking file to reside  
  
The following non-standard libraries need installing for this project:
- discord.py
- dotenv
- requests

Before first running the bot, run tests/main.py; if there is a discrepency between the number of tests attempted and tests passed, consult the particular test logs for the failed tests. It may be the case that due to spotty internet, certain tests fail; if this is the case, the bot may function correctly regardless but it is recommended that a stable internet is used for the most reliable experience.  
NOTE: It is not guaranteed that the bot will work when passing all tests, just that it is very likely to work; this is elaborated on in Information below
NOTE: There should be more than 0 tests attempted
  
To run the bot, run src/main.py  
  
# Information

Web scraping is used over the [X API](https://docs.x.com/x-api/introduction) or a proxy API to avoid the lack-of or small-number-of free number of requests.  
This being said, caching of the images to disk is used to avoid any significant number of requests being sent.  
  
Posts are tracked in a file called PostTracker.csv.  
If a post is untracked in PostTracker.csv, it does not matter if there is a file associated to a day as this file takes precident.  
Each entry is in the format `day,image_found,link`  
-> `day` refers to the current post day  
-> `image_found` refers to whether an image was downloaded in association to the post  
-> `link` refers to the link to the post  
NOTE: `image_found` is potentially unimportant, however it exists as a failsafe in case not every image is a jpg (which it is unclear if twitter always converts photos into)  
  
Post image and body are stored in the format `day.jpg` and `day.txt` respectively.  
These will be in a directory that is created upon first run (if it doesn't already exist), which is defined by the user defined environment variable "POSTS_DIRECTORY"  
  
The tests cover most functionality of the bot, but misses some notable "untestable" holes:  
- Anything sending or receiving to or from discord  
- Any x.com specific downloading/processing (this is technically not untestable, however x.com has harsh rate-limit rules so I opted out of requiring requests to x.com in the test cases; in most cases however, x.com is simply replaced with a non-rate-limited source)  
  
NOTE: Tests were written to test that functions adhere to a correct standard, and the code was rewritten to fit that standard if it did not; mostly, the tests are designed to be testing the effects of functions and not 'how' those effects are produced, such that any solution to the problems that fit the standards will pass the tests  