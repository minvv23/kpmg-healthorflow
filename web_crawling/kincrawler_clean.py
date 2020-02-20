#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import requests, time, sqlite3, re, json, urllib, math, numpy as np, pandas as pd
from selenium import webdriver
from pandas import Series, DataFrame


# In[ ]:


def download(method, url, param = None, data = None, headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}, timeout = 1, maxretries = 3):

    try:        
        resp = requests.request(method, url, params = param, data = data, headers = headers)
        resp.raise_for_status()
    
    except requests.exceptions.HTTPError as e:
        if 500 <= e.response.status_code < 600 and maxretries > 0:
            print(maxretries)
#             print(e.response.status_code)
#             print(e.response.reason)
#             print('재시도')
            time.sleep(timeout)
            resp = download(method, url, headers, param, data, timeout, maxretries-1)
        else:
            print(e.response.status_code)
            print(e.response.reason)
            
    return resp


# In[ ]:


query = ["복통", "배가+아파", "변비", "설사", "기침", "콧물", "흉통", "가슴이+두근", "가슴이+아파", "열이+나", "두통", "어지러움", "어지러워"]


# In[ ]:


url = "https://kin.naver.com/search/list.nhn"
separator = " "
df = pd.DataFrame()

for i in range(0, len(query)):
    queue = list()
    resptype = list()
    #queuelen = list()
    
    param = {
        "query": query[i],
        "section" : "qna"
    }
    print(param)
    
    html = download("get", url, param = param)
    dom = BeautifulSoup(html.text, "lxml")
    
    pagenum = math.ceil(int(dom.select_one("span.number").text.split('/')[1][:-1].replace(',',''))/10)
    print(f'total page number : {pagenum}')
    
    for j in range(1, min(1001, pagenum+1)):
        param = {
            "query": query[i],
            "section" : "qna",
            "page" : j
        }
        html = download("get", url, param = param)
        dom = BeautifulSoup(html.text, "lxml")
        
        resplist = [_ for _ in dom.select("dt")]
        #len(resplist)

        linkList = [_.find("a")["href"] for _ in resplist]
        
        if linkList[0] in queue:
            break
        
        for link in linkList:
            queue.append(link)
        
        [_.find("img") for _ in resplist]
        [resptype.append(int(1)) if _.find("img") != None else resptype.append(int(0)) for _ in resplist]
           
        if j % 100 == 0:
            print(f'pagenum : {j}, {round((j/min(1000, pagenum)*100))}% done')
            
    qname = list()
    qcontent = list()
    acontent = list()

    for index, baseURL in enumerate(queue):
        if index % 50 == 0:
            print(f'{index}/{len(queue)}, {round(index/len(queue)*100)}% done')
        html = download("get", baseURL)
        dom = BeautifulSoup(html.text, "lxml")

        qname.append(str.strip(dom.select_one("div.title").text))

        qcontent1 = dom.select_one("div.c-heading__content")
        if qcontent1 != None:
            qcontent1 = qcontent1.text
            qcontent1 = qcontent1.replace(u'\xa0', u' ')
            qcontent1 = qcontent1.replace(u'\u200b', u' ')
            qcontent1 = qcontent1.replace(u'\n', u' ')
            qcontent1 = qcontent1.replace(u'\t', u' ')
            qcontent1 = qcontent1.replace(u'\u0311', u' ')
            qcontent1 = qcontent1.replace(u'\u0308', u' ')
            qcontent1 = qcontent1.strip()
            qcontent.append(qcontent1)
        else:
            qcontent.append(np.nan)

        acontent1 = separator.join([_.text for _ in dom.select("p.se-text-paragraph.se-text-paragraph-align-")])
        if acontent1 == "":
            acontent1 = dom.select_one("div._endContents.c-heading-answer__content").text
        acontent1 = acontent1.replace(u'\xa0', ' ')
        acontent1 = acontent1.replace(u'\u200b', ' ')
        acontent1 = acontent1.replace(u'\n', ' ')
        acontent1 = acontent1.replace(u'\t', ' ')
        acontent1 = acontent1.replace(u'\u0311', ' ')
        acontent1 = acontent1.replace(u'\u0308', ' ')
        acontent1 = acontent1.strip()
        acontent.append(acontent1)
        
        time.sleep(1)
        
    time.sleep(120)
        
    data = {'query': query[i],
        'address' : queue,
        'resptype' : resptype,
        'qname': qname,
        'qcontent': qcontent,
        'acontent' : acontent
    }
        
    print(len(queue))
    print(len(resptype))
    print(len(qname))
    print(len(qcontent))
    print(len(acontent))

    df1 = pd.DataFrame(data)
    df = df.append(df1, ignore_index=True)
    
    df.to_csv('jisikin_Q&A.csv', encoding = "utf-8")

df.index += 1
df


# In[ ]:




