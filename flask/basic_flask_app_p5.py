from datetime import datetime
from logging import DEBUG
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.logger.setLevel(DEBUG)

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
        return redirect(url_for('index'))
    return render_template('feedback.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
