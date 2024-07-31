import matplotlib.pyplot as plt
import numpy as np

class Modu_8QAM:
    def __init__(self):
        self.tax_modul = 8
        self.tax_transm = 24
    
    def modulac_8QAM(self,bits):
        while len(bits) % 3 != 0:
            bits = np.append(bits,0)

        bits_simbol = [tuple(bits[i:i +3]) for i in range(0, len(bits), 3)]

        #Configuração para o 8QAM
        mapa = {
            (0, 0, 0): complex(-1, -1),
            (0, 0, 1): complex(-1, 1),
            (0, 1, 0): complex(1, -1),
            (0, 1, 1): complex(1, 1),
            (1, 0, 0): complex(-1, -3),
            (1, 0, 1): complex(-1, 3),
            (1, 1, 0): complex(1, -3),
            (1, 1, 1): complex(1, 3)
        }
        simb_modul = [mapa[bits] for bits in bits_simbol]
        
        return simb_modul
    def band_base_8qam(self, simb_modul):
        durac_simbol = 1/ self.tax_modul

        num_simbol = len(simb_modul)
        time_simbol = np.linspace(0, durac_simbol, 100)

        time_total = np.linspace(
            0, durac_simbol* num_simbol, num_simbol * 100)
        make_wave = np.zeros(len(time_total), dtype= complex)

        for i, simbol in enumerate(simb_modul):
            make_wave[i * 100: (i+1) * 100] = simbol * np.exp(1j*2*np.pi*self.tax_modul*time_simbol)
        
        num_bauds = len(simb_modul)
        baud_duracao = 1/ self.tax_transm
        time_total = np.linspace(0, baud_duracao * num_bauds, num_bauds*100)
        return num_bauds, time_total, make_wave
    
    def run(self, bits):
        simbol_modul = self.modulac_8QAM(bits)
        num_bauds, time, signal_bbase = self.band_base_8qam(simbol_modul)

        return num_bauds, time, signal_bbase

if __name__ == '__main__':
    modulador = Modu_8QAM()
    bits = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1,
            0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
    
    balds, tempo, signal_bbase = modulador.run(bits)
