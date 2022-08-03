import logging

from flask import Flask, request, jsonify

from services import exchange, transactions

currencies = ['EUA', 'USD', 'BRL', 'JPY']

app = Flask(__name__)


@app.get('/transactions')
def get_transactions():
    logging.debug('Get transactions')
    request_data = get_request_data()
    logging.debug(f'Request data: {request_data}')
    valid = validate_user_id(request_data)
    if not valid[0]:
        return bad_request_error(valid[1])
    else:
        return jsonify(transactions(request_data['user_id']))


@app.get('/convert')
def convert():
    logging.debug('Convert')
    request_data = get_request_data()
    logging.debug(f'Request data: {request_data}')
    valid = validate(request_data)
    if not valid[0]:
        return bad_request_error(valid[1])
    else:
        return exchange(request_data)


def get_request_data():
    return {'user_id': request.args.get('user_id', ''),
            'amount': request.args.get('amount', ''),
            'source': request.args.get('source', '').upper(),
            'target': request.args.get('target', '').upper()}


def validate_user_id(resquest_data):
    errors = []
    if resquest_data['user_id'] == '':
        errors.append('user_id is required')
    return len(errors) == 0, errors


def validate(resquest_data):
    errors = validate_user_id(resquest_data)[1]

    if resquest_data['amount'] == '':
        errors.append('amount is required')
    else:
        try:
            resquest_data['amount'] = float(resquest_data['amount'])
        except ValueError:
            errors.append(f'amount: Value {resquest_data["amount"]} is invalid')

    if resquest_data['source'] == '':
        errors.append('source is required')
    elif resquest_data['source'] not in currencies:
        errors.append(f'source: Value {resquest_data["source"]} is invalid. Valid values: {currencies}')

    if resquest_data['target'] == '':
        errors.append('target is required')
    elif resquest_data['target'] not in currencies:
        errors.append(f'target: Value {resquest_data["target"]} is invalid. Valid values: {currencies}')

    return len(errors) == 0, errors


def error(message, details, http_status):
    resp = {'message': message, 'details': details, 'status': http_status}
    return resp, http_status


def bad_request_error(errors):
    return error('Invalid request', errors, 400)
