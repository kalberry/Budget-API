from flask_login import UserMixin
from app import login
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime

HOST = 'https://127.0.0.1:5000'

@login.user_loader
def load_user(id):
    print('loading user ', id)
    payload = {"id": id}
    user_data = requests.get(HOST + '/api/v1/users', params=payload, verify=False)
    if user_data.status_code == 200:
        if 'data' in user_data.json():
            user = User(user_data.json()['data'][0])
        if user:
            return user
        else:
            return None
    else:
        return None

def check_user(email, password):
    print('logging in user')
    payload = {'email': email, 'password': password}
    user_data = requests.post(HOST + '/api/v1/auth/login', params=payload, verify=False)
    if user_data.status_code == 200:
        print('check user ', user_data)
        if 'data' in user_data.json():
            user = User(user_data.json()['data'][0])
        if user:
            return user
        else:
            return None
    else:
        return None

def register_user(email, password, last_pay_date, pay_frequency, pay_dates):
    password_hash = generate_password_hash(password)

    for date in pay_dates:
        if date == '':
            pay_dates = None

    payload = {
    'email': email,
    'password_hash': password_hash,
    'last_pay_date': last_pay_date,
    'pay_frequency': pay_frequency,
    'pay_dates': pay_dates
    }
    user_data = requests.post(HOST + '/api/v1/auth/register', params=payload, verify=False)
    if user_data.status_code == 201:
        if 'data' in user_data.json():
            user = User(user_data.json()['data'][0])
        if user:
            return user
        else:
            return None
    else:
        return None

def add_bill(user_id, name, cost, due_date, frequency, last_paid, category):
    payload = {
    'user_id': user_id,
    'name': name,
    'cost': cost,
    'due_date': due_date,
    'frequency': frequency,
    'last_paid': last_paid,
    'category': category
    }

    bill_data = requests.post(HOST + '/api/v1/bills', params=payload, verify=False)
    if bill_data.status_code == 201:
        return True
    else:
        return None

def find_bill(id, bills):
    for bill in bills:
        if int(bill.id) == int(id):
            return bill

def update_bill(id, name, cost, due_date, frequency, last_paid, category):
    payload = {
    'id': id,
    'name': name,
    'cost': cost,
    'due_date': due_date,
    'frequency': frequency,
    'last_paid': last_paid,
    'category': category
    }

    bill_data = requests.put(HOST + '/api/v1/bills', params=payload, verify=False)
    if bill_data.status_code == 200:
        return True
    else:
        return False

def find_ppe(id, ppes):
    for ppe in ppes:
        if int(ppe.id) == int(id):
            return ppe

def update_ppe(id, name, cost, category):
    payload = {
    'id': id,
    'name': name,
    'cost': cost,
    'category': category
    }

    ppe_data = requests.put(HOST + '/api/v1/ppe', params=payload, verify=False)
    if ppe_data.status_code == 200:
        return True
    else:
        return False

def add_pay_period_expense(user_id, name, cost, category):
    payload = {
    'user_id': user_id,
    'name': name,
    'cost': cost,
    'category': category
    }

    ppe_data = requests.post(HOST + '/api/v1/ppe', params=payload, verify=False)
    if ppe_data.status_code == 201:
        return True
    else:
        return None

def get_budget_schedule(user_id, count=None):
    payload = {
    'user_id': user_id,
    'count': count
    }

    budget_schedule_data = requests.get(HOST + '/api/v1/bidget-schedule', params=payload, verify=False)
    if budget_schedule_data.status_code == 200:
        return budget_schedule_data.json()
    else:
        return None

class User(UserMixin):
    def __init__(self, user_data):
        data = user_data

        self.id = data['id']
        self.email = data['email']
        self.password_hash = data['password_hash']
        self.last_pay_date = data['last_pay_date']
        self.pay_frequency = data['pay_frequency']
        self.pay_dates = data['pay_dates']
        self.bills = self.get_bills(data)
        self.pay_period_expenses = self.get_pay_period_expenses(data)
        self.budget_schedule = self.get_budget_schedule()

    def get_bills(self, data):
        self.ret_bills = []
        for bill in data['bills']:
            print(bill)
            self.ret_bills.append(Bill(bill))
        return self.ret_bills

    def get_pay_period_expenses(self, data):
        self.ret_ppe = []
        for ppe in data['pay_period_expenses']:
            self.ret_ppe.append(PayPeriodExpense(ppe))
        return self.ret_ppe

    def get_budget_schedule(self):
        payload = {
        'id': self.id,
        'count': 24
        }
        budget_schedule_data = requests.get(HOST + '/api/v1/budget-schedule', params=payload, verify=False)
        if budget_schedule_data.status_code == 200:
            pay_periods = []
            for pay_period_data in budget_schedule_data.json()['data']:
                print(pay_period_data)
                pay_periods.append(PayPeriod(pay_period_data))
            return pay_periods
        else:
            return None

    def get_id(self):
        return self.id


class Bill:
    def __init__(self, bill_data):
        self.id = bill_data['id']
        self.name = bill_data['name']
        self.cost = bill_data['cost']
        self.due_date = bill_data['due_date']
        self.frequency = bill_data['frequency']
        self.last_paid = bill_data['last_paid']
        self.category = bill_data['category']

class PayPeriodExpense:
    def __init__(self, ppe_data):
        self.id = ppe_data['id']
        self.name = ppe_data['name']
        self.cost = ppe_data['cost']
        self.category = ppe_data['category']

class PayPeriod:
    def __init__(self, data):
        self.pay_date = datetime.strptime(data['pay_date'], '%Y-%m-%d').strftime('%m/%d/%Y')
        print(type(self.pay_date))
        self.end_pay_date = datetime.strptime(data['end_pay_date'], '%Y-%m-%d').strftime('%m/%d/%Y')
        self.pay_period_expenses = self.get_pay_period_expenses(data['pay_period_expenses'])
        self.bills = self.get_bills(data['bills'])

    def get_pay_period_expenses(self, data):
        self.ret_ppe = []
        for ppe in data:
            self.ret_ppe.append(PayPeriodExpense(ppe))
        return self.ret_ppe

    def get_bills(self, data):
        self.ret_bills = []
        for bill in data:
            print(bill)
            self.ret_bills.append(Bill(bill))
        return self.ret_bills
