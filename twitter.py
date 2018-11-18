import folium
import tweepy
from openpyxl import Workbook
from textblob import TextBlob
import preprocessor as p
from geopy.geocoders import Nominatim
#input your credentials here
consumer_key = "<Your Consumer Key Goes Here>"
consumer_secret = "<Your Consumer Secret Token Goes Here>"
access_token = "<Your Acsess Token Goes Here>"
access_secret = "<Your Acsess Secret Token Goes Here>"
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
