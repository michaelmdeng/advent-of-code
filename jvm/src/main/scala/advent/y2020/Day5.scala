package advent.y2020

import cats.effect.IO
import scala.util.matching.Regex

import advent.shared.DayRunner

object Day5 extends DayRunner[Int, Int] {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 5

  private val PATTERN: Regex = new Regex("([FB]{7})([LR]{3})")
  private val MAX_ROW: Int = 127
  private val MAX_COL: Int = 7

  private def getSeat(line: String): (Int, Int) = {
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
    val row = Integer.parseInt(rowStr, 2)

    val colStr = m
      .group(2)
      .map(char => {
        if (char == 'L') {
          '0'
        } else {
          '1'
        }
      })
    val col = Integer.parseInt(colStr, 2)

    (row, col)
  }

  private def getSeatId(seat: (Int, Int)): Int = seat._1 * 8 + seat._2

  def runPart1(lines: Seq[String]): IO[Int] = IO {
    lines.map(getSeat(_)).map(getSeatId(_)).max
  }

  def runPart2(lines: Seq[String]): IO[Int] = IO {
    val seatIds = lines.map(getSeat(_)).map(getSeatId(_))

    Range(1, getSeatId(MAX_ROW, MAX_COL) - 1)
      .find(id => {
        !seatIds.contains(id) && seatIds.contains(id - 1) && seatIds
          .contains(id + 1)
      })
      .get
  }
}
