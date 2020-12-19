package advent.y2020

import cats.effect.IO

import advent.shared.DayRunner

object Day1 extends DayRunner[Int, Int] {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 1

  def runPart1(lines: Seq[String]): IO[Int] = IO {
    val data: Seq[Int] = lines.map(_.toInt)

    val entries: (Int, Int) = data.tails
      .filter(_.length >= 2)
      .map(tail => {
        val head: Int = tail.head
        tail.tail
          .find(d => head + d == 2020)
          .map(d => (head, d))
      })
      .find(_.isDefined)
      .flatten
      .get

    entries._1 * entries._2
  }

  def runPart2(lines: Seq[String]): IO[Int] = IO {
    val data: Seq[Int] = lines.map(_.toInt)

    val entries: (Int, Int, Int) = data.tails
      .filter(_.length >= 3)
      .map(tail => {
        val first: Int = tail.head
        val rest: Seq[Int] = tail.tail

        rest.tails
          .filter(_.length >= 2)
          .map(tail2 => {
            val second: Int = tail2.head
            val rest2: Seq[Int] = tail2.tail

            rest2
              .find(d => first + second + d == 2020)
              .map(d => (first, second, d))
          })
          .find(_.isDefined)
          .flatten
      })
      .find(_.isDefined)
      .flatten
      .get

    entries._1 * entries._2 * entries._3
  }
}
