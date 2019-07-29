from app import app
import tweepy
import os
from flask import Flask, render_template, session, redirect, request, flash
from flask_paginate import Pagination, get_page_args
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from app import db
from app.models import User, Friendship, Timeline_Member
from app.populate import populate_db
from app.util import get_friend_timeline


#Connect to Database and create database session
# engine = create_engine('sqlite:///twitter_user.db', convert_unicode=True)
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# db_session = DBSession()

consumer_key = 'kd8Mq1XlxRnjMH4xdWxReBXKm'
consumer_secret = 'oBmGcMYkkYC4Cs45Bam3Uf0qTSaBi7KnC7DPAKKDIJMP6VgOVi'
#access_token = '897868147033874432-2SxfYZtr8q5lY7omNtOVXpwxAjSXyA9'
#access_token_secret = 'BI8H1V5Kqj41SkWDF0DsPLMcoGQMUoK7naogG0RIYkxUF'
callback = 'http://127.0.0.1:5000/callback'

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/auth')
def authen():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
	#url = auth.get_authorization_url(signin_with_twitter=True)
	url = auth.get_authorization_url()
	session['request_token'] = auth.request_token
	return redirect(url)


@app.route('/callback')
def twitter_callback():
	request_token = session['request_token']
	del session['request_token']

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
	auth.request_token = request_token
	verifier = request.args.get('oauth_verifier')
	auth.get_access_token(verifier)
	session['token'] = (auth.access_token, auth.access_token_secret)
	return redirect('/mytwygator')

@app.route('/logout')
def logout():
	session.clear()
	flash('You were signed out')
	return redirect('/')
	

@app.route('/mytwygator')
def mytwygator_option():
	access_token, access_token_secret = session.get('token')
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	session['logged_in'] = True	
	api = tweepy.API(auth, wait_on_rate_limit=True)
	list_all = api.lists_all()
	return render_template('mytwygator.html', my_lists=list_all)

@app.route('/mytwygator/<list_name>_<list_id>')
def mytwygator_view(list_name='all-friends', list_id=-1):
	access_token, access_token_secret = session.get('token')
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	session['logged_in'] = True	
	api = tweepy.API(auth, wait_on_rate_limit=True)
	me = api.me()
	session['name'] = me.name
	session['user_id'] = me.id
	
	print(type(list_id))	
	list_id = int(list_id)
	print(list_name+':', list_id)
	print(type(list_id))
	populate_db(api, list_id)

	#construct list of friends and their timelines for template rendering
	friend_id_all = []
	print(list_name+':', list_id)
	if list_id < 0:
		user_id = session.get('user_id')
		friendship_all = Friendship.query.filter_by(id=user_id).all()
		friend_id_all = [friendship.friend_id for friendship in friendship_all]
	else:
		friend_all = tweepy.Cursor(api.list_members, list_id=list_id).items()
		friend_id_all = [member.id for member in friend_all]

	f_timelines = []
	for friend_id in friend_id_all:
		#get friend name and screen_name
		friend_user = User.query.filter_by(id=friend_id).first()
		f_name = friend_user.name
		f_screen_name = friend_user.screen_name
		#get recent 5 statuses from friend
		tmpTimeline = Timeline_Member.query.filter_by(user_id=friend_id).all()
		all_status_ids = []
		all_status_texts = []
		for status in tmpTimeline:
			all_status_ids.append(status.id)
			all_status_texts.append(status.text)
		f_timelines.append((f_name,
						   f_screen_name,
						   all_status_ids,
						   all_status_texts))

	total = len(f_timelines)
	#pagination_timelines = f_timelines[offset : offset + per_page]
	page, per_page, offset= get_page_args(page_parameter='page',
										  per_page_parameter='per_page')
	per_page = 9
	offset = (page - 1) * per_page
	pagination_timelines = f_timelines[offset : offset + per_page]
	pagination = Pagination(page=page, per_page=per_page, total=total,
							css_framework='bootstrap4')
	return render_template('view_friends.html', 
							f_timelines = pagination_timelines,
							page=page,
							per_page=per_page,
							pagination=pagination,
							)


# @app.route('/processing')
# def processTimeline():
# 	#get user's twitter api
# 	access_token, access_token_secret = session.get('token')
# 	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# 	auth.set_access_token(access_token, access_token_secret)
# 	session['logged_in'] = True	
# 	api = tweepy.API(auth, wait_on_rate_limit=True)
# 	#get the name of the user
# 	me = api.me()
# 	session['name'] = me.name
# 	session['user_id'] = me.id

# 	populate_db(api)

# 	return redirect('/mytwygator')

# @app.route('/mytwygator/all_friends')
# def view_all():
# 	#construct list of friends and their timelines for template rendering
# 	f_timelines = []
# 	user_id = session.get('user_id')
# 	all_friendships = Friendship.query.filter_by(id=user_id).all()
# 	all_friend_ids = [friendship.friend_id for friendship in all_friendships]
# 	for friend_id in all_friend_ids:
# 		#get friend name and screen_name
# 		friend_user = User.query.filter_by(id=friend_id).first()
# 		f_name = friend_user.name
# 		f_screen_name = friend_user.screen_name
# 		#get recent 5 statuses from friend
# 		tmpTimeline = Timeline_Member.query.filter_by(user_id=friend_id).all()
# 		all_status_ids = []
# 		all_status_texts = []
# 		for status in tmpTimeline:
# 			all_status_ids.append(status.id)
# 			all_status_texts.append(status.text)
# 		f_timelines.append((f_name,
# 						   f_screen_name,
# 						   all_status_ids,
# 						   all_status_texts))

# 	total = len(f_timelines)
# 	#pagination_timelines = f_timelines[offset : offset + per_page]
# 	page, per_page, offset= get_page_args(page_parameter='page',
# 										  per_page_parameter='per_page')
# 	per_page = 9
# 	offset = (page - 1) * per_page
# 	pagination_timelines = f_timelines[offset : offset + per_page]
# 	pagination = Pagination(page=page, per_page=per_page, total=total,
# 							css_framework='bootstrap4')
# 	return render_template('view_all.html', 
# 							f_timelines = pagination_timelines,
# 							page=page,
# 							per_page=per_page,
# 							pagination=pagination,
# 							)
