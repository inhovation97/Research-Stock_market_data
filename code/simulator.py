def simulator( date_code_lst, test_prob, fold ) :

    
    from load_data import adding_information
    import FinanceDataReader as fdr
    import pandas as pd
    import numpy as np

############################################################################################################ 주문 일지 코드
    order_dict = {}
    # order_df
    for row, y in zip(date_code_lst, test_prob) :
        date = row[0].strftime("%Y-%m-%d")
        code = row[1]

        if date not in order_dict.keys() and  y >= 0.8:
            order_dict[date] = [[code], "buy", 1.0]

        elif date in order_dict.keys() and y >= 0.8:
            order_dict[date][0].append(code)
            order_dict[date][2] = (1/len(order_dict[date][0]))

    order_dict = sorted(order_dict.items())

########################################################################################################### 시뮬레이터 코드
    
    start_money = 1000000 # 초기 현금 1천만원
    money = start_money

    if fold == 1:
        start = pd.to_datetime('2016-01-01') # 원래는 2013 01 01로 1년치 땡겨서 14~16 train
        end = pd.to_datetime('2018-01-05') 
    elif fold == 2:
        start = pd.to_datetime('2021-01-01') # 원래는 2013 01 01로 1년치 땡겨서 14~16 train
        end = pd.to_datetime('2022-01-05') 



    sell_change_lst =[]
    result=[]
    print('시작 금액 : {} 만원'.format(start_money/10000))
    for i, row in enumerate(order_dict): #주문 일지를 한 줄 읽어 옴
        buy_date = pd.to_datetime(row[0])
        code_lst = row[1][0]    
        buy_ratio = row[1][2] 

        sell_date_dict={} # 매도를 위한 딕셔너리
        no_subtract_money = money # 예측한 기업이 여러 개일 때 매수 금액을 계산하는 돈
        for code in code_lst:
            stock = fdr.DataReader(code, start, end).reset_index()
            stock_lst = stock.values.tolist()

            for ii,stock_row in enumerate(stock_lst):

                buy_stock_date = stock_row[0]
                buy_close_price = stock_row[4]


                sell_stock_date = stock_lst[ii+1][0]
                sell_close_price = stock_lst[ii+1][4]
                sell_change = stock_lst[ii+1][6]


                    # 예측한 기업이 1개일때
                if buy_date == buy_stock_date and sell_stock_date not in sell_date_dict.keys():
                # 매수    
                    buy_stock_count = int((money*buy_ratio)/buy_close_price)
                    money -= buy_stock_count*buy_close_price

                    sell_date_dict[sell_stock_date] = [[code, buy_stock_count, buy_close_price, sell_close_price, sell_change, ]]

                    print('\n{} : BUY {} -> {}주 구입, 매수 금액: {}만원'.format(
                                                      str(buy_date).split(" ")[0], 
                                                      code, 
                                                      buy_stock_count,
                                                      (buy_stock_count * buy_close_price)/10000)
                                                       )
                    break

                    # 예측한 기업이 2개 이상일때
                elif buy_date == buy_stock_date and sell_stock_date in sell_date_dict.keys():
                # 매수    
                    buy_stock_count = int((no_subtract_money * buy_ratio) / buy_close_price)
                    money -= buy_stock_count*buy_close_price

                    sell_date_dict[sell_stock_date].append([code, buy_stock_count, buy_close_price, sell_close_price, sell_change])

                    print('{} : BUY {} -> {}주 구입, 매수 금액: {}만원'.format(
                                                      str(buy_date).split(" ")[0], 
                                                      code, 
                                                      buy_stock_count,
                                                      (buy_stock_count * buy_close_price)/10000)
                                                       )
                    break

        for sell_stock in sell_date_dict[sell_stock_date]:
            sell_stock_code = sell_stock[0] # 팔아야 할 기업 코드
            buy_stock_count = sell_stock[1] # 매수 수량
            buy_close_price = sell_stock[2] # 매수 가격
            sell_close_price = sell_stock[3] # 매도 가격
            close_change = sell_stock[4] # 다음 날 d+1의 종가 변화량

        # 매도
            earnings = (buy_stock_count * sell_close_price) - (buy_stock_count * buy_close_price)
            money += (buy_stock_count * sell_close_price)
            print('{} : SELL {} -> 매도 금액 : {}만원, 전날 대비 상승률 {}:, 이익금 : {}만원, 현재 자산 : {:.2f}만원'.format(str(sell_stock_date).split(" ")[0],
                                                                                    sell_stock_code, 
                                                                                    (buy_stock_count * sell_close_price)/10000,                     
                                                                                    close_change,
                                                                                      (earnings/10000), 
                                                                                    (money/10000)))
            sell_change_lst.append(close_change)
        result.append([str(sell_stock_date).split(" ")[0], money])
    print('\n earning_rate :',100*(money/start_money))
    return result
