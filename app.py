# app.py
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy database instance
db = SQLAlchemy(app)

# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    book_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Student:'{self.name}', email:'{self.email}', course:'{self.course}', address:'{self.address}', phone:'{self.phone}', book_name:'{self.book_name}'"

# Create tables in the database
with app.app_context():
    if not os.path.exists('library_database.db'):
        db.create_all()

# Home route
@app.route('/')
def index():
    return "Welcome to the Library Management System"

# Route for the home page displaying all students
@app.route('/home')
def home():
    student_home = Student.query.all()
    return render_template('home.html', student_home=student_home)

# Route to add a new student
@app.route('/add/student', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        course = request.form.get('course')
        address = request.form.get('address')
        phone = request.form.get('phone')
        book_name = request.form.get('book_name')

        new_student = Student(name=name, email=email, course=course, address=address, phone=phone, book_name=book_name)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add_student.html')

# Route to update student details
@app.route('/update/student/<int:student_id>', methods=['GET', 'POST'])
def update(student_id):
    student_edit = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student_edit.name = request.form['name']
        student_edit.email = request.form['email']
        student_edit.course = request.form['course']
        student_edit.address = request.form['address']
        student_edit.phone = request.form['phone']
        student_edit.book_name = request.form['book_name']
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('update_student.html', student=student_edit)

# Route to delete a student
@app.route('/delete/student/<int:student_id>', methods=['GET', 'POST'])
def delete(student_id):
    student_delete = Student.query.get_or_404(student_id)
    db.session.delete(student_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
