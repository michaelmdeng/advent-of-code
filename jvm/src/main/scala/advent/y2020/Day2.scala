package advent.y2020

import scala.util.matching.Regex

import advent.shared.SafeDayRunner

object Day2 extends SafeDayRunner[String, Int, Int] {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 2

  private val PATTERN: Regex = new Regex("(\\d+)-(\\d+)\\s([a-z]):\\s([a-z]+)")

  def safeRunPart1(lines: Seq[String]): Int = {
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

  def safeRunPart2(lines: Seq[String]): Int = {
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
}
