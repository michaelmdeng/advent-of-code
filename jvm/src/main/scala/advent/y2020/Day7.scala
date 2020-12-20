package advent.y2020

import scala.util.parsing.combinator.RegexParsers
import scalax.collection.Graph
import scalax.collection.GraphEdge
import scalax.collection.GraphTraversal

import advent.shared.SafeDayRunner

object RuleParsers extends RegexParsers {
  override val skipWhitespace: Boolean = true

  def bagColor: Parser[String] =
    for {
      col1 <- regex("\\w+".r)
      col2 <- regex("\\w+".r)
      _ <- literal("bag")
      _ <- opt(literal("s"))
    } yield (col1 + " " + col2)

  def clause: Parser[(Int, String)] =
    for {
      amount <- regex("\\d+".r)
      color <- bagColor
    } yield ((amount.toInt, color))

  def noBags: Parser[Set[(Int, String)]] =
    literal("no other bags").map(_ => Set())

  def clauses: Parser[Set[(Int, String)]] =
    for {
      others <- rep1sep(clause, literal(", "))
    } yield (Set(others: _*))

  def rule: Parser[(String, Set[(Int, String)])] =
    for {
      color <- bagColor
      _ <- literal("contain")
      others <- clauses | noBags
      _ <- literal(".")
    } yield ((color, others))
}

object Day7 extends SafeDayRunner[String, Int, Int] {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 7

  private val SHINY_GOLD: String = "shiny gold"

  def safeRunPart1(lines: Seq[String]): Int = {
    val contentsByColor = Map(lines.map(line => {
      val parseResult = RuleParsers.parse(RuleParsers.rule, line)
      parseResult.get
    }): _*)

    val contentsGraph =
      Graph.from(contentsByColor.keys, contentsByColor.flatMap {
        case (color, colorContents) =>
          colorContents.map {
            case (amt, c) => GraphEdge.DiEdge(color, c)
          }
      })

    contentsGraph
      .get(SHINY_GOLD)
      .withDirection(GraphTraversal.Predecessors)
      .count(_.value != SHINY_GOLD)
  }

  private def sumContaining(
    contentsByColor: Map[String, Set[(Int, String)]]
  ): Int =
    sumContainingHelper(contentsByColor, SHINY_GOLD, 1) - 1 // don't count the bag itself

  private def sumContainingHelper(
    contentsByColor: Map[String, Set[(Int, String)]],
    curr: String,
    amt: Int
  ): Int = {
    amt + contentsByColor(curr).toSeq.map {
      case (nextAmt, next) => {
        sumContainingHelper(contentsByColor, next, amt * nextAmt)
      }
    }.sum
  }

  def safeRunPart2(lines: Seq[String]): Int = {
    val contentsByColor = Map(lines.map(line => {
      val parseResult = RuleParsers.parse(RuleParsers.rule, line)
      parseResult.get
    }): _*)

    sumContaining(contentsByColor)
  }
}
