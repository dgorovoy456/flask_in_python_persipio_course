from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return """
    <!doctype html>
    <html>
    <head>
        <title>Welcome</title>
    </head>
    <body>
    Hello World
    </body>
    </html>"""


if __name__ == '__main__':
    app.run(debug=True)
