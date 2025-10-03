import pika
import json
import sys

def callback_log(ch, method, properties, body):
    data = json.loads(body)
    user = data.get('user', 'Usuário Desconhecido')
    event_type = data.get('event', 'evento desconhecido')
    # Saída solicitada: [LOG] João executou o evento: user.login
    print(f"[LOG] {user} executou o evento: {event_type}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_log():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
    except pika.exceptions.AMQPConnectionError as e:
        print(f"[-] ERRO: Não foi possível conectar ao RabbitMQ. Detalhes: {e}")
        sys.exit(1)

    channel.queue_declare(queue="log_queue", durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue="log_queue", 
        on_message_callback=callback_log, 
        auto_ack=False
    )

    print("[*] Aguardando mensagens de log geral. CTRL+C para sair.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print(" [x] Consumidor interrompido.")
        connection.close()

if __name__ == '__main__':
    consume_log()