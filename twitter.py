import folium
import tweepy
from openpyxl import Workbook
from textblob import TextBlob
import preprocessor as p
from geopy.geocoders import Nominatim
#input your credentials here
consumer_key = "jedN8eSwXoEuBwz5eHwFrGwbd"
consumer_secret = "BM9oKPoTot47YRFUo4378Ov4Jzfwz4Zf20bkuk84y9aMC2H5Wr"
access_token = "113678439-akUhAwJoSKt3Taw5vfWAnn8KgrPeShD6hxR96fMi"
access_secret = "PldNZ2VvyFzqbHtYQ0d2AeGZ9VoFYvJks06cbjdSblep9"
#twitter authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
#Take the hashtag as input
hashtag = raw_input("Input the hashtag for which tweets are to be extracted: ")
#Take limiting number of tweets
limiting_value=int(raw_input("Input the number of live tweets that are to be extracted: "))
mapvar=folium.Map(location=[45.38,-121.67],zoom_start=1)
geolocator = Nominatim()
#Row number
i=0
for tweet in tweepy.Cursor(api.search,q=hashtag,lang="en").items():
	tweet_location=p.clean(tweet.user.location.encode('ascii','ignore'))
	try:
		location = geolocator.geocode(tweet_location)
	except:
		location="NULL"
	#write in excel only if location is not null
	if location != "NULL" and tweet_location!='' and location is not None:
		#clean tweet
		tweet_text=p.clean(tweet.text.encode('ascii','ignore'))[2:]
		print tweet_text
		print "\n"
		#sentiment analysis
		feelings=TextBlob(tweet_text).sentiment.polarity
		icon=folium.Icon()
		if feelings>=0:
			i=i+1
			icon=folium.Icon(color='green')
		elif feelings<0:
			i=i+1
			icon=folium.Icon(color='red')
		folium.Marker(location=[location.latitude,location.longitude],icon=icon).add_to(mapvar)
		if i==limiting_value:
			break
mapvar.save('twittermap.html')
