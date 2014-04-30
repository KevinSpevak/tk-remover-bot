"""
A bot for removing the .tk links that are submitted to /r/smashbros
Currently it just reports them since I do not have a reddit account with moderator status.

I've commented out the use of memchached for keeping track of which posts we've already looked at since
I'm running this on heroku which requires credit card verification for the (free) memcached service, and I
don't have a credit card.  Boo. 

written by Kevin Spevak, based on bot.py from https://gist.github.com/avidw/9438841
"""
from __future__ import print_function

import praw, time, os     # for all bots
#import bmemcached 

from requests import HTTPError        # to escape ban errors
import sys                            # for all errors
 
import re                             # if you want to use regex
 
reddit = praw.Reddit('tk remover bot 1.0 by /u/spevak')
reddit.login(os.environ['REDDIT_USERNAME'], os.environ['REDDIT_PASSWORD'])

#already = bmemcached.Client((os.environ['MEMCACHEDCLOUD_SERVERS'],), 
#                             os.environ['MEMCACHEDCLOUD_USERNAME'],
#                             os.environ['MEMCACHEDCLOUD_PASSWORD'])
 
regex = r'\.tk'
message = "I have reported this link because it looks like malware to me.  PM me if you think this was a mistake."
sub = 'smashbros'

for post in praw.helpers.submission_stream(reddit, sub):
    #id = str(post.id)
    #if re.search(regex,post.url) and not already.get(id):
    if re.search(regex, post.url):
      try:
          #already.set(cit, 'True')
          post.downvote()
          post.add_comment(message)
          post.report()
          
      except HTTPError as err:
          print("Got httpError while trying to handle the link " + post.url \
                    + "\n" + str(err), file=syst.stderr)
      # This one is pretty rare, since PRAW controls the rate automatically, but just in case
      except praw.errors.RateLimitExceeded as err:
          print("Rate Limit Exceeded \n" + str(err), file=sys.stderr)
          time.sleep(err.sleep_time)     
