import mysql.connector
import json

class Database:
    def create_tables(self):
        con = mysql.connector.connect(user='root', password='123456789', host='127.0.0.1', database='budget')
        cur = con.cursor()

        # Comment out in production
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("DROP TABLE IF EXISTS bills")

        cur.execute('''CREATE TABLE IF NOT EXISTS users \
        ( \
        id int(11) NOT NULL AUTO_INCREMENT, \
        email varchar(80) NOT NULL, \
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
        PRIMARY KEY (id) \
        ) \
        ''')

        cur.close()
        con.close()

    def add_bill(self, bill):
        con = mysql.connector.connect(user='root', password='123456789', host='127.0.0.1', database='budget')
        cur = con.cursor()

        data = (bill.name, bill.cost, bill.due_date, bill.last_paid, bill.category)
        sql = '''INSERT INTO bills (name, cost, due_date, last_paid, category) \
        VALUES (%s, %s, %s, %s, %s)'''

        cur.execute(sql, data)
        con.commit()

        cur.close()
        con.close()

    def get_bills(self):
        bills = []
        con = mysql.connector.connect(user='root', password='123456789', host='127.0.0.1', database='budget')
        cur = con.cursor()

        sql = '''SELECT * FROM bills'''

        cur.execute(sql)

        for (id, name, cost, due_date, frequency, last_paid, category) in cur:
            bills.append({
            "id": id,
            "name": name,
            "cost": cost,
            "due_date": due_date,
            "frequency": frequency,
            "last_paid": last_paid,
            "category": category
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
