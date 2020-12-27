# Part 1

A brute-force algorithm is to perform an *n^2* traversal of the input list by
iterating through each element, and for each element, iterate through *every
other* element of the list, checking each pair if they sum to 2020.

## Traversals

Rather than performing an index-based iteration of the input list, we can
iterate using the `tails` method, which returns all successive tails of the list
(ie the first through the last element, followed by the second through the last
element, then the third through the last element, and so on until the end of the
list). For each tail, we treat the head as the outer traversal, and the rest of
the tail as the inner traversal.

For those less familiar with these Scala built-in methods, we present different
versions of this *n^2* traversal for comparison:

```scala
for (i <- 0 until entries.size - 1) {
  for (j <- i + 1 until entries.size) {
    entries(i) + entries(j) == 2020
  }
}

(0 until entries.size - 1).map(i => {
  (i + 1 until entries.size).map(j => {
    entries(i) + entries(j) == 2020
  })
})

entries.tails
  .filter(_.length >= 2) // filter the tail that consists of only the last element
  .map(tail => {
    val entryI = tail.head
    tail.tail.map(entryJ => {
      entryI + entryJ == 2020
    })
  })
```

The following three traversals yield the same result. The first is a traditional
index-based iteration via for-loops - however outputting data from this
iteration requires mutable data structures. The second traversal is also
index-based, but maps over ranges of indices so that mutable data structures are
not needed. The third traversal iterates without indices, as described above.

You can select the iteration-style that feels most comfortable to you - the first is
most recognizable to those coming from traditional, imperative-style languages.
The second provides a good balance between traditional index-based iteration
without the use of mutable data structures. The last is most functional in that
it ignores indices altogether - the algorithm is independent of the order in
which the tails or the elements within each tail are returned (and if you
imagine we are performing this algorithm over a large list distributed across
multiple machines, it may be disadvantageous to impose our arbitrary 0 to *n -
1* ordering anyways!).

## A faster version

However, an alternative that only performs a single traversal of the input list
is to iterate through the list a single time and store the differences between
2020 and each element in a set. When we encounter an element that is present in
our difference set, we know the values of the two elements that sum to 2020.
This algorithm has only *O(n)* time-complexity, at the cost of *O(n)*
space-complexity.

# Part 2

Similar to [Part 1](#part-1), the brute-force algorithm is to perform an *n^3*
traversal of the input list, taking three elements at a time and checking if
they sum to 2020.

Once again, we can reduce the time-complexity of the algorithm from *O(n^3)* to
*O(n^2)* if we store differences. In this version, we store the differences
between 2020 and all pairwise sums in a set (as well as the specific entry pair
itself), requiring *O(n^2)* space. We can do this using a `Map[Int, (Int,
Int)]`, representing the difference between 2020 and the pairwise sum as the key
and the pair itself as the value. If additional pairs lead to the same pairwise
difference, we can ignore them in our `Map` (this would lead to multiple triples
of entries summing to 2020, which shouldn't be possible given the problem
description).

Once we've built up our set of pairwise differences, we can iterate through the
list a single time and check if an entry exists in our difference set - if it
does, we can multiply all three elements together to yield the result.
