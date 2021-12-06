package advent.y2021

import cats.Id
import cats.implicits._

import advent.shared.Algorithm
import advent.shared.Day
import advent.shared.InputTransformer
import advent.shared.InputTransformer.implicits._

import Day3Implicits._

object Day3Implicits {
  implicit val input: InputTransformer[List[Day3Algorithms.Bit]] =
    new InputTransformer[List[Day3Algorithms.Bit]] {
      def transformInput(line: String): List[Day3Algorithms.Bit] = {
        line
          .map(digit => {
            digit.toString.toInt match {
              case 1 => Day3Algorithms.One
              case 0 => Day3Algorithms.Zero
            }
          })
          .toList
      }
    }
}

object Day3Algorithms {
  sealed trait Bit {
    val flip: Bit

    def toString(): String
  }

  object Bit {
    def asInt(bits: Iterable[Bit]): Int =
      Integer.parseInt(bits.map(_.toString).reduce(_ + _), 2)
  }

  case object One extends Bit {
    val flip: Bit = Zero

    override def toString(): String = "1"
  }

  case object Zero extends Bit {
    val flip: Bit = One

    override def toString(): String = "0"
  }

  private def mostCommon(bits: Iterable[Bit]): Bit = {
    val oneBits = bits
      .filter(bit => {
        bit match {
          case One => true
          case Zero => false
        }
      })

    if (2 * oneBits.size >= bits.size) {
      One
    } else {
      Zero
    }
  }

  val part1: Algorithm[List[Bit], Int] = Algorithm.safe(
    "default",
    readings => {
      val mostCommonBits = readings.transpose.map(mostCommon(_))
      val gamma = Bit.asInt(mostCommonBits)
      val epsilon = Bit.asInt(mostCommonBits.map(_.flip))

      gamma * epsilon
    }
  )

  val part2: Algorithm[List[Bit], Int] = Algorithm.safe(
    "default",
    readings => {
      val numDigits = readings(0).size

      val oxygenList = Range(0, numDigits)
        .foldLeft(readings)((acc, idx) => {
          if (acc.size == 1) {
            acc
          } else {
            val mostCommonBit = mostCommon(acc.map(_(idx)))
            acc.filter(_(idx) == mostCommonBit)
          }
        })
        .head
      val oxygen = Bit.asInt(oxygenList)

      val co2List = Range(0, numDigits)
        .foldLeft(readings)((acc, idx) => {
          if (acc.size == 1) {
            acc
          } else {
            val mostCommonBit = mostCommon(acc.map(_(idx)))
            acc.filter(_(idx) != mostCommonBit)
          }
        })
        .head
      val co2 = Bit.asInt(co2List)

      oxygen * co2
    }
  )
}

object Day3
    extends Day[List[Day3Algorithms.Bit], Id, Int, Id, Int](
      Day3Algorithms.part1,
      Day3Algorithms.part2
    ) {
  protected def YEAR: Int = 2021
  protected def DAY: Int = 3
}
