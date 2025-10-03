import pika

def setup():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Exchange direct
    channel.exchange_declare(exchange="user_events", exchange_type="direct", durable=True)

    # Filas
    channel.queue_declare(queue="login_queue", durable=True)
    channel.queue_declare(queue="log_queue", durable=True)

    # Bindings
    channel.queue_bind(exchange="user_events", queue="login_queue", routing_key="user.login")

    for key in ["user.login", "user.upload", "user.logout"]:
        channel.queue_bind(exchange="user_events", queue="log_queue", routing_key=key)

    print("Exchange e filas configuradas com sucesso.")
    connection.close()

if __name__ == "__main__":
    setup()
