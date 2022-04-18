def model( fold ) :

    from lightgbm import LGBMClassifier
    import os
    from utils import plot_roc_curve, confusion_matrix
    import pandas as pd
    import numpy as np
    
# 각 fold의 데이터 불균형도가 다름
    if fold == 1:
        scale_pos_weight = 6.8
    elif fold == 2:
        scale_pos_weight = 6.4
    
    
    
    params = {  'random_state' : 42,
                'scale_pos_weight' : scale_pos_weight,
                'learning_rate' : 0.1, 
                'num_iterations' : 1000,
                'max_depth' : 4,
                'n_jobs' : 30,
                'boost_from_average' : False,
                'objective' : 'binary' }
    
    model = LGBMClassifier( **params )
    print( '{}번째 fold를 위한 모델이 준비되었습니다.'.format(fold) )
    return model






