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
g = g_pool[0]

# Sending requests to github's server until reaching the rate limits
while True:
    try:
        # generate a random number to select a random repository
        rand_int = np.random.randint(5.7e7)
        # collect contributors info of a specific repository
        a = g.get_repos(since=rand_int)[0]
        V = [i.id for i in a.get_contributors()]
        # Store the randomly sampled edges
        E = [e for e in product(V, [a.id])]
        edges.extend(E)

    except RateLimitExceededException as e1:
        # If current user's rate limit used up, switch to the next user
        # until no more user in the pool; If no more user is available
        # break out the loop

        # Write the edges into the edges.txt file
        with open('edges.txt', 'a') as f:
            f.write('\n'.join([str(e) for e in edges]))
            f.write('\n')
        # Clear the edges list
        edges = []
        # Check if there is any GitHub instance with remaining rate_limit >= 10
        remain_rates = [g.get_rate_limit().raw_data['core']['remaining']
                        for g in g_pool]
        if any([rl >= 10 for rl in remain_rates]):
            i = np.min(np.where(np.array(remain_rates) >= 10))
            g = g_pool[int(i)]
            continue
        else:
            break

    except (GithubException, Exception) as e2:
        # For the other kind of exception (such as 404 and 502 error, etc.), write
        # the elements in vertices and edges into respective text file
        with open('edges.txt', 'a') as f:
            f.write('\n'.join([str(e) for e in edges]))
            f.write('\n')
        # Clear list in edges
        edges = []
        continue
