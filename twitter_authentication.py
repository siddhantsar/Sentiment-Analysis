# Importing Libraries
import os
import sys
from tweepy import API
from tweepy import OAuthHandler

# Getting Twitter Authentication
def get_twitter_authentication():

    """
    Setup Twitter Authentication
    Return: tweepy.OAuthHandler Object
    """
    try:
        consumer_key =    # Your API Keys and Tokens Here
        consumer_secret = # Your API Keys and Tokens Here
        access_token =    # Your API Keys and Tokens Here
        access_secret =   # Your API Keys and Tokens Here
    except KeyError:
        print("Twitter Key Not Found\n")
        sys.exit(1)
    
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth

# Returning Twitter Client API
def get_twitter_client():
    """
    Setup Twitter API client
    Return: tweepy.API object
    """
    auth = get_twitter_authentication()
    client = API(auth)
    return client

