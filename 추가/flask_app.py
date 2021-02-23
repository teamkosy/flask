from flask import Flask, render_template
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
import pandas as pd
import random

app = Flask(__name__)

#index 화면
@app.route('/')
def index():
    return render_template('/index.html')


@app.route('/ml')
def ml():
    return render_template('/ml.html')


@app.route('/mlOk')
def mlOk():
    tbl = pd.read_csv('train_car2.csv', encoding='euc-kr')

    label = tbl['label']
    a = tbl['region']
    b = tbl['speed'] / 200
    c = tbl['situation'] / 8
    abc = pd.concat([a, b, c], axis=1)

    data_train, data_test, label_train, label_test = \
        train_test_split(abc, label)

    clf = svm.SVC()
    clf.fit(data_train, label_train)

    predict = clf.predict(data_test)

    ac_score = metrics.accuracy_score(label_test, predict)
    cl_report = metrics.classification_report(label_test, predict)

    ac_score = ac_score *100

    return render_template('/index.html',ac_score=ac_score, cl_report=cl_report)

@app.route('/ranOk1')
def ranOk1():
    tbl = pd.read_csv("random2.csv", encoding='utf-8')
    tbl=pd.DataFrame(tbl)

    del tbl['Unnamed: 0']

    tbl.rename(columns = {'0' : '지역','1' : '속도','2' :'상황','3' : '행동'}, inplace = True)

    tbl=tbl.replace('일반',1)
    tbl=tbl.replace('고속도로',2)
    tbl=tbl.replace('어린이보호구역',3)
    tbl=tbl.replace('직선도로',1)
    tbl=tbl.replace('좌코너',2)
    tbl=tbl.replace('우코너',3)
    tbl=tbl.replace('차선변경',4)
    tbl=tbl.replace('장애물',5)
    tbl=tbl.replace('신호정지',6)
    tbl=tbl.replace('신호시작',7)
    tbl=tbl.replace('유턴',8)

    tbl=tbl.astype({'지역':int,'속도':int,'상황':int})

    label=tbl['행동']
    a=tbl['지역']
    b=tbl['속도']/200
    c=tbl['상황']/8
    abc=pd.concat([a,b,c],axis=1)

    data_train, data_test, label_train, label_test = \
        train_test_split(abc, label)

    clf = svm.SVC()
    clf.fit(data_train, label_train)

    predict = clf.predict(data_test)

    ac_score1 = metrics.accuracy_score(label_test, predict)
    cl_report1 = metrics.classification_report(label_test, predict)

    score1 = ac_score1 * 100

    return render_template('/index.html', score1=score1, cl_report1=cl_report1)

