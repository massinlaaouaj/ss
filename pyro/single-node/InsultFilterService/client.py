import Pyro4

def main():
    print("Conectando al InsultFilterService...")
    uri = "PYRO:InsultFilterService@localhost:4040"
    filter_service = Pyro4.Proxy(uri)

    text = "Realmente eres un stupid"
    print("Texto a filtrar:", text)
    if text:    
        result = filter_service.add_text(text)
        print("📤 Resultado:", result)


if __name__ == "__main__":
    main()
