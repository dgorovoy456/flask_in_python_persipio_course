from flask import render_template, request, redirect, url_for, flash
from flask_package.forms import RegistrationForm, LoginFrom
from flask_package import app, db, bcrypt
from datetime import datetime
from flask_package.models import User
from flask_login import login_user, logout_user, current_user

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
    if current_user.is_authentificated():
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
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
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
    else:
        flash('Log in unsuccessful')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
