import pika, json

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"[LOG] {data['user']} executou o evento: {data['event']}")

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.basic_consume(queue="log_queue", on_message_callback=callback, auto_ack=True)

print(" [*] Aguardando mensagens de log geral. CTRL+C para sair.")
channel.start_consuming()
