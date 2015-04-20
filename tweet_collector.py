# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 11:08:55 2015

@author: Manoj Sharma
"""

import tweepy


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import json

#Variables that contains the user credentials to access Twitter API 
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

#OAuth process using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Creation of the actual interface, using authentication
api= tweepy.API(auth)
#api.update_status("The Changing Nature of Predictive Analysis in the Enterprise http://tinyurl.com/nvw2uxx")

#Creates the user object. The me() method returns the user whose authentication keys were used
#user = api.me()
user = api.get_user('MSharma_Quantum')

print('Name:' + user.name)
print('Location:' + user.location)
print('Friends:' + str(user.friends_count))

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print tweet.text
    
query = 'python'
max_tweets = 50
searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
#print(searched_tweets)

filepath = './/tweet_search.txt'
target = open(filepath, 'w')

for tweet in searched_tweets:
    #print tweet.text
    tweet_str = json.dumps(tweet._json)
    target.write(tweet_str + "\n")

target.close()
      
class StdOutListener(StreamListener):
    
    def __init__(self, api=None):
        self.api = api or API()
        self.number_tweets = 0
        self.max_tweets = 100
        #tweets_data_path = '.\\tweepy_text.txt'
        tweets_data_path = 'C://Users//u23139//flaskr//tweepy_text.txt'        
        self.output = open(tweets_data_path, 'w')
    
    
    
    def on_data(self,data):
        #print data
        self.output.write(data + "\n")
        self.number_tweets = self.number_tweets + 1
        if self.number_tweets < self.max_tweets:
            return True
        else:
            self.output.close()
            print "Number of tweets stored = " + str(self.number_tweets)
            return False
            
    def on_error(self,status):
        print status
        return True
        
if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    
    stream = Stream(auth,listener)
    stream.filter(track=['python','ruby'])    
    
    
