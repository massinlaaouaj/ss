import pika
import json
from config.config import config

def publish_insults(insult_list):
    credentials = pika.PlainCredentials(config.USERNAME, config.PASSWORD)
    parameters = pika.ConnectionParameters(config.RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=config.INSULTSERVICE_QUEUE_NAME, durable=True)

    if isinstance(insult_list, str):
        insult_list = [insult_list]

    for insult in insult_list:
        message = json.dumps({"insult": insult})
        channel.basic_publish(
            exchange='',
            routing_key=config.INSULTSERVICE_QUEUE_NAME,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(f"📤 Sent insult: {insult}")

    connection.close()

if __name__ == "__main__":
    insults = ["moron", "twit", "loser", "clown"]
    publish_insults(insults)
