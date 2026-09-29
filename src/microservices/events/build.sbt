ThisBuild / scalaVersion := "2.13.15"
ThisBuild / version := "1.0.0"

lazy val root = (project in file("."))
  .settings(
    name := "events-service",
    Compile / mainClass := Some("cinemaabyss.events.Main"),
    libraryDependencies ++= Seq(
      "org.http4s" %% "http4s-ember-server" % "0.23.30",
      "org.http4s" %% "http4s-dsl" % "0.23.30",
      "org.http4s" %% "http4s-circe" % "0.23.30",
      "io.circe" %% "circe-core" % "0.14.10",
      "io.circe" %% "circe-generic" % "0.14.10",
      "io.circe" %% "circe-parser" % "0.14.10",
      "com.github.fd4s" %% "fs2-kafka" % "3.4.0",
      "ch.qos.logback" % "logback-classic" % "1.5.12"
    ),
    assembly / assemblyMergeStrategy := {
      case PathList("META-INF", "services", _*)           => MergeStrategy.concat
      case PathList("META-INF", "io.netty.versions.properties") => MergeStrategy.last
      case PathList("META-INF", _*)                       => MergeStrategy.discard
      case "module-info.class"                            => MergeStrategy.discard
      case x =>
        val old = (assembly / assemblyMergeStrategy).value
        old(x)
    },
    assembly / assemblyJarName := "events-service.jar"
  )
