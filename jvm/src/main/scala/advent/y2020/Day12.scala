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

object Day12 extends SafeDayRunner[FerryInstruction, Int, Int] {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 12

  private val NORTH: String = "N"
  private val EAST: String = "E"
  private val SOUTH: String = "S"
  private val WEST: String = "W"
  private val LEFT: String = "L"
  private val RIGHT: String = "R"
  private val FORWARD: String = "F"

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

  private def transitionPart1(
    instruction: FerryInstruction
  ): State[FerryState, Int] =
    State(state => {
      val xPos = state.position._1
      val yPos = state.position._2

      val realInstruction = if (instruction.action == FORWARD) {
        state.direction match {
          case North => FerryInstruction(NORTH, instruction.value)
          case East => FerryInstruction(EAST, instruction.value)
          case South => FerryInstruction(SOUTH, instruction.value)
          case West => FerryInstruction(WEST, instruction.value)
        }
      } else {
        instruction
      }

      val nextState = realInstruction.action match {
        case NORTH => state.copy(position = (xPos, yPos + instruction.value))
        case EAST => state.copy(position = (xPos + instruction.value, yPos))
        case SOUTH => state.copy(position = (xPos, yPos - instruction.value))
        case WEST => state.copy(position = (xPos - instruction.value, yPos))
        case LEFT =>
          state.copy(direction = turn(state.direction, true, instruction.value))
        case RIGHT =>
          state.copy(direction =
            turn(state.direction, false, instruction.value)
          )
      }

      (nextState, distance(nextState.position))
    })

  def safeRunPart1(instructions: Seq[FerryInstruction]): Int = {
    instructions
      .map(transitionPart1(_))
      .reduce((s1, s2) => s1.flatMap(_ => s2))
      .runA(FerryState(East, (0, 0)))
      .value
  }

  private def rotate(position: (Int, Int), angle: Int): (Int, Int) = {
    (angle + 360) % 360 match {
      case 0 => position
      case 90 => (-position._2, position._1)
      case 180 => (-position._1, -position._2)
      case 270 => (position._2, -position._1)
    }
  }

  private def transitionPart2(
    instruction: FerryInstruction
  ): State[FerryStatePart2, Int] =
    State(state => {
      val wayXPos = state.waypoint._1
      val wayYPos = state.waypoint._2
      val nextState = instruction.action match {
        case NORTH =>
          state.copy(waypoint = (wayXPos, wayYPos + instruction.value))
        case EAST =>
          state.copy(waypoint = (wayXPos + instruction.value, wayYPos))
        case SOUTH =>
          state.copy(waypoint = (wayXPos, wayYPos - instruction.value))
        case WEST =>
          state.copy(waypoint = (wayXPos - instruction.value, wayYPos))
        case LEFT =>
          state.copy(waypoint = rotate(state.waypoint, instruction.value))
        case RIGHT =>
          state.copy(waypoint = rotate(state.waypoint, -instruction.value))
        case FORWARD => {
          state.copy(position =
            (
              state.position._1 + instruction.value * wayXPos,
              state.position._2 + instruction.value * wayYPos
            )
          )
        }
      }

      (nextState, distance(nextState.position))
    })

  def safeRunPart2(instructions: Seq[FerryInstruction]): Int = {
    instructions
      .map(transitionPart2(_))
      .reduce((s1, s2) => s1.flatMap(_ => s2))
      .runA(FerryStatePart2((0, 0), (10, 1)))
      .value
  }
}
