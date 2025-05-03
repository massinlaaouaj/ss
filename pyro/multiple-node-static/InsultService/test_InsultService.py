import time
from loadBalancerInsultService import RoundRobinBalanceadorInsult
from client import ClienteInsult

N = 1000

def main():
    balanceador = RoundRobinBalanceadorInsult("InsultService_")
    cliente = ClienteInsult(balanceador)

    print(f"🔁 Enviando {N} insultos a través del balanceador RoundRobin...")
    start = time.time()
    cliente.enviar_insultos(N)
    end = time.time()

    total_time = end - start
    throughput = N / total_time

    resultado = (
        f"TEST MODULAR: InsultService (RoundRobin)\n"
        f"Total instancias: {balanceador.total}\n"
        f"Total peticiones: {N}\n"
        f"Tiempo total: {total_time:.4f} segundos\n"
        f"Throughput combinado: {throughput:.2f} peticiones/segundo\n"
    )

    print(resultado)
    with open("resultados_scaling_insultservice.txt", "w") as f:
        f.write(resultado)

if __name__ == "__main__":
    main()
