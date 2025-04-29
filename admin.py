from flask import Flask, render_template,redirect,url_for,g,flash,request,session
import psycopg2

conn=psycopg2.connect(host="localhost",database="lms",user="postgres",password="@RAGAVAN999")
cur=conn.cursor()

app = Flask(__name__)

@app.route("/")
def admin():
    query1 = "SELECT COUNT(*) FROM books"
    query2 = "SELECT COUNT(*) FROM users"
    query3 = "SELECT COUNT(*) FROM booklog WHERE issued_date = CURRENT_DATE"
    query4 = "SELECT COUNT(*) FROM booklog"

    cur.execute(query1)
    book_count=cur.fetchone()[0]

    cur.execute(query2)
    user_count=cur.fetchone()[0]

    cur.execute(query3)
    issue_today = cur.fetchone()[0]
    
    cur.execute(query4)
    pending = cur.fetchone()[0]

    return render_template('admin.html',Total_books=book_count,Active_users=user_count,issued_today=issue_today,book_pending=pending)
if __name__ == '__main__':
    app.run(debug=True)