package advent.y2020

import scala.annotation.tailrec

import advent.shared.SafeDayRunner

sealed trait SeatType
case object Empty extends SeatType
case object Occupied extends SeatType
case object Floor extends SeatType

// TODO: clean this up with {@link cats.data.State}
object Day11 extends SafeDayRunner[String, Int, Int] {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 11

  @tailrec
  def transitionUntil(grid: Seq[Seq[SeatType]])(
    transition: Seq[Seq[SeatType]] => (Seq[Seq[SeatType]], Int)
  ): (Seq[Seq[SeatType]], Int) = {
    val (next, count) = transition(grid)

    if (count == 0) {
      (next, grid.flatten.filter(_ == Occupied).length)
    } else {
      transitionUntil(next)(transition)
    }
  }

  private def extractState(
    gridChanges: Seq[Seq[(SeatType, Boolean)]]
  ): (Seq[Seq[SeatType]], Int) = {
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

  private def adjacentSeats(
    rowIdx: Int,
    colIdx: Int,
    grid: Seq[Seq[SeatType]]
  ): Seq[SeatType] = {
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
  }

  private def transition(
    grid: Seq[Seq[SeatType]]
  ): (Seq[Seq[SeatType]], Int) = {
    val nextGrid = grid.zipWithIndex.map {
      case (row, rowIdx) => {
        row.zipWithIndex.map {
          case (seat, colIdx) => {
            val curr = grid(rowIdx)(colIdx)
            if (curr == Floor) {
              (Floor, false)
            } else {
              val numOccupied = adjacentSeats(rowIdx, colIdx, grid)
                .filter(_ == Occupied)
                .length

              val next = if (numOccupied == 0) {
                Occupied
              } else if (numOccupied >= 4) {
                Empty
              } else {
                curr
              }

              (next, next != curr)
            }
          }
        }
      }
    }

    extractState(nextGrid)
  }

  private def directionIdxs(
    rowIdx: Int,
    colIdx: Int,
    direction: (Int, Int),
    rowSize: Int,
    colSize: Int
  ): Stream[(Int, Int)] = {
    Stream
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

  private def closestAdjacentSeats(
    rowIdx: Int,
    colIdx: Int,
    grid: Seq[Seq[SeatType]]
  ): Seq[SeatType] = {
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
  }

  private def transitionPart2(
    grid: Seq[Seq[SeatType]]
  ): (Seq[Seq[SeatType]], Int) = {
    val nextGrid = grid.zipWithIndex.map {
      case (row, rowIdx) => {
        row.zipWithIndex.map {
          case (seat, colIdx) => {
            val curr = grid(rowIdx)(colIdx)
            if (curr == Floor) {
              (Floor, false)
            } else {
              val numOccupied = closestAdjacentSeats(
                rowIdx,
                colIdx,
                grid
              ).filter(_ == Occupied).length

              val next = if (numOccupied == 0) {
                Occupied
              } else if (numOccupied >= 5) {
                Empty
              } else {
                curr
              }

              (next, next != curr)
            }
          }
        }
      }
    }

    extractState(nextGrid)
  }

  private def readGrid(lines: Seq[String]): Seq[Seq[SeatType]] =
    lines
      .map(line => {
        line.map(seat => {
          seat match {
            case 'L' => Empty
            case '#' => Occupied
            case _ => Floor
          }
        })
      })

  def safeRunPart1(lines: Seq[String]): Int = {
    val (_, count) = transitionUntil(readGrid(lines))(transition)
    count
  }

  def safeRunPart2(lines: Seq[String]): Int = {
    val (_, count) = transitionUntil(readGrid(lines))(transitionPart2)
    count
  }
}
