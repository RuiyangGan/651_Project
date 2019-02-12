The fork_edges.txt and contrib_edges.txt are the files that contain edges between GitHub
users and GitHub repos. 

fork_edges.txt contains the edges from GitHub repos to GitHub users. Such edge is formed if 
the user forks from a repo.
The structure is as following:
from_node   to_node
repo_id     user_id

contrib_edges.txt contains the edges from GitHub users to GitHub repos. Such edges is formed
if the user contributes to a repo.
The strucutre is as following:
from_node   to_node
user_id     repo_id

In this way, we have a biparite graph $G = (E, U, R)$, where $e \in E$ is $(u,r)$ for  $u \in U$, $r \in R$. In this case, U is the set of users and R is the set of repos.
