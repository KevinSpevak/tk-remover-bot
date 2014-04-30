"""
A bot for removing the .tk links that are submitted to /r/smashbros
Currently it just reports them since I do not have a reddit account with moderator status.

written by Kevin Spevak, based on bot.py from https://gist.github.com/avidw/9438841
"""

import praw, bmemcached, time, os     # for all bots
 
from requests import HTTPError        # to escape ban errors
import sys                            # for all errors
 
import re                             # if you want to use regex
 
reddit = praw.Reddit('tk remover bot 1.0 by /u/spevak')
reddit.login(os.environ['REDDIT_USERNAME'], os.environ['REDDIT_PASSWORD'])
#reddit.login('tk_remover_bot', 'alldayeveryday')

already = bmemcached.Client((os.environ['MEMCACHEDCLOUD_SERVERS'],), 
                             os.environ['MEMCACHEDCLOUD_USERNAME'],
                             os.environ['MEMCACHEDCLOUD_PASSWORD'])
 
regex = r'\.tk'
message = "I have reported this link because it looks like malware to me.  PM me if you think this was a mistake."
sub = 'bottest'

for post in praw.helpers.submission_stream(reddit, sub):
  if re.search(regex, post.url):
      cid = str(post.id)
      try:
          already.set(cit, 'True')
          post.downvote()
          post.add_comment(message)
          post.report()
          
      except HTTPError as err:
          pass
      # This one is pretty rare, since PRAW controls the rate automatically, but just in case
      except praw.errors.RateLimitExceeded as err:
          time.sleep(err.sleep_time)     

#for comment in praw.helpers.comment_stream(reddit, '+'.join(subreddits)):
#  cid = str(comment.id)
#  match = re.search(regex, comment.body, re.IGNORECASE)
#  if match and not(already.get(cid)):
#    try:
#      comment.reply(reply)
#      already.set(cid, "True")
    # If you are banned from a subreddit, reddit throws a 403 instead of a helpful message :/
#    except HTTPError as err:
#      print("Probably banned from /r/" + str(comment.subreddit), file=sys.stderr)
    # This one is pretty rare, since PRAW controls the rate automatically, but just in case
#    except praw.errors.RateLimitExceeded as err:
#      print("Rate Limit Exceeded:\n" + str(err), file=sys.stderr)
#      time.sleep(err.sleep_time)
