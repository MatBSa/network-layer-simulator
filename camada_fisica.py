import numpy as np

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