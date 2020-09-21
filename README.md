# Retweet networks and analysis of twitter discussions

Intro BLABLABLA 

---

## Workspace

### Data Mining

We propose three ways to collect tweets in the [data-mining](https://github.com/Fanfou02/twitter-retweets-analysis/tree/master/data-mining) folder : 
- `searchKeyword.py`: collect tweets from the twitter api using the search call, by specifying one or more keywords or hashtags, we can retrieve up to the last week of the tweet corresponding to this keyword(s). (with the free twitter license)
- `streamUsers.py`: use the streaming api of twitter to fetch in real time all tweets related to the list of accounts we specify.
- `getTimelines.py`: retrieve up to 3200 tweets (depending on the license) of each user we specify.

### Graph generation

Once we have our dataset of tweets, we can generate two type of interaction graph : 
- Retweet Graph: BLABLABLA
- Co-retweet Graph: co-retweeting is the act of a single user retweeting two - or more - different accounts. These acts are used to create between accounts co-returned in the network. The more users retweet these two accounts, the more likely they are to retweet, the more the advantage gains weight

Example with keyword "police" in french: 
<div style="text-align:center"><img src="https://raw.githubusercontent.com/Fanfou02/twitter-retweets-analysis/master/imgs/police_graph.png" /></div>

### Plots
- Reactions versus Number of followers
<div style="text-align:center"><img src="https://raw.githubusercontent.com/Fanfou02/twitter-retweets-analysis/master/imgs/ReactionsVsFollowers.png" /></div>

- Partisanship
<div style="text-align:center"><img src="https://raw.githubusercontent.com/Fanfou02/twitter-retweets-analysis/master/imgs/partisanship.png" /></div>

## Getting Started

### Clone

> Clone this repo to your local machine using 
```shell
$ git clone https://github.com/com-480-data-visualization/com-480-project-coronateam.git
```

### Install Dependencies

> Go to the `docs` folder with your terminal and install dependencies by executing the following

```shell
$ npm install
```

### Get some tweets
BLABLABLA

### Build the retweet/co-retweet graph
BLABLABLA

### Plot your results
BLABLABLA


## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2020 © François Quellec
