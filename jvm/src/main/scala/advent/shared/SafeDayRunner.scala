package advent.shared

import cats.effect.IO
import cats.Show

abstract class SafeDayRunner[I: InputTransformer, A: Show, B: Show]
    extends UnsafeDayRunner[I, A, B] {
  def safeRunPart1(lines: Seq[I]): A

  def safeRunPart2(lines: Seq[I]): B

  def runPart1(lines: Seq[I]): IO[A] = IO.pure {
    safeRunPart1(lines)
  }

  def runPart2(lines: Seq[I]): IO[B] = IO.pure {
    safeRunPart2(lines)
  }
}
