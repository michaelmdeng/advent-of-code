package advent.y2020

import cats.data.State
import scala.annotation.tailrec

import advent.shared.InputTransformer
import advent.shared.SafeDayRunner

sealed trait SeatType
case object Empty extends SeatType
case object Occupied extends SeatType
case object Floor extends SeatType

import Day11Implicits._

object Day11Implicits {
  type SeatRow = Seq[SeatType]
  type SeatLayout = Seq[SeatRow]

  implicit val input: InputTransformer[SeatRow] = s => {
    s.map(seat => {
      seat match {
        case 'L' => Empty
        case '#' => Occupied
        case _ => Floor
      }
    })
  }
}

object Day11 extends SafeDayRunner[SeatRow, Int, Int] {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 11

  private def extractState(
    gridChanges: Seq[Seq[(SeatType, Boolean)]]
  ): (SeatLayout, Int) = {
    (
      gridChanges.map(row => {
        row.map {
          case (col, _) => col
        }
      }),
      gridChanges.flatten.filter {
        case (_, changed) => changed
      }.length
    )
  }

  private def transition(
    getNumOccupied: (SeatLayout, Int, Int) => Int,
    getNextSeat: (SeatType, Int) => SeatType
  ): State[SeatLayout, Int] =
    State(grid => {
      val gridChanges = grid.zipWithIndex.map {
        case (row, rowIdx) => {
          row.zipWithIndex.map {
            case (seat, colIdx) => {
              val curr = grid(rowIdx)(colIdx)
              if (curr == Floor) {
                (Floor, false)
              } else {
                val next =
                  getNextSeat(curr, getNumOccupied(grid, rowIdx, colIdx))
                (next, next != curr)
              }
            }
          }
        }
      }

      extractState(gridChanges)
    })

  private def transitionUntil(
    transition: State[SeatLayout, Int]
  ): State[SeatLayout, Int] =
    State(grid => {
      val (next, count) = transition.run(grid).value

      if (count == 0) {
        (next, grid.flatten.filter(_ == Occupied).length)
      } else {
        transitionUntil(transition).run(next).value
      }
    })

  def numOccupiedPart1(grid: SeatLayout, rowIdx: Int, colIdx: Int): Int = {
    val rowSize = grid.length
    val colSize = grid(0).length

    Seq(
      (rowIdx - 1, colIdx - 1),
      (rowIdx - 1, colIdx),
      (rowIdx - 1, colIdx + 1),
      (rowIdx, colIdx - 1),
      (rowIdx, colIdx + 1),
      (rowIdx + 1, colIdx - 1),
      (rowIdx + 1, colIdx),
      (rowIdx + 1, colIdx + 1)
    ).filter {
        case (row, col) =>
          row >= 0 && row < rowSize && col >= 0 && col < colSize
      }
      .map {
        case (row, col) => grid(row)(col)
      }
      .filter(_ == Occupied)
      .length
  }

  def nextSeatPart1(seat: SeatType, numOccupied: Int): SeatType = {
    if (numOccupied == 0) {
      Occupied
    } else if (numOccupied >= 4) {
      Empty
    } else {
      seat
    }
  }

  def safeRunPart1(grid: SeatLayout): Int = {
    transitionUntil(transition(numOccupiedPart1, nextSeatPart1))
      .runA(grid)
      .value
  }

  private def directionIdxs(
    rowIdx: Int,
    colIdx: Int,
    direction: (Int, Int),
    rowSize: Int,
    colSize: Int
  ): LazyList[(Int, Int)] = {
    LazyList
      .continually(direction)
      .scanLeft((0, 0)) {
        case ((accRow, accCol), (row, col)) =>
          (accRow + row, accCol + col)
      }
      .tail // skip the initial (0, 0) term
      .map {
        case (rowDelta, colDelta) =>
          (rowIdx + rowDelta, colIdx + colDelta)
      }
      .takeWhile {
        case (row, col) =>
          row >= 0 && row < rowSize && col >= 0 && col < colSize
      }
  }

  private def numOccupiedPart2(
    grid: SeatLayout,
    rowIdx: Int,
    colIdx: Int
  ): Int = {
    val rowSize = grid.length
    val colSize = grid(0).length

    val forwardIdxs = directionIdxs(rowIdx, colIdx, (-1, 0), rowSize, colSize)
    val backwardIdxs = directionIdxs(rowIdx, colIdx, (1, 0), rowSize, colSize)
    val leftIdxs = directionIdxs(rowIdx, colIdx, (0, -1), rowSize, colSize)
    val rightIdxs = directionIdxs(rowIdx, colIdx, (0, 1), rowSize, colSize)
    val forwardLeftIdxs =
      directionIdxs(rowIdx, colIdx, (-1, -1), rowSize, colSize)
    val forwardRightIdxs =
      directionIdxs(rowIdx, colIdx, (-1, 1), rowSize, colSize)
    val backwardLeftIdxs =
      directionIdxs(rowIdx, colIdx, (1, -1), rowSize, colSize)
    val backwardRightIdxs =
      directionIdxs(rowIdx, colIdx, (1, 1), rowSize, colSize)

    Seq(
      forwardIdxs,
      backwardIdxs,
      leftIdxs,
      rightIdxs,
      forwardLeftIdxs,
      forwardRightIdxs,
      backwardLeftIdxs,
      backwardRightIdxs
    ).flatMap {
        case direction =>
          direction.find {
            case (row, col) =>
              grid(row)(col) == Occupied || grid(row)(col) == Empty
          } match {
            case Some((row, col)) => Seq(grid(row)(col))
            case None => Seq()
          }
      }
      .filter(_ == Occupied)
      .length
  }

  def nextSeatPart2(seat: SeatType, numOccupied: Int): SeatType = {
    if (numOccupied == 0) {
      Occupied
    } else if (numOccupied >= 5) {
      Empty
    } else {
      seat
    }
  }

  def safeRunPart2(grid: SeatLayout): Int = {
    transitionUntil(transition(numOccupiedPart2, nextSeatPart2))
      .runA(grid)
      .value
  }
}
