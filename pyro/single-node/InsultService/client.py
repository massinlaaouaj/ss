import Pyro4
import random

def main():
    ns = Pyro4.locateNS()
    insult_service_server_uri = ns.lookup("InsultService")
    insult_service_server = Pyro4.Proxy(insult_service_server_uri)
    
    insults = [
        "idiot", "moron", "jerk", "loser", "dumbass", "numbskull",
        "nitwit", "clown", "blockhead", "twit", "doofus", "airhead"
    ]

    def get_random_insult():
        insult = random.choice(insults)
        print("Insulto:", insult)
        return insult
    
    print("Connecting to the InsultService...")
    result = insult_service_server.add_insult(get_random_insult())
    print("✅", result)

if __name__ == "__main__":
    main()
