package advent.y2020

import scala.collection.mutable

import advent.shared.SafeDayRunner

object Day10 extends SafeDayRunner[String, Int, Long] {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 10

  def safeRunPart1(lines: Seq[String]): Int = {
    val adapters = lines.map(_.toInt).sorted
    val jolts = 0 +: adapters :+ (adapters.max + 3)
    val differences =
      jolts.sliding(2, 1).map(window => window(1) - window(0)).toList
    differences.filter(_ == 1).length * differences.filter(_ == 3).length
  }

  def safeRunPart2(lines: Seq[String]): Long = {
    val adapters = lines.map(_.toInt).sorted
    val jolts = 0 +: adapters :+ (adapters.max + 3)

    /* break the adapters into continuous runs of adapters - we are modeling the
     * adapters as a graph from 0 to (max+3) - a directed edge between two nodes
     * exists if the second node has a higher voltage that is less than 3 volts
     * higher than the first node
     *
     * based on this modeling, we need to find the number of possible walks in
     * the graph
     *
     * to simplify this, we break the graph into subgraphs - between each
     * subgraph, only a single path exists - within each subgraph multiple paths
     * may exist - this means we can calculate the number of paths through each
     * subgraph independently
     *
     * each subgraph consists of a set of adapters with a continous run of
     * voltages
     */
    val chunks = jolts.foldLeft(Seq[Seq[Int]]())((acc, elem) => {
      if (acc.isEmpty) {
        acc :+ Seq(elem)
      } else if (acc.last.last == elem - 1 ) {
        acc.init :+ (acc.last :+ elem)
      } else {
        acc :+ Seq(elem)
      }
    })

    /**
     * based on the length of the run, there is a specific permutation of
     * possible paths through the subgraph
     *
     * for example, with 1- or 2-element runs, there is only a single path that
     * visits both the first and last element of the run
     *
     * for a 3-element run, there are two paths, one that visits all 3 elements
     * and one that visits only the first and last
     *
     * 4-element: 4 total
     * (1,2,3,4), (1,2,4), (1,3,4), (1,4)
     *
     * 5-element: 7 total
     * (1,2,3,4,5), (1,2,3,5), (1,3,4,5), (1,2,4,5), (1,2,5), (1,3,5), (1,4,5)
     *
     * since there is only a single path connecting each run, each run is
     * independent and we can simply multiply together to find the total number
     * of paths
     */
    chunks.map(chunk => {
      chunk.length match {
        case 1 | 2 => 1L
        case 3 => 2L
        case 4 => 4L
        case 5 => 7L
      }
    }).reduce(_ * _)
  }
}
