import os


headers = {"User-Agent": os.getenv("USER_AGENT")}
profileLink = "https://x.com/EveryDayABA"
titleMatch = "Day \\d+ of A\\.B\\.A posting\\."
ordinalMatch = "Day (\\d+) of A\\.B\\.A posting\\."
postMatch = "data-href=\"/EveryDayABA/status/(\\d+)\""
postTrackerFile = "Posts/PostTracker.csv"

