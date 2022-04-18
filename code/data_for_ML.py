def prepare_data(fold, mode):
    import scaling1
    import scaling2
    import scaling3
    import scaling4
    
    import pandas as pd
    import ipywidgets as widgets
    from ipywidgets import interact, interact_manual
    import cufflinks as cf
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    import warnings
    from utils import imbalance_plot, plot_roc_curve, confusion_matrix, plot_distribute
    warnings.filterwarnings('ignore')
    cf.go_offline(connected=True)
    
    
    train = scaling3.load_data_using_multi_process(fold = 1, mode='train', processes=40)
    test = scaling3.load_data_using_multi_process(fold = 1, mode='test', processes=40)
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
    test_date_code=[]
    for row in test:
        if len(row[2:-1]) == 550:
            test_date_code.append(row[:2])
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
    imbalance_plot(trainX, trainY, testX, testY)
    return trainX, trainY, testX, testY, train_change, test_change, test_date_code
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    