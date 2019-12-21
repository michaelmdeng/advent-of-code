module Y2019.Day2 where

import Shared

import Control.Monad.State.Lazy
import Data.List.Index
import Data.List.Split
import GHC.Arr
import GHC.Base
import GHC.Enum
import GHC.Read
import GHC.Show

data Operation
  = Add
  | Mult
  | Halt
  deriving (Eq, Enum, Read, Show)

fromOpcode :: Int -> Operation
fromOpcode code =
  case code of
    1 -> Add
    2 -> Mult
    99 -> Halt
    other -> error "Invalid opcode."

type ProgramPosition = Int

type ProgramInstructions = [Int]

type ProgramState = (ProgramInstructions, ProgramPosition)

processAdd :: State ProgramState ()
processAdd = do
  state <- get
  let (instructions, position) = state
  let operand1Idx = instructions !! (position + 1)
  let operand1 = instructions !! operand1Idx
  let operand2Idx = instructions !! (position + 2)
  let operand2 = instructions !! operand2Idx
  let updatePos = instructions !! (position + 3)
  put (setAt updatePos (operand1 + operand2) instructions, position + 4)
  return ()

processMult :: State ProgramState ()
processMult = do
  state <- get
  let (instructions, position) = state
  let operand1Idx = instructions !! (position + 1)
  let operand1 = instructions !! operand1Idx
  let operand2Idx = instructions !! (position + 2)
  let operand2 = instructions !! operand2Idx
  let updatePos = instructions !! (position + 3)
  put (setAt updatePos (operand1 * operand2) instructions, position + 4)
  return ()

processHalt :: State ProgramState ()
processHalt = do
  state <- get
  put (fst state, -1)

processOperation :: State ProgramState ()
processOperation = do
  state <- get
  let opcode = fst state !! snd state
  let op = fromOpcode opcode
  case op of
    Add -> processAdd
    Mult -> processMult
    Halt -> processHalt
  return ()

processAll :: State ProgramState Int
processAll = do
  processOperation
  state <- get
  if snd state < 0 || snd state >= length (fst state)
    then return ((fst state) !! 0)
    else processAll

formatInput :: [String] -> [Int]
formatInput lines = map (\s -> read s) (splitOn "," (head lines))

setInput :: Int -> Int -> [Int] -> [Int]
setInput noun verb program = setAt 2 verb (setAt 1 noun program)

part1 lines = evalState processAll ((setInput 12 2 (formatInput lines)), 0)

processPart2 lines = do
  noun <- [1 .. 100]
  verb <- [1 .. 100]
  let a = evalState processAll ((setInput noun verb (formatInput lines)), 0)
  return (noun, verb, a)

part2 lines =
  head
    (map
       (\(n, v, out) -> 100 * n + v)
       (filter (\(n, v, out) -> out == 19690720) (processPart2 lines)))

main = runAdventCalendarPure (2019, 2) part1 part2
