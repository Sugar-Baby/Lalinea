from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# 多对多关联表：用户-爱好
user_hobbies = db.Table(
    'user_hobbies',
    db.Column('user_id', db.Integer, db.ForeignKey('user_data.id'), primary_key=True),
    db.Column('hobby_id', db.Integer, db.ForeignKey('hobby.id'), primary_key=True)
)

# 多对多关联表：用户-用户（认识的人，双向）
user_friends = db.Table(
    'user_friends',
    db.Column('user_id', db.Integer, db.ForeignKey('user_data.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user_data.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'user_data'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    contact = db.Column(db.String(128))
    hobbies = db.relationship('Hobby', secondary=user_hobbies, back_populates='users')
    friends = db.relationship(
        'User',
        secondary=user_friends,
        primaryjoin=id == user_friends.c.user_id,
        secondaryjoin=id == user_friends.c.friend_id,
        backref='friend_of'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Hobby(db.Model):
    __tablename__ = 'hobby'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', secondary=user_hobbies, back_populates='hobbies')

class CompatibilityScore(db.Model):
    __tablename__ = 'compatibility_score'
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user_data.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user_data.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=db.func.now())
    
    # Ensure user1_id is always smaller than user2_id to avoid duplicates
    __table_args__ = (
        db.CheckConstraint('user1_id < user2_id', name='check_user_order'),
        db.UniqueConstraint('user1_id', 'user2_id', name='unique_user_pair'),
    )

    user1 = db.relationship('User', foreign_keys=[user1_id], backref='compatibility_scores_as_user1')
    user2 = db.relationship('User', foreign_keys=[user2_id], backref='compatibility_scores_as_user2')
