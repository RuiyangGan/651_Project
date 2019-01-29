The edges.txt contains edges in a bipartite graph. The contribution networks of GitHub can be divided into two
parts: Users and Repositories. If a GitHub repo is randomly sampled, then we collect all the users who have contributed
to this particular repo. Thus we can form the edges between the user(s) and this particular repo. The file of edges
have this particular strucutre:
edges.txt:
User_ID  Repo_ID

In this way, we have a biparite graph G = (E, U, R), where e \in E is (u,r) for u \in U, r \in R. In this case,
U is the set of users and R is the set of repos.
