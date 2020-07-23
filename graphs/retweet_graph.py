import networkx as nx
from networkx.readwrite import json_graph
import pandas as pd
import metis


FILENAME_TWEET 				= "data/trump_tweets.csv"		# CSV of all tweets considered in the graph, build with one of data_mining script
FILENAME_GRAPH				= "trump_graph"					# Output filename

INTERACTION_TREASHOLD 		= 2								# Remove interactions when there are not at least 2 interactions
LARGEST_COMPONENT 			= True 							# Should it save the largest component of the graph or save the whole graph
HITS						= True 							# Compute HITS algorithm for hubs and authorities
PARTITIONS 					= True 							# Partition the graph in two parts
CENTRALITIES				= True 							# Compute centralities stats
PARTISANSHIP				= True 							# Compute partisanship score of nodes works only if PARTITIONS is set to True



# Create target Directory if don't exist
if not os.path.exists('retweet_graphs'):
    os.mkdir('retweet_graphs')

# Load all tweets
tweets = pd.read_csv(FILENAME_TWEET, dtype='str')

# Construct retweet graph 
graph = nx.DiGraph()
for index, tweet in tweets.iterrows():
    print(f"{index}/{tweets.shape[0]}\r", end="")
    if graph.has_node(tweet.user_id):
        graph.nodes[tweet.user_id]['nb_tweets'] += 1
        graph.nodes[tweet.user_id]['followers'] = tweet.followers
    else:
        graph.add_node(tweet.user_id, followers=tweet.followers, label=tweet.user_name, nb_tweets=1)
    
    if str(tweet.retweet_from_id) != "nan":
        if not graph.has_node(tweet.retweet_from_id):
            graph.add_node(tweet.retweet_from_id, label=tweet.retweet_from_username, nb_tweets=0)
            
        # Add or update edge user - interaction
        if graph.has_edge(tweet.user_id, tweet.retweet_from_id):
            graph[tweet.user_id][tweet.retweet_from_id]['weight'] += 1
        else:
            graph.add_edge(tweet.user_id, tweet.retweet_from_id, weight=1)
            
print()
print(f"There are {graph.number_of_nodes()} nodes and {graph.number_of_edges()} \
edges present in the whole Graph")


# Prune edges that do not satisfy INTERACTION_TREASHOLD
edgeToRemove = []
for edge in graph.edges():
    weight = graph.get_edge_data(edge[0], edge[1])['weight']
    if weight < INTERACTION_TREASHOLD:
        edgeToRemove.append(edge)
    
for edge in edgeToRemove:
    graph.remove_edge(edge[0], edge[1])

# Remove isolated nodes
graph.remove_nodes_from(list(nx.isolates(graph)))

# Reset indexes
graph = nx.convert_node_labels_to_integers(graph, label_attribute="tweet_id")
    
print(f"There are {graph.number_of_nodes()} nodes and {graph.number_of_edges()} \
edges present in the Graph after pruning edges")



# Computes HITS algorithm for hubs and authorities
if HITS:
	h, a = nx.hits(graph, max_iter=300, tol=1e-07, nstart=None, normalized=True)
	nx.set_node_attributes(G=graph, name='hub_score', values=h)
	nx.set_node_attributes(G=graph, name='aut_score', values=a)


# Take only largest component of the graph
def connected_component_subgraphs(G):
    for c in nx.connected_components(G):
        yield G.subgraph(c)

if LARGEST_COMPONENT:      
	graph = max(connected_component_subgraphs(graph.to_undirected()), key=len)

	print(f"There are {graph.number_of_nodes()} nodes and {graph.number_of_edges()} \
	edges present in the largest component of the Graph")

if PARTITIONS:
	colors = ['#f22613', '#3498db']
	(edgecuts, parts) = metis.part_graph(graph, 2)
	for i, p in enumerate(parts):
	    graph.nodes[i]['group'] = p
	    graph.nodes[i]['color'] = colors[p]

if CENTRALITIES:
	deg_centrality =  nx.degree_centrality(graph)
	clos_centrality =  nx.closeness_centrality(graph)
	betw_centrality =  nx.betweenness_centrality(graph)

	nx.set_node_attributes(G=graph, name='betw_centrality', values=betw_centrality)
    nx.set_node_attributes(G=graph, name='clos_centrality', values=clos_centrality)
    nx.set_node_attributes(G=graph, name='deg_centrality', values=deg_centrality)

if PARTISANSHIP:
    for node in list(graph.nodes): 
        deg_0 = 0
        deg_1 = 0
        for n in graph.neighbors(node):
            if graph.nodes[n]['group'] == 0:
                deg_0 += graph[node][n]['weight']
            else: 
                deg_1 += graph[node][n]['weight']

        partisanship = max(deg_0,deg_1)/(deg_0 + deg_1)
        graph.nodes[node]['partisanship'] = partisanship


# Save graph to json
json_ = json_graph.node_link_data(graph)
with open("retweet_graphs/" + FILENAME_GRAPH + ".json", 'w') as outfile:
    json.dump(json_, outfile)

# Save graph to Gephi format
nx.write_gexf(graph,"retweet_graphs/" + FILENAME_GRAPH + ".gexf") 




