package advent.y2020

import cats.effect.IO
import scala.util.matching.Regex

import advent.shared.DayRunner

object Day4 extends DayRunner[Int, Int] {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 4

  private val FIELD_PATTERN: Regex = "([^\\s:]+):([^\\s]+)".r
  private val REQUIRED_FIELDS: Set[String] = Set(
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid"
  )

  private val HEIGHT_PATTERN: Regex = "([\\d]+)(in)|([\\d]+)(cm)".r
  private val HAIR_COLOR_PATTERN: Regex = "#[0-9a-f]{6}".r
  private val EYE_COLORS: Set[String] =
    Set("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
  private val REQUIRED_FIELD_VALIDATIONS: Map[String, String => Boolean] = Map(
    ("byr", (s: String) => s.toInt >= 1920 && s.toInt <= 2002),
    ("iyr", (s: String) => s.toInt >= 2010 && s.toInt <= 2020),
    ("eyr", (s: String) => s.toInt >= 2020 && s.toInt <= 2030),
    ("hgt", (s: String) => {
      val res = HEIGHT_PATTERN.findFirstMatchIn(s)
      res match {
        case Some(m) => {
          if (m.group(2) == "in") {
            m.group(1).toInt >= 59 && m.group(1).toInt <= 76
          } else if (m.group(4) == "cm") {
            m.group(3).toInt >= 150 && m.group(3).toInt <= 193
          } else {
            false
          }
        }
        case None => false
      }
    }),
    ("hcl", (s: String) => HAIR_COLOR_PATTERN.findFirstMatchIn(s).isDefined),
    ("ecl", (s: String) => EYE_COLORS.contains(s)),
    ("pid", (s: String) => "^\\d{9}$".r.findFirstMatchIn(s).isDefined)
  )

  private def parsePassports(lines: Seq[String]): Seq[Seq[String]] = {
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

  private def parseFields(passport: Seq[String]): Seq[(String, String)] = {
    passport
      .flatMap(line => {
        FIELD_PATTERN
          .findAllMatchIn(line)
          .map(m => {
            val key = m.group(1)
            val value = m.group(2)
            (key, value)
          })
      })
  }

  def runPart1(lines: Seq[String]): IO[Int] = IO {
    parsePassports(lines)
      .map(passport => {
        parseFields(passport)
      })
      .filter(fields => {
        REQUIRED_FIELDS
          .filter(reqField => !fields.map(_._1).contains(reqField))
          .size == 0
      })
      .length
  }

  def runPart2(lines: Seq[String]): IO[Int] = IO {
    parsePassports(lines)
      .map(passport => {
        parseFields(passport)
      })
      .filter(fields => {
        REQUIRED_FIELDS
          .filter(reqField => !fields.map(_._1).contains(reqField))
          .size == 0
      })
      .filter(fields => {
        val failedFields = fields.filter {
          case (key, value) => {
            if (REQUIRED_FIELD_VALIDATIONS.contains(key)) {
              !REQUIRED_FIELD_VALIDATIONS(key)(value)
            } else {
              false
            }
          }
        }

        failedFields.isEmpty
      })
      .length
  }
}
