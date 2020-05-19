import mysql.connector
import json
import os
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash

class Database:
    DB_USERNAME = os.environ['DB_USERNAME']
    DB_PASSWORD = os.environ['DB_PASSWORD']

    def create_tables(self):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        # Comment out in production
        cur.execute("DROP TABLE IF EXISTS pay_period_expenses")
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("DROP TABLE IF EXISTS bills")

        cur.execute('''CREATE TABLE IF NOT EXISTS users \
        ( \
        id int(11) NOT NULL AUTO_INCREMENT, \
        email varchar(80) NOT NULL UNIQUE, \
        password_hash varchar(160) NOT NULL, \
        last_pay_date varchar(80) NOT NULL, \
        pay_frequency int(10), \
        pay_dates varchar(80), \
        PRIMARY KEY (id) \
        ) \
        ''')

        cur.execute('''CREATE TABLE IF NOT EXISTS bills \
        ( \
        id int(11) NOT NULL AUTO_INCREMENT, \
        name varchar(80) NOT NULL, \
        cost float(11) NOT NULL, \
        due_date varchar(15), \
        frequency int(10), \
        last_paid varchar(15) NOT NULL, \
        category varchar(80), \
        user_id int(11) NOT NULL,
        PRIMARY KEY (id) \
        ) \
        ''')

        cur.execute('''CREATE TABLE IF NOT EXISTS pay_period_expenses \
        ( \
        id int(11) NOT NULL AUTO_INCREMENT, \
        name varchar(80) NOT NULL, \
        cost float(11) NOT NULL, \
        category varchar(80), \
        user_id int(11) NOT NULL,
        PRIMARY KEY (id) \
        ) \
        ''')

        cur.close()
        con.close()

    def add_bill(self, bill):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        data = (bill.name, bill.cost, bill.due_date, bill.last_paid, bill.category, bill.user_id)
        sql = '''INSERT INTO bills (name, cost, due_date, last_paid, category, user_id) \
        VALUES (%s, %s, %s, %s, %s, %s)'''

        cur.execute(sql, data)
        con.commit()

        cur.close()
        con.close()

    def get_bills(self, id=None, user_id=None):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        if id and not user_id:
            sql = '''SELECT * FROM bills WHERE id=%s'''
            data = (id,)
            cur.execute(sql, data)
            bill = self.cursor_to_bills(cur)
            con.close()
            cur.close()
            return bill
        elif not id and user_id:
            sql = '''SELECT * FROM bills WHERE user_id=%s'''
            data = (user_id,)
            cur.execute(sql, data)
            bill = self.cursor_to_bills(cur)
            con.close()
            cur.close()
            return bill
        elif id and user_id:
            sql = '''SELECT * FROM bills WHERE id=%s AND user_id=%s'''
            data = (id, user_id)
            cur.execute(sql, data)
            bill = self.cursor_to_bills(cur)
            con.close()
            cur.close()
            return bill
        else:
            sql = '''SELECT * FROM bills'''
            cur.execute(sql,)
            bill = self.cursor_to_bills(cur)
            con.close()
            cur.close()
            return bill

    def get_bills_by_user_id_range(self, user_id, start, end):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        sql = '''SELECT * FROM bills WHERE user_id=%s AND due_date BETWEEN %s AND %s'''
        data = (user_id, start, end)
        cur.execute(sql, data)
        bill = self.cursor_to_bills(cur)
        con.close()
        cur.close()
        return bill

    def get_bills_by_frequency(self, user_id):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        sql = '''SELECT * FROM bills WHERE user_id=%s AND frequency IS NOT NULL'''
        data = (user_id,)
        cur.execute(sql, data)
        bill = self.cursor_to_bills(cur)
        con.close()
        cur.close()
        return bill

    def get_users(self, id=None):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        if id:
            sql = '''SELECT * FROM users WHERE id = %s'''
            data = (id, )
            cur.execute(sql, data)
            user = self.cursor_to_user(cur)
            cur.close()
            con.close()
            return user
        else:
            sql = '''SELECT * FROM users'''
            cur.execute(sql,)
            res = cur.fetchall()
            users = self.tuple_to_user(res)
            cur.close()
            con.close()
            return users

    def register_user(self, email, password_hash, last_pay_date, pay_frequency, pay_dates):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        self.email = email
        self.password_hash = password_hash
        self.last_pay_date = last_pay_date
        self.pay_frequency = pay_frequency
        self.pay_dates = pay_dates
        if pay_dates is not None:
            pay_dates_int = json.dumps(list(map(int, pay_dates)))
        else:
            pay_dates_int = None

        sql = '''SELECT * FROM users WHERE email=%s LIMIT 1'''
        data = (email, )
        cur.execute(sql, data)

        user = self.cursor_to_user(cur)

        if (user != []):
            cur.close()
            con.close()
            return {}
        else:
            sql = '''INSERT INTO users (email, password_hash, last_pay_date, pay_frequency, pay_dates) VALUES (%s, %s, %s, %s, %s); '''
            data = (email, password_hash, last_pay_date, pay_frequency, pay_dates_int)
            cur.execute(sql, data)
            con.commit()
            sql = '''SELECT * FROM users WHERE email=%s LIMIT 1;'''
            data = (email, )
            cur.execute(sql, data)
            user = self.cursor_to_user(cur)

            cur.close()
            con.close()
            return user

    def login_user(self, email, password):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        self.email = email
        self.password = password

        sql = '''SELECT * FROM users WHERE email=%s LIMIT 1'''
        data = (email,)
        cur.execute(sql, data)

        user = self.cursor_to_user(cur)
        if user is []:
            return []
        cur.close()
        con.close()
        if (check_password_hash(user[0]['password_hash'], password)):
            return user
        else:
            return []

    def update_user(self, id, email=None, password_hash=None, last_pay_date=None, pay_frequency=None, pay_dates=None):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        if pay_dates is not None:
            pay_dates_int = json.dumps(list(map(int, pay_dates)))
        else:
            pay_dates_int = None

        if email:
            sql = '''UPDATE users SET email=%s WHERE id=%s '''
            data = (email, id)
            cur.execute(sql, data)
            con.commit()
        if password_hash:
            sql = '''UPDATE users SET password_hash=%s WHERE id=%s '''
            data = (password_hash, id)
            cur.execute(sql, data)
            con.commit()
        if last_pay_date:
            sql = '''UPDATE users SET last_pay_date=%s WHERE id=%s '''
            data = (last_pay_date, id)
            cur.execute(sql, data)
            con.commit()
        if pay_frequency:
            sql = '''UPDATE users SET pay_frequency=%s WHERE id=%s '''
            data = (pay_frequency, id)
            cur.execute(sql, data)
            con.commit()
        if pay_dates:
            sql = '''UPDATE users SET pay_dates=%s WHERE id=%s '''
            data = (pay_dates_int, id)
            cur.execute(sql, data)
            con.commit()

    def delete_bill(self, id):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        sql = '''DELETE FROM bills WHERE id=%s'''
        data = (id,)

        cur.execute(sql, data)
        con.commit()

        cur.close()
        con.close()

    def delete_pay_period_expense(self, id):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        sql = '''DELETE FROM pay_period_expenses WHERE id=%s'''
        data = (id,)

        cur.execute(sql, data)
        con.commit()

        cur.close()
        con.close()

    def delete_user(self, id):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        sql = '''DELETE FROM users WHERE id=%s'''
        data = (id,)

        cur.execute(sql, data)
        con.commit()

        cur.close()
        con.close()

    def add_pay_period_expense(self, name, cost, user_id, category=None):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        sql = '''INSERT INTO pay_period_expenses (name, cost, category, user_id) VALUES (%s, %s, %s, %s)'''
        data = (name, cost, category, user_id)

        cur.execute(sql, data)
        con.commit()

        cur.close()
        con.close()

    def get_pay_period_expenses(self, id=None, user_id=None):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        if id and not user_id:
            sql = '''SELECT * FROM pay_period_expenses WHERE id=%s'''
            data = (id,)
            cur.execute(sql, data)
            ppe = self.cursor_to_pay_period_expenses(cur)
            con.close()
            cur.close()
            return ppe
        elif not id and user_id:
            sql = '''SELECT * FROM pay_period_expenses WHERE user_id=%s'''
            data = (user_id,)
            cur.execute(sql, data)
            ppe = self.cursor_to_pay_period_expenses(cur)
            con.close()
            cur.close()
            return ppe
        elif id and user_id:
            sql = '''SELECT * FROM pay_period_expenses WHERE id=%s AND user_id=%s'''
            data = (id, user_id)
            cur.execute(sql, data)
            ppe = self.cursor_to_pay_period_expenses(cur)
            con.close()
            cur.close()
            return ppe
        else:
            sql = '''SELECT * FROM pay_period_expenses'''
            cur.execute(sql,)
            ppe = self.cursor_to_pay_period_expenses(cur)
            con.close()
            cur.close()
            return ppe

    def update_pay_period_expense(self, id, name=None, cost=None, category=None):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        if (name):
            sql = '''UPDATE pay_period_expenses SET name=%s WHERE id=%s '''
            data = (name, id)
            cur.execute(sql, data)
            con.commit()
        if (cost):
            sql = '''UPDATE pay_period_expenses SET cost=%s WHERE id=%s '''
            data = (cost, id)
            cur.execute(sql, data)
            con.commit()
        if (category):
            sql = '''UPDATE pay_period_expenses SET category=%s WHERE id=%s '''
            data = (category, id)
            cur.execute(sql, data)
            con.commit()

        cur.close()
        con.close()

    def update_bill(self, id, name=None, cost=None, category=None):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        if (name):
            sql = '''UPDATE bills SET name=%s WHERE id=%s '''
            data = (name, id)
            cur.execute(sql, data)
            con.commit()
        if (cost):
            sql = '''UPDATE bills SET cost=%s WHERE id=%s '''
            data = (cost, id)
            cur.execute(sql, data)
            con.commit()
        if (category):
            sql = '''UPDATE bills SET category=%s WHERE id=%s '''
            data = (category, id)
            cur.execute(sql, data)
            con.commit()

        cur.close()
        con.close()

    def get_budget_schedule(self, user_id, count=24):
        budget_schedule = []
        user = self.get_users(id=user_id)
        if user != []:
            user_data = user[0]
        else:
            return []
        pay_date = datetime.strptime(user_data['last_pay_date'], '%m/%d/%Y').date()

        for i in range(int(count)):
            bills = []
            end_pay_date = pay_date + timedelta(days=13)

            pay_period_expenses = self.get_pay_period_expenses(user_id=user_data['id'])

            bills = bills + self.get_bills_by_user_id_range(user_id=user_data['id'], start=pay_date.day, end=end_pay_date.day)
            bills = bills + self.get_bills_by_frequency(user_id=user_data['id'])

            budget_schedule.append({
            "pay_date": str(pay_date),
            "end_pay_date": str(end_pay_date),
            "pay_period_expenses": pay_period_expenses,
            "bills": bills
            })

            pay_date = end_pay_date + timedelta(days=1)

        return budget_schedule

    def cursor_to_pay_period_expenses(self, cur):
        ppe = []
        for (id, name, cost, category, user_id) in cur:
            ppe.append({
            "id": id,
            "name": name,
            "cost": cost,
            "category": category,
            "user_id": user_id
            })
        return ppe

    def tuple_to_user(self, user_tuple_list):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        users = []
        for user_tuple in user_tuple_list:
            id = user_tuple[0]
            email = user_tuple[1]
            password_hash = user_tuple[2]
            last_pay_date = user_tuple[3]
            pay_frequency = user_tuple[4]
            pay_dates = user_tuple[5]

            if pay_dates is not None:
                pay_dates = json.loads(user_tuple[5])
            else:
                pay_dates = None

            sql = '''SELECT * FROM bills WHERE user_id=%s'''
            data = (id, )
            cur.execute(sql, data)
            bills = self.cursor_to_bills(cur)

            sql = '''SELECT * FROM pay_period_expenses WHERE user_id=%s'''
            data = (id, )
            cur.execute(sql, data)
            pay_period_expenses = self.cursor_to_pay_period_expenses(cur)

            users.append({
            "id": id,
            "email": email,
            "last_pay_date": last_pay_date,
            "pay_frequency": pay_frequency,
            "pay_dates": pay_dates,
            "bills": bills,
            "pay_period_expenses": pay_period_expenses
            })

        con.close()
        cur.close()
        return users

    def cursor_to_user(self, cur):
        users = []
        for (id, email, password_hash, last_pay_date, pay_frequency, pay_dates) in cur:
            sql = '''SELECT * FROM bills WHERE user_id=%s'''
            data = (id, )
            cur.execute(sql, data)
            bills = self.cursor_to_bills(cur)

            sql = '''SELECT * FROM pay_period_expenses WHERE user_id=%s'''
            data = (id, )
            cur.execute(sql, data)
            pay_period_expenses = self.cursor_to_pay_period_expenses(cur)

            if pay_dates is not None:
                pay_dates = json.loads(pay_dates)
            else:
                pay_dates = None

            users.append({
            "id": id,
            "email": email,
            "password_hash": password_hash,
            "last_pay_date": last_pay_date,
            "pay_frequency": pay_frequency,
            "pay_dates": pay_dates,
            "bills": bills,
            "pay_period_expenses": pay_period_expenses
            })
        return users

    def cursor_to_bills(self, cur):
        bills = []
        for (id, name, cost, due_date, frequency, last_paid, category, user_id) in cur:
            bills.append({
            "id": id,
            "name": name,
            "cost": cost,
            "due_date": due_date,
            "frequency": frequency,
            "last_paid": last_paid,
            "category": category,
            "user_id": user_id
            })
        return bills

class User:
    def __init__(self, id, email, password_hash, last_pay_date, pay_frequency, pay_dates):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.last_pay_date = last_pay_date
        self.pay_frequency = pay_frequency
        self.pay_dates = pay_dates

    def __repr__(self):
        return '<User %r>' % self.username

class Bill:
    def __init__(self, user_id, name, cost, last_paid, category, due_date=None, frequency=None):
        self.user_id = user_id
        self.name = name
        self.cost = cost
        self.due_date = due_date
        self.frequency = frequency
        self.last_paid = last_paid
        self.category = category

    def __repr__(self):
        return '<User %r>' % self.username
