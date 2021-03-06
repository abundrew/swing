#!/bin/python3

import os
import sys
import pandas as pd
import av
import calcs
import config

class History:
    def __init__(self):
        self._reader = av.DataReader()

    def to_dataframe(self, symbol):
        try:
            fname = config.FORMAT_DAILY_HISTORY.format(symbol)
            if not os.path.isfile(fname): return None
            return pd.read_csv(fname, parse_dates=['date'], index_col='date')
        except:
            print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))

    # outputsize: full
    def download(self, symbols, skip_if_exists=True):
        print('-----> downloading daily history ...')
        if isinstance(symbols, str):
            symbols = [symbols]
        for symbol in symbols:
            fname = config.FORMAT_DAILY_HISTORY.format(symbol)
            if skip_if_exists and os.path.isfile(fname):
                continue
            print(symbol)
            try:
                data = self._reader.time_series_daily(symbol, True)
                if (data['success']):
                    df = data['data']
                    df.to_csv(fname)
            except KeyboardInterrupt:
                print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
                break
            except:
                print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        print('<----- downloading daily history ...')

    # outputsize: compact
    def update(self, symbols):
        print('-----> updating daily history ...')
        data = self._reader.time_series_daily(config.SYMBOL_A)
        if not data['success']:
            print('ERROR: {}'.format(data['error']))
            return
        update_date = str(data['data'].index.max())
        if isinstance(symbols, str):
            symbols = [symbols]
        for symbol in symbols:
            fname = config.FORMAT_DAILY_HISTORY.format(symbol)
            print(symbol)
            try:
                if not os.path.isfile(fname):
                    print('- the file not found -')
                    continue
                df = pd.read_csv(fname, parse_dates=['date'], index_col='date')
                last_date = str(df.index.max())
                if last_date >= update_date:
                    print('+ data is up to date +')
                    continue
                data = self._reader.time_series_daily(symbol)
                if not data['success']:
                    print('ERROR: {}'.format(data['error']))
                    continue
                df_update = data['data']
                df_new = pd.concat([df, df_update[last_date:].iloc[1:]]).drop_duplicates()
                df_new.to_csv(fname)
            except KeyboardInterrupt:
                print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
                break
            except:
                print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        print('<----- updating daily history ...')

    def update_from_file(self, symbols, fname):
        if not os.path.isfile(fname):
            print('- file not found -')
            return
        with open(fname, 'r') as f:
            for line in f:
                parts = line.split(',')
                symbol = parts[0]
                if symbol in symbols:
                    hdf = self.to_dataframe(symbol)
                    sdate = pd.Timestamp('{}-{}-{}'.format(parts[1][:4], parts[1][4:6], parts[1][6:]))
                    if not sdate in hdf.index:
                        try:
                            hdf.loc[sdate] = [parts[2], parts[3], parts[4], parts[5], parts[6].strip()]
                            hdf = hdf.sort_index()
                            hdf.to_csv(config.FORMAT_DAILY_HISTORY.format(symbol))
                        except:
                            print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))

class Study:
    def __init__(self):
        self._history = History()

    def to_dataframe(self, symbol):
        try:
            fname = config.FORMAT_DAILY_STUDY.format(symbol)
            if not os.path.isfile(fname): return None
            return pd.read_csv(fname, parse_dates=['date'], index_col='date')
        except:
            print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))

    def update(self, symbols):
        print('-----> updating daily study ...')
        if isinstance(symbols, str):
            symbols = [symbols]
        for symbol in symbols:
            fname = config.FORMAT_DAILY_STUDY.format(symbol)
            print(symbol)
            try:
                hdf = self._history.to_dataframe(symbol)
                if hdf is None: continue
                adx_10 = pd.Series(calcs.ADX(hdf['high'].values, hdf['low'].values, hdf['close'].values, 10),
                                   index=hdf['high'].index).round(2)
                bb_mean = hdf['close'].rolling(20).mean().round(2)
                bb_std = hdf['close'].rolling(20).std().round(2)
                crsi = pd.Series(calcs.Connors_RSI(hdf['close'].values, 3, 2, 100), index=hdf['close'].index).round(2)
                ma_200 = hdf['close'].rolling(200).mean().round(2)
                ma_50 = hdf['close'].rolling(50).mean().round(2)
                rsi_14 = pd.Series(calcs.RSI(hdf['close'].values, 14), index=hdf['close'].index).round(2)
                df_study = pd.DataFrame(data={'adx_10': adx_10,
                                              'bb_mean': bb_mean,
                                              'bb_std': bb_std,
                                              'crsi': crsi,
                                              'ma_200': ma_200,
                                              'ma_50': ma_50,
                                              'rsi_14': rsi_14}, index=hdf.index)
                df_study.to_csv(fname)
            except KeyboardInterrupt:
                print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
                break
            except:
                print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        print('<----- updating daily study ...')

# ----- self-test -------------------------------------------------------------

if __name__ == "__main__":
    print('-' * 80)
    print('test daily.History ...')
    print('-' * 80)
    try:
        history = History()
        history.download('MSFT', False)
        data = history.to_dataframe('MSFT')
        print('MSFT ...')
        print(data.tail())
        history.update('MSFT')
        data = history.to_dataframe('MSFT')
        print('MSFT ...')
        print(data.tail())
    except:
        print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
    print('-' * 80)
    print('test daily.Study ...')
    print('-' * 80)
    try:
        study = Study()
        study.update('MSFT')
        data = study.to_dataframe('MSFT')
        print('MSFT ...')
        print(data.tail())
    except:
        print("ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1]))
    print('-' * 80)
