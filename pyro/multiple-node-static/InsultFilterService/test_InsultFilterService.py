import time
from loadBalancerInsultFilterService import RoundRobinBalanceadorFilter
from client import ClienteFilter

N = 1000

def main():
    balanceador = RoundRobinBalanceadorFilter("InsultFilterService_")
    cliente = ClienteFilter(balanceador)

    print(f"🔁 Enviando {N} textos a través del balanceador RoundRobin...")
    start = time.time()
    cliente.enviar_textos(N)
    end = time.time()

    total_time = end - start
    throughput = N / total_time

    resultado = (
        f"TEST MODULAR: InsultFilterService (RoundRobin)\n"
        f"Total instancias: {balanceador.total}\n"
        f"Total peticiones: {N}\n"
        f"Tiempo total: {total_time:.4f} segundos\n"
        f"Throughput combinado: {throughput:.2f} peticiones/segundo\n"
    )

    print(resultado)
    with open("resultados_scaling_insultfilterservice.txt", "w") as f:
        f.write(resultado)

if __name__ == "__main__":
    main()
