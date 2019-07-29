import tweepy
from app import db
from flask import session
from app.models import User, Friendship, Timeline_Member

def get_friend_timeline(api, list_id=-1):
	friend_id_all = []
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
	return f_timelines