import pandas as pd
import requests
import time
from datetime import datetime
import pandas_datareader as web
from bs4 import BeautifulSoup
import logging


class ScrapeStock:
    def __init__(self, code):
        self.code = code
        self.frame = pd.DataFrame
        self.y0 = '2010-01-01'
        self.y1 = datetime.now().strftime('%Y-%m-%d')
        self.method = 'stooq'

    def scraypeData(self):
        if self.method == 'stooq':
            codeJP = str(self.code) + '.jp'
            try:
                self.frame = web.stooq.StooqDailyReader(symbols=codeJP, start=self.y0, end=self.y1).read()
            except Exception as e:
                logging.warning('CRITICAL at stooq ERROR {}'.format(e))
                self.method = 'bs'
            else:
                logging.info('Success to Scrayping at stooq {}'.format(len(self.frame)))
                self.index_list = self.frame.index
                if len(self.frame) > 0:
                    return True
                else:
                    logging.warning('No stock data has got {}'.format(self.code))
                    self.method = 'bs'
        if self.method == 'bs':
            try:
                try:
                    y = datetime.now().year
                    url = 'https://kabuoji3.com/stock/{}/{}/'.format(self.code, y)
                    headers = {
                        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
                    }
                    soup = BeautifulSoup(requests.get(url=url, headers=headers).content, 'html.parser')
                except Exception as e:
                    logging.info('no stock data : '.format(self.code))
                    return False
                data = []
                headers = {
                    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
                }
                for i in range(datetime.now().year - datetime.strptime(self.y0, '%Y-%m-%d').year):
                    y = datetime.strptime(self.y0, '%Y-%m-%d').year + i
                    url = 'https://kabuoji3.com/stock/{}/{}/'.format(self.code, y)
                    soup = BeautifulSoup(requests.get(url=url, headers=headers).content, 'html.parser')
                    tag_tr = soup.find_all('tr')

                    head = [h.text for h in tag_tr[0].find_all('th')]
                    for j in range(1, len(tag_tr)):
                        data.append([float(d.text) if d.text.isdecimal() else d.text for d in tag_tr[j].find_all('td')])
                    logging.info('{} data scrayping was done'.format(y))
                    time.sleep(1)
                self.frame = pd.DataFrame(data, columns=head)
                self.frame = self.frame.rename(
                    columns={'日付': 'date', '始値': 'Open', '終値': 'Close', '高値': 'High', '安値': 'Low', '出来高': 'Volume'})
                logging.info('Success to Scrayping at bs {}'.format(len(self.frame)))
            except Exception as e:
                logging.warning('CRITICAL at beautifulsoup ERROR {}'.format(e))
            else:
                if self.frame.empty:
                    return False
                else:
                    logging.info('Success to Scrayping at bs {}'.format(self.frame.iloc[0]))
                    self.index_list = self.frame.index
                    if len(self.frame) > 0:
                        return True
                    else:
                        logging.warning('No stock data has got {}'.format(self.code))
                        return False

    def getData(self):
        return self.frame

    def get_date(self, i):
        if self.frame.empty:
            return 'null'
        else:
            logging.info('i_data function is called method=={}'.format(self.method))
            i_date = ''
            if self.method == 'stooq':
                i_date = str(self.index_list[i].strftime('%Y-%m-%d'))
                logging.info('i_data {}'.format(i_date))
            elif self.method == 'bs':
                # else:
                logging.info('i_data function is called method=={}'.format(self.method))
                logging.info('getdata {}'.format(self.method))
                i_date = str(self.frame.iloc[i].loc['date'])
                logging.info('i_data {}'.format(i_date))
            logging.info('i_data {}'.format(i_date))
            return i_date

    def get_open(self, i):
        if self.frame.empty:
            return 0
        else:
            return self.frame.iloc[i].loc['Open']

    def get_high(self, i):
        if self.frame.empty:
            return 0
        else:
            return self.frame.iloc[i].loc['High']

    def get_low(self, i):
        if self.frame.empty:
            return 0
        else:
            return self.frame.iloc[i].loc['Low']

    def get_close(self, i):
        if self.frame.empty:
            return 0
        else:
            return self.frame.iloc[i].loc['Close']

    def get_volume(self, i):
        if self.frame.empty:
            return 0
        else:
            return self.frame.iloc[i].loc['Volume']

    def get_length(self):
        logging.info('length {}'.format(len(self.frame)))
        return len(self.frame)



