package advent.y2018

import advent.shared.Coord

case class FuelCell(coord: Coord, serial: Int) {
  val rackId: Int = coord.x + 10
  val power: FuelCell.Power = {
    val tmp = (rackId * coord.y + serial) * rackId
    val hDigit = (tmp / 100) % 10
    hDigit - 5
  }
}

object FuelCell {
  type Power = Int
}

object Day11 {
  private val SERIAL: Int = 8868

  def createGrid(x: Int, y: Int, serial: Int): Seq[Seq[FuelCell]] = {
    (1 to x).map(x => {
      (1 to y).map(y => FuelCell(Coord(x, y), serial))
    })
  }

  def maxPower(
    grid: Seq[Seq[FuelCell]],
    cellSize: Int = 3
  ): (FuelCell.Power, Coord) = {
    def gridPower(
      grid: Seq[Seq[FuelCell]],
      cellSize: Int
    ): Seq[Seq[FuelCell.Power]] = {
      (0 to grid.size + 1 - cellSize).map(x => {
        (0 to grid(0).size + 1 - cellSize).map(y => {
          val cell = grid.slice(x, x + cellSize).map(_.slice(y, y + cellSize))
          cell.flatten.map(_.power).sum
        })
      })
    }

    val maxRow = gridPower(grid, cellSize).map(yRow => {
      yRow.zip(0 to (yRow.size) - 1).maxBy(_._1)
    })
    val ((power, maxY), maxX) =
      maxRow.zip(0 to (maxRow.size - 1)).maxBy(_._1._1)
    (power, Coord(maxX, maxY))
  }

  def main(args: Array[String]): Unit = {
    val gridSize = 300
    val grid = createGrid(gridSize, gridSize, SERIAL)
    val (power, maxCoord) = maxPower(grid)
    println(f"Result 1: (${maxCoord.x + 1}, ${maxCoord.y + 1})")

    val sizes = 3 to 30
    val maxes = sizes.map(maxPower(grid, _)).zip(sizes).maxBy(_._1._1)
    val maxesCoord = maxes._1._2
    val maxSize = maxes._2
    println(f"Result 2: (${maxesCoord.x + 1},${maxesCoord.y + 1},$maxSize)")
  }
}
