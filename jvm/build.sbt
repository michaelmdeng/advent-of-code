// ---------------
// Global settings
// ---------------

Global / onChangedBuildSource := ReloadOnSourceChanges

// ---------------
// Common settings
// ---------------
name := "AdventOfCode"
organization := "com.michaelmdeng"

fork := true

scalacOptions ++= Seq("-feature", "-deprecation")

// -------------------
// Dependency settings
// --------------------

libraryDependencies ++= Seq(
  "com.jsuereth" %% "scala-arm" % "2.0",
  "org.scala-graph" %% "graph-core" % "1.13.1",
  "org.scala-lang.modules" %% "scala-parser-combinators" % "1.1.2",
  "org.typelevel" %% "cats-core" % "1.1.0",
  "org.typelevel" %% "cats-effect" % "2.3.1",
)
