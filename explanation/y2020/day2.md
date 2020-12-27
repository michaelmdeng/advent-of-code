# Part 1

We can use the following regex to parse each password policy:

```
(\d+)-(\d+)\s([a-z]):\s([a-z]+)
```

In explainable language, this regex parses:

* a group of digits, followed by a hyphen
* another group of digits, followed by a space
* a letter, followed by a colon and a space
* a group of letters

The first group of digits represents the low-range, or the minimum number of
appearances of the letter. The second group represents the high-range, or the
maximum number of appearances of the letter. The third group represents the
letter to track, and the last group represents the password itself.

From this password and policy, we can find all characters in the password that
match the letter we care about and ensure that the count is within the given
bounds.

# Part 2

Rather than check the count of occurrences of the specified letter, we instead
check the specified indices of our password (remembering to offset indices by
1) to see if either match the specified letter.
