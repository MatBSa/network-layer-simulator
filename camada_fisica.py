import numpy as np
import matplotlib.pyplot as plt

def qam8(bit_array, carrier_frequency=10, sampling_rate=100):
    """
    Implementação da modulação 8QAM.
    
    Args:
    bit_array (str): Sequência de bits a serem modulados. Deve ter um comprimento múltiplo de 3.
    carrier_frequency (int): Frequência da portadora em Hz.
    sampling_rate (int): Taxa de amostragem em Hz.
    
    Returns:
    np.array: Sinal modulado.
    """
    if len(bit_array) % 3 != 0:
        raise ValueError("O comprimento da sequência de bits deve ser múltiplo de 3")
    
    #Mapeamento de bits para simbolos 8QAM (I + jQ): onde I é a componente em fase e Q é a componente em quadratura
    bit_to_symbol = { 
        '000':(1 + 1j),
        '001':(1 - 1j),
        '010':(-1 + 1j),
        '011':(-1 - 1j),
        '100':(1 + 3j),
        '101':(1 - 3j),
        '110':(-1 + 3j),
        '111':(-1 - 3j)
    }
    t = np.linspace(0, len(bit_array)//3, len(bit_array) // 3 * sampling_rate,endpoint=False)
    carrier_cos = np.cos(2 * np.pi * carrier_frequency * t) # onda cossenoidal que representa a portadora para a compenente em fase 'I'
    carrier_sin = np.sin(2 * np.pi * carrier_frequency * t) # onda senoidal que representa a portadora para a componente em quadratura 'Q'
    modulated_signal = np.zeros(len(t))

    for i in range(0, len(bit_array), 3):
        bits = bit_array[i:i+3]
        symbol = bit_to_symbol[bits]

        I = symbol.real
        Q = symbol.imag

        modulated_signal[i//3*sampling_rate:(i//3+1)*sampling_rate] = I * carrier_cos[i//3*sampling_rate:(i//3+1) *sampling_rate] + Q * carrier_sin[i // 3 * sampling_rate:(i//3+1) * sampling_rate]

    return modulated_signal

# Função para plotar o sinal 
def plot_signal_8qam(data, signal, title='Signal', filename = 'signal.png'):
    t = np.linspace(0, len(data), len(signal), endpoint=False)
    plt.figure(figsize=(10,4))
    plt.plot(t,signal)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.savefig(filename)
    plt.close()


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
def ask(bit_array, carrier_frequency=10, sampling_rate=100, amplitude_1=1, amplitude_0=0.5):
    t = np.linspace(0, len(bit_array), len(bit_array) * sampling_rate, endpoint=False)
    carrier = np.sin(2 * np.pi * carrier_frequency * t)
    modulated_signal = np.zeros(len(t))
    
    for i, bit in enumerate(bit_array):
        if bit == '1':
            modulated_signal[i * sampling_rate:(i + 1) * sampling_rate] = amplitude_1 * carrier[i * sampling_rate:(i + 1) * sampling_rate]
        else:
            modulated_signal[i * sampling_rate:(i + 1) * sampling_rate] = amplitude_0 * carrier[i * sampling_rate:(i + 1) * sampling_rate]
    
    return modulated_signal

######################### Frequency Shift Keying (FSK) #########################
def fsk(bit_array, carrier_frequency_0=10, carrier_frequency_1=20, sampling_rate=100):
    t = np.linspace(0, len(bit_array), len(bit_array) * sampling_rate, endpoint=False)
    modulated_signal = np.zeros(len(t))
    
    for i, bit in enumerate(bit_array):
        if bit == '1':
            carrier = np.sin(2 * np.pi * carrier_frequency_1 * t[i * sampling_rate:(i + 1) * sampling_rate])
        else:
            carrier = np.sin(2 * np.pi * carrier_frequency_0 * t[i * sampling_rate:(i + 1) * sampling_rate])
        modulated_signal[i * sampling_rate:(i + 1) * sampling_rate] = carrier
    
    return modulated_signal


