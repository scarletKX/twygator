import tweepy
import timeit

consumer_key = 'kd8Mq1XlxRnjMH4xdWxReBXKm'
consumer_secret = 'oBmGcMYkkYC4Cs45Bam3Uf0qTSaBi7KnC7DPAKKDIJMP6VgOVi'
access_token = '897868147033874432-TTNGeCvKj5KJbThhfDqbOXrnWPLq9nl'
access_token_secret = 'JPwJP60eIwhUHVvK0kCqktlaiq97OraCRnAJ55gNohCvN'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

me = api.me()

def tupleTest():
	strArr1 = ['a','b','c','d','e']
	strArr2 = ['f','g','h','i','j']
	strTup = (strArr1, strArr2)
	intArr1 = range(1,6)
	intArr2 = range(6,11)
	combo = []
	for idx in range(5):
		combo.append((strTup[0][idx],
				  strTup[1][idx],
				  [n for n in intArr1],
				  [n for n in intArr2]))
	print(combo)
	for alf1, alf2, arr1, arr2 in combo:
		print(alf1)
		print(arr1)


def messingAround():
	timer_start = timeit.default_timer()
	all_f_ids = api.friends_ids()
	f_timelines = []
	count = 0
	for f_id in all_f_ids:
		count += 1
		get_api_time_start = timeit.default_timer()
		friend = api.get_user(f_id)
		timeline = api.user_timeline(f_id, count=5)
		get_api_time_stop = timeit.default_timer()
		print(count, "current friend is", friend.name, " with username @", friend.screen_name)
		print("His/her current 5 statuses are: ")
		for idx in range(5):
			print("The ", idx, "th status is ", timeline[idx].text)
		append_start = timeit.default_timer()
		f_timelines += (friend.name, 
						friend.screen_name, 
						[status.id for status in timeline],
						[status.text for status in timeline])
		append_stop = timeit.default_timer()
		print("Retrieving Twitter data cost ", round(get_api_time_stop - get_api_time_start, 3), "seconds")
		print("Appending the data used ", round(append_stop - append_start, 5), "seconds")
		print('\n')
	timer_stop = timeit.default_timer()
	print('Whole function took: ', round(timer_stop - timer_start, 3), 'seconds')

def is_jsonable(obj):
	try:
		json.dumps(obj._json)
		print('The object is jsonable')
	except:
		print('No, not jsonable')

tupleTest()
messingAround()
is_jsonable(api.user_timeline(me.id, count=1)[0])