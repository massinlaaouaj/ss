class ClienteInsult:
    def __init__(self, balanceador):
        self.balanceador = balanceador

    def enviar_insultos(self, N):
        for i in range(N):
            insulto = f"insulto_{i}"
            self.balanceador.enviar(insulto)
