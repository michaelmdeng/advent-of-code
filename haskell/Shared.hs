module Shared where

import System.IO

app :: [String] -> String -> [String]
app acc elem = acc ++ [elem]

readAllHelper :: Handle -> [String] -> IO [String]
readAllHelper handle acc = do
        isEOF <- hIsEOF handle
        out <- if isEOF
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

