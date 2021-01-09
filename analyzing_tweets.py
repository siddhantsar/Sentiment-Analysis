# Importing Libraries
import os
import sys
import tweepy
import csv
import re
import json
import traceback
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from textblob import TextBlob
from twitter_authentication import get_twitter_client

class SentimentAnalysisProject:

    tweetList = []
    tweetText = []
    tweetRawData = []

    client = get_twitter_client()

    searchTerm = sys.argv[1]
    searchNumber = int(sys.argv[2])

    tweetList = tweepy.Cursor(
        client.search, q=searchTerm, lang="en").items(searchNumber)
    
    def createFolder (searchTerm, searchNumber):
        try:  
            os.mkdir("{}-{}-Data".format(searchTerm, searchNumber))
        except OSError:  
            print()

        return str("{}-{}-Data".format(searchTerm, searchNumber))

    pathToFolder = createFolder(searchTerm, searchNumber)

    for _ in tweetList:
        tweetRawData.append(_)

    # Remove Links, Special Characters etc from tweet
    def cleanTweet(tweet):
        return str(' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()))

    # Calculate the percentage of data values
    def percentage(part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    # Plot pie chart and show it
    def plotPieChart(positive, weaklyPositive, stronglyPositive, neutral, negative, weaklyNegative, stronglyNegative, searchTerm, searchNumber):
        labels = ["Positive [" + str(positive) + "%]", "Weakly Positive [" + str(weaklyPositive) + " %]", "Strongly Positive [" + str(stronglyPositive) + " %]", "Neutral [" + str(neutral) + "%]",
                  "Negative [" + str(negative) + "%]", "Weakly Negative [" + str(weaklyNegative) + "%]", "Strongly Negative [" + str(stronglyNegative) + "%]"]
        sizes = [positive, weaklyPositive, stronglyPositive,
                 neutral, negative, weaklyNegative, stronglyNegative]
        colors = ["#8aac49", "#c6c96a", "#488f31",
                  "#ffe792", "#fbb36a", "#f27d58", "#de425b"]
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title("How Twitterati's are reacting on " + searchTerm +
                  " by analyzing " + str(searchNumber) + " Tweets.")
        plt.axis("equal")
        # plt.tight_layout()
        plt.savefig("./{}-{}-Data/{}-{}.png".format(searchTerm, searchNumber, searchTerm, searchNumber))
        plt.show()

    # Saving the Tweets (and other data) to CSV file format
    def getCSVData (tweetRawData, searchTerm, searchNumber, cleanedTweets, pathToFolder):
        data = pd.DataFrame()
        data['Username'] = np.array([tweet.user.name for tweet in tweetRawData])
        data['Tweets Text'] = np.array([tweet.text for tweet in tweetRawData])
        data['Clean Tweet Text'] = np.array([cleanTweet for cleanTweet in cleanedTweets])
        data['len'] = np.array([len(tweet.text) for tweet in tweetRawData])
        data['ID'] = np.array([tweet.id for tweet in tweetRawData])
        data['Date'] = np.array([tweet.created_at for tweet in tweetRawData])
        data['Source'] = np.array([tweet.source for tweet in tweetRawData])
        data['Location'] = np.array([tweet.user.location for tweet in tweetRawData])
        data['Coordinates'] = np.array([tweet.coordinates for tweet in tweetRawData])
        data.to_csv(os.path.join(pathToFolder, r"{}-{}.csv".format(searchTerm, searchNumber)), index=None, encoding="utf-8")

    # Saving complete Tweets in JSONL file format
    def getJSONLData (tweetRawData, searchTerm, searchNumber):
        filePath = "./{}-{}-Data/{}-{}.jsonl".format(searchTerm, searchNumber, searchTerm, searchNumber)
        with open(filePath, "w") as json_file:
            for status in tweetRawData:
                json_file.write(json.dumps(status._json) + "\n")
    
    polarity = 0
    positive = weaklyPositive = stronglyPositive = 0
    neutral = 0
    negative = weaklyNegative = stronglyNegative = 0

    for tweets in tweetRawData:

        tweetTextCleaned = cleanTweet(tweets.text)
        tweetText.append(tweetTextCleaned)
        analysis = TextBlob(tweetTextCleaned)
        polarity += analysis.sentiment.polarity

        if (analysis.sentiment.polarity == 0):
            neutral += 1
        elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
            weaklyPositive += 1
        elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
            positive += 1
        elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
            stronglyPositive += 1
        elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
            weaklyNegative += 1
        elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
            negative += 1
        elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
            stronglyNegative += 1

    getJSONLData (tweetRawData, searchTerm, searchNumber)
    getCSVData (tweetRawData, searchTerm, searchNumber, tweetText, pathToFolder)

    positive = percentage(positive, searchNumber)
    weaklyPositive = percentage(weaklyPositive, searchNumber)
    stronglyPositive = percentage(stronglyPositive, searchNumber)
    neutral = percentage(neutral, searchNumber)
    negative = percentage(negative, searchNumber)
    weaklyNegative = percentage(weaklyNegative, searchNumber)
    stronglyNegative = percentage(stronglyNegative, searchNumber)

    polarity = polarity / searchNumber

    print("How Twitterati's are reacting on term {} by analyzing {} Tweets".format(searchTerm, str(searchNumber)))
    print("Polarity: {}".format(str(polarity)))
    print("General Report: ")
    if (polarity == 0):
        print("Neutral")
    elif (polarity > 0 and polarity <= 0.3):
        print("Weakly Positive")
    elif (polarity > 0.3 and polarity <= 0.6):
        print("Positive")
    elif (polarity > 0.6 and polarity <= 1):
        print("Strongly Positive")
    elif (polarity > -0.3 and polarity <= 0):
        print("Weakly Negative")
    elif (polarity > -0.6 and polarity <= -0.3):
        print("Negative")
    elif (polarity > -1 and polarity <= -0.6):
        print("Strongly Negative")

    print("Detailed Report: ")
    print("Twitterati's who thougth term '{}' as positive are . . . . . . . . . . . . . . . . . . . . . {:>15.2f}%".format(searchTerm, float(positive)))
    print("Twitterati's who thougth term '{}' as weakly positive are . . . . . . . . . . . . . {:>8.2f}%".format(searchTerm, float(weaklyPositive)))
    print("Twitterati's who thougth term '{}' as strongly positive are . . . . . . . . . . . . {:>6.2f}%".format(searchTerm, float(stronglyPositive)))
    print("Twitterati's who thougth term '{}' as neutral are . . . . . . . . . . . . . . . . . . . . . {:>16.2f}%".format(searchTerm, float(neutral)))
    print("Twitterati's who thougth term '{}' as negative are . . . . . . . . . . . . . . . . . . . . . {:>15.2f}%".format(searchTerm, float(negative)))
    print("Twitterati's who thougth term '{}' as weakly negative are . . . . . . . . . . . . . {:>8.2f}%".format(searchTerm, float(weaklyNegative)))
    print("Twitterati's who thougth term '{}' as strongly negative are . . . . . . . . . . . . {:>6.2f}%".format(searchTerm, float(stronglyNegative)))

    plotPieChart(positive, weaklyPositive, stronglyPositive, neutral,
                 negative, weaklyNegative, stronglyNegative, searchTerm, searchNumber)


if __name__ == "__main__":
    SAP = SentimentAnalysisProject()

