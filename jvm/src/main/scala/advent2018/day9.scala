package advent2018

import cats.data.State

case class MarbleState(marbles: day9.CircularList[Long], currMarble: Int) {}

object MarbleState {
  type Score = Long

  def starting: MarbleState = MarbleState(day9.CircularList.starting(0L), 0)

  def placeMarble: State[MarbleState, Score] =
    State(state => {
      if (state.currMarble % 10000 == 0) println(state.currMarble / 10000)

      // val numPrint = state.currMarble + 1 - (2 * (state.currMarble / 23))
      // val str = state.marbles.foldLeft(numPrint)("")((acc, data) => f"$acc $data")
      // println(str)

      val nextMarble = state.currMarble + 1

      if ((nextMarble % 23) != 0) {
        val next = new day9.Node(nextMarble.toLong, null, null)
        (MarbleState(state.marbles.shift(1).insert(next), nextMarble), 0)
      } else {
        val tmp = state.marbles.shift(-7)
        val score = nextMarble.toLong + tmp.curr.data
        (MarbleState(tmp.remove().shift(1), nextMarble), score)
      }

    })
}

case class PlayerState(scores: Seq[Long], current: Int)

object PlayerState {
  def starting(numPlayers: Int) = PlayerState((1 to numPlayers).map(_ => 0L), 0)

  def addScore(score: Long): State[PlayerState, Unit] =
    State(state => {
      val startScore = state.scores(state.current)
      val nextScores =
        state.scores.patch(state.current, Seq[Long](startScore + score), 1)
      val nextPlayer = (state.current + 1) % state.scores.size
      (PlayerState(nextScores, nextPlayer), ())
    })
}

case class GameState(marbleState: MarbleState, playerState: PlayerState)

object GameState {
  def takeTurn: State[GameState, Unit] =
    State(state => {
      val (nextMarble, score) =
        MarbleState.placeMarble.run(state.marbleState).value
      val nextPlayer =
        PlayerState.addScore(score).runS(state.playerState).value
      (GameState(nextMarble, nextPlayer), ())
    })

  def runGame(numMarbles: Int): State[GameState, Unit] = {
    val startState = State.pure[GameState, Unit](())
    (1 to numMarbles).foldLeft(startState)((acc, idx) => {
      acc.flatMap(_ => takeTurn)
    })
  }

  def main(args: Array[String]): Unit = {
    val numPlayers = 470
    val numMarbles1 = 72170
    val start =
      GameState(MarbleState.starting, PlayerState.starting(numPlayers))
    val state1 = runGame(numMarbles1).runS(start).value
    println(f"Result 1: ${state1.playerState.scores.max}")

    val numMarbles2 = numMarbles1 * 100
    val state2 = runGame(numMarbles2).runS(start).value
    println(f"Result 2: ${state2.playerState.scores.max}")
  }
}
