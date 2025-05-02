import Pyro4
import redis

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
    def add_text(self, string):
        text_filtered = self.filter_text(string)
        if not self.r.sismember("filtered_texts", text_filtered):
            self.r.sadd("filtered_texts", text_filtered)
            return "Texto registrado: " + text_filtered
        else:
            return "Cadena ya se encontraba registrada"

    @Pyro4.expose
    def get_texts(self):
        return list(self.r.smembers("filtered_texts"))

def main():
    daemon = Pyro4.Daemon(port=4040)
    obj = InsultFilterService()
    uri = daemon.register(obj, objectId="InsultFilterService")
    print(f"InsultFilterService with URI: {uri} in execution...")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
