from camada_fisica import ask_transmit, ask_receive


def main():
    data = "1100101"  # Exemplo de dados binários
    
    # Modulação ASK
    ask_signal = ask_transmit(data)
    demodulated_ask = ask_receive(ask_signal)
    print(f"ASK Demodulated Data: {demodulated_ask}")

    # Modulação FSK
    fsk_signal = fsk_transmit(data)

if __name__ == "__main__":
    main()