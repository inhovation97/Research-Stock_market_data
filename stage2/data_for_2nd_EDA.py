def make_stock_data(code):
    
    import os
    import time
    import pandas as pd
    import numpy as np
    import datetime
    import pymysql
    from sqlalchemy import create_engine
    import FinanceDataReader as fdr
    from tqdm import tqdm
            
#sql을 위해 데이터 베이스 정보 변수 생성

    db_dsml = pymysql.connect(
#     host = 'localhost', 
    host = 'localhost', 
    port = 3306, 
    user = 'stock_user', 
    passwd = 'bigdata', 
    db = 'stock', 
    charset = 'utf8'
    )

    cursor = db_dsml.cursor()
    
# 딕셔너리를 이용하여 데이터 생성

    sql_query = '''
                SELECT *
                FROM stock_{}
                WHERE Date
                BETWEEN '2017-01-01' AND '2020-12-31'
                '''.format(code)
    stock = pd.read_sql(sql = sql_query, con = db_dsml)

    new_stock_lst = []    
    if stock.shape[0] == 981: # nan값 있는 기업 방지

        lst_stock = stock.values.tolist()

        # feature engineering
        ma_5 = stock['Close'].rolling(window=5).mean()
        ma_20 = stock['Close'].rolling(window=20).mean()
        ma_60 = stock['Close'].rolling(window=60).mean()
        ma_120 = stock['Close'].rolling(window=120).mean()
        min_vol = stock['Volume'].min()
        max_vol = stock['Volume'].max()
        shifting_Change = stock['Change'].shift(-1)

        for row, ma_5, ma_20, ma_60, ma_120, shifting_Change in zip(lst_stock, ma_5, ma_20, ma_60, ma_120, shifting_Change):
            Date, Open, High, Low, Close, Volume, Change = row
            Date = pd.to_datetime(Date)
            trading_value = Volume * Close
            Scaled_vol = (Volume - min_vol)/(max_vol-stock['Volume'].min())

            if Date < pd.to_datetime('2018-01-01') or Date >= pd.to_datetime('2020-12-29'): # 18년 데이터부터 생성, nan값 제거
                continue

            if Volume == 0 or abs(Change) > 0.3 : # 거래정지일 & 이상치는 제거함.
                continue

            else:
                new_stock_lst.append([Date, code, Open, High, Low, Close, Change, Volume, Scaled_vol, trading_value, ma_5, ma_20, ma_60, ma_120, shifting_Change])

        return new_stock_lst
    
    else:
        return None
    
    
    

def make_stock_data_multi(processes):
    
    import time, os
    from multiprocessing import Pool
    import multiprocessing
    import itertools
    
    start_time=time.time()

    IF = open('code_list.txt', 'r')
    code_list=[]
    for row in IF:
        row = row.split('\n')
        code_list.append(row[0])
    IF.close()
    
    # 모듈로 만들어주었으므로 if __name__ == '__main__':은 빼야함 (모듈을 쓰지 않고 건넛다리 없이 함수를 그냥 쓸 때 넣음.)
    pool = multiprocessing.Pool(processes=processes)
    stock_data_lst = pool.map( make_stock_data, code_list) # -> 이렇게하면 이중 리스트가 되므로 풀어줘야 함
    pool.close()
    pool.join()
    
    result=[]
    # 기업별로 리스트화 되어있으므로 그냥 쭉 기업 관계없이 스택해주는 작업
    for row in stock_data_lst:
        for row2 in row:
            result.append(row2)


    print("---%s seconds ---" % (time.time() - start_time))
    
    return result