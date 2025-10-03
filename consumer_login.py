import pika, json

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"[LOGIN] {data['user']} acabou de fazer login!")

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.basic_consume(queue="login_queue", on_message_callback=callback, auto_ack=True)

print(" [*] Aguardando mensagens de login. CTRL+C para sair.")
channel.start_consuming()
