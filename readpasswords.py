#!/usr/bin/env python

### Adobe's recent password leak gives us great insight into people's 
### password and hint selections.
### If you don't have the data, I can't help you. But if you do,
### this'll nicely stick it in a database for you.

import sqlite3, re, base64, sys

def convertB64ToHexString(n):
    "Convert the base64-encoded password strings in the dump into nice hex strings."
    bytestring = base64.b64decode(n)
    toReturnString = ""
    for char in range(len(bytestring)):
        toReturnString += hex(ord(bytestring[char]))[2:].zfill(2)
        if (char % 8) == 7:
            toReturnString += " "
    return toReturnString

# the format of the lines. The second is for people who can't properly type in emails.
lineformat = re.compile(r'(\d+)-\|-.*?-\|-([\w\+._&-]+)@([\w\+.-]+)-\|-([\w=\+\/]+)-\|-(.*?)\|--')
lineformat2 = re.compile(r'(\d+)-\|-.*?-\|-(.+?)-\|-([\w=\+\/]+)-\|-(.*?)\|--')

# the dump file
origfile = open('cred')
# the sqlite3 file
conn = sqlite3.connect('passwords.db')
c = conn.cursor()

# Make things faster
c.execute("PRAGMA journal_mode = MEMORY")
c.execute("PRAGMA syncrhonous = OFF")
conn.isolation_level = "DEFERRED"

# Create our tables
c.execute("""
CREATE TABLE hints(
encryptedpassword varchar(100) REFERENCES passwords(encryptedpasswords),
idnumber int,
hint varchar(100),
email varchar(100),
emaildomain varchar(100))""")

conn.commit()
origfile.next()
count = 0
updateEvery = 100000 # how frequently do we make a commit?

for line in origfile:
    #most lines match the first format
    match = re.match(lineformat, line)
    if match is None:
        #but if it doesn't, try the other one
        match2 = re.match(lineformat2, line)
        if match2 is None:
            print line
            continue
        idnum = int(match2.group(1))
        email_first = match2.group(2)
        email_second = None
        encpassword = convertB64ToHexString(match2.group(3))
        hint = match2.group(4)
    else:
        idnum = int(match.group(1))
        email_first = match.group(2)
        email_second = match.group(3)
        encpassword = convertB64ToHexString(match.group(4))
        hint = match.group(5)
    
    #see if the password is already in the database. If it is, just increment the number
    #otherwise create a new row
    c.execute("insert into hints values (?,?,?,?,?)", (encpassword, idnum, hint, email_first, email_second))
    # Only update every 1000-ish rows
    if (count % updateEvery == 0):
        conn.commit()
        print >> sys.stderr, "\r" + str(count),
    count += 1

c.execute("""CREATE INDEX idx1 ON hints(encryptedpassword)""")
print "Total count: " + count
conn.commit()
conn.close()
