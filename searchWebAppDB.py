#integrated library
from flask import Flask, render_template, request, redirect, escape, session, copy_current_request_context
from time import sleep
from threading import Thread

#samopis
from vsearch import search_for_letters
from checker import check_logged_in
from DBcm import UseDatabase, select_SQL, ConnectionError, CredentialsError, SQLError


app = Flask(__name__)

app.secret_key = 'secretnosecret'

app.config['dbconfig'] = { 'host' : '127.0.0.1',
                           'user' : 'vsearch',
                           'password' : 'vsepasswd',
                           'database' : 'vsearchlogDB',}

@app.route('/')
def hello() -> '302':
    return redirect('/entry')


@app.route('/vsearch', methods=['POST'])
def do_search() -> 'html':

    @copy_current_request_context
    def log_request(req: 'flask_request', res: str) -> None:
        """Log details of web-request and the results"""
        sleep(15) # For test exception with long waiting
        try:
            with UseDatabase(app.config['dbconfig']) as cursor:
                _SQL = """insert into log
                          (phrase, letters, ip, browser_string, results)
                          values
                          (%s, %s, %s, %s, %s)"""
                cursor.execute(_SQL, (req.form['phrase'],
                                      req.form['letters'],
                                      req.remote_addr,
                                      req.user_agent.browser,
                                      res, ))
        except ConnectionError as err:
            print('Is your DB on? Error:', str(err))
        except CredentialsError as err:
            print('User-id/Password issues. Error:', str(err))
        except SQLError as err:
            print('Is your query correct? Error:', str(err))


    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search_for_letters(phrase, letters))
    try:
        t = Thread(target=log_request,args=(request, results))
        t.start()
    except Exception as err:
        print('Something wrong: ', str(err))
    return render_template('results.html',
                           the_results=results,
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,)


@app.route('/entry')
def entry() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome tosearch4letters on the Web!')


@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are logged in now.'


@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are logged out.'


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    """Display the contents of the log table from DB as a HTML table."""
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select ts, phrase, letters, ip, browser_string, results
                      from log"""
            cursor.execute(_SQL)
            result = cursor.fetchall()
            _SQL = """select count(*) from log"""
            cursor.execute(_SQL)
            allreq = cursor.fetchall()
            _SQL = """select count(letters) as 'count', letters from log
                      group by letters
                      order by count desc
                      limit 1"""
            cursor.execute(_SQL)
            freqletters = cursor.fetchall()
            _SQL = """select browser_string, count(browser_string) as 'count' from log
                      group by browser_string
                      order by count desc
                      limit 1"""
            cursor.execute(_SQL)
            freqbrowser = cursor.fetchall()
            
            ips = select_SQL(cursor, """select distinct ip from log""")
            #cursor.execute(_SQL)
            #ips = cursor.fetchall()
            
        titles = ('TimeStamp', 'Phrase', 'Letters', 'Remote Address', 'User Agent','Results')
        return render_template('viewlog.html',
                               the_title='View Log',
                               the_row_titles=titles,
                               the_data=result,
                               stat_requests=allreq,
                               stat_freqletters=freqletters,
                               stat_freqbrowser=freqbrowser,
                               stat_ip=ips,)
    except ConnectionError as err:
        print('Is your DB on? Error:', str(err))
    except CredentialsError as err:
        print('User-id/Password issues. Error:', str(err))
    except SQLError as err:
        print('Is your query correct? Error:', str(err))
    return 'Error'
    

if __name__ == '__main__':
    app.run(port='8000', debug=True)
