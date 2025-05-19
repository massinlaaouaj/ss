import Pyro4
import redis
import logging
import time
from datetime import datetime, timezone

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
        self.cached_insults = set()
        self.last_cache_time = 0
        self.cache_ttl = 10

    def get_insults_list(self):
        now = time.time()
        if now - self.last_cache_time > self.cache_ttl:
            self.cached_insults = self.r.smembers("insults")
            self.last_cache_time = now
        return self.cached_insults


    def filter_text(self, text):
        insults_set = self.get_insults_list()
        words = text.split()
        censored = [
            "CENSORED" if word.lower() in insults_set else word
            for word in words
        ]
        return " ".join(censored)

    @Pyro4.expose
    def add_text(self, input_texts):
        if isinstance(input_texts, str):
            input_texts = [input_texts]

        insults_set = self.get_insults_list()
        existing_texts = {v.split("|")[0] for v in self.r.hvals("filtered_texts")}

        pipe = self.r.pipeline()
        resultados = []

        for text in input_texts:
            text = text.lower()
            words = text.split()
            filtered = " ".join("CENSORED" if word in insults_set else word for word in words)

            if filtered not in existing_texts:
                timestamp = datetime.now(timezone.utc).isoformat()
                next_id = self.r.incr("filtered_texts_id")
                pipe.hset("filtered_texts", next_id, f"{filtered}|{timestamp}")
                resultados.append(f"Texto registrado: {filtered} (UTC: {timestamp})")
                logging.info(f"Texto filtrado añadido: {filtered}")
            else:
                resultados.append(f"Texto ya registrado: {filtered}")
                logging.info(f"Texto ya registrado: {filtered}")

        pipe.execute()
        return resultados




    @Pyro4.expose
    def get_texts(self):
        raw = self.r.hgetall("filtered_texts")
        return [{ "id": k, "text": v.split("|")[0], "timestamp": v.split("|")[1] } for k, v in raw.items()]

def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    obj = InsultFilterService()
    uri = daemon.register(obj, objectId="InsultFilterService")
    ns.register("InsultFilterService", uri)
    logging.info(f"InsultFilterService registrado en {uri}")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
