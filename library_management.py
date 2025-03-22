from flask import Flask, request, jsonify

app = Flask(_name_)

books = {"Python Programming": 5, "Data Structures": 3, "Artificial Intelligence": 4}
issued_books = {}

@app.route("/issue", methods=["POST"])
def issue_book():
    student = request.form.get("student")
    book = request.form.get("book")
    if book in books and books[book] > 0:
        books[book] -= 1
        issued_books[student] = book
        return f"{book} issued to {student}"
    return "Book not available", 400

@app.route("/return", methods=["POST"])
def return_book():
    student = request.form.get("student")
    if student in issued_books:
        book = issued_books.pop(student)
        books[book] += 1
        return f"{student} returned {book}"
    return "No book issued", 400

@app.route("/books", methods=["GET"])
def show_books():
    return jsonify(books)

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=9000)
