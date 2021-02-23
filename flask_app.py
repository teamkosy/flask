from flask import Flask, render_template, request, session, flash
import urllib
import urllib.request
import json
import pymysql
import math
# import requests
# import matplotlib.pyplot as plt
# import matplotlib
# from matplotlib import font_manager

app = Flask(__name__)

# index 화면
@app.route('/')
def index():
    lists = select()
    list_num =5
    list_count = select_count()
    page_count = math.ceil(list_count/list_num)

    return render_template('/index.html', lists=lists, page_count=page_count)


# login
@app.route('/login')
def login():
    return render_template('/login.html')

# myPage
@app.route('/myPage')
def myPage():
    return render_template('/myPage.html')

# member
@app.route('/member')
def member():
    host = 'TeamKosy.mysql.pythonanywhere-services.com'
    user = 'TeamKosy'
    password = 'rootpass'
    db = 'TeamKosy$teamkosy'
    conn = pymysql.connect(host=host, user=user, password=password, db=db)

    try:
        with conn.cursor() as cursor:
             sql = 'select * from member order by idx desc'
             cursor.execute(sql)
             rows = cursor.fetchall()
             conn.close()

             return render_template('/member.html', rows=rows)

    finally:
        conn.close()

# modify
@app.route('/modify', methods=['GET'])
def modify():
    idx = request.args.get('idx')

    host = 'TeamKosy.mysql.pythonanywhere-services.com'
    user = 'TeamKosy'
    password = 'rootpass'
    db = 'TeamKosy$teamkosy'
    conn = pymysql.connect(host=host, user=user, password=password, db=db)

    try:
        with conn.cursor() as cursor:
             sql = 'select * from member where idx = %s'
             cursor.execute(sql(idx,))
             rows = cursor.fetchall()
             conn.close()

             return render_template('/modifyOk',rows=rows)
    finally:
        conn.close()

# -------- modifyOk ------------------------------

@app.route('/modifyOk', methods=['GET'])
def modifyOk():
    uid = request.args.get('uid')
    upwd = request.args.get('upwd')
    uname = request.args.get('uname')
    unick = request.args.get('unick')
    uphone1 = request.args.get('uphone1')
    uphone2 = request.args.get('uphone2')
    uphone3 = request.args.get('uphone3')
    ugender = request.args.get('ugender')
    sedan = request.args.get('sedan')
    suv = request.args.get('suv')
    mini = request.args.get('mini')
    elec = request.args.get('elec')

    host = 'TeamKosy.mysql.pythonanywhere-services.com'
    user = 'TeamKosy'
    password = 'rootpass'
    db = 'TeamKosy$teamkosy'
    conn = pymysql.connect(host=host, user=user, password=password, db=db)

    try:
        with conn.cursor() as cursor:
            sql = 'update member set uid = %s, upwd = %s, uname= %s, unick= %s, uphone1= %s, uphone2= %s, uphone3= %s, ugender= %s, sedan= %s, suv= %s, mini= %s, elec= %s where idx = %s'
            cursor.execute(sql,(uid, upwd, uname, unick,uphone1,uphone2,uphone3,ugender,sedan,suv,mini,elec))
            conn.comit()
            flash('수정이 완료 되었습니다.')

            return render_template('/myPage.html')
    finally:
        conn.close()

# -----------------modifyOk end -----------------------------------------------

# logOut
@app.route('/logOut', methods=['POST','GET'])
def logOut():
    session['logFlag'] = False
    session.pop('uid', None)
    session.pop('unick', None)
    flash('로그아웃 되었습니다.')

    return index()

# -------- loginOk ------------------------------
@app.route('/loginOk', methods=['POST'])
def loginOk():
    # uid = request.args.get('uid')
    # upwd = request.args.get('upwd')

    uid = request.form['uid']
    upwd = request.form['upwd']
    if len(uid) == 0 or len(upwd) == 0:
        flash('ID'+','+'PW'+'로그인 정보가 틀립니다.')
        return login()
    else:
        host = 'TeamKosy.mysql.pythonanywhere-services.com'
        user = 'TeamKosy'
        password = 'rootpass'
        db = 'TeamKosy$teamkosy'
        conn = pymysql.connect(host=host, user=user, password=password, db=db)

        try:
            with conn.cursor() as cursor:
                sql = 'select idx, uid, upwd, unick from member where uid = %s'
                cursor.execute(sql,(uid,))
                rows = cursor.fetchall()
                for rs in rows:
                    if rs[1] == uid and rs[2] == upwd:
                        session['logFlag'] = True
                        session['idx'] = rs[0]
                        session['uid'] = uid
                        session['unick'] = rs[3]

                        return index()

                    else:
                        flash('ID'+','+'PW'+'로그인 정보가 틀립니다.')

                        return  render_template('/login.html')

        finally:
            conn.close()
# -----------------loginOk end -----------------------------------------------

# ------------------- join -------------------------------------
@app.route('/join')
def jogin():
    return render_template('/join.html')

