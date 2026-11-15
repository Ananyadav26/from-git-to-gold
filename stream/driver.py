import pika
import json
import sys

if len(sys.argv) != 3:
    print("Usage: python driver.py NAME PATTERN")
    sys.exit(1)

name = sys.argv[1]
pattern = sys.argv[2]

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)
channel = connection.channel()

channel.exchange_declare(
    exchange="rapido-dispatch",
    exchange_type="topic",
    durable=True
)

result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

channel.queue_bind(
    exchange="rapido-dispatch",
    queue=queue_name,
    routing_key=pattern
)

channel.basic_qos(prefetch_count=1)

def process_message(ch, method, properties, body):
    message = json.loads(body)

    if "zone" not in message:
        print(
            f"{name} | NACK | Missing zone | {message}",
            flush=True
        )
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )
    else:
        print(
            f"{name} | ACK | {method.routing_key} | {message}",
            flush=True
        )
        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )

print(
    f"{name} listening with pattern: {pattern}",
    flush=True
)

channel.basic_consume(
    queue=queue_name,
    on_message_callback=process_message,
    auto_ack=False
)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print(f"{name} stopped")
finally:
    connection.close()