def driving(a, b, c):
    if a == '일반' and b <= 80 and c == '직선도로': return '이동'
    if a == '일반' and b > 80 and c == '직선도로': return '속도 80 이하로 내린 후 이동'
    if a == '일반' and b <= 30 and c == '좌코너': return '좌회전'
    if a == '일반' and b > 30 and c == '좌코너': return '속도 30 이하로 내린 후 이동'
    if a == '일반' and b <= 30 and c == '우코너': return '우회전'
    if a == '일반' and b > 30 and c == '우코너': return '속도 30 이하로 내린 후 우회전'
    if a == '일반' and b <= 80 and c == '차선변경': return '변경'
    if a == '일반' and b > 80 and c == '차선변경': return '속도 80이하로 내린 후 변경'
    if a == '일반' and b <= 30 and c == '장애물': return '정지'
    if a == '일반' and 30 < b and c == '장애물': return '급정거'
    if a == '일반' and b <= 30 and c == '신호정지': return '정지'
    if a == '일반' and 30 < b and c == '신호정지': return '급정거'
    if a == '일반' and b <= 200 and c == '신호시작': return '이동'
    if a == '일반' and b <= 30 and c == '유턴': return '유턴하기'
    if a == '일반' and 30 < b <= 200 and c == '유턴': return '속도 30 이하로 내린 후 유턴'

    if a == '어린이보호구역' and b <= 30 and c == '직선도로': return '이동'
    if a == '어린이보호구역' and b > 30 and c == '직선도로': return '속도 30 이하로 내린 후 이동'
    if a == '어린이보호구역' and b <= 30 and c == '좌코너': return '좌회전'
    if a == '어린이보호구역' and b > 30 and c == '좌코너': return '속도 30 이하로 내린 후 좌회전'
    if a == '어린이보호구역' and b <= 30 and c == '우코너': return '우회전'
    if a == '어린이보호구역' and b > 30 and c == '우코너': return '속도 30 이하로 내린 후 우회전'
    if a == '어린이보호구역' and b <= 30 and c == '차선변경': return '변경'
    if a == '어린이보호구역' and b > 30 and c == '차선변경': return '속도 30 이하로 내린 후 변경'
    if a == '어린이보호구역' and b <= 30 and c == '장애물': return '정지'
    if a == '어린이보호구역' and 30 < b and c == '장애물': return '급정거'
    if a == '어린이보호구역' and b <= 30 and c == '신호정지': return '정지'
    if a == '어린이보호구역' and 30 < b and c == '신호정지': return '급정거'
    if a == '어린이보호구역' and b <= 200 and c == '신호시작': return '이동'
    if a == '어린이보호구역' and b <= 30 and c == '유턴': return '유턴하기'
    if a == '어린이보호구역' and 30 < b <= 200 and c == '유턴': return '속도 30 이하로 내린 후 유턴'

    if a == '고속도로' and b <= 200 and c == '직선도로': return '이동'
    if a == '고속도로' and b <= 30 and c == '좌코너': return '좌회전'
    if a == '고속도로' and b > 30 and c == '좌코너': return '속도 30 이하로 내린 후 좌회전'
    if a == '고속도로' and b <= 30 and c == '우코너': return '우회전'
    if a == '고속도로' and b > 30 and c == '우코너': return '속도 30 이하로 내린 후 우회전'
    if a == '고속도로' and b <= 200 and c == '차선변경': return '변경'
    if a == '고속도로' and b <= 100 and c == '장애물': return '정지'
    if a == '고속도로' and b > 100 and c == '장애물': return '급정거'
    if a == '고속도로' and b <= 30 and c == '신호정지': return '정지'
    if a == '고속도로' and 30 < b and c == '신호정지': return '급정거'
    if a == '고속도로' and b <= 200 and c == '신호시작': return '이동'
    if a == '고속도로' and b <= 30 and c == '유턴': return '유턴하기'
    if a == '고속도로' and 30 < b <= 200 and c == '유턴': return '속도 30 이하로 내린 후 유턴'

@app.route('/ranOk2')
def ranOk2():
    #코스생성
    aaList=['일반','어린이보호구역']
    aaaList=['고속도로']
    ccList = ['직선도로','좌코너','우코너','차선변경','장애물','신호정지','신호시작','유턴']
    cccList = ['직선도로','좌코너','우코너','차선변경','장애물']
    aa=[]
    bb=[]
    cc=[]
    label1=[]
    for i in range(20000):
        q=random.choice(aaList)
        w=random.randint(0, 200)
        e=random.choice(ccList)
        r=random.choice(aaaList)
        t=random.choice(cccList)
        aa.append(q)
        aa.append(r)
        bb.append(w)
        cc.append(e)
        cc.append(t)
        label1.append(driving(q,w,e))
        label1.append(driving(r,w,t))

    course=[]
    course.append(aa)
    course.append(bb)
    course.append(cc)
    course.append(label1)

    course = [[element for element in t] for t in zip(*course)]

    course= pd.DataFrame(course)
    course.to_csv('course1.csv',header=True, encoding='utf-8')

    course1= pd.read_csv("course1.csv", encoding='utf-8')
    course1=pd.DataFrame(course1)

    del course1['Unnamed: 0']
    course1.rename(columns = {'0' : '지역','1' : '속도','2' :'상황','3' : '행동'}, inplace = True)

    course1=course1.replace('일반',1)
    course1=course1.replace('고속도로',2)
    course1=course1.replace('어린이보호구역',3)
    course1=course1.replace('직선도로',1)
    course1=course1.replace('좌코너',2)
    course1=course1.replace('우코너',3)
    course1=course1.replace('차선변경',4)
    course1=course1.replace('장애물',5)
    course1=course1.replace('신호정지',6)
    course1=course1.replace('신호시작',7)
    course1=course1.replace('유턴',8)

    label1=course1['행동']
    a1=course1['지역']
    b1=course1['속도']/200
    c1=course1['상황']/8
    abc1=pd.concat([a1,b1,c1],axis=1)

    data_train1, data_test1, label_train1, label_test1 = \
        train_test_split(abc1, label1)

    clf = svm.SVC()
    clf.fit(data_train1, label_train1)

    predict1 = clf.predict(data_test1)

    ac_score2 = metrics.accuracy_score(label_test1, predict1)
    cl_report2 = metrics.classification_report(label_test1, predict1)


    score2 = ac_score2* 100

    return render_template('/index.html', score2=score2, cl_report2=cl_report2)


#---------------------- machine learnig end---------------------------------------------


if __name__ == '__main__':
    app.debug = True
    app.run()