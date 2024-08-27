import numpy as np
import matplotlib.pyplot as plt


# bipolar nrz
def bipolar_nrz(binary_message):
    bipolar_nrz_msg = binary_message.copy()
    signal = False
    index = 0
    while index < len(bipolar_nrz_msg):
        current_bit = bipolar_nrz_msg[index]
        if current_bit == 1:
            if not signal:
                bipolar_nrz_msg[index] = 1
            else:
                bipolar_nrz_msg[index] = -1
            signal = not signal
        index += 1
    return bipolar_nrz_msg



# 'transmitter' sends a text message that must be converted into a binary array of bits

# 0) converts a string message to an array of bits 1/0 (based on ascii byte char representation)
def binary_conversor(message):
    binary_message = []
    message = message.encode('utf8')
    for char in message:                    # each char (ascii decimal)
        byte = format(char, '08b')          # ascii dec -> binary (byte) repr
        bit_list = [int(bit) for bit in byte]  
        binary_message.extend(bit_list)     # put all in a single list
        
    return binary_message


# 1) polar nrz digital modulation
# 0 becomes -1 (-Voltage) while 1 stands as 1 (+Voltage)
def polar_nrz(binary_message):
    return [bit if bit == 1 else -1 for bit in binary_message]


# 2) manchester digital modulation
# 2-bit signal representation
# 0 -> (-1, 1)
# 1 -> (1, -1)
def manchester(binary_message):
    manchester_code = {0: [0, 1], 1: [1, 0]}
    
    manchester_msg = []
    for bit in binary_message:
        manchester_msg.extend(manchester_code[bit])
    return manchester_msg


# 'receptor' receives a binary encoded message from the transmitter
def text_conversor(binary_message):
    binary_message = ''.join(str(bit) for bit in binary_message)
    bytes = [int(binary_message[i:i+8], 2) for i in range(0, len(binary_message), 8)]  # obtains separate bytes (8 to 8), specifying base 2 integers
    message = bytearray(bytes).decode('utf-8')
    
    return message


######################### Amplitude Shift Keying (ASK) #########################
def ask(carrier_freq, amplitude, binary_message, sampling_rate=100):  
    modulated_signal = np.zeros(len(binary_message) * sampling_rate, dtype=float)

    for i, bit in enumerate(binary_message):
        if bit == 1:
            for k in range(sampling_rate):
                modulated_signal[i * sampling_rate + k] = amplitude * np.sin(2 * np.pi * carrier_freq * k / sampling_rate)
        else:
            for k in range(sampling_rate):
                modulated_signal[i * sampling_rate + k] = 0

    return modulated_signal


######################### Frequency Shift Keying (FSK) #########################
def fsk(carrier_freq_0, carrier_freq_1, amplitude, binary_message, sampling_rate=100):
        modulated_signal = np.zeros(len(binary_message) * sampling_rate, dtype=float)

        for i, bit in enumerate(binary_message):
            if bit == 1:
                for k in range(sampling_rate):
                    modulated_signal[i * sampling_rate + k] = amplitude * np.sin(2 * np.pi * carrier_freq_0 * k / sampling_rate)
            else:
                for k in range(sampling_rate):
                    modulated_signal[i* sampling_rate + k] = amplitude * np.sin(2 * np.pi * carrier_freq_1 * k / sampling_rate)

        return modulated_signal
    
    
######################### 8QAM #########################
def modulacao_8qam(bits):
    while len(bits) % 3 != 0:
        bits.append(0)

    simbolos_bits = [tuple(bits[i:i + 3]) for i in range(0, len(bits), 3)]

    # Mapeamento para a constelação 8QAM
    constelacao = {
        (0, 0, 0): complex(-1, -1),
        (0, 0, 1): complex(-1, 1),
        (0, 1, 0): complex(1, -1),
        (0, 1, 1): complex(1, 1),
        (1, 0, 0): complex(-1, -3),
        (1, 0, 1): complex(-1, 3),
        (1, 1, 0): complex(1, -3),
        (1, 1, 1): complex(1, 3)
    }

    sinais_modulados = [constelacao[simbolo] for simbolo in simbolos_bits]
    duracao_sinal = 1 / 8

    quantidade_simbolos = len(sinais_modulados)
    tempo_sinal = np.linspace(0, duracao_sinal, 100)

    tempo_total = np.linspace(0, duracao_sinal * quantidade_simbolos, quantidade_simbolos * 100)
    onda = np.zeros(len(tempo_total), dtype=complex)

    for idx, sinal in enumerate(sinais_modulados):
        onda[idx * 100: (idx + 1) * 100] = sinal * np.exp(1j * 2 * np.pi * 8 * tempo_sinal)

    return quantidade_simbolos, tempo_total, onda
    



    