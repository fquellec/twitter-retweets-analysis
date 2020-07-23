import networkx as nx
from networkx.readwrite import json_graph
import pandas as pd
import metis


FILENAME_TWEET 				= "data/trump_tweets.csv"		# CSV of all tweets considered in the graph, build with one of data_mining script
FILENAME_GRAPH				= "trump_graph"					# Output filename

INTERACTION_TREASHOLD 		= 2								# Remove interactions when there are not at least 2 interactions
LARGEST_COMPONENT 			= True 							# Should it save the largest component of the graph or save the whole graph
PARTITIONS 					= True 							# Partition the graph in two parts
CENTRALITIES				= True 							# Compute centralities stats
PARTISANSHIP				= True 							# Compute partisanship score of nodes works only if PARTITIONS is set to True



# Create target Directory if don't exist
if not os.path.exists('co_retweet_graphs'):
    os.mkdir('co_retweet_graphs')

# Load all tweets
tweets = pd.read_csv(FILENAME_TWEET, dtype='str')

