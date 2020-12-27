# Part 1

## Parsing passports

We represent each passport as a list of lines `Seq[String]`, and we parse the
input into a list of separate passports, `Seq[Seq[String]]`. We do this via the
following fold:

```scala
lines.foldLeft(Seq[Seq[String]]())((acc, elem) => {
  if (acc.isEmpty) {
    Seq(Seq(elem))
  } else if (elem.nonEmpty) {
    acc.init :+ (acc.last :+ elem)
  } else {
    acc :+ Seq[String]()
  }
})
```

We start with an empty accumulator, representing an empty list of passports.

When we start the fold (the `if (acc.isEmpty)` clause of the fold), we should
initialize our accumulator with an empty passport. This has the same effect as
starting the input with an empty line to denote a new passport.

If the current line is non-empty (the `else if (elem.nonEmpty)` clause of the
fold), we have found another line for our current passport. We append this line
to the current passport (ie the last element of our accumulator).

If the current line is empty (the `else` clause of the fold), we have reached
the end of the given passport and should start a new one - we do this by
finishing the current passport and appending a new empty passport
(`Seq[String]()`) to our accumulator.

## Parsing fields

Once we've parsed the input into separate passports, we need to parse each
passport into the relevant fields. The following regex parses a single field,
consisting of the field name, followed by a colon, followed by the field value:

```
([^\s:]+):([^\s]+)
```

We apply this regex repeatedly to find all fields in a single line of a
passport, and repeat this process for each line of the passport to parse all
fields from all lines.

## Field validation

Once we've parsed all the fields for a passport, we are ready to perform
validation.

Our initial validation checks that all required fields are present. Given a
static set of required fields (the `REQUIRED_FIELDS` constant), we iterate
through each required field one-by-one to check that they are present. If any
are not, we mark the passport as invalid.

# Part 2

## Additional validation

In addition to validating whether all required fields are present, we also need
to validate the value for each field.

We represent our validations as a `Map[String, String => Boolean]`. The map is
keyed by the field name (ex. `"byr"`), and the value for each key represents
a validation function that we run on the field value to return a boolean result.

For a given passport, we iterate through fields, checking if a validation for
that field exists in our map. If it does, we apply the validation function to
the value for that field, and mark the passport valid if all validations for all
fields return true. If any field is not valid, we mark the passport as invalid.
