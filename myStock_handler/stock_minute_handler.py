import psycopg2
import datetime
import logging
# STOCK MODEL
### stock_num: stock number and company name
# stock_num integer (primary key), comp_name varchar(50);

### stock_day: stock data of date
#  (num integer, date date, open float, high float, low float, close float, volumes integer);


def regist_minute(num, datetime, open, high, low, close, volumes, interval):
    get_data_query = 'SELECT count(*) FROM stock_minute WHERE num=%(num)s AND datetime=%(datetime)s AND time_interval=%(time_interval)s '
    # insert_query ='INSERT INTO stock_day (num, date, open, high, low, close, volumes) VALUES (%(num)s, %(date)s, %(open)s, $(high)s, %(low)s, %(close)s, $(volumes)s)'
    insert_query ='INSERT INTO stock_minute (num, datetime, open, high, low, close, volumes, time_interval) ' \
                  'VALUES (%(num)s, %(datetime)s, %(open)s, %(high)s, %(low)s, %(close)s, %(volumes)s, %(time_interval)s)'
    DATABASE_DIR = 'postgres://ryo:maryo1994@localhost/stockmodel'
    conn = psycopg2.connect(DATABASE_DIR)
    cur = conn.cursor()
    try:
        data_exist = cur.execute(get_data_query, {'num':num, 'datetime':datetime, 'time_interval':interval})
        if cur.fetchone()[0] == 0:
            logging.info("Registration is begin")
            print("Registration is begin")
            cur.execute(insert_query, {'num':num, 'datetime':datetime, 'open':open, 'high':high, 'low':low, 'close':close, 'volumes':volumes, 'time_interval':interval})
            conn.commit()
            logging.info("Registration is success")
        else:
            print('The Data has already registered  ' + str(datetime) + " " + str(interval))
    except Exception as e:
        logging.critical('critical error {}'.format(e))
        cur.execute('ROLLBACK')
        conn.close()
        return False
    conn.close()
    return True

def get_stock_minute(num, date_begin, date_end, interval):
    get_data_query = 'SELECT * FROM stock_minute WHERE num = %(num)s AND time_interval = %(interval)s AND datetime BETWEEN timestamp %(begin)s AND timestamp %(end)s ORDER BY datetime '
    DATABASE_DIR = 'postgres://ryo:maryo1994@localhost/stockmodel'
    conn = psycopg2.connect(DATABASE_DIR)
    cur = conn.cursor()
    date_begin = datetime.datetime(date_begin.year, date_begin.month, date_begin.day, 0, 0, 0)
    date_end = datetime.datetime(date_end.year, date_end.month, date_end.day, 0, 0, 0) + datetime.timedelta(days=1)
    try:
        cur.execute(get_data_query, {'num':num ,'begin':date_begin, 'end': date_end, 'interval': interval})
        print('query is success')
        counter = 0
        datalist = cur.fetchall()
        length = len(datalist)
        # data = [length, length]
        # for data in datalist:
        #     date[counter] = data[1]
        #     open[counter] = data[2]
        #     print(str(date[counter]) + " " + str(open[counter]))
        return True, datalist
    except Exception as e:
        logging.critical('CRITICAL {}'.format(e))






