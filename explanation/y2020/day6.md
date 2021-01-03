# Part 1

We can parse the questions for each group similarly to how we [parsed individual
passports on Day 4](day4#parsing-passports). We can fold over the input - if we
come across a blank line, we know to end the previous group and start a new one,
and if we come across a non-blank line, we know to add the line to the current
group.

Once we've parsed the questions into groups, we construct a `Set` for each
person's questions in the group. Given multiple sets that consist of the
questions that each person answered, the total set of questions that **any**
person answered is the union of all the individual sets:

```scala
val anyAnswer = answers.reduce(_ | _)
```

Once we have the set of answers that any person answered, we can sum the sizes
of these sets for all groups to determine the final answer.

# Part 2

If we instead want to determine the set of questions that **all** individuals
answered, then we should perform a set intersection (`&`) instead of a set union
(`|`).

```scala
val allAnswer = answers.reduce(_ & _)
```
