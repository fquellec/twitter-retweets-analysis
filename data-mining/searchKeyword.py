import tweepy
import os
import csv
import credentials
import pandas as pd

# Create target Directory if don't exist
if not os.path.exists('results'):
    os.mkdir('results')

# Search Parameters
QUERY               = '#swisscovid OR #SwissCovidApp OR @SwissCovid OR swisscovid'  # Twitter Api query (OR/AND operators)
LANGUAGE            =  None                                                         # Restrict the query to a specific language ('fr', 'en'), None for all
SINCE_ID            =  None                                                         # If results after a specific ID are required, if resulting file already exist will take last tweet id fetch
MAX_ID              =  None                                                         # If results before a specific ID are required
FILENAME            = 'results/' + QUERY + "_tweets.csv"                            # Resulting file

# Fields we wants to retrieve from tweets
header = ['tweet_id', 'user_id', 'user_name', 'followers', 'following', 'likes', 'retweets', 'date', 'reply_to_tweet_id', 'reply_to_user_id', 'reply_to_username', 'user_mentions_ids', 'user_mentions_names', 'text', 'retweet_from_user_id', 'retweet_from_username', 'retweet_from_tweet_id']

# Get last ID if file already exist
if os.path.isfile(FILENAME):
    df = pd.read_csv(FILENAME)
    print(df.tweet_id.max())
    SINCE_ID = str(df.tweet_id.max() + 1)
else:
    with open(FILENAME, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)

# Set access tokens for Twitter Api, use Application only Auth instead of the Access Token Auth since it has higher limits rates.
auth = tweepy.AppAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

def saveTweet(row, filename):
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)

counter = 0
for tweets in tweepy.Cursor(api.search, q=QUERY,lang=LANGUAGE, max_id=MAX_ID, since_id=SINCE_ID, count=100).pages():
    for tweet in tweets:
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

            try:
                text = tweet.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                text = tweet.retweeted_status.text

        row = [tweet_id, user_id, user_name, followers, following, likes, retweets, date, reply_to_tweet_id, reply_to_user_id, reply_to_username, user_mentions_ids, user_mentions_names, text, retweet_from_user_id, retweet_from_username, retweet_from_tweet_id]
        saveTweet(row, FILENAME)

        counter += 1
        print(f"tweets fetched: {counter}\r", end="")    


print("Total fetched : " + str(counter))


