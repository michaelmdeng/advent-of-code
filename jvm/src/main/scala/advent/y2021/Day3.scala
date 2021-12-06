package advent.y2021

import cats.Id
import cats.implicits._

import advent.shared.Algorithm
import advent.shared.Day
import advent.shared.InputTransformer
import advent.shared.InputTransformer.implicits._

object Day3Algorithms {
  val part1: Algorithm[String, Int] = Algorithm.safe(
    "default",
    readings => {
      val numReadings = readings.size
      val (gammaList, epsilonList) = readings
        .map(reading => {
          reading.map(_.toString.toInt).toList
        })
        .reduce((r1, r2) => {
          (r1, r2).parMapN(_ + _)
        })
        .map(digit => {
          val mostCommon = 2 * digit / numReadings
          val leastCommon = 1 - mostCommon
          (mostCommon, leastCommon)
        })
        .unzip
      val gamma = Integer.parseInt(gammaList.map(_.toString).reduce(_ + _), 2)
      val epsilon =
        Integer.parseInt(epsilonList.map(_.toString).reduce(_ + _), 2)

      gamma * epsilon
    }
  )

  val part2: Algorithm[String, Int] = Algorithm.safe(
    "default",
    readings => {
      val numDigits = readings(0).size

      val formattedReadings =
        readings.map(reading => reading.map(_.toString.toInt))
      val oxygenList = Range(0, numDigits)
        .foldLeft(formattedReadings)((acc, idx) => {
          if (acc.size == 1) {
            acc
          } else {
            val mostCommon = 2 * acc.map(_(idx)).reduce(_ + _) / acc.size
            acc.filter(_(idx) == mostCommon)
          }
        })
        .head
      val oxygen = Integer.parseInt(oxygenList.map(_.toString).reduce(_ + _), 2)

      val co2List = Range(0, numDigits)
        .foldLeft(formattedReadings)((acc, idx) => {
          if (acc.size == 1) {
            acc
          } else {
            val mostCommon = 2 * acc.map(_(idx)).reduce(_ + _) / acc.size
            acc.filter(_(idx) != mostCommon)
          }
        })
        .head
      val co2 = Integer.parseInt(co2List.map(_.toString).reduce(_ + _), 2)

      oxygen * co2
    }
  )
}

object Day3
    extends Day[String, Id, Int, Id, Int](
      Day3Algorithms.part1,
      Day3Algorithms.part2
    ) {
  protected def YEAR: Int = 2021
  protected def DAY: Int = 3
}
