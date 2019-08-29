from app import db
from app.models import User, Friendship, Timeline_Member
# #Let’s import our Book and Base classes from our database_setup.py file
# from db_setup import Base, User, Friendship, Timeline_Member
import tweepy
import timeit


def populate_db(api, list_id=-1):
	#populate/update User and Timeline_Member for the user
	me = api.me()
	user_id = me.id
	populate_single_user(me)

    
	populate_single_timeline(getRecentStatus(api, user_id), user_id)
	#populate/update Friendship for the user
	friends = []
	if list_id < 0:
		friends = tweepy.Cursor(api.friends).items()
	else:
		friends = tweepy.Cursor(api.list_members, list_id=list_id).items()
	populate_friendship(friends, user_id)

	friends = []
	#populate/update User and Timeline_Member for the user's friends
	if list_id < 0:
		friends = tweepy.Cursor(api.friends).items()
	else:
		friends = tweepy.Cursor(api.list_members, list_id=list_id).items()

	for friend in friends:
		populate_single_user(friend)
		populate_single_timeline(getRecentStatus(api, friend.id), friend.id)


def populate_single_user(me):
	tmpUser = User.query.filter_by(id=me.id).first()
	#populate/update the user to the db
	if not tmpUser:
		newUser = User(id=me.id, name=me.name, screen_name=me.screen_name)
		db.session.add(newUser)
		db.session.commit()
	elif (tmpUser.name != me.name) or (tmpUser.screen_name != me.screen_name):
		tmpUser.name = me.name
		tmpUser.screen_name = me.screen_name
		db.session.add(tmpUser)
		db.session.commit()

def populate_friendship(friends, user_id):
	twt_friend_ids = []

	db_friendships = Friendship.query.filter_by(id=user_id).all()
	db_friend_ids = [friendship.friend_id for friendship in db_friendships]
	#populate if the friendship in twt, but NOT in db
	for friend in friends:
		twt_friend_ids.append(friend.id)

		if friend.id not in db_friend_ids:
			newFriendship = Friendship(id=user_id, friend_id=friend.id)
			db.session.add(newFriendship)
			db.session.commit()
	#delete if the friendship in db, but NOT in twt
	for f_id in db_friend_ids:
		if f_id not in twt_friend_ids:
			Friendship.query.filter_by(id=user_id, friend_id=f_id).delete()
			db.session.commit()


def populate_single_timeline(timeline, user_id):
	''' populate/update 5 statuses for a user '''
	tmpStatus = Timeline_Member.query.filter_by(user_id=user_id).first()
	need_populate = False

	# populate/update if the user's timeline in db is outdated or DNE
	if (tmpStatus is not None) and (tmpStatus.id != timeline[0].id):
		Timeline_Member.query.filter_by(user_id=user_id).delete()
		db.session.commit()
		need_populate = True
	
	if (need_populate) or (tmpStatus is None):
		for status in timeline:
			newStatus = Timeline_Member(id=status.id, text=status.text, user_id=user_id)
			db.session.add(newStatus)
		db.session.commit()
	#populate/update the timeline

def getRecentStatus(api, user_id):
	timeline = [status for status in tweepy.Cursor(api.user_timeline, id=user_id).items(5)]
	return timeline


	