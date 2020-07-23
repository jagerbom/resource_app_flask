from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.String(200), nullable=False)
    owner = db.Column(db.String(200), nullable=True)
    comment = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(200), nullable=True)
    last_updated = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_platform = request.form['type']
        task_owner = request.form['owner']
        task_comment = request.form['comment']
        task_status = request.form['status']
        task_last_updated = datetime.now().strftime("%c")
        new_task = Todo(content=task_content, platform=task_platform, owner=task_owner, comment=task_comment, status=task_status, last_updated=task_last_updated)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.owner = request.form['owner']
        task.comment = request.form['comment']
        task.status = request.form['status']
        task.last_updated = datetime.now().strftime("%c")
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)