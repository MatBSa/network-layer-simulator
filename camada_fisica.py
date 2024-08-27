############################## imports ##############################
import numpy as np
import matplotlib.pyplot as plt


############################## camada fisica ##############################


############################## transmissor ##############################


############################## codificacao ##############################


# codificacao: nrz bipolar
# 0 -> 0
# 1 alternando entre 1 e -1
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


# converte uma mensagem de texto em uma lista de bits inteiros
# codifica com utf8 levando em conta a acentuacao
# converte para binario cada char em decimal codificado
# retorna uma lista de bits, adicionando cada lista de cada byte corresp. a cada char
def binary_conversor(message):
    binary_message = []
    message = message.encode('utf8')
    for char in message:                   
        byte = format(char, '08b')          
        bit_list = [int(bit) for bit in byte]  
        binary_message.extend(bit_list)     
    return binary_message


# nrz polar
# 0 -> -1 (-V)
# 1 -> 1 (+V)
def polar_nrz(binary_message):
    return [bit if bit == 1 else -1 for bit in binary_message]


# manchester -> representacao em pares de dois bits
# 0 -> (-1, 1)
# 1 -> (1, -1)
def manchester(binary_message):
    manchester_code = {0: [0, 1], 1: [1, 0]}
    manchester_msg = []
    for bit in binary_message:
        manchester_msg.extend(manchester_code[bit])
    return manchester_msg


############################## modulacao portadora ##############################

# modulacao ask
# amostra o sinal a uma taxa de 100 (100 amostras da onda gerada no grafico)
# se o bit for 1 -> senoide modulada com a amplitude e a frequencia passada
# se o bit for 0 -> sem onda (0)
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


# modulacao fsk
# bit 1 -> senoide modulada com frequencia carrier_freq_1
# bit 0 -> senoide modulada com frequencia carrier_freq_0
# taxa de amostragem de 100 -> 100 pontos das senoides por cada bit
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
     
    
# modulacao 8qam 
# combinacao amplitude e fase -> 8 estados diferentes
# 3 bits por simbolo eletrico
# cada estado (combinacao de 3 bits)/simbolo e mapeado na constelacao 8qam
def modulacao_8qam(bits):
    while len(bits) % 3 != 0:
        bits.append(0)

    # garante que bits sera um array de inteiros
    bits = [int(bit) for bit in bits]
    simbolos_bits = [tuple(bits[i:i + 3]) for i in range(0, len(bits), 3)]

    # mapeamento para a constelação 8QAM
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

############################## receptor ##############################


# converte uma mensagem binaria recebida pelo transmissor em texto
def text_conversor(binary_message):
    binary_message = ''.join(str(bit) for bit in binary_message)
    bytes = [int(binary_message[i:i+8], 2) for i in range(0, len(binary_message), 8)]  # obtem bytes isolados (8 em 8), convertendo em inteiro base 2
    message = bytearray(bytes).decode('utf-8')                                         # decodifica os inteiros base 2 em chars novamente 
    return message
    



    