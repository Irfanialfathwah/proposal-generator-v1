from pathlib import Path
from flask import render_template, redirect, url_for, request, session, flash
from functools import wraps
from datetime import datetime
from app import app
from db import db
from app.models import Customer, Proposal
from app.form_validations import validate_customer_form, validate_proposal_form
from werkzeug.utils import secure_filename
from app.functions import allowed_file
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
        is_valid = validate_customer_form(request.form)
        if 'errors' not in is_valid:
            timestamp = datetime.now().replace(microsecond=0)
            customer = Customer(**is_valid, created_at=timestamp, updated_at=timestamp)
            db.session.add(customer)
            db.session.commit()
            flash('successfully added', category='success')
        else:
            flash(f'Error {is_valid}', category='danger')
    table_data = Customer.query.order_by(Customer.id).all()
    list_prop_comp = [len([d for d in data.proposals if d.status == 'Completed']) for data in table_data]
    context = {
        'table_data': zip(table_data, list_prop_comp),
        'customers': table_data
    }
    return render_template("customers.html", **context)


@app.route('/customers/delete', methods=['POST'])
@login_required
def delete_customer():
    id = request.form.get('id')
    customer = Customer.query.filter_by(id=id).first()
    db.session.delete(customer)
    db.session.commit()
    return redirect('/customers')


@app.route('/customers/update', methods=['POST'])
@login_required
def edit_customer():
    id = request.form.get('id')
    is_valid = validate_customer_form(request.form)
    if 'errors' not in is_valid:
        customer = Customer.query.filter_by(id=id).first()
        customer.update(**is_valid)
        db.session.commit()
        flash('Success update customers', 'success')
    return redirect('/customers')


@app.route('/proposals')
@login_required
def proposals():
    proposals = Proposal.query.order_by(Proposal.id).all()
    return render_template("proposals.html", proposals=proposals)


@app.route('/add-proposal', methods=('GET','POST'))
@login_required
def addproposal():
    if request.method == 'POST':
        is_valid = validate_proposal_form(request.form)
        if 'errors' not in is_valid:
            timestamp = datetime.now().replace(microsecond=0)
            date_of_proposals = timestamp.replace(hour=0, minute=0, second=0)
            if 'skecthup_model' in request.files:
                file = request.files['skecthup_model']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = app.config.get('UPLOAD_FOLDER') / filename
                    file.save(file_path)
                    is_valid.update({'skecthup_model' : file_path})
            proposal = Proposal(**is_valid, date_of_proposals=date_of_proposals, created_at=timestamp, updated_at=timestamp, status='Pending')
            db.session.add(proposal)
            db.session.commit()
            flash('successfully added', 'success')
            return redirect('/proposals')
    customers = Customer.query.order_by(Customer.id).all()
    return render_template("add-proposal.html", customers=customers)


@app.route('/proposal-details/<int:id>', methods=('POST',))
@login_required
def proposaldetails(id):
    proposal = Proposal.query.filter_by(id=id).first()
    if request.method == 'POST':
        is_valid = validate_proposal_form(request.form)
        if 'errors' not in is_valid:
            if 'skecthup_model' in request.files:
                file = request.files['skecthup_model']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = app.config.get('UPLOAD_FOLDER') / filename
                    file.save(file_path)
                    is_valid.update({'skecthup_model' : file_path})
            proposal.update(**is_valid)
            db.session.commit()
            flash('successfully updated', 'success')
            return redirect('/proposals-details')
    return render_template("proposal-details.html", proposal=proposal)


@app.route('/proposals/delete', methods=('POST',))
@login_required
def delete_proposal():
    id = request.form.get('id')
    proposal = Proposal.query.filter_by(id=id).first()
    db.session.delete(proposal)
    db.session.commit()
    return redirect('/proposals')


@app.route('/proposal-details-un')
@login_required
def proposaldetailsun():
    return render_template("proposal-details-un.html")


@app.route('/user')
@login_required
def user():
    return render_template("user.html")


@app.route('/role')
@login_required
def register():
    return render_template("role.html")
