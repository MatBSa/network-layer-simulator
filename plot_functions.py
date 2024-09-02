from camada_enlace import *
from camada_fisica import *
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

############################## plotar bits codificados ##############################


def plota_bits_codificados(bits_codificados, codificacao):
    # considera amplitudes de sinal +1/-1 para plotar, de digital 0/1 para sinal -v/v -> melhor de ler/representacao de simbolo eletrico
    simbolo = [1 if bit == 1 else 0 if bit == 0 else -1 for bit in bits_codificados]
    
    # steps/degraus com eixo com n faixas tanto quanto n bits que temos
    plt.figure(figsize=(20, 12))
    plt.title(f'Mensagem codificada em código {codificacao}')
    plt.step(np.arange(len(bits_codificados)), simbolo, where='post', linewidth=2)
    
    # linha em y=0 e linhas de grade
    plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='black')
    
    # marcacoes em y, rotulos e limites
    plt.yticks(ticks=[-1, 0, 1], labels=['-V', '0', 'V'])
    plt.ylim(-1.2, 1.2)
    
    # remove marcacoes de x
    plt.xticks([])
    plt.savefig('images/bits_codificados.png')
    

############################## plotar modulacoes ##############################


def plota_modulacoes(sinal, modulacao):
    if modulacao == '8qam':
        quantidade_simbolos = sinal[0]
        tempo_total = sinal[1]
        onda = sinal[2]
        
        # plot
        plt.figure(figsize=(20, 12))

        for i in range(quantidade_simbolos):
            plt.plot(tempo_total[i * 100: (i + 1) * 100],
                    np.real(onda[i * 100: (i + 1) * 100]), color='black')

        plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='black')
        plt.title('Modulação 8qam')
        plt.xlabel('t')
        plt.ylabel('A')
        plt.savefig('images/modulacao.png')
        
    else:
        t = np.arange(len(sinal))
        # plot 
        plt.figure(figsize=(20, 12))
        plt.title(f'Modulacao: {modulacao}')
        plt.step(t, sinal, where='post')
        plt.ylim([-1.5, 1.5])
        plt.grid(True)
        plt.show()
        plt.savefig('images/modulacao.png')


if __name__ == '__main__':
    binary_message = [1, 1, 0, 0, 0, 1, 1, 0, 1]
    sinal = modulacao_8qam(binary_message)
    plota_modulacoes(sinal, '8qam')
