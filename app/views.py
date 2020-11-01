from flask import render_template, redirect, url_for, request

from app import app


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/admin', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again!'
        else:
            return redirect(url_for('index'))
    return render_template("login.html", error=error)


@app.route('/about')
def about():
    return render_template("about.html")
