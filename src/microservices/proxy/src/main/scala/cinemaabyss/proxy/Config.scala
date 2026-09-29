package cinemaabyss.proxy

import scala.util.Try

final case class Config(
    port: Int,
    monolithUrl: String,
    moviesServiceUrl: String,
    eventsServiceUrl: String,
    gradualMigration: Boolean,
    moviesMigrationPercent: Int
)

object Config {
  def load: Config = {
    val gradualMigration = sys.env.get("GRADUAL_MIGRATION").exists(_.equalsIgnoreCase("true"))
    val percent = sys.env
      .get("MOVIES_MIGRATION_PERCENT")
      .flatMap(v => Try(v.toInt).toOption)
      .getOrElse(0)
      .max(0)
      .min(100)

    Config(
      port = sys.env.get("PORT").flatMap(v => Try(v.toInt).toOption).getOrElse(8000),
      monolithUrl = stripTrailingSlash(sys.env.getOrElse("MONOLITH_URL", "http://monolith:8080")),
      moviesServiceUrl =
        stripTrailingSlash(sys.env.getOrElse("MOVIES_SERVICE_URL", "http://movies-service:8081")),
      eventsServiceUrl =
        stripTrailingSlash(sys.env.getOrElse("EVENTS_SERVICE_URL", "http://events-service:8082")),
      gradualMigration = gradualMigration,
      moviesMigrationPercent = percent
    )
  }

  private def stripTrailingSlash(url: String): String =
    if (url.endsWith("/")) url.dropRight(1) else url
}
