# Part 1

Based on the halving properties of the binary space partitioning, we can treat
the assignment as two binary numbers - one for the row and one for the column.

For rows, `'F'` takes the first half, which corresponds to 0, while `'B'` takes
the back half, which corresponds to 1. Similarly, `'L'` and `'R'` correspond to
0 and 1 respectively for columns.

Since the ID multiples the row number by 8 (shifts bits to left by 3 spaces),
and adds the column number, the entire seat assignment can be treated as a
single binary number, with `'F'` and `'L'` representing 0 and `'B'` and `'R'`
representing 1.

Once we convert the assignment into a binary string, we can use the built-in
`Integer.parseInt(string, base)` method to parse the string into an integer.
However, since this feels a little easy, we can write a parser ourself:

```scala
numberString.reverse.zipWithIndex.foldLeft(0) {
  case (acc, (number, idx)) =>
    acc + (if (number == '0') 0 else 1) * Math.pow(2, idx).toInt
}
```

This simple implementation iterates over the digits right-to-left - at each
digit, it takes the value of the digit and multiplies it by the respective base,
adding up each place into the final number.

This implementation is pretty slow in that it performs exponentiation and
multiplication rather than bit-shifting - try writing a faster version yourself!

# Part 2

Once we are able to calculate the seat IDs for every seat, we can iterate
through all possible seat IDs to see if the ID is in our input. If the ID is not
in our input, then we know there is an open seat that we can take. The maximum
possible seat ID is `127 * 8 + 7 = 1023`.

```scala
(0 until 1023).map(!seatIds.contains(_))
```

We can account for the possibility that there are missing seats at the front or
back by ensuring that the previous and next seat IDs are occupied for every open
seat.

```scala
(0 until 1023).find(id => {
  !seatIds.contains(id) && seatIds.contains(id - 1) && seatIds.contains(id + 1)
})
```
