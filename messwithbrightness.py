#!/usr/bin/env python
import time

f = open("/sys/class/backlight/intel_backlight/brightness", "w")
while True:
    for i in range(10, 976):
        f.write(str(i))
        print "\r" + str(i),
        f.flush()
        time.sleep(0.001)
    for i in range(976, 10, -1):
        f.write(str(i))
        print "\r" + str(i),
        f.flush()
        time.sleep(0.001)
