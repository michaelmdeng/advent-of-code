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
