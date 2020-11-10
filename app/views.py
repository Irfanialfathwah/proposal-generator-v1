from flask import render_template, redirect, url_for, request, session, flash
from functools import wraps
from datetime import datetime
from app import app
from db import db
from app.models import Customer
from app.form_validations import validate_customer_form

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


@app.route('/customers', methods=['GET', 'POST'])
@login_required
def customers():
    if request.method == 'POST':
        print(request.form)
        is_valid = validate_customer_form(request.form)
        print(is_valid)
        if 'errors' not in is_valid:
            timestamp = datetime.now().replace(microsecond=0)
            customer = Customer(**is_valid, created_at=timestamp, updated_at=timestamp)
            print(customer)
            db.session.add(customer)
            db.session.commit()
            flash('successfully added', category='success')
        else:
            flash(f'Error {is_valid}', category='danger')
    context = {
        'table_data': Customer.query.order_by(Customer.id).all()
    }
    print(context)
    return render_template("customers.html", **context)

@app.route('/customers/delete', methods=['POST'])
@login_required
def delete_customer():
    id = request.form.get('id')
    customer = Customer.query.filter_by(id=id).first()
    db.session.delete(customer)
    db.session.commit()
    return redirect('/customers')

@app.route('/proposals')
@login_required
def proposals():
    return render_template("proposals.html")


@app.route('/add-proposal')
@login_required
def addproposal():
    return render_template("add-proposal.html")


@app.route('/proposal-details')
@login_required
def proposaldetails():
    return render_template("proposal-details.html")


@app.route('/proposal-details-un')
@login_required
def proposaldetailsun():
    return render_template("proposal-details-un.html")
