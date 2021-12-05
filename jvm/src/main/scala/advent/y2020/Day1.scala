package advent.y2020

import cats.effect.IO

import advent.shared.Algorithm
import advent.shared.Day
import advent.shared.InputTransformer
import advent.shared.SafeDayRunner

import Day1Implicits._

object Day1Implicits {
  implicit val input: InputTransformer[Int] = s => s.toInt
}

object Day1Algorithms {
  private val SUM: Int = 2020

  private def part1BruteForce(entries: Seq[Int]): Int = {
    entries.tails
      .filter(_.length >= 2)
      .map(tail => {
        val head = tail.head
        tail.tail
          .find(d => head + d == SUM)
          .map(d => (head, d))
      })
      .find(_.isDefined)
      .flatten match {
      case Some((entry1, entry2)) => entry1 * entry2
      case None => throw new Exception(f"No elements found that sum to ${SUM}")
    }
  }

  private def part1Differences(entries: Seq[Int]): Int = {
    val differences = entries.map(SUM - _).toSet

    entries.find(entry => differences.contains(entry)) match {
      case Some(entry) => (SUM - entry) * entry
      case None => throw new Exception(f"No elements found that sum to ${SUM}")
    }
  }

  val part1: Seq[Algorithm[Int, Int]] = Seq(
    Algorithm.safe("brute force", part1BruteForce(_)),
    Algorithm.safe("differences", part1Differences(_))
  )

  private def part2BruteForce(entries: Seq[Int]): Int = {
    entries.tails
      .filter(_.length >= 3)
      .map(tail => {
        val first = tail.head
        val rest = tail.tail

        rest.tails
          .filter(_.length >= 2)
          .map(tail2 => {
            val second = tail2.head
            val rest2 = tail2.tail

            rest2
              .find(d => first + second + d == SUM)
              .map(d => (first, second, d))
          })
          .find(_.isDefined)
          .flatten
      })
      .find(_.isDefined)
      .flatten match {
      case Some((entry1, entry2, entry3)) => entry1 * entry2 * entry3
      case None => throw new Exception(f"No elements found that sum to ${SUM}")
    }
  }

  private def part2Differences(entries: Seq[Int]): Int = {
    val differences = Map.from(
      entries.tails
        .filter(_.length >= 2)
        .flatMap(tail => {
          val head = tail.head
          tail.tail
            .map(tailEntry => (SUM - (head + tailEntry), (head, tailEntry)))
        })
    )

    entries.find(entry => differences.contains(entry)) match {
      case Some(entry) => {
        val others = differences(entry)
        entry * others._1 * others._2
      }
      case None => throw new Exception(f"No elements found that sum to ${SUM}")
    }
  }

  val part2: Seq[Algorithm[Int, Int]] = Seq(
    Algorithm.safe("brute force", part2BruteForce(_)),
    Algorithm.safe("differences", part2Differences(_))
  )
}

object Day1
    extends Day[Int, Int, Int](Day1Algorithms.part1, Day1Algorithms.part2) {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 1

  private val SUM: Int = 2020
}
