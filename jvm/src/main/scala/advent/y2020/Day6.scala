package advent.y2020

import cats.effect.IO

import advent.shared.DayRunner

object Day6 extends DayRunner[Int, Int] {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 6

  private def parseGroups(lines: Seq[String]): Seq[Seq[String]] = {
    lines.foldLeft[Seq[Seq[String]]](Seq[Seq[String]]())((acc, elem) => {
      if (acc.isEmpty) {
        Seq(Seq(elem))
      } else if (elem.nonEmpty) {
        acc.init :+ (acc.last :+ elem)
      } else {
        acc :+ Seq[String]()
      }
    })
  }

  private def parseQuestions(line: String): Set[Char] = line.toSet

  def runPart1(lines: Seq[String]): IO[Int] = IO {
    parseGroups(lines).map(group => {
      group.map(parseQuestions(_)).reduce(_.union(_)).size
    }).reduce(_ + _)
  }

  def runPart2(lines: Seq[String]): IO[Int] = IO {
    parseGroups(lines).map(group => {
      group.map(parseQuestions(_)).reduce(_ & _).size
    }).reduce(_ + _)
  }
}
