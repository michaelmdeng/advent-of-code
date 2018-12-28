package advent.y2018

import cats.data.State

case class CircularList[T](curr: CircularList.Node[T]) {
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

  def insert(newNode: CircularList.Node[T]): CircularList[T] = {
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
    val node = new CircularList.Node[T](start, null, null)
    node.left = node
    node.right = node
    CircularList(node)
  }

  class Node[T](val data: T, var left: Node[T], var right: Node[T])

  object Node {
    def starting: Node[Int] = {
      val node = new Node[Int](0, null, null)
      node.left = node
      node.right = node
      node
    }
  }
}
