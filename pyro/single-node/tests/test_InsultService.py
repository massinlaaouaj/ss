import Pyro4
import time

N = 1000

def main():
    ns = Pyro4.locateNS()
    insult_service_server_uri = ns.lookup("InsultService")
    insult_service_server = Pyro4.Proxy(insult_service_server_uri)

    print(f" Enviando {N} insultos al servicio InsultService (Pyro4)...")

    start = time.time()
    for i in range(N):
        insult = f"insulto_{i}"
        insult_service_server.add_insult(insult)
    end = time.time()

    total_time = end - start
    throughput = N / total_time

    print(f" Tiempo total: {total_time:.4f} segundos")
    print(f" Throughput: {throughput:.2f} peticiones/segundo")

if __name__ == "__main__":
    main()
