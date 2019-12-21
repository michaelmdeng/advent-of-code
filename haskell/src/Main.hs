module Main where

import qualified Y2019.Day1
import qualified Y2019.Day2

main :: IO ()
main = do
  res <- Y2019.Day1.main
  putStrLn res
  res <- Y2019.Day2.main
  putStrLn res
