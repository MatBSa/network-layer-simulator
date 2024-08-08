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
    t = np.linspace(0, len(data), len(signal), endpoin=False)
    plt.figure(figsize=(10,4))
    plt.plot(t,signal)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

#Exemplo de uso
bit_sequence = "110001101"
qam8_signal = qam8(bit_sequence)

plot_signal_8qam(bit_sequence, qam8_signal, title="8QAM Modulated Signal", filename="qam8_signal.png")
