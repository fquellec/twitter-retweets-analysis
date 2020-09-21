# Retweet networks and analysis of twitter discussions

In this repo, we propose several tools to easily get an overview of the debates on twitter using Python. We first propose three ways to collect tweets with the twitter API, then we build different types of interactions graphs with these tweets to visualize the polarization in the discussions and obtain statistics on the actors of the flows. Finally, with the statistics obtained from the graphs we added previously, we propose two possible visualizations to interpret some of the previous results.

---

## Workspace

### Data Mining

We propose three ways to collect tweets in the [data-mining](https://github.com/Fanfou02/twitter-retweets-analysis/tree/master/data-mining) folder : 
- `searchKeyword.py`: collect tweets from the twitter api using the search call, by specifying one or more keywords or hashtags, we can retrieve up to the last week of the tweet corresponding to this keyword(s). (with the free twitter license)
- `streamUsers.py`: use the streaming api of twitter to fetch in real time all tweets related to the list of accounts we specify.
- `getTimelines.py`: retrieve up to 3200 tweets (with the free twitter license) of each user we specify.

### Graph generation

Once we have gathered our tweets, we can generate two type of interaction graph in the [graphs](https://github.com/Fanfou02/twitter-retweets-analysis/tree/master/graphs) folder: 
- Retweet Graph: One of the more popular way to visualize interactions on twitter, a retweet graph is a directed graph
of users that have participated in the discussion on a specific topic/keyword. Each node correspond to a twitter account and a directed edge between to nodes `u` and `v` indicates that user `v` has been retweeted by user `u`. Since retweet often indicates endorsement ([source](http://cs.wellesley.edu/~pmetaxas/WorkingPapers/Retweet-meaning.pdf)), we can use this kind of graph to detect polarization and communities in twitter discussions.

- Co-retweet Graph: The co-retweeted network is constructed as the undirected weighted graph that connects highly visible accounts who have been retweeted by members of the audience during some real-time event. If two accounts have been retweeted several times by the same people, an edge is added between theses two accounts. The co-retweeted network can be seen as a form of consulting the opinion of the crowd that is following the discussion about the similarity (or difference) of positions expressed by the highly visible accounts. When applied to polarized discussions, it can be applied to retrieve orientation of major players in the discussion. [source](https://pdfs.semanticscholar.org/02a3/7c9c0f57cc60ab282fd39367cb93dd1b97b4.pdf)

These two interaction graphs can be used for different purposes, one is directed and allows us to use well-known algorithms such as HITS for computing hubs and authorities. Whereas the other one highlights the important actors and better represents the polarization in the twitter debates.

Example of co-retweet network with keyword "police" in french: 
<div style="text-align:center"><img src="https://raw.githubusercontent.com/Fanfou02/twitter-retweets-analysis/master/imgs/police_graph.png" /></div>

### Plots
In this section, we offer two ways to visualize some of the information we have from the data we have collected. 

- Reactions versus Number of followers: This plot can help us better understand which account generates the most reactions in relation to its number of followers, we only need a tweet list to generate the plot.

<div style="text-align:center"><img src="https://raw.githubusercontent.com/Fanfou02/twitter-retweets-analysis/master/imgs/ReactionsVsFollowers.png" /></div>

- Partisanship: This plot allows us to visualize the orientation of some twitter accounts in a discussion, for now it only makes sense when a discussion is polarized on two opposite sides, it calculates the number of links a node shares with each side of the discussion. (Carefully check that the retweet or co-retweet graph is polarized on two opposite sides and that the partition is well defined).

<div style="text-align:center"><img src="https://raw.githubusercontent.com/Fanfou02/twitter-retweets-analysis/master/imgs/partisanship.png" /></div>

## Getting Started

### Clone

Clone this repo to your local machine using 
```shell
$ git clone https://github.com/Fanfou02/twitter-retweets-analysis.git
```

### Install Dependencies

Go to the `docs` folder with your terminal and install dependencies by executing the following

```shell
$ npm install
```

If you want to use the partitioning function, which is useful for calculating partitions and visualizing polarization in graphs, install METIS for python following instructions [here](https://metis.readthedocs.io/en/latest/).

### Get some tweets
First we need some data to generate interactions graphs, go to the [data-mining](https://github.com/Fanfou02/twitter-retweets-analysis/tree/master/data-mining) folder and choose one of the three methods. For example, if you want to search for all discussions mentionning the keyword `police` in the last week, open `searchKeyword.py`, change the query option and execute the following command: 

```shell
$ python3 searchKeyword.py
```

Then, a CSV file in the directory `results` will be generated with all the tweets corresponding to your query

### Build the retweet/co-retweet graph
Once you got some tweets, go to the [graphs](https://github.com/Fanfou02/twitter-retweets-analysis/tree/master/graphs) folder and choose between co-retweet and retweet graph. Open the corresponding python file and change the input/output filenames variables with the previously generated csv file. For example, open [retweet_graph.py](https://github.com/Fanfou02/twitter-retweets-analysis/tree/master/graphs/retweet_graph.py) and change the following variable as follow:

```shell
FILENAME_TWEET              = "../data-mining/results/police_tweets.csv"        # CSV of all tweets considered in the graph, build with one of data_mining script
FILENAME_GRAPH              = "police_graph"                                    # Output filename
```

Then execute `retweet_graph.py`: 

```shell
$ python3 retweet_graph.py
```

Finally, a JSON file and a GEPHI file containing the produced graph will be generated in the retweet_graphs folder. You can view the graph directly using [Gephi](https://gephi.org/) or [networkx](https://networkx.github.io/)

### Plot your results

Not Implemented yet

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2020 © François Quellec
