import csv
import datetime

import tweepy

access_token = "18828690-wEF8uyuBWvoENx45aLcEngMJ0afO08HNMJ3R6pLiz"
access_token_secret = "cKLvDBVyMas9ClFnbIOmETnlBB2wXAyeaRLk9OCI0"
consumer_key = "MxErE1sR6yl3xOpiPLax4w"
consumer_secret = "UXRkN3lW7rklGi3cZUMht0stR7AHvZ2tVUTj0L81dfA"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

username = '@CitronResearch'
start_date = datetime.datetime(2011, 12, 31, 0, 0, 0)
end_date = datetime.datetime(2017, 10, 17, 0, 0, 0)

tweets = []
tmpTweets = api.user_timeline(username)
for tweet in tmpTweets:
    if tweet.created_at < end_date and tweet.created_at > start_date:
        tweets.append(tweet)

while (tmpTweets[-1].created_at > start_date):
    print("Last Tweet @", tmpTweets[-1].created_at, " - fetching some more")
    tmpTweets = api.user_timeline(username, max_id=tmpTweets[-1].id)
    for tweet in tmpTweets:
        if tweet.created_at < end_date and tweet.created_at > start_date:
            tweets.append(tweet)


with open('CitronResearch.csv', 'w', encoding = 'utf-8') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',', quotechar='|',
                            quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['ID', 'Created at', 'Text', 'Tickers'])
    for tweet in tweets:
        # We want alphabetic texts that are longer than 1
        # character and the first character is $.
        tickers = [t[1:] for t in tweet.text.split() if
                   t.startswith('$') and t[1:].isalpha() and len(t) > 1]
        csv_writer.writerow([str(tweet.id), tweet.created_at,
                             tweet.text, ', '.join(tickers)])
