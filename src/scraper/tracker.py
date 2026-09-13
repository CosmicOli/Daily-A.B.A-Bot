import scraper.globals as sg


def trackPost(ordinal, imageExists, link):
    file = open(sg.postTrackerFile, "a+")
    file.write(f"{ordinal},{imageExists},{link}\n")
    file.close()

def getPostTrackingEntry(ordinal):
    file = open(sg.postTrackerFile, "r")
    lines = file.readlines()
    file.close()

    matchingEntries = [x for x in lines if x.split(",")[0] == ordinal]

    if (len(matchingEntries) == 0):
        return False
    
    entry = matchingEntries[0].split(",")

    return entry
