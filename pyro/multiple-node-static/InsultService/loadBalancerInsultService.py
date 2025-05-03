import Pyro4

class RoundRobinBalanceadorInsult:
    def __init__(self, servicio_prefix):
        ns = Pyro4.locateNS()
        servicios = sorted(ns.list(prefix=servicio_prefix).keys())
        if not servicios:
            raise Exception("No se encontraron servicios con ese prefijo.")
        self.proxies = [Pyro4.Proxy(ns.lookup(name)) for name in servicios]
        self.total = len(self.proxies)
        self.i = 0

    def enviar(self, insulto):
        proxy = self.proxies[self.i]
        self.i = (self.i + 1) % self.total
        proxy.add_insult(insulto)
