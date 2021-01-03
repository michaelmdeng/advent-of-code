package advent.y2020

import scala.util.matching.Regex

import advent.shared.SafeDayRunner

object Day5 extends SafeDayRunner[String, Int, Int] {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 5

  private val PATTERN: Regex = new Regex("([FB]{7})([LR]{3})")
  private val MAX_ROW: Int = 127
  private val MAX_COL: Int = 7

  private def parseBinary(numberString: String): Int = {
    numberString.reverse.zipWithIndex.foldLeft(0) {
      case (acc, (number, idx)) =>
        acc + (if (number == '0') 0 else 1) * Math.pow(2, idx).toInt
    }
  }

  private def getSeatId(
    line: String,
    parser: String => Int = Integer.parseInt(_, 2)
  ): Int = {
    val m = PATTERN.findFirstMatchIn(line).get
    val rowStr = m
      .group(1)
      .map(char => {
        if (char == 'F') {
          '0'
        } else {
          '1'
        }
      })

    val colStr = m
      .group(2)
      .map(char => {
        if (char == 'L') {
          '0'
        } else {
          '1'
        }
      })

    Integer.parseInt(rowStr + colStr, 2)
  }

  def safeRunPart1(lines: Seq[String]): Int = {
    if (false) {
      lines.map(getSeatId(_, parseBinary)).max
    }

    lines.map(getSeatId(_)).max
  }

  def safeRunPart2(lines: Seq[String]): Int = {
    val seatIds = lines.map(getSeatId(_)).toSet

    Range(1, 8 * MAX_ROW + MAX_COL - 1)
      .find(id => {
        !seatIds.contains(id) && seatIds.contains(id - 1) && seatIds
          .contains(id + 1)
      })
      .get
  }
}
