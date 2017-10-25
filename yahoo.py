
import csv
from datetime import datetime, timedelta

# https://pandas-datareader.readthedocs.io/en/latest/remote_data.html#remote-data-yahoo
import pandas_datareader.data as web

tickers = set()
with open('CitronResearch.csv', newline='', encoding = 'utf-8') as csvfile:
    ticker_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(ticker_reader, None)  # skip the header
    for row in ticker_reader:
        if len(row)>2:
            tickers.update(row[3].split(', '))

for ticker in tickers:
    if not ticker:
        continue
    # first time create a file (w - write)
    mode = 'w'
    start = datetime(2012, 1, 1)
    end = datetime(2017, 10, 17)
    while start <= end:
        temp_end = min(start + timedelta(days=365), end)
        print(ticker, start, temp_end)
        try:
            data = web.DataReader(ticker, 'yahoo', start, temp_end)
            data.to_csv(ticker + '.csv', mode=mode, sep=',', quotechar='|', encoding = 'utf-8')
        except:
            print('ERROR (maybe no data): ', ticker, start, temp_end)
        start = temp_end + timedelta(days=1)
        # in the next iteration we want to append data (a - append)
        mode = 'a'
