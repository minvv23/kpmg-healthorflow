
from flask import Flask,render_template,request
from query_interpreter import symptom_classifier
from chatbot import csv_to_json, ask ,possible_answer, final

import json
global length
global tree
global length
global mainanswer
global subtree
global t

t = int(0)
app = Flask(__name__)
length = '10'
mainanswer = int(0)
c =int(0)
print(mainanswer)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/main', methods=['POST'])
def post():
    global tree
    global length
    global mainanswer
    global subtree
    global t
    global c
    mainanswer=0
    t=0
    c=0
    value = request.form['mainSymptom']
    a=symptom_classifier(value)
    tree=csv_to_json(a)
    if a=='가슴문제':
        a='흉통/두근거림'
    if a =='열발생':
        a='발열'
    length=int(len(tree))
    leaf=ask(tree)
    answer=possible_answer(tree)
    subtree=tree
    a={'isEnded': False, 'text': leaf, 'answer': answer, 'symptom':a}
    leaf1= json.dumps(a)
    return leaf1

@app.route('/sub',methods=['POST'])
def post1():
    global tree
    global length
    global mainanswer
    global subtree
    global c
    global t
    value = request.form['description']
    if t==c:
        try:
            value=int(value)
            subtree=subtree[0]['children'][int(value)-1]['children']
            c= len(subtree)
            t=0
        except:
            subtree=subtree[0]['children'][0]['children']
            c= len(subtree)
            t=0        
    if subtree[t]['name'] == '<end>':

        if int(mainanswer)==int(length)-1:
            a={'isEnded': True, 'text':'<end>', 'answer': None}
            leaf1=json.dumps(a)
            return leaf1    
        mainanswer= mainanswer+1
        subtree=[tree[mainanswer]]
    
    asking=subtree[t]['name']

    poss=[]
    
    for j in range(len(subtree[t]['children'])):
        poss.append(subtree[t]['children'][j]['name'])
    t=t+1
    a={'isEnded': False, 'text':asking, 'answer':poss}
    leaf1=json.dumps(a)
  
    return leaf1

    
    
    
    
    
    
    

           
    
if __name__ == '__main__':
    app.run()



