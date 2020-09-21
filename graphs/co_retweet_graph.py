import networkx as nx
from networkx.readwrite import json_graph
import pandas as pd
import os
import json


FILENAME_TWEET              = "../data-mining/results/police_tweets.csv"        # CSV of all tweets considered in the graph, build with one of data_mining script
FILENAME_GRAPH              = "police_graph"                    # Output filename

INTERACTION_TREASHOLD       = 2                             # Remove interactions when there are not at least 2 interactions
LARGEST_COMPONENT           = True                          # Should it save the largest component of the graph or save the whole graph
PARTITIONS                  = True                          # Partition the graph in two parts, need to install metis
CENTRALITIES                = True                          # Compute centralities stats
PARTISANSHIP                = True                          # Compute partisanship score of nodes works only if PARTITIONS is set to True



# Create target Directory if don't exist
if not os.path.exists('co_retweet_graphs'):
    os.mkdir('co_retweet_graphs')

# Load all tweets
tweets = pd.read_csv(FILENAME_TWEET, dtype='str')

# Construct retweet matrix 
users = tweets.user_name.unique()
retweeted_users = tweets[~tweets.retweet_from_username.isna()].retweet_from_username.unique()
retweet_matrix = pd.DataFrame(0, index =users, columns =retweeted_users) 

for index, tweet in tweets.iterrows():
    print(f"{index}/{tweets.shape[0]}\r", end="")
    if str(tweet.retweet_from_tweet_id) != "nan":
        retweet_matrix.loc[tweet.user_name, tweet.retweet_from_username] += 1

# Construct co-retweet matrix
co_retweet_matrix = pd.DataFrame(0, index =retweeted_users, columns =retweeted_users)
for index, row in retweet_matrix.iterrows():  
    for account in row[row > 1].index:   
        co_retweet_matrix.loc[account, account] += 1
        if len(row[row > 1]) > 1:    
            for co_account in row[row > 1].index:
                if account != co_account:
                    co_retweet_matrix.loc[account, co_account] += row[row > 1].sum()


# build graph from co-retweets
graph = nx.Graph()
for node in co_retweet_matrix.index:
    graph.add_node(node, nb_users=int(co_retweet_matrix.loc[node, node]))
    
for index, row in co_retweet_matrix.iterrows():
    for column in row[row > 1].index:
        if not graph.has_edge(index, column) and index!=column:
            graph.add_edge(index, column, weight=int(row[column]))
            
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

# Take only largest component of the graph
def connected_component_subgraphs(G):
    for c in nx.connected_components(G):
        yield G.subgraph(c)

if LARGEST_COMPONENT:      
    graph = max(connected_component_subgraphs(graph.to_undirected()), key=len)

    print(f"There are {graph.number_of_nodes()} nodes and {graph.number_of_edges()} \
    edges present in the largest component of the Graph")

# Reset indexes
graph = nx.convert_node_labels_to_integers(graph, label_attribute="label")
    
print(f"There are {graph.number_of_nodes()} nodes and {graph.number_of_edges()} \
edges present in the Graph after pruning edges")

if PARTITIONS:
    import metis
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

if PARTITIONS and PARTISANSHIP:
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
with open("co_retweet_graphs/" + FILENAME_GRAPH + ".json", 'w') as outfile:
    json.dump(json_, outfile)

# Save graph to Gephi format
nx.write_gexf(graph,"co_retweet_graphs/" + FILENAME_GRAPH + ".gexf") 

