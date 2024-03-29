import re

def validate_customer_form(form):
    errors = {}
    name = form.get('name')
    email = form.get('email')
    phone_number = form.get('phone_number')
    address = form.get('address')

    if len(name) > 30:
        errors.update({'name' : 'name length must not exceed 30 char'})
    if len(email) > 50:
        errors.update({'email': 'email length must not exceed 50 char'})
    if len(address) > 80:
        errors.update({'address': 'address length must not exceed 80 char'})
    if len(phone_number) > 18:
        errors.update({'phone_number': 'phone_number length must not exceed 18 char'})

    if errors:
        return {
            'errors': errors
        }
    return {
        "name":name,
        "email": email,
        "phone_number": phone_number,
        "address":address
    }

def validate_proposal_form(form):
    errors = {}

    customer_id = form.get('customer')
    num_of_roofs = form.get('num_of_roofs')
    # location = form.get('location')
    # geocoordinates = form.get('geocoordinates')

    return {
        'num_of_roofs': num_of_roofs,
        # 'location' : location,
        # 'geocoordinates' : geocoordinates,
        'customer_id': customer_id
    }

def validate_product_form(form):
    errors = {}

    product_name = form.get('product_name')
    unit = form.get('unit')
    std_price = int(form.get('std_price').replace(",",""))

    return {
        'product_name': product_name,
        'unit': unit,
        'std_price': std_price
    }

def validate_pln_tariff_form(form):
    errors = {}

    pln_tariff_group = form.get('pln_tariff_group')
    power_limit = form.get('power_limit')
    pln_price = form.get('pln_price')
    
    return {
        'pln_tariff_group': pln_tariff_group,
        'power_limit': power_limit,
        'pln_price': pln_price
    }

def validate_bid_form(form):
    errors = {}

    number = form.get('number')
    customer_id = form.get('customer')
    proposal_id = form.get('project_name')

    return {
        'number': number,
        'customer_id': customer_id,
        'proposal_id': proposal_id
    }