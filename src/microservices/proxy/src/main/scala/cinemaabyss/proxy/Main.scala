package cinemaabyss.proxy

import cats.effect._
import com.comcast.ip4s._
import org.http4s.ember.client.EmberClientBuilder
import org.http4s.ember.server.EmberServerBuilder
import org.slf4j.LoggerFactory

object Main extends IOApp.Simple {
  private val log = LoggerFactory.getLogger(getClass)

  override def run: IO[Unit] = {
    val config = Config.load
    log.info(s"Starting proxy on port ${config.port}")

    EmberClientBuilder.default[IO].build.use { client =>
      val httpApp = ProxyRoutes.routes(config, client).orNotFound

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
