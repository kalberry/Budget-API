import os
import markdown

from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

api = Api(app)

@app.route("/")
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
            return {"message": "Getting user data for " + args['id'] + "."}, 200

        return {"message": "Getting all users."}, 200

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

        if (args['user_id'] and args['id']):
            return {"message": "Bad Request"}, 400
        if (args['user_id'] and not args['id']):
            return {"message": "Getting bills for user " + args['user_id']}, 200
        elif (not args['user_id'] and args['id']):
            return {"message": "Getting bill with id " + args['id']}, 200

        return {"message": "Getting all bills"}, 200

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

        if ((args['frequency'] and not args['due_date']) or (not args['frequency'] and args['due_date'])):
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

api.add_resource(User, '/users')
api.add_resource(Bill, '/bills')
api.add_resource(PayPeriodExpense, '/ppe')
