import threading
from camada_fisica import ask, fsk, plot_signal
from transmissor import transmissor
from receptor import receptor

# Constantes
DATA = "1100101"
PORT_TRANSMISSION = 8001
PORT_RECEPTION = 8002

def main():
    data = DATA
    use_crc = True  # Escolha entre CRC (True) e Paridade (False)
    modulation_type = "ASK"  # Escolha entre "ASK" e "FSK"

    receptor_thread = threading.Thread(target=receptor, args=(use_crc, PORT_RECEPTION))
    receptor_thread.start()

    transmissor(data, use_crc, PORT_TRANSMISSION)

    if modulation_type == "ASK":
        ask_signal = ask(data)
        plot_signal(data, ask_signal, title="Amplitude Shift Keying (ASK)", filename="ask_signal.png")
    elif modulation_type == "FSK":
        fsk_signal = fsk(data)
        plot_signal(data, fsk_signal, title="Frequency Shift Keying (FSK)", filename="fsk_signal.png")

if __name__ == "__main__":
    main()
