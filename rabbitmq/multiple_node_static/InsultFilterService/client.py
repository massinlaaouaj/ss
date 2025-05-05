import pika
import json
from config.config import config

def publish_texts(text_list):
    credentials = pika.PlainCredentials(config.USERNAME, config.PASSWORD)
    parameters = pika.ConnectionParameters(config.RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(parameters)


    channel = connection.channel()

    channel.queue_declare(queue=config.INSULTFILTERSERVICE_QUEUE_NAME, durable=True)

    if isinstance(text_list, str):
        text_list = [text_list]

    for text in text_list:
        message = json.dumps({"text": text})
        channel.basic_publish(
            exchange='',
            routing_key=config.INSULTFILTERSERVICE_QUEUE_NAME,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(f"📤 Sent text: {text}")

    connection.close()

if __name__ == "__main__":
    texts = [
        "You're such a clown",
        "That was a moron move",
        "Twit behavior again?",
        "What a loser you are"
    ]
    publish_texts(texts)
