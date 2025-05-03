import subprocess
import time

def lanzar(nombre, comando, espera=1):
    print(f"🚀 Iniciando: {nombre}")
    proceso = subprocess.Popen(comando, shell=True)
    time.sleep(espera)
    return proceso

def main():
    procesos = []

    try:
        # Lanzar múltiples instancias de InsultService
        num_instancias_insult = 4
        base_port_insult = 4800
        for i in range(num_instancias_insult):
            port = base_port_insult + i
            nombre = f"InsultService_{i}"
            cmd = f"python3 InsultService/server.py {port} {nombre}"
            procesos.append(lanzar(nombre, cmd))

        # Lanzar múltiples instancias de InsultFilterService
        num_instancias_filter = 4
        base_port_filter = 4900
        for i in range(num_instancias_filter):
            port = base_port_filter + i
            nombre = f"InsultFilterService_{i}"
            cmd = f"python3 InsultFilterService/server.py {port} {nombre}"
            procesos.append(lanzar(nombre, cmd))

        print("✅ Todas las instancias están en ejecución.")
        print("🛑 Ctrl+C para detener todo.")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("🧹 Deteniendo procesos...")
        for p in procesos:
            p.terminate()
        print("👋 Listo.")

if __name__ == "__main__":
    main()
