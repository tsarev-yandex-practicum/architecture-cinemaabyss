package cinemaabyss.events

import cats.effect._
import fs2.kafka._
import org.slf4j.LoggerFactory

import scala.concurrent.duration._

object KafkaSupport {
  private val log = LoggerFactory.getLogger(getClass)

  val MovieTopic: String = "movie-events"
  val UserTopic: String = "user-events"
  val PaymentTopic: String = "payment-events"

  def producerSettings(brokers: String): ProducerSettings[IO, String, String] =
    ProducerSettings[IO, String, String].withBootstrapServers(brokers)

  def consumerSettings(brokers: String): ConsumerSettings[IO, String, String] =
    ConsumerSettings[IO, String, String]
      .withBootstrapServers(brokers)
      .withGroupId("events-service-mvp")
      .withAutoOffsetReset(AutoOffsetReset.Earliest)
      .withEnableAutoCommit(true)

  def waitForKafka(
      producer: KafkaProducer.PartitionsFor[IO, String, String],
      brokers: String
  ): IO[Unit] = {
    def loop(attempt: Int): IO[Unit] =
      producer.partitionsFor(MovieTopic).void.handleErrorWith { err =>
        if (attempt >= 15)
          IO.raiseError(new RuntimeException(s"Failed to connect to Kafka at $brokers", err))
        else
          IO.sleep(2.seconds) >> loop(attempt + 1)
      }

    loop(0)
  }

  def consumerStream(brokers: String): fs2.Stream[IO, Unit] =
    KafkaConsumer
      .stream(consumerSettings(brokers))
      .subscribeTo(MovieTopic, UserTopic, PaymentTopic)
      .records
      .evalMap { committable =>
        IO {
          val record = committable.record
          log.info(
            s"Consumed event topic=${record.topic} partition=${record.partition} offset=${record.offset} payload=${record.value}"
          )
        }
      }
}
