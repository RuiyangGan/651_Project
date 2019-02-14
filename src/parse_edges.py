import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os.path


def parse_edges(edge_file, edge_type):
    """ This function parse different type of edges into a list
    and return a parquet file that is in arrow (columnar storage)
    format.

    Keyword Arguments:

    edge_file -- A .txt file that contains edges between repos and users

    edge_type -- A single character indicating the type of edges; 'f' means
    fork edges (repo to usr), 'c' means contribution edge (usr to repo)
    """
    with open(edge_file, 'r') as f:
        edge_lines = f.readlines()
        edges = []
    for l in edge_lines:
        if len(l.strip('\n')) != 0:
            e = l.strip('\n').split(',')
            # To save space, we will use numeric IDs, Since both users and
            # repos has numeric IDs, we will encode them in different ways
            # to reduce memory footprint. The positive numeric ID will be
            # user ID, and the negative numeric ID will be repository ID
            if edge_type == 'c':
                a = (int(e[0][1:]), -int(e[1][1:-1]))
            elif edge_type == 'f':
                a = (-int(e[0][1:]), int(e[1][1:-1]))
            edges.append(a)
    return edges


def list_to_pq(contrib_edges, fork_edges, data_dir):
    """This function takes in list of two types of edges
    in the fork/contribution network and create two parquet
    file (vertices.parquet, edges.parquet) that is in columnar
    storage format.

    Keyword Arguments:

    fork_edges, contrib_edges -- Two list of edges that contains
    tuples that contains the edges in the network.

    data_dir -- The source directory that list_to_pq write the
    parquet file to.
    """
    edges = fork_edges + contrib_edges
    # Create the list of vertices
    vertices = [(v,) for v in set([l for e in edges for l in e])]
    vertices_pd = pd.DataFrame(vertices, columns = ['id'])
    edges_pd = pd.DataFrame(edges, columns = ['src', 'dst'])
    edges_table = pa.Table.from_pandas(edges_pd)
    vertices_table = pa.Table.from_pandas(vertices_pd)

    # Write to data folder in parquet format
    pq.write_table(vertices_table, os.path.join(data_dir, 'vertices.parquet'))
    pq.write_table(edges_table, os.path.join(data_dir, 'edges.parquet'))


def txt_to_pq(contrib_edge_file, fork_edge_file, data_dir = 'data'):
    """ This function parse different type of edges into a list
    and return a parquet file that is in arrow (columnar storage)
    format.

    Keyword Arguments:

    contrib_edge_file, fork_edge_file -- Two text files that contains
    different types of edges. 
    """
    contrib_edges, fork_edges = (parse_edges(contrib_edge_file, 'c'),
                                 parse_edges(fork_edge_file, 'f'))
    list_to_pq(contrib_edges, fork_edges, data_dir)
