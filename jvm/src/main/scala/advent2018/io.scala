package advent2018

import java.io._

import resource._

object IO {
  def readFile(filePath: String): Seq[String] = {
    var acc = Seq[String]()
    val fis = new FileInputStream(filePath)
    val br = new BufferedReader(new InputStreamReader(fis));
    while (br.ready()) {
      acc = acc :+ br.readLine()
    }

    acc
  }
}
