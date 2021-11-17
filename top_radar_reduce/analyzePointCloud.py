import pandas as pd
from sklearn.cluster import DBSCAN
import seaborn as sns
import numpy as np
# import matplotlib.pyplot  as plt

model = DBSCAN(eps=1,min_samples=5)

def analyzePoint(pointCloud) :
    result = []
    data = pd.DataFrame({"x" : pointCloud[0, ], "y" : pointCloud[1, ], "z" : pointCloud[2, ]})
    
    predict = pd.DataFrame(model.fit_predict(data))
    predict.columns=['predict']
    
    predictData = pd.concat([data,predict],axis=1)
    
    i = 0
    while True :
        pointData = predictData[predictData['predict'] == i]
        if len(pointData) != 0 :
            pointX = np.mean(pointData["x"])
            pointY = np.mean(pointData["y"])
            if (pointX * pointY != 0) :
                result.append([pointX, pointY])
                isDanger = (2 * pointX + 3 * pointY - 30 >= 0)
                if (isDanger) :
                    print('danger')
                    # api 전송
                else :
                    print('safe')
            i += 1
        else :
            break
    
    return result