from flask import Flask, request
from flask_restful import reqparse, Resource
import pprint ,random

from common.verification import genrateToken

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')


class Login(Resource):

    def __init__(self, **kwargs):
        self.mongo = kwargs['db']

    def post(self):
        args = parser.parse_args()

        user = self.mongo.db.users.find_one({'username': args['username'], 'password': args['password']})
        if user:
            token = genrateToken(self.mongo)
            self.mongo.db.tokens.remove({'user': user['_id']})
            self.mongo.db.tokens.insert_one({
                'token': token,
                'user': user['_id'],
            })
            return {'token': token}, 200

        else:
            return 402

