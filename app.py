from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# initialize the database
db = SQLAlchemy(app)

# create model
class Todo(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   content = db.Column(db.String(200), nullable=False)
   completed = db.Column(db.Integer, default=0)
   date_created = db.Column(db.DateTime, default=datetime.utcnow())

   # return string every time new element is created
   def __repr__(self):
      return '<Task $r>' %self.id

# add methods for posting and getting
@app.route('/', methods=['POST', 'GET'])
def index():
   if request.method == 'POST':
      task_content = request.form['content']
      new_task = Todo(content=task_content)

      try:
         db.session.add(new_task)
         db.session.commit()
         return redirect('/')
      except:
         return "There was an issue adding task "

   else:
      tasks = Todo.query.order_by(Todo.date_created).all()
      return render_template('index.html', tasks=tasks)

# Deleting
@app.route('/delete/<int:id>')
def delete(id):
   task_to_delete = Todo.query.get_or_404(id)

   try:
      db.session.delete(task_to_delete)
      db.session.commit()
      return redirect('/')
   except:
      return 'Problem deleting task '

# udpate
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
   task = Todo.query.get_or_404(id)

   if request.method == 'POST':
     task.content = request.form['content']

     try:
        db.session.commit()
        return redirect('/')

     except:
        return 'There is issue updating task'

   else:
      return render_template('update.html', task=task)


if __name__ == '__app__':
   app.run(debug = True)