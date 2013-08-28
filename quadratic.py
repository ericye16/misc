#!/usr/bin/python
import sys, math

if len(sys.argv) != 4:
    print "Incorrect number of arguments. ./quadratic.py a b c"
    sys.exit(-1)

a = float(sys.argv[1])
b = float(sys.argv[2])
c = float(sys.argv[3])

if a == 0:
    print "Cannot have a zero for A. Cowardly exiting."
    sys.exit(-2)

# check determinant
if (b * b - 4 * a * c) < 0:
    print "Nonreal solutions. Cowardly exiting."
    sys.exit(-2)

ans_1 = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
ans_2 = (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)

print ans_1
print ans_2
