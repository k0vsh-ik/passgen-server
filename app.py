from flask import Flask
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
    user_id = db.Column(db.Integer, default='Null')

    def __repr__(self):
        return '<Passwords %r>' % self.id


@app.route('/')
def main():
    return {"passwords": ["pass1", "pass2", "pass3"]}


if __name__ == "__main__":
    app.run(debug=True)
