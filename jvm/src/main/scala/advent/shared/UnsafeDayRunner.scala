package advent.shared

import cats.Show
import cats.effect.ExitCode
import cats.effect.IO
import cats.effect.IOApp

abstract class UnsafeDayRunner[I: InputTransformer, A: Show, B: Show]
    extends DayInput
    with IOApp {
  def runPart1(lines: Seq[I]): IO[A]

  def runPart2(lines: Seq[I]): IO[B]

  def run(args: List[String]): IO[ExitCode] =
    for {
      input <- readInput()
      transformedInput = input.map(InputTransformer[I].transformInput(_))
      part1 <- runPart1(transformedInput)
      _ <- IO(println(f"Part 1: ${Show[A].show(part1)}"))
      part2 <- runPart2(transformedInput)
      _ <- IO(println(f"Part 2: ${Show[B].show(part2)}"))
    } yield {
      ExitCode.Success
    }
}
