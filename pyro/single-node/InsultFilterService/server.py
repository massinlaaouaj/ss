import Pyro4
import redis
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("insult_filter_service.log", mode="a"),
        logging.StreamHandler()
    ]
)

@Pyro4.behavior(instance_mode="single")
class InsultFilterService:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.subscribers = []

    def get_insults_list(self):
        return self.r.smembers("insults")

    def filter_text(self, text):
        insults_set = self.get_insults_list()
        return "CENSORED" if text in insults_set else text

    @Pyro4.expose
    def add_text(self, input_texts):
        if isinstance(input_texts, str):
            input_texts = [input_texts]

        resultados = []
        for text in input_texts:
            filtered = self.filter_text(text)
            if not self.r.sismember("filtered_texts", filtered):
                timestamp = datetime.utcnow().isoformat()
                next_id = self.r.incr("filtered_texts_id")
                self.r.hset("filtered_texts", next_id, f"{filtered}|{timestamp}")
                logging.info(f"Texto filtrado añadido: {filtered}")
                resultados.append(f"Texto registrado: {filtered} (UTC: {timestamp})")
            else:
                logging.info(f"Texto ya registrado: {filtered}")
                resultados.append(f"Texto ya registrado: {filtered}")
        return resultados

    @Pyro4.expose
    def get_texts(self):
        raw = self.r.hgetall("filtered_texts")
        return [{ "id": k, "text": v.split("|")[0], "timestamp": v.split("|")[1] } for k, v in raw.items()]

def main():
    daemon = Pyro4.Daemon(port=4040)
    obj = InsultFilterService()
    uri = daemon.register(obj, objectId="InsultFilterService")
    logging.info(f"InsultFilterService registrado en {uri}")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
