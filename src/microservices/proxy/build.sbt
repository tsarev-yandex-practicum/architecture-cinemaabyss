ThisBuild / scalaVersion := "2.13.15"
ThisBuild / version := "1.0.0"

lazy val root = (project in file("."))
  .settings(
    name := "proxy-service",
    Compile / mainClass := Some("cinemaabyss.proxy.Main"),
    libraryDependencies ++= Seq(
      "org.http4s" %% "http4s-ember-server" % "0.23.30",
      "org.http4s" %% "http4s-ember-client" % "0.23.30",
      "org.http4s" %% "http4s-dsl" % "0.23.30",
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
    assembly / assemblyJarName := "proxy-service.jar"
  )
