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
    query5 = "SELECT COUNT(*) FROM users WHERE joined_date = CURRENT_DATE"
    query6 = "SELECT COUNT(*) FROM books WHERE added_date = CURRENT_DATE"

    cur.execute(query1)
    book_count=cur.fetchone()[0]

    cur.execute(query2)
    user_count=cur.fetchone()[0]

    cur.execute(query3)
    issue_today = cur.fetchone()[0]
    
    cur.execute(query4)
    pending = cur.fetchone()[0]

    cur.execute(query5)
    joined_today = cur.fetchone()[0]

    cur.execute(query6)
    recent_add_books = cur.fetchone()[0]

    return render_template('admin.html',Total_books=book_count,Active_users=user_count,issued_today=issue_today,book_pending=pending,new_registration=joined_today,recent_books=recent_add_books)

@app.route("/manage.html",methods=["GET","POST"])
def manage():
    if request.method=='POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        quantity = request.form['quantity']
        description = request.form['description']
        publisher = request.form['publisher']

        query = "INSERT INTO books(title,author,genre,publishyear,total_copies,copies_available,description,publisher) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(query,(title,author,genre,year,quantity,quantity,description,publisher))
        conn.commit()


    query1 = "SELECT book_id,title,author,genre,publishyear,total_copies,copies_available,description,publisher FROM books"
    cur.execute(query1)
    books = cur.fetchall()
    return render_template('manage.html',books=books)


@app.route('/editbook/<int:book_id>', methods=['GET'])
def editbook(book_id):
    query = "SELECT book_id,title,author,genre,publishyear,total_copies,description,publisher FROM books WHERE book_id = %s"
    cur.execute(query,(book_id,))
    book = cur.fetchone()
    return render_template('editbook.html',book = book)

@app.route('/update_book/<int:book_id>', methods=['POST'])
def update_book(book_id):
    title = request.form['title']
    author = request.form['author']
    genre = request.form['genre']
    year = request.form['year']
    quantity = int(request.form['quantity'])
    description = request.form['description']
    publisher = request.form['publisher']

    query = "SELECT copies_available FROM books WHERE book_id=%s"
    cur.execute(query,(book_id,))
    current_avail = cur.fetchone()[0]
    new_avail = current_avail+quantity

    que = "SELECT total_copies FROM BOOKS WHERE book_id = %s"
    cur.execute(que,(book_id,))
    old_total = cur.fetchone()[0]
    new_total = old_total+quantity

    query1 = "UPDATE books SET title=%s, author=%s, genre=%s, publishyear=%s,total_copies=%s, copies_available=%s, description=%s, publisher=%s WHERE book_id=%s"
    cur.execute(query1,(title,author,genre,year,new_total,new_avail,description,publisher,book_id))
    conn.commit()

    return redirect(url_for('manage'))


if __name__ == '__main__':
    app.run(debug=True)