import folium
import tweepy
from textblob import TextBlob
import preprocessor as p
from geopy.geocoders import Nominatim

# input your credentials here
consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""
# twitter authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
# Take the hashtag as input
hashtag = input("Input the hashtag for which tweets are to be extracted: ")
# Take limiting number of tweets
limiting_value = int(input("Input the number of live tweets that are to be extracted: "))
mapvar = folium.Map(location=[45.38, -121.67], zoom_start=3)
geolocator = Nominatim()
# Row number
i = 0
for tweet in tweepy.Cursor(api.search, q=hashtag, lang="en").items():
    tweet_location = p.clean(tweet.user.location)
    try:
        location = geolocator.geocode(tweet_location)
    except:
        location = "NULL"
    # write in excel only if location is not null
    if location != "NULL" and tweet_location != '' and location is not None:
        # clean tweet
        type(tweet.text)
    tweet_text = p.clean(tweet.text)[2:]
    print(tweet_text)
    print("\n")
    # sentiment analysis
    feelings = TextBlob(tweet_text).sentiment.polarity
    icon = folium.Icon()
    if feelings >= 0:
        i = i + 1
        icon = folium.Icon(color='green')
    elif feelings < 0:
        i = i + 1
        icon = folium.Icon(color='red')
    try:
        folium.Marker(location=[location.latitude, location.longitude], icon=icon).add_to(mapvar)
    except:
        pass
    if i == limiting_value:
        break
mapvar.save('twittermap.html')
