def parse_edges(edge_file, edge_type):
    with open(edge_file, 'r') as f:
        edge_lines = f.readlines()
        edges = []
    for l in edge_lines:
        if len(l.strip('\n')) != 0:
            e = l.strip('\n').split(',')
            # To save space, we will use numeric IDs, Since both users and repos
            # has numeric IDs, we will encode them in different ways to reduce memory
            # footprint. The positive numeric ID will be user ID, and the negative
            # numeric ID will be repository ID
            if edge_type == 'c':
                a = (int(e[0][1:]), -int(e[1][1:-1]))
            elif edge_type == 'f':
                a = (-int(e[0][1:]), int(e[1][1:-1]))
            edges.append(a)
    return edges
