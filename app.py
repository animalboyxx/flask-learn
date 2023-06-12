import os
from flask import Flask, render_template, request, url_for, flash, session, redirect, abort
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SDFGUTYE65675D8686XC'

menu = [{'name': 'Установка', 'url': 'install-flask'},
        {'name': 'Первое приложение', 'url': 'first-app'},
        {'name': 'Обратная связь', 'url': 'contact'}]


@app.route('/')  # декоратор страницы
def index():
    print(url_for('index'))
    return render_template('index.html', title='xcvjk', menu=menu)


@app.route('/about')  # декоратор страницы
def about():
    print(url_for('about'))
    return render_template('about.html', title='vskaleno', menu=menu)


@app.route('/contact', methods=["POST", 'GET'])  # в обработчике явно указано то, что он может принимать данные переданные методом POST
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('message sent', category='success')
        else:
            flash('error while sending', category='error')
    return render_template('contact.html', title='обратная связь', menu=menu)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='page fucked', menu=menu), 404


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f"Пользователь: {username}"


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "selfedu" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title="Авторизация", menu=menu)
















app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Student {self.firstname}>'


if __name__ == '__main__':
    app.run(debug=True)
