import pika
import json
import sys

def callback_login(ch, method, properties, body):
    data = json.loads(body)
    user = data.get('user', 'Usuário Desconhecido')
    # Saída solicitada: [LOGIN] João acabou de fazer login!
    print(f"[LOGIN] {user} acabou de fazer login!")
    ch.basic_ack(delivery_tag=method.delivery_tag) # Confirmação explícita (melhor que auto_ack=True)

def consume_login():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
    except pika.exceptions.AMQPConnectionError as e:
        print(f"[-] ERRO: Não foi possível conectar ao RabbitMQ. Detalhes: {e}")
        sys.exit(1)

    # Garante a fila e QOS para processar uma mensagem por vez
    channel.queue_declare(queue="login_queue", durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue="login_queue", 
        on_message_callback=callback_login, 
        auto_ack=False # Usar ack explícito no callback
    )

    print("[*] Aguardando mensagens de login. CTRL+C para sair.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print(" [x] Consumidor interrompido.")
        connection.close()

if __name__ == '__main__':
    consume_login()