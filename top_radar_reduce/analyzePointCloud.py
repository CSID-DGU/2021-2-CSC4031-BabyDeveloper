import pandas as pd
from sklearn.cluster import DBSCAN
import numpy as np
import requests
# import matplotlib.pyplot  as plt


modelLen, modelCount = 1.7, 15 # 집단화 할 최대 거리, 최소 점 갯수
dataSnr = 100 # 모델링에 사용할 포인트의 최소 snr값
cycle = 20 # 몇 프레임마다 request를 보낼지 나타내는 값

model = DBSCAN(eps=modelLen, min_samples=modelCount)

def analyzePoint(pointCloud, index) :
    result = []
    isDanger = False
    data = pd.DataFrame(pointCloud, columns = ["x", "y", "z", "doppler", "snr"])
    
    # data = data.dropna()
    data = data[data["snr"] >= dataSnr]
    
    if (len(data) > 0) :
        predict = pd.DataFrame(model.fit_predict(data))
        predict.columns=['predict']
        
        predictData = pd.concat([data,predict],axis=1)
        predictData = predictData.dropna() # NAN 제거
        
        print(len(predictData))
        i = 0
        while True :
            print("testtest")
            print(i)
            pointData = predictData[predictData['predict'] == i]
            print(len(pointData))
            if len(pointData) != 0 :
                pointX, pointY, pointZ = np.mean(pointData["x"]), np.mean(pointData["y"]), np.mean(pointData["z"])
                if (pointX * pointY * pointZ != 0) :
                    result.append([pointX, pointY, pointZ])
                    if (not isDanger) :
                        isDanger = (2 * pointX + 22 * pointY - 7 * pointZ + 66 >= 0)
                    
                i += 1
            else :
                if (index % cycle == 0) :
                    if (i == 0) :
                        requests.get('http://52.79.198.17:5000/notify_condition/noPerson')
                    elif (isDanger) :
                        requests.get('http://52.79.198.17:5000/notify_condition/danger')
                    else :
                        requests.get('http://52.79.198.17:5000/notify_condition/safe')
                break
    
    return result