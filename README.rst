pandas-datareader
=================

Up to date remote data access for pandas, works for multiple versions of pandas.

.. image:: https://img.shields.io/pypi/v/pandas-datareader.svg
    :target: https://pypi.python.org/pypi/pandas-datareader/
    
.. image:: https://img.shields.io/pypi/dm/pandas-datareader.svg
    :target: https://pypi.python.org/pypi/pandas-datareader/

.. image:: https://travis-ci.org/pydata/pandas-datareader.svg?branch=master
    :target: https://travis-ci.org/pydata/pandas-datareader

.. image:: https://coveralls.io/repos/pydata/pandas-datareader/badge.svg?branch=master
    :target: https://coveralls.io/r/pydata/pandas-datareader

.. image:: https://readthedocs.org/projects/pandas-datareader/badge/?version=latest
    :target: http://pandas-datareader.readthedocs.org/en/latest/

.. image:: https://landscape.io/github/pydata/pandas-datareader/master/landscape.svg?style=flat
   :target: https://landscape.io/github/pydata/pandas-datareader/master
   :alt: Code Health

Installation
------------

Install via pip

.. code-block:: shell

   $ pip install pandas-datareader

Usage
-----

Starting in 0.19.0, pandas will no longer support ``pandas.io.data`` or ``pandas.io.wb``, so
you must replace your imports from ``pandas.io`` with those from ``pandas_datareader``:

.. code-block:: python

   from pandas.io import data, wb # becomes
   from pandas_datareader import data, wb

Many functions from the data module have been included in the top level API.

.. code-block:: python

   import pandas_datareader as pdr
   pdr.get_data_yahoo('AAPL')

See the `pandas-datareader documentation <http://pandas-datareader.readthedocs.org/>`_ for more details.
