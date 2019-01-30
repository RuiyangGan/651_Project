from github import Github, GithubException, RateLimitExceededException
import numpy as np
import gc
from itertools import product
from configparser import ConfigParser


# Parse the authentification information in the file
# github.auth and create a github 'user pool'
parser = ConfigParser()
parser.read('github.auth')
auth_sections = [i for i in parser.sections()]
g_pool = []
for user in auth_sections:
    auth = {}
    params = parser.items(user)
    for param in params:
        auth[param[0]] = param[1]
    g = Github(**auth)
    g_pool.append(g)

# We can form the sample GitHub network by using its contribute
# and fork features. An edge from a user to a repo is formed if
# the user contributes to the repo; If a user forks from a repo,
# then there exists an edge from this repo to this user. This
# sample graph is a bipartite graph, as every edge connects a user
# to a repo. For the ease of storage, we will use two list to
# represent these two types of edges, called fork_edges and
# contrib_edges

fork_edges = []
contrib_edges = []
g = g_pool[0]
r = []

# Sending requests to github's server until reaching the rate limits
while True:
    try:
        # generate a random number to select a random repository
        # that is not forked from other user
        rand_int = np.random.randint(5.7e7)
        r = g.get_repos(since=rand_int)[0]

        if not r.fork:
            # collect contributors and forks info of a specific repository
            U_contrib = [i.id for i in r.get_contributors()]
            U_fork = [i.id for i in r.get_forks()]
            # Store the randomly sampled fork edges and contributors edge
            contribE = [ce for ce in product(U_contrib, [r.id])]
            forkE = [fe for fe in product([r.id], U_fork)]
            contrib_edges.extend(contribE)
            fork_edges.extend(forkE)
        else:
            continue

    except RateLimitExceededException as e1:
        # If current user's rate limit used up, switch to the next user
        # until no more user in the pool; If no more user is available
        # break out the loop

        # Write the edges into the respective edges file
        if contrib_edges is not None:
            with open('contrib_edges.txt', 'a') as f1:
                f1.write('\n'.join([str(e) for e in contrib_edges]))
                f1.write('\n')
        if fork_edges is not None:
            with open('fork_edges.txt', 'a') as f2:
                f2.write('\n'.join([str(e) for e in fork_edges]))
                f2.write('\n')

        # Clear the edges list
        fork_edges, contrib_edges = ([], [])
        # Check if there is any GitHub instance with remaining rate_limit >= 10
        remain_rates = [g.get_rate_limit().raw_data['core']['remaining']
                        for g in g_pool]
        if any([rl >= 10 for rl in remain_rates]):
            i = np.min(np.where(np.array(remain_rates) >= 10))
            g = g_pool[int(i)]
            continue
        else:
            break

    except (GithubException) as e2:
        # For the other kind of exception (such as 404 and 502 error, etc.), write
        # the elements in vertices and edges into respective text file
        with open('contrib_edges.txt', 'a') as f1:
            f1.write('\n'.join([str(e) for e in contrib_edges]))
            f1.write('\n')
        if fork_edges is not None:
            with open('fork_edges.txt', 'a') as f2:
                f2.write('\n'.join([str(e) for e in fork_edges]))
                f2.write('\n')
        # Clear list in edges
        fork_edges, contrib_edges = ([], [])
        continue
