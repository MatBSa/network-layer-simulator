from camada_fisica import ask, fsk, plot_signal
from camada_enlace import generate_parity, check_parity

def main():
    data = "1100101"  # Exemplo de dados binários

    #########Camada de enlace

    # Adicionando Paridade
    data_with_parity = generate_parity(data)
    print(f"Data with Parity: {data_with_parity}")
    
    # Verificando Paridade
    checked_data, parity_valid = check_parity(data_with_parity)
    print(f"Checked Data: {checked_data}, Parity Valid: {parity_valid}")

    #########Camada física
    
    # Modulação ASK
    ask_signal = ask(data)
    plot_signal(data, ask_signal, title="Amplitude Shift Keying (ASK)", filename="ask_signal.png")
    
    # Modulação FSK
    fsk_signal = fsk(data)
    plot_signal(data, fsk_signal, title="Frequency Shift Keying (FSK)", filename="fsk_signal.png")

if __name__ == "__main__":
    main()