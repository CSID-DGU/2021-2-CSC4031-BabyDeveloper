#  레이더 센서를 활용한 옥상 안전 케어 서비스


Texas Instrument 의 60GHz 레이더 센서를 활용하여 클라우드 포인트 데이터를 수집한 후, 실시간으로 데이터를 정제한다. 정제한 데이터를 통해 사람이 있는 경우를 판별하고, 사람이 옥상 난간 등 위험지역에 있는 경우 api를 전송하여 앱에서 확인할 수 있는 시스템을 구축한다. 

##시스템 구성도
![image](https://user-images.githubusercontent.com/70522531/143551493-68ef2fff-9750-4c51-a8cf-a66be708bad0.png)

## 시연 절차

1. 동국대학교 중앙도서관 난간 근처에 레이서 센서를 설치한다. 

2. 관련 Python 모듈을 설치한 후, top_radar_reduce/gui_main.py 를 실행한다.

```

pip install pyqt5
pip install pyqtgraph
pip install numpy
pip install pandas
pip install sklearn

```

3. 연결 포트와 configuration file(people_detection_and_tracking_50m_3D.cfg)을 확인 후, 연결을 시도하면 클라우드 포인트를 확인할 수 있다.

4. 위험상황을 알리는 역할을 하는 flask로 빌드한 서버를 실행한다. 

5. 앱을 실행하여 옥상에 위험상황이 발생하는지 확인한다. 
  

## 노이즈 제거 알고리즘

*  n개의 프레임 합치기 
	+ 한 프레임이 변할때마다 산발적으로 분포하는 노이즈 포인트가 발생
	+ 사람의 경우, 비교적 프레임마다 비슷한 위치에 점이 찍히는 포인트를 이용하여, 여러 프레임의 점을 합쳐서 분석
	+  노이즈는 프레임을 합쳐도 비슷한 분포를 보이지만, 사람의 경우 더 많은 포인트가 찍히는 결과를 도출, 아래 dbscan 알고리즘을 적용하기에 유리함

*  dbscan 을 통한 그룹화
	+ dbscan은 점 사이의 거리와 그룹 점 최소 개수를 통해 점을 그룹화하는 알고리즘
	+ 다른 그룹화 알고리즘보다 빠른 수행시간을 갖고 있어, 초당 약 10프레임의 좌표를 도출하는 레이더 센서 좌표의 그룹화에 적합

*  snr 활용
	+ 레이더 센서 데이터에 포함된 snr(신호 대 잡음비)을 활용하여 노이즈가 심한 좌표를 분석에서 제외하였다. 

*  Point_jupyter 에 있는 jupyter 파일과 test_data를 통해, 노이즈 제거 알고리즘들을 테스트해볼 수 있다.

  

## 위험 상황 알림 시스템


*   위험 상황을 전송하기 위해, Flask로 간단한 api를 작성하고, EC2에 업로드하였다. 

* gui_main.py에 위에 작성한 노이즈 제거 알고리즘을 적용하고, 그 결과를 api로 전송하는 코드를 작성한다.

* flutter 로 위험 상황을 받는 간단한 앱을 작성하였다.


## 유무선 레이더 센서 연결 방법


* 레이더센서 모듈에 따라 직접연결, WIFI연결이 가능한 모델이 있다. 프로젝트에 사용한 레이더 센서 모델의 경우, Indoor(감지 거리 ~ 9.8m) 모듈인 경우 WIFI 연결이 가능하고, 직접연결은 Indoor, Outdoor용 모두 가능하다.

* 사용하고 있는 레이더 센서 모델 Wifi 연결의 경우, 데이터 크기 문제로 1초마다  (x, y) 타겟 좌표값만을 얻을 수 있다. 프로젝트에서는 프레임마다 모든 포인트 클라우드 데이터를 얻을 수 있는 직접 연결을 선택하였다.

* 각 연결 방법은 top_radar_connect/(주)파워로직스_TSF-P100_연결메뉴얼.pptx 에 작성하였다.

  
## 참고한 자료


###  Texas Instrument PointCloud

[Industrial Toolbox 4.8.0](https://dev.ti.com/tirex/explore/node?node=AJoMGA2ID9pCPWEKPi16wg__VLyFKFf__LATEST)

### seunghwanly 님의 Texas Radar 연결 관련 자료

[mobius-docker repository](https://github.com/seunghwanly/mobius-docker)
