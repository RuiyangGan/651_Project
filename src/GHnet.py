from pyspark.sql import SparkSession
from pyspark import SparkConf
import numpy as np
from graphframes import *
import matplotlib.pyplot as plt
import os.path
import sys

class GHnet:
    """
    A wrapper class that represents graphframe object in pyspark with specific
    attributes related to GitHub forking and contribution network
    """

    def __init__(self, vertices_pq, edges_pq):
        # Create configuration for Spark Session
        conf = SparkConf() \
            .setAll([('spark.executor.memory', '8g'),
                     ('spark.executor.cores', '3'),
                     ('spark.cores.max', '3'),
                     ('spark.driver.memory','8g'),
                     ('spark.sql.execution.arrow.enabled', True)])

        # Create a spark session
        self.SS = SparkSession.builder.config(conf=conf).getOrCreate()

        # Construct the vertices and edges DataFrame
        vertices_df = self.SS.read.parquet(vertices_pq)
        edges_df = self.SS.read.parquet(edges_pq)

        # Create the graphframe object
        self.gf = GraphFrame(vertices_df, edges_df)


    def degree_dist(self, deg_type, plot=False, id=None):
        """A function that returns a py

        Keyword Arguments:

        deg_type -- A character indicates the degree type of GitHub's repo.
        'f' indicates the fork degree (out degree) of the repo, while
        'c' indicates the contribution degree (in degree) of the repo

        plot -- A boolean type indicates whether the log-log approxmiate
        degree emprical ecdf will be plotted

        id -- GitHub repository ID; If None is provieded, return all
        of the fork degrees
        """
        if deg_type == 'c':
            degree_dtf = self.gf.outDegrees
        elif deg_type == 'f':
            degree_dtf = self.gf.inDegrees
        else:
            sys.exit("The degree type input is neither fork or contribution!"+
                    "Please try again.")

        colName = degree_dtf.columns[1]
        if id is not None:
            degree_dtf = degree_dtf \
                    .filter("id = " + str(id)).cache()
        else:
            degree_dtf = degree_dtf.filter("id < 0").cache()

        # If asked for plot, plot the empirical degree distribution function
        # of out Degrees of repos
        if plot and (id is None):
            samp_probs = np.linspace(0, 1, int(1e3)).tolist()
            degree_quantile = degree_dtf.stat \
                    .approxQuantile(col=colName,
                                    probabilities=samp_probs,
                                    relativeError=1e-4)
            plt.figure(figsize=(10, 10))
            plt.axis([0,
                     degree_dtf.agg({colName:'max'}) \
                             .collect()[0], 0, 1])

            plt.plot(np.log(degree_quantile),
                     np.log([1 - i for i in samp_probs]),
                     'bo')
            plt.xlabel('Degree')
            plt.ylabel('Probability')
            plt.title('Fork degree distribution' if deg_type == 'f' \
                    else 'Contribution degree distribution')
        return degree_dtf


    def userPageRank(self):
        pass


    def repoPageRank(self):
        pass


    def graphSpectrum(self):
        pass


