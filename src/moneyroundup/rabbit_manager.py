from typing import Tuple
from pika import BlockingConnection, ConnectionParameters
from pika.spec import BasicProperties
from pika.spec import Basic


class RabbitManager:
    def __init__(self, host: str, queue: str) -> None:
        self.queue = queue
        self.connection = BlockingConnection(ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)

    def consume(self) -> str:
        BODY = 2
        message: Tuple[
            Basic.GetOk | None, BasicProperties | None, bytes | None
        ] = self.channel.basic_get(self.queue, auto_ack=True)

        return str(message[BODY])

    def produce(self, body: str) -> bool:
        try:
            self.channel.basic_publish(exchange="", routing_key=self.queue, body=body)
        except Exception as e:
            raise e

        return True
