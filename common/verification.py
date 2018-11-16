import random, string

def verifyToken(token):
    if token:
        return True
        # if token['expires']:
        #     pass
        # else: True
    return False

def genrateToken(database):
    token = ''.join([random.choice(string.ascii_letters + string.digits) for x in range(72)])
    if database.db.tokens.find_one({'token': token}):
        token = genrateToken(database)
    return token

def verifyMessageText(message):
    return len(message) < 300

