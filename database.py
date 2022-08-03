import os
import sqlite3

db_filename = 'currency-exchange.db'
schema_filename = 'currency-exchange_schema.sql'


def get_database_dir():
    database_dir = os.getenv('DATABASE_DIR', 'db')
    if not database_dir.endswith('/'):
        database_dir += '/'
    return database_dir


def get_connection():
    database = get_database_dir() + db_filename
    schema = get_database_dir() + schema_filename
    db_is_new = not os.path.exists(database)
    with sqlite3.connect(database) as conn:
        if db_is_new:
            print('Creating schema')
            try:
                with open(schema, 'rt') as f:
                    schema_script = f.read()
            except FileNotFoundError:
                print('Database schema not found!')
            else:
                conn.executescript(schema_script)
        return conn


def insert(trans):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'insert into exchange_transaction(user_id, currency_source, amount_source, currency_target, currency, date) '
        'values(?, ?, ?, ?, ?, ?)',
        (trans['user_id'], trans['source'], trans['amount'], trans['target'], trans['currency'], trans['date']))
    conn.commit()
    return cursor.lastrowid


def transactions_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'select id, user_id, currency_source, amount_source, currency_target, currency, date from '
        'exchange_transaction where user_id = ?', (user_id,))
    transactions = []
    for transaction_id, user_id, source, amount, target, currency, date in cursor.fetchall():
        transactions.append({'id': transaction_id,
                             'user_id': user_id,
                             'source_currency': source,
                             'source_amount': amount,
                             'target_currency': target,
                             'target_amount': amount * currency,
                             'currency': currency,
                             'date': date})
    return transactions
