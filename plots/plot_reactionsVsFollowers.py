import matplotlib.cm as cm
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
import numpy as np

###############################################################################################################
#  IMPORTANT: USE ONLY WITH LIST OF TWEETS CONTAINING A SIGNIFICANT AMOUNT FROM EACH USER PRESENT IN THE LIST #
#  FOR EXAMPLE TWEETS OBTAINED WITH data-mining/getTimelines.py 											  #
###############################################################################################################

FILENAME_TWEET 	= "../data-mining/results/timeline.csv" # List of tweets to consider
OUTPUT_FILENAME = "ReactionsVsFollowers.pdf"			# Filename to store the plot
BUBBLE_SCALE 	= (300, 1600)							# Scale of the bubbles
X_LOG 			= True									# Wether or not to use log scale on X axis
Y_LOG			= True									# Wether or not to use log scale on Y axis


# Load all tweets
tweets = pd.read_csv(FILENAME_TWEET, dtype='str')

tweets.date = pd.to_datetime(tweets.date)
tweets.likes = pd.to_numeric(tweets.likes)
tweets.retweets = pd.to_numeric(tweets.retweets)
tweets.followers = pd.to_numeric(tweets.followers)

# Get number of followers
number_followers = tweets.drop_duplicates(subset="user_name", keep="first").reset_index()[['user_name', 'followers']].set_index('user_name')

# Get average number of tweets per day
min_date = pd.Timestamp((tweets.groupby('user_name')['date'].min().max() + pd.DateOffset(1)).date())
print("Min Date = ", min_date)
tweets_per_day = tweets[tweets.date > min_date].groupby('user_name').resample('d', on='date').count()[['tweet_id']].reset_index()
average_tweets_per_day = tweets_per_day.groupby('user_name').mean().reset_index().set_index('user_name')

total_tweets = tweets[tweets.date > min_date].groupby('user_name').count()[['tweet_id']]
total_tweets.rename(columns={'tweet_id':'count'}, inplace=True)

# Get reactions
reactions = tweets[tweets.date > min_date].groupby('user_name')['likes', 'retweets'].sum().reset_index()
reactions['total'] = reactions.likes + reactions.retweets
reactions = reactions[['user_name', 'total']].set_index('user_name')

# Join infos 
df = reactions.join(average_tweets_per_day).join(number_followers).join(total_tweets).reset_index()
df.rename(columns={'total': 'reactions','tweet_id':'tweets_per_day'}, inplace=True)

print(df.reactions.head())
# Add one for log scale
df.reactions = df.reactions + 1

# Plot 
sns.set_style("whitegrid")
plt.figure(figsize=(20,10))

colors = cm.get_cmap('Blues')(np.linspace(0, 1, df.shape[0]))
#plt.scatter(df.reactions, df.followers, s=df.tweets_per_day, c=colors, alpha=0.8)
ax = sns.scatterplot(x="reactions", y="followers", hue="user_name", size="tweets_per_day", data=df, sizes=BUBBLE_SCALE, palette=colors)

ax.get_legend().remove()
plt.title("Number of reactions versus number of followers", fontsize=25, weight='bold')
plt.xlabel("Number of reactions",fontsize=16, weight='semibold')
plt.ylabel("Number of followers",fontsize=16, weight='semibold')

#For each point, we add a text inside the bubble
for line in range(0,df.shape[0]):
     plt.text(df.reactions[line], df.followers[line], df.user_name[line], horizontalalignment='center', size='small', color='black', weight='semibold')

if Y_LOG:
	plt.yscale('log')
if X_LOG:
	plt.xscale('log')

plt.savefig(OUTPUT_FILENAME)  