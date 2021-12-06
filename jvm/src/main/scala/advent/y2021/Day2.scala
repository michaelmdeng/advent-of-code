package advent.y2021

import cats.Id

import advent.shared.Algorithm
import advent.shared.Day
import advent.shared.InputTransformer

import Day2Implicits._

object Day2Implicits {
  implicit val input: InputTransformer[Day2Algorithms.Command] =
    Day2Algorithms.Command.parse(_)
}

object Day2Algorithms {
  sealed trait Command
  case class Forward(amount: Int) extends Command
  case class Up(amount: Int) extends Command
  case class Down(amount: Int) extends Command

  object Command {
    def parse(command: String): Command = {
      val parts = command.split(" ")
      parts(0) match {
        case "forward" => Forward(parts(1).toInt)
        case "up" => Up(parts(1).toInt)
        case "down" => Down(parts(1).toInt)
      }
    }

  }

  val part1: Algorithm[Command, Int] = Algorithm.safe(
    "default",
    commands => {
      val finalPos = commands.foldLeft((0, 0))((pos, command) => {
        val horiz = pos._1
        val depth = pos._2
        command match {
          case Forward(amt) => (horiz + amt, depth)
          case Up(amt) => (horiz, depth - amt)
          case Down(amt) => (horiz, depth + amt)
        }
      })

      finalPos._1 * finalPos._2
    }
  )

  val part2: Algorithm[Command, Int] = Algorithm.safe(
    "default",
    commands => {
      val finalPos = commands.foldLeft((0, 0, 0))((pos, command) => {
        val horiz = pos._1
        val depth = pos._2
        val aim = pos._3
        command match {
          case Forward(amt) => (horiz + amt, depth + aim * amt, aim)
          case Up(amt) => (horiz, depth, aim - amt)
          case Down(amt) => (horiz, depth, aim + amt)
        }
      })

      finalPos._1 * finalPos._2
    }
  )
}

object Day2
    extends Day[Day2Algorithms.Command, Id, Int, Id, Int](
      Day2Algorithms.part1,
      Day2Algorithms.part2
    ) {
  protected def YEAR: Int = 2021
  protected def DAY: Int = 2
}
