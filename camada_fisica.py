import numpy as np

######################### Amplitude Shift Keying (ASK) #########################
def ask_transmit(data, carrier_frequency=10, sampling_rate=100, amplitude_1=1, amplitude_0=0.5):
    """
    Modulação ASK para transmissão.

    Args:
    data (str): Sequência de bits a serem modulados.
    carrier_frequency (int): Frequência da portadora em Hz.
    sampling_rate (int): Taxa de amostragem em Hz.
    amplitude_1 (float): Amplitude para bit 1.
    amplitude_0 (float): Amplitude para bit 0.

    Returns:
    np.array: Sinal modulado.
    """
    t = np.linspace(0, len(data), len(data) * sampling_rate, endpoint=False)
    carrier = np.sin(2 * np.pi * carrier_frequency * t)
    modulated_signal = np.zeros(len(t))
    
    for i, bit in enumerate(data):
        if bit == '1':
            modulated_signal[i * sampling_rate:(i + 1) * sampling_rate] = amplitude_1 * carrier[i * sampling_rate:(i + 1) * sampling_rate]
        else:
            modulated_signal[i * sampling_rate:(i + 1) * sampling_rate] = amplitude_0 * carrier[i * sampling_rate:(i + 1) * sampling_rate]
    
    return modulated_signal

def ask_receive(modulated_signal, carrier_frequency=10, sampling_rate=100, amplitude_threshold=0.75):
    """
    Demodulação ASK para recepção.

    Args:
    modulated_signal (np.array): Sinal modulado recebido.
    carrier_frequency (int): Frequência da portadora em Hz.
    sampling_rate (int): Taxa de amostragem em Hz.
    amplitude_threshold (float): Amplitude mínima para considerar bit 1.

    Returns:
    str: Sequência de bits demodulada.
    """
    t = np.linspace(0, len(modulated_signal) / sampling_rate, len(modulated_signal), endpoint=False)
    carrier = np.sin(2 * np.pi * carrier_frequency * t)
    demodulated_bits = []
    
    for i in range(0, len(modulated_signal), sampling_rate):
        segment = modulated_signal[i:i + sampling_rate] * carrier[i:i + sampling_rate]
        amplitude = np.mean(segment)
        if amplitude > amplitude_threshold:
            demodulated_bits.append('1')
        else:
            demodulated_bits.append('0')
    
    return ''.join(demodulated_bits)

######################### Frequency Shift Keying (FSK) #########################

def fsk_transmit(data, carrier_frequency_0=10, carrier_frequency_1=20, sampling_rate=100):
    """
    Modulação FSK para transmissão.

    Args:
    data (str): Sequência de bits a serem modulados.
    carrier_frequency_0 (int): Frequência da portadora para bit 0 em Hz.
    carrier_frequency_1 (int): Frequência da portadora para bit 1 em Hz.
    sampling_rate (int): Taxa de amostragem em Hz.

    Returns:
    np.array: Sinal modulado.
    """
    t = np.linspace(0, len(data), len(data) * sampling_rate, endpoint=False)
    modulated_signal = np.zeros(len(t))
    
    for i, bit in enumerate(data):
        if bit == '1':
            carrier = np.sin(2 * np.pi * carrier_frequency_1 * t[i * sampling_rate:(i + 1) * sampling_rate])
        else:
            carrier = np.sin(2 * np.pi * carrier_frequency_0 * t[i * sampling_rate:(i + 1) * sampling_rate])
        modulated_signal[i * sampling_rate:(i + 1) * sampling_rate] = carrier
    
    return modulated_signal