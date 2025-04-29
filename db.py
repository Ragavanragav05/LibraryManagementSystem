from flask import Flask, render_template,redirect,url_for,g,flash,request,session
import psycopg2

conn=psycopg2.connect(host="localhost",database="lms",user="postgres",password="@RAGAVAN999")
cur=conn.cursor()

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def login():
    if request.method=='POST':
        uname = request.form['uname']
        pwd = request.form['password']

        sel="SELECT username FROM users"             #Username Generate generation
        cur.execute(sel)
        names=cur.fetchall()

        usernames=[]
        for val in names:
            usernames.append(val[0])

        if uname  in usernames:
            return redirect(url_for('index'))
        else:
            return "<center><h1>signup please</h1></center>"
    
        #return redirect(url_for('home'))
    return render_template('login.html')


@app.route("/signup.html",methods=['GET','POST'])
def signup():
    if request.method=='POST':
        u_name = request.form['name']
        gmail = request.form['mail']
        password = request.form['password']
        phone_no = request.form['mobileno']

        sel="SELECT username FROM users"             #Username Generate generation
        cur.execute(sel)
        names=cur.fetchall()

        usernames=[]
        for val in names:
            usernames.append(val[0])

        if u_name in usernames:
            error_message = "Username already exists"
            return render_template('signup.html', error=error_message)
        else:
            ins="INSERT INTO users VALUES('"+u_name+"','"+gmail+"','"+password+"','"+phone_no+"')"
            cur.execute(ins)
            conn.commit()
            
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route("/index.html",methods=["GET","POST"])
def index():
    if request.method=='POST':
        username = request.form['name']
        bookname = request.form['bname']
        booktype = request.form['btype']

        user = "SELECT COUNT(*) FROM users WHERE username = %s"
        book = "SELECT COUNT(*) FROM books WHERE title = %s AND genre = %s"

        cur.execute(user,(username,))
        unames = cur.fetchone()[0]

        cur.execute(book,(bookname,booktype))
        bnames = cur.fetchone()[0] 

        if(unames<1):
            error_message = "check your username"
            return render_template('index.html', error1=error_message)
        if(bnames<1):
            error_message = "Type book title correctly"
            return render_template('index.html',error2=error_message)
        
        copies = "SELECT copies_available FROM books WHERE title = %s"
        cur.execute(copies,(bookname,))
        avail = cur.fetchone()[0]

        if(avail>0):
            query = "UPDATE books SET copies_available = %s WHERE title = %s AND genre = %s"
            cur.execute(query,(avail-1,bookname,booktype))
            conn.commit()

            query1 = "INSERT INTO booklog(username,title,genre) VALUES(%s,%s,%s)"
            cur.execute(query1,(username,bookname,booktype))
            conn.commit()
            
            return "<html><head><title>Successfull</title></head><body><h1>SuccessFully book is registered</h1></body></html>"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

