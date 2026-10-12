attempted = 0
passed = 0

currentTestNumber = 0
currentTestGroupName = ""
currentTestFailed = False

def attemptTest(testGroupName, testNumber):
    global currentTestNumber
    currentTestNumber = testNumber
    global currentTestGroupName
    currentTestGroupName = testGroupName
    global currentTestFailed
    currentTestFailed = False
    global attempted 
    attempted += 1
    print(f"Test group '{testGroupName}' test '{testNumber}':")

def passCurrentTest(variable):
    global passed
    passed += 1
    print(f"Test group '{currentTestGroupName}' test '{currentTestNumber}' passed: {variable}\n")

def failCurrentTest(variable):
    global currentTestFailed
    if (not currentTestFailed): # After one fail in a test, the rest of the test may still run and fail a subsequent time due to a runon effect, so this suppresses the confusing extra messages
        currentTestFailed = True
        print(f"Test group '{currentTestGroupName}' test '{currentTestNumber}' failed: {variable}\n")

def passTest(testGroupName, testNumber, variable):
    global passed
    passed += 1
    print(f"Test group '{testGroupName}' test '{testNumber}' passed: {variable}\n")

def failTest(testGroupName, testNumber, variable):
    print(f"Test group '{testGroupName}' test '{testNumber}' failed: {variable}\n")