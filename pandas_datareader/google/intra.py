import pandas as pd

from pandas_datareader.base import _DailyBaseReader


class CANDLE():
    DATE = 'Date'
    OPEN = 'Open'
    HIGH = 'High'
    LOW = 'Low'
    CLOSE = 'Close'
    VOLUME = 'Volume'
    
    @staticmethod
    def LST_PRICE():
        return([CANDLE.OPEN, CANDLE.HIGH, CANDLE.LOW, CANDLE.CLOSE])

    @staticmethod
    def LST_ALL():
        return([CANDLE.DATE, CANDLE.OPEN, CANDLE.HIGH, CANDLE.LOW, CANDLE.CLOSE, CANDLE.VOLUME])

    @staticmethod
    def LST():
        return([CANDLE.OPEN, CANDLE.HIGH, CANDLE.LOW, CANDLE.CLOSE, CANDLE.VOLUME])


def timestamp_to_unix(dt, unit='s'):
    """
    Return unix timestamp from Pandas Timestamp
    """
    d = {
        's': 1000000000,
        'ms': 1000000,
        'us': 1000,
        'ns': 1
    }
    return(dt.value / d[unit])


class GoogleIntraReader(_DailyBaseReader):

    @property
    def url(self):
        return 'https://www.google.com/finance/getprices'

    def _read_lines(self, data):
        df = pd.read_csv(data, sep=',', skiprows=7, header=None, names=CANDLE.LST_ALL())
        b_dateround = df[CANDLE.DATE].map(lambda dt: dt[0]=='a')
        ts_dateround = df[b_dateround][CANDLE.DATE].map(lambda dt: int(dt[1:]))
        ts_dateround = ts_dateround.align(df[CANDLE.DATE])[0]
        ts_dateround = ts_dateround.fillna(method='ffill')
        ts_seconds = df[~b_dateround][CANDLE.DATE].astype(int) * self.interval_seconds
        ts_seconds = ts_seconds.align(df[CANDLE.DATE])[0].fillna(0)
        df[CANDLE.DATE] = ts_dateround + ts_seconds
        df[CANDLE.DATE] = pd.to_datetime(df[CANDLE.DATE], unit='s')
        df = df.set_index(CANDLE.DATE)
        return(df[CANDLE.LST()])

    @property
    def interval_seconds(self):
        return self.freq.total_seconds()

    def _get_params(self, symbol, format_data='d,c,h,l,o,v', df='cpct', auto='', ei='', 
                    exchange='NASD', period='3d'):
        ts = timestamp_to_unix(self.start)
        params = {
            'q': symbol,  # Stock symbol
            'x': exchange,  # Stock exchange symbol on which stock is traded (ex: NASD ETR ...)
            'i': self.interval_seconds,  # Interval size in seconds (86400 = 1 day intervals)
            'p': period,  # Period. (A number followed by a "d" or "Y", eg. Days or years. Ex: 40Y = 40 years.)
            'f': format_data,  # What data do you want? d (date - timestamp/interval, c - close, v - volume, etc...) Note: Column order may not match what you specify here
            'df': df,
            'auto': auto,
            'ei': ei,
            'ts': ts  # Starting timestamp (Unix format). If blank, it uses today.
        }
        print(params)
        return params