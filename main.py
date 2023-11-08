 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///science_tutors.db'
db = SQLAlchemy(app)

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    subjects = db.Column(db.String(255), nullable=False)
    availability = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Tutor %r>' % self.name

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    subjects = db.Column(db.String(255), nullable=False)
    grade_level = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Student %r>' % self.name

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return '<Session %r>' % self.id

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tutors')
def tutors():
    tutors = Tutor.query.all()
    return render_template('tutors.html', tutors=tutors)

@app.route('/schedule')
def schedule():
    tutors = Tutor.query.all()
    students = Student.query.all()
    subjects = Subject.query.all()
    return render_template('schedule.html', tutors=tutors, students=students, subjects=subjects)

@app.route('/progress')
def progress():
    students = Student.query.all()
    sessions = Session.query.all()
    return render_template('progress.html', students=students, sessions=sessions)

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/add_tutor', methods=['GET', 'POST'])
def add_tutor():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        subjects = request.form['subjects']
        availability = request.form['availability']
        new_tutor = Tutor(name=name, email=email, phone_number=phone_number, subjects=subjects, availability=availability)
        db.session.add(new_tutor)
        db.session.commit()
        return redirect(url_for('tutors'))
    return render_template('add_tutor.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        subjects = request.form['subjects']
        grade_level = request.form['grade_level']
        new_student = Student(name=name, email=email, phone_number=phone_number, subjects=subjects, grade_level=grade_level)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('students'))
    return render_template('add_student.html')

@app.route('/add_session', methods=['GET', 'POST'])
def add_session():
    if request.method == 'POST':
        tutor_id = request.form['tutor_id']
        student_id = request.form['student_id']
        subject = request.form['subject']
        date = request.form['date']
        time = request.form['time']
        new_session = Session(tutor_id=tutor_id, student_id=student_id, subject=subject, date=date, time=time)
        db.session.add(new_session)
        db.session.commit()
        return redirect(url_for('sessions'))
    return render_template('add_session.html')

@app.route('/delete_tutor/<int:id>')
def delete_tutor(id):
    tutor = Tutor.query.get_or_404(id)
    db.session.delete(tutor)
    db.session.commit()
    return redirect(url_for('tutors'))

@app.route('/delete_student/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('students'))

@app.route('/delete_session/<int:id>')
def delete_session(id):
    session = Session.query.get_or_404(id)
    db.session.delete(session)
    db.session.commit()
    return redirect(url_for('sessions'))

if __name__ == '__main__':
    app.run(debug=True)
