# Adapted from https://gist.github.com/yanofsky/5436496#file-tweet_dumper-py-L36
#http://stackoverflow.com/questions/27351207/gracefully-handle-errors-and-exceptions-for-user-timeline-method-in-tweepy

import tweepy
import csv
import time

#Variables that contains the user credentials to access Twitter API
consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''

#Twitter only allows access to a users most recent 3240 tweets with this method

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

openfile = open("data/screen_names.csv", "rb")
r = csv.reader(openfile)

writefile=open("data/sample_tweets.csv", "wb")
w=csv.writer(writefile)

#counter = 0

for i in r:
    #initialize a list to hold all the tweepy Tweets
    alltweets = []
    print i[0]

    try:
        new_tweets = api.user_timeline(screen_name = i[0], count=200, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    except:
        pass
    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    try:
        oldest = alltweets[-1].id - 1
    except:
        pass

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)

        #all subsiquent requests use the max_id param to prevent duplicates
        try:
            new_tweets = api.user_timeline(screen_name = i[0],count=200,max_id=oldest, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        except:
            pass
        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "...%s tweets downloaded so far" % (len(alltweets))

    #counter += 1
        #write the csv
    for tweet in alltweets:
        w.writerow([i[0], tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")])
        #w.writerow([i, tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.source])

openfile.close()
writefile.close()