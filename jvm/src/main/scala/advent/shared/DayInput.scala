package advent.shared

import cats.effect.IO
import java.io.BufferedReader
import java.io.FileInputStream
import java.io.InputStreamReader

trait DayInput {
  protected def YEAR: Int
  protected def DAY: Int

  def filePath(): String = {
    f"../input/${YEAR}/day-${DAY}-input.txt"
  }

  def readInput(): IO[Seq[String]] = IO {
    var acc = Seq[String]()
    val fis = new FileInputStream(filePath())
    val br = new BufferedReader(new InputStreamReader(fis));
    while (br.ready()) {
      acc = acc :+ br.readLine()
    }

    acc
  }
}
