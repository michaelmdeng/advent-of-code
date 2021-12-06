package advent.y2020

import cats.Id

import advent.shared.Algorithm
import advent.shared.Day

object Day3Algorithms {
  private final val X_SLOPE_PT_1: Int = 3
  private final val Y_SLOPE_PT_1: Int = 1

  def countTrees(grid: Seq[String], xSlope: Int, ySlope: Int): Int = {
    val width = grid.head.length
    val height = grid.length

    Range(ySlope, height, ySlope)
      .zip(Range(xSlope, xSlope * (height / ySlope + 1), xSlope))
      .map(_.swap)
      .map {
        case (x, y) => {
          val gridValue = grid(y)(x % width)
          if (gridValue == '#') 1 else 0
        }
      }
      .reduce(_ + _)
  }

  def part1: Algorithm[String, Int] =
    Algorithm.safe("default", lines => {
      countTrees(lines, X_SLOPE_PT_1, Y_SLOPE_PT_1)
    })

  def part2: Algorithm[String, Long] =
    Algorithm.safe("default", lines => {
      List((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
        .map {
          case (xSlope, ySlope) => countTrees(lines, xSlope, ySlope)
        }
        .map(_.toLong)
        .reduce(_ * _)
    })
}

object Day3
    extends Day[String, Id, Int, Id, Long](
      Day3Algorithms.part1,
      Day3Algorithms.part2
    ) {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 3
}
