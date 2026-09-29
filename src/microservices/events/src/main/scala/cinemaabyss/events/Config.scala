package cinemaabyss.events

import scala.util.Try

final case class Config(
    port: Int,
    kafkaBrokers: String
)

object Config {
  def load: Config =
    Config(
      port = sys.env.get("PORT").flatMap(v => Try(v.toInt).toOption).getOrElse(8082),
      kafkaBrokers = sys.env.getOrElse("KAFKA_BROKERS", "kafka:9092")
    )
}
