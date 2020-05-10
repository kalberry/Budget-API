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

@app.route("/")
def index():
    db.get_bills({"user_id": 5})

    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:
        content = markdown_file.read()

        return markdown.markdown(content)

class User(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id')
        args = parser.parse_args()

        if (args['id']):
            user = db.get_users(args['id'])
            if (user is not None):
                return {"message": "User retrieved", "data": db.get_users(args['id'])}, 200
            else:
                return {"message": "User not found"}, 404

        users = db.get_users()
        print(users)
        if (users):
            return {"message": "Retrieved all users.", "data": users}, 200
        else:
            return {"message": "Count not find user"}, 404

    def put(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)
        parser.add_argument('email')
        parser.add_argument('password_hash')
        parser.add_argument('starting_pay_date')
        parser.add_argument('pay_frequency')
        parser.add_argument('pay_dates', action='append')

        args = parser.parse_args()

        message = 'For ' + str(args['id']) + " we "
        if (args['email']):
            message += 'updated email. '
        if (args['password_hash']):
            message += 'updated password. '
        if (args['starting_pay_date']):
            message += 'updated starting pay date. '
        if (args['pay_frequency']):
            message += 'updated pay frequency. '
        if (args['pay_dates']):
            message += 'updated pay dates. '

        return {"message": message}, 200


class Bill(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('user_id')
        parser.add_argument('id')

        args = parser.parse_args()

        #db.get_bills()

        if (args['user_id'] and args['id']):
            return {"message": "Bad Request"}, 400
        if (args['user_id'] and not args['id']):
            return {"message": "Getting bills for user " + args['user_id']}, 200
        elif (not args['user_id'] and args['id']):
            return {"message": "Getting bill with id " + args['id']}, 200

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

        return {"message": "Deleting bill with id " + args['id']}

class PayPeriodExpense(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('user_id')
        parser.add_argument('id')

        args = parser.parse_args()

        if (args['user_id'] and args['id']):
            return {"message": "Bad Request"}, 400
        if (args['user_id'] and not args['id']):
            return {"message": "Getting pay period expenses for user " + args['user_id']}, 200
        elif (not args['user_id'] and args['id']):
            return {"message": "Getting pay period expense with id " + args['id']}, 200

        return {"message": "Getting all pay period expenses"}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('user_id', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('cost', required=True)
        parser.add_argument('category')

        args = parser.parse_args()

        return {"message": "Pay period expense " + args['name'] + " for " + args['user_id'] + " costing " + args['cost']}, 201

    def delete(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', required=True)

        args = parser.parse_args()

        return {"message": "Deleting pay period expense with id " + args['id']}

class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('email', required=True)
        parser.add_argument('password_hash', required=True)
        parser.add_argument('starting_pay_date', required=True)
        parser.add_argument('pay_frequency')
        parser.add_argument('pay_dates', action='append')

        args = parser.parse_args()

        #db.register_user

class Login(Resource):
    def post(self):
        pass

api.add_resource(User, '/users')
api.add_resource(Bill, '/bills')
api.add_resource(PayPeriodExpense, '/ppe')
api.add_resource(Register, '/auth/register')
api.add_resource(Login, '/auth/login')
