 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///science_tutors.db'
db = SQLAlchemy(app)

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    rate = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Tutor %r>' % self.name

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    grade = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Student %r>' % self.name

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

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
    return render_template('schedule.html', tutors=tutors, students=students)

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
        subject = request.form['subject']
        rate = request.form['rate']
        tutor = Tutor(name=name, email=email, subject=subject, rate=rate)
        db.session.add(tutor)
        db.session.commit()
        return redirect(url_for('tutors'))
    return render_template('add_tutor.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        grade = request.form['grade']
        student = Student(name=name, email=email, grade=grade)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('students'))
    return render_template('add_student.html')

@app.route('/add_session', methods=['GET', 'POST'])
def add_session():
    if request.method == 'POST':
        tutor_id = request.form['tutor_id']
        student_id = request.form['student_id']
        date = request.form['date']
        time = request.form['time']
        duration = request.form['duration']
        session = Session(tutor_id=tutor_id, student_id=student_id, date=date, time=time, duration=duration)
        db.session.add(session)
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
