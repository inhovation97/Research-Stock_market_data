def imbalance_plot( trainX, trainY, testX, testY):
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.rcParams['font.family'] ='NanumSquareRound'
    
    fig = plt.figure(figsize=(14,6))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    axes = [ax1,ax2]
    for i,ax in enumerate(axes):
        
        if i == 0:
            data = pd.Series(trainY).value_counts()
            title = 'train_imbalance_pie_chart'
            xlabel = 'train 데이터 shape : {}'.format(trainX.shape)
            print('권장 scale_pos_weight :',(data[0]/data[1]))
        else:
            data = pd.Series(testY).value_counts()
            title = 'test_imbalance_pie_chart'
            xlabel = 'test 데이터 shape : {}'.format(testX.shape)

        labels = ['label 0', 'label 1']
        ax.pie( data, colors = ['steelblue', 'firebrick'],
                                                 startangle=90,
                                                 autopct = '%1.2f%%',
                                                 labels = labels, 
                                                 )
        ax.set_title(title,fontsize = 16)
        ax.set_ylabel('')
        ax.set_xlabel(xlabel, fontsize = 14)
    plt.tight_layout()
    plt.show()
        
    
####################################################################################################################    
    
def plot_roc_curve(trainY, testY, train_pred, test_pred, train_prob, test_prob):
    import matplotlib.pyplot as plt
    from sklearn.metrics import roc_curve, roc_auc_score, f1_score, f1_score, accuracy_score, recall_score, precision_score, confusion_matrix
    
    fpr, tpr, thresholds = roc_curve(testY, test_prob) # output 3개가 나오는데, 각 threshhold 마다의 fpr, tpr값 인듯
    
    train_f1 = f1_score(trainY, train_pred)
    test_f1 = f1_score(testY, test_pred)
    
    train_recall = recall_score(trainY, train_pred)
    test_recall = recall_score(testY, test_pred)
    
    train_pre = precision_score(trainY, train_pred)
    test_pre = precision_score(testY, test_pred)  
    
    train_acc = accuracy_score(trainY, train_pred)
    test_acc = accuracy_score(testY, test_pred)
    
    plt.plot(fpr, tpr, color='red', label='ROC')
    plt.plot([0, 1], [0, 1], color='green', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('test ROC : {}'.format(round(roc_auc_score(testY, test_prob),3)),fontsize=16)
    plt.legend()
    plt.show()
    print('train_f1 score: ',train_f1)
    print('test_f1 score: ',test_f1,'\n')
    
    print('train_recall score: ',train_recall)
    print('test_recall score: ',test_recall,'\n')

    print('train_pre score: ',train_pre)
    print('test_pre score: ',test_pre,'\n')
    
    print('train acc score: ',train_acc)
    print('test acc score: ',test_acc, '\n')
    
#################################################################################################################    
    
def confusion_matrix(testY, test_pred):
    TP, FP, TN, FN = 0, 0, 0, 0
    for (y,pred) in zip(testY, test_pred):
        if y == 1 and pred==1:
            TP+=1

        elif y==0 and pred==1:
            FP+=1

        elif y == 0 and pred==0:
            TN+=1
            
        elif y==1 and pred==0:
            FN+=1
    
    print('     y_true') 
    print('pred',[TP, FP],'\n    ',[FN,TN])
    
##################################################################################################################    
    
def plot_distribute(test_prob, test_change):
    import seaborn as sns
    import matplotlib.pyplot as plt
    import matplotlib
    import pandas as pd
    import numpy as np

    matplotlib.rcParams['font.family'] ='NanumSquareRound'

    distrib1 = []
    distrib2 = [] 
    distrib3 = [] 
    distrib4 = []
    distrib5 = []

    for prob, change in zip(test_prob, test_change):

        if prob >= 0.8:
            distrib1.append(change)

        elif 0.6 <= prob < 0.8:
            distrib2.append(change)

        elif 0.4 <= prob < 0.6:
            distrib3.append(change)

        elif 0.2 <= prob < 0.4:
            distrib4.append(change)

        elif prob < 0.2:
            distrib5.append(change)
            
        
    # 리스트 데이터를 series로 변환
    distrib_list = [distrib1, distrib2, distrib3, distrib4, distrib5]
    for i in range(5):
        distrib_list[i] = pd.Series(distrib_list[i])
        
    # 원래 데이터 플롯    
    fig = plt.figure(figsize=(16,10))
    sns.distplot(test_change)
    plt.axvline(test_change.mean(), color='r')
    plt.title('testY 전체 분포', fontsize=20)
    print('평균 값:', test_change.mean())
    
    label_lst = ['upper_0.8', '0.6 ~ 0.8', '0.4 ~ 0.6', '0.2 ~ 0.4', 'lower_0.2']
    # 5구간 종합 플롯
    plt.figure(figsize=(16,10))
    for i, label in enumerate(label_lst):
        sns.distplot(distrib_list[i], bins = 30, label = label)
    
    plt.axvline(0, color='black')    
    plt.title('머신 러닝이 예측한 확률 별 5구간 분포', fontsize=20)
    plt.legend()
    plt.show()
    
    # 개별 플롯
    for i, label in enumerate(label_lst):
        plt.figure(figsize=(16,30))
        plt.subplot(5, 1, i+1)
        
        sns.distplot(distrib_list[i], bins = 30, label = label)
        plt.axvline(distrib_list[i].mean(), color='r')
        plt.axvline(0, color='black')
        plt.title('{}구간 분포, 평균 : {}, 예측 개수 : {}'.format(label, round(distrib_list[i].mean(),3), len(distrib_list[i])), fontsize=15)
        plt.tight_layout()
    
    
    # 5구간 박스플롯
    f,box_ax = plt.subplots(1,1,figsize=(16,10),sharex=False)
        
    _= sns.boxplot(data=distrib_list, orient="h" ,ax= box_ax) 
    _=plt.axvline(test_change.mean(),color='r',linewidth=2)
    _=plt.yticks(range(5), label_lst)
    _=plt.xlabel("Change")
    _=plt.ylabel("prob")
    _=plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05))
    plt.show()
    
    
    # 0.8 이상 구간 불균형도 & 정밀도
    f, ax = plt.subplots(1,1,figsize=(12,6),sharex=False)
    
    data = (pd.Series(distrib1) >= 0.05).value_counts(ascending=True)
    print('0.8 이상 구간의 정밀도 :',(data[0]/len(distrib1)))
    title = 'predited_imbalance_pie_chart'
    labels = ['label 0', 'label 1']
    ax.pie( data, colors = ['steelblue','firebrick'],
                                             startangle=90,
                                             autopct = '%1.2f%%',
                                             labels = labels, 
                                             )
    ax.set_title(title,fontsize = 16)
    ax.set_ylabel('')
    ax.set_xlabel('0.8이상 구간 불균형도', fontsize = 14)
    plt.tight_layout()
    plt.show()
    return box_ax