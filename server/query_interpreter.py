#!/usr/bin/env python
# coding: utf-8

# In[13]:


import re, os, glob, pickle, numpy as np, pandas as pd
from sklearn.externals import joblib
from itertools import chain
import hangul_jamosplit
import sentencepiece as spm
from IPython.display import clear_output
def split_text_cleaner(x) :
    return hangul_jamosplit.hangul_jamosplit(' '.join(re.compile(r'[^a-zA-Z0-9ㄱ-ㅣ가-힣.,-_?!~]+').sub(' ',str(x).lower()).split()), 'E')
def unsplit_text_cleaner(x) :
    return ' '.join(re.compile(r'[^a-zA-Z0-9ㄱ-ㅣ가-힣.,-_?!~]+').sub(' ',str(x).lower()).split())

# 띄어쓰기 패턴 학습 알고리즘
from soyspacing.countbase import RuleDict, CountSpace

# SentencePiece 형태소 추출용 학습 알고리즘
from WordPieceModel import wordpiecemodel 

# FastText 워드임베딩 알고리즘
from gensim.models import FastText

with open('hanbon_dict.p', 'rb') as f :
    hanbon_dict = pickle.load(f)

def hangul_to_kana_converter(x) :
    output = x
    for idx, each_output in enumerate(output) :
        for key, value in hanbon_dict.items() :
            output = output.replace(key, value)
    return output


def kana_to_hangul_converter(x) :
    output = x
    for idx, each_output in enumerate(output) :
        for key, value in hanbon_dict.items() :
            output = output.replace(value, key)
    return output

spacing_model = CountSpace()
spacing_model.load_model('healthnews_spacing_model', json_format=False)
sp = spm.SentencePieceProcessor()
sp.Load('healthcare_hanbon.model')
ftmodel = FastText.load('fasttext_healthqna.model')
def ft_dimension_retriever(x) :
    try :
        return ftmodel.wv[x]
    except :
        return np.repeat(0,200)
    
def final_meanvector_retriever(x) :
    return np.mean(ft_dimension_retriever([kana_to_hangul_converter(each) for each in sp.EncodeAsPieces(hangul_to_kana_converter(split_text_cleaner(spacing_model.correct(str(x))[0])))]), axis=0)

classifier = joblib.load('ensembled_classifier.pkl')

def symptom_classifier(x) :
    if '콜록' in str(x) :
        symptom = '기침'
    elif '쿨럭' in str(x) :
        symptom = '기침'
    elif '에취에취' in str(x) :
        symptom = '기침'
    elif '물똥' in str(x) :
        symptom = '설사'
    elif '뜨겁' in str(x) :
        symptom = '열발생'
    elif '뜨거' in str(x) :
        symptom = '열발생'
    else :
        symptom = classifier.predict(pd.DataFrame(final_meanvector_retriever(str(x))).T)[0]        
    return symptom


# In[14]:


symptom_classifier('머리가 너무 아파요')

