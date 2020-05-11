import os
import markdown

from budget_api.models import User, Bill, Database
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
db = models.Database()

app.config['SECRET_KEY'] = 'applesauce'
db.create_tables()

@app.route("/api/v1")
def index():
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
        content = markdown_file.read()

        return markdown.markdown(content)

class User(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id')
        args = parser.parse_args()

        if (args['id']):
            user = db.get_users({"id": args['id']})
            if (user != []):
                return {"message": "User retrieved", "data": user}, 200
            else:
                return {"message": "User not found"}, 404

        users = db.get_users()
        if (users):
            return {"message": "Retrieved all users.", "data": users}, 200
        else:
            return {"message": "Count not find user"}, 404

    def put(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)
        parser.add_argument('email')
        parser.add_argument('password_hash')
        parser.add_argument('last_pay_date')
        parser.add_argument('pay_frequency')
        parser.add_argument('pay_dates', action='append')

        args = parser.parse_args()

        message = 'For ' + str(args['id']) + " we "
        if (args['email']):
            db.update_user({"email": args['email'], "id": args['id']})
            message += 'updated email. '
        if (args['password_hash']):
            db.update_user({"password_hash": args['password_hash'], "id": args['id']})
            message += 'updated password. '
        if (args['last_pay_date']):
            db.update_user({"last_pay_date": args['last_pay_date'], "id": args['id']})
            message += 'updated starting pay date. '
        # TODO - Eventually make sure they can either have pay_freq or pay_dates
        if (args['pay_frequency']):
            db.update_user({"pay_frequency": args['pay_frequency'], "id": args['id']})
            message += 'updated pay frequency. '
        if (args['pay_dates']):
            db.update_user({"pay_dates": args['pay_dates'], "id": args['id']})
            message += 'updated pay dates. '

        user = db.get_users({"id": args['id']})
        if (user):
            return {"message": message}, 200
        else:
            return {"message": "Failed to update user"}, 404

    def delete(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)

        args = parser.parse_args()
        print(args['id'])

        db.delete_user(args['id'])

        return 204

class Bill(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('user_id')
        parser.add_argument('id', action='append')
        parser.add_argument('category')

        args = parser.parse_args()

        if (args['user_id'] and args['id']):
            return {"message": "Bad Request"}, 400
        elif (args['user_id'] and not args['id']):
            user = db.get_bills({"user_id": args['user_id']})
            return {"message": "Received bills successfully", "data": user}, 200
        elif (not args['user_id'] and args['id']):
            bill = db.get_bills(id=args['id'])
            return {"message": "Received bill successfully", "data": bill}, 200

        return {"message": "Getting all bills", "data": db.get_bills()}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('user_id', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('cost', required=True)
        parser.add_argument('due_date')
        parser.add_argument('frequency')
        parser.add_argument('last_paid', required=True)
        parser.add_argument('category')

        args = parser.parse_args()

        if args['frequency'] and not args['due_date']:
            b = models.Bill(user_id=args['user_id'], name=args['name'], cost=args['cost'], due_date=args['due_date'], frequency=None, last_paid=args['last_paid'], category=args['category'])

            db.add_bill(b)
            return {"message": args['name'] + " bill with the cost of $" + args['cost']}, 201
        elif not args['frequency'] and args['due_date']:
            b = models.Bill(user_id=args['user_id'], name=args['name'], cost=args['cost'], due_date=args['due_date'], frequency=None, last_paid=args['last_paid'], category=args['category'])

            db.add_bill(b)
            return {"message": args['name'] + " bill with the cost of $" + args['cost']}, 201

        return {"message": "Bad Request"}, 400

    def delete(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)

        args = parser.parse_args()
        print(args['id'])

        db.delete_bill(args['id'])

        return 204

class PayPeriodExpense(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('user_id')
        parser.add_argument('id', action='append')

        args = parser.parse_args()

        if (args['user_id'] and args['id']):
            ppe = db.get_pay_period_expenses(user_id=args['user_id'], id=args['id'])
        elif (args['user_id'] and not args['id']):
            ppe = db.get_pay_period_expenses(user_id=args['user_id'])
        elif (not args['user_id'] and args['id']):
            ppe = db.get_pay_period_expenses(id=args['id'])

        if ppe != None and ppe != []:
            return {"message": "Recieved pay period expense request", "data": ppe}, 200
        else:
            return 404

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('user_id', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('cost', required=True)
        parser.add_argument('category')

        args = parser.parse_args()

        if args['category'] is not None:
            db.add_pay_period_expense(name=args['name'], cost=args['cost'], user_id=args['user_id'], category=args['category'])
            db.get_pay_period_expenses()
        else:
            db.add_pay_period_expense(name=args['name'], cost=args['cost'], user_id=args['user_id'])

        return {"message": "Pay period expense added successfully"}, 201

    def delete(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)

        args = parser.parse_args()

        db.delete_pay_period_expense(args['id'])

        return 204

    def put(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)
        parser.add_argument('name')
        parser.add_argument('cost')
        parser.add_argument('category')

        args = parser.parse_args()

        id = args['id']
        name = args['name']
        cost = args['cost']
        category = args['category']

        if name:
            db.update_pay_period_expense(id=id, name=name)
        if cost:
            db.update_pay_period_expense(id=id, cost=cost)
        if category:
            db.update_pay_period_expense(id=id, category=category)

        return {"message": "Pay period updated."}, 200

class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('email', required=True)
        parser.add_argument('password_hash', required=True)
        parser.add_argument('last_pay_date', required=True)
        parser.add_argument('pay_frequency')
        parser.add_argument('pay_dates', action='append')

        args = parser.parse_args()

        email = args['email']
        password_hash = args['password_hash']
        last_pay_date = args['last_pay_date']
        pay_frequency = args['pay_frequency']
        pay_dates = args['pay_dates']

        user = db.register_user(email, password_hash, last_pay_date, pay_frequency, pay_dates)

        if user != {}:
            return {"message": "User registered", "data": user}, 201
        else:
            return{"message": "User failed to register"}, 404

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('email', required=True)
        parser.add_argument('password_hash', required=True)

        args = parser.parse_args()

        user = db.login_user(args['email'], args['password_hash'])

        if user != {}:
            return {"message": "User logged in", "data": user}, 200
        else:
            return{"message": "User failed to register"}, 404

class BudgetSchedule(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)

        args = parser.parse_args()
        id = args['id']

        db.get_budget_schedule(user_id=id)

api.add_resource(User, '/api/v1/users')
api.add_resource(Bill, '/api/v1/bills')
api.add_resource(PayPeriodExpense, '/api/v1/ppe')
api.add_resource(Register, '/api/v1/auth/register')
api.add_resource(Login, '/api/v1/auth/login')
api.add_resource(BudgetSchedule, '/api/v1/budget-schedule')
