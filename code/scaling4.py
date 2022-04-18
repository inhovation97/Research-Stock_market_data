########################################### 전날 종가로 나누기 컬럼 별 비독립

def perform_scaling(code, fold, mode):
    
    import os
    import time
    import pandas as pd
    import numpy as np
    import datetime
    import FinanceDataReader as fdr
    from tqdm import tqdm  
    from load_data import adding_information
    import warnings
    warnings.filterwarnings('ignore')
    
    sequence = 10 # 10일치의 데이터
    tr_value = 1000000000 # 10억 기준

# 첫 번째 fold
    if (fold == 1) & (mode == 'train'):
        start = pd.to_datetime('2011-01-01') # 원래는 2013 01 01로 1년치 땡겨서 14~16 train
        end = pd.to_datetime('2015-12-31') 
    elif (fold == 1) & (mode == 'test'):
        start = pd.to_datetime('2015-01-01') # 원래는 2016 01 01로 1년치 땡겨서 17 test
        end = pd.to_datetime('2017-12-31')

# 두 번째 fold
    elif (fold == 2) & (mode == 'train'):
        start = pd.to_datetime('2017-01-01')
        end = pd.to_datetime('2020-12-31')
    elif (fold == 2) & (mode == 'test'):
        start = pd.to_datetime('2020-01-01')
        end = pd.to_datetime('2021-12-31')
        
    stock = adding_information(code, start, end)
# 전처리에 필요한 정보 리스트 생성
    change_lst = stock['Change']
    date_lst = stock['Date']
    label_lst = stock['next_change']

# 데이터 프레임 정렬 ( 스케일링 필요한 24개앞으로 )
    stock = stock[['Open', 'High', 'Low', 'Close', 'ma_5', 'ma_20', 'ma_60', 'ma_120', 
                   'VMAP', 'BHB', 'BLB', 'KCH', 'KCL', 'KCM', 'DCH', 'DCL', 'DCM',
                   'SMA', 'EMA', 'WMA', 'Ichimoku', 'Parabolic SAR', 'KAMA','MACD',
                   'Volume','trading_value',
                   'MFI', 'ADI', 'OBV',
                   'CMF', 'FI', 'EOM, EMV', 'VPT', 'NVI', 'ATR', 'UI',
                   'ADX', '-VI', '+VI', 'TRIX', 'MI', 'CCI', 'DPO', 'KST',
                   'STC', 'RSI', 'SRSI', 'TSI', 'UO', 'SR',
                   'WR', 'AO', 'ROC', 'PPO', 'PVO']]    
    stock_lst = stock.values.tolist()    
    scaled_stock_lst=[]
# 스케일링 과정
    for i, (stock_row, date) in enumerate(zip(stock_lst, date_lst)):
        
        volume = stock_row[24]
        if date <= start + pd.DateOffset(months=11) or volume == 0: # 거래정지일 드롭 & 1년치 땡겨서 불렀으므로 1년 이후 데이터만 취급
            # 행 개수 맞춰줌 (반드시 필요)
            del date_lst[i]
            del label_lst[i]
            del change_lst[i]
            continue
            
        scaled_inform=[]
        non_scaled_inform=stock_row[24:]
        prev_close = stock_lst[i-1][3]
        for value in stock_row[:24]:
            scaled_inform.append( (value/prev_close) - 1 )
        
        scaled_inform += non_scaled_inform
        scaled_stock_lst.append(scaled_inform)
    
    merging_data=[]    
# 10일치 stack 과정
    for ii, (row, date, label, change) in enumerate(zip(scaled_stock_lst, date_lst, label_lst, change_lst)):

        if date <= start + pd.DateOffset(years=1) or np.isnan(label): # 드롭 조건
            continue
        
        trading_value = row[25]      
        
        # 10억 이상 and 5% 이상 변동
        if (trading_value >= tr_value) and (abs(change) >= 0.05) :
            data_10days = scaled_stock_lst[ii - sequence+1 : ii+1]
            
            # 10 days 스케일링
            merge = [date, code]
            for row2 in data_10days:
                merge += list(row2)
            
            merge += [label]
            merging_data.append(merge)
           
    return merging_data
    
    
    
    
    

def load_data_using_multi_process(fold, mode):
    
    import time, os
    from multiprocessing import Pool
    import multiprocessing
    import itertools
    
    start_time=time.time()
    processes=30
    
    if fold == 1 :
        file_name = 'code_list_fold1.txt'
    elif fold == 2:
        file_name = 'code_list_fold2.txt'
    else:
        raise ValueError

# 멀티프로세싱 argument 생성
    IF = open(file_name, 'r')
    args_list=[]
    for i,row in enumerate(IF):
        code = row.split('\n')[0]
        args_list.append([code, fold, mode])
    IF.close()
    
    result = []
# 멀티프로세싱 진행
    pool = multiprocessing.Pool(processes = processes)
    for data in pool.starmap( perform_scaling, args_list ): # 각 코어에 입력값들을 병렬 처리
        result+=data
    pool.close() # 멀티 프로세싱 종료
    pool.join()


    print("--- %s seconds ---" % (time.time() - start_time))
    return result


