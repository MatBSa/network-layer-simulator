from camada_fisica import ask, fsk, plot_signal
from camada_enlace import generate_parity, check_parity, generate_crc, check_crc

def main():
    data = "1100101"  # Exemplo de dados binários

    #########Camada de enlace

    # Adicionando Paridade
    data_with_parity = generate_parity(data)
    print(f"Data with Parity: {data_with_parity}")
    
    # Verificando Paridade
    checked_data, parity_valid = check_parity(data_with_parity)
    print(f"Checked Data: {checked_data}, Parity Valid: {parity_valid}")
    
    # Adicionando CRC
    polynomial = "1101"  # Exemplo de polinômio
    data_with_crc = generate_crc(data, polynomial)
    print(f"Data with CRC: {data_with_crc}")
    
    # Verificando CRC
    crc_valid = check_crc(data_with_crc, polynomial)
    print(f"CRC Valid: {crc_valid}")

    #########Camada física
    
    # Modulação ASK
    ask_signal = ask(data)
    plot_signal(data, ask_signal, title="Amplitude Shift Keying (ASK)", filename="ask_signal.png")
    
    # Modulação FSK
    fsk_signal = fsk(data)
    plot_signal(data, fsk_signal, title="Frequency Shift Keying (FSK)", filename="fsk_signal.png")

if __name__ == "__main__":
    main()