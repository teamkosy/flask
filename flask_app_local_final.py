from flask import Flask, render_template, request, session, flash, app
from datetime import timedelta
import urllib
import urllib.request
import json
import pymysql
import math

app = Flask(__name__)


def dbcon():
    host = 'TeamKosy.mysql.pythonanywhere-services.com'
    user = 'TeamKosy'
    password = 'rootpass'
    db = 'TeamKosy$teamkosy'
    conn = pymysql.connect(host=host, user=user, password=password, db=db)

    return conn

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
    if session.get('logFlag') != True:
        flash('로그인 이후 사용 가능합니다.')
        # return render_template('/login.html')
        return login()
    else:
        return render_template('/myPage.html')
    # return render_template('/myPage.html')

# member
@app.route('/member')
def member():
    conn = dbcon()
    with conn.cursor() as cursor:
        sql = 'select * from member order by idx desc'
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()

        return render_template('/member.html', rows=rows)

# memberSearch
@app.route('/memberSearch', methods=['POST'])
def memberSearch():
    uid = request.form['uid']

    conn = dbcon()

    with conn.cursor() as cursor:
         sql = 'select * from member where uid=%s'
         cursor.execute(sql,uid)
         rows = cursor.fetchall()
         conn.close()
         if rows == ():
             flash('존재하지 않는 ID 입니다.')
             return member()
         else:
             rs = rows[0][1]
             return render_template('/memberSearch.html', rows=rows, rs=rs)

# modify
@app.route('/modify')
def modify():
    idx = session['idx']

    conn = dbcon()
    with conn.cursor() as cursor:
        sql = 'select * from member where idx = %s'
        cursor.execute(sql,idx)
        rows = cursor.fetchall()
        conn.close()
        for rs in rows:
            upwd = rs[2]
            uname = rs[3]
            unick = rs[4]
            phone2 = rs[6]
            phone3 = rs[7]

        return render_template('/modify.html',upwd=upwd, uname=uname, unick=unick,phone2=phone2, phone3=phone3 )

# -------- modifyOk ------------------------------

@app.route('/modifyOk', methods=['GET'])
def modifyOk():
    idx = session['idx']
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

    conn = dbcon()
    with conn.cursor() as cursor:
        sql = 'update member set  upwd = %s, uname= %s, unick= %s, uphone1= %s, uphone2= %s, uphone3= %s, ugender= %s, sedan= %s, suv= %s, mini= %s, elec= %s where idx = %s'
        cursor.execute(sql,(upwd, uname, unick, uphone1, uphone2, uphone3, ugender, sedan, suv, mini, elec, idx))
        rows = cursor.fetchall()
        conn.commit()
        conn.close()

        session['unick'] = unick

        flash('수정이 완료 되었습니다.')
        return render_template('/myPage.html', rows=rows)

# -----------------modifyOk end -----------------------------------------------

#회원 탈퇴
@app.route('/del', methods=['POST'])
def memberdel():
    idx = session['idx']

    conn = dbcon()
    with conn.cursor() as cursor:
        sql = 'delete from member where idx = %s'
        cursor.execute(sql,idx)
        conn.commit()
        conn.close()

        session['logFlag'] = False
        session.pop('idx', None)
        session.pop('uid', None)
        session.pop('unick', None)

        flash('회원 탈퇴 되었습니다 ㅠㅠ')

        return index()

#------------------------------------------------------------------

# logOut
@app.route('/logOut')
def logOut():
    session['logFlag'] = False
    session.pop('idx', None)
    session.pop('uid', None)
    session.pop('unick', None)
    flash('로그아웃 되었습니다.')

    return index()

#  -------- loginOk ------------------------------
@app.route('/loginOk', methods=['POST'])
def loginOk():

    uid = request.form['uid']
    upwd = request.form['upwd']
    if len(uid) == 0 or len(upwd) == 0:
        flash('ID'+','+'PW'+'로그인 정보가 틀립니다.')
        return login()
    else:
        conn = dbcon()

        try:
            with conn.cursor() as cursor:
                sql = 'select idx, uid, upwd, unick from member where uid = %s'
                cursor.execute(sql, (uid,))
                rows = cursor.fetchall()
                if rows == ():
                    flash('ID' + ',' + 'PW' + '로그인 정보가 틀립니다.')

                    return render_template('/login.html')
                else:
                    for rs in rows:
                        if rs[1] == uid and rs[2] == upwd:
                            session['logFlag'] = True
                            session['idx'] = rs[0]
                            session['uid'] = uid
                            session['unick'] = rs[3]

                            return index()

                        else:
                            flash('ID' + ',' + 'PW' + '로그인 정보가 틀립니다.')

                            return render_template('/login.html')

        finally:
            conn.close()

