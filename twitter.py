#n!/usr/bin/env python
#
# Copyright 2010 Ryan R. Rosario All Rights Reserved
# 

'''A simple library providing a Python interface to the Twitter API'''

__author__ = 'ryan@bytemining.com'
__version__ = '0.1-devel'

from time import strftime
import urllib2
import base64
import simplejson
import pdb
import time
import calendar
import httplib
import sys

selfuser = ""
selfpass = ""
maxtweets = 200


def process_HTTPerror(code):
    '''
    Indicates to this API how to handle the particular error
    that occurred based on the method that caused the 
    exception.

    Code    Error           Method and Action
    ----    -------------  ------------------------------------------
    304     Not Modified   NOT IMPLEMENTED
    400     Bad Request    User is being rate limited.
                           Standard API => Call wait function
                           Other => NOT IMPLEMENTED
    401     Unauthorized   Standard API => Skip user
                           Other => Fail
    403     Forbidden      Malformed request, or update
                           Standard API, Post => Fail or call wait.
    404     Not Found      Standard API => Fail, skip object
    406     Not Acceptable Search API => Fail
    500     Internal Err.  Fail or call retry function.
    502     Bad gateway    Fail or call retry function.
    503     Serivce unav.  System overload.
                           Fail or call retry function.

    Action Codes:
    -------------
    -1  Unable to retrieve this object, but execution can continue.
    -2  Error occurred at Twitter. Call retry function, if any.
    -3  Rate limiting has occurred. Call waiting function, if any.
    '''
    if code in [401, 404]:
        return -1
    elif code in [500, 502, 503]:
        return -2
    elif code in [400, 403]:
        return -3


def thetime():
    return strftime("%Y-%m-%d %H:%M:%S")


def log(stamp, type, code, user, action, url):
    LOG = open("verbose.log", "a")
    print >> LOG, '\t'.join([stamp, type, str(code), user, action, url])
    LOG.close()
    return


def get_followers(username, all=True):
    '''
    Retrieves the followers for user given by username.

    Args:
            username: user for which to extract followers.
            all: True to get all followers (using pagination)
                 False to get just one page.
    '''
    global selfuser, selfpass
    cursor = -1
    followers = []
    pw_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    pw_mgr.add_password(None, "http://twitter.com/", selfuser, selfpass)
    handler = urllib2.HTTPBasicAuthHandler(pw_mgr)
    opener = urllib2.build_opener(handler)
    while cursor != 0:
        url = 'http://twitter.com/statuses/followers/%s.json?cursor=%s' % (username, str(cursor))
        retries = 0
        while True:
            try:
                data = opener.open(url).read()
                page = simplejson.loads(data)
                newdata = page['users']
                followers.extend(newdata)
                cursor = page['next_cursor']
                break
            except urllib2.HTTPError, e:
                action = process_HTTPerror(e.code)
                print " Error ", str(e.code), " occurred on ", username, "."
                if action == -1:
                    log(thetime(), "HTTP", str(e.code), username, "FAIL", url)
                    return -1   #return failure
                elif action == -2:
                    retries += 1
                    log(thetime(), "HTTP", str(e.code), username, "RETRY", url)
                    if retries > 5:
                        log(thetime(), "HTTP", str(e.code), username, "RETRY AFTER FAIL", url)
                        return -1
                    retry()
                elif action == -3:
                    log(thetime(), "HTTP", str(e.code), username, "WAIT", url)
                    wait()
            except urllib2.URLError:
                log(thetime(), "URL", "NA", username, "RETRY", url)
                print "Error occurred: URLError"
                retry() 
            except httplib.BadStatusLine, e:
                log(thetime(), "BadStatus", "NA", username, "RETRY", url)
                print "Error occurred: BadStatusLine"
                retry()
    return followers 


def get_friends(username, all=True):
    global selfuser, selfpass
    cursor = -1
    friends = []
    pw_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    pw_mgr.add_password("Twitter API", "http://twitter.com/", selfuser, selfpass)
    handler = urllib2.HTTPBasicAuthHandler(pw_mgr)
    opener = urllib2.build_opener(handler)
    while cursor != 0:
        retries = 0
        url = 'http://twitter.com/statuses/friends/%s.json?cursor=%s' % (username, str(cursor))
        while True:
            try:
                data = opener.open(url).read()
                page = simplejson.loads(data)
                newdata = page['users']
                friends.extend(newdata)
                cursor = page['next_cursor']
                break
            except urllib2.HTTPError, e:
                action = process_HTTPerror(e.code)
                print " Error ", str(e.code), " occurred on ", username, "."
                if action == -1:
                    log(thetime(), "HTTP", str(e.code), username, "FAIL", url)
                    return -1   #return failure
                elif action == -2:
                    log(thetime(), "HTTP", str(e.code), username, "RETRY", url)
                    retries += 1
                    if retries > 5:
                        log(thetime(), "HTTP", str(e.code), username, "FAIL AFTER RETRY", url)
                        return -1
                    retry()
                elif action == -3:
                    log(thetime(), "HTTP", str(e.code), username, "WAIT", url)
                    wait()            
            except urllib2.URLError:
                log(thetime(), "URL", "NA", username, "RETRY", url)
                print "Error occurred: URLError"
                retry()
            except httplib.BadStatusLine, e:
                log(thetime(), "BadStatus", "NA", username, "RETRY", url)
                print "Error occurred: BadStatusLine"
                retry()
    return friends


