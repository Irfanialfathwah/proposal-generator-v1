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
    return {**form}