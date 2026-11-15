import pika
import json
import random
import time
import uuid
from datetime import datetime, timezone

EXCHANGE = "rapido-dispatch"

cities = {
    "bangalore": ["koramangala", "indiranagar", "whitefield"],
    "chennai": ["tnagar", "whitefield"]
}

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)
channel = connection.channel()

channel.exchange_declare(
    exchange=EXCHANGE,
    exchange_type="topic",
    durable=True
)

count = 0

try:
    while True:
        count += 1

        city = random.choice(list(cities.keys()))
        zone = random.choice(cities[city])
        request_type = random.choice(["ride", "food"])

        routing_key = f"{city}.{zone}.{request_type}"

        message = {
            "id": str(uuid.uuid4()),
            "city": city,
            "zone": zone,
            "type": request_type,
            "ts": datetime.now(timezone.utc).isoformat()
        }

        if count % 10 == 0:
            message.pop("zone")

        channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2
            )
        )

        print(
            f"PUBLISHED #{count} | {routing_key} | {message}",
            flush=True
        )

        time.sleep(2)

except KeyboardInterrupt:
    print("Dispatcher stopped")

finally:
    connection.close()
