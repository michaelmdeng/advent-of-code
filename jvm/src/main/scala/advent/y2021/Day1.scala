package advent.y2021

import advent.shared.Algorithm
import advent.shared.Day
import advent.shared.InputTransformer

import Day1Implicits._

object Day1Implicits {
  implicit val input: InputTransformer[Int] = s => s.toInt
}

object Day1Algorithms {
  val runPart1: Algorithm[Int, Int] = Algorithm.safe("default", depths => {
    depths.sliding(2).filter(pair => pair(1) > pair(0)).size
  })

  val part1 = Seq(runPart1)

  val runPart2: Algorithm[Int, Int] = Algorithm.safe("default", depths => {
    depths
      .sliding(3)
      .map(_.sum)
      .sliding(2)
      .filter(pair => pair(1) > pair(0))
      .size
  })

  val part2 = Seq(runPart2)
}

object Day1
    extends Day[Int, Int, Int](Day1Algorithms.part1, Day1Algorithms.part2) {
  protected def YEAR: Int = 2021
  protected def DAY: Int = 1

  private val SUM: Int = 2021
}
