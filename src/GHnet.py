# pyspark dependency
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql import types
from pyspark.sql.functions import pandas_udf, PandasUDFType
import pyspark.sql.functions as F

# graphframe dependency
from graphframes import GraphFrame
from graphframes.lib import AggregateMessages as AM

# python package dependency
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import sys


class GHnet:
    """
    A wrapper class that represents graphframe object in pyspark with specific
    attributes related to GitHub forking and contribution network
    """

    def __init__(self, vertices_pq, edges_pq):
        # Create configuration for Spark Session
        conf = SparkConf() \
            .setAll([('spark.executor.memory', '16g'),
                     ('spark.executor.cores', '8'),
                     ('spark.cores.max', '8'),
                     ('spark.driver.memory','16g'),
                     ('spark.sql.execution.arrow.enabled', True),
                     ('spark.python.profile', True),
                     ('spark.python.profile.dump',
                      './spark_profile')])

        # Create a spark session
        self.SS = SparkSession.builder.config(conf=conf).getOrCreate()

        # Construct the vertices and edges DataFrame
        vertices_df = self.SS.read.parquet(vertices_pq)
        edges_df = self.SS.read.parquet(edges_pq)

        # Append a column that specifies whether the
        # node is a user or a repo in the table of vertices
        # 1 is for user, 2 is for repo
        nodeTypeUDF = F.udf(lambda i: 1 if i > 0 else 2, types.IntegerType())
        vertices_df = vertices_df.withColumn('nodeType', nodeTypeUDF(F.col('id')))
        # Create the graphframe object
        self.gf = GraphFrame(vertices_df, edges_df)


    def repo_degree_dist(self, deg_type, plot=False, id=None):
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
            degree_dtf = self.gf.inDegrees
        elif deg_type == 'f':
            degree_dtf = self.gf.outDegrees
        else:
            sys.exit("The degree type input is neither fork or contribution!"+
                    "Please try again.")

        colName = degree_dtf.columns[1]
        if id is not None:
            degree_dtf = degree_dtf \
                    .filter("id = " + str(id)).cache()
        else:
            degree_dtf = degree_dtf.filter("nodeType = 2").cache()

        # If asked for plot, plot the empirical degree distribution function
        # of out Degrees of repos
        if plot and (id is None):
            samp_probs = np.linspace(1e-4, 1, int(1e4)).tolist()
            degree_quantile = degree_dtf.stat \
                    .approxQuantile(col=colName,
                                    probabilities=samp_probs,
                                    relativeError=1e-4)
            plt.figure(figsize=(10, 10))
            plt.plot(np.log(degree_quantile),
                     np.log([1 - i for i in samp_probs]),
                     'bo')
            plt.xlabel('Degree')
            plt.ylabel('Probability')
            plt.title('Fork degree distribution' if deg_type == 'f' \
                    else 'Contribution degree distribution')
        return degree_dtf


    def delta(x, y):
            if any([a is None for a in [x,y]]) or (x != y):
                return 0
            else:
                return 1

    def Modularity(gf):
        """ Calculate the modularity of the given graphframe with
        label assignment to each vertex

        Keyword Arguments:

        labels -- A list or a data frame that contains the labeling
        assignment of the vertices. Labels should have the same length
        as the number of rows in the self.gf.vertices data frame
        """
       # Create a new graphframe object with labels attached
        outDegree = gf.outDegrees.select("*").toPandas()
        inDegree = gf.inDegrees.select("*").toPandas()
        E = gf.edges.select("*").toPandas()
        V = gf.vertices.select("*").toPandas()

        f = len(E.loc[E['src'] < 0])
        c = len(E.loc[E['src'] > 0])

        users = V.loc[V['nodeType'] == 1]
        repos = V.loc[V['nodeType'] == 2]

        Q_c = 0
        for user in users.itertuples():
            if len(inDegree.loc[inDegree['id'] == user.id]) != 0:
                k_in = inDegree.loc[inDegree['id'] == user.id]['inDegree']
            else:
                k_in = 0
            for repo in repos.itertuples():
                if len(outDegree.loc[outDegree['id'] == repo.id]) != 0:
                    k_out = outDegree.loc[outDegree['id'] == repo.id]['outDegree']
                else:
                    k_out = 0
                if len(E.loc[(E['src'] == user.id) & (E['dst'] == repo.id)]) != 0:
                    A = 1
                else:
                    A = 0
                Q_c += Q_c + (A - k_in*k_out/c)*delta(user.label, repo.label)
        Q_c /= c

        Q_f = 0
        for repo in repos.itertuples():
            if len(inDegree.loc[inDegree['id'] == repo.id]) != 0:
                k_out = inDegree.loc[inDegree['id'] == repo.id]['inDegree']
            else:
                k_out = 0
            for user in users.itertuples():
                if len(outDegree.loc[outDegree['id'] == user.id]) != 0:
                    k_out = outDegree.loc[outDegree['id'] == user.id]['outDegree']
                else:
                    k_out = 0
                if len(E.loc[(E['src'] == repo.id) & (E['dst'] == user.id)]) != 0:
                    A = 1
                else:
                    A = 0
                Q_f += Q_f + (A - k_in*k_out/c)*delta(user.label, repo.label)
        Q_f /= f

        Q = Q_c + Q_f
        return Q



    def LPAImp(self, numIter, modularity=True):
        """Label propogation algorithm for bipartite networks with synchronous
        updating scheme; Return a data frame with columns which containts the
        vertices ID, labeling assignment and modularity (if specified to
        be returned)

        Keyword Arguments:

        numIter -- Number of iteration for LPAb

        modularity -- A boolean variable indicating whether the
        modularity should be calculated and returned.
        """
        # Assign initial label to the users
        initLabelUDF = F.udf(lambda i, j: i if j == 1 else None,
                             types.IntegerType())
        v = self.gf.vertices.withColumn('label',
                initLabelUDF(F.col('id'), F.col('nodeType')))
        # Add edges for every node that goes to itself
        E_self = self.SS.createDataFrame(v.select(F.col('id')).rdd)
        E = AM.getCachedDataFrame(self.gf.edges.union(
                E_self.withColumn('dst', F.col('id'))
                .withColumnRenamed('id', 'src')))

        # Create a new graphframe object with labels attached
        LPAbgf = GraphFrame(v, E)

        # Create a UDAF (User Defined Aggregate Function) that returns the most frequent
        # label
        @pandas_udf("int", PandasUDFType.GROUPED_AGG)
        def maxLabel_udf(label_list):
            label_list = list(filter(None, label_list))
            LabelCounts = Counter(label_list)
            mostCommonLabels = [i[0] for i in LabelCounts.items()
                                if i[1] == max(LabelCounts.values())]
            return np.random.choice(mostCommonLabels)


        for iter_ in range(numIter):
            for nodeType in [1, 2]:
                # For user and repo nodes, send their labels to
                # their destination nodes in alternating order
                msgForDst = F.when(AM.src['nodeType'] == nodeType,
                                   AM.src['label'])
                # If it's repo's turn to send label to their destinations,
                # also send repo's label's to its contributors
                if nodeType == 2:
                    msgForSrc = F.when(AM.src['nodeType'] == 1, AM.dst['label'])
                else:
                    msgForSrc = None

                # Aggregate messages received from each node
                aggregates = LPAbgf.aggregateMessages(
                    aggCol = maxLabel_udf(AM.msg).alias("aggMess"),
                    sendToDst = msgForDst,
                    sendToSrc = msgForSrc)
                v = LPAbgf.vertices

                # Update Labels for each node; If there is message for
                # the node, update the node's Label
                newLabelCol = F.when(aggregates["aggMess"].isNotNull(),
                                     aggregates["aggMess"]
                                     ).otherwise(v['label'])
                # Outer join aggregates and vertices
                vNew = (v
                    .join(aggregates, on=(v['id'] == aggregates['id']),
                          how='left_outer').drop(aggregates['id'])
                    # Compute new column
                    .withColumn('newLabel', newLabelCol)
                    # Drop messages
                    .drop('aggMess')
                    # Drop old labels
                    .drop('label')
                    .withColumnRenamed('newLabel', 'label')
                )

                cachedvNew = AM.getCachedDataFrame(vNew)
                LPAbgf = GraphFrame(cachedvNew, E)
        # Delete the edges that goes from itself
        LPAbgf = GraphFrame(LPAbgf.vertices, self.gf.edges)
        return LPAbgf



    def LPAbp(self, type = "Vanila", modularity=True):
        """"""
        pass


