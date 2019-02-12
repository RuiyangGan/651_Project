# Week 5 Progress Report

Ruiyang Gan

## Expected task to finish during last Week (Week 3, Feb 5 - Feb 12)

1. Catch up on my schedule to build a graph data strucutre using graphframe and PySpark. Read through the two tutuorials on graphframe and parquet.

2. Conduct EDA on the contribution-fork network

## What I actually did during last Week

1. I have created the grapgframe object in Spark (using pyspark and pyspark.sql)

2. I have written some simple EDA functionalities (such as empricial fork/contribution (in/out) degree distrbution)

## Obstacles I faced

1. Setting up the pyspark/graphframe environment initially cost me some trouble. But it is not a very big difficulty as the error message is somewhat helpful

2. I noticed that create a dataframe in pyspark.sql is very slow in a spark session. I found a post on github.io which enlighten me on how to speed up the data frame construction by enabling the spark arrow setting in config of the Spark Session.

3. The approximate quantile function implemented in pyspark.sql.DataFrame.stat is slow when the table has around 1 million rows. I don't know how to speed up that calculation.

4. I didn't have an idea on how to use the message passing functionality to implement algorithms such as graph spectrum and other community detection algorithms.


## What I aim to complete this upcoming Week (Week 5, Feb 12 - Feb 19)

1. Learn more about the message-passing functionality in graphframe

2. Implement more graph EDA functionalities (such as Graph spectrum and/or laplacian)

