from datetime import datetime

import numpy as np
import pandas as pd
from pandas import compat
import pandas_datareader.data as web
from pandas_datareader.data import GoogleDailyReader
from pandas_datareader._utils import (RemoteDataError, SymbolWarning)

import requests

import warnings
import nose
import pandas.util.testing as tm
from nose.tools import assert_equal
from pandas.util.testing import assert_series_equal
from pandas_datareader.tests._utils import _get_session, _get_logger

logger = _get_logger()

def assert_n_failed_equals_n_null_columns(wngs, obj, cls=SymbolWarning):
    all_nan_cols = pd.Series(dict((k, pd.isnull(v).all()) for k, v in
                                  compat.iteritems(obj)))
    n_all_nan_cols = all_nan_cols.sum()
    valid_warnings = pd.Series([wng for wng in wngs if wng.category == cls])
    assert_equal(len(valid_warnings), n_all_nan_cols)
    failed_symbols = all_nan_cols[all_nan_cols].index
    msgs = valid_warnings.map(lambda x: x.message)
    assert msgs.str.contains('|'.join(failed_symbols)).all()


class TestGoogle(tm.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestGoogle, cls).setUpClass()
        cls.locales = tm.get_locales(prefix='en_US')
        if not cls.locales:  # pragma: no cover
            raise nose.SkipTest("US English locale not available for testing")

    @classmethod
    def tearDownClass(cls):
        super(TestGoogle, cls).tearDownClass()
        del cls.locales

    def test_google(self):
        # asserts that google is minimally working and that it throws
        # an exception when DataReader can't get a 200 response from
        # google
        start = datetime(2010, 1, 1)
        end = datetime(2013, 1, 27)

        for locale in self.locales:
            with tm.set_locale(locale):
                panel = web.DataReader("F", 'google', start, end)
            self.assertEqual(panel.Close[-1], 13.68)

        self.assertRaises(Exception, web.DataReader, "NON EXISTENT TICKER",
                          'google', start, end)

    def test_get_quote_stringlist(self):
        df = web.get_quote_google(['GOOG', 'AMZN', 'GOOG'])
        assert_series_equal(df.ix[0], df.ix[2])

    def test_get_goog_volume(self):
        for locale in self.locales:
            with tm.set_locale(locale):
                df = web.get_data_google('GOOG').sort_index()
            self.assertEqual(df.Volume.ix['JAN-02-2015'], 1446662)

    def test_get_multi1(self):
        for locale in self.locales:
            sl = ['AAPL', 'AMZN', 'GOOG']
            with tm.set_locale(locale):
                pan = web.get_data_google(sl, '2012')
            ts = pan.Close.GOOG.index[pan.Close.AAPL < pan.Close.GOOG]
            if (hasattr(pan, 'Close') and hasattr(pan.Close, 'GOOG') and
                    hasattr(pan.Close, 'AAPL')):
                self.assertEqual(ts[0].dayofyear, 3)
            else:  # pragma: no cover
                self.assertRaises(AttributeError, lambda: pan.Close)

    def test_get_multi_invalid(self):
        sl = ['AAPL', 'AMZN', 'INVALID']
        pan = web.get_data_google(sl, '2012')
        self.assertIn('INVALID', pan.minor_axis)

    def test_get_multi_all_invalid(self):
        sl = ['INVALID', 'INVALID2', 'INVALID3']
        self.assertRaises(RemoteDataError, web.get_data_google, sl, '2012')

    def test_get_multi2(self):
        with warnings.catch_warnings(record=True) as w:
            for locale in self.locales:
                with tm.set_locale(locale):
                    pan = web.get_data_google(['GE', 'MSFT', 'INTC'],
                                              'JAN-01-12', 'JAN-31-12')
                result = pan.Close.ix['01-18-12']
                assert_n_failed_equals_n_null_columns(w, result)

                # sanity checking

                assert np.issubdtype(result.dtype, np.floating)
                result = pan.Open.ix['Jan-15-12':'Jan-20-12']
                self.assertEqual((4, 3), result.shape)
                assert_n_failed_equals_n_null_columns(w, result)

    def test_dtypes(self):
        # GH3995, #GH8980
        data = web.get_data_google('F', start='JAN-01-10', end='JAN-27-13')
        assert np.issubdtype(data.Open.dtype, np.number)
        assert np.issubdtype(data.Close.dtype, np.number)
        assert np.issubdtype(data.Low.dtype, np.number)
        assert np.issubdtype(data.High.dtype, np.number)
        assert np.issubdtype(data.Volume.dtype, np.number)

    def test_unicode_date(self):
        # GH8967
        data = web.get_data_google('F', start='JAN-01-10', end='JAN-27-13')
        self.assertEqual(data.index.name, 'Date')

    def test_google_reader_class(self):
        r = GoogleDailyReader('GOOG')
        df = r.read()
        self.assertEqual(df.Volume.ix['JAN-02-2015'], 1446662)

        session = requests.Session()
        r = GoogleDailyReader('GOOG', session=session)
        self.assertTrue(r.session is session)

    def test_bad_retry_count(self):

        with tm.assertRaises(ValueError):
            web.get_data_google('F', retry_count=-1)
    

class TestGoogleIntraday(tm.TestCase):
    def test_google_intra(self):
        session = _get_session()
        freq = '1Min'
        df = web.DataReader(name='GOOG', data_source='google-intraday', 
                start='2016-02-20', end='2016-02-05', freq=freq, session=session)
        print(df)
        assert 'Open' in df.columns
        assert 'High' in df.columns
        assert 'Low' in df.columns
        assert 'Close' in df.columns
        idx = pd.Series(df.index)
        assert (idx - idx.shift()).value_counts().index[0] == pd.offsets.to_timedelta(freq)

    def test_google_intra_multi(self):
        session = _get_session()
        freq = '1Min'
        df = web.DataReader(name=['GOOG', 'MSFT'], data_source='google-intraday', start='2016-02-01', end='2016-02-05', freq=freq, session=session)
        print(df)
        print(df.loc['Close', :, :])


if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)  # pragma: no cover
