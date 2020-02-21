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
### 1. Data Scraping
**데이터 수집 단계**에서는 환자들이 증상에 대해 자신의 언어로 직접 자유롭게 서술한 텍스트를 확보하고, 이를 증상명과 일대일로 대응(matching)시키는 것이 일차적인 목표입니다. 이를 위해 (1)기침, (2)콧물, (3)복통, (4)변비, (5)설사, (6)흉통, (7)호흡곤란, (8)두근거림, (9)어지러움 (10)두통의 10가지 증상에 대해 <u>네이버 지식iN 의학 답변</u>과 <u>건강의학포털 'HiDOC'</u> 두 곳의 웹사이트에서 데이터를 수집했습니다.

free-text로 질문한 내용과 이에 해당하는 주증상을 labeling 하고자 하였습니다. 따라서 10가지 증상별로 각각 query 검색을 한 후, 검색 결과로 나오는 질문들을 해당 query의 학습 내용으로 사용하였습니다.

10가지 query는 ‘가슴이 두근’, ‘가슴이 아파 / 흉통’, ‘기침’, ‘두통’, ‘배가 아파 / 복통’, ‘변비’, ‘설사’, ‘어지러워’, ‘열이 나’, ‘콧물’입니다. 하나의 질문에 관한 내용은 ‘주요증상’, ‘웹 주소’, ‘질문 제목’, ‘질문내용’, ‘답변내용’으로 정리했습니다.  

query로 검색을 했을 때 한 페이지당 20개의 질문이 등록되어 있었고 query마다 등록된 질문 개수에 차이가 있었기 때문에 총 페이지 수는 상이했습니다. 하지만 등록된 질문 개수가 많더라도 대략 250페이지 이후로 등록된 질문의 내용은 query와 관련이 없는 내용이 많이 포함되었다고 판단하여 웹으로부터 크롤링할 최대 페이지 수는 최대 250으로 한정했습니다. 따라서 10가지 query에 대한 질문 수는 대략 각각 5000개씩 얻을 수 있었습니다. hidoc_로 시작하는 csv파일이 각 query별로 질문과 답변을 정리한 내용입니다. 

### Classify Model 

증상분류모델은 환자가 입력한 쿼리를 바꾼 임베딩 벡터를 주증상 9개중 하나로 multiclassify 하는 모델입니다.


증상분류 모델은 Base Model은 XGBoost 모델을 사용하였으며
Bayesian optimization을 통해 optimize 된 모델을 찾은 뒤 DNN Model과 앙상블을 하여 최종 모델을 선정했습니다.


주요 모델의 Accuracy는 다음과 같습니다.

Model                                    | Accuracy        |
---------------------------------------- | :-------------: | 
xgboost                                  | 81.2            | 
xgboost using Bayesian optimize          | 89.2            | 
optimize xgboost and ensemble            | 92.4            | 


