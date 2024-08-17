import numpy as np
import matplotlib.pyplot as plt

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

def plot_signal(data, signal, title="Signal", filename="signal.png"):
    t = np.linspace(0, len(data), len(signal), endpoint=False)
    plt.figure(figsize=(10, 4))
    plt.plot(t, signal)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
