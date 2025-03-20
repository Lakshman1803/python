from Flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__library__)
library = {}
students = {}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/view_books')
def view_books():
    return render_template("view_books.html", library=library)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_name = request.form['book_name']
        copies = int(request.form['copies'])
        library[book_name] = library.get(book_name, 0) + copies
        return redirect(url_for('view_books'))
    return render_template("add_book.html")

@app.route('/issue_book', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST':
        book_name = request.form['book_name']
        student_name = request.form['student_name']
        student_no = request.form['student_no']
        if library.get(book_name, 0) > 0:
            library[book_name] -= 1
            issue_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            student_key = (student_name, student_no)
            students[student_key] = students.get(student_key, []) + [(book_name, issue_date)]
            return redirect(url_for('index'))
        return "Book not available"
    return render_template("issue_book.html")

@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        book_name = request.form['book_name']
        student_name = request.form['student_name']
        student_no = request.form['student_no']
        student_key = (student_name, student_no)
        if student_key in students:
            for entry in students[student_key]:
                if entry[0] == book_name:
                    students[student_key].remove(entry)
                    library[book_name] = library.get(book_name, 0) + 1
                    return redirect(url_for('index'))
        return "Error returning the book"
    return render_template("return_book.html")

if __name__ == '__main__':
    app.run(debug=True)

