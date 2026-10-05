package cinemaabyss.events

import io.circe.{Encoder, Json}
import io.circe.generic.semiauto._

final case class HealthResponse(status: Boolean)

final case class EventResponse(
    status: String,
    partition: Int,
    offset: Long,
    event: Json
)

object Models {
  implicit val healthEncoder: Encoder[HealthResponse] = deriveEncoder
  implicit val eventResponseEncoder: Encoder[EventResponse] = deriveEncoder
}
