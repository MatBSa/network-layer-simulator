from camada_fisica import ask, fsk, plot_signal

def main():
    data = "1100101"  # Exemplo de dados binários
    
    # Modulação ASK
    ask_signal = ask(data)
    plot_signal(data, ask_signal, title="Amplitude Shift Keying (ASK)", filename="ask_signal.png")
    
    # Modulação FSK
    fsk_signal = fsk(data)
    plot_signal(data, fsk_signal, title="Frequency Shift Keying (FSK)", filename="fsk_signal.png")

if __name__ == "__main__":
    main()