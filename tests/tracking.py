attempted = 0
passed = 0

def attemptTest(testGroupName, testNumber):
    global attempted 
    attempted += 1
    print(f"Test group '{testGroupName}' test '{testNumber}':")

def passTest(testGroupName, testNumber, variable):
    global passed 
    passed += 1
    print(f"Test group '{testGroupName}' test '{testNumber}' passed: {variable}\n")

def failTest(testGroupName, testNumber, variable):
    print(f"Test group '{testGroupName}' test '{testNumber}' failed: {variable}\n")