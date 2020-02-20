#!/usr/bin/env python
# coding: utf-8

# In[5]:


from tree_maker import csv_to_jsontree


# In[6]:


def csv_to_json(x):
    return csv_to_jsontree('./tree_csv/'+x+'.csv')


# In[11]:


global answer_list

answer_list=[]

def chatbot(question_tree):
    
    for i in range(len(question_tree)):

        print(question_tree[i]['name'])
        possible_answer = []
        
        for j in range(len(question_tree[i]['children'])):
            possible_answer.append(question_tree[i]['children'][j]['name'])
        
        
        if possible_answer == ['주관식']:
            print('주관식으로 서술해 주십시오')
            answer = input('답 : ')
            print('\n') 
            answer_list.append([question_tree[i]['name'],answer])
            
            if question_tree[i]['children'][0]['children'][0]['name']=='<end>':
                continue
            else:
                chatbot(question_tree[i]['children'][0]['children'])

        else:
            print('객관식 번호를 입력 해 주십시오')
            for k in range(len(possible_answer)):
                print(k+1,".", possible_answer[k])
            while True:
                answer = input('답 : ')
                if answer.isnumeric():
                    break
        
                else:
                    print(answer,'는 숫자가 아닙니다')
                    continue
                break
            print('\n')       
        
            while not(int(answer) in range(1,len(possible_answer)+1)):
                print("'숫자를 정확히 입력 해 주십시오")
                print(question_tree[i]['name'])
                for k in range(len(possible_answer)):
                    print(k+1, possible_answer[k])
                answer = input('답 : ')
                print('\n')
            answer_list.append([question_tree[i]['name'],possible_answer[int(answer)-1]])
            if question_tree[i]['children'][possible_answer.index(possible_answer[int(answer)-1])]['children'][0]['name']=='<end>':
                continue
            else:
                chatbot(question_tree[i]['children'][possible_answer.index(possible_answer[int(answer)-1])]['children'])
                
def ask(question_tree,i=0):

        return(question_tree[i]['name'])
    
def possible_answer(question_tree,i=0):
    
        possible_answer = []
        
        for j in range(len(question_tree[i]['children'])):
            possible_answer.append(question_tree[i]['children'][j]['name'])
            
        return possible_answer


    
def final(question_tree):
    if question_tree[i]['children'][0]['children'][0]['name']=='<end>':
        return True
    else:
        return False
    


# In[12]:


