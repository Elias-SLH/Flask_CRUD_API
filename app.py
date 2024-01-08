from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flask_crud_api.db"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}


with app.app_context():
    db.create_all()


# create a test route
@app.route('/test')
def test():
    return jsonify({'message': 'test route'}), 200


# create a user
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'user created'}), 201
    except Exception as e:
        return jsonify({'message': f'error creating user: {e.args}'}), 500


# get all users
@app.route('/users')
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.json() for user in users]), 200
    except Exception as e:
        return jsonify({'message': f'error getting users: {e.args}'}), 500


# get a user by id
@app.route('/users/<int:id>')
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return jsonify({'user': user.json()}), 200
        return jsonify({'message': 'user not found'}), 404
    except Exception as e:
        return jsonify({'message': f'error getting user: {e.args}'}), 500


# update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            db.session.commit()
            return jsonify({'message': 'user updated'}), 200
        return jsonify({'message': 'user not found'}), 404
    except Exception as e:
        return jsonify({'message': f'error updating user: {e.args}'}), 500


# delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'user deleted'}), 200
        return jsonify({'message': 'user not found'}), 404
    except Exception as e:
        return jsonify({'message': f'error deleting user: {e.args}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
