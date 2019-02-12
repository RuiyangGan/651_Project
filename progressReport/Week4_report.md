# Week 4 Progress Report

Ruiyang Gan

## Expected task to finish during last Week (Week 3, Jan 29 - Feb 5)

1. Construct the GitHub’s collaborator network in Spark using PySparkand GitHub’s REST API

## What I actually did during last Week

1. I modified the scraping script used to retrieve user and repositories information on GitHub. Now the statistical network that I collected is in the form of a bipartite directed graph. The vertices can now be patitioned into two independent and disjoint sets, Users and Repos. Let u1 be a user and r1 a repo, then there is an edge (u1, r1) if user u1 contributes to the repo r1. If a user u2 owns a repo r2 that is forked from r1, then there is an edge (r1, u2).

## Obstacles I faced

1. I'm a little behind schedule as I haven't formed a Graph Data Structure in Spark yet. I came across an tutorial on graphframe and PySpark <https://docs.databricks.com/spark/latest/graph-analysis/graphframes/user-guide-python.html>. However, I have not yet had time to read through it and construct the collaboration network using the edges and node that I have collected.

2. I have not yet looked at the details of Apache Parquet and have not thought of a way to continuously store the edges in columnar storage format as I scrape user and repo information from GitHub. This documentation contains details <https://arrow.apache.org/docs/python/parquet.html#writing-to-partitioned-datasets>.

## What I aim to complete this upcoming Week (Week 4, Feb 5 - Feb 12)

1. Catch up on my schedule to build a graph data strucutre using graphframe and PySpark. Read through the two tutuorials on graphframe and parquet.

2. Conduct EDA on the contribution-fork network
