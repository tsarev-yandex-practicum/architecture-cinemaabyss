package cinemaabyss.events

import cats.effect.IO
import fs2.kafka._
import io.circe.Json
import org.http4s.circe.CirceEntityCodec._
import org.http4s.dsl.io._
import org.http4s.HttpRoutes
import cinemaabyss.events.Models._

object EventsRoutes {
  def routes(producer: KafkaProducer.PartitionsFor[IO, String, String]): HttpRoutes[IO] = HttpRoutes.of[IO] {
    case GET -> Root / "api" / "events" / "health" =>
      Ok(HealthResponse(status = true))

    case req @ POST -> Root / "api" / "events" / "movie" =>
      publishEvent(producer, KafkaSupport.MovieTopic, req)

    case req @ POST -> Root / "api" / "events" / "user" =>
      publishEvent(producer, KafkaSupport.UserTopic, req)

    case req @ POST -> Root / "api" / "events" / "payment" =>
      publishEvent(producer, KafkaSupport.PaymentTopic, req)
  }

  private def publishEvent(
      producer: KafkaProducer.PartitionsFor[IO, String, String],
      topic: String,
      req: org.http4s.Request[IO]
  ): IO[org.http4s.Response[IO]] =
    req.as[Json].flatMap { body =>
      val payload = body.noSpaces

      producer
        .produceOne_(topic, "event-key", payload)
        .flatten
        .flatMap { metadata =>
          Created(
            EventResponse(
              status = "success",
              partition = metadata.partition(),
              offset = metadata.offset(),
              event = body
            )
          )
        }
        .handleErrorWith { err =>
          InternalServerError(Json.obj("error" -> Json.fromString(err.getMessage)))
        }
    }
}
