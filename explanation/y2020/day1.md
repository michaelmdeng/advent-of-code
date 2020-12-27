# Part 1

The brute-force algorithm is to perform an *n^2* traversal of the input list by
iterating through each element, and for each element, iterate through *every
other* element of the list, checking each pair if they sum to 2020.

However, an alternative that only performs a single traversal of the input list
is to iterate through the list a single time and store the differences of 2020
and each element in a set. When we encounter an element that is present in our
difference set, we know the values of the two elements that sum to 2020. This
algorithm has only *O(n)* time-complexity, at the cost of *O(n)*
space-complexity.

# Part 2

Similar to [Part 1](#part-1), the brute-force algorithm is to perform an *n^3*
traversal of the input list, taking three elements at a time and checking if
they sum to 2020.

Once again, we can reduce the time-complexity of the algorithm from *O(n^3)* to
*O(n^2)* if we store differences. In this version, we store differences of 2020
and all pairwise sums in a set (as well as the specific entry pair itself),
requiring *O(n^2)* space. Once we've built up our set of pairwise differences,
we can iterate through the list a single time and check if an entry exists in
our difference set - if it does, we can multiply all three elements together to
yield the result.
