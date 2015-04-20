# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 08:38:22 2015

@author: Manoj Sharma
"""
import json
import pprint
import pandas as pd

tweets_data_path = '//tweet_search.txt'        
tweets_data = []
tweets_file = open(tweets_data_path, "r")

#tweets = json.load(tweets_file)
#tweets["text"]

for line in tweets_file:
        try:
            tweet = json.loads(line)
            #pprint.pprint(tweet["text"])
            #pprint.pprint(tweet["user"]["screen_name"])
           #print tweet
            #tweet["text"]
            #tweets_data.append(tweet)
            hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
            tweets_data.append([tweet["text"],tweet["user"]["screen_name"],hashtags])
            pprint.pprint(tweets_data)
            #print(tweets_data)
        except:
            continue

#pprint.pprint(tweets_data[0][1])
#pprint(tweet)
#pprint(tweets_data)

#tweetsDF = pd.DataFrame.from_records(tweets_data)
tweetsDF = pd.DataFrame(tweets_data)
##tweetsDF = pd.read_json(tweet)
#print(tweetsDF)
print(tweetsDF.index)
print(tweetsDF.columns)
#print(tweetsDF['user'])