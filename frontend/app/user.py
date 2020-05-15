from flask_login import UserMixin
from app import login
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import json

HOST = 'https://127.0.0.1:5000'

@login.user_loader
def load_user(id):
    payload = {"id": id}
    user_data = requests.get(HOST + '/api/v1/users', params=payload)
    print(user_data)
    user = User(user_data)
    if user:
        return user
    else:
        return None

def login_user(self, email, password):
    payload = {'email': email, 'password_hash': generate_password_hash(password)}
    user_data = requests.post(HOST + '/api/v1/auth/login', params=payload)


class User(UserMixin, user_data):
    pay_period_expenses = []


    id = json.dumps(user_data['id'])
    email = json.dumps(user_data['email'])
    password_hash = json.dumps(user_data['password_hash'])
    last_pay_date = json.dumps(user_data['last_pay_date'])
    pay_frequency = json.dumps(user_data['pay_frequency'])
    pay_dates = json.dumps(user_data['pay_dates'])
    bills = get_bills(user_data)

    def get_bills(self, user_data):
        ret_bills = []
        for bill in user_data['bills']:
            ret_bills.append(Bill(bill))

    def get_pay_period_expenses(self, user_data):
        ret_ppe = []
        for ppe in user_data['pay_period_expenses']:
            ret_bills.append(PayPeriodExpense(ppe))


class Bill(bill_data):
    pass

class PayPeriodExpense(ppe_data)
