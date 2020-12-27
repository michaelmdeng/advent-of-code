# Part 1

We can construct a list of coordinates we have to check by successively
offsetting each point by the slope, so that the starting point `(0, 0)` becomes
`(3, 1)`, then `(6, 2)`, and so on until we reach the bottom of the input grid.

For each of these coordinates, we check the value of the grid at the coordinate
to see if it's a tree. Rather than copying the grid multiple times to the right
once we move past the edge of the initial grid, we instead take the modulus `%`
of the *x*-coordinate with the width of the initial grid - this allows us to
effectively wraparound instead.

# Part 2

We repeat the process for [Part 1](part-1) for the specified slopes, and
multiple the results together.
