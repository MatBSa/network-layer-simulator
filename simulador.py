from camada_fisica import ask, fsk, plot_signal
from camada_enlace import generate_parity, check_parity, generate_crc, check_crc

def main():
    data = "1100101"  # Exemplo de dados binários
    print(f"Original data:            {data}")

    #########Camada de enlace

    # Adicionando Paridade
    data_with_parity = generate_parity(data)
    print(f"Data with Parity:         {data_with_parity}")
    
    # Verificando Paridade
    checked_data, parity_valid = check_parity(data_with_parity)
    print(f"Checked Data:             {checked_data}, Parity Valid: {parity_valid}")

    ## Caso de erro do Bit de Paridade

    # Introduz erro no Bit de Paridade
    altered_data_with_parity = data_with_parity[:-1] + ("0" if data_with_parity[-1] == "1" else "1")
    print(f"Altered data with Parity: {altered_data_with_parity}")

    # Esperando erro na verificação
    checked_data, parity_valid = check_parity(altered_data_with_parity)
    print(f"Checked Data:             {checked_data}, Parity Valid: {parity_valid}\n")

    print(f"Original data:         {data}")
    
    # Adicionando CRC
    polynomial = "1101"  # Exemplo de polinômio
    data_with_crc = generate_crc(data, polynomial)
    print(f"Data with CRC:         {data_with_crc}")
    
    # Verificando CRC
    crc_valid = check_crc(data_with_crc, polynomial)
    print(f"CRC Valid:             {crc_valid}")

    ## Caso de erro do CRC

    # Introduz erro no CRC
    altered_data_with_crc = data_with_crc[:-1] + ("0" if data_with_crc[-1] == "1" else "1")
    print(f"Altered data with CRC: {altered_data_with_crc}")

    # Esperando erro na verificação
    crc_valid = check_crc(altered_data_with_crc, polynomial)
    print(f"CRC Valid:             {crc_valid}")


    #########Camada física
    
    # Modulação ASK
    ask_signal = ask(data)
    plot_signal(data, ask_signal, title="Amplitude Shift Keying (ASK)", filename="ask_signal.png")
    
    # Modulação FSK
    fsk_signal = fsk(data)
    plot_signal(data, fsk_signal, title="Frequency Shift Keying (FSK)", filename="fsk_signal.png")

if __name__ == "__main__":
    main()