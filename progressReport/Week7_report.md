# Week 7 Progress Report

Ruiyang Gan

## Expected task to finish during last Week (Week 6, Feb 19 - Feb 26)

1. Finish the LPAb and its invariants

2. Preparing for presentations

## What I actually did during last Week

1. Finished LPAb

2. Finished preperation for presentation

3. Finished an naive algorithm for computing modularity of given label assignment (can run, is right, but extremely slow); Finished the prototype of a new implementation of modularity computing algorithm that utilizes Spark SQL's and Pandas UDAF (highly-likely faster than the naive implementation, but have not tested yet, and I believe testing will take quite long time and get annoyed by Java's error message)

## Obstacles I faced

1. I still have some issues understanding the Pandas UDAF and aggregate message: Do arguments of pandas udaf have to be serializable? When I run some_pandas_udf(AM.msg, F.first(AM.src['label'], ignorenulls = True)), the error messsage tells me that 'src' is not an aggregate function.

2. The `spark.python.profile.dump` doesn't seem to work as I can not find the dumpled profiling report.


## What I aim to complete this upcoming Week (Week 7, Feb 26 - Mar 02)

1. Finish testing the (faster) implementation of modularity computing algorithm

2. Finish writing the invariant of LPAb that involves using modularity in label selection criterion 

3. Wrap up the project (repository cleaning, writing README.md and Meta.md) and prepare for writing the tutorial
