import pika, json, datetime, sys

def publish(event: str, user: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    msg = {
        "user": user,
        "event": event,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

    channel.basic_publish(
        exchange="user_events",
        routing_key=event,
        body=json.dumps(msg),
        properties=pika.BasicProperties(content_type="application/json")
    )
    print(f"[PRODUTOR] Enviado: {msg}")
    connection.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python producer.py <evento> <usuario>")
        sys.exit(1)
    publish(sys.argv[1], sys.argv[2])
