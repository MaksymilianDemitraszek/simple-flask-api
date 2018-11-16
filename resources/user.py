from flask_restful import reqparse, Resource
import pprint

from common.verification import verifyToken

token_parser = reqparse.RequestParser()
token_parser.add_argument('token', location='headers')

parser_update = reqparse.RequestParser()
parser_update.add_argument('new_username')
parser_update.add_argument('old_password')
parser_update.add_argument('new_password')




class User(Resource):

    def __init__(self, **kwargs):
        self.mongo = kwargs['db']

    def get(self):
        token = self.mongo.db.tokens.find_one(token_parser.parse_args()) #gets token from headers and queries it token collection

        if verifyToken(token):
            return self.mongo.db.users.find_one({'_id': token['user']}, {'_id': 0, 'password': 0, 'messages.time_stamp': 0, 'messages.license_plate': 0}), 200
        else: return 401

    def post(self):
        args = parser_update.parse_args()
        token = self.mongo.db.tokens.find_one(token_parser.parse_args()) #gets token from headers and queries it token collection

        if verifyToken(token):
            user = self.mongo.db.users.find_one({'_id': token['user']}, {'_id': 0})
            if user['password'] == args['old_password']:
                self.mongo.db.users.update({'_id': token['user']},
                                           {"$set": {'username': args['new_username'], 'password': args['new_password']}})
                return 202

        return 401


class AnyUser(Resource):

    def __init__(self, **kwargs):
        self.mongo = kwargs['db']

    def get(self, username):
        return self.mongo.db.users.find_one({'username': username},
                                            {"_id": 0, 'username': 1, 'upvotes': 1, 'downvotes': 1}), 200

