package advent.y2020

import advent.shared.DayInput

object Day1 extends DayInput {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 1

  def main(args: Array[String]): Unit = {
    readInput()
      .map(lines => {
        val data: Seq[Int] = lines.map(_.toInt)

        val part1: (Int, Int) = data.tails
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

        println(f"Part 1: ${part1._1 * part1._2}")

        val part2: (Int, Int, Int) = data.tails
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

        println(f"Part 2: ${part2._1 * part2._2 * part2._3}")
      })
      .unsafeRunSync()
  }
}
