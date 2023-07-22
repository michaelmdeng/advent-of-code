# Part 1

For each point, we calculate the # of points that are adjacent. The exposed
surface area of the point is 6 - the # of adjacent points. Sum over all points
to get the total surface area.

Our initial brute-force approach does an *O(n^2)* comparison of each point to
every other point to determine which pairs are adjacent.

A better approach simplifies these comparisons through memory and a dictionary.
We first place each point into the dictionary. For each point, we examine each
of the 6 adjacent points and determine how many of them exist in our point
dictionary -- the # that exist is the # of adjacent points.

# Part 2

We can calculate the exposed surface area of the droplet by ignoring the
interior trapped points, or equivalently, treating it as if those interior
trapped points were part of the droplet itself.

Thus, we need a way to determine which points are trapped within the droplet
volume.

We can visualize our bounding volume as consisting of three types of points: 1)
solid points of the droplet, 2) interior points trapped by the droplet, and 3)
exterior points outside the droplet.

We are given 1) as input. Determining 2) directly is difficult -- however, we
can determine 3) and then calculate 2) as the complement of 1) + 3).

To determine the exterior points on the outside of the droplet, we can use graph
search and connected components to fill/mark the exterior points. Starting from
1 exterior point, visit all adjacent points in the volume and mark them if they
are not in the input 1). We implement this using BFS so that we avoid hitting
Python's maximum recursion depth in a DFS approach.

Because our BFS only visits adjacent points, we are guaranteed to only mark
points that are reachable from the exterior of the droplet. Inverting this set
of exterior points along with the set of input points results in only the
interior points remaining.

We can then treat these interior points as if they were part of our input point
set and calculate the surface area of the resulting solid.
