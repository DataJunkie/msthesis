#!/usr/bin/env python

import twitter
from multiprocessing import Process, Pipe, Queue, Pool
import time
import pdb
import urllib2
from collections import deque
import simplejson
from neo4j import NeoService
import sys
import neo4j
import pickle


def get_friends_parallel(conn, username):
    friends = twitter.get_friends(username)
    conn.send(friends)


def get_followers_parallel(conn, username):
    followers = twitter.get_followers(username)
    conn.send(followers)


def get_tweets_parallel(user):
    cxn = Connection()
    db = cxn.tweets
    print "Getting tweets for ", user
    updates = twitter.get_tweets(user,limit = 1000)


def get_ff(user):
    assert (type(user) == str)
    parent_friends_pi, friends_pi = Pipe()
    parent_followers_pi, followers_pi = Pipe()
    friend_pr = Process(target = get_friends_parallel, args=(friends_pi, user))
    follower_pr = Process(target = get_followers_parallel, args=(followers_pi, user))
    #Get friends and followers.
    friend_pr.start()
    follower_pr.start()
    friends = parent_friends_pi.recv()
    followers = parent_followers_pi.recv()
    friend_pr.join()
    follower_pr.join()
    return friends, followers


def in_index(ind, key):
    if key in ind:
        return True
    return False


def already_expanded(u):
    global expanded
    if u in expanded:
        return True
    return False


def already_scraped(index, user):
    if user in index:
        return True
    return False


def dump(data):
    OUT = open("userinfo.dat","a")
    print >> OUT, simplejson.dumps(data)
    OUT.close()
    return

def main():
    global expanded
    staff = {'al3x': True, 'rsarver': True, 'kevinweil': True, 'jointheflock': True, 'squarecog': True}
    crawl_deque = deque()
    idx = {}
    #Seed the crawler with an initial user, DEGREE 0
    seed = twitter.get_user("datajunkie")
    crawl_deque.append(seed)
    crawl_deque.append("\n")
    degree = 2
    current_degree = 1  #1-current user + friends/followers, etc.
    start = time.time()
    deque_size = 0
    expanded = {}
    while True: 
        user = crawl_deque.popleft()
        if user == "\n":
            LOG = open("process.log","a")
            print >> LOG, "Queue now has size %d after degree %d." % (deque_size, current_degree)
            crawl_deque.append("\n")
            end = time.time()
            print >> LOG, "Time required for degree %d was %s s." % (current_degree, str(end-start))
            LOG.close()
            current_degree += 1
            if current_degree > degree:
                break
            start = time.time()
            continue
        #If this user has already been expanded (got friends and followers), don't do it again
        if already_expanded(user['screen_name']):
            continue
        #If this user's information has already been scraped, don't do it again.
        #if not already_scraped(idx, user['screen_name']):      #in_index
        dump(user)
            #idx[user['screen_name']] = user['id']     #mark the user as scraped.
            #TO DO: Print user info to file.
        LOG = open("process.log", "a")
        print >> LOG, "Getting friends and followers for %s." % user
        LOG.close()
        #Check that the user is not a crawler bomb.
        if user.has_key('friends_count') and user.has_key('followers_count') and \
            user['friends_count'] + user['followers_count'] > 20000:
            continue
        friends, followers = get_ff(user['screen_name'])
        for friend in friends:
            #if user information has already been scraped, don't do it again.
            #if not already_scraped(idx, friend['screen_name']):
                #user_data = twitter.get_user(friend['screen_name'])
            dump(friend)
                #idx[friend['screen_name']] = friend['id']    #Mark the user as scraped.
            if friend['screen_name'] not in staff:
                crawl_deque.append(friend)
                deque_size += 1
            GRAPH = open("graph.log","a")
            print >> GRAPH, ','.join([user['screen_name'], friend['screen_name']])
            GRAPH.close()
        for follower in followers:
            #if the node exists, get it. Otherwise, create it.
            #if not already_scraped(idx, follower['screen_name']):
                #user_data = twitter.get_user(follower['screen_name'])
            if len(follower) == 0:
                print "HERE"
                continue
            print "FOLLOWER"
            dump(follower)
            #idx[follower['screen_name']] = follower['id']  #mark user as scraped
            if follower['screen_name'] not in staff:
                crawl_deque.append(follower)
                deque_size += 1
            GRAPH = open("graph.log","a")
            print >> GRAPH, ','.join([follower['screen_name'], user['screen_name']])
            GRAPH.close()
        expanded[user['screen_name']] = True
        OUT = open("index.pickle", "w")
        pickle.dump(idx, OUT)
        OUT.close()


if __name__ == '__main__':
    main()
