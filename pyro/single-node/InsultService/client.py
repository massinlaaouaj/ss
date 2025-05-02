import Pyro4

def main():
    ns = Pyro4.locateNS()
    insult_service_server_uri = ns.lookup("InsultService")
    insult_service_server = Pyro4.Proxy(insult_service_server_uri)
    
    insult = "stupid"
    print("Insult to add:", insult)
    
    print("Connecting to the InsultService...")
    result = insult_service_server.add_insult(insult)
    print("✅", result)

if __name__ == "__main__":
    main()
