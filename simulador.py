from camada_fisica import ask_transmit


def main():
    data = "1100101"  # Exemplo de dados binários
    
    # Modulação ASK
    ask_signal = ask_transmit(data)

if __name__ == "__main__":
    main()