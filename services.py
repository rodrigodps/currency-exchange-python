from datetime import datetime

import gateway
from database import insert, transactions_by_user


def exchange(request_data):
    ex = gateway.exchange(request_data['source'], request_data['target'], True)
    currency = ex['rates'][request_data['target']]
    request_data['currency'] = currency
    request_data['date'] = datetime.today()
    trans_id = insert(request_data)
    return {'id': trans_id,
            'user_id': request_data['user_id'],
            'source_currency': request_data['source'],
            'source_amount': request_data['amount'],
            'target_currency': request_data['target'],
            'target_amount': request_data['amount'] * currency,
            'currency': currency,
            'date': request_data['date']}


def transactions(user_id):
    return transactions_by_user(user_id)
