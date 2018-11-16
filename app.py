from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo

from resources.login import Login
from resources.user import User, AnyUser
from resources.message import Message

app = Flask(__name__)
api = Api(app)
mongo = PyMongo(app, config_prefix='MONGO')

app.config['SECRET_KEY'] = 'secret!'

api.add_resource(Login, '/login', resource_class_kwargs={'db': mongo})

api.add_resource(User, '/user', resource_class_kwargs={'db': mongo})
api.add_resource(AnyUser, '/user/<username>', resource_class_kwargs={'db': mongo})

api.add_resource(Message, '/message', resource_class_kwargs={'db': mongo})


if __name__ == "__main__":
    app.run()
