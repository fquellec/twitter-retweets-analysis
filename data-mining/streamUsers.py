from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import credentials
import tweepy
import os
import csv

USER_NAMES = ['@lemondefr','@courrierinter','@leJDD','@humanite_fr',
              '@LEXPRESS','@libe','@LesEchos','@lobs','@MarianneleMag',
              '@Le_Figaro','@AlterEco_','@_polemia','@sputnik_fr',
              '@Europe_Israel','@Breizh_Info','@BVoltaire','@RTenfrancais',
              '@InfoMdia','@Valeurs','@tvlofficiel','@LePoint','@F_Desouche',
              '@Dreuz_1fo','@ndffr','@FrDesouche','@1RiposteLaique','@Contreinfo',
              '@LaManifPourTous','@RNational_off','@EetR_National','@lenouvelliste',
              '@letemps','@24heuresch','@20min','@20minutesOnline','@tdgch',
              '@tagesanzeiger','@Blickch','@derbund','@LuzernerZeitung','@lecourrier',
              '@laliberte','@heidi_news','@Lematinch','@BernerZeitung','@AargauerZeitung',
              '@RTSinfo','@CdT_Online','@watson_news','@srfnews','@laregione','@RSInews']               # List of twitter accounts to stream
FILENAME   = "results/stream.csv"

# Create target Directory if don't exist
if not os.path.exists('results'):
    os.mkdir('results')

header = ['tweet_id', 'user_id', 'user_name', 'followers', 'following', 'likes', 
          'retweets', 'date', 'reply_to_tweet_id', 'reply_to_user_id', 'reply_to_username', 
          'user_mentions_ids', 'user_mentions_names', 'text', 'retweet_from_user_id', 
          'retweet_from_username', 'retweet_from_tweet_id', 'urls']
          
# write header to file if not exist
if not os.path.exists(FILENAME):
    with open(FILENAME, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)

def saveTweet(row, filename):
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)

count = 0
class StdOutListener(StreamListener):
    def on_status(self, tweet):
        global count
        tweet_id = tweet.id_str
        user_id = tweet.user.id_str
        user_name = tweet.user.screen_name
        followers = tweet.user.followers_count
        following = tweet.user.friends_count
        likes = tweet.favorite_count
        retweets = tweet.retweet_count
        date = tweet.created_at
        reply_to_tweet_id = tweet.in_reply_to_status_id_str
        reply_to_user_id = tweet.in_reply_to_user_id_str
        reply_to_username = tweet.in_reply_to_screen_name
        user_mentions_ids = [mention['id_str'] for mention in tweet.entities['user_mentions']]
        user_mentions_names = [mention['screen_name'] for mention in tweet.entities['user_mentions']]

        urls=[]
        for url in tweet.entities['urls']:
            urls.append(url['expanded_url'])

        try:
            text = tweet.extended_tweet["full_text"]
        except AttributeError:
            text = tweet.text

        retweet_from_user_id = None
        retweet_from_username = None
        retweet_from_tweet_id = None

        if hasattr(tweet, "retweeted_status"):  
            retweet_from_user_id = tweet.retweeted_status.user.id_str
            retweet_from_username = tweet.retweeted_status.user.screen_name
            retweet_from_tweet_id = tweet.retweeted_status.id_str

        row = [tweet_id, user_id, user_name, followers, following, likes, retweets, date, reply_to_tweet_id, reply_to_user_id, reply_to_username, user_mentions_ids, user_mentions_names, text, retweet_from_user_id, retweet_from_username, retweet_from_tweet_id, urls]
        saveTweet(row, FILENAME)
        count += 1
        print("{}\r".format(count), end="")

    def on_error(self, status_code):
        if status_code == 420:
            # Returning False in on_error disconnects the stream
            return False

l = StdOutListener()
auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
stream = Stream(auth, l, tweet_mode='extended')

queries = []

# Fetch users ids
api = tweepy.API(auth)
for user_name in USER_NAMES:
    user = api.get_user(user_name)
    queries.append(user.id_str)

while True:
    stream.filter(follow=queries)

