class ClienteFilter:
    def __init__(self, balanceador):
        self.balanceador = balanceador

    def enviar_textos(self, N):
        for i in range(N):
            texto = f"este texto contiene insulto_{i}"
            self.balanceador.enviar(texto)
