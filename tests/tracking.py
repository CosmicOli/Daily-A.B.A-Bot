attempted = 0
passed = 0

currentTestNumber = 0
currentTestGroupName = ""

def attemptTest(testGroupName, testNumber):
    global currentTestNumber
    currentTestNumber = testNumber
    global currentTestGroupName
    currentTestGroupName = testGroupName
    global attempted 
    attempted += 1
    print(f"Test group '{testGroupName}' test '{testNumber}':")

def passCurrentTest(variable):
    global passed
    passed += 1
    print(f"Test group '{currentTestGroupName}' test '{currentTestNumber}' passed: {variable}\n")

def failCurrentTest(variable):
    print(f"Test group '{currentTestGroupName}' test '{currentTestNumber}' failed: {variable}\n")

def passTest(testGroupName, testNumber, variable):
    global passed
    passed += 1
    print(f"Test group '{testGroupName}' test '{testNumber}' passed: {variable}\n")

def failTest(testGroupName, testNumber, variable):
    print(f"Test group '{testGroupName}' test '{testNumber}' failed: {variable}\n")