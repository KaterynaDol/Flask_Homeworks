from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Hello, Flask!</h1>'


@app.route('/user/<username>')
def user(username):
    return f'<h1>Hello, {username}!</h1>'



if __name__ == '__main__':
    app.run(debug=True)
