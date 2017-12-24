#!/usr/bin/env python
import os, sys, time
import json
import tweepy
import argparse

#----------------------------------------------------------------------
def get_args():
    """"""
    parser = argparse.ArgumentParser(
        description="Twitter Helper",
        epilog="tweetux.py -p authfile.txt -r/F/f/l/R/r "
    )

    # required argument
    parser.add_argument('-p', '--path-creds-file', action="store", required=True, help='Path to credential file') 
    # optional arguments
    parser.add_argument('-f', '--follow-new-followers', help='Auto follow new followers', action='store_true')
    parser.add_argument('-F', '--follow-user', help='Follow user', type=str)
    parser.add_argument('-l', '--list-id-screenname', help='Get ID username from a list. Input MUST BE comma (,) separated', type=str)
    parser.add_argument('-t', '--tweet-text', help='Tweet from command line', type=str)
    parser.add_argument('-R', '--retweet-follow', help='Retweet some topic and follow', type=str)
    parser.add_argument('-r', '--retweet-user', help='Retweet specific user', type=str)
    #print parser.parse_args()
    opts = parser.parse_args()
    return opts

def Tweeter_Auth():
    opts = get_args()
    if opts.path_creds_file:
        credfilepath = opts.path_creds_file 
        #Creds file
        credsfile = os.path.expanduser(credfilepath)
        creds = json.load(open(credsfile))
        
        # Get authentication token
        auth = tweepy.OAuthHandler(consumer_key = creds['consumer_key'],
          consumer_secret = creds['consumer_secret'])
        auth.set_access_token(creds['access_token'],
          creds['access_token_secret'])
        
        # create an API handler
        api = tweepy.API(auth)
        return api
    else:
        print "Must provide credentianls to login"
        return None

#Follow new Followers -- Linked to user account creds
def followNewFollowers():
    print "-----------------------"
    print "Adding users to follow:"
    print "-----------------------"
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()
        print follower.screen_name
    print "-----------------------"
    print "Process finished, See ya'"
    print "-----------------------"

def getScreenNamesList():
    terminal_screen_name_list = [str(item) for item in opts.list_id_screenname.split(',')]
    #print terminal_screen_name_list
    return terminal_screen_name_list

def getUsersId(screen_names):
    try:
        print "--------------------------------------------------------"
        print 'UserName: \t\t\t\tID:'
        print "--------------------------------------------------------"
        for screen_name in screen_names:
            user = api.get_user(screen_name)
            #print 'UserName:"%s" ID: \t\t"%s"' % (user.name, user.id)
            print '"%s"\t\t\t\t"%s"' % (user.name, user.id)
        return True
    except TypeError:
        pass
    except tweepy.TweepError, e:
        print 'Error: %s' % (e)

def tweet_text(tweetvar):
    """ tweets text from input variable """
    try:
        api.update_status(tweetvar)
    except:
        return False
    return True

def follow_user(searchuser):
    """searches tweets with searchterms, retweets, then follows"""
    for tweet in tweepy.Cursor(api.search, q=searchuser).items(10):
        try:
            if not tweet.user.following:
                tweet.user.follow()
            return True
        except tweepy.TweepError as e:
            print(e.reason)
            pass
    return False

def retweet_follow(searchterms):
    """searches tweets with searchterms, retweets, then follows"""
    for tweet in tweepy.Cursor(api.search, q=searchterms).items(10):
        try:
            tweet.retweet()
            if not tweet.user.following:
                tweet.user.follow()
            return True
        except tweepy.TweepError as e:
            print(e.reason)
            pass
    return False

def retweet_user(searchuser):
    """searches tweets with searchuser, retweets"""
    for tweet in tweepy.Cursor(api.search, searchuser, result_type="recent", include_entities=True).items(10):
        try:
            if (not tweet.retweeted) and ('RT @' not in tweet.text):
                tweet.retweet()
        except tweepy.TweepError as e:
            print(e.reason)
            pass
    return False

if __name__ == '__main__':

    api = Tweeter_Auth()
    opts = get_args()
    if opts.follow_new_followers:
        followNewFollowers()
    elif opts.list_id_screenname:
        #print (opts.list_id_screenname)
        list_from_terminal = getScreenNamesList()
        getUsersId(list_from_terminal)
    elif opts.tweet_text:
        #print opts.tweet_text 
        tweet_text(opts.tweet_text)
    elif opts.retweet_follow:
        #print opts.retweet_follow
        retweet_follow(opts.retweet_follow)
    elif opts.retweet_user:
        #print opts.retweet_user
        retweet_user(opts.retweet_user)
    elif opts.follow_user:
        #print opts.follow_user
        retweet_user(opts.follow_user)
    else: 
        print "Needs Argument"
