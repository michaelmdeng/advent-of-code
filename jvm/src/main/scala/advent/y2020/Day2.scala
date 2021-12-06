package advent.y2020

import cats.Id
import scala.util.matching.Regex

import advent.shared.Algorithm
import advent.shared.Day

object Day2Algorithms {
  private val PATTERN: Regex = new Regex("(\\d+)-(\\d+)\\s([a-z]):\\s([a-z]+)")

  def part1: Algorithm[String, Int] =
    Algorithm.safe(
      "default",
      lines => {
        lines
          .filter(line => {
            val res = PATTERN.findFirstMatchIn(line).get

            val lowRange = res.group(1).toInt
            val highRange = res.group(2).toInt
            val char = res.group(3).head
            val password = res.group(4)

            val occurs = password.filter(c => c == char).length
            occurs >= lowRange && occurs <= highRange
          })
          .length
      }
    )

  def part2: Algorithm[String, Int] =
    Algorithm.safe(
      "default",
      lines => {
        lines
          .filter(line => {
            val res = PATTERN.findFirstMatchIn(line).get

            val firstIdx = res.group(1).toInt - 1
            val secondIdx = res.group(2).toInt - 1
            val char = res.group(3).head
            val password = res.group(4)

            (password(firstIdx) == char && password(secondIdx) != char) ||
            (password(firstIdx) != char && password(secondIdx) == char)
          })
          .length
      }
    )
}

object Day2
    extends Day[String, Id, Int, Id, Int](
      Day2Algorithms.part1,
      Day2Algorithms.part2
    ) {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 2
}
