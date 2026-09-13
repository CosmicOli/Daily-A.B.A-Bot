import testcounts as t

import bot.utils as bu
import bot.globals as bg

testGroupName = "utils"


# Test 1: for updateCurrentDay; checks if current day updates
# NOTE: Cannot test against a known 'correct' day, so this only checks for a change in day
t.attemptTest()

bg.day = -1
bu.updateCurrentDay()
if (bg.day != -1):
    t.passTest(testGroupName, 1, f"day={bg.day}")
else:
    t.failTest(testGroupName, 1, f"day={bg.day}")


# Test 2: for generateMessageContentAndImage; 
t.attemptTest()


