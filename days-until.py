#!/usr/bin/env python
#Days until a deadline or something. I like to put it in my .bashrc.

from datetime import date

IS_WEBSERVER = True

#format: ("name", yyyy, mm, dd, doICare)
deadlines = {
    ("Waterloo for Ontario high school students", 2014, 1, 15, True),
    ("U of T for Ontario high school students", 2014, 2, 28, True),
    ("MIT early action interview schedule", 2013, 10, 20, True),
    ("MIT early action", 2013, 11, 1, True),
    ("MIT regular action interview schedule", 2013, 12, 10, True),
    ("MIT regular action", 2014, 1, 1, True),
    ("Harvard early action", 2013, 11, 1, True),
    ("Harvard regular decision", 2014, 1, 1, True),
    ("SAT -- October", 2013, 10, 5, True),
    ("SAT -- November", 2013, 11, 2, True),
    ("AP Calculus", 2013, 5, 13, True),
    ("McMaster for Ontario high school students", 2014, 1, 15, True),
    ("Today", 2013, 9, 3, True),
}

class Colours:
    END = '\033[0m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    PINK = '\033[95m'
    YELLOW = '\033[93m'
    RED = '\033[91m'

def get_colour(days_left):
    if days_left < 15:
        return Colours.RED
    elif days_left < 30:
        return Colours.PINK
    elif days_left < 60:
        return Colours.YELLOW
    elif days_left < 120:
        return Colours.GREEN
    else:
        return Colours.BLUE

## calculate
today = date.today()
output = set()
for deadline in deadlines:
    if not deadline[4]: # If we don't care
        continue
    then = date(deadline[1], deadline[2], deadline[3])
    if then < today: # Already passed
        continue
    delta = then - today
    # subract 1 from the remaining days because I'm probably going to be looking
    # at this at night.
    output.add((delta.days - 1, deadline[0]))

## Display
if IS_WEBSERVER: #print the headers
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers
    print """
    <html>
    <head>
    <title>Days until</title>
    </head>
    <body>
    <h1>Days Until...?</h1>
    <ul>
    """
    
for deadline in sorted(output, reverse=True):
    if IS_WEBSERVER:
        print "<li>",
    else:
        print get_colour(deadline[0]),
        
    print deadline[1] + ": " + str(deadline[0]),
    
    if deadline[0] == 1:
         print "day left.",
    else:
        print "days left.",
        
    if IS_WEBSERVER:
        print "</li>",
    else:
        print Colours.END,
        
    print

if IS_WEBSERVER:
    print """
    </ul>
    </body>
    </html>
    """
