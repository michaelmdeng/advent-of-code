package advent.y2020

import cats.data.State
import scala.annotation.tailrec
import scala.util.parsing.combinator.RegexParsers
import scalax.collection.Graph
import scalax.collection.GraphEdge
import scalax.collection.GraphTraversal

import advent.shared.SafeDayRunner

case class Instruction(op: Operation, amt: Int)

sealed trait Operation
case object Acc extends Operation
case object Jmp extends Operation
case object Nop extends Operation

object Operation {
  def fromString(instruction: String): Operation = {
    if (instruction == "acc") Acc
    else if (instruction == "jmp") Jmp
    else if (instruction == "nop") Nop
    else {
      throw new Exception(f"Invalid instruction ${instruction}")
    }
  }
}

object InstructionParsers extends RegexParsers {
  def instruction: Parser[Instruction] =
    for {
      op <- regex("\\w+".r)
      amt <- regex("[\\d-+]+".r)
    } yield (Instruction(Operation.fromString(op), amt.toInt))
}

case class MachineState(
  instructions: Seq[Instruction],
  curr: Int,
  acc: Int,
  pastInstructions: Set[Int],
  terminated: Boolean
)

object MachineState {
  def default(instructions: Seq[Instruction]): MachineState =
    MachineState(instructions, 0, 0, Set(), false)

  def transition(state: MachineState): MachineState = {
    if (state.pastInstructions.contains(state.curr) ||
      state.curr >= state.instructions.length) {
      state.copy(terminated = true)
    } else {
      val currInstruction = state.instructions(state.curr)
      currInstruction.op match {
        case Acc => {
          state.copy(
            curr = state.curr + 1,
            acc = state.acc + currInstruction.amt,
            pastInstructions = state.pastInstructions + state.curr
          )
        }
        case Jmp => {
          state.copy(
            curr = state.curr + currInstruction.amt,
            pastInstructions = state.pastInstructions + state.curr
          )
        }
        case Nop => {
          state.copy(
            curr = state.curr + 1,
            pastInstructions = state.pastInstructions + state.curr
          )
        }
      }
    }
  }

  @tailrec
  def runUntil(state: MachineState): MachineState = {
    if (state.terminated) {
      state
    } else {
      runUntil(transition(state))
    }
  }
}

object Day8 extends SafeDayRunner[String, Int, Int] {
  protected def YEAR: Int = 2020
  protected def DAY: Int = 8

  def safeRunPart1(lines: Seq[String]): Int = {
    val instructions = lines
      .map(line => {
        val parseResult =
          InstructionParsers.parse(InstructionParsers.instruction, line)
        parseResult.get
      })

    val start = MachineState.default(instructions)
    val end = MachineState.runUntil(start)
    end.acc
  }

  def safeRunPart2(lines: Seq[String]): Int = {
    val instructions = lines
      .map(line => {
        val parseResult =
          InstructionParsers.parse(InstructionParsers.instruction, line)
        parseResult.get
      })

    val start = MachineState.default(instructions)
    val end = MachineState.runUntil(start)

    val visitedInstructions = end.pastInstructions

    // all nops that, if switched to a jmp, would execute an instruction that
    // hasn't been visited
    val possibleNops = end.pastInstructions
      .filter(instructions(_).op match {
        case Acc => false
        case Jmp => false
        case Nop => true
      })
      .filter(curr => {
        val currInstruction = instructions(curr)
        val next = curr + currInstruction.amt
        !visitedInstructions.contains(next)
      })

    // all jmps that, if switched to a nop, would execute the next instruction
    // that hasn't been visited
    val possibleJmps = end.pastInstructions
      .filter(instructions(_).op match {
        case Acc => false
        case Jmp => true
        case Nop => false
      })
      .filter(curr => {
        val currInstruction = instructions(curr)
        val next = curr + 1
        !visitedInstructions.contains(next)
      })

    // for all instructions that lead to new paths, run the machine until
    // termination and check if it terminated at the end
    val switch = (possibleNops ++ possibleJmps)
      .map(switch => {
        val currInstruction = instructions(switch)
        val switchedInstruction = currInstruction.copy(
          op = if (currInstruction.op == Nop) Jmp else Nop
        )
        val switchedInstructions =
          instructions.updated(switch, switchedInstruction)

        val start = MachineState.default(switchedInstructions)
        MachineState.runUntil(start)
      })
      .find(_.curr >= instructions.size)

    switch.get.acc
  }
}
