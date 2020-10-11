import time
import datetime

import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def plot_stock_price_from_date_to_date(stock_name, from_date, to_date):

    ticker = yf.Ticker(stock_name)
    df = ticker.history(start=from_date, end=to_date)["Close"]
    stock_price = df.values
    dates = df.index.values

    _min_stock_price = min(stock_price)
    _max_stock_price = max(stock_price)
    _cur_stock_price = stock_price[-1]

    from_date_as_dt = datetime.datetime.strptime(str(from_date), '%Y-%m-%d')
    to_date_as_dt = datetime.datetime.strptime(str(to_date), '%Y-%m-%d')

    sns.lineplot(dates, stock_price)
    title = str(stock_name + " " + from_date + "-" + to_date)
    plt.title(title)
    plt.show(block=True)


if __name__ == '__main__':

    ticker = yf.Ticker("MNST")
    from_date = "2015-01-01"
    to_date = "2021-01-01"
    stock_price = ticker.history(start=from_date, end=to_date)

    plot_stock_price_from_date_to_date("MNST", from_date, to_date)
