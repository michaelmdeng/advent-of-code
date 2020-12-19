package advent.y2020

import advent.shared.SafeDayRunner

object Day6 extends SafeDayRunner[String, Int, Int] {
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

  def safeRunPart1(lines: Seq[String]): Int = {
    parseGroups(lines)
      .map(group => {
        group.map(parseQuestions(_)).reduce(_.union(_)).size
      })
      .reduce(_ + _)
  }

  def safeRunPart2(lines: Seq[String]): Int = {
    parseGroups(lines)
      .map(group => {
        group.map(parseQuestions(_)).reduce(_ & _).size
      })
      .reduce(_ + _)
  }
}
