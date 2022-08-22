from random import randint

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passgen.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


class Passwords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Password %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        content = request.json

        totArr = checker(content)
        passwd = genPass(totArr, content['amount'])

        record = Passwords(password=passwd)

        try:
            db.session.add(record)
            db.session.commit()
            return f'{passwd}   JSON: {content}'

        except:
            return 'An error while recording'

    else:
        return "What r u doing here?"


def checker(content):
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'
    symbols = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    totArr = ''

    if content['ll']:
        totArr += uppercase

    if content['sl']:
        totArr += lowercase

    if content['num']:
        totArr += digits

    if content['sym']:
        totArr += symbols

    return totArr


def genPass(totArr, amount):
    passwd = ''

    if amount == '':
        return "Amount is empty!"

    for i in range(int(amount)):
        passwd += totArr[randint(0, len(totArr) - 1)]

    return passwd


if __name__ == "__main__":
    app.run(debug=True)