# -----------------loginOk end -----------------------------------------------

# ------------------- join -------------------------------------
#회원 가입 화면
@app.route('/join')
def join():
    return render_template('/join.html')

#id 체크 팝업
@app.route('/idCheck')
def idCheck():
    return render_template('/idCheck.html')


#id 중복 체크
@app.route('/idCheckOk', methods=['GET', 'POST'])
def idCheckOk():
    # uid = request.args.get('uid')
    uid = request.form['uid']

    host = 'localhost'
    user = 'root'
    password = 'rootpass'
    db = 'jspdb'
    conn = pymysql.connect(host=host, user=user, password=password, db=db)

    with conn.cursor() as cursor:
        sql = 'select * from member where uid=%s'
        cursor.execute(sql, uid)
        rows = cursor.fetchall()
        conn.close()
        if rows == ():
            flash('사용 가능한 ID입니다.')
            return join()
        else:
            flash('사용중인 ID입니다. 다른 ID를 사용해주세요~')
            return render_template('/join.html')

#------------------ joinOk ------------------------------------
@app.route('/joinOk', methods=['GET','POST'])
def joinOk():
    uid = request.form['uid']
    upwd = request.form['upwd']
    uname = request.form['uname']
    unick = request.form['unick']
    uphone1 = request.form['uphone1']
    uphone2 = request.form['uphone2']
    uphone3 = request.form['uphone3']
    ugender = request.form.getlist('ugender')
    if ugender == []:
        ugender = 'NULL'
    sedan = request.form.getlist('sedan')
    if sedan == []:
        sedan = 'NULL'
    suv = request.form.getlist('suv')
    if suv == []:
        suv = 'NULL'
    mini = request.form.getlist('mini')
    if mini == []:
        mini = 'NULL'
    elec = request.form.getlist('elec')
    if elec == []:
        elec = 'NULL'


    if len(uid) == 0 or len(upwd) == 0:
        flash('ID' + ',' + 'PW' + '필수 입력 사항입니다.')
        return joinOk()
    else:
        conn = dbcon()
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

#teamkosy
@app.route('/kosy')
def kosy():
    return render_template('/kosy.html')

#carInfo
@app.route('/cal')
def cal():
    return render_template('/cal.html')

#calOk
@app.route('/calOk')
def calOk():
    cname = request.args.get('info')

    conn = dbcon()
    with conn.cursor() as cursor:
        sql = 'select cname, cprice, cpay, cbat, coil from carboard where cname = %s'
        cursor.execute(sql,(cname,))
        rows = cursor.fetchall()
        conn.close()
        return render_template('/cal.html', row=rows)

#data
@app.route('/data')
def gwrite():
    return render_template('/data.html')

#map
@app.route('/map')
def map():
    return render_template('/map_1.html')

#map search
@app.route('/map_1')
def map_1():
     return render_template('/map_1.html')

#map search
@app.route('/map_2')
def map_2():
     return render_template('/map_2.html')

#map search
@app.route('/map_3')
def map_3():
     return render_template('/map_3.html')

#map search
@app.route('/map_4')
def map_4():
     return render_template('/map_4.html')

#map search
@app.route('/map_5')
def map_5():
     return render_template('/map_5.html')

#map search
@app.route('/map_6')
def map_6():
     return render_template('/map_6.html')

#map search
@app.route('/map_7')
def map_7():
     return render_template('/map_7.html')

#map search
@app.route('/map_8')
def map_8():
     return render_template('/map_8.html')

@app.route('/map_9')
def map_9():
     return render_template('/map_9.html')

#map search
@app.route('/map_10')
def map_10():
     return render_template('/map_10.html')

#map search
@app.route('/map_11')
def map_11():
     return render_template('/map_11.html')

#map search
@app.route('/map_12')
def map_12():
     return render_template('/map_12.html')

