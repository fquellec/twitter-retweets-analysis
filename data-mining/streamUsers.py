import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from credentials import *
import tweepy

count = 0
class StdOutListener(StreamListener):
    def on_status(self, status):
        global count
        json_str = json.dumps(status._json)
        with open("/mnt/datastore/data/medias/all_medias_stream.csv", 'a') as fout:
            fout.write(json_str)
            fout.write("\n")
        count += 1
        print("{}\r".format(count), end="")
    def on_error(self, status_code):
        if status_code == 420:
            # Returning False in on_error disconnects the stream
            return False

consumer_key        = CONSUMER_KEY
consumer_secret     = CONSUMER_SECRET
access_token        = ACCESS_TOKEN
access_token_secret = ACCESS_TOKEN_SECRET

l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l, tweet_mode='extended')

#with open("/home/fanfou/re-info-analysis/data/reinfo_ids_extended.txt") as fin:
#    queries = [l.strip().split(';')[1] for l in fin.readlines()]
user_names = ['@lemondefr','@courrierinter','@leJDD','@humanite_fr','@LEXPRESS','@libe','@LesEchos','@lobs','@MarianneleMag','@Le_Figaro','@AlterEco_','@_polemia','@sputnik_fr','@Europe_Israel','@Breizh_Info','@BVoltaire','@RTenfrancais','@InfoMdia','@Valeurs','@tvlofficiel','@LePoint','@F_Desouche','@Dreuz_1fo','@ndffr','@FrDesouche','@1RiposteLaique','@Contreinfo','@LaManifPourTous','@RNational_off','@EetR_National','@lenouvelliste','@letemps','@24heuresch','@20min','@20minutesOnline','@tdgch','@tagesanzeiger','@Blickch','@derbund','@LuzernerZeitung','@lecourrier','@laliberte','@heidi_news','@Lematinch','@BernerZeitung','@AargauerZeitung','@RTSinfo','@CdT_Online','@watson_news','@srfnews','@laregione','@RSInews']
queries = []
api = tweepy.API(auth)
for user_name in user_names:
    user = api.get_user(user_name)
    queries.append(user.id_str)

print(queries)

while True:
    try:
        stream.filter(follow=queries)
    except Exception as err:
        print(err)
