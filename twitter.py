import folium
import tweepy
from textblob import TextBlob
import preprocessor as p
from geopy.geocoders import Nominatim


def main(a, b, c, d):
    '''Function to geocode the location data, perform sentiment analysis and plot on the map'''
    consumer_key = a
    consumer_secret = b
    access_token = c
    access_secret = d
    # twitter authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # Take the hashtag as input
    hashtag = input("Input the hashtag for which tweets are to be extracted: ")
    # Take limiting number of tweets
    limiting_value = int(input("Input the number of live tweets that are to be extracted: "))
    mapvar = folium.Map(location=[45.38, -121.67], zoom_start=3)
    geolocator = Nominatim(user_agent = 'tweet_plot')
    # Row number
    i = 0
    try:
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
    except tweepy.error.TweepError:
        print("Check your credentials for correctness")
    mapvar.save('twittermap.html')
    
    
if __name__ == '__main__':
    '''INPUT YOUR CREDENTIALS HERE'''
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_secret = ""
    main(consumer_key, consumer_secret, access_token, access_secret)
