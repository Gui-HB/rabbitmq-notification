import pika
import sys

def setup():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
    except pika.exceptions.AMQPConnectionError as e:
        print(f"[-] ERRO: Não foi possível conectar ao RabbitMQ. Detalhes: {e}")
        sys.exit(1)

    # Exchange direct
    channel.exchange_declare(exchange="user_events", exchange_type="direct", durable=True)

    # Filas
    channel.queue_declare(queue="login_queue", durable=True)
    channel.queue_declare(queue="log_queue", durable=True)

    # Bindings
    # 1. login_queue recebe apenas 'user.login'
    channel.queue_bind(exchange="user_events", queue="login_queue", routing_key="user.login")
    
    # 2. log_queue recebe todos os eventos
    for key in ["user.login", "user.upload", "user.logout"]:
        channel.queue_bind(exchange="user_events", queue="log_queue", routing_key=key)

    print("Exchange e filas configuradas com sucesso.")
    connection.close()

if __name__ == "__main__":
    setup()