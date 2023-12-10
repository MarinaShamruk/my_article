from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template,request, redirect,url_for
from datetime import datetime
import os


spisok = {"1":"культура", "2":"здоровье", "3":"природа", "4":"история", "5":"общество", "6":"еда", "7":"путешествия",
          "8":"работа", "9":"образование", "10":"наука", "11":"животные", "12":"другое"}

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'journal.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.app_context().push()
db = SQLAlchemy(app)

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    theme = db.Column(db.String(40), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    quick = db.Column(db.String(300), nullable=False)
    text= db.Column(db.Text, nullable=False)
    date= db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<article{self.id}>"

@app.route("/")
def index():
    info = []
    try:
        info = Articles.query.order_by(Articles.date.desc()).all()

    except:
        print('Ошибка при работе с БД')
    return render_template("index.html", title='Главная', list=info, spisok=spisok)

@app.route("/<int:id>/all_text")
def all_text(id):
    info = []
    try:
        info = Articles.query.get(id)
        temp = info.text.split('\r')
    except:
        print('Ошибка при работе с БД')
    return render_template("all_text.html", title='Главная', list=info, spisok=spisok,temp=temp)


@app.route("/<int:id>/update", methods=('POST','GET'))
def update_record(id):
    r = Articles.query.get(id)
    if request.method == "POST":
        try:
           r.name = request.form['name']
           r.theme=request.form['theme']
           r.quick=request.form['quick']
           r.text=request.form['text']

           db.session.commit()
        except:
           db.session.rollback()
           print("Ошибка при редактировании записи")
        return redirect(url_for('all_text',id=id))
    else:
        return render_template('update.html', titile='Редактирование', list=r)

@app.route("/<int:id>/delete")
def del_record(id):
    info=Articles.query.get_or_404(id)
    try:
        db.session.delete(info)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'При удалении записи произошла ошибка'


@app.route("/article_add", methods=('POST','GET'))
def article_add():
    if request.method == "POST":
       try:
           info = Articles(name=request.form['name'], theme=request.form['theme'], title=request.form['title'],
                           quick=request.form['quick'], text=request.form['text'])

           db.session.add(info)
           db.session.commit()
       except:
           db.session.rollback()
           print("Ошибка добавления в БД")
       return redirect(url_for('index'))

    return render_template('article_add.html', titile='Размещение статьи',sp=spisok)

if __name__ == "__main__":
   app.run(debug=True)

