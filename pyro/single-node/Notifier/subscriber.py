from Pyro4 import Daemon, Proxy, expose, locateNS
from observer import Observer

class Subscriber(Observer):
    @expose
    def update(self, insult):   
        print("Event: ", insult)

def main():
    with Daemon() as daemon:
        # Crear y registrar el callback
        subscriber = Subscriber()
        subscriber_uri = daemon.register(subscriber)

        # Conectarse al servidor (usa el URI que imprime tu servidor)
        server = Proxy("PYRO:InsultService@localhost:4718")

        # Añadir insulto
        result = server.add_insult("asshole")
        print("Resultado al añadir insulto:", result)

        # Suscribirse al broadcasting
        server.subscribe(subscriber_uri)

        daemon.requestLoop()

if __name__ == "__main__":
    main()