from flask_restful import reqparse, Resource
import pprint ,datetime

from common.verification import verifyToken, verifyMessageText

token_parser = reqparse.RequestParser()
token_parser.add_argument('token', location='headers')

message_parser = reqparse.RequestParser()
message_parser.add_argument('text')
message_parser.add_argument('license_plate')

class Message(Resource):

    def __init__(self, **kwargs):
        self.mongo = kwargs['db']

    def post(self):
        token = self.mongo.db.tokens.find_one(token_parser.parse_args()) # gets token from headers and queries it token collection
        message = message_parser.parse_args()

        if verifyToken(token):
            if verifyMessageText(message['text']):
                message['time_stamp'] = datetime.datetime.now()
                recipient = self.mongo.db.users.find_one({'license_plate': message['license_plate']})
                if recipient:
                    self.mongo.db.users.update({'_id': recipient['_id']}, {'$push': {'messages': message}})
                    return 200

                else:
                    return {'error': 'There is no user with this plate'}, 400

            else:
                return {'error': 'Wrong message'}, 400

        return 401

    def get(self):
        token = self.mongo.db.tokens.find_one(token_parser.parse_args())  # gets token from headers and queries it token collection
        if verifyToken(token):
            messages = self.mongo.db.users.find_one({'_id': token['user']}, {'_id': 0, 'messages.text': 1})['messages']
            return messages



