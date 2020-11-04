from flask import render_template, redirect, url_for, request, session, flash
from functools import wraps
from app import app

# Adding encription key with Secret Key Variable for User Authentication

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
@login_required
def index():
    return render_template("index.html")


@app.route('/admin', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['email'] != 'admin@admin.com' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again!'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('index'))
    return render_template("login.html", error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('index'))


@app.route('/customers')
@login_required
def customers():
    return render_template("customers.html")


@app.route('/proposals')
@login_required
def proposals():
    return render_template("proposals.html")


@app.route('/add-proposal')
@login_required
def addproposal():
    return render_template("add-proposal.html")
