import pika, sys, os


QUEUE = "transactions_summary"


def main():
    conn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))

    channel = conn.channel()

    channel.queue_declare(queue=QUEUE)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue=QUEUE, auto_ack=True, on_message_callback=callback)

    print("WAITING FOR MESSAGES")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("RECEIVING STOPPED")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
