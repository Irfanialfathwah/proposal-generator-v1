from pathlib import Path
from flask import render_template, redirect, url_for, request, session, flash
from functools import wraps
from datetime import datetime
from app import app
from db import db
from app.models import Customer, Proposal, Roof
from app.form_validations import validate_customer_form, validate_proposal_form
from werkzeug.utils import secure_filename
from app.functions import allowed_file, add_gsa_report_to_db
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
                    file_path = app.config.get('UPLOAD_IMAGES_FOLDER') / filename
                    file.save(file_path)
                    is_valid.update({'skecthup_model' : file_path})
            proposal = Proposal(**is_valid, date_of_proposals=date_of_proposals, created_at=timestamp, updated_at=timestamp, status='Pending')
            db.session.add(proposal)
            db.session.commit()
            flash('successfully added', 'success')
            return redirect('/proposals')
    customers = Customer.query.order_by(Customer.id).all()
    return render_template("add-proposal.html", customers=customers)


@app.route('/proposal-details/<int:id>', methods=('POST','GET'))
@login_required
def proposaldetails(id):
    proposal = Proposal.query.filter_by(id=id).first()
    customers = Customer.query.order_by(Customer.id).all()
    if request.method == 'POST':
        is_valid = validate_proposal_form(request.form)
        if 'errors' not in is_valid:
            if 'skecthup_model' in request.files:
                file = request.files['skecthup_model']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = app.config.get('UPLOAD_IMAGES_FOLDER') / filename
                    file.save(file_path)
                    is_valid.update({'skecthup_model' : file_path})
            proposal.update(**is_valid)
            db.session.commit()
            flash('successfully updated', 'success')
            return redirect(f'/proposal-details/{id}')
    return render_template("proposal-details.html", proposal=proposal, customers=customers)


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


@app.route('/proposal-details/<int:id>/add', methods=("POST",))
@login_required
def add_order(id):
    # print(request.files)
    data = {}
    roofs = []
    timestamp = datetime.now().replace(microsecond=0)
    proposal = Proposal.query.filter_by(id=id).first()
    if request.files:
        filepaths = []
        print(request.files)
        for index,gsa_report in enumerate(request.files):
            file = request.files[f'gsa_report_file{index+1}']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = app.config.get('UPLOAD_FILES_FOLDER') / filename
                file.save(file_path)
                filepaths.append(file_path)
                s_data = add_gsa_report_to_db(filepaths)
    for nums in range(1,proposal.num_of_roofs+1):
        data['pv_panel'] = request.form.get(f"pv_panel{nums}")
        data['pv_panel_qty'] = request.form.get(f"pv_panel_qty{nums}")
        data['pv_cable'] = request.form.get(f"pv_cable{nums}")
        data['add_construction_qty'] = request.form.get(f"add_construction_qty{nums}")
        data['add_construction_price'] = request.form.get(f"add_construction_price{nums}")
        data['azimuth'] = request.form.get(f"azimuth{nums}")
        data['angle'] = request.form.get(f"angle{nums}")
        roof = Roof(**data, created_at=timestamp, updated_at=timestamp)
        roof.solar_data.extend(s_data[nums-1])
        roofs.append(roof)
    proposal.roofs.extend(roofs)
    db.session.add(proposal)
    db.session.add_all(roofs)
    db.session.commit()
    flash('successfully add roofs', category='success')
    return redirect(f'/proposal-details/{id}')


@app.route('/proposal-details/<int:id>/update', methods=("POST",))
@login_required
def update_order(id):
    # print(request.files)
    data = {}
    roofs = []
    proposal = Proposal.query.filter_by(id=id).first()
    for nums in range(1,proposal.num_of_roofs+1):
        data['pv_panel'] = request.form.get(f"pv_panel{nums}")
        data['pv_panel_qty'] = request.form.get(f"pv_panel_qty{nums}")
        data['pv_cable'] = request.form.get(f"pv_cable{nums}")
        data['add_construction_qty'] = request.form.get(f"add_construction_qty{nums}")
        data['add_construction_price'] = request.form.get(f"add_construction_price{nums}")
        data['azimuth'] = request.form.get(f"azimuth{nums}")
        data['angle'] = request.form.get(f"angle{nums}")
        proposal.roofs[nums-1].update(**data)
    db.session.commit()
    flash('successfully update roofs', category='success')
    return redirect(f'/proposal-details/{id}')


@app.route('/user')
@login_required
def user():
    return render_template("user.html")


@app.route('/role')
@login_required
def register():
    return render_template("role.html")


@app.route('/proposal-report')
@login_required
def proposal_report():
    return render_template("proposal-report.html")
