import io
import base64
import yfinance as yf
import backtrader as bt
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from .models import Back_Test_Trade
import datetime as dt
from django.utils.timezone import make_naive

class TestStrategy(bt.Strategy):
    params = (('ticker', ''),)

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close)
    
    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.buy()
                Back_Test_Trade.objects.create(
                    trade_type='BUY',
                    ticker=self.params.ticker,
                    quantity=1,
                    price=self.data.close[0],
                    timestamp=self.data.datetime.datetime(0)  # Save exact timestamp of execution
                )
        elif self.rsi > 70:
            self.sell()
            Back_Test_Trade.objects.create(
                    trade_type='SELL',
                    ticker=self.params.ticker,
                    quantity=1,
                    price=self.data.close[0],
                    timestamp=self.data.datetime.datetime(0)  # Save exact timestamp of execution
                )

class PandasData(bt.feeds.PandasData):
    cols = (
        ('Open', 'open'),
        ('High', 'high'),
        ('Low', 'low'),
        ('Close', 'close'),
        ('Volume', 'volume'),
        ('Adj Close', 'adj close'),
    )

def home(request):
    return render(request, 'trading_app/backtest_menu.html')

def run_backtest(request):
    Back_Test_Trade.objects.all().delete()

    ticker = request.GET.get('ticker', 'AAPL')
    start_date = request.GET.get('start_date', '2021-01-01')
    end_date = request.GET.get('end_date', dt.datetime.now().strftime('%Y-%m-%d'))

    data = yf.download(str(ticker), start=start_date, end=end_date)

    if data.empty or len(data) == 0:
        return HttpResponse("No data fetched. Please check the ticker symbol and date range.", status=400)

    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy, ticker=ticker)

    data_feed = PandasData(dataname=data)
    cerebro.adddata(data_feed)
    cerebro.run()

    trade_data = Back_Test_Trade.objects.all().values('timestamp', 'trade_type', 'price')
    if not trade_data.exists():
        return HttpResponse("No trades were made during the backtest.", status=400)

    trades = pd.DataFrame(trade_data)

    if trades.empty:
        return HttpResponse("No trades were recorded in this backtest.", status=400)

    data['Date'] = data.index
    data.reset_index(drop=True, inplace=True)
    data['Trade'] = ''

    # Make all timestamps timezone-naive for comparison
    trades['timestamp'] = trades['timestamp'].apply(make_naive)

    for index, row in trades.iterrows():
        closest_index = (data['Date'] - row['timestamp']).abs().idxmin()
        data.at[closest_index, 'Trade'] = row['trade_type']

    plotly_data = {
        'dates': data['Date'].astype(str).tolist(),
        'open': data['Open'].tolist(),
        'high': data['High'].tolist(),
        'low': data['Low'].tolist(),
        'close': data['Close'].tolist(),
        'trades': data['Trade'].tolist(),
    }

    return render(request, 'trading_app/results.html', {'plotly_data': plotly_data, 'ticker': ticker})

def trades_list(request):
    trades = Back_Test_Trade.objects.all().order_by('-timestamp')
    return render(request, 'trading_app/trades_list.html', {'trades': trades})
