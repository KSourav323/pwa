from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore
app = Flask(__name__)

cred = credentials.Certificate('flutterflask-eee58-firebase-adminsdk-xbqm5-647816caab.json')
firebase_admin.initialize_app(cred)
db = firestore.client()



@app.route('/')
def index():
    students_ref = db.collection('Student')
    students = students_ref.stream()
    return render_template('index.html', students=students)



@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    mail = request.form['mail']
    gpa = float(request.form['gpa'])

    students_ref = db.collection('Student')
    students_ref.add({
        'Name': name,
        'Mail': mail,
        'GPA': gpa
    })
    return redirect(url_for('index'))



@app.route('/update/<student_id>', methods=['GET'])
def update(student_id):
    student_ref = db.collection('Student').document(student_id)
    doc_snapshot = student_ref.get()
    stud = doc_snapshot.to_dict()
    return render_template('update.html', student= stud, studid= student_id)



@app.route('/update/<student_id>', methods=['POST'])
def update_student(student_id):
    name = request.form['name']
    mail = request.form['mail']
    gpa = float(request.form['gpa'])

    student_ref = db.collection('Student').document(student_id)
    student_ref.update({
        'Name': name,
        'Mail': mail,
        'GPA': gpa
    })
    return redirect(url_for('index'))


@app.route('/delete/<student_id>', methods=['GET'])
def delete(student_id):
    student_ref = db.collection('Student').document(student_id)
    student_ref.delete()
    return redirect(url_for('index'))



@app.route('/offline.html')
def offline():
    return app.send_static_file('offline.html')


@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')


if __name__ == '__main__':
    app.run()
