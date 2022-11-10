# Research-Stock-market-Data
🔍Research Stock market Data as undergraduate research student   
#### [안홍렬]()교수님 지도하에 교내 DSML 연구센터에서 학부연구생으로서 주가 데이터에 대한 연구를 진행.   
##### [1] 정인호, 이하늘, 김민주, 안홍렬. (2022). [_통합 종목 주가 예측을 위한 시계열 스케일러 비교._](https://drive.google.com/file/d/1M2y1nrhyQc2Ulz3_2QaNwhxR3Fg6P34E/view?usp=share_link) 한국정보과학회 학술발표논문집, 1961-1963. | 2022.05 ~ 07 

##### [2] 위 연구를 기반으로 [_제1회 KRX 금융 빅데이터 활용 아이디어 경진대회_](https://m.mk.co.kr/news/stock/10457335)에 참가하여 [우수상 수상](https://drive.google.com/file/d/114Nj8cKeec77VjsbCT45Z_uWgBCUlydq/view?usp=share_link)(3,000,000원) | 2022.07 ~ 09
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## 2022 한국정보과학회 학술 발표회에서 포스터 발표 진행 [[Poster]](https://drive.google.com/file/d/1ECQcIRsyXVPVwUN1oYDlzZc_-JFKrXqr/view?usp=share_link)[[code]](https://github.com/inhovation97/Research-Stock-market-Data/tree/main/code)   
> 2022.07.29    
> 데이터 속 잡음이 너무 많아 추론이 안되는 어려움.   
> 많은 조건들을 추가해가며 예측이 될 때까지 데이터 정제 시도.   

#### 어떤 기업의 10일간의 주가 정보를 통해 다음날 종가가 상승할지 하락할지 이진 분류를 하는 모델을 연구한다.   
![image](https://user-images.githubusercontent.com/59557720/164187413-4b6d85fd-45fc-41fe-8150-4f94947d479a.png)

#### 이 과정에서 기업마다 액면가가 전부 다르며 시계열적인 특성을 가진 점에 초점을 맞추어 4가지 방식의 스케일링 고안하여 이를 비교함.   
1. [데이터 수집과정](https://inhovation97.tistory.com/54)   
2. [EDA 과정](https://inhovation97.tistory.com/59) -> 코넥스 기업 존재를 발견하여 종목 코드 선정 방식을 다시 고려   
3. [4가지 스케일링을 정의하여 비교](https://inhovation97.tistory.com/60) -> 논문의 주제로 선정   
4. [모델링 과정에서 데이터 불균형 문제를 해소함](https://inhovation97.tistory.com/61)   

#### [[code]](https://github.com/inhovation97/Research-Stock-market-Data/tree/main/code)   




## <연구 초기 데이터 베이스 구축>   
> 2022.01.03 ~ 2022.02.28   
> 교수님이 주신 과제를 수행하면서 피드백을 받고 수정함.   

1. 서버PC를 이용하기 위한 리눅스 사용법을 익힘.   
2. 프로그래밍적 사고에 대한 피드백을 받고 과제를 수행함   
   -> "데이터 프레임의 사용을 최소한으로 변수명을 명확히하며 각 개체를 순차적으로 처리하는 간결하고 가독성 높은 코드를 지향"
3. 시간 복잡도를 줄이기위한 멀티 프로세싱을 이용.   
4. mysql을 통해 서버에 DB를 생성하여 데이터를 저장.
5. 본격적인 연구를 위한 기본적인 modeling   

+ sql을 이용하여 데이터베이스에 데이터를 올리는 방법을 경험.   
+ [멀티 프로세싱](2022-01-10_assignments_on_feedback.ipynb)을 이용하여, 5분 -> 10초로 시간 복잡도를 크게 줄이는 것을 경험.   
+ 해당 과정에서 [LSTM을 이용하여 주가 상승 여부를 예측](https://github.com/inhovation97/Research-Stock-market-Data/blob/main/stage1/2022-01-18_trying_lstm.ipynb)해보았지만 실패 
  -> 파이토치를 이용하여 시계열 모델 RNN 모델링을 경험, 데이터 퀄리티로 인해 전혀 수렴이 안되는 것을 경험.   
