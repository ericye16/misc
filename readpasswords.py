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
lineformat2 = re.compile(r'(\d+)-\|-.*?-\|-([\w\+._&-]+)-\|-([\w=\+\/]+)-\|-(.*?)\|--')

# the dump file
origfile = open('cred')
# the sqlite3 file
conn = sqlite3.connect('passwords.db')
conn.isolation_level = "DEFERRED"
c = conn.cursor()

# Create our tables
c.execute("begin")
c.execute("""
CREATE TABLE passwords (
encryptedpassword varchar(100) primary key,
number int
)""")
c.execute("""
CREATE TABLE hints(
encryptedpassword varchar(100) REFERENCES passwords(encryptedpasswords),
idnumber int primary key,
hint varchar(100),
email varchar(100),
emaildomain varchar(100))""")
conn.commit()
origfile.next()
count = 0

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
    if count % 1000 == 0:
        c.execute("begin")
    c.execute("select * from passwords where encryptedpassword = ?", [encpassword])
    row = c.fetchone()
    if row is None:
        c.execute("insert into passwords values (?,?)", (encpassword, 1))
    else:
        c.execute("update passwords set number = number + 1 where encryptedpassword =?", [encpassword])        
    c.execute("insert into hints values (?,?,?,?,?)", (encpassword, idnum, hint, email_first, email_second))
    # Only update every 1000-ish rows
    if (count % 1000 == 0):
        conn.commit()
        print >> sys.stderr, "\r" + str(count),
    count += 1
print "Total count: " + count
conn.commit()
conn.close()
