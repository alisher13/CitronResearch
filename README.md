In this study I analyze the effect of tweets by Citron - a renowned investment research company - on the short-term and long-term stock performance companies. I initially hypothesized that after Citron's (http://www.citronresearch.com/who-is-citron-research/) comments stock prices would move significantly. My analysis analyzes the sentiment in Citron's tweets and matches them with stock performance. Also, this analysis investigates opportunities for longer term trading, if any. Morever, such effects as firm size and trading exchane are also tested.
TweetdataRetrieval.py obtains tweets posted by Citron for 2015-2017
yahoo.py obtains historical stock data for stock covered by Citron
match.py matches tweet data and stock symbol with stock data from yahoo for analysis
NaiveBayes_sentiment.py is a script for analyzing sentiment in tweets - can be applied to large scale tweets
tools and libraries: tweepy, nltk, csv libraries.
