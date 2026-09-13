# Daily-A.B.A-Bot
A simple discord bot for posting the daily A.B.A post from https://x.com/EveryDayABA
  
Uses the python library [requests](https://pypi.org/project/requests/) to web-scrape the most recent daily post.  
  
This was made not in association with @EveryDayABA

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
These will be in a directory that is created upon first run, called `Posts`.  
E.g. Day 250's image will be at `Posts/250.jpg`.