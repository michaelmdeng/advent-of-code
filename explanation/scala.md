The Scala solutions use the following scaffolding.

We use the `cats` package, specifically `IOApp` to run our `main()` methods
purely. The `IOApp` trait allows us to define our solution as the following
method:

```scala
def run(args: List[String]): IO[ExitCode]
```

# Input

These solutions ignore input arguments since all input is loaded from text
files. Helpers to load input are contained in the `DayInput` trait, including
the following methods:

```scala
trait DayInput {
  protected def YEAR: Int
  protected def DAY: Int

  def readInput(): IO[Seq[String]]
  def readTestInput(): IO[Seq[String]]
}
```

# Running

All solutions are run using the `UnsafeDayRunner` trait, which extends `IOApp`
and `DayInput` to read input and apply the solution functions to it.

```scala
/**
 * I - input type
 * A - Part 1 output type
 * B - Part 2 output type
 */
trait UnsafeDayRunner[I, A, B]
```

## Input formatting

The `DayInput` trait can be used to read input data as strings - however, many
problem solutions need to transform the input first (ex. parsing to `Int`,
formatting, etc.). Rather than requiring the solution for each part to format
input (and duplicating the formatting work), `UnsafeDayRunner` can instead
apply the transformations implicitly before passing the input to the solution
functions.

## Output

Output is formatted using `cats.Show`, ensuring we have reasonable
representations for types that have specified a valid `toString()` method.

## Safety

Since many of our solutions will be written as pure functions, we include a
helper `SafeDayRunner` that allows subclasses to write solutions as pure
functions - the runner itself takes care of wrapping the solutions as proper
`IO`.
