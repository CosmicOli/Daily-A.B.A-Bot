import os


headers = {"User-Agent": os.getenv("USER_AGENT")}
profileLink = "https://x.com/EveryDayABA"
titleMatch = "Day \\d+ of A\\.B\\.A posting\\."
ordinalMatch = "Day (\\d+) of A\\.B\\.A posting\\."
postMatch = "data-href=\"/EveryDayABA/status/(\\d+)\""
postsDirectory = f"{os.getenv("POSTS_DIRECTORY")}"
postTrackerFile = f"{postsDirectory}PostTracker.csv"

