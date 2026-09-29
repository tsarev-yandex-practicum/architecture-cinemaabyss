package cinemaabyss.proxy

import cats.effect.IO
import org.http4s._
import org.http4s.client.Client
import org.http4s.dsl.io._
import org.slf4j.LoggerFactory
import org.typelevel.ci.CIString

import scala.util.Random

object ProxyRoutes {
  private val log = LoggerFactory.getLogger(getClass)

  private val HopByHopHeaders: Set[String] = Set(
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "host"
  )

  def routes(config: Config, client: Client[IO]): HttpRoutes[IO] = HttpRoutes.of[IO] {
    case GET -> Root / "health" =>
      Ok("Strangler Fig Proxy is healthy")

    case req =>
      selectUpstreamBase(config, req.uri.path.renderString).flatMap { upstreamBase =>
        proxyRequest(client, req, upstreamBase)
      }
  }

  private def selectUpstreamBase(config: Config, path: String): IO[String] =
    if (path.startsWith("/api/events")) {
      IO.pure(config.eventsServiceUrl)
    } else if (path.startsWith("/api/movies")) {
      val target =
        if (config.gradualMigration) {
          val roll = Random.nextInt(100)
          if (roll < config.moviesMigrationPercent) config.moviesServiceUrl
          else config.monolithUrl
        } else {
          config.moviesServiceUrl
        }

      IO {
        log.info(
          s"Movies request routed to $target (gradual=${config.gradualMigration}, percent=${config.moviesMigrationPercent})"
        )
        target
      }
    } else {
      IO.pure(config.monolithUrl)
    }

  private def proxyRequest(client: Client[IO], req: Request[IO], upstreamBase: String): IO[Response[IO]] = {
    val targetUri = Uri
      .unsafeFromString(upstreamBase)
      .withPath(req.uri.path)
      .withQueryParams(req.uri.query.params)

    val forwardedHeaders = req.headers.headers.filterNot { header =>
      HopByHopHeaders.contains(header.name.toString.toLowerCase)
    }

    val forwarded = req
      .withUri(targetUri)
      .withHeaders(forwardedHeaders)
      .removeHeader(CIString("Host"))

    client
      .run(forwarded)
      .use { response =>
        val responseHeaders = response.headers.headers.filterNot { header =>
          HopByHopHeaders.contains(header.name.toString.toLowerCase)
        }

        IO.pure(
          response
            .withHeaders(responseHeaders)
            .removeHeader(CIString("Transfer-Encoding"))
        )
      }
      .handleErrorWith { err =>
        IO {
          log.error(s"Upstream request failed for ${req.method} ${req.uri}", err)
        } >> ServiceUnavailable(s"Upstream unavailable: ${err.getMessage}")
      }
  }
}
