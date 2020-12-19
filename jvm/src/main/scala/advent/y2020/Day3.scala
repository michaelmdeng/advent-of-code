package advent.y2020

import cats.effect.ExitCode
import cats.effect.IO
import cats.effect.IOApp
import scala.util.matching.Regex

import advent.shared.DayInput

object Day3 extends DayInput with IOApp {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 3

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

  def run(args: List[String]): IO[ExitCode] =
    readInput()
      .map(grid => {
        println(f"Part 1: ${countTrees(grid, X_SLOPE_PT_1, Y_SLOPE_PT_1)}")

        val part2 = List((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
          .map {
            case (xSlope, ySlope) => countTrees(grid, xSlope, ySlope)
          }
          .map(_.toLong)
          .reduce(_ * _)

        println(f"Part 2: ${part2}")
      })
      .as(ExitCode.Success)
}
