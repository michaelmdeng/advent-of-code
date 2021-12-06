package advent.y2021

import cats.Id

import advent.shared.Algorithm
import advent.shared.Day
import advent.shared.InputTransformer
import advent.shared.InputTransformer.implicits._

object Day1Algorithms {
  val runPart1: Algorithm[Int, Int] = Algorithm.safe("default", depths => {
    depths.sliding(2).filter(pair => pair(1) > pair(0)).size
  })

  val runPart2: Algorithm[Int, Int] = Algorithm.safe("default", depths => {
    depths
      .sliding(3)
      .map(_.sum)
      .sliding(2)
      .filter(pair => pair(1) > pair(0))
      .size
  })
}

object Day1
    extends Day[Int, Id, Int, Id, Int](
      Day1Algorithms.runPart1,
      Day1Algorithms.runPart2
    ) {
  protected def YEAR: Int = 2021
  protected def DAY: Int = 1
}
