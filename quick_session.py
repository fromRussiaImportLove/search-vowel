from flask import Flask, session
from checker import check_logged_in

app = Flask(__name__)

app.secret_key = 'changeme'

@app.route('/setuser/<user>')
def setuser (user: str) -> str:
    session['user'] = user
    return 'User value set to: ' + session['user']


@app.route('/getuser')
def getuser() -> str:
    return 'User value is currently set to: ' + session['user']


@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are logged in now.'


@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are logged out.'

@app.route('/session')
def check_status() -> str:
    if 'logged_in' in session:
        return 'You are currently logged in.'
    return 'You are NOT logged in yet.'


@app.route('/page1')
@check_logged_in
def page1() -> str:
    return 'page1'


@app.route('/page2')
def page2() -> str:
    return 'page2'



if __name__ == '__main__':
    app.run(debug=True)