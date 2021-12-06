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

scalaVersion := "2.13.4"
scalacOptions ++= Seq("-feature", "-deprecation")

// -------------------
// Dependency settings
// --------------------

libraryDependencies ++= Seq(
  "org.scala-graph" %% "graph-core" % "1.13.1",
  "org.scala-lang.modules" %% "scala-parser-combinators" % "1.1.2",
  "org.typelevel" %% "cats-core" % "2.1.0",
  "org.typelevel" %% "cats-effect" % "2.3.1",
)

addCompilerPlugin("org.typelevel" % "kind-projector" % "0.13.2" cross CrossVersion.full)
