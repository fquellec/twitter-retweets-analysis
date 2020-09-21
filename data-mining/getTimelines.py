import tweepy
import json
import os
import csv
import pandas as pd
import credentials

ACTORS                      = ['@lemondefr','@courrierinter','@leJDD','@humanite_fr',
                            '@LEXPRESS','@libe','@LesEchos','@lobs','@MarianneleMag',
                            '@Le_Figaro','@AlterEco_','@_polemia','@sputnik_fr','@Europe_Israel',
                            '@Breizh_Info','@BVoltaire','@RTenfrancais','@InfoMdia','@Valeurs',
                            '@tvlofficiel','@LePoint','@F_Desouche','@Dreuz_1fo','@ndffr','@FrDesouche',
                            '@1RiposteLaique','@Contreinfo','@LaManifPourTous','@RNational_off',
                            '@EetR_National','@lenouvelliste','@letemps','@24heuresch','@20min',
                            '@20minutesOnline','@tdgch','@tagesanzeiger','@Blickch','@derbund',
                            '@LuzernerZeitung','@lecourrier','@laliberte','@heidi_news','@Lematinch',
                            '@BernerZeitung','@AargauerZeitung','@RTSinfo','@CdT_Online','@watson_news',
                            '@srfnews','@laregione','@RSInews']  
                                                                          
                             # List of twitter accounts to retrieve
FILENAME                    = 'results/timeline.csv'                                                                    # Resulting file
LANG                        = 'fr'                                                                              # Restrict the query to a specific language ('fr', 'en'), None for all
MAX_TWEETS_PER_ACCOUNT      = 4000                                                                              # Max number of tweets to retrieve by account, if free twitter license max is 3200


# Create target Directory if don't exist
if not os.path.exists('results'):
    os.mkdir('results')

auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

header = ['tweet_id', 'user_id', 'user_name', 'followers', 'following', 'likes', 
          'retweets', 'date', 'reply_to_tweet_id', 'reply_to_user_id', 'reply_to_username', 
          'user_mentions_ids', 'user_mentions_names', 'text', 'retweet_from_user_id', 
          'retweet_from_username', 'retweet_from_tweet_id', 'urls']

def saveTweet(row, filename):
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)

for actor in ACTORS: 
    min_id = None

    if os.path.exists(FILENAME):
        df = pd.read_csv(FILENAME)
        df = df[df.user_name == actor[1:]]
        df.date = pd.to_datetime(df.date)
        ids = df.tweet_id.values
        counter = len(ids)        
        if counter:
            min_id = int(df.loc[df.date.idxmax()].tweet_id)

    else: 
        with open(FILENAME, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)
        counter = 0
    print(min_id)
    for tweets in tweepy.Cursor(api.user_timeline, since_id=min_id, screen_name=actor, tweet_mode="extended", lang=LANG, count=100).pages(MAX_TWEETS_PER_ACCOUNT/100):
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

            urls=[]
            for url in tweet.entities['urls']:
                urls.append(url['expanded_url'])

            try:
                text = tweet.extended_tweet["full_text"]
            except AttributeError:
                text = tweet.full_text

            retweet_from_user_id = None
            retweet_from_username = None
            retweet_from_tweet_id = None

            if hasattr(tweet, "retweeted_status"):  
                retweet_from_user_id = tweet.retweeted_status.user.id_str
                retweet_from_username = tweet.retweeted_status.user.screen_name
                retweet_from_tweet_id = tweet.retweeted_status.id_str

            row = [tweet_id, user_id, user_name, followers, following, likes, retweets, date, reply_to_tweet_id, reply_to_user_id, reply_to_username, user_mentions_ids, user_mentions_names, text, retweet_from_user_id, retweet_from_username, retweet_from_tweet_id, urls]
            saveTweet(row, FILENAME)

            counter += 1
            print(f"{actor} -> Total fetched : {counter}\r", end="")    


    print(actor, " -> Total fetched : " + str(counter))


