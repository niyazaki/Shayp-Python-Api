from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# User Class/Model
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  # birthdate = db.Column(db.Date())
  adress = db.Column(db.String(150))

  def __init__(self, name, adress):
    self.name = name
    # self.birthdate = birthdate
    self.adress = adress

# User Schema
class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'adress')

# Init schema
user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)

# Create a User
@app.route('/user', methods=['POST'])
def add_user():
  name = request.json['name']
  adress = request.json['adress']
  # birthdate = request.json['birthdate']


  new_user = User(name, adress)

  db.session.add(new_user)
  db.session.commit()

  return user_schema.jsonify(new_user)

# Get All Users
@app.route('/user', methods=['GET'])
def get_users():
  all_users = User.query.all()
  result = users_schema.dump(all_users)
  return jsonify(result.data)

# Get Single Users
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
  user = User.query.get(id)
  return user_schema.jsonify(user)

# Update a User
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
  user = User.query.get(id)

  name = request.json['name']
  adress = request.json['adress']
  # birthdate = request.json['birthdate']

  user.name = name
  user.adress = adress
  # user.birthdate = birthdate

  db.session.commit()

  return user_schema.jsonify(user)

# Delete User
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
  user = User.query.get(id)
  db.session.delete(user)
  db.session.commit()

  return user_schema.jsonify(user)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)