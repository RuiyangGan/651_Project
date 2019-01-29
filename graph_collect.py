from github import Github, GithubException, RateLimitExceededException
import numpy as np
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

# Suppose we now collect a bipartite graph, then we will need to keep track
# of information about both the repository and the user(s)
edges = []
num_of_acct = len(g_pool)
i = 0
g = g_pool[i]

# Sending requests to github's server until reaching the rate limits
while g.get_rate_limit().raw_data['core']['remaining'] >= 0:
    try:
        # generate a random number to select a random repository
        rand_int = np.random.randint(5.7e7)
        # collect contributors info of a specific repository
        a = g.get_repos(since=rand_int)[0]
        V = [i.id for i in a.get_contributors()]
        # Store the edges if there are more than two contributors
        if len(V) > 1:
            E = [e for e in product(V, [a.id])]
            edges.extend(E)
    except RateLimitExceededException as e1:
        # If current user's rate limit used up, switch to the next user
        # until no more user in the pool; If no more user is available
        # break out the loop
        if i < num_of_acct-1:
            i += 1
            g = g_pool[i]
            continue
        else:
            break
    except (GithubException, Exception) as e2:
        # For the other kind of exception (such as strange 404 error, etc.), write
        # the elements in vertices and edges into respective text file
        with open('vertices.txt', 'a') as f1:
            f1.write('\n'.join([str(v) for v in vertices]))
        with open('edges.txt', 'a') as f2:
            f2.write('\n'.join([str(e) for e in edges]))
        # Clear list in vertices and edges
        vertices, edges = ([], [])
        continue
