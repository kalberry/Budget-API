import mysql.connector
import json
import os

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
        password_hash varchar(80) NOT NULL, \
        starting_pay_date varchar(80) NOT NULL, \
        pay_frequency int(10), \
        pay_dates varchar(80) NOT NULL, \
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
        category varchar(80) NOT NULL, \
        user_id int(11) NOT NULL,
        PRIMARY KEY (id) \
        ) \
        ''')

        cur.execute('''CREATE TABLE IF NOT EXISTS pay_period_expenses \
        ( \
        id int(11) NOT NULL AUTO_INCREMENT, \
        name varchar(80) NOT NULL, \
        cost float(11) NOT NULL, \
        category varchar(80) NOT NULL, \
        user_id int(11) NOT NULL,
        PRIMARY KEY (id) \
        ) \
        ''')

        cur.close()
        con.close()

    def add_bill(self, bill):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        data = (bill.name, bill.cost, bill.due_date, bill.last_paid, bill.category)
        sql = '''INSERT INTO bills (name, cost, due_date, last_paid, category) \
        VALUES (%s, %s, %s, %s, %s)'''

        cur.execute(sql, data)
        con.commit()

        cur.close()
        con.close()

    def get_bills(self, *args, **kwargs):
        bills = []
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        if (args is None):
            sql = '''SELECT * FROM bills'''
            cur.execute(sql)
        elif "user_id" in args[0].keys():
            sql = '''SELECT * FROM bills WHERE user_id = %s'''
            data = (args[0]['user_id'], )
            cur.execute(sql, data)
        elif "id" in args[0].keys():
            sql = '''SELECT * FROM bills WHERE id = %s'''
            data = (args[0]['id'], )
            cur.execute(sql, data)

        return cursor_to_bills(cur)

    def get_users(self, *args, **kwargs):
        users = []

        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()

        if (args == ()):
            sql = '''SELECT * FROM users'''
            cur.execute(sql)
        elif "id" in args[0].keys():
            sql = '''SELECT * FROM users WHERE id = %s'''
            data = (args[0]['id'], )
            cur.execute(sql, data)

        users = self.cursor_to_user(cur)

        return users

    def register_user(self, email, password_hash, starting_pay_date, pay_frequency, pay_dates):
        con = mysql.connector.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD, host='127.0.0.1', database='budget')
        cur = con.cursor()
        self.email = email
        self.password_hash = password_hash
        self.starting_pay_date = starting_pay_date
        self.pay_frequency = pay_frequency
        self.pay_dates = pay_dates

        sql = '''SELECT * FROM users WHERE email=%s LIMIT 1'''
        data = (email, )
        cur.execute(sql, data)

        user = self.cursor_to_user(cur)

        print(user)
        if (user != []):
            return {}
        else:
            sql = '''INSERT INTO users (email, password_hash, starting_pay_date, pay_frequency, pay_dates) VALUES (%s, %s, %s, %s, %s); '''
            data = (email, password_hash, starting_pay_date, pay_frequency, str(pay_dates))
            cur.execute(sql, data)
            con.commit()
            sql = '''SELECT * FROM users WHERE email=%s LIMIT 1;'''
            data = (email, )
            cur.execute(sql, data)
            user = self.cursor_to_user(cur)
            return user

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

    def cursor_to_user(self, cur):
        users = []
        for (id, email, password_hash, starting_pay_date, pay_frequency, pay_dates) in cur:
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
            "starting_pay_date": starting_pay_date,
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
    def __init__(self, id, email, password_hash, starting_pay_date, pay_frequency, pay_dates):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.starting_pay_date = starting_pay_date
        self.pay_frequency = pay_frequency
        self.pay_dates = pay_dates

    def __repr__(self):
        return '<User %r>' % self.username


class Bill:
    def __init__(self, user_id, name, cost, due_date, frequency, last_paid, category):
        self.user_id = user_id
        self.name = name
        self.cost = cost
        self.due_date = due_date
        self.frequency = frequency
        self.last_paid = last_paid
        self.category = category

    def __repr__(self):
        return '<User %r>' % self.username