#------------------ joinOk ------------------------------------
@app.route('/joinOk', methods=['POST'])
def joinOk():

        uid = request.form['uid']
        upwd = request.form['upwd']
        uname = request.form['uname']
        unick = request.form['unick']
        uphone1 = request.form['uphone1']
        uphone2 = request.form['uphone2']
        uphone3 = request.form['uphone3']
        ugender = request.form.getlist('ugender')
        sedan = request.form.getlist('sedan')
        suv = request.form.getlist('suv')
        mini = request.form.getlist('mini')
        elec = request.form.getlist('elec')

        # uid = request.args.get('uid')
        # upwd = request.args.get('upwd')
        # uname = request.args.get('uname')
        # unick = request.args.get('unick')
        # uphone1 = request.args.get('uphone1')
        # uphone2 = request.args.get('uphone2')
        # uphone3 = request.args.get('uphone3')
        # ugender = request.args.get('ugender')
        # sedan = request.args.get('sedan')
        # suv = request.args.get('suv')
        # mini = request.args.get('mini')
        # elec = request.args.get('elec')
        if len(uid) == 0 or len(upwd) == 0:
            flash('ID'+','+'PW'+'필수 입력 사항입니다.')
            return login()
        else:
            host = 'TeamKosy.mysql.pythonanywhere-services.com'
            user = 'TeamKosy'
            password = 'rootpass'
            db = 'TeamKosy$teamkosy'
            conn = pymysql.connect(host=host, user=user, password=password, db=db)

            try:
                with conn.cursor() as cursor:
                    sql = 'insert into member (uid,upwd,uname,unick,uphone1,uphone2,uphone3,ugender,sedan,suv,mini,elec)'
                    sql = sql + ' values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    cursor.execute(sql,(uid,upwd,uname,unick,uphone1,uphone2,uphone3,ugender,sedan,suv,mini,elec))
                    conn.commit()
                    session['logFlag'] = True
                    session['uid'] = uid
                    flash('가입을 환영합니다. 로그인 해주세요')

                    return  render_template('/login.html')
            finally:
                conn.close()
# ------------ joinOk end ------------------------------------

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

#calOk
@app.route('/calOk')
def calOk():
    cname = request.args.get('info')

    host = 'TeamKosy.mysql.pythonanywhere-services.com'
    user = 'TeamKosy'
    password = 'rootpass'
    db = 'TeamKosy$teamkosy'
    conn = pymysql.connect(host=host, user=user, password=password, db=db)

    try:
        with conn.cursor() as cursor:
             sql = 'select cname, cprice, cpay, cbat, coil from carboard where cname = %s'
             cursor.execute(sql,(cname,))
             row = cursor.fetchall()

             return render_template('/cal.html', row=row)

    finally:
        conn.close()

#data
@app.route('/data')
def gwrite():
    return render_template('/data.html')

#map search
@app.route('/map')
def map():
    #return render_template('/map.html')
    return render_template('/map_s.html')

# ------------------ news -----------------------------------
@app.route('/search')
def news():
    return render_template('/search.html')

# ------------------ news search-----------------------------------
@app.route('/s',methods=['POST'])
def s():
    rs = request.form['search']
    skind = request.form['skind']
    if len(rs) == 0 or len(skind) == 0:
        flash('검색 내용을 입력해주세요')
        return render_template('/search.html')
    else:
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
            lists.append(info)
        return render_template('/view.html', lists=lists, skind=skind)
    else:
        print('Error Code:' + rescode)
# -------------- news end ----------------------------------------

#--------------------- board write---------------------------------
@app.route('/bwrite', methods=['POST'])
def bwrite():
    messege = request.form['messege']
    bnick = request.form['unick']
    # messege = request.args.get('messege')
    # bnick = request.args.get('unick')

    host = 'TeamKosy.mysql.pythonanywhere-services.com'
    user = 'TeamKosy'
    password = 'rootpass'
    db = 'TeamKosy$teamkosy'
    conn = pymysql.connect(host=host, user=user, password=password, db=db)

    try:
        with conn.cursor() as cursor:
             sql = 'insert into board (messege,bnick)'
             sql = sql + ' values(%s, %s)'
             cursor.execute(sql,(messege,bnick))
             conn.commit()

             #return  render_template('/index.html')
             return index()
    finally:
        conn.close()
#--------------------- board write end ---------------------------------

#--------------------- board 페이징 ---------------------------------
def select():
    host = 'TeamKosy.mysql.pythonanywhere-services.com'
    user = 'TeamKosy'
    password = 'rootpass'
    db = 'TeamKosy$teamkosy'
    conn = pymysql.connect(host=host, user=user, password=password, db=db)

    with conn.cursor() as cursor:
         sql = 'select * from board order by bidx desc limit 5'
         cursor.execute(sql)
         rows = cursor.fetchall()
         conn.close()

         return rows

def select_count():
    host = 'TeamKosy.mysql.pythonanywhere-services.com'
    user = 'TeamKosy'
    password = 'rootpass'
    db = 'TeamKosy$teamkosy'
    conn = pymysql.connect(host=host, user=user, password=password, db=db)

    with conn.cursor() as cursor:
         sql = 'select count(bidx) from board'
         cursor.execute(sql)
         row = cursor.fetchone()
         conn.close()

         return row[0]

def select_page(list_limit, page):
    host = 'TeamKosy.mysql.pythonanywhere-services.com'
    user = 'TeamKosy'
    password = 'rootpass'
    db = 'TeamKosy$teamkosy'
    conn = pymysql.connect(host=host, user=user, password=password, db=db)

    with conn.cursor() as cursor:
         offset = (page -1) * list_limit
         sql = 'select * from board order by bidx desc limit %s offset %s'
         cursor.execute(sql, (list_limit,offset))
         rows = cursor.fetchall()
         conn.close()

         return rows

@app.route('/list/<int:page>')
def list(page):
    list_num = 5
    list_count = select_count()
    page_count = math.ceil(list_count / list_num)
    lists = select_page(list_num, page)

    return render_template('/index.html', lists=lists, page_count=page_count)

#--------------------- board 페이징 end ---------------------------------

app.secret_key = 'sample_secreat_key'
if __name__ == '__main__':
    app.debug = True
    app.run()