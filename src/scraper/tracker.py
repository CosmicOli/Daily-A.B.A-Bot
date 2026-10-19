import scraper.globals as sg


# NOTE: Imma be so fr, this is not a good way of doing csv io, but as only one post will be added every day, the size of the csv will always be fairly negligable and the innefficiencies of this approach will not be significant 
# Next time I'll use pandas or something I promise lol


def getPostTrackingEntry(ordinal: str) -> (list[str] | None):
    file = open(sg.postTrackerFile, "r")
    lines = file.readlines()
    file.close()

    matchingEntries = [x for x in lines if x.split(",")[0] == ordinal]

    if (len(matchingEntries) == 0):
        return None
    
    entry = matchingEntries[0].removesuffix("\n").split(",")

    return entry


def trackPost(ordinal: str, imageExists: bool, link: str):
    if (not getPostTrackingEntry(ordinal) is None):
        raise Exception(f"Post already tracked for ordinal '{ordinal}'")

    file = open(sg.postTrackerFile, "a+")
    file.write(f"{ordinal},{imageExists},{link}\n")
    file.close()


def untrackPost(ordinal: str):
    entry = getPostTrackingEntry(ordinal)
    if (entry is None):
        raise Exception(f"Post already untracked for ordinal '{ordinal}'")

    file = open(sg.postTrackerFile, "r")
    lines = file.read()
    file.close()
    lines = lines.replace(f"{entry[0]},{entry[1]},{entry[2]}\n", "")
    file = open(sg.postTrackerFile, "w")
    file.write(lines)
    file.close()
