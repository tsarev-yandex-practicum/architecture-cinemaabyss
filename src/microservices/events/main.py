import os
import json
import asyncio
from fastapi import FastAPI
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from contextlib import asynccontextmanager

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BROKERS", "kafka:9092")
TOPICS = ["movie-events", "user-events", "payment-events"]

producer = None

async def run_consumer():
    # Ждем немного перед запуском консьюмера
    await asyncio.sleep(5)
    consumer = AIOKafkaConsumer(
        *TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="events-group-python"
    )
    
    connected = False
    while not connected:
        try:
            await consumer.start()
            connected = True
            print("[Kafka Consumer] Connected successfully")
        except Exception:
            print("[Kafka Consumer] Waiting for Kafka...")
            await asyncio.sleep(3)
            
    try:
        async for msg in consumer:
            print(f"[Kafka Consumer] Topic: {msg.topic} | Message: {msg.value.decode('utf-8')}")
    finally:
        await consumer.stop()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global producer
    # Логика подключения Producer с повторами
    connected = False
    while not connected:
        try:
            producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
            await producer.start()
            connected = True
            print("[Kafka Producer] Connected successfully")
        except Exception as e:
            print(f"[Kafka Producer] Waiting for Kafka to be ready... ({e})")
            await asyncio.sleep(3)
    
    # Запускаем консьюмер в фоне
    consumer_task = asyncio.create_task(run_consumer())
    
    yield  # Здесь приложение работает
    
    # Логика при выключении
    await producer.stop()
    consumer_task.cancel()

app = FastAPI(lifespan=lifespan)

@app.get("/api/events/health")
async def health():
    return {"status": True}

@app.post("/api/events/{event_type}", status_code=201)
async def create_event(event_type: str, data: dict):
    if event_type not in ["movie", "user", "payment"]:
        return {"error": "Invalid event type"}, 400
    
    topic = f"{event_type}-events"
    message = json.dumps(data).encode("utf-8")
    
    await producer.send_and_wait(topic, message)
    
    return {
        "status": "success",
        "event": data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)
