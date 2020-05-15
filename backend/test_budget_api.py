import unittest
from budget_api import app, db

class TestSample(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG']
        self.app = app.test_client()
        db.create_tables()

    def test_index(self):
        response = self.app.get('/api/v1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    ## HELPERS
    def register(self, email, password, last_pay_date, pay_frequency=None, pay_dates=None):
        return self.app.post('/api/v1/auth/register',\
        data=dict(email=email, password_hash=password, last_pay_date=last_pay_date, pay_frequency=pay_frequency, pay_dates=pay_dates),\
        follow_redirects=True \
        )

    def login(self, email, password):
        return self.app.post('/api/v1/auth/login',\
        data=dict(email=email, password_hash=password),\
        follow_redirects=True \
        )

    def update_user_email(self, id, email):
        return self.app.put('/api/v1/users',\
        data=dict(id=id, email=email),\
        follow_redirects=True \
        )

    def update_user_password(self, id, password):
        return self.app.put('/api/v1/users',\
        data=dict(id=id, password_hash=password),\
        follow_redirects=True \
        )

    def update_user_last_pay_date(self, id, last_pay_date):
        return self.app.put('/api/v1/users',\
        data=dict(id=id, last_pay_date=last_pay_date),\
        follow_redirects=True \
        )

    def update_user_pay_frequency(self, id, pay_frequency):
        return self.app.put('/api/v1/users',\
        data=dict(id=id, pay_frequency=pay_frequency),\
        follow_redirects=True \
        )

    def update_user_pay_dates(self, id, pay_dates):
        url = '/api/v1/users?'
        if pay_dates is not None:
            for i in pay_dates:
                url += '&pay_dates=' + str(i)
        url += '&id=' + str(id)

        return self.app.put(url, follow_redirects=True)

    def get_user(self, id):
        return self.app.get('/api/v1/users',\
        data=dict(id=id),\
        follow_redirects=True \
        )

    def get_users(self):
        return self.app.get('/api/v1/users', follow_redirects=True)

    def add_bill(self, user_id, name, cost, last_paid, due_date=None, frequency=None, category=None):
        return self.app.post('/api/v1/bills',\
        data=dict(user_id=user_id, name=name, cost=cost, due_date=due_date, frequency=frequency, last_paid=last_paid, category=category),\
        follow_redirects=True \
        )

    def get_bills(self, id=None, user_id=None):
        data = {}
        if id:
            data['id'] = id
        if user_id:
            data['user_id'] = user_id
        if not id and not user_id:
            return self.app.get('/api/v1/bills', follow_redirects=True)
        return self.app.get('/api/v1/bills', data=dict(id=id, user_id=user_id), follow_redirects=True)

    def update_bill_name(self, id, name):
        return self.app.put('/api/v1/bills',\
        data=dict(id=id, name=name),\
        follow_redirects=True \
        )

    def update_bill_cost(self, id, cost):
        return self.app.put('/api/v1/bills',\
        data=dict(id=id, cost=cost),\
        follow_redirects=True \
        )

    def update_bill_category(self, id, category):
        return self.app.put('/api/v1/bills',\
        data=dict(id=id, category=category),\
        follow_redirects=True \
        )

    def delete_bill(self, id):
        return self.app.delete('/api/v1/bills',\
        data=dict(id=id),\
        follow_redirects=True \
        )

    def add_pay_period_expense(self, user_id, name, cost, category=None):
        return self.app.post('/api/v1/ppe',
        data=dict(user_id=user_id, name=name, cost=cost, category=category),
        follow_redirects=True)

    def get_pay_period_expenses(self, id=None, user_id=None):
        data = {}
        if id:
            data['id'] = id
        if user_id:
            data['user_id'] = user_id
        if not id and not user_id:
            return self.app.get('/api/v1/ppe', follow_redirects=True)
        return self.app.get('/api/v1/ppe', data=data, follow_redirects=True)

    def delete_pay_period_expense(self, id):
        return self.app.delete('/api/v1/ppe',
        data=dict(id=id),
        follow_redirects=True)

    def update_pay_period_expense_name(self, id, name):
        return self.app.put('/api/v1/ppe',\
        data=dict(id=id, name=name),\
        follow_redirects=True \
        )

    def update_pay_period_expense_cost(self, id, cost):
        return self.app.put('/api/v1/ppe',\
        data=dict(id=id, cost=cost),\
        follow_redirects=True \
        )

    def update_pay_period_expense_category(self, id, category):
        return self.app.put('/api/v1/ppe',\
        data=dict(id=id, category=category),\
        follow_redirects=True \
        )

    def get_budget_schedule(self, id, count=12):
        return self.app.get('/api/v1/budget-schedule',\
        data=dict(id=id, count=count),\
        follow_redirects=True \
        )

    ## TESTS
    def test_users(self):
        reg1 = self.register('email@email.com', 'PassWord1', '02/25/2020', pay_frequency=14)
        reg2 = self.register('email2@email.com', 'PassWord2', '02/14/2020', pay_dates=[1])
        reg3 = self.register('email3@email.com', 'PassWord3', '02/14/2020', pay_dates=[1, 15])
        reg4 = self.register('email3@email.com', 'PassWord3', '02/14/2020', pay_dates=[1, 15])

        self.assertEqual(reg1.status_code, 201)
        self.assertEqual(reg2.status_code, 201)
        self.assertEqual(reg3.status_code, 201)
        self.assertEqual(reg4.status_code, 404)

        login1 = self.login('email@email.com', 'PassWord1')
        login2 = self.login('email2@email.com', 'PassWord2')
        login3 = self.login('email3@email.com', 'PassWord3')
        login4 = self.login('email0@email.com', 'PassWord3')
        login5 = self.login('email3@email.com', 'PassWord1')

        self.assertEqual(login1.status_code, 200)
        self.assertEqual(login2.status_code, 200)
        self.assertEqual(login3.status_code, 200)
        self.assertEqual(login4.status_code, 404)
        self.assertEqual(login5.status_code, 404)

        all = self.get_users()
        get1 = self.get_user(1)
        get2 = self.get_user(2)
        get3 = self.get_user(3)
        get4 = self.get_user(4)

        self.assertEqual(all.status_code, 200)
        self.assertEqual(get1.status_code, 200)
        self.assertEqual(get2.status_code, 200)
        self.assertEqual(get3.status_code, 200)
        self.assertEqual(get4.status_code, 404)

        update1 = self.update_user_email(1, 'maile@email.com')
        update2 = self.update_user_password(2, 'WordPass2')
        update3 = self.update_user_last_pay_date(1, '05/02/2020')
        update4 = self.update_user_pay_frequency(1, 7)
        update5 = self.update_user_pay_dates(3, [5,7])
        update6 = self.update_user_pay_dates(7, [5,7])

        self.assertEqual(update1.status_code, 200)
        self.assertEqual(update2.status_code, 200)
        self.assertEqual(update3.status_code, 200)
        self.assertEqual(update4.status_code, 200)
        self.assertEqual(update5.status_code, 200)
        self.assertEqual(update6.status_code, 404)

    def test_bills(self):
        reg1 = self.register('email4@email.com', 'PassWord1', '02/25/2020', pay_frequency=14)
        reg2 = self.register('email5@email.com', 'PassWord2', '02/14/2020', pay_dates=[1])
        reg3 = self.register('email6@email.com', 'PassWord3', '02/14/2020', pay_dates=[1, 15])

        bill1 = self.add_bill(user_id=1, name="National Grid", cost=40.40, due_date=12, last_paid="02/20/2020", category="Utility")
        bill2 = self.add_bill(user_id=2, name="Spectrum", cost=49.99, frequency=30, last_paid="02/20/2020", category="Entertainment")
        bill3 = self.add_bill(user_id=2, name="Netflix", cost=14.99, frequency=30, last_paid="02/20/2020")

        self.assertEqual(bill1.status_code, 201)
        self.assertEqual(bill2.status_code, 201)
        self.assertEqual(bill3.status_code, 201)

        get_bill1 = self.get_bills(id=1)
        get_bill2 = self.get_bills(user_id=2)
        get_bill3 = self.get_bills(id=[1, 2])
        get_bills = self.get_bills()
        get_bill5 = self.get_bills(user_id=7)

        self.assertEqual(get_bill1.status_code, 200)
        self.assertEqual(get_bill2.status_code, 200)
        self.assertEqual(get_bill3.status_code, 200)
        self.assertEqual(get_bill5.status_code, 404)

        update1 = self.update_bill_name(1, "Nateal Greed")
        update2 = self.update_bill_cost(2, 44.99)
        update3 = self.update_bill_category(3, "Waste of money")
        update4 = self.update_bill_category(4, "Waste of money")

        self.assertEqual(update1.status_code, 200)
        self.assertEqual(update2.status_code, 200)
        self.assertEqual(update3.status_code, 200)
        self.assertEqual(update4.status_code, 404)

        delete1 = self.delete_bill(1)
        delete2 = self.delete_bill(2)
        delete3 = self.delete_bill(3)

        self.assertEqual(delete1.status_code, 204)
        self.assertEqual(delete2.status_code, 204)
        self.assertEqual(delete3.status_code, 204)

    def test_pay_period_expenses(self):
        reg1 = self.register('email7@email.com', 'PassWord1', '02/25/2020', pay_frequency=14)
        reg2 = self.register('email8@email.com', 'PassWord2', '02/14/2020', pay_dates=[1])
        reg3 = self.register('email9@email.com', 'PassWord3', '02/14/2020', pay_dates=[1, 15])

        ppe1 = self.add_pay_period_expense(1, "Gas", 40.00, "auto")
        ppe2 = self.add_pay_period_expense(2, "Groceries", 250.00)
        ppe3 = self.add_pay_period_expense(3, "Savings", 50.00)

        self.assertEqual(ppe1.status_code, 201)
        self.assertEqual(ppe2.status_code, 201)
        self.assertEqual(ppe3.status_code, 201)

        get_ppe1 = self.get_pay_period_expenses(id=2)
        get_ppe2 = self.get_pay_period_expenses(user_id=2)
        get_ppe3 = self.get_pay_period_expenses()
        get_ppe4 = self.get_pay_period_expenses(user_id=6)
        get_ppe5 = self.get_pay_period_expenses(id=5)

        self.assertEqual(get_ppe1.status_code, 200)
        self.assertEqual(get_ppe2.status_code, 200)
        self.assertEqual(get_ppe3.status_code, 200)
        self.assertEqual(get_ppe4.status_code, 404)
        self.assertEqual(get_ppe5.status_code, 404)

        delete_ppe1 = self.delete_pay_period_expense(id=1)
        update_ppe1 = self.update_pay_period_expense_name(id=2, name="Groseriez")
        update_ppe2 = self.update_pay_period_expense_cost(id=3, cost=100)
        update_ppe3 = self.update_pay_period_expense_category(id=2, category="Idk")
        update_ppe4 = self.update_pay_period_expense_category(id=1, category="Idk")

        self.assertEqual(delete_ppe1.status_code, 200)
        self.assertEqual(update_ppe1.status_code, 200)
        self.assertEqual(update_ppe2.status_code, 200)
        self.assertEqual(update_ppe3.status_code, 200)
        self.assertEqual(update_ppe4.status_code, 404)

    def test_budget_schedule(self):
        reg1 = self.register('email14@email.com', 'PassWord1', '02/25/2020', pay_frequency=14)

        budget_schedule1 = self.get_budget_schedule(id=1)
        budget_schedule2 = self.get_budget_schedule(id=1, count=24)
        budget_schedule3 = self.get_budget_schedule(id=2)

        self.assertEqual(budget_schedule1.status_code, 200)
        self.assertEqual(budget_schedule2.status_code, 200)
        self.assertEqual(budget_schedule3.status_code, 404)

if __name__ == "__main__":
    unittest.main()
