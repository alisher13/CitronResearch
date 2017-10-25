import csv
from datetime import datetime, timedelta
 import os.path


 def get_stock_prices(file_name):
    # date (object, not string) will be the dictionary key, adjusted
    # close will be the value something like {"2017-01-01": 200, ...}
    data = {}

    if not os.path.isfile(file_name):
        print("ERROR: %s doesn't exist" % file_name)
        return data

    with open(file_name) as ticker_csv:
        ticker_reader = csv.reader(
            ticker_csv, delimiter=',', quotechar='|')
        next(ticker_reader, None)  # skip the header
        for row in ticker_reader:
            try:
                data[datetime.strptime(row[0], "%Y-%m-%d")] = float(row[5])
            except Exception as e:
                # print('Skipping row: ', row, e)
                # headers appear multiple times in the input data
                pass
    return data


def get_price_on_or_before_date(date, prices):
    """Given the date, find the price on that date, if the price doesn't
    exist on that date, go back one day and return the price, do so
    5 days until the price is found. Because, assuming date is on
    Monday, if there's no price for Monday, look at Sunday, and of
    course no price for Sunday, so do it for Saturday, and lastly for
    Friday. For some reason Friday maybe a holiday, so do it 2 more
    days.
    The return value will look something like (200, 1), where 200 is the
    price and 1 is the 1 day before the given date. The values for 1 can
    be anything between 0 and 5 inclusive. 0 means the price is for the
    given date. If no price is found, an empty tuple is returned.
    """
    for i in range(6):
        current_date = date - timedelta(days=i)
        if current_date in prices:
            return float(prices[current_date]), i
    return (None, None)


def get_tweets(citron_file):
    """Get tweet date, text, and symbol from the Citron CSV file."""
    tweets = []
    with open(citron_file) as csvfile:
        ticker_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(ticker_reader, None)  # skip the header
        for row in ticker_reader:
       
            if row[3].strip():
              
                tweets.append({
                    'date': datetime.strptime(row[1], "%y-%m-%d"),
                    'text': row[2],
                    'ticker': row[3].strip()
                })
    return tweets


output = []
tweets = get_tweets('stock data/@CitronResearch222.csv')
for tweet in tweets:
    print('processing %s' % tweet['ticker'])
    stock_prices = get_stock_prices('stock data/%s.csv' %
                                    tweet['ticker'])
    prev_day_price, days_early = get_price_on_or_before_date(
        tweet['date'] - timedelta(days=1), stock_prices
    )
    days = (0, 3, 30, 180, 365)
    price_changes = []
    for day in days:
        price, diff = get_price_on_or_before_date(
            tweet['date'] + timedelta(days=day), stock_prices
        )
        if price is None or prev_day_price is None or\
           (day in (0, 3) and diff != 0):
            price_changes.append('')
        else:
            price_changes.append(
                (price - prev_day_price) / prev_day_price
            )

    output.append(
        [
            tweet['date'].strftime('%Y-%m-%d'),
            tweet['text'],
            tweet['ticker'],
            prev_day_price,
        ] + price_changes
    )


with open('results.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        'Tweet Date', 'Tweet Text', 'Tweet Ticker',
        'Prev day price',
        '1 day price change', '3 day price change',
        '1 month price change',  '6 month price change',
        '1 year price change'
    ])

    for row in output:
        writer.writerow(row)
    print("Done: see results.csv")
