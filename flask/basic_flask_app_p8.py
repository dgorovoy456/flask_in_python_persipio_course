from datetime import datetime
from logging import DEBUG
from flask_package.forms import RegistrationForm, LoginFrom
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = b'\xc5J3\x81\xce2\xda\x10'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.logger.setLevel(DEBUG)

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"User('{self.username}','{self.email}', '{self.image_file}')"


feedback_list = []


def store_feedback(url):
    feedback_list.append(dict(
        url=url,
        user='Lonycorn',
        date=datetime.utcnow()
    ))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        url = request.form['url']
        store_feedback(url)
        app.logger.debug('stored feedback ' + url)
        flash('Your Feedback: ' + url)
        return redirect(url_for('index'))
    return render_template('feedback.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created !')
        return redirect(url_for('login'))
    if form.errors:
        flash('Validation Errors: ' + str(form.errors))
        app.logger.error('ValidationError:\n' + str(form.errors))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        if form.email.data == 'den.h@gmail.com' and form.password.data == 'qwerty':
            flash('Logged in')
            return redirect(url_for('index'))
        else:
            flash('Log in unsuccessful')
    return render_template('login.html', title='Login', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
