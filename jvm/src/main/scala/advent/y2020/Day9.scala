package advent.y2020

import advent.shared.SafeDayRunner

object Day9 extends SafeDayRunner[String, Long, Long] {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 9

  private val BUFFER_LENGTH: Int = 25

  def validNext(buffer: Seq[Long], next: Long): Boolean = {
    val members = Set(buffer: _*)
    val diffs = Set(buffer.map(next - _): _*)
    (diffs & members).nonEmpty
  }

  def safeRunPart1(lines: Seq[String]): Long = {
    lines
      .map(_.toLong)
      .sliding(BUFFER_LENGTH + 1)
      .find(bufferPlus => !validNext(bufferPlus.init, bufferPlus.last))
      .map(_.last)
      .get
  }

  def safeRunPart2(lines: Seq[String]): Long = {
    val invalidNumber = safeRunPart1(lines)

    LazyList(lines.map(_.toLong): _*).tails
      .map(tail => {
        // Stream partial sums until we've surpassed the SECRET_NUMBER
        // This we way don't have to calculate unecessary sums
        val sums = tail
          .scanLeft(0L)(_ + _)
          .takeWhile(_ <= invalidNumber)
          .tail
          .force
          .toSeq
        (tail.take(sums.length), sums)
      })
      .find {
        case (_, sums) => sums.last == invalidNumber
      }
      .map {
        case (tail, _) => tail
      }
      .map(sequence => sequence.min + sequence.max)
      .get
  }
}
