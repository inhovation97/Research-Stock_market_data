####################################### load_data 함수는 fold와 스케일링을 정하여 전처리가 완료된 학습을 위한 데이터를 리턴합니다.

####################################### train 함수는 불러온 데이터로 모델을 학습시키고 추론하여 결과값을 리턴합니다.


def load_data(fold, scaling):
    
    import scaling1
    import scaling2
    import scaling3
    import scaling4
    
    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    import warnings
    from utils import imbalance_plot, plot_roc_curve, confusion_matrix, plot_distribute
    
    warnings.filterwarnings('ignore')
    
    if scaling == 1:
        train = scaling1.load_data_using_multi_process(fold = fold, mode='train')
        test = scaling1.load_data_using_multi_process(fold = fold, mode='test')
        
    elif scaling == 2:
        train = scaling2.load_data_using_multi_process(fold = fold, mode='train')
        test = scaling2.load_data_using_multi_process(fold = fold, mode='test')    
        
    elif scaling == 3:
        train = scaling3.load_data_using_multi_process(fold = fold, mode='train')
        test = scaling3.load_data_using_multi_process(fold = fold, mode='test')
        
    elif scaling == 4:
        train = scaling4.load_data_using_multi_process(fold = fold, mode='train')
        test = scaling4.load_data_using_multi_process(fold = fold, mode='test')
        
        
    trainX=[]
    trainY=[]
    
    train_change=[]
    test_change=[]
    
    for row in train:
        if len(row[2:-1]) == 550:
            trainX.append(row[2:-1])
            trainY.append(int(row[-1] >= 0.05))
            train_change.append(row[-1])
    
    testX=[]
    testY=[]
    date_code_lst =  []
    for row in test:
        if len(row[2:-1]) == 550:
            date_code_lst.append(row[0:2])
            testX.append(row[2:-1])
            testY.append(int(row[-1] >= 0.05))
            test_change.append(row[-1])
        
    train_change = np.array(train_change)
    test_change = np.array(test_change)
    
    trainX = np.array(trainX)
    trainY = np.array(trainY)
    
    testX = np.array(testX)
    testY = np.array(testY)
    
    print(trainX.shape, testX.shape)
    imbalance_plot(trainX, trainY, testX , testY)
    print('{}번째 fold의 {}번 스케일링 데이터가 준비되었습니다.'.format(fold, scaling))
    
    return trainX, trainY, testX , testY, train_change, test_change, date_code_lst 





def train_model_and_inference(fold, trainX, trainY, testX, testY):
    from model import model
    from utils import imbalance_plot, plot_roc_curve, confusion_matrix, plot_distribute
    import os
    import time
    import numpy as np
    import pandas as pd
    start_time = time.time()
    
    model = model(fold)
    trained_model = model.fit( trainX,trainY,
              eval_set=[(testX,testY)],
              early_stopping_rounds = 25,
              verbose = 5,
              eval_metric = 'auc')
    
    train_pred = trained_model.predict(trainX)
    train_prob = trained_model.predict_proba(trainX)[:, 1]
    
    test_pred = trained_model.predict(testX)
    test_prob = trained_model.predict_proba(testX)[:, 1]
    
    plot_roc_curve(trainY, testY, train_pred, test_pred, train_prob, test_prob)
    confusion_matrix(testY, test_pred)
    print("---%s seconds ---" % (time.time() - start_time))
    
    return train_pred, train_prob, test_pred , test_prob























