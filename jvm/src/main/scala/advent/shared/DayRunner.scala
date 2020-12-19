package advent.shared

import cats.Show
import cats.effect.ExitCode
import cats.effect.IO
import cats.effect.IOApp

abstract class DayRunner[A: Show, B: Show] extends DayInput with IOApp {
  def runPart1(lines: Seq[String]): IO[A]

  def runPart2(lines: Seq[String]): IO[B]

  def run(args: List[String]): IO[ExitCode] =
    for {
      input <- readInput()
      part1 <- runPart1(input)
      _ <- IO(println(f"Part 1: ${Show[A].show(part1)}"))
      part2 <- runPart2(input)
      _ <- IO(println(f"Part 2: ${Show[B].show(part2)}"))
    } yield {
      ExitCode.Success
    }
}
