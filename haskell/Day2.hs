import Shared

import Control.Monad.State.Lazy
import Data.List.Split
import GHC.Base
import GHC.Show
import GHC.Read
import GHC.Arr
import GHC.Enum

set :: Int -> Int -> [Int] -> [Int]
set x idx list = if idx < 0 || idx >= length list
		    then list
	else take idx list ++ [x] ++ drop (idx + 1) list

data Operation = Add | Mult | Halt
	deriving (Eq
	  , Ord
	  , Ix
	  , Enum
	  , Read
	  , Show
	  )

fromOpcode :: Int -> Operation
fromOpcode code = case code of 1 -> Add
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
 	put (set (operand1 + operand2) updatePos instructions, position + 4)
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
 	put (set (operand1 * operand2) updatePos instructions, position + 4)
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
	case op of Add -> processAdd
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

setInput :: Int -> Int -> [Int] -> [Int]
setInput noun verb program = set verb 2 (set noun 1 program)

part1 = do
    lines <- Shared.readAll "../input/2019/day2.txt"
    let program = setInput 12 2 (map (\s -> read s) (splitOn "," (head lines)))
    return (evalState processAll (program, 0))

part2 = do
	lines <- Shared.readAll "../input/2019/day2.txt"
	let program = map (\s -> read s::Int) (splitOn "," (head lines))
	let outputs = do
		noun <- [1..100]
		verb <- [1..100]
		let a = evalState processAll ((setInput noun verb program), 0)
		return (noun, verb, a)
	let output = head (map (\(n, v, out) -> 100 * n + v) (filter (\(n, v, out) -> out == 19690720) outputs))
	return output

main = do
        res1 <- part1
        putStrLn (show res1)
        res2 <- part2
        putStrLn (show res2)

