from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lalinea.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(20))
    hobbies = db.relationship('Hobby', secondary='user_hobbies', backref=db.backref('users', lazy='dynamic'))

class Hobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

user_hobbies = db.Table('user_hobbies',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('hobby_id', db.Integer, db.ForeignKey('hobby.id'), primary_key=True)
)

@app.route('/api/hobbies/search', methods=['GET'])
def search_hobbies():
    query = request.args.get('q', '')
    hobbies = Hobby.query.filter(Hobby.name.like(f'%{query}%')).all()
    return jsonify([{'id': h.id, 'name': h.name} for h in hobbies])

@app.route('/api/hobbies', methods=['POST'])
def add_hobby():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    hobby = Hobby.query.filter_by(name=name).first()
    if hobby:
        return jsonify({'id': hobby.id, 'name': hobby.name}), 200
    new_hobby = Hobby(name=name)
    db.session.add(new_hobby)
    db.session.commit()
    return jsonify({'id': new_hobby.id, 'name': new_hobby.name}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 