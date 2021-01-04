package advent.y2020

import cats.data.State
import scala.util.matching.Regex

import advent.shared.InputTransformer
import advent.shared.SafeDayRunner

import Day12Implicits._

object Day12Implicits {
  private val PATTERN = "([NSEWLRF])(\\d+)".r

  implicit val input: InputTransformer[FerryInstruction] = s => {
    val m = PATTERN.findFirstMatchIn(s).get
    val action = m.group(1)
    val value = m.group(2).toInt

    FerryInstruction(action, value)
  }
}

case class FerryInstruction(action: String, value: Int)

sealed trait FerryDirection {
  val toAngle: Int
}
case object North extends FerryDirection {
  val toAngle: Int = 90
}
case object East extends FerryDirection {
  val toAngle: Int = 0
}
case object South extends FerryDirection {
  val toAngle: Int = 270
}
case object West extends FerryDirection {
  val toAngle: Int = 180
}
object FerryDirection {
  def fromAngle(angle: Int): FerryDirection = {
    (angle + 360) % 360 match {
      case 0 => East
      case 90 => North
      case 180 => West
      case 270 => South
    }
  }
}

case class FerryState(direction: FerryDirection, position: (Int, Int))

case class FerryStatePart2(position: (Int, Int), waypoint: (Int, Int))

// TODO: clean this up with {@link cats.data.State}
object Day12 extends SafeDayRunner[FerryInstruction, Int, Int] {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 12

  private def distance(position: (Int, Int)): Int =
    math.abs(position._1) + math.abs(position._2)

  private def turn(
    direction: FerryDirection,
    isLeft: Boolean,
    degrees: Int
  ): FerryDirection = {
    if (isLeft) {
      FerryDirection.fromAngle(direction.toAngle + degrees)
    } else {
      FerryDirection.fromAngle(direction.toAngle - degrees)
    }
  }

  private def transition(
    state: FerryState,
    instruction: FerryInstruction
  ): FerryState = {
    val xPos = state.position._1
    val yPos = state.position._2

    val realInstruction = if (instruction.action == "F") {
      state.direction match {
        case North => FerryInstruction("N", instruction.value)
        case East => FerryInstruction("E", instruction.value)
        case South => FerryInstruction("S", instruction.value)
        case West => FerryInstruction("W", instruction.value)
      }
    } else {
      instruction
    }

    realInstruction.action match {
      case "N" => state.copy(position = (xPos, yPos + instruction.value))
      case "E" => state.copy(position = (xPos + instruction.value, yPos))
      case "S" => state.copy(position = (xPos, yPos - instruction.value))
      case "W" => state.copy(position = (xPos - instruction.value, yPos))
      case "L" =>
        state.copy(direction = turn(state.direction, true, instruction.value))
      case "R" =>
        state.copy(direction = turn(state.direction, false, instruction.value))
    }
  }

  def safeRunPart1(instructions: Seq[FerryInstruction]): Int = {
    val finalState =
      instructions.foldLeft(FerryState(East, (0, 0)))((state, instruction) =>
        transition(state, instruction)
      )

    distance(finalState.position)
  }

  private def transitionPart2(
    state: FerryStatePart2,
    instruction: FerryInstruction
  ): FerryStatePart2 = {
    val wayXPos = state.waypoint._1
    val wayYPos = state.waypoint._2

    instruction.action match {
      case "N" => state.copy(waypoint = (wayXPos, wayYPos + instruction.value))
      case "E" => state.copy(waypoint = (wayXPos + instruction.value, wayYPos))
      case "S" => state.copy(waypoint = (wayXPos, wayYPos - instruction.value))
      case "W" => state.copy(waypoint = (wayXPos - instruction.value, wayYPos))
      case "L" => {
        val nextWaypoint = instruction.value match {
          case 90 => (-wayYPos, wayXPos)
          case 180 => (-wayXPos, -wayYPos)
          case 270 => (wayYPos, -wayXPos)
          case 360 => state.waypoint
        }
        state.copy(waypoint = nextWaypoint)
      }
      case "R" => {
        val nextWaypoint = instruction.value match {
          case 90 => (wayYPos, -wayXPos)
          case 270 => (-wayYPos, wayXPos)
          case 180 => (-wayXPos, -wayYPos)
          case 360 => state.waypoint
        }
        state.copy(waypoint = nextWaypoint)
      }
      case "F" => {
        val xPos = state.position._1
        val yPos = state.position._2
        state.copy(position =
          (
            xPos + instruction.value * wayXPos,
            yPos + instruction.value * wayYPos
          )
        )
      }
    }
  }

  def safeRunPart2(instructions: Seq[FerryInstruction]): Int = {
    val finalState =
      instructions.foldLeft(FerryStatePart2((0, 0), (10, 1)))(
        (state, instruction) => transitionPart2(state, instruction)
      )

    distance(finalState.position)
  }
}
