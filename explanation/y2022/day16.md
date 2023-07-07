# Part 1

We can determine the maximum pressure released for the current state (current
valve position and current set of open valves) by maximizing across the choice
of visiting all possible unopened valves and determining the maximum pressure
released from that point forward. This allows us to establish a recurrence
relation for the maximum pressure released.

Let:

* `t` denote the current time
* `cv` denote the current valve
* `opened` denote the set of currently opened valves
* `traversal(v1, v2)` denote the time it takes to move from valve `v1` to valve
  `v2`
* `released(t, v)` denote the amount of pressure released by opening valve `v`
  at time `t`

Thus our recurrence relation is:

```
max_released(t, cv, opened) = max(
    released(t + traversal(cv, nv) + 1, nv) +
    max_released(t + traversal(cv, nv) + 1, opened | nt)
    for nv not in opened
)
```

Additionally, we can further filter results by ignoring valves that don't
release any pressure and ignoring any pressure release after `t = 30`.

The key to being able to calculate this recurrence relation is the `traversal`
function, which determines how long it would take to navigate to the given next
valve using the fastest route possible. We can construct this traversal by
fully traversing the graph of valves and their connections.

# Part 2

We are unable to use the same recurrence relation directly for part 2 because
there are two independent actors occupying different positions. There isn't a
simple way to increment to the next time step for the recursion because one
actor may be midway through a move to another valve.

However we are helped by the fact that we and the elephant are equivalent actors
-- both we and the elephant move at the same speed and open valves at the same
speed.

Thus we can consider the problem as dividing the valves into two sets -- one set
of valves for us to open and another for the elephant to open. We can then use
the recurrence relation above to determine the maximum pressure released by
visiting and opening a given set of valves.

Thus, for each possible splitting of the valves into sets, we determine the max
pressure released for us visiting the first set of valves and the max pressure
released for the elephant visiting the second set of valves. The total pressure
released is the sum of these maxes. The overall max pressure released is the
maximum total pressure released across all possible splits of valves into
separate sets.

Since we expect the maximum pressure released to result from splitting the
valves evenly (ie. have both us and the elephant visit a similar number of
valves), we can restrict the search set to splits where this fact holds.
Additionally, we only care about valves that release positive pressure and can
ignore all other valves in our search.

We thus modify our `max_released` recurrence relation from above to 1) have a
configurable time window to account for the now shorter time window and 2)
enable only visiting a subset of valves instead of considering the full set of
possible valves.
