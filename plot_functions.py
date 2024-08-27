from camada_enlace import *
from camada_fisica import *
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plota_bits_codificados(bits_codificados, codificacao):
    # considera amplitudes de sinal +1/-1 para plotar, de digital 0/1 para sinal -v/v -> melhor de ler/representacao de simbolo eletrico
    simbolo = [1 if bit == 1 else 0 if bit == 0 else -1 for bit in bits_codificados]
    
    # steps/degraus com eixo com n faixas tanto quanto n bits que temos
    plt.figure(figsize=(20, 12))
    plt.title(f'Mensagem codificada em código {codificacao}')
    plt.step(np.arange(len(bits_codificados)), simbolo, where='post', linewidth=2)
    # linha em y=0
    plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='black')
    # marcacoes em y, rotulos e limites
    plt.yticks(ticks=[-1, 0, 1], labels=['-V', '0', 'V'])
    plt.ylim(-1.2, 1.2)
    # remove marcacoes de x
    plt.xticks([])
    # centraliza em 0 eixo x
    plt.savefig('images/bits_codificados.png')

    
message = 'Hello World!'
binary_msg = binary_conversor(message)
print(binary_msg)
bits_codificados = manchester(binary_msg)
print(bits_codificados)

#print(binary_msg == [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])