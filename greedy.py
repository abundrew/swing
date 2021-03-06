#!/bin/python3

import time
import pandas as pd
import os
import config
import daily
import intraday
import stock

while True:
    print('=' * 80)
    print('$$$$$ GREEDY $$$$$')
    print('-' * 80)
    print('1 - help')
    print('2 - update fundamentals (once in a while)')
    print('3 - download missing daily files')
    print('4 - update daily files (with US Equities files)')
    print('5 - update studies')
    print('6 - update selections')
    print('7 - get cross-selection')
    print('8 - get stats')
    print('9 - update intraday files (once a week)')
    print('10 - update symbols (with US Equities files)')
    print('0 - exit')
    print('=' * 80)
    print('enter choice #', end=':')
    script = int(input())

    if script == 1:
        # ---------------------------------------------------------------------------
        # help
        # ---------------------------------------------------------------------------
        print('A. Download fundamentals')
        print('B. Download daily files')
        print('C. Download US Equities')
        print('   at http://eoddata.com/myaccount/accountdetails.aspx')
        print("   to '../data/daily/eoddata/USE_{}.txt'")
        print("   Skip holidays")
        print("   (http://www.theholidayschedule.com/nyse-holidays.php)")
        print('D. Update symbols.csv with symbols from US Equities file')
        print("   Replace '^([^,]+)(.*)$' with '\\1'")
        print('E. Update daily files using US Equities files by date')
        print('F. Update study files')
        print('G. Update selections')
        print('H. Get cross-selection')
        print('I. Get stats')

    elif script == 2:
        # ---------------------------------------------------------------------------
        # update fundamentals (once in a while)
        # ---------------------------------------------------------------------------
        if input('update fundamentals. start? [Y/N]').upper() == 'Y':
            started = time.time()
            stock.Fundamentals().update()
            print(time.strftime('"update fundamentals" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 3:
        # ---------------------------------------------------------------------------
        # download missing daily files
        # ---------------------------------------------------------------------------
        if input('download missing daily files. start? [Y/N]').upper() == 'Y':
            started = time.time()
            history = daily.History()
            symbols = stock.Symbol().symbols()
            history.download(symbols)
            print(time.strftime('"download missing daily files" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 4:
        # ---------------------------------------------------------------------------
        # update daily files (with US Equities file)
        # ---------------------------------------------------------------------------
        if input('update daily files (with US Equities file). start? [Y/N]').upper() == 'Y':
            print('start date [YYYY-MM-DD]', end=':')
            start_date = input()
            print('end date [YYYY-MM-DD]', end=':')
            end_date = input()
            started = time.time()
            history = daily.History()
            symbols = stock.Symbol().symbols()
            for di in pd.date_range(start_date, end_date):
                eoddate = str(di)[:10]
                print(eoddate)
                fname = config.FORMAT_DAILY_EODDATA.format(eoddate[:4] + eoddate[5:7] + eoddate[8:])
                history.update_from_file(symbols, fname)
            print(time.strftime('"update daily files (with US Equities file)" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 5:
        # ---------------------------------------------------------------------------
        # update studies
        # ---------------------------------------------------------------------------
        if input('update studies. start? [Y/N]').upper() == 'Y':
            started = time.time()
            symbols = stock.Symbol().symbols()
            daily.Study().update(symbols)
            print(time.strftime('"update studies" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 6:
        # ---------------------------------------------------------------------------
        # update selections
        # ---------------------------------------------------------------------------
        started = time.time()
        stock.Selection().update()
        print(time.strftime('"update selections" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 7:
        # ---------------------------------------------------------------------------
        # get cross-selection
        # ---------------------------------------------------------------------------
        print ('1. uptrend + more $20 + liquid + crsi < 10')
        print ('2. uptrend + more $20 + liquid + crsi < 20')
        print ('3. uptrend + more $20 + liquid + crsi < 25')
        print('enter choice #', end=':')
        choice = int(input())

        if choice == 1:
            # ---------------------------------------------------------------------------
            # uptrend + more $20 + liquid + crsi < 10
            # ---------------------------------------------------------------------------
            selected = stock.Selection().select(['UPTREND','MORE_20','LIQUID','CRSI_10'])

        elif choice == 2:
            # ---------------------------------------------------------------------------
            # uptrend + more $20 + liquid + crsi < 20
            # ---------------------------------------------------------------------------
            selected = stock.Selection().select(['UPTREND','MORE_20','LIQUID','CRSI_20'])

        elif choice == 3:
            # ---------------------------------------------------------------------------
            # uptrend + more $20 + liquid + crsi < 25
            # ---------------------------------------------------------------------------
            selected = stock.Selection().select(['UPTREND','MORE_20','LIQUID','CRSI_25'])

        else:
            continue

        history = daily.History()
        study = daily.Study()
        fundamentals = stock.Fundamentals()
        print()
        print(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))
        print('{} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format('-' * 5, '-' * 6, '-' * 6, '-' * 6, '-' * 8, '-' * 8, '-' * 8, '-' * 8, '-' * 8, '-' * 5, '-' * 5, '-' * 5, '-' * 5, '-' * 20))
        print('stock +/-(%) +/-(%) +/-(%)    close   w52low  w52high   vol(M)   cap(B)  crsi   p/s   p/b   d/e company')
        print('{} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format('-' * 5, '-' * 6, '-' * 6, '-' * 6, '-' * 8, '-' * 8, '-' * 8, '-' * 8, '-' * 8, '-' * 5, '-' * 5, '-' * 5, '-' * 5, '-' * 20))
        for symbol in selected:
            hdf = history.to_dataframe(symbol)
            sdf = study.to_dataframe(symbol)
            stats = fundamentals.stats(symbol)
            try:
                print('{:5} {:6.2f} {:6.2f} {:6.2f} {:8.2f} {:8.2f} {:8.2f} {:8.2f} {:8.2f} {:5.1f} {:5.1f} {:5.1f} {:5.1f} {}'.format(
                    symbol,
                    ((hdf.iloc[-3]['close'] - hdf.iloc[-4]['close']) / hdf.iloc[-4]['close']) * 100,
                    ((hdf.iloc[-2]['close'] - hdf.iloc[-3]['close']) / hdf.iloc[-3]['close']) * 100,
                    ((hdf.iloc[-1]['close'] - hdf.iloc[-2]['close']) / hdf.iloc[-2]['close']) * 100,
                    hdf.iloc[-1]['close'],
                    hdf.iloc[-255:]['close'].min(),
                    hdf.iloc[-255:]['close'].max(),
                    hdf.iloc[-10:]['volume'].mean() / 1000000,
                    stats['marketcap'] / 1000000000,
                    sdf.iloc[-1]['crsi'],
                    stats['priceToSales'],
                    stats['priceToBook'],
                    stats['debt'] / stats['EBITDA'],
                    stats['companyName'][:20]
                ))
            except:
                pass
        print('{} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format('-' * 5, '-' * 6, '-' * 6, '-' * 6, '-' * 8, '-' * 8, '-' * 8, '-' * 8, '-' * 8, '-' * 5, '-' * 5, '-' * 5, '-' * 5, '-' * 20))
        print()

    elif script == 8:
        # ---------------------------------------------------------------------------
        # get stats
        # ---------------------------------------------------------------------------
        symbol = input('enter symbol:').upper()
        fundamentals = stock.Fundamentals()
        stats = fundamentals.stats(symbol)
        for key in list(stats):
            print('{} : {}'.format(key, stats[key]))

    elif script == 9:
        # ---------------------------------------------------------------------------
        # update intraday files (once a week)
        # ---------------------------------------------------------------------------
        if input('update intraday files. start? [Y/N]').upper() == 'Y':
            started = time.time()
            history = intraday.History()
            symbols = stock.Symbol().symbols()
            history.download(symbols)
            history.update(symbols)
            print(time.strftime('"update intraday files" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 10:
        # ---------------------------------------------------------------------------
        # update symbols (with US Equities files)
        # ---------------------------------------------------------------------------
        if input('update symbols (with US Equities files). start? [Y/N]').upper() == 'Y':
            print('start date [YYYY-MM-DD]', end=':')
            start_date = input()
            print('end date [YYYY-MM-DD]', end=':')
            end_date = input()
            started = time.time()
            symbols = set([])
            for di in pd.date_range(start_date, end_date):
                eoddate = str(di)[:10]
                print(eoddate)
                selected = set([])
                fname = config.FORMAT_DAILY_EODDATA.format(eoddate[:4] + eoddate[5:7] + eoddate[8:])
                if not os.path.isfile(fname):
                    print('- file not found -')
                    continue
                with open(fname, 'r') as f:
                    for line in f:
                        parts = line.split(',')
                        symbol = parts[0]
                        if '.' in symbol: continue
                        if '-' in symbol: continue
                        if len(symbols) == 0 or symbol in symbols:
                            selected.add(symbol)
                symbols = selected
            symbols = list(symbols)
            symbols.sort()
            with open(config.PATH_SYMBOLS, 'w') as f:
                for symbol in symbols:
                    f.write(symbol + '\n')

            print("symbols # {}".format(len(symbols)))
            print(time.strftime('"update symbols (with US Equities files)" finished in %H:%M:%S ', time.gmtime(time.time() - started)))

    elif script == 0:
        # ---------------------------------------------------------------------------
        # exit
        # ---------------------------------------------------------------------------
        break
