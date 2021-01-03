from yahoo_finance_api2 import share
import pandas as pd
import  numpy
import datetime
import matplotlib.pyplot as plt
import logging

class Scrape_yahoo():

    def __init__(self, num):
        self.num = num
        self.numT = str(num)+".T"
        self.share = share.Share(self.numT)

    def getScrape(self, minute, day):
        dataset = self.share.get_historical(share.PERIOD_TYPE_DAY, day, share.FREQUENCY_TYPE_MINUTE, minute)
        df = pd.DataFrame(dataset.values(), index=dataset.keys()).T
        df.timestamp = pd.to_datetime(df.timestamp, unit='ms')
        df.index = pd.DatetimeIndex(df.timestamp, name='timestamp').tz_localize('UTC').tz_convert('Asia/Tokyo')
        self.frame=df
        for i in range(len(self.frame.timestamp)):
           self.frame.timestamp[i] = self.frame.timestamp[i].to_pydatetime() + datetime.timedelta(hours=9)
           # print(str(df.timestamp[i]) )


    def getScrape_month(self, minute, month):
        dataset = self.share.get_historical(share.PERIOD_TYPE_MONTH, month, share.FREQUENCY_TYPE_MINUTE, minute)
        self.frame = pd.DataFrame(dataset.values(), index=dataset.keys()).T
        self.frame.timestamp = pd.to_datetime(self.frame.timestamp, unit='ms')
        self.frame.index = pd.DatetimeIndex(self.frame.timestamp, name='timestamp').tz_localize('UTC').tz_convert('Asia/Tokyo')
        for i in range(len(self.frame.timestamp)):
           self.frame.timestamp[i] = self.frame.timestamp[i].to_pydatetime() + datetime.timedelta(hours=9)
           # print(str(df.timestamp[i]) )

    def get_length(self):
        return len(self.frame)

    def get_date(self, i):
        if self.frame.empty:
            return 'null'
        else:
            i_date = ''
            i_date = str(self.frame.iloc[i].timestamp)
            return i_date

    def get_open(self, i):
        if self.frame.empty:
            return 0
        else:
            return self.frame.iloc[i].open

    def get_high(self, i):
        if self.frame.empty:
            return 0
        else:
            return self.frame.iloc[i].high

    def get_low(self, i):
        if self.frame.empty:
            return 0
        else:
            return self.frame.iloc[i].low

    def get_close(self, i):
        if self.frame.empty:
            return 0
        else:
            return self.frame.iloc[i].close

    def get_volume(self, i):
        if self.frame.empty:
            return 0
        else:
            return self.frame.iloc[i].volume

    def get_length(self):
        logging.info('length {}'.format(len(self.frame)))
        return len(self.frame)




