import psycopg2
import datetime
import logging
# STOCK MODEL
### stock_num: stock number and company name
# stock_num integer (primary key), comp_name varchar(50);

### stock_day: stock data of date
#  (num integer, date date, open float, high float, low float, close float, volumes integer);


def regist_statistics(num, datetime, open, high, low, close, volumes, label):
    get_data_query = 'SELECT count(*) FROM stock_statistics WHERE num=%(num)s AND datetime=%(datetime)s AND label=%(label)s '
    # insert_query ='INSERT INTO stock_day (num, date, open, high, low, close, volumes) VALUES (%(num)s, %(date)s, %(open)s, $(high)s, %(low)s, %(close)s, $(volumes)s)'
    insert_query ='INSERT INTO stock_statistics (num, datetime, open, high, low, close, volumes, label) ' \
                  'VALUES (%(num)s, %(datetime)s, %(open)s, %(high)s, %(low)s, %(close)s, %(volumes)s, %(label)s)'
    DATABASE_DIR = 'postgres://ryo:maryo1994@localhost/stockmodel'
    conn = psycopg2.connect(DATABASE_DIR)
    cur = conn.cursor()
    try:
        data_exist = cur.execute(get_data_query, {'num':num, 'datetime':datetime, 'label':label})
        if cur.fetchone()[0] == 0:
            logging.info("Registration is begin")
            print("Registration is begin")
            cur.execute(insert_query, {'num':num, 'datetime':datetime, 'open':open, 'high':high, 'low':low, 'close':close, 'volumes':volumes, 'label':label})
            conn.commit()
            logging.info("Registration is success")
        else:
            print('The Data has already registered  ' + str(datetime) + " " + str(label))
    except Exception as e:
        logging.critical('critical error {}'.format(e))
        cur.execute('ROLLBACK')
        conn.close()
        return False
    conn.close()
    return True

def get_stock_statistics(num, date_begin, date_end, label):
    get_data_query = 'SELECT * FROM stock_statistics WHERE num = %(num)s AND label = %(label)s AND datetime BETWEEN timestamp %(begin)s AND timestamp %(end)s ORDER BY datetime '
    DATABASE_DIR = 'postgres://ryo:maryo1994@localhost/stockmodel'
    conn = psycopg2.connect(DATABASE_DIR)
    cur = conn.cursor()
    date_begin = datetime.datetime(date_begin.year, date_begin.month, date_begin.day, 0, 0, 0)
    date_end = datetime.datetime(date_end.year, date_end.month, date_end.day, 0, 0, 0) + datetime.timedelta(days=1)
    try:
        cur.execute(get_data_query, {'num': num,'begin': date_begin, 'end': date_end, 'label': label})
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






