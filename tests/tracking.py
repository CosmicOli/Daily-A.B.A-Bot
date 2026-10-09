attempted = 0
passed = 0

currentTestNumber = 0

def attemptTest(testGroupName, testNumber):
    global currentTestNumber
    currentTestNumber = testNumber
    global attempted 
    attempted += 1
    print(f"Test group '{testGroupName}' test '{testNumber}':")

def passCurrentTest(testGroupName, variable):
    global passed
    passed += 1
    print(f"Test group '{testGroupName}' test '{currentTestNumber}' passed: {variable}\n")

def failCurrentTest(testGroupName, variable):
    print(f"Test group '{testGroupName}' test '{currentTestNumber}' failed: {variable}\n")

def passTest(testGroupName, testNumber, variable):
    global passed
    passed += 1
    print(f"Test group '{testGroupName}' test '{testNumber}' passed: {variable}\n")

def failTest(testGroupName, testNumber, variable):
    print(f"Test group '{testGroupName}' test '{testNumber}' failed: {variable}\n")