# Week 3 Progress report

Ruiyang Gan

## Expected tasks to be completed during Week 2

1. Learning about GitHub's REST API for publicly available user information

2. Learning about fundamental data structure in Spark

## What I really did during Week 2 and obstacles I faced

I spent most of the time (on stat 651) on figuring out how to use the Python wrapper (PyGithub)
and figuring out an efficient way (in rate limit sense) to sample vertices and edges from the
huge population graph from GitHub. I use the incident-subgraph sampling approach to sample the
the networks, which means we do a simple random sampling from the population edges. Under the context
of GitHub collaboration networks, we will randomly draw a GitHub repositories and retrieve the
contributing users (their id). Use these informations, we can then form a subgraph of the population graph.
_Note_: This is not a 'collaborators' networks, preciesly, as we do not have direct access to the collaborators information for a certain repository unless we have push access to that repo. Thus we
can only get the list of contributors. But if weregard committing some code to the same project in a broader sense of collaboration, this is a collaboration network.

Currently, I have collected around 12 million edges and vertices (due to the way we sample the population graph, we are expected to see repeated vertices in our collected vertices table, and I'm glad to actually see such repetitive vertices). However, as the data aggregates, the data file itself become large and hard to transmit from the local machine (2 Gigabytes currently for the text file containing 12 million edges) to other machines.

During Week 2, I have not yet started to read about basics of Spark, thus I'm a little behind schedule.

## What to do during in upcoming Week (Week 3)

1. Continue sampling from the population graph

2. Getting started on AWS and migrate the (locally) collected data to the cloud storage

3. Learning about Spark and graph building in Spark (prepare for EDA in Week 4)