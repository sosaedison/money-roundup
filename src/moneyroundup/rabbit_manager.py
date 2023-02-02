from typing import Protocol
from pika import BlockingConnection, ConnectionParameters


class QueueManager(Protocol):
    def consume(self) -> str:
        """Consume a message from the queue.

        Returns:
            str: The message consumed from the queue.
        """
        ...

    def produce(self, body: str) -> bool:
        """Produce a message to the queue.

        Args:
            body (str): The message to be produced.

        Returns:
            bool: True if the message was produced successfully.
        """
        ...


class RabbitManager:
    def __init__(self, host: str, queue: str) -> None:
        self.queue = queue
        self.connection = BlockingConnection(ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)

    def consume(self) -> str:
        BODY = 2
        message = self.channel.basic_get(self.queue, auto_ack=True)

        return str(message[BODY])

    def produce(self, body: str) -> bool:
        try:
            self.channel.basic_publish(exchange="", routing_key=self.queue, body=body)
        except Exception as e:
            raise e

        return True
