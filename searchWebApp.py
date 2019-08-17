
from flask import Flask, render_template, request, redirect, escape
from vsearch import search_for_letters
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def hello() -> '302':
    return redirect('/entry')


def log_request(req: 'flask_request', res: str) -> None:
    if req.headers.getlist("X-Forwarded-For"):
       ip = req.headers.getlist("X-Forwarded-For")[0]
    else:
       ip = req.remote_addr
    with open('vsearch.log', 'a') as vsearch_log:
        print(datetime.now().isoformat(),
              req.form, ip, req.user_agent,
              res, file=vsearch_log, sep='|')


@app.route('/vsearch', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search_for_letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_results=results,
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,)


@app.route('/entry')
def entry() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome tosearch4letters on the Web!')


@app.route('/viewlog')
def viewlog() -> 'html':
    with open('vsearch.log') as vsearch_log:
        i = 1
        result = []
        while i:
            i = escape(vsearch_log.readline())
            result.append(i.split('|'))
    titles = ('Date','Form Data','Remote Address', 'User Agent','Results')
    return render_template('viewlog.html',
                           the_title='View Log',
                           the_row_titles=titles,
                           the_data=result,)


if __name__ == '__main__':
    app.run(port='8000', debug=True)
