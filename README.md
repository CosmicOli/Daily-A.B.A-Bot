# Daily-A.B.A-Bot
A simple discord bot for posting the daily A.B.A post from https://x.com/EveryDayABA

Uses the python library [requests](https://pypi.org/project/requests/) to web-scrape the most recent daily post.  

# Information

Web scraping is used over the [X API](https://docs.x.com/x-api/introduction) or a proxy API to avoid the lack-of or small-number-of free number of requests.  
This being said, caching of the images to disk is used to avoid any significant number of requests being sent.  

# Plan
Two halves  
-> twitter scraper  
-> -> does daily requests (or more likely hourly until a new post is detected)  
-> discord bot  
-> -> has a command to bind a new channel to post the daily post into  
-> -> upon a new post being detected by the twitter scraper, the bot will then send a message with the twitter post and content to each bound channel  