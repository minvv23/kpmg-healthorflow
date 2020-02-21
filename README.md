# KPMG Healthorflow
Team 'Healthorflow' development code for KPMG Ideation Challenge

## Team Members & Role
### Data Scraping
- 진승욱 (KAIST 경영공학 석사과정)
- 황유진 (KAIST 경영공학 석사과정)
### NLP & ML
- 강태영 (KAIST 경영공학 석사과정)
- 장준규 (KAIST 경영공학 석사과정)
### Chatbot Design
- 김윤재 (울산대 의학)
- 김진하 (서울대 의학)
### Web Dev.
- 장준규 (KAIST 경영공학 석사과정)

## Task Description
### 1. 데이터 수집(Data Scraping)
**데이터 수집 단계**에서는 환자들이 증상에 대해 자신의 언어로 직접 자유롭게 서술한 텍스트를 확보하고, 이를 증상명과 일대일로 대응(matching)시키는 것이 일차적인 목표입니다. 이를 위해 *(1)기침, (2)콧물, (3)복통, (4)변비, (5)설사, (6)흉통, (7)호흡곤란, (8)두근거림, (9)어지러움 (10)두통*의 10가지 증상에 대해 **네이버 지식iN** 의학 답변과 건강의학포털 **HiDOC** 두 곳의 웹사이트에서 데이터를 수집했습니다.  

검색 쿼리(query)로 '가슴이 두근', '가슴이 아파' / '두통', '어지러워', '머리가 아파' 등을 입력한 후 이에 대응되는 질문들의 텍스트 본문을 수집하는 형태로 데이터 수집이 진행되었습니다. 각 쿼리(query)에 대해 약 5,000개의 질의응답 데이터를 수집할 수 있었으며, 활용한 툴은 *BeautifulSoup*과 *Selenium*입니다. 수집 코드 및 결과 데이터는 *web_crawling* 폴더에서 확인할 수 있습니다.

### 3. 머신러닝을 활용한 분류모델 (Query Prediction Model with Machine Learning)

증상분류모델은 환자가 입력한 쿼리를 바꾼 임베딩 벡터를 주증상 10가지 중 하나로 multiclassify 하는 모델입니다.


증상분류 모델은 Base Model은 XGBoost 모델을 사용하였으며
Bayesian optimization을 통해 optimize 된 모델을 찾은 뒤 DNN Model과 앙상블을 하여 최종 모델을 선정했습니다.


주요 모델의 Accuracy는 다음과 같습니다.

Model                                     | F1-Score        |
----------------------------------------- | :-------------: | 
XGBoost                                   | 81.2%           | 
XGBoost with Bayesian Optimization        | 89.2%           | 
Ensembled ML Model with Optimized XGBoost | 92.4%           | 


