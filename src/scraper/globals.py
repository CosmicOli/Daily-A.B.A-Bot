import os


headers = {"User-Agent": os.getenv("USER_AGENT")}
profileLink = "https://x.com/EveryDayABA"
titleMatch = "Day \\d+ of A\\.B\\.A posting\\."
ordinalMatch = "Day (\\d+) of A\\.B\\.A posting\\."
imagePartialLinkMatch = "src=\"(https://pbs.twimg.com/media/.{15}\\?format=).*?\""
postIDMatch = "data-href=\"/EveryDayABA/status/(\\d+)\""
postBodyMatch = f"content=\"({titleMatch}(?s:.)*?)\""
postsDirectory = f"{os.getenv("POSTS_DIRECTORY")}"
postTrackerFile = f"{postsDirectory}PostTracker.csv"
postLinkPrefix = "https://x.com/EveryDayABA/status/"

