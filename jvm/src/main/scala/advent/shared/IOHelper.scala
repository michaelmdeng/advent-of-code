package advent.shared

import java.io._

object IOHelper {
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
