package advent.y2018

import advent.shared.IOHelper
import cats.data.State

case class Node(
  childCount: Int,
  metadataCount: Int,
  children: Seq[Node],
  metadata: Seq[Int]
) {
  def foldMetadata[B](z: Int)(op: (Int, Int) => Int): Int = {
    val start = this.metadata.fold(z)(op(_, _))

    children.foldLeft(start)((acc, child) => {
      child.foldMetadata(acc)(op)
    })
  }

  def getValue(): Int = {
    def getChildValue(idx: Int): Int = {
      if (idx >= 1 && idx < (this.children.size + 1)) {
        children(idx - 1).getValue()
      } else {
        0
      }
    }

    if (childCount == 0) {
      this.metadata.fold(0)(_ + _)
    } else {
      this.metadata.map(getChildValue(_)).fold(0)(_ + _)
    }
  }
}

object Day8 {
  def parseNodes(n: Int): State[Seq[Int], Seq[Node]] = {
    def parseData(n: Int): State[Seq[Int], Seq[Int]] =
      State[Seq[Int], Seq[Int]] { state =>
        (state.takeRight(state.length - n), state.take(n))
      }

    def parseNode: State[Seq[Int], Node] =
      for {
        childCount <- parseData(1)
        metadataCount <- parseData(1)
        children <- parseNodes(childCount(0))
        metadata <- parseData(metadataCount(0))
      } yield {
        Node(childCount(0), metadataCount(0), children, metadata)
      }

    (0 to (n - 1))
      .foldLeft(State.pure[Seq[Int], Seq[Node]](Seq[Node]()))((state, idx) => {
        state.flatMap(nodes => {
          parseNode.map(nodes :+ _)
        })
      })
  }

  def main(args: Array[String]): Unit = {
    val input = IOHelper.readFile(
      "/Users/michaeldeng/Documents/advent-of-code-2018/input/day8-input.txt"
    )
    val data = input(0).split(" ").map(_.toInt)

    val node = parseNodes(1).runA(data.toIndexedSeq).value(0)
    val sum = node.foldMetadata(0)(_ + _)
    println(f"Result 1: $sum")
    println(f"Result 2: ${node.getValue()}")
  }
}
