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
// ----------ß---------

libraryDependencies ++= Seq(
  "org.typelevel" %% "cats-core" % "1.1.0",
  "com.jsuereth" %% "scala-arm" % "2.0"
)
