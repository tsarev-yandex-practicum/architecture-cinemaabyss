import os
import json
import logging
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from kafka import KafkaProducer, KafkaConsumer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("events")

KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", "kafka:9092").split(",")
PORT = int(os.getenv("PORT", "8082"))

TOPIC_MOVIE_EVENTS = "movie-events"
TOPIC_USER_EVENTS = "user-events"
TOPIC_PAYMENT_EVENTS = "payment-events"

producer = None


def get_producer():
    global producer
    if producer is None:
        for attempt in range(30):
            try:
                producer = KafkaProducer(
                    bootstrap_servers=KAFKA_BROKERS,
                    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                    key_serializer=lambda k: k.encode("utf-8") if k else None,
                )
                logger.info("Kafka producer connected")
                return producer
            except Exception as e:
                logger.warning("Kafka not ready (attempt %d): %s", attempt + 1, e)
                time.sleep(2)
        raise RuntimeError("Could not connect to Kafka")
    return producer


def consume_topic(topic):
    """Consumer thread for a single topic."""
    time.sleep(10)  # Wait for Kafka to be ready
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=KAFKA_BROKERS,
            group_id="events-service-group",
            auto_offset_reset="earliest",
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        logger.info("[Consumer] Started consuming topic: %s", topic)
        for message in consumer:
            logger.info(
                "[Consumer] Topic=%s Partition=%d Offset=%d Key=%s Value=%s",
                message.topic,
                message.partition,
                message.offset,
                message.key.decode("utf-8") if message.key else None,
                json.dumps(message.value),
            )
    except Exception as e:
        logger.error("[Consumer] Error consuming %s: %s", topic, e)


def start_consumers():
    for topic in [TOPIC_MOVIE_EVENTS, TOPIC_USER_EVENTS, TOPIC_PAYMENT_EVENTS]:
        t = threading.Thread(target=consume_topic, args=(topic,), daemon=True)
        t.start()


class EventsHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/api/events/health":
            self._json_response(200, {"status": True})
        else:
            self._json_response(404, {"error": "Not found"})

    def do_POST(self):
        if self.path == "/api/events/movie":
            self._handle_movie_event()
        elif self.path == "/api/events/user":
            self._handle_user_event()
        elif self.path == "/api/events/payment":
            self._handle_payment_event()
        else:
            self._json_response(404, {"error": "Not found"})

    def _read_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(content_length)
        return json.loads(raw)

    def _handle_movie_event(self):
        try:
            event = self._read_body()
        except (json.JSONDecodeError, ValueError):
            self._json_response(400, {"error": "Invalid request body"})
            return

        if not event.get("movie_id") or not event.get("title") or not event.get("action"):
            self._json_response(400, {"error": "movie_id, title, and action are required"})
            return

        key = f"movie-{event['movie_id']}-{event['action']}"
        partition, offset = self._publish(TOPIC_MOVIE_EVENTS, key, event)
        logger.info("[Producer] Movie event published: %s", key)
        self._json_response(201, {
            "status": "success",
            "partition": partition,
            "offset": offset,
            "event": event,
        })

    def _handle_user_event(self):
        try:
            event = self._read_body()
        except (json.JSONDecodeError, ValueError):
            self._json_response(400, {"error": "Invalid request body"})
            return

        if not event.get("user_id") or not event.get("action") or not event.get("timestamp"):
            self._json_response(400, {"error": "user_id, action, and timestamp are required"})
            return

        key = f"user-{event['user_id']}-{event['action']}"
        partition, offset = self._publish(TOPIC_USER_EVENTS, key, event)
        logger.info("[Producer] User event published: %s", key)
        self._json_response(201, {
            "status": "success",
            "partition": partition,
            "offset": offset,
            "event": event,
        })

    def _handle_payment_event(self):
        try:
            event = self._read_body()
        except (json.JSONDecodeError, ValueError):
            self._json_response(400, {"error": "Invalid request body"})
            return

        required = ["payment_id", "user_id", "amount", "status", "timestamp"]
        if not all(event.get(f) for f in required):
            self._json_response(400, {"error": "payment_id, user_id, amount, status, and timestamp are required"})
            return

        key = f"payment-{event['payment_id']}-{event['status']}"
        partition, offset = self._publish(TOPIC_PAYMENT_EVENTS, key, event)
        logger.info("[Producer] Payment event published: %s", key)
        self._json_response(201, {
            "status": "success",
            "partition": partition,
            "offset": offset,
            "event": event,
        })

    def _publish(self, topic, key, event):
        p = get_producer()
        future = p.send(topic, key=key, value=event)
        record = future.get(timeout=10)
        return record.partition, record.offset

    def _json_response(self, status_code, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        logger.info(format, *args)


if __name__ == "__main__":
    start_consumers()
    logger.info("Events service listening on port %d, Kafka brokers: %s", PORT, KAFKA_BROKERS)
    server = HTTPServer(("0.0.0.0", PORT), EventsHandler)
    server.serve_forever()
