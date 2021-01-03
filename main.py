# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from myStock_handler.scrape import ScrapeStock
from myStock_handler.scrape_yahoo import Scrape_yahoo
from myStock_handler.stock_day_handler import regist_day, get_stock_day
from myStock_handler.stock_minute_handler import regist_minute, get_stock_minute
from myStock_handler.stock_statistic_handler import regist_statistics, get_stock_statistics
import datetime
import numpy as np
from my_utils.utils import movingAve
import os

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   register = False
   stock_num = 6502
   interval_minute = 5
   timelenght_month = 2
   scraype_branch = 2  ## 0 == minute, 1 == day, 2==statistics
   if register:

        if scraype_branch == 0:
            m_model = Scrape_yahoo(stock_num)
            m_model.getScrape_month(interval_minute, timelenght_month)
            low=m_model.get_low(10)
            for i in range(m_model.get_length()):
                is_success = regist_minute(stock_num, m_model.get_date(i),m_model.get_open(i),
                                               m_model.get_high(i),m_model.get_low(i),
                                               m_model.get_close(i), m_model.get_volume(i), interval_minute)
                print(str(i)+ ' th DB registration is ' +str(is_success))

        if scraype_branch == 1:
            s_model = ScrapeStock(stock_num)
            s_model.scraypeData()
            low=s_model.get_low(10)
            for i in range(s_model.get_length()):
                is_success = regist_day(stock_num, s_model.get_date(i),s_model.get_open(i),
                                               s_model.get_high(i),s_model.get_low(i),
                                               s_model.get_close(i), s_model.get_volume(i))
                print(str(i)+ ' th DB registration is ' + str(is_success))
        if scraype_branch == 2:
            s_model = ScrapeStock(stock_num)
            s_model.scraypeData()
            is_success, data = get_stock_day(stock_num, s_model.y0, s_model.y1)
            if is_success:
               print('Date range is ' + str(data[0][1]) + " to " + str(data[-1][1]))
               print('Data size is ' + str(len(data)))
               data_2 = np.array(data)
               data_np = np.zeros((len(data_2), len(data_2[0])-2))
               date = []
               for i in range(len(data_np)):
                   date.append(data_2[i][1])
                   for j in range(len(data_np[0])):
                       data_np[i, j] = data_2[i][j+2]
               print(data_np)
               data_ma200 = movingAve(data_np, 200)
               data_ma75 = movingAve(data_np, 75)
               data_ma50 = movingAve(data_np, 50)
               data_ma25 = movingAve(data_np, 25)
               print(data_ma200)
               label_ma200 = 'ma200'
               label_ma75 = 'ma75'
               label_ma50 = 'ma50'
               label_ma25 = 'ma25'
               for i in range(len(data_2)):
                   is_success = regist_statistics(stock_num, date[i], data_ma200[i,0],
                                              data_ma200[i,1], data_ma200[i,2],
                                              data_ma200[i,4], data_ma200[i,4], label_ma200)
                   is_success = regist_statistics(stock_num, date[i], data_ma75[i,0],
                                              data_ma75[i,1], data_ma75[i,2],
                                              data_ma75[i,4], data_ma75[i,4], label_ma75)
                   is_success = regist_statistics(stock_num, date[i], data_ma50[i,0],
                                              data_ma50[i,1], data_ma50[i,2],
                                              data_ma50[i,4], data_ma50[i,4], label_ma50)
                   is_success = regist_statistics(stock_num, date[i], data_ma25[i,0],
                                              data_ma25[i,1], data_ma25[i,2],
                                              data_ma25[i,4], data_ma25[i,4], label_ma25)

        # print(low)
   else:
       num=6502
       date_begin=datetime.date(2018, 1, 1)
       date_end=datetime.date(2020, 12, 30)
       interval_minute = 5
       scraype_branch = 2

       # filepath=str(num)+"_"+str(date_begin)+"to"+str(date_end)+".csv"
       filepath="/Users/ryo/Documents/StockData/"+str(num)+"_"+str(date_begin)+"to"+str(date_end)+".csv"
       filepath_minute="/Users/ryo/Documents/StockData_min"+str(interval_minute)+"/"+str(num)+"_"+str(date_begin)+"to"+str(date_end)+".csv"
       # filepath = "~/Documents/StockData/" + str(num) + "_" + str(date_begin) + "to" + str(date_end) + ".csv"

       if scraype_branch == 0:
           is_success, data = get_stock_minute(num, date_begin, date_end, interval_minute)
           # is_success = True
           # data=[[0,0],[0,0]]
           print('DB loading is ' + str(is_success))
           header = "stocknum date open high low close volume interval"
           if is_success:
               print('Date range is ' + str(data[0][1]) + " to " + str(data[-1][1]) )
               print('Data size is ' + str(len(data)))
               data_np = np.array(data)
               for i in range(len(data_np[:,1])):
                   data_np[i,1] = data_np[i,1].strftime('%Y-%m-%d %H:%M:%S')
               print('converted data array' + str(data_np))
               np.savetxt(filepath_minute, data_np,delimiter=",", fmt="%d, %s, %.5e, %.5e, %.5e, %.5e, %d, %d", header=header)

       if scraype_branch == 1:
           is_success, data = get_stock_day(num, date_begin, date_end)
           header = "stocknum date open high low close volume"
           if is_success:
               print('Date range is ' + str(data[0][0]) + " to " + str(data[-1][1]) )
               print('Data size is ' + str(len(data)))
               data_np = np.array(data)
               for i in range(len(data_np[:,1])):
                   data_np[i,1] = data_np[i,1].strftime('%Y-%m-%d')
               print('converted data array' + str(data_np))
               np.savetxt(filepath, data_np,delimiter=",", fmt="%d, %s, %.5e, %.5e, %.5e, %.5e, %d", header=header)

       if scraype_branch == 2:
           label_ma200 = 'ma200'
           label_ma75 = 'ma75'
           label_ma50 = 'ma50'
           label_ma25 = 'ma25'
           is_success, data200 = get_stock_statistics(num, date_begin, date_end, label_ma200)
           if not is_success:
               raise Exception
           is_success, data75 = get_stock_statistics(num, date_begin, date_end, label_ma75)
           if not is_success:
               raise Exception
           is_success, data50 = get_stock_statistics(num, date_begin, date_end, label_ma50)
           if not is_success:
               raise Exception
           is_success, data25 = get_stock_statistics(num, date_begin, date_end, label_ma25)
           header = "stocknum date open high low close volume label"
           if is_success:
               data_np = np.array(data200)
               filepath = "/Users/ryo/Documents/StockData/" + str(num) + "_" + str(date_begin) + "to" + str(
                   date_end) + "_" + str(label_ma200) + ".csv"
               for i in range(len(data_np[:, 1])):
                   data_np[i, 1] = data_np[i, 1].strftime('%Y-%m-%d')
               print('converted data array' + str(data_np))
               np.savetxt(filepath, data_np, delimiter=",", fmt="%d, %s, %.5e, %.5e, %.5e, %.5e, %d, %s", header=header)

               data_np = np.array(data75)
               filepath = "/Users/ryo/Documents/StockData/" + str(num) + "_" + str(date_begin) + "to" + str(
                   date_end) + "_" + str(label_ma75) + ".csv"
               for i in range(len(data_np[:, 1])):
                   data_np[i, 1] = data_np[i, 1].strftime('%Y-%m-%d')
               print('converted data array' + str(data_np))
               np.savetxt(filepath, data_np, delimiter=",", fmt="%d, %s, %.5e, %.5e, %.5e, %.5e, %d, %s", header=header)

               data_np = np.array(data50)
               filepath = "/Users/ryo/Documents/StockData/" + str(num) + "_" + str(date_begin) + "to" + str(
                   date_end) + "_" + str(label_ma50) + ".csv"
               for i in range(len(data_np[:, 1])):
                   data_np[i, 1] = data_np[i, 1].strftime('%Y-%m-%d')
               print('converted data array' + str(data_np))
               np.savetxt(filepath, data_np, delimiter=",", fmt="%d, %s, %.5e, %.5e, %.5e, %.5e, %d, %s", header=header)

               data_np = np.array(data25)
               filepath = "/Users/ryo/Documents/StockData/" + str(num) + "_" + str(date_begin) + "to" + str(
                   date_end) + "_" + str(label_ma25) + ".csv"
               for i in range(len(data_np[:, 1])):
                   data_np[i, 1] = data_np[i, 1].strftime('%Y-%m-%d')
               print('converted data array' + str(data_np))
               np.savetxt(filepath, data_np, delimiter=",", fmt="%d, %s, %.5e, %.5e, %.5e, %.5e, %d, %s", header=header)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
