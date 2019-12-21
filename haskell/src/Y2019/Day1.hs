module Y2019.Day1 where

import Shared

fuel :: Integer -> Integer
fuel mass = max 0 ((mass `div` 3) - 2)

totalFuel :: [String] -> Integer
totalFuel masses =
  sum
    (do massStr <- masses
        let mass = read massStr :: Integer
        return (fuel mass))

recursiveFuel :: Integer -> Integer
recursiveFuel mass =
  if fuel (mass) > 0
    then fuel mass + recursiveFuel (fuel mass)
    else 0

totalRecursiveFuel :: [String] -> Integer
totalRecursiveFuel masses =
  sum
    (do massStr <- masses
        let mass = read massStr :: Integer
        return (recursiveFuel mass))

part1 lines = show (totalFuel lines)

part2 lines = show (totalRecursiveFuel lines)

main = runAdventCalendarPure (2019, 1) part1 part2
