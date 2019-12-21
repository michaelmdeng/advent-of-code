module Shared where

import Data.Advent

import Paths_advent
import System.IO

app :: [String] -> String -> [String]
app acc elem = acc ++ [elem]

readAllHelper :: Handle -> [String] -> IO [String]
readAllHelper handle acc = do
  isEOF <- hIsEOF handle
  out <-
    if isEOF
      then pure acc
      else do
        line <- hGetLine handle
        lines <- readAllHelper handle (app acc line)
        return lines
  return out

readAll :: FilePath -> IO [String]
readAll path = do
  handle <- openFile path ReadMode
  lines <- readAllHelper handle []
  return lines

runAdventPart :: Show a => AdventCalendar -> ([String] -> IO a) -> IO String
runAdventPart calendar operation = do
  lines <-
    readAll
      ("../../input/y" ++
       (show (fst calendar)) ++ "/day" ++ (show (snd calendar)) ++ ".txt")
  output <- operation lines
  let outputStr = "Result: " ++ show output
  return outputStr

runAdventPartPure :: Show a => AdventCalendar -> ([String] -> a) -> IO String
runAdventPartPure calendar operation = do
  filePath <-
    getDataFileName
      ("data/" ++
       (show (fst calendar)) ++ "/day" ++ (show (snd calendar)) ++ ".txt")
  lines <- readAll filePath
  output <- pure (operation lines)
  let outputStr = "Result: " ++ show output
  return outputStr

runAdventCalendar ::
     (Show a, Show b)
  => AdventCalendar
  -> ([String] -> IO a)
  -> ([String] -> IO b)
  -> IO String
runAdventCalendar calendar op1 op2 = do
  output1 <- runAdventPart calendar op1
  output2 <- runAdventPart calendar op2
  return (output1 ++ "\n" ++ output2)

runAdventCalendarPure ::
     (Show a, Show b)
  => AdventCalendar
  -> ([String] -> a)
  -> ([String] -> b)
  -> IO String
runAdventCalendarPure calendar op1 op2 = do
  output1 <- runAdventPartPure calendar op1
  output2 <- runAdventPartPure calendar op2
  return (output1 ++ "\n" ++ output2)
