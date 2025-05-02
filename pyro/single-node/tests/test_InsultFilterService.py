import Pyro4
import time

N = 1000  # número de textos a filtrar

def main():
    ns = Pyro4.locateNS()
    insult_filter_service_server_uri = ns.lookup("InsultService")
    insult_filter_server = Pyro4.Proxy(insult_filter_service_server_uri)

    print(f" Enviando {N} textos al servicio InsultFilterService (Pyro4)...")

    start = time.time()
    for i in range(N):
        texto = f"este texto contiene insulto_{i}"
        insult_filter_server.add_text(texto)
    end = time.time()

    total_time = end - start
    throughput = N / total_time

    print(f" Tiempo total: {total_time:.4f} segundos")
    print(f" Throughput: {throughput:.2f} peticiones/segundo")

if __name__ == "__main__":
    main()
