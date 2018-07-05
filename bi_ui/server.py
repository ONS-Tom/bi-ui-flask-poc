from flask import Flask, render_template, redirect, url_for, request


def create_app():
    app = Flask(__name__)
    return app


app = create_app()


@app.route('/Login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('.home'))
    return render_template('login.html', error=error)


@app.route('/Home')
def home():
    return 'Home Page'


@app.route('/Results')
def results():
    return 'Results Page'


@app.route('/NotFound')
def not_found():
    return 'Not Found'
