#!/usr/bin/env python

import os, twitter, time
from secret_keys import *

DELAY = 0.05

MY_TWITTER_CREDS = os.path.expanduser('~/.pyTweetSplitter')
if not os.path.exists(MY_TWITTER_CREDS):
    twitter.oauth_dance("Python-TweetSplitter", CONSUMER_KEY, CONSUMER_SECRET,
                        MY_TWITTER_CREDS)

oauth_token, oauth_secret = twitter.read_token_file(MY_TWITTER_CREDS)

t = twitter.Twitter(auth=twitter.OAuth(
    oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

print 'Enter the text you want split. Type \'done\' in its own line to finish.'

inputs = []
while True:
    line = raw_input()
    if line == 'done':
        break
    else:
        inputs.append(line)

text = "\n".join(inputs)

##def splitText(text):
toTweet = []
while text:
    numChars = 140
    h = text[:numChars]
    if text[numChars:] == '':
        toTweet.append(h)
    elif ' ' not in h:
        toTweet.append(h)
    else:
        spaceAt = h.rfind(' ')
        toTweet.append(h[:spaceAt])
        numChars = spaceAt + 1
    text = text[numChars:]
##return toTweet

##toTweet = splitText(text)
##Check with user
for i in range(len(toTweet)):
    print "{0}.============================================".format(i + 1)
    print toTweet[i]
areWeOkayToGo = raw_input('Total of {0} tweets. Continue (y/n)?'.format(len(toTweet)))
if areWeOkayToGo != 'y':
    exit()
for tweet in toTweet:
    t.statuses.update(status = tweet)
    #timer.sleep(DELAY)

