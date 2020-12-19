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

  def testFilePath(): String = {
    f"../input/${YEAR}/day-${DAY}-input-test.txt"
  }

  def readFile(file: String): IO[Seq[String]] = IO {
    var acc = Seq[String]()
    val fis = new FileInputStream(file)
    val br = new BufferedReader(new InputStreamReader(fis));
    while (br.ready()) {
      acc = acc :+ br.readLine()
    }

    acc
  }

  def readInput(): IO[Seq[String]] = readFile(filePath())

  def readTestInput(): IO[Seq[String]] = readFile(testFilePath())
}
