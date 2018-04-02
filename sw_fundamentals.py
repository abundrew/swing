#!/bin/python3

import os
import json
import sys
import iex_api
import sw_config
import sw_stock

class Fundamentals:
    def __init__(self,
                 stocks = None,
                 path_financials=sw_config.PATH_FINANCIALS,
                 path_peers=sw_config.PATH_PEERS,
                 path_stats=sw_config.PATH_STATS):
        self._stocks = stocks
        if stocks is None:
            stock = sw_stock.Stock()
            self._stocks = stock.stocks()
        self._path_financials = path_financials
        self._path_peers = path_peers
        self._path_stats = path_stats

    def financials(self, stock):
        try:
            fname = self._path_financials
            if not os.path.isfile(fname):
                financials = iex_api.stock_batch_100(self._stocks, 'financials')
                s = json.dumps(financials)
                with open(fname, 'w') as f:
                    f.write(s)
            with open(fname) as f:
                financials = json.load(f)
            return financials['data'][stock]['financials']['financials']
        except:
            error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
            print(error)

    def peers(self, stock):
        try:
            fname = self._path_peers
            if not os.path.isfile(fname):
                peers = iex_api.stock_batch_100(self._stocks, 'peers')
                s = json.dumps(peers)
                with open(fname, 'w') as f:
                    f.write(s)
            with open(fname) as f:
                peers = json.load(f)
            return peers['data'][stock]['peers']
        except:
            error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
            print(error)

    def stats(self, stock):
        try:
            fname = self._path_stats
            if not os.path.isfile(fname):
                stats = iex_api.stock_batch_100(self._stocks, 'stats')
                s = json.dumps(stats)
                with open(fname, 'w') as f:
                    f.write(s)
            with open(fname) as f:
                stats = json.load(f)
            return stats['data'][stock]['stats']
        except:
            error = "ERROR: {} {}".format(sys.exc_info()[0], sys.exc_info()[1])
            print(error)
