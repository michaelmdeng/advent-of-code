package advent2018.day9

import cats.data.State

case class CircularList[T](curr: Node[T]) {
  private def shiftLeft: CircularList[T] = CircularList[T](curr.left)
  private def shiftRight: CircularList[T] = CircularList[T](curr.right)

  def shift(idx: Int): CircularList[T] = {
    if (idx < 0) {
      (1 to Math.abs(idx)).foldLeft(this)((acc, _) => acc.shiftLeft)
    } else if (idx > 0) {
      (1 to Math.abs(idx)).foldLeft(this)((acc, _) => acc.shiftRight)
    } else {
      this
    }
  }

  def insert(newNode: Node[T]): CircularList[T] = {
    val right = curr.right
    curr.right = newNode
    newNode.left = curr
    newNode.right = right
    right.left = newNode
    CircularList(newNode)
  }

  def remove(): CircularList[T] = {
    val left = curr.left
    val right = curr.right
    left.right = right
    right.left = left
    CircularList(left)
  }

  def foldLeft[B](count: Int)(z: B)(op: (B, T) => B): B = {
    val (out, list) = (1 to Math.abs(count)).foldLeft((z, this))((acc, _) => {
      val newZ = op(acc._1, acc._2.curr.data)
      val newList = acc._2.shiftRight
      (newZ, newList)
    })

    out
  }
}

object CircularList {
  def starting[T](start: T): CircularList[T] = {
    val node = new Node[T](start, null, null)
    node.left = node
    node.right = node
    CircularList(node)
  }
}

class Node[T](val data: T, var left: Node[T], var right: Node[T]) {
  def traverseLeft: Node[T] = left
  def traverseRight: Node[T] = right

  def traverse(idx: Int): Node[T] = {
    if (idx < 0) {
      (1 to Math.abs(idx)).foldLeft(this)((acc, _) => {
        acc.traverseLeft
      })
    } else if (idx > 0) {
      (1 to Math.abs(idx)).foldLeft(this)((acc, _) => {
        acc.traverseRight
      })
    } else {
      this
    }
  }

  def insertRight(newNode: Node[T]): Node[T] = {
    val right = this.right
    this.right = newNode
    newNode.left = this
    newNode.right = right
    right.left = newNode
    newNode
  }

  def insertLeft(newNode: Node[T]): Node[T] = {
    val left = this.left
    this.left = newNode
    newNode.right = this
    newNode.left = left
    left.right = newNode
    newNode
  }

  def foreachRight(count: Int)(f: T => Unit): Unit = {
    var node = this
    for (idx <- (0 to count)) {
      f(node.data)
      node = node.right
    }
  }
}

object Node {
  def starting: Node[Int] = {
    val node = new Node[Int](0, null, null)
    node.left = node
    node.right = node
    node
  }

  def main(args: Array[String]): Unit = {
    val node = CircularList.starting(0)
    (1 to 25).foldLeft(node)((acc, idx) => {
      val (newAcc, score) = if (idx % 23 == 0) {
        val tmp = acc.shift(-7)
        val score = idx + tmp.curr.data
        (tmp.remove(), score)
      } else {
        (acc.shift(1).insert(new Node(idx, null, null)), 0)
      }
      val numPrint = idx + 1 - (2 * (idx / 23))
      val str = newAcc.foldLeft(numPrint)("")((acc, data) => f"$acc $data")
      println(str)
      newAcc
    })
  }
}
