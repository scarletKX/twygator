# import sys
# #for creating the mapper code
# from sqlalchemy import Column, ForeignKey, Integer, String
# #for configuration and class code
# from sqlalchemy.ext.declarative import declarative_base
# #for creating foreign key relationship between the tables
# from sqlalchemy.orm import relationship, scoped_session, sessionmaker
# #for configuration
# from sqlalchemy import create_engine

from app import db


# #we'll add classes here

# #creates a create_engine instance at the bottom of the file
# engine = create_engine('sqlite:///twitter_user.db', convert_unicode=True)

# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))

# #create declarative_base instance
# Base = declarative_base()
# Base.query = db_session.query_property()

# Base.metadata.create_all(engine)



class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	screen_name = db.Column(db.String(100), nullable=False)
	friends = db.relationship('Friendship', backref='User', lazy=True)
	statuses = db.relationship('Timeline_Member', backref='User', lazy=True)

	def __repr__(self):
		return '<User @{}>'.format(self.screen_name)

class Friendship(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


class Timeline_Member(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(250), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)