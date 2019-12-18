import Shared

fuel :: Integer -> Integer
fuel mass = max 0 ((quot mass 3) - 2)

totalFuel :: [String] -> Integer
totalFuel masses = sum (do
        massStr <- masses
        let mass = read massStr::Integer
        return (fuel mass))

recursiveFuel :: Integer -> Integer
recursiveFuel mass = if fuel (mass) > 0
        then fuel mass + recursiveFuel (fuel mass)
        else 0

totalRecursiveFuel :: [String] -> Integer
totalRecursiveFuel masses = sum (do
        massStr <- masses
        let mass = read massStr::Integer
        return (recursiveFuel mass))

part1 = do
    lines <- Shared.readAll "../input/2019/day1.txt"
    return (show (totalFuel lines))

part2 = do
    lines <- Shared.readAll "../input/2019/day1.txt"
    return (show (totalRecursiveFuel lines))

main = do
        res1 <- part1
        putStrLn (res1)
        res2 <- part2
        putStrLn (res2)
