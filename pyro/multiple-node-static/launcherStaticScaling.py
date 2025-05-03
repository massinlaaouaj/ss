import subprocess
import time
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def launch(name, command, wait_time=1):
    print(f"🚀 Iniciando: {name}")
    process = subprocess.Popen(command, shell=True)
    time.sleep(wait_time)
    return process

def main():
    processes = []

    try:
        # 0. Name Server
        processes.append(launch("NameServer", "pyro4-ns"))

        # 1. Redis
        processes.append(launch("Redis", f"python3 {BASE_DIR}/RedisServer.py"))

        # 2. Multiple instancias de InsultService
        number_instances_insult_service = 4
        base_port_insult = 49152
        for i in range(number_instances_insult_service):
            port = base_port_insult + i
            name = f"InsultService_{i}"
            cmd = f"python3 InsultService/server.py {port} {name}"
            processes.append(launch(name, cmd))

        # 3. Multiple instancias de InsultFilterService
        number_instances_insult_filter_service = 4
        base_port_filter = 50152
        for i in range(number_instances_insult_filter_service):
            port = base_port_filter + i
            name = f"InsultFilterService_{i}"
            cmd = f"python3 InsultFilterService/server.py {port} {name}"
            processes.append(launch(name, cmd))

        # 4. Notifier
        processes.append(launch("Notifier", f"python3 {BASE_DIR}/Notifier/notifier.py"))

        # 5. Subscriber
        processes.append(launch("Subscriber", f"python3 {BASE_DIR}/Notifier/subscriber.py"))

        # 6. Test InsultService
        processes.append(launch("Test InsultService", f"python3 {BASE_DIR}/InsultService/test_InsultService.py"))

        # 7. Test InsultFilterService
        processes.append(launch("Test InsultFilterService", f"python3 {BASE_DIR}/InsultFilterService/test_InsultFilterService.py"))

        print("✅ Todas las instancias están en ejecución.")
        print("🛑 Ctrl+C para detener todo.")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("🧹 Deteniendo process...")
        for p in processes:
            p.terminate()
        print("👋 Listo.")

if __name__ == "__main__":
    main()
