import Pyro4
import redis
import time
import random
from multiprocessing import Process

@Pyro4.behavior(instance_mode="single")
class Notifier:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.subscribers = []

    @Pyro4.expose
    def subscribe(self, subscriber_uri):
        if subscriber_uri not in self.subscribers:
            self.subscribers.append(subscriber_uri)
            print(f"🟢 Suscriptor añadido: {subscriber_uri}")
        else:
            print("Suscriptor ya existente")

    @Pyro4.expose
    def unsubscribe(self, subscriber_uri):
        if subscriber_uri in self.subscribers:
            self.subscribers.remove(subscriber_uri)
            print(f"🔴 Suscriptor eliminado: {subscriber_uri}")

    def broadcast_loop(self):
        while True:
            insults = list(self.r.smembers("insults"))
            if not insults:
                print("⏳ No hay insultos disponibles.")
            elif not self.subscribers:
                print("⏳ No hay suscriptores registrados.")
            else:
                insult = random.choice(insults)
                for uri in self.subscribers:
                    try:
                        proxy = Pyro4.Proxy(uri)
                        proxy.update(insult)
                        print("📤 Enviado a:", uri)
                    except Exception as e:
                        print(f"❌ Error al enviar a {uri}: {e}")
            time.sleep(5)

def main():
    obj = Notifier()
    daemon = Pyro4.Daemon(port=4719)
    uri = daemon.register(obj, objectId="Notifier")
    print(f"Notifier con URI {uri} ejecutándose...")

    p = Process(target=obj.broadcast_loop, args=(), daemon=True)
    p.start()

    daemon.requestLoop()

if __name__ == "__main__":
    main()
