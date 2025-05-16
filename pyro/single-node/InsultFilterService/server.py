import Pyro4
import redis
import logging
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

    def get_insults_list(self):
        return self.r.smembers("insults")

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

        # 1) Preprocesar y filtrar
        filtered_list = [self.filter_text(txt.lower()) for txt in input_texts]

        # 2) Pipeline fase 1: comprobamos membresía
        pipe = self.r.pipeline()
        for f in filtered_list:
            pipe.sismember(self.texts_set, f)
        exists = pipe.execute()  # lista de bool

        resultados = []
        nuevos = []  # recogemos (filtro, timestamp) de los nuevos

        # 3) Construir respuesta y lista de inserción
        for f, ex in zip(filtered_list, exists):
            if not ex:
                ts = datetime.now(timezone.utc).isoformat()
                nuevos.append((f, ts))
                resultados.append(None)  # placeholder
            else:
                resultados.append(f"Texto ya registrado: {f}")

        # 4) Pipeline fase 2: añadimos solo los nuevos en lote
        pipe2 = self.r.pipeline()
        for f, ts in nuevos:
            pipe2.incr("filtered_texts_id")
            pipe2.hset("filtered_texts", "__ID__", f"{f}|{ts}")  # __ID__ será remplazado tras ejecutar
            pipe2.sadd(self.texts_set, f)
        resp2 = pipe2.execute()

        # 5) Extraer IDs y rellenar mensajes
        # resp2 = [id1,1,1, id2,1,1, ...]
        ids = [resp2[i] for i in range(0, len(resp2), 3)]
        j = 0
        for idx, val in enumerate(resultados):
            if val is None:
                f, ts = nuevos[j]
                resultados[idx] = f"Texto registrado: {f} (ID: {ids[j]}, UTC: {ts})"
                j += 1

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
