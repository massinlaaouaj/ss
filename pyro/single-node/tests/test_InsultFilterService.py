import Pyro4
import time

N = 1000  # número de textos a filtrar

def main():
    print(f" Enviando {N} textos al servicio InsultFilterService (Pyro4)...")
    proxy = Pyro4.Proxy("PYRONAME:InsultFilterService")

    start = time.time()
    for i in range(N):
        texto = f"este texto contiene insulto_{i}"
        proxy.add_text(texto)
    end = time.time()

    total_time = end - start
    throughput = N / total_time

    print(f" Tiempo total: {total_time:.4f} segundos")
    print(f" Throughput: {throughput:.2f} peticiones/segundo")

if __name__ == "__main__":
    main()
