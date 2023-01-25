import pika

from moneyroundup.settings import settings

QUEUE = "transactions_summary"

conn = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBIT_HOST))

channel = conn.channel()

channel.queue_declare(queue=QUEUE)

channel.basic_publish(exchange="", routing_key=QUEUE, body="Hello World")

print("SENT")

conn.close()
