import numpy as np
from pathlib import Path
import pdfkit
import os
from flask import render_template, redirect, url_for, request, session, flash, Response, send_file
from functools import wraps
from datetime import datetime
from app import app
from db import db
from app.models import Customer, Proposal, Roof, Product, Pln_tariff
from app.form_validations import validate_customer_form, validate_proposal_form, validate_product_form, validate_pln_tariff_form
from werkzeug.utils import secure_filename
from app.functions import allowed_file, add_gsa_report_to_db
# Adding encription key with Secret Key Variable for User Authentication
# from flask_weasyprint import HTML, render_pdf


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

def basicAuth(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if request.authorization['username'] == 'admin@admin.com':
            if request.authorization['password'] == 'admin':
                return f(*args, **kwargs)
            else:
                return redirect(url_for('login'))
        else:
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
        print(is_valid)
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
        'customers': table_data,
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


@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    if request.method == 'POST':
        is_valid = validate_product_form(request.form)
        print(is_valid)
        if 'errors' not in is_valid:
            timestamp = datetime.now().replace(microsecond=0)
            product = Product(**is_valid, created_at=timestamp, updated_at=timestamp)
            db.session.add(product)
            db.session.commit()
            flash('successfully added', category='success')
        else:
            flash(f'Error {is_valid}', category='danger')
    products = Product.query.order_by(Product.id).all()
    return render_template("products.html", products=products)


@app.route('/products/delete', methods=['POST'])
@login_required
def delete_product():
    id = request.form.get('id')
    product = Product.query.filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()
    return redirect('/products')


@app.route('/products/update', methods=['POST'])
@login_required
def edit_product():
    id = request.form.get('id')
    is_valid = validate_product_form(request.form)
    if 'errors' not in is_valid:
        product = Product.query.filter_by(id=id).first()
        product.update(**is_valid)
        db.session.commit()
        flash('Success update product', 'success')
    return redirect('/products')


@app.route('/pln_tariffs', methods=['GET', 'POST'])
@login_required
def pln_tariffs():
    if request.method == 'POST':
        is_valid = validate_pln_tariff_form(request.form)
        print(is_valid)
        if 'errors' not in is_valid:
            timestamp = datetime.now().replace(microsecond=0)
            pln_tariff = Pln_tariff(**is_valid, created_at=timestamp, updated_at=timestamp)
            db.session.add(pln_tariff)
            db.session.commit()
            flash('successfully added', category='success')
        else:
            flash(f'Error {is_valid}', category='danger')
    pln_tariffs = Pln_tariff.query.order_by(Pln_tariff.id).all()
    return render_template("pln-tariffs.html", pln_tariffs=pln_tariffs)


@app.route('/pln_tariffs/delete', methods=['POST'])
@login_required
def delete_pln_tariff():
    id = request.form.get('id')
    pln_tariff = Pln_tariff.query.filter_by(id=id).first()
    db.session.delete(pln_tariff)
    db.session.commit()
    return redirect('/pln_tariffs')


@app.route('/pln_tariffs/update', methods=['POST'])
@login_required
def edit_pln_tariff():
    id = request.form.get('id')
    is_valid = validate_pln_tariff_form(request.form)
    if 'errors' not in is_valid:
        pln_tariff = Pln_tariff.query.filter_by(id=id).first()
        pln_tariff.update(**is_valid)
        db.session.commit()
        flash('Success update PLN Tariff', 'success')
    return redirect('/pln_tariffs')


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
            if 'sketchup_model' in request.files:
                file = request.files['sketchup_model']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = app.config.get('UPLOAD_IMAGES_FOLDER') / filename
                    file.save(file_path)
                    is_valid.update({'sketchup_model' : file_path.relative_to(Path('app')).__str__()})
            proposal = Proposal(**is_valid, date_of_proposals=date_of_proposals, project_name=request.form.get('project_name'),proposal_no=request.form.get('proposal_no'), pln_tariff_id=int(request.form.get('pln_tariff')),created_at=timestamp, updated_at=timestamp,  status='Pending')
            db.session.add(proposal)
            db.session.commit()
            flash('successfully added', 'success')
            proposal_current = Proposal.query.filter_by(created_at=proposal.created_at).first()
            return redirect(f'/proposal-details/{proposal_current.id}')
    customers = Customer.query.order_by(Customer.id).all()
    pln_tariffs = Pln_tariff.query.order_by(Pln_tariff.id).all()
    return render_template("add-proposal.html", customers=customers, pln_tariffs=pln_tariffs)


@app.route('/proposal-details/<int:id>', methods=('POST','GET'))
@login_required
def proposaldetails(id):
    proposal = Proposal.query.filter_by(id=id).first()
    if proposal is None:
        return redirect('/proposals')
    customers = Customer.query.order_by(Customer.id).all()
    pln_tariffs = Pln_tariff.query.order_by(Pln_tariff.id).all()
    # print(proposal.__dict__)
    if request.method == 'POST':
        is_valid = validate_proposal_form(request.form)
        print('is_valid', is_valid)
        if 'errors' not in is_valid:
            print(request.files)
            if 'sketchup_model' in request.files:
                print("masuk")
                file = request.files['sketchup_model']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = app.config.get('UPLOAD_IMAGES_FOLDER') / filename
                    file.save(file_path)
                    is_valid.update({'sketchup_model' : file_path.relative_to(Path('app')).__str__()})
            proposal.update(**is_valid, project_name=request.form.get('project_name'), proposal_no=request.form.get('proposal_no'), location=request.form.get('location'), pv_system_model=request.form.get('pv_system_model'), pln_tariff_id=int(request.form.get('pln_tariff')))
            db.session.commit()
            flash('successfully updated', 'success')
            return redirect(f'/proposal-details/{id}')
    context = {
        'proposal' : proposal,
        'customers' : customers,
        'pln_tariffs' : pln_tariffs
    }
    return render_template("proposal-details.html", **context)


@app.route('/proposals/delete', methods=('POST',))
@login_required
def delete_proposal():
    id = request.form.get('id')
    proposal = Proposal.query.filter_by(id=id).first()
    db.session.delete(proposal)
    db.session.commit()
    return redirect('/proposals')


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
        for index,gsa_report in enumerate(request.files):
            file = request.files[f'gsa_report_file{index+1}']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = app.config.get('UPLOAD_FILES_FOLDER') / filename
                file.save(file_path)
                filepaths.append(file_path)
        s_data, proposal_data = add_gsa_report_to_db(filepaths)
    roofs_data = proposal_data.pop('roofs')
    for nums in range(1,proposal.num_of_roofs+1):
        data['pv_panel'] = request.form.get(f"pv_panel{nums}")
        data['pv_panel_qty'] = request.form.get(f"pv_panel_qty{nums}")
        data['pv_cable'] = request.form.get(f"pv_cable{nums}")
        data['add_construction_qty'] = request.form.get(f"add_construction_qty{nums}")
        data['add_construction_price'] = request.form.get(f"add_construction_price{nums}")
        data['azimuth'] = roofs_data[nums-1].get('azimuth')
        data['angle'] = roofs_data[nums-1].get('angle')
        data['gsa_report_file'] = filepaths[nums-1].relative_to(Path('app')).__str__()
        roof = Roof(**data, created_at=timestamp, updated_at=timestamp)
        roof.solar_data.extend(s_data[nums-1])
        roofs.append(roof)
    proposal.roofs.extend(roofs)
    print(request.form)
    proposal.geocoordinates = proposal_data.get('geocoordinates')
    proposal.location = proposal_data.get('location')
    proposal.pv_system_model = proposal_data.get('pv_system_model')
    proposal.inverter_stg3 = request.form.get('inverter_stg3')
    proposal.inverter_stg6 = request.form.get('inverter_stg6')
    proposal.inverter_stg20 = request.form.get('inverter_stg20')
    proposal.inverter_stg60 = request.form.get('inverter_stg60')
    proposal.inverter_stg125 = request.form.get('inverter_stg125')
    proposal.inverter_stg250 = request.form.get('inverter_stg250')
    proposal.energy_accounting_system = request.form.get('energy_accounting_system')
    proposal.transport_price = request.form.get('transport_price')
    proposal.installation_price = request.form.get('installation_price')
    proposal.discount = request.form.get('discount')
    db.session.add(proposal)
    db.session.add_all(roofs)
    db.session.commit()
    flash('successfully add roofs', category='success')
    return redirect(f'/proposal-details/{id}')


@app.route('/proposal-details/<int:id>/update', methods=("POST",))
@login_required
def update_order(id):
    data = {}
    roofs = []
    proposal = Proposal.query.filter_by(id=id).first()
    s_data = None
    if request.files:
        filepaths = []
        for index,gsa_report in enumerate(request.files):
            file = request.files[f'gsa_report_file{index+1}']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = app.config.get('UPLOAD_FILES_FOLDER') / filename
                file.save(file_path)
                filepaths.append(file_path)
                s_data, proposal_data = add_gsa_report_to_db(filepaths)
    for nums in range(1,proposal.num_of_roofs+1):
        data['pv_panel'] = request.form.get(f"pv_panel{nums}")
        data['pv_panel_qty'] = request.form.get(f"pv_panel_qty{nums}")
        data['pv_cable'] = request.form.get(f"pv_cable{nums}")
        data['add_construction_qty'] = request.form.get(f"add_construction_qty{nums}")
        data['add_construction_price'] = request.form.get(f"add_construction_price{nums}")
        data['azimuth'] = request.form.get(f"azimuth{nums}")
        data['angle'] = request.form.get(f"angle{nums}")
        print('proposals', len(proposal.roofs))
        print('sdata', s_data)
        proposal.roofs[nums-1].update(**data, gsa_report_file=s_data[nums-1]) if s_data is not None else proposal.roofs[nums-1].update(**data, gsa_report_file=None)
    proposal.inverter_stg3 = request.form.get('inverter_stg3')
    proposal.inverter_stg6 = request.form.get('inverter_stg6')
    proposal.inverter_stg20 = request.form.get('inverter_stg20')
    proposal.inverter_stg60 = request.form.get('inverter_stg60')
    proposal.inverter_stg125 = request.form.get('inverter_stg125')
    proposal.inverter_stg250 = request.form.get('inverter_stg250')
    proposal.energy_accounting_system = request.form.get('energy_accounting_system')
    proposal.transport_price = request.form.get('transport_price')
    proposal.installation_price = request.form.get('installation_price')
    proposal.discount = request.form.get('discount')
    db.session.commit()
    flash('successfully update roofs', category='success')
    return redirect(f'/proposal-details/{id}')

@app.route('/files/download')
@login_required
def download_excel():
    filepath = request.args.get('filepath')
    if filepath is None:
        return redirect('/proposals')
    return send_file(filepath, as_attachment=True)

@app.route('/user')
@login_required
def user():
    return render_template("user.html")


@app.route('/role')
@login_required
def register():
    return render_template("role.html")

@app.route('/proposal-report/<int:id>')
@login_required
def proposal_report(id):
    proposal = Proposal.query.filter_by(id=id).first()
    if proposal is None:
        return redirect('/proposals')
    if proposal.roofs:
        proposal.status = 'Completed'
        db.session.commit()
    else:
        return redirect(f'/proposal-details/{id}')
    proposal.calculate_monthly_data()
    yield_roof_total = proposal.yield_roof_total
    print(yield_roof_total)
    calendar = ['Jan', 'Feb', 'Mar', 'Apr','May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    value_to_kwh = [int((data*1550)/1000) for data in yield_roof_total]
    avg_energy_perhour = (np.array([data for data in list(map(sum, zip(*proposal.total_energy_perhour)))]) / proposal.num_of_roofs).tolist()
    total_energy_perhour = [e.tolist() for e in proposal.total_energy_perhour]
    # yield_per_roof = proposal.yield_roof
    context = {
        'customer' : proposal.customer,
        'proposal' : proposal,
        'date_of_prop' : proposal.date_of_proposals.strftime('%B %dth %Y'),
        'yearly_chart' : zip(calendar,yield_roof_total, value_to_kwh, [i for i in range(1,13)]),
        'yearly_total' : [sum(yield_roof_total), sum(value_to_kwh)],
        'daily_chart' : total_energy_perhour,
        'avg_daily' : avg_energy_perhour,
    }
    return render_template('proposal-report.html', **context)

