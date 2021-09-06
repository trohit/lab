#!/usr/bin/python3
# just a quick way to time long running tasks in python
import time

# start time - t1
t1 = time.time()

# do some long-running work
time.sleep(1)

# end time - t2
t2 = time.time()
print(t2-t1)
