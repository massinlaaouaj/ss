import Pyro4
import redis

@Pyro4.behavior(instance_mode="single")
class InsultService:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    @Pyro4.expose
    def add_insult(self, insult):
        if not self.r.sismember("insults", insult):
            self.r.sadd("insults", insult)
            return "Insulto registrado: " + insult
        else:
            return "Insulto ya registrado"

    @Pyro4.expose
    def get_insults(self):
        return list(self.r.smembers("insults"))

def main():
    daemon = Pyro4.Daemon(port=4718)
    ns = Pyro4.locateNS()
    obj = InsultService()
    uri = daemon.register(obj, objectId="InsultService")
    ns.register("InsultService", uri)
    print(f"InsultService with URI {uri} in execution...")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
