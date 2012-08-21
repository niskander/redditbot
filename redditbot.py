# redditbot.py
# author: Nancy (github: C-xC-q)

"""Framework for a redditbot (that comments)"""

import redditthings
import json
import requesthandler
from customexceptions import *

# reddit api
LOGINCALL = 'http://www.reddit.com/api/login'
REPLYCALL = 'http://www.reddit.com/api/comment'


class RedditUser(object):
    """Wrapper for the login/reply api calls, and stores user information."""
    def __init__(self, username, secret, useragent):
        self.username = username
        self.secret = secret
        self.useragent = useragent
        http.setuseragent(useragent)
        self.cookiename = 'reddit%scookie.lwp' % self.username
        self.loggedin = False
        self.login()
        return

    def login(self):
        data = {}
        data['user'] = self.username
        data['passwd'] = self.secret
        data['api_type'] = 'json'
        url = '%s/%s' % (LOGINCALL, self.username)
        response = requesthandler.reqhandler.postrequest(url, data)
        js = json.loads(response.read())
        # modhash is needed when posting
        try:
            self.modhash = js['json']['data']['modhash']
        except KeyError:
            raise FailedFetch(self.username, self.secret, js)
            return
        self.loggedin = True
        requesthandler.reqhandler.savecookiefile(self.cookiename)
    
    def reply(self, text, parent_type, parent_id, parent_kind):
        # TODO: cookie
        if not self.loggedin or self.modhash is None:
            context = 'posting \'%s\' as %s in reply to %s with id %s' % \
                      (text, self.username, parent_type, parent_id)
            raise LoginRequired(context)
            return

        data = {}
        data['uh'] = self.modhash
        data['text'] = text
        data['thing_id'] = '%s_%s' % (parent_kind, parent_id)

        response = requesthandler.reqhandler.postrequest(REPLYCALL, data)
        return response


class RedditBot(RedditUser):
    """Extends RedditUser. Adds functions to iterate over posts/comments
    and compose replies to them if desired.
    """
    def __init__(self, \
                 username, secret, useragent, \
                 wantcomments=True, wantposts=False, \
                 fetchblocksize=50, maxcommentdepth=5, \
                 subredditlist=['all'])
        super(RedditBot, self).__init__(username, secret, useragent)
        self.wantcomments = wantcomments
        self.wantposts = wantposts
        self.redditerator = redditthings.RedditIterator( \
            subreddits=subredditlist, blocksize=fetchblocksize)
        self.maxcommentdepth = maxcommentdepth
        
    def roamposts(self):
        """Iterates over posts, considers them for replying and relplies
        to those that are selected. Exit with C-c.
        """
        while True:
            try:
                post = self.redditerator.nextpost()
                if self.wantposts and self.wantpost(post):
                    replytext = self.composereply(post)
                    self.reply(replytext, 'thread', post.kind, post.id)
                if self.wantcomments:
                    comments_js = self.redditerator.fetchcomments(post)
                    self.roamcomments(comments_js, 0)
            except KeyboardInterrupt:
                break
            except FailedFetch as f:
                print f.message
                break
            except LoginRequired as l:
                self.login()
                continue

    def roamcomments(self, comments_js, depth):
        """Recursively iterates over comments/comment replies, and replies
        to those that are selected.
        """
        if depth > self.maxcommentdepth or comments_js is None: return
        for comment_dict in comments_js:
            if comment_dict['kind'] == 'more': return
            comment = redditthings.RedditComment(comment_dict['data'])
            if self.wantcomment(comment):
                replytext = self.composereply(comment)
                self.reply(replytext, 'comment', comment.kind, comment.id)
            self.roamcomments(comment.replies_js, depth+1)

    def wantpost(self, post):
        """Returns True if the post is to be replied to; False otherwise."""
        print 'Not replying to %s' % post.title
        return False

    def wantcomment(self, comment):
        """Returns True if the comment is to be replied to; False otherwise."""
        print 'Not replying to %s' % comment.body[:20]
        return False

    def composereply(self, thing):
        """Returns the text of a reply to a comment or a post."""
        return ''
    