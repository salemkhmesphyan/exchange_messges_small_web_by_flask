"""
programmer by en:salem khmes phyan
"""
import os,sys
from flask import Flask,render_template,request,send_file,flash,redirect,url_for,session
import sqlite3
from functools import wraps
from datetime import date
import time
import datetime

def login_required(function):
    @wraps(function) 
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return function(*args, **kwargs)
        else:
            flash(u'سجّل دخولك أولا')
            return redirect(url_for('login1'))
    return wrapper
app = Flask(__name__)
app.config['SECRET_KEY'] = "Secret"
app.config['USERNAME']   = "admin"
app.config['PASSWORD']   = "password"
APP_ROOT=os.path.dirname(os.path.abspath(__file__))
@app.route("/",methods=['GET','POST'])#methods=['GET']
def login1():
	return render_template(u'des1.html',t=u'صفحة تسجيل الدخول')
@app.route("/log2",methods=['GET','POST'])#methods=['GET']
def log2():
	n1= request.form['us1']
	pa1= request.form['pass1']
	db1=sqlite3.connect('dr1.db')
	db1.row_factory=sqlite3.Row
	db1.execute('create table if not exists users(ID integer primary Key autoincrement,namusr text,pass text)')
	db1.execute('''insert into users(namusr,pass) values(?,?)''',(n1,pa1))
	db1.commit()
	flash(u"لقد تم اضافة {}بنجاح".format(n1))
	return redirect(url_for('login1'))
@app.route("/log3",methods=['GET','POST'])#methods=['GET']
def log3():
	su=[]
	n1= request.form['us2']
	db1=sqlite3.connect('dr1.db')
	db1.row_factory=sqlite3.Row
	d=db1.execute("select * from users")
	for n in d:
		su.append(n['namusr'])
	if (n1) in su:
		session['logged_in'] =n1
		flash(u'سُجّل دخولك بنجاح، ستبقى مُسجّلا لمدّة نصف ساعة فقط.')
		return redirect(url_for('login1'))
	else:
		return """<h1>خطا في اسم المستخدم</h1><br>
		<a href="/">back</a>
		"""
@app.route("/out",methods=['GET','POST'])
def out():
	r1=[]
	db1=sqlite3.connect('dr1.db')
	db1.row_factory=sqlite3.Row
	d=db1.execute("select * from users")
	for n in d:
		#r1.append(n['namusr'])
		if n["namusr"]==session['logged_in']:
			g=n['pass']
			return render_template('showlog.html',ff=session['logged_in'],tt=g)
		#else:
			##session.pop('logged_in', None)
			#return """gooo """

@app.route("/logout")
def logout():
	h=session['logged_in']
	session.pop('logged_in', None)
	flash(h+":"+u'تم تسجل خروجك بنجاح')
	return redirect(url_for('login1'))
@app.route("/u1",methods=['GET','POST'])
def u1():
	db1=sqlite3.connect('dr1.db')
	db1.row_factory=sqlite3.Row
	d=db1.execute("select * from users")
	return render_template('mrslh.html',d=d)

@app.route("/<id1>",methods=['GET','POST'])
def u2(id1):
	ff=session['logged_in']
	db1=sqlite3.connect('dr1.db')
	db1.row_factory=sqlite3.Row
	db1.execute('create table if not exists usersdrdsh(ID integer primary Key autoincrement,namusr text,nammr text,time text,date text,drdsh text,shrk text)')
	db1.commit()
	f1=db1.execute("select * from users where ID='{}'".format(id1))
	for s in f1:
		h1=s["namusr"]
	cb=db1.cursor()
	cb.execute("select * from usersdrdsh where (namusr='{}' and nammr='{}')or(namusr='{}' and nammr='{}')".format(ff,h1,h1,ff))
	d=cb.fetchall()
	cb=db1.cursor()
	cb.execute("select * from usersdrdsh where namusr='{}' ORDER BY ID DESC limit 1".format(h1))
	d1=cb.fetchall()
	return render_template('smu.html',d=d,h1=h1,t=id1,d1=d1)
@app.route("/u3",methods=['GET','POST'])
def u3():
	t=time.asctime(time.localtime(time.time()))
	x=datetime.datetime.now().hour
	s=datetime.datetime.now().minute
	a=datetime.datetime.now().second
	time1=str(str(x)+":"+str(s)+":"+str(a))
	today = str(date.today())
	x1=0
	n1= request.form['s1']
	n2= request.form['s2']
	ff=session['logged_in']
	db1=sqlite3.connect('dr1.db')
	db1.row_factory=sqlite3.Row
	#e=db1.execute('select * from usersdrdsh where namusr="{}" and nammr="{}"'.format(ff,n2))
	e1=db1.execute('select * from users where namusr="{}"'.format(n2))
	
	for x in e1:
		f1=x["ID"]
	db1.execute("insert into usersdrdsh(namusr,nammr,time,date,drdsh,shrk) values(?,?,?,?,?,?)",(n2,ff,t,today,n1,"3"))
	db1.commit()
	d=db1.execute("select * from usersdrdsh where (namusr='{}' and nammr='{}')or(namusr='{}' and nammr='{}')".format(ff,n2,n2,ff))
	#if n1[1:4]=='img':
	print(request.files.getlist("data1"))
	target=os.path.join(APP_ROOT,'static/img/')
	if not os.path.isdir(target):
		os.mkdir(target)
	for fill in request.files.getlist("data1"):
		filename=fill.filename
		dest="/".join([target,filename])
		fill.save(dest)	
	#return render_template('smu.html',d=d,h1=n2,t=f1)
	return redirect(url_for('u2',id1=f1))
				
@app.route("/u4",methods=['GET','POST'])
def u4():
	n1= request.form['ii']
	return redirect(url_for('u2',id1=n1 ))
	#return redirect(url_for(u2(n2)))
if __name__ == "__main__":
	app.run(debug=True)
