package cinemaabyss.events

import cats.effect._
import com.comcast.ip4s._
import fs2.kafka.KafkaProducer
import org.http4s.ember.server.EmberServerBuilder
import org.slf4j.LoggerFactory

object Main extends IOApp.Simple {
  private val log = LoggerFactory.getLogger(getClass)

  override def run: IO[Unit] = {
    val config = Config.load
    log.info(s"Starting events service on port ${config.port}, kafka=${config.kafkaBrokers}")

    KafkaProducer.resource(KafkaSupport.producerSettings(config.kafkaBrokers)).use { producer =>
      KafkaSupport.waitForKafka(producer, config.kafkaBrokers) >>
        KafkaSupport
          .consumerStream(config.kafkaBrokers)
          .compile
          .drain
          .background
          .use { _ =>
            val httpApp = EventsRoutes.routes(producer).orNotFound

            EmberServerBuilder
              .default[IO]
              .withHost(ipv4"0.0.0.0")
              .withPort(Port.fromInt(config.port).get)
              .withHttpApp(httpApp)
              .build
              .useForever
          }
    }
  }
}
