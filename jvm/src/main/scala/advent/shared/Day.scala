package advent.shared

import cats.Functor
import cats.NonEmptyParallel
import cats.Show
import cats.Traverse
import cats.effect.ExitCode
import cats.effect.IO
import cats.effect.IOApp
import cats.syntax.functor._
import cats.syntax.parallel._

/* Runs an Advent of Code solution for a given day
 *
 * I - Input type
 * F - Parametrized type for part 1 algorithms
 * A - Part 1 output type
 * G - Parametrized type for part 2 algorithms
 * B - Part 2 output type
 */
abstract class Day[I: InputTransformer, F[_]: Functor: Traverse: NonEmptyParallel, A: Show, G[
  _
]: Functor: Traverse: NonEmptyParallel, B: Show](
  methods1: F[Algorithm[I, A]],
  methods2: G[Algorithm[I, B]]
) extends DayInput
    with IOApp {

  private def runAlgorithms[I, F[_]: Functor: Traverse: NonEmptyParallel, O: Show](
    input: Seq[I],
    methods: F[Algorithm[I, O]]
  ): IO[Unit] =
    for {
      outputs <- methods
        .map(method => {
          for {
            output <- method.run(input)
            _ <- IO(
              println(
                f"${method.name} algorithm output: ${Show[O].show(output)}"
              )
            )
          } yield ()
        })
        .parSequence
    } yield ()

  private def runPart1(input: Seq[I]): IO[Unit] =
    for {
      _ <- IO(println("Running part 1"))
      _ <- runAlgorithms(input, methods1)
    } yield ()

  private def runPart2(input: Seq[I]): IO[Unit] =
    for {
      _ <- IO(println("Running part 2"))
      _ <- runAlgorithms(input, methods2)
    } yield ()

  private def runParts(input: Seq[I]): IO[Unit] =
    for {
      _ <- runPart1(input)
      _ <- runPart2(input)
    } yield ()

  private def runTest(): IO[Unit] = {
    val read = for {
      _ <- IO(println("Reading test data"))
      testInput <- readTestInput()
    } yield (testInput)

    read.flatMap(input => {
      input match {
        case Some(lines) => {
          for {
            _ <- IO.unit
            testTransformedInput = lines.map(
              InputTransformer[I].transformInput(_)
            )
            _ <- IO(println("Running against test data"))
            _ <- runParts(testTransformedInput)
            _ <- IO(println("---"))
          } yield ()
        }
        case None => {
          IO(println("Did not find test data"))
        }
      }
    })
  }

  def run(args: List[String]): IO[ExitCode] =
    for {
      _ <- IO(println(f"Running Year: ${YEAR} Day: ${DAY}"))
      _ <- runTest()
      _ <- IO(println("Reading real data"))
      input <- readInput()
      transformedInput = input.map(InputTransformer[I].transformInput(_))
      _ <- IO(println("Running against real data"))
      _ <- runParts(transformedInput)
    } yield {
      ExitCode.Success
    }
}
