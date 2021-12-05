package advent.shared

import cats.effect.IO

trait Algorithm[I, O] {
  val name: String

  def run(input: Seq[I]): IO[O]
}

object Algorithm {
  def safe[I, O](n: String, f: Seq[I] => O): Algorithm[I, O] =
    new Algorithm[I, O] {
      val name: String = n

      def run(input: Seq[I]): IO[O] = IO(f(input))
    }
}
