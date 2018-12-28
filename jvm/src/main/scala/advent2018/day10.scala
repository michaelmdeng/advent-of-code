package advent2018

case class Vec2(x: Int, y: Int)
case class Light(pos: Vec2, v: Vec2) {
  def transition(): Light = {
    Light(Vec2(pos.x + v.x, pos.y + v.y), v)
  }
}

object Day10 {
  def parse(line: String): Light = {
    val splits = line.replaceAll("\\s", "").split("<").flatMap(_.split(">"))
    val posStr = splits(1)
    val pos = Vec2(posStr.split(",")(0).toInt, posStr.split(",")(1).toInt)
    val vStr = splits(3)
    val v = Vec2(vStr.split(",")(0).toInt, vStr.split(",")(1).toInt)
    Light(pos, v)
  }

  def transition(points: Seq[Light]): Seq[Light] = {
    points.map(_.transition())
  }

  def boundBox(points: Seq[Vec2]): (Int, Int, Int, Int) = {
    val minX = points.map(_.x).min
    val maxX = points.map(_.x).max
    val minY = points.map(_.y).min
    val maxY = points.map(_.y).max
    (minX, maxX, minY, maxY)
  }

  def render(points: Seq[Vec2]): Unit = {
    val (minX, maxX, minY, maxY) = boundBox(points)
    val xs = minX to maxX
    val ys = minY to maxY
    val output = ys.map(_ => collection.mutable.Seq(xs.map(_ => "."): _*))

    for (point <- points) {
      output(point.y - minY)(point.x - minX) = "#"
    }

    for (line <- output) {
      println(line)
    }
  }

  def main(args: Array[String]): Unit = {
    val input = IO.readFile(
      "/Users/michaeldeng/Documents/advent-of-code-2018/input/day10-input.txt")
    val lights = input.map(parse(_))

    val maxIter = 15000
    var minH = Int.MaxValue
    var minIdx = -1
    var minLights: Option[Seq[Light]] = None
    (1 to maxIter).foldLeft(lights)((acc, idx) => {
      val (minX, maxX, minY, maxY) = boundBox(acc.map(_.pos))
      if ((maxX - minX) < minH) {
        minIdx = idx
        minH = maxX - minX
        minLights = Some(acc)
      }

      transition(acc)
    })

    println("Result 1")
    render(minLights.get.map(_.pos))
    println(f"Result 2: $minIdx")
  }
}
