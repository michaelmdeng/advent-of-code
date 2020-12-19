package advent.y2020

import scala.util.matching.Regex

import advent.shared.DayInput

object Day2 extends DayInput {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 2

  def main(args: Array[String]): Unit = {
    val pattern = new Regex(
      "(\\d+)-(\\d+)\\s([a-z]):\\s([a-z]+)"
    )
    readInput()
      .map(lines => {
        val part1 = lines
          .filter(line => {
            val res = pattern.findFirstMatchIn(line).get

            val lowRange = res.group(1).toInt
            val highRange = res.group(2).toInt
            val char = res.group(3).head
            val password = res.group(4)

            val occurs = password.filter(c => c == char).length
            occurs >= lowRange && occurs <= highRange
          })
          .length

        println(f"Part 1: ${part1}")

        val part2 = lines
          .filter(line => {
            val res = pattern.findFirstMatchIn(line).get

            val firstIdx = res.group(1).toInt - 1
            val secondIdx = res.group(2).toInt - 1
            val char = res.group(3).head
            val password = res.group(4)

            (password(firstIdx) == char && password(secondIdx) != char) ||
            (password(firstIdx) != char && password(secondIdx) == char)
          })
          .length

        println(f"Part 2: ${part2}")
      })
      .unsafeRunSync()
  }
}
