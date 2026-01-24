const express = require("express");
const { Kafka } = require("kafkajs");

const app = express();
app.use(express.json());

const PORT = 8082;
const KAFKA_BROKERS = (process.env.KAFKA_BROKERS || "kafka:9092").split(",");
const TOPICS = ["movie-events", "user-events", "payment-events"];

let producer;

const kafka = new Kafka({
    clientId: "events-service-node",
    brokers: KAFKA_BROKERS,
});

async function runConsumer() {
    await new Promise(r => setTimeout(r, 5000));

    const consumer = kafka.consumer({ groupId: "events-group-node" });

    let connected = false;
    while (!connected) {
        try {
            await consumer.connect();
            for (const topic of TOPICS) {
                await consumer.subscribe({ topic, fromBeginning: false });
            }
            connected = true;
            console.log("[Kafka Consumer] Connected successfully");
        } catch (err) {
            console.log("[Kafka Consumer] Waiting for Kafka...");
            await new Promise(r => setTimeout(r, 3000));
        }
    }

    await consumer.run({
        eachMessage: async ({ topic, message }) => {
            console.log(
                `[Kafka Consumer] Topic: ${topic} | Message: ${message.value.toString()}`
            );
        }
    });
}

async function initProducer() {
    let connected = false;

    while (!connected) {
        try {
            producer = kafka.producer();
            await producer.connect();
            connected = true;
            console.log("[Kafka Producer] Connected successfully");
        } catch (err) {
            console.log(`[Kafka Producer] Waiting for Kafka to be ready... (${err.message})`);
            await new Promise(r => setTimeout(r, 3000));
        }
    }
}

app.get("/api/events/health", (req, res) => {
    res.json({ status: true });
});

app.post("/api/events/:eventType", async (req, res) => {
    const { eventType } = req.params;
    const data = req.body;

    if (!["movie", "user", "payment"].includes(eventType)) {
        return res.status(400).json({ error: "Invalid event type" });
    }

    const topic = `${eventType}-events`;
    const message = JSON.stringify(data);

    await producer.send({
        topic,
        messages: [{ value: message }]
    });

    res.status(201).json({
        status: "success",
        event: data
    });
});

async function start() {
    await initProducer();
    runConsumer().catch(err =>
        console.error("[Kafka Consumer] Fatal error:", err)
    );

    app.listen(PORT, "0.0.0.0", () => {
        console.log(`Events service listening on port ${PORT}`);
    });
}

process.on("SIGTERM", async () => {
    if (producer) await producer.disconnect();
    process.exit(0);
});

process.on("SIGINT", async () => {
    if (producer) await producer.disconnect();
    process.exit(0);
});

start();