#map search
@app.route('/map_13')
def map_13():
     return render_template('/map_13.html')

#map search
@app.route('/map_14')
def map_14():
     return render_template('/map_14.html')

#map search
@app.route('/map_15')
def map_15():
     return render_template('/map_15.html')

#map search
@app.route('/map_16')
def map_16():
     return render_template('/map_16.html')

#map search
@app.route('/map_17')
def map_17():
     return render_template('/map_17.html')

# kosyInfo
@app.route('/kosyInfo')
def kosyInfo():
    return render_template('/kosyInfo.html')

# web
@app.route('/web')
def web():
    return render_template('/web.html')

# ment
@app.route('/ment')
def ment():
    if session.get('logFlag') != True:
        flash('로그인 이후 사용 가능합니다.')
        # return render_template('/login.html')
        return login()
    else:
        return render_template('/ment.html')
    # return render_template('/ment.html')

# ------------------ news -----------------------------------
@app.route('/search')
def news():
    return render_template('/search.html')

# ------------------ news search-----------------------------------
@app.route('/s',methods=['GET'])
def s():
    rs = request.args.get('search')
    skind = request.args.get('skind')
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
        url = "https://openapi.naver.com/v1/search/news?query=" + encText +"&display=50&start=1&sort=sim"
    elif skind == 2:
        url = "https://openapi.naver.com/v1/search/book?query=" + encText +"&display=50&start=1&sort=sim"
    elif skind == 3:
        url = "https://openapi.naver.com/v1/search/blog?query=" + encText +"&display=50&start=1&sort=sim"
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

    # now_aware = datetime.now(timezone('Asia/Seoul'))

    conn = dbcon()
    with conn.cursor() as cursor:
         sql = 'insert into board (messege,bnick)'
         sql = sql + ' values(%s, %s)'
         cursor.execute(sql,(messege,bnick))
         conn.commit()
         conn.close()
         return index()

#--------------------- board write end ---------------------------------

#--------------------- board 페이징---------------------------------
def select():
    conn = dbcon()
    with conn.cursor() as cursor:
         sql = 'select * from board order by bidx desc limit 5'
         cursor.execute(sql)
         rows = cursor.fetchall()
         conn.close()

         return rows

def select_count():
    conn = dbcon()
    with conn.cursor() as cursor:
         sql = 'select count(bidx) from board'
         cursor.execute(sql)
         row = cursor.fetchone()
         conn.close()

         return row[0]

def select_page(list_limit, page):

    conn = dbcon()
    with conn.cursor() as cursor:
         offset = (page - 1) * list_limit
         sql = 'select * from board order by bidx desc limit %s offset %s'
         cursor.execute(sql, (list_limit, offset))
         rows = cursor.fetchall()
         conn.close()

         return rows

@app.route('/<int:page>')
def list(page):
    list_num = 5
    list_count = select_count()
    page_count = math.ceil(list_count / list_num)
    lists = select_page(list_num, page)

    return render_template('/index.html', lists=lists, page_count=page_count)

#--------------------- board 페이징 end ---------------------------------

#---------------------- BMI ---------------------------------------------
@app.route('/bmi')
def bmi():
    return render_template('/bmi.html')

@app.route('/bmiOk', methods=['POST'])
def calc_bmi():
    w1 = request.form['w']
    h1 = request.form['h']

    if len(w1) == 0 or len(h1) == 0:
        flash('측정 값을 입력하세요.')
        return render_template('/bmi.html')
    else:
        w = int(w1)
        h = int(h1)
        bmi = w / (h/100) ** 2
        if bmi < 18.5:
            return render_template('/bmi.html', bmi="저체중 : 마른편입니다. 조금 더 먹어도 괜찮아요^^")
        if bmi < 25:
            return render_template('/bmi.html', bmi="정상 :적당하네요^^ 잘 유지하세요~")
        return render_template('/bmi.html', bmi="비만 ㅠㅠ : 다이어트가 필요합니다~")
#---------------------- BMI end ---------------------------------------------

@app.before_request
def make_session_permanent():
    session.permanent =True
    app.permanent_session_lifetime = timedelta(minutes=1)

app.secret_key = 'sample_secreat_key'
if __name__ == '__main__':
    app.debug = True
    app.run()



