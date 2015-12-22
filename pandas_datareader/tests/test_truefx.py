import pandas as pd
import pandas.util.testing as tm
import pandas_datareader.data as web
from pandas_datareader.truefx import TrueFXReader

class TestTrueFX(tm.TestCase):
    def setUp(self):
        #session = None
        
        # Uncomment this for local tests without network
        import requests_cache
        from datetime import timedelta
        session = requests_cache.CachedSession(cache_name='cache', expire_after=timedelta(days=30))
        
        self.dr = TrueFXReader(retry_count=3, pause=0.001, session=session)

    def test_url(self):
        expected = 'http://www.truefx.com/dev/data/2014/JANUARY-2014/AUDUSD-2014-01.zip'
        tm.assert_equal(self.dr.url('AUDUSD', 2014, 1), expected)

    def test_filename_csv(self):
        expected = 'AUDUSD-2014-01.csv'
        tm.assert_equal(self.dr._filename_csv('AUDUSD', 2014, 1), expected)

    def test_get_truefx_read_one_month(self):
        symbol = 'AUDUSD'
        df = self.dr._read_one_month(symbol, 2014, 1)
        tm.assert_equal(df['Ask']['2014-01-01 21:55:34.404'], 0.88922)

    def test_get_truefx_datareader(self):
        df = web.DataReader('AUD/USD', 'truefx', '2014-01-01', '2014-02-28')
        tm.assert_equal(df['Ask']['2014-01-01 21:55:34.404'], 0.88922)
        tm.assert_equal(df['Ask']['2014-02-03 00:03:38.169'], 0.87524)

if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
