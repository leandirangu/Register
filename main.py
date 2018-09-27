from flask import (Flask, render_template, request, make_response, redirect)
import json
import models
from models import Student

app = Flask('app')


@app.route('/')
def index():
    models.initialize()
    return render_template("index.html",)

@app.route('/register', methods=['POST', 'GET'])
def register():
  data = dict(request.form.items())
  if data.get('username',None):
    models.Student.create(
      username=data.get('username', 'anonymous'),
      name=data.get('name', 'Jane Doe'),
      course=data.get('course', 'Java'),
      age=data.get('age', '18')
    )
  return render_template("register_student.html")


@app.route('/students')
def students():
    students = models.Student.select()
    return render_template("students.html", students=students)

@app.route('/students/edit/<id>',  methods=['POST', 'GET'])
def edit_student(id="1"):
  student = Student.select().where(Student.id==id).first()
  data = dict(request.form.items())
  if data.get('id',None):
    student.name = data.get('name', student.name)
    student.course = data.get('course', student.course)
    student.age = data.get('age', student.age)
    student.save()
    return redirect('/students')
  context = {'student':student}
  return render_template('edit.html', **context)

@app.route('/welcome', methods=['POST'])
def welcome():
    data = dict(request.form.items())
    name = str(data.get('name', 'Guest'))
    email = str(data.get('email', 'no@email.com'))
    course = str(data.get('course', 'Not provided'))
    context = {'name':name, 'email':email, 'course': course}
    response = make_response(render_template("welcome.html", **context))
    response.set_cookie('register_app',json.dumps(context))
    return response

@app.route('/edit')
def edit():
    data = request.cookies.get('register_app')
    context = json.loads(data)
    response = make_response(render_template("edit.html", **context))
    return response



app.run(host='0.0.0.0', port=8080)