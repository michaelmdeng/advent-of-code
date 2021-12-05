package advent.shared

import cats.Show
import cats.effect.ExitCode
import cats.effect.IO
import cats.effect.IOApp
import cats.implicits._

abstract class Day[I: InputTransformer, A: Show, B: Show](
  methods1: Seq[Algorithm[I, A]],
  methods2: Seq[Algorithm[I, B]]
) extends DayInput
    with IOApp {

  private def runAlgorithms[I, O: Show](
    input: Seq[I],
    methods: Seq[Algorithm[I, O]]
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

  def runPart1(input: Seq[I]): IO[Unit] =
    for {
      _ <- IO(println("Running part 1"))
      _ <- runAlgorithms(input, methods1)
    } yield ()

  def runPart2(input: Seq[I]): IO[Unit] =
    for {
      _ <- IO(println("Running part 2"))
      _ <- runAlgorithms(input, methods2)
    } yield ()

  def runParts(input: Seq[I]): IO[Unit] = for {
    _ <- runPart1(input)
    _ <- runPart2(input)
  } yield ()

  def runTest(): IO[Unit] = {
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
