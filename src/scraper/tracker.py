import scraper.globals as sg


def getPostTrackingEntry(ordinal):
    file = open(sg.postTrackerFile, "r")
    lines = file.readlines()
    file.close()

    matchingEntries = [x for x in lines if x.split(",")[0] == ordinal]

    if (len(matchingEntries) == 0):
        return None
    
    entry = matchingEntries[0].removesuffix("\n").split(",")

    return entry


def trackPost(ordinal, imageExists, link):
    if (not getPostTrackingEntry(ordinal) is None):
        raise Exception

    file = open(sg.postTrackerFile, "a+")
    file.write(f"{ordinal},{imageExists},{link}\n")
    file.close()