def get_tweets(username, limit = None):
    global selfuser, selfpass, maxtweets
    tweets = []
    pw_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    pw_mgr.add_password("Twitter API", "http://twitter.com/", selfuser, selfpass)
    handler = urllib2.HTTPBasicAuthHandler(pw_mgr)
    opener = urllib2.build_opener(handler)
    page = 1
    no_tweets = 0
    while True:
        url = 'http://twitter.com/statuses/user_timeline/%s.json?page=%s&count=%s' \
            % (username, page, maxtweets)
        while True:
            try:
                data = opener.open(url).read()
                tweetpage = simplejson.loads(data)
                if len(tweetpage) == 0:
                    #either hit pagination limit, or
                    #user has no more tweets.
                    return tweets
                else:
                    page += 1
                    if limit and no_tweets + len(tweetpage) >= limit:
                        tweets.extend(tweetpage[:(limit - no_tweets + 1)])
                        return tweets
                    else:
                        tweets.extend(tweetpage)
                        no_tweets += len(tweetpage)
                        break
            except urllib2.HTTPError, e:
                action = process_HTTPerror(e.code)
                print "Error occurred with user %s, error: %s. " % (username, str(e.code))
                if action == -1:
                    return tweets
                elif action == -2:
                    retry()
                elif action == -3:
                    wait()
            except urllib2.URLError:
                print "Error occurred: URLError."
                retry()
            except httplib.BadStatusLine, e:
                print "Error occurred: BadStatusLine."
                retry()
    return tweets

def get_user(username):
    global selfuser, selfpass
    pw_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    pw_mgr.add_password("Twitter API", "http://twitter.com/", selfuser, selfpass)
    handler = urllib2.HTTPBasicAuthHandler(pw_mgr)
    opener = urllib2.build_opener(handler)
    url = 'http://twitter.com/users/show/%s.json' \
        % username
    retries = 0
    while True:
        try:
            data = opener.open(url).read()
            userpage = simplejson.loads(data)
            break
        except urllib2.HTTPError, e:
            if e.code == 404:
                retries += 1
                continue
            if retries >= 5:
                return {}
            action = process_HTTPerror(e.code)
            print "Error occurred with user %s, error: %s. " % (username, str(e.code))
            if action == -1:
                return userpage
            elif action == -2:
                retry()
            elif action == -3:
                wait()
        except urllib2.URLError:
            print "Error occurred: URLError."
            print url
            retry()
        except httplib.BadStatusLine, e:
            print "Error occurred: BadStatusLine."
            retry()
        except:
            print url
            print data
            print userpage
    return userpage


def retry():
    time.sleep(2)
    return


def api_status():
    global selfuser, selfpass
    pw_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    pw_mgr.add_password("Twitter API", "http://twitter.com/", selfuser, selfpass)
    handler = urllib2.HTTPBasicAuthHandler(pw_mgr)
    opener = urllib2.build_opener(handler)
    url = 'http://api.twitter.com/1/account/rate_limit_status.json'
    doc = opener.open(url).read()
    acct = simplejson.loads(doc)
    reset_time = J['reset_time_in_seconds']
    hits = J['remaining_hits']
    curr_time = calendar.timegm(time.gmtime())
    delay = reset_time - curr_time
    return {'reset': delay, 'hits': hits}


def wait():
    pw_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    pw_mgr.add_password("Twitter API", "http://twitter.com/", selfuser, selfpass)
    handler = urllib2.HTTPBasicAuthHandler(pw_mgr)
    opener = urllib2.build_opener(handler)
    url = "http://twitter.com/account/rate_limit_status.json"
    reset_time = simplejson.loads(opener.open(url).read())['reset_time_in_seconds']
    curr_time = calendar.timegm(time.gmtime())
    delay = reset_time - curr_time
    if delay <= 0: 
        delay = 300
    else:
        time.sleep(delay)

