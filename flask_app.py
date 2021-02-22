from flask import Flask, render_template, request
import urllib
import urllib.request
import json
# import requests
# import matplotlib.pyplot as plt
# import matplotlib
# from matplotlib import font_manager
# import pymysql
#from flask.ext.mysql import MySQl

app = Flask(__name__)

# index 화면
@app.route('/')
def index():
    return render_template('/index.html')

# login
@app.route('/login')
def login():
    return render_template('/login.html')

#회원가입 화면
@app.route('/join')
def join():
    return render_template('/join.html')

#teamkosy
@app.route('/kosy')
def kosy():
    return render_template('/kosy.html')

#cal
@app.route('/cal')
def cal():
    return render_template('/cal.html')

#data
@app.route('/data')
def gwrite():
    return render_template('/data.html')

# data notebook
@app.route('/data_test')
def data():
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key=f9e46ed8e2b842376cd516c304c7fde2&targetDt=20201107'
    response = requests.get(url)
    data = response.json()

    r_list = []
    for i in range(0, 10):
        j = data['boxOfficeResult']['dailyBoxOfficeList'][i]['movieNm']
        r_list.append(j)

    open_list = []
    for i in range(0, 10):
        j = data['boxOfficeResult']['dailyBoxOfficeList'][i]['openDt']
        open_list.append(j)

    audiAcc_list = []
    for i in range(0, 10):
        j = data['boxOfficeResult']['dailyBoxOfficeList'][i]['audiAcc']
        audiAcc_list.append(j)

    audiAcc_list = [int(i) for i in audiAcc_list]

    total = []
    for i in range(0, 10):
        j = [r_list[i], open_list[i], audiAcc_list[i]]
        total.append(j)

    font_location = '/static/font/GILLUBCD.TTF'
    font_name = font_manager.FontProperties(fname=font_location).get_name()
    matplotlib.rc('font', family=font_name)

    plt.bar(r_list, audiAcc_list, color='red')
    plt.xlabel('제목', fontsize=15)
    plt.ylabel('관객수', fontsize=15)
    plt.xticks(rotation=90)
    plt.grid(True)
    gr = plt.show()
    gr

    return render_template('/data.html', plt=gr)
#------------ data end ------------------------------------

#map search
@app.route('/map')
def map():
    return render_template('/map.html')

# ------ news ------------
@app.route('/search')
def news():
    return render_template('/search.html')

@app.route('/s',methods=['POST'])
def s():
    rs = request.form['search']
    skind = request.form['skind']
    return search(rs,skind)

def search(rs,skind):
    skind = int(skind)
    client_id = "agr5hRZvAHuvK9Dv8sW4"
    client_secret = "BUf3PuRWNb"
    encText = urllib.parse.quote(rs)
    if skind == 1:
        url = "https://openapi.naver.com/v1/search/news?query=" + encText
    elif skind == 2:
        url = "https://openapi.naver.com/v1/search/book?query=" + encText
    elif skind == 3:
        url = "https://openapi.naver.com/v1/search/blog?query=" + encText
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if (rescode == 200):
        response_body = response.read()
        data = response_body.decode('utf-8')
        data = data.replace('<b>','').replace('</b>','').replace('&quot;','').replace('&amp;','')
        data_json = json.loads(data)

        lists =[]
        items = data_json['items']
        item_kind = [
            ('title', 'originallink', 'pubDate'),
            ('title', 'price', 'publisher'),
            ('title', 'bloggername', 'bloggerlink')
        ]
        for item in items:
            i1 = item[item_kind[skind - 1][0]]
            i2 = item[item_kind[skind - 1][1]]
            i3 = item[item_kind[skind - 1][2]]
            info = (i1,i2,i3)
            lists.append(info) # dict를 list에 담아서 보냄
        return render_template('/view.html', lists=lists, skind=skind)
    else:
        print('Error Code:' + rescode)
# ----- news end ------------

# -------- joinOk -----------
@app.route('/join')
def jogin():
    return render_template('/join.html')

# @app.route('/joinOk', methods=['POST'])
# def joinOk():
#      if request.method == 'POST':
#          uid = request.form['uid']
#          upwd = request.form['upwd']
#          uname = request.form['uname']
#          unick = request.form['unick']
#          uphone1 = request.form['uphone1']
#          uphone2 = request.form['uphone2']
#          uphone3 = request.form['uphone3']
#          ugender = request.form['ugender']
#          sedan = request.form['sedan']
#          suv = request.form['suv']
#          mini = request.form['mini']
#          elec = request.form['elec']

#          host = 'TeamKosy.mysql.pythonanywhere-services.com'
#          user = 'TeamKosy'
#          password = 'rootpass'
#          db = 'TeamKosy$teamkosy'
#          conn = pymysql.connect(host=host, user=user, password=password, db=db)

#          try:
#              with conn.cursor() as cursor:
#                  sql = 'insert into member (uId,uPwd,uName,uNick)'
#                  sql = sql + ' values(%s, %s, %s, %s)'
#                  cursor.execute(sql,(uid,upwd,uname,unick))
#                  conn.commit()

#                  return  render_template('/index.html')
#          finally:
#              conn.close()
# ------------ joinOk end ------------------------------------

if __name__ == '__main__':
    app.debug = True
#   db.create_all()
    app.run()